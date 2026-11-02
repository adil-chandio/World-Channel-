#!/usr/bin/env python3
"""Build a 9:16 Short (1080x1920) from clips + burned captions.

Usage:
    python3 tools/render_shorts.py pipeline/produce/SHORT-01/edl.json [--out output/SHORT-01.mp4]
                                   [--skip-rights-check]

EDL schema:
{
  "id": "SHORT-01",
  "segments": [
    {"src": "media/clips/x.mp4", "in": 12.0, "out": 19.5, "clip_gain": 1.0}
  ],
  "captions": [
    {"text": "He came back FOUR times", "start": 0.4, "dur": 2.4}
  ],
  "end_cta": {"text": "FULL STORY ON MONARCH CAM", "dur": 1.4},
  "music": null, "music_gain": 0.15
}
Caption times are global (relative to the final timeline, before the end CTA card).
Clips must be cleared in ops/rights-ledger.csv.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vidlib import (REPO, assert_cleared, ffmpeg_exe, make_card, make_caption,
                    probe_duration, run)  # noqa: E402

W, H = 1080, 1920
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30,format=yuv420p"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("edl")
    ap.add_argument("--out", default=None)
    ap.add_argument("--skip-rights-check", action="store_true",
                    help="ONLY for owned/test footage")
    args = ap.parse_args()

    edl_path = Path(args.edl).resolve()
    edl = json.loads(edl_path.read_text(encoding="utf-8"))
    vid_id = edl.get("id", "SHORT")
    work = edl_path.parent / "_render_shorts"
    work.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.out) if args.out else REPO / "output" / f"{vid_id}.mp4"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[render_shorts] {vid_id} → {out_path}")
    parts: list[Path] = []
    for i, seg in enumerate(edl["segments"]):
        src = seg["src"]
        assert_cleared(src, args.skip_rights_check)
        in_s, out_s = float(seg["in"]), float(seg["out"])
        dur = out_s - in_s
        gain = float(seg.get("clip_gain", 1.0))
        sp = work / f"seg_{i:03d}.mp4"
        print(f"  [{i:03d}] {src} {in_s}→{out_s}")
        run([ffmpeg_exe(), "-y", "-ss", f"{in_s}", "-t", f"{dur}", "-i", str(REPO / src),
             "-filter_complex", f"[0:v]{FILL}[v];[0:a]volume={gain}[a]",
             "-map", "[v]", "-map", "[a]"] + ENC + ["-t", f"{dur}", str(sp)], quiet=True)
        parts.append(sp)

    cta = edl.get("end_cta")
    if cta:
        card = work / "cta.png"
        make_card(card, cta.get("text", "FULL STORY ON MONARCH CAM"), sub="",
                  footer="", size=(W, H))
        cdur = float(cta.get("dur", 1.4))
        sp = work / "cta.mp4"
        run([ffmpeg_exe(), "-y", "-loop", "1", "-t", f"{cdur}", "-i", str(card),
             "-f", "lavfi", "-t", f"{cdur}", "-i", "anullsrc=r=48000:cl=stereo",
             "-filter_complex", "[0:v]fps=30,format=yuv420p[v]",
             "-map", "[v]", "-map", "1:a"] + ENC + ["-t", f"{cdur}", str(sp)], quiet=True)
        parts.append(sp)

    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
    concat = work / "concat.mp4"
    run([ffmpeg_exe(), "-y", "-f", "concat", "-safe", "0", "-i", str(lst)] + ENC +
        [str(concat)], quiet=True)

    caps = edl.get("captions", [])
    cur = concat
    if caps:
        print(f"  burning {len(caps)} captions...")
        cmd = [ffmpeg_exe(), "-y", "-i", str(concat)]
        fc_parts, prev = [], "0:v"
        for i, c in enumerate(caps):
            png = work / f"cap_{i:03d}.png"
            make_caption(png, c["text"], size=(W, H), y_frac=0.30, font_size=76)
            cmd += ["-i", str(png)]
            s = float(c["start"])
            e = s + float(c["dur"])
            lbl = f"v{i}"
            fc_parts.append(f"[{prev}][{i + 1}:v]overlay=0:0:enable='between(t,{s},{e})'[{lbl}]")
            prev = lbl
        cmd += ["-filter_complex", ";".join(fc_parts), "-map", f"[{prev}]", "-map", "0:a"] + \
               ENC + [str(work / "captioned.mp4")]
        run(cmd, quiet=True)
        cur = work / "captioned.mp4"

    music = edl.get("music")
    vo = edl.get("vo")
    vo_gain = float(edl.get("vo_gain", 1.0))
    if music or vo:
        print("  mixing audio bed..." + (" + VO" if vo else ""))
        cmd = [ffmpeg_exe(), "-y", "-i", str(cur)]
        fc_in, fc_mids = "[0:a]", []
        n = 1
        if music:
            cmd += ["-stream_loop", "-1", "-i", str(REPO / music)]
            mg = float(edl.get("music_gain", 0.15))
            fc_mids.append(f"[{n}:a]volume={mg}[m]")
            fc_in += "[m]"
            n += 1
        if vo:
            cmd += ["-i", str(REPO / vo)]
            fc_mids.append(f"[{n}:a]volume={vo_gain}[v]")
            fc_in += "[v]"
            n += 1
        inputs = 1 + (1 if music else 0) + (1 if vo else 0)
        fc_mids.append(f"{fc_in}amix=inputs={inputs}:duration=first:normalize=0[a]")
        cmd += ["-filter_complex", ";".join(fc_mids), "-map", "0:v", "-map", "[a]"] + \
               ENC + [str(out_path)]
        run(cmd, quiet=True)
    else:
        run([ffmpeg_exe(), "-y", "-i", str(cur), "-c", "copy", str(out_path)], quiet=True)

    dur = probe_duration(out_path)
    print(f"[render_shorts] DONE: {out_path}  ({dur:.1f}s)")


if __name__ == "__main__":
    main()
