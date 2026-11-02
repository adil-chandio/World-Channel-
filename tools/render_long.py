#!/usr/bin/env python3
"""Assemble a long-form (1920x1080) commentary video from an EDL + per-segment VO.

Usage:
    python3 tools/render_long.py pipeline/produce/BRIEF-01/edl.json [--out output/BRIEF-01_long.mp4]
                                 [--skip-rights-check]

EDL schema (see tools/README.md for details):
{
  "id": "BRIEF-01",
  "title": "...",
  "music": null | "path.mp3",
  "music_gain": 0.05,
  "segments": [
    {"type": "card",    "text": "HE CAME BACK", "sub": "...", "duration": 2.0},
    {"type": "clip",    "src": "media/clips/x.mp4", "in": 3.0, "out": 9.5,
     "clip_gain": 0.2, "vo": "pipeline/produce/BRIEF-01/vo/seg01.mp3",
     "caption": "optional text", "caption_start": 0.5, "caption_dur": 2.5},
    {"type": "endcard", "text": "WATCH NEXT: ...", "vo": "...", "duration": 20.0}
  ]
}
Caption times are segment-local. Clips must be cleared in ops/rights-ledger.csv.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vidlib import (REPO, assert_cleared, ffmpeg_exe, make_card, make_caption,
                    probe_duration, run)  # noqa: E402

ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
       "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]


def clip_vf(w: int, h: int) -> str:
    return (f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p")


def render_clip_segment(seg: dict, out: Path, w: int, h: int, work: Path, idx: int,
                        skip_rights: bool) -> None:
    src = seg["src"]
    assert_cleared(src, skip_rights)
    in_s, out_s = float(seg["in"]), float(seg["out"])
    dur = out_s - in_s
    if dur <= 0:
        raise SystemExit(f"segment {idx}: out must be > in")
    gain = float(seg.get("clip_gain", 0.2))
    vo = seg.get("vo")
    cap = seg.get("caption")

    cmd = [ffmpeg_exe(), "-y", "-ss", f"{in_s}", "-t", f"{dur}", "-i", str(REPO / src)]
    inputs = 1
    vo_idx = cap_idx = None
    if vo:
        vo_path = REPO / vo
        vo_dur = probe_duration(vo_path)
        if vo_dur > dur + 0.15:
            print(f"  warn seg {idx}: VO {vo_dur:.1f}s longer than window {dur:.1f}s — trimmed")
        cmd += ["-t", f"{dur}", "-i", str(vo_path)]
        vo_idx = inputs
        inputs += 1
    if cap:
        cap_png = work / f"cap_{idx:03d}.png"
        make_caption(cap_png, cap, size=(w, h))
        cmd += ["-i", str(cap_png)]
        cap_idx = inputs
        inputs += 1

    if cap_idx is not None:
        cs = float(seg.get("caption_start", 0.3))
        cd = float(seg.get("caption_dur", 3.0))
        fc = (f"[0:v]{clip_vf(w, h)}[v0];"
              f"[v0][{cap_idx}:v]overlay=0:0:enable='between(t,{cs},{cs + cd})'[v];")
        vmap = "[v]"
    else:
        fc = ""
        vmap = "0:v"

    if vo_idx is not None:
        fc += (f"[0:a]volume={gain}[ca];[ca][{vo_idx}:a]"
               f"amix=inputs=2:duration=first:normalize=0[a]")
    else:
        fc += f"[0:a]volume={gain}[a]"
    amap = "[a]"

    cmd += ["-filter_complex", fc, "-map", vmap, "-map", amap] + ENC + \
           ["-t", f"{dur}", str(out)]
    run(cmd, quiet=True)


def render_card_segment(seg: dict, out: Path, w: int, h: int, work: Path, idx: int) -> None:
    dur = float(seg.get("duration", 2.0))
    text = seg.get("text", "")
    card = work / f"card_{idx:03d}.png"
    make_card(card, text, sub=seg.get("sub", ""), footer=seg.get("footer", "MONARCH CAM"),
              size=(w, h))
    vo = seg.get("vo")
    cmd = [ffmpeg_exe(), "-y", "-loop", "1", "-t", f"{dur}", "-i", str(card)]
    if vo:
        cmd += ["-t", f"{dur}", "-i", str(REPO / vo),
                "-f", "lavfi", "-t", f"{dur}", "-i", "anullsrc=r=48000:cl=stereo",
                "-filter_complex", f"[0:v]fps=30,format=yuv420p[v];"
                                   f"[1:a][2:a]amix=inputs=2:duration=first:normalize=0[a]",
                "-map", "[v]", "-map", "[a]"]
    else:
        cmd += ["-f", "lavfi", "-t", f"{dur}", "-i", "anullsrc=r=48000:cl=stereo",
                "-filter_complex", "[0:v]fps=30,format=yuv420p[v]",
                "-map", "[v]", "-map", "1:a"]
    cmd += ENC + ["-t", f"{dur}", str(out)]
    run(cmd, quiet=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("edl", help="path to edl.json")
    ap.add_argument("--out", default=None, help="output mp4 (default output/<id>_long.mp4)")
    ap.add_argument("--skip-rights-check", action="store_true",
                    help="ONLY for owned/test footage")
    args = ap.parse_args()

    edl_path = Path(args.edl).resolve()
    edl = json.loads(edl_path.read_text(encoding="utf-8"))
    w = int(edl.get("width", 1920))
    h = int(edl.get("height", 1080))
    vid_id = edl.get("id", "VIDEO")
    work = edl_path.parent / "_render"
    work.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.out) if args.out else REPO / "output" / f"{vid_id}_long.mp4"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    segs = edl["segments"]
    print(f"[render_long] {vid_id}: {len(segs)} segments → {out_path}")
    rendered: list[Path] = []
    for i, seg in enumerate(segs):
        stype = seg.get("type", "clip")
        sp = work / f"seg_{i:03d}.mp4"
        if stype in ("card", "endcard"):
            print(f"  [{i:03d}] {stype}: {seg.get('text', '')[:60]}")
            render_card_segment(seg, sp, w, h, work, i)
        else:
            print(f"  [{i:03d}] clip {seg['src']}  {seg['in']}→{seg['out']}")
            render_clip_segment(seg, sp, w, h, work, i, args.skip_rights_check)
        rendered.append(sp)

    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in rendered), encoding="utf-8")
    pre = work / "pre_master.mp4"
    print("  concatenating...")
    run([ffmpeg_exe(), "-y", "-f", "concat", "-safe", "0", "-i", str(lst)] + ENC +
        [str(pre)], quiet=True)

    music = edl.get("music")
    final_src = pre
    if music:
        mg = float(edl.get("music_gain", 0.05))
        print("  mixing music bed...")
        run([ffmpeg_exe(), "-y", "-i", str(pre), "-stream_loop", "-1", "-i", str(REPO / music),
             "-filter_complex",
             f"[1:a]volume={mg}[m];[0:a][m]amix=inputs=2:duration=first:normalize=0[a]",
             "-map", "0:v", "-map", "[a]"] + ENC + [str(out_path)], quiet=True)
    else:
        run([ffmpeg_exe(), "-y", "-i", str(pre), "-c", "copy", str(out_path)], quiet=True)

    dur = probe_duration(out_path)
    print(f"[render_long] DONE: {out_path}  ({dur:.1f}s ≈ {dur / 60:.1f} min)")


if __name__ == "__main__":
    main()
