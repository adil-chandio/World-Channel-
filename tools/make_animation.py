#!/usr/bin/env python3
"""Motion-graphics generator: brand-safe animated cards/clips for explainers.

Presets:
  text_pop     — title card with eased text pop + growing gold bar (intro/outro beats)
  bar_reveal   — animated comparison bars (e.g. "952K vs 7.7K") for forensic explainers
  zoom_callout — Ken-Burns zoom on an image + fading callout ring/label ("microscope" beats)

All outputs are owned/generated footage (silent AAC track included) — auto-cleared for
renders when written under media/animations/.

Usage:
  python3 tools/make_animation.py text_pop --text "HE CAME BACK" --sub "The footage shows more" \
      --duration 3.0 --out media/animations/he_came_back.mp4
  python3 tools/make_animation.py bar_reveal --title "Same formula, different results" \
      --bars "Bear original|952" --bars "Shark copycat|7.7" --unit "K views" \
      --duration 4.5 --out media/animations/bars.mp4
  python3 tools/make_animation.py zoom_callout --image /path/frame.jpg --label "The door handle" \
      --at 0.35,0.55 --duration 4.0 --out media/animations/callout.mp4
"""
from __future__ import annotations

import argparse
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vidlib import (BG, GOLD, GREY, REPO, WHITE, _wrap, ffmpeg_exe, load_font,
                    make_card)  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

FPS = 30


def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3


