#!/usr/bin/env python3
"""Extract frames from a clip for forensic study.

Usage:
    python3 tools/extract_frames.py media/inbox/clip.mp4 --every 2.0 --out pipeline/forensics/frames/CLIP-001
    python3 tools/extract_frames.py media/inbox/clip.mp4 --at 1.5,3.2,7.0 --out pipeline/forensics/frames/CLIP-001
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vidlib import ffmpeg_exe, probe_duration, run  # noqa: E402


def grab(src: Path, t: float, out: Path) -> None:
    run([ffmpeg_exe(), "-y", "-ss", f"{t:.3f}", "-i", str(src),
         "-frames:v", "1", "-q:v", "2", str(out)], quiet=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src")
    ap.add_argument("--every", type=float, default=0, help="seconds between frames")
    ap.add_argument("--at", default="", help="comma-separated timestamps in seconds")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    src = Path(args.src).resolve()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    dur = probe_duration(src)
    print(f"Source: {src.name}  ({dur:.1f}s)")

    times: list[float] = []
    if args.at:
        times = [float(x) for x in args.at.split(",") if x.strip()]
    elif args.every > 0:
        t = 0.0
        while t < dur:
            times.append(t)
            t += args.every
    else:
        raise SystemExit("Use --every N or --at t1,t2,...")

    for t in times:
        if t >= dur:
            continue
        fp = out / f"frame_{t:07.2f}.jpg"
        grab(src, t, fp)
        print(f"  {fp.name}")

    print(f"{len(times)} frames → {out}")


if __name__ == "__main__":
    main()