def frames_to_mp4(frames_dir: Path, out: Path, dur: float, size: tuple[int, int]) -> None:
    w, h = size
    ff = ffmpeg_exe()
    subprocess.run([ff, "-y", "-framerate", str(FPS), "-i", str(frames_dir / "f_%04d.png"),
                    "-f", "lavfi", "-t", f"{dur}", "-i", "anullsrc=r=48000:cl=stereo",
                    "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
                    "-t", f"{dur}", str(out)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not out.exists():
        raise SystemExit("render failed")
    out.parent.mkdir(parents=True, exist_ok=True)


def render_text_pop(args, size, out: Path) -> None:
    w, h = size
    n = int(args.duration * FPS)
    frames_dir = Path(tempfile.mkdtemp())
    try:
        for i in range(n):
            t = i / n
            img = Image.new("RGB", size, BG)
            d = ImageDraw.Draw(img)
            font_big = load_font(int(h * 0.105))
            font_sub = load_font(int(h * 0.045), bold=False)

            # gold bar grows
            bar_w = int(w * 0.12 * ease_out_cubic(min(1, t * 2.2)))
            cy = int(h * 0.42)
            d.rectangle([(w - bar_w) // 2, cy, (w + bar_w) // 2, cy + 10], fill=GOLD)

            # text pop: scale via font size ease + fade via blend
            pop = ease_out_cubic(min(1, max(0, (t - 0.08) * 2.4)))
            if pop > 0:
                fsize = int(h * 0.105 * (0.82 + 0.18 * pop))
                f = load_font(fsize)
                lines = _wrap(d, args.text, f, int(w * 0.82))
                lh = int(fsize * 1.14)
                y = cy + 34
                shade = tuple(int(BG[j] + (WHITE[j] - BG[j]) * pop) for j in range(3))
                for ln in lines:
                    tw = d.textlength(ln, font=f)
                    d.text(((w - tw) // 2, y), ln, font=f, fill=shade)
                    y += lh
                if args.sub and t > 0.35:
                    sp = min(1.0, (t - 0.35) / 0.25)
                    sc = tuple(int(BG[j] + (GOLD[j] - BG[j]) * sp) for j in range(3))
                    y += 12
                    for ln in _wrap(d, args.sub, font_sub, int(w * 0.75)):
                        tw = d.textlength(ln, font=font_sub)
                        d.text(((w - tw) // 2, y), ln, font=font_sub, fill=sc)
                        y += int(h * 0.055)
            foot = load_font(int(h * 0.035))
            fw = d.textlength("MONARCH CAM", font=foot)
            d.text(((w - fw) // 2, h - int(h * 0.09)), "MONARCH CAM", font=foot, fill=GREY)
            img.save(frames_dir / f"f_{i:04d}.png")
        frames_to_mp4(frames_dir, out, args.duration, size)
    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)


def render_bar_reveal(args, size, out: Path) -> None:
    w, h = size
    n = int(args.duration * FPS)
    bars = []
    for b in args.bars:
        label, val = b.rsplit("|", 1)
        bars.append((label.strip(), float(val)))
    vmax = max(v for _, v in bars) or 1
    frames_dir = Path(tempfile.mkdtemp())
    try:
        for i in range(n):
            t = i / n
            img = Image.new("RGB", size, BG)
            d = ImageDraw.Draw(img)
            f_title = load_font(int(h * 0.052))
            f_label = load_font(int(h * 0.036))
            f_val = load_font(int(h * 0.04))
            y = int(h * 0.16)
            for ln in _wrap(d, args.title, f_title, int(w * 0.86)):
                tw = d.textlength(ln, font=f_title)
                d.text(((w - tw) // 2, y), ln, font=f_title, fill=WHITE)
                y += int(h * 0.065)
            y += int(h * 0.06)
            bar_x = int(w * 0.12)
            bar_max = int(w * 0.62)
            for bi, (label, val) in enumerate(bars):
                grow = ease_out_cubic(min(1, max(0, (t - bi * 0.12) * 1.9)))
                bw = int(bar_max * (val / vmax) * grow)
                bh = int(h * 0.075)
                color = GOLD if bi == 0 else (110, 122, 138)
                d.rectangle([bar_x, y, bar_x + bw, y + bh], fill=color)
                d.text((bar_x + bw + 14, y + 2), f"{val:g}{args.unit}", font=f_val, fill=WHITE)
                d.text((bar_x, y - int(h * 0.038)), label, font=f_label, fill=GREY)
                y += int(h * 0.16)
            img.save(frames_dir / f"f_{i:04d}.png")
        frames_to_mp4(frames_dir, out, args.duration, size)
    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)


def render_zoom_callout(args, size, out: Path) -> None:
    w, h = size
    n = int(args.duration * FPS)
    src = Image.open(args.image).convert("RGB")
    # pre-resize once to cover canvas at max zoom (keeps per-frame crop fast)
    tw, th = int(w * 1.14), int(h * 1.14)
    iw0, ih0 = src.size
    scale = max(tw / iw0, th / ih0)
    if scale < 1:
        src = src.resize((int(iw0 * scale), int(ih0 * scale)))
    cx, cy = (float(x) for x in args.at.split(","))
    frames_dir = Path(tempfile.mkdtemp())
    try:
        for i in range(n):
            t = i / n
            zoom = 1.0 + 0.14 * ease_out_cubic(t)
            iw, ih = int(w * zoom), int(h * zoom)
            img = src.resize((iw, ih))
            left = int(cx * iw - w / 2)
            top = int(cy * ih - h / 2)
            left = max(0, min(iw - w, left))
            top = max(0, min(ih - h, top))
            frame = img.crop((left, top, left + w, top + h))
            d = ImageDraw.Draw(frame)
            if t > 0.25:
                fade = min(1.0, (t - 0.25) / 0.2)
                rx, ry = int(cx * w), int(cy * h)
                rr = int(h * 0.13)
                ring = tuple(int(c * fade) for c in GOLD)
                d.ellipse([rx - rr, ry - rr, rx + rr, ry + rr], outline=ring, width=8)
                f = load_font(int(h * 0.042))
                if args.label:
                    tw = d.textlength(args.label, font=f)
                    ly = ry + rr + 12
                    d.rectangle([rx - tw / 2 - 12, ly - 8, rx + tw / 2 + 12, ly + int(h * 0.055)],
                                fill=(0, 0, 0))
                    d.text((rx - tw / 2, ly), args.label, font=f, fill=WHITE)
            frame.save(frames_dir / f"f_{i:04d}.png")
        frames_to_mp4(frames_dir, out, args.duration, size)
    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("preset", choices=["text_pop", "bar_reveal", "zoom_callout"])
    ap.add_argument("--text", default="")
    ap.add_argument("--sub", default="")
    ap.add_argument("--title", default="MONARCH CAM")
    ap.add_argument("--label", default="")
    ap.add_argument("--image", default="")
    ap.add_argument("--at", default="0.5,0.5")
    ap.add_argument("--bars", action="append", default=[],
                    help='bar_reveal: "Label|value" (repeatable)')
    ap.add_argument("--unit", default="")
    ap.add_argument("--duration", type=float, default=3.0)
    ap.add_argument("--size", default="1920x1080", help="1920x1080 or 1080x1920")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    w, h = (int(x) for x in args.size.lower().split("x"))
    out = Path(args.out)
    if not str(out).startswith("/"):
        out = REPO / out
    out.parent.mkdir(parents=True, exist_ok=True)
    print(f"[make_animation] {args.preset} {args.size} {args.duration}s → {out}")

    if args.preset == "text_pop":
        if not args.text:
            raise SystemExit("text_pop needs --text")
        render_text_pop(args, (w, h), out)
    elif args.preset == "bar_reveal":
        if not args.bars:
            raise SystemExit('bar_reveal needs --bars "Label|value" (repeatable)')
        render_bar_reveal(args, (w, h), out)
    else:
        if not args.image:
            raise SystemExit("zoom_callout needs --image")
        render_zoom_callout(args, (w, h), out)
    print(f"[make_animation] DONE: {out}")


if __name__ == "__main__":
    main()
