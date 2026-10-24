#!/usr/bin/env python3
"""Keyframed PNG-element compositor for vertical shorts.

Builds PNG elements (timestamp, REC, rings, glow, arrow, warning, credit bar,
vignette, viewfinder corners, flashes) and composites them onto a video with
keyframed animation: fades, fly-ins, blink, impact flashes, camera shakes.

Usage:
    python3 tools/keyframe_elements.py spec.json

Spec:
{
  "input": "output/SHORT-03_FINAL.mp4",
  "output": "output/SHORT-03_FINAL_GFX.mp4",
  "duration": 27.5,
  "gfx_dir": "pipeline/produce/SHORT-03/v2/gfx",
  "elements": [
    {"kind": "timestamp", "text": "3:02 AM", "sub": "WOODLAND PARK, CO",
     "at": 0.25, "dur": 25.6, "x": 55, "y": 62, "fade_in": 0.35, "fade_out": 0.4},
    {"kind": "rec", "at": 0.3, "dur": 25.6, "x": 870, "y": 70, "blink": true},
    {"kind": "credit_bar", "text": "FOOTAGE: COLORADO PARKS & WILDLIFE",
     "at": 10.3, "dur": 3.2, "x": 60, "y": 1520, "x_from": -950,
     "fade_in": 0.2, "fade_out": 0.35}
  ],
  "shakes": [{"at": 7.35, "dur": 0.6, "amp": 7}],
  "flashes": [{"at": 7.32, "dur": 0.2, "alpha": 60}]
}
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vidlib import ffmpeg_exe, run  # noqa: E402

W, H = 1080, 1920
FONT_DIRS = ["/usr/share/fonts/truetype/dejavu"]
SANS_B = "DejaVuSans-Bold.ttf"
MONO_B = "DejaVuSansMono-Bold.ttf"


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for d in FONT_DIRS:
        p = Path(d) / name
        if p.exists():
            return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size)


def _canvas(w: int, h: int) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def png_timestamp(path: Path, text: str, sub: str) -> None:
    im, d = _canvas(336, 94)
    d.rounded_rectangle([0, 0, 335, 93], radius=14, fill=(8, 8, 12, 118))
    d.rounded_rectangle([0, 0, 8, 93], radius=4, fill=(220, 60, 50, 205))
    d.text((22, 12), text, font=_font(MONO_B, 40), fill=(245, 245, 248, 235))
    d.text((24, 60), sub, font=_font(SANS_B, 20), fill=(215, 215, 222, 185))
    im.save(path)


def png_rec(path: Path) -> None:
    im, d = _canvas(150, 58)
    d.ellipse([8, 14, 42, 48], fill=(235, 45, 38, 235))
    glow = im.filter(ImageFilter.GaussianBlur(6))
    im = Image.alpha_composite(glow, im)
    d = ImageDraw.Draw(im)
    d.text((56, 13), "REC", font=_font(MONO_B, 32), fill=(245, 245, 248, 225))
    im.save(path)


def png_corners(path: Path) -> None:
    im, d = _canvas(W, H)
    arm, th, ins, col = 92, 3, 70, (255, 255, 255, 118)
    for cx, cy, dx, dy in ((ins, ins, 1, 1), (W - ins, ins, -1, 1),
                           (ins, H - ins, 1, -1), (W - ins, H - ins, -1, -1)):
        x0, x1 = sorted((cx, cx + dx * arm))
        y0, y1 = sorted((cy, cy + dy * th))
        d.rectangle([x0, y0, x1, y1], fill=col)
        x0, x1 = sorted((cx, cx + dx * th))
        y0, y1 = sorted((cy, cy + dy * arm))
        d.rectangle([x0, y0, x1, y1], fill=col)
    im.save(path)


def png_ring(path: Path, size: int, rgb: tuple[int, int, int], width: int) -> None:
    im, d = _canvas(size, size)
    pad = width + 14
    d.ellipse([pad, pad, size - pad, size - pad], outline=rgb + (255,), width=width)
    glow = im.filter(ImageFilter.GaussianBlur(12))
    im = Image.alpha_composite(glow, im)
    im.save(path)


def png_glow(path: Path, size: int) -> None:
    im, d = _canvas(size, size)
    d.ellipse([size * 0.18, size * 0.18, size * 0.82, size * 0.82], fill=(255, 255, 255, 110))
    im = im.filter(ImageFilter.GaussianBlur(size // 7))
    im.save(path)


def png_arrow(path: Path) -> None:
    im, d = _canvas(300, 170)
    col, out = (255, 255, 255, 240), (10, 10, 12, 220)
    shaft = [(8, 58), (178, 58), (178, 28), (282, 85), (178, 142), (178, 112), (8, 112)]
    d.polygon(shaft, fill=col)
    d.line(shaft + [shaft[0]], fill=out, width=6, joint="curve")
    im.save(path)


def png_triangle(path: Path) -> None:
    im, d = _canvas(150, 140)
    tri = [(75, 8), (142, 130), (8, 130)]
    d.polygon(tri, fill=(235, 200, 70, 245), outline=(40, 32, 8, 255))
    d.line(tri + [tri[0]], fill=(40, 32, 8, 255), width=6)
    d.text((63, 48), "!", font=_font(SANS_B, 72), fill=(35, 28, 8, 255))
    im.save(path)


def png_credit_bar(path: Path, text: str) -> None:
    im, d = _canvas(660, 62)
    d.rounded_rectangle([0, 0, 659, 61], radius=12, fill=(8, 8, 12, 105))
    d.text((22, 16), text, font=_font(SANS_B, 26), fill=(235, 235, 240, 215))
    im.save(path)


def png_bar(path: Path, color: tuple[int, int, int, int], w: int = 1080) -> None:
    im = Image.new("RGBA", (w, 8), color)
    im.save(path)


def png_vignette(path: Path) -> None:
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W].astype("float64")
    cx, cy = W / 2, H / 2
    r = np.sqrt(((xx - cx) / (W * 0.62)) ** 2 + ((yy - cy) / (H * 0.58)) ** 2)
    a = np.clip((r - 0.62) * 170, 0, 105).astype("uint8")
    img = np.zeros((H, W, 4), dtype="uint8")
    img[..., 3] = a
    Image.fromarray(img, "RGBA").save(path)


def png_flash(path: Path, alpha: int) -> None:
    im = Image.new("RGBA", (W, H), (255, 255, 255, alpha))
    im.save(path)


BUILDERS = {
    "timestamp": lambda p, e: png_timestamp(p, e.get("text", "00:00 AM"), e.get("sub", "")),
    "rec": lambda p, e: png_rec(p),
    "corners": lambda p, e: png_corners(p),
    "ring_red": lambda p, e: png_ring(p, int(e.get("size", 260)), (225, 58, 48), int(e.get("width", 10))),
    "ring_white": lambda p, e: png_ring(p, int(e.get("size", 300)), (255, 255, 255), int(e.get("width", 9))),
    "glow": lambda p, e: png_glow(p, int(e.get("size", 600))),
    "arrow": lambda p, e: png_arrow(p),
    "triangle": lambda p, e: png_triangle(p),
    "credit_bar": lambda p, e: png_credit_bar(p, e.get("text", "")),
    "bar": lambda p, e: png_bar(p, tuple(e.get("color", [255, 255, 255, 170])), int(e.get("w_px", 1080))),
    "progress": lambda p, e: png_bar(p, tuple(e.get("color", [255, 255, 255, 185])), int(e.get("w_px", 1080))),
    "vignette": lambda p, e: png_vignette(p),
}


def build_pngs(elements: list[dict], gfx: Path) -> list[Path]:
    gfx.mkdir(parents=True, exist_ok=True)
    out = []
    for i, el in enumerate(elements):
        kind = el["kind"]
        if kind == "flash":
            p = gfx / f"el_{i:02d}_flash.png"
            png_flash(p, int(el.get("alpha", 70)))
        else:
            p = gfx / f"el_{i:02d}_{kind}.png"
            BUILDERS[kind](p, el)
        out.append(p)
    return out


def apply(spec: dict) -> None:
    src = Path(spec["input"])
    dst = Path(spec["output"])
    dur = float(spec["duration"])
    elements = spec.get("elements", [])
    pngs = build_pngs(elements, Path(spec.get("gfx_dir", "gfx")))

    cmd = [ffmpeg_exe(), "-y", "-i", str(src)]
    for p in pngs:
        cmd += ["-loop", "1", "-t", f"{dur}", "-i", str(p)]

    parts = []
    prev = "0:v"
    for i, el in enumerate(elements):
        at, d = float(el["at"]), float(el["dur"])
        fi, fo = float(el.get("fade_in", 0.2)), float(el.get("fade_out", 0.25))
        lbl = f"e{i}"
        f = f"[{i + 1}:v]format=rgba"
        if fi > 0:
            f += f",fade=t=in:st={at}:d={fi}:alpha=1"
        if fo > 0 and at + d - fo > at + fi:
            f += f",fade=t=out:st={at + d - fo}:d={fo}:alpha=1"
        f += f"[{lbl}]"
        parts.append(f)

        x = int(el.get("x", 0))
        y = int(el.get("y", 0))
        if "x_from" in el:
            xf = int(el["x_from"])
            t_in = min(0.5, max(d * 0.25, 0.2))
            xexpr = f"{x}+({xf}-{x})*(1-min(max((t-{at})/{t_in},0),1))"
        else:
            xexpr = str(x)
        if "y_from" in el:
            yf = int(el["y_from"])
            t_in = min(0.5, max(d * 0.25, 0.2))
            yexpr = f"{y}+({yf}-{y})*(1-min(max((t-{at})/{t_in},0),1))"
        else:
            yexpr = str(y)
        en = ""
        if el.get("enable_raw"):
            en = f":enable='{el['enable_raw']}'"
        elif el.get("blink"):
            en = f":enable='between(t,{at},{at + d})*lt(mod(t-{at},1.15),0.78)'"
        ov = f"[{prev}][{lbl}]overlay=x='{xexpr}':y='{yexpr}'{en}:eof_action=pass[v{i}]"
        parts.append(ov)
        prev = f"v{i}"

    shake_x, shake_y = "", ""
    for s in spec.get("shakes", []):
        at, d, amp = float(s["at"]), float(s["dur"]), float(s.get("amp", 6))
        shake_x += f"+if(between(t,{at},{at + d}),{amp}*sin(88*(t-{at})),0)"
        shake_y += f"+if(between(t,{at},{at + d}),{amp * 0.8}*sin(73*(t-{at} + 0.6)),0)"
    pad_x, pad_y = 24, 42
    fin = (f"[{prev}]scale=1128:2005,crop=1080:1920:x='{pad_x}{shake_x}':y='{pad_y}{shake_y}',"
           "format=yuv420p[vout]")
    parts.append(fin)

    cmd += ["-filter_complex", ";".join(parts), "-map", "[vout]", "-map", "0:a"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "copy", str(dst)]
    run(cmd, quiet=True)
    print(f"[keyframe_elements] {dst}  elements={len(elements)} "
          f"shakes={len(spec.get('shakes', []))} flashes={len(spec.get('flashes', []))}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("spec")
    args = ap.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    expanded: list[dict] = []
    for el in spec.get("elements", []):
        if el.get("kind") == "progress":
            n = int(el.pop("chunks", 30))
            at, dur = float(el["at"]), float(el["dur"])
            y = int(el.get("y", 0))
            col = el.get("color", [255, 255, 255, 185])
            for k in range(n):
                t0 = at + dur * k / n
                t1 = at + dur * (k + 1) / n
                expanded.append({
                    "kind": "bar", "color": col,
                    "w_px": max(2, int(1080 * (k + 1) / n)),
                    "at": t0, "dur": t1 - t0, "x": 0, "y": y,
                    "fade_in": 0, "fade_out": 0,
                    "enable_raw": f"between(t,{t0:.3f},{t1 + 0.25:.3f})",
                })
        else:
            expanded.append(el)
    spec["elements"] = expanded
    for fl in spec.get("flashes", []):
        spec.setdefault("elements", []).append({
            "kind": "flash", "alpha": fl.get("alpha", 70),
            "at": fl["at"], "dur": fl["dur"],
            "x": 0, "y": 0, "fade_in": 0.04, "fade_out": fl["dur"] - 0.06,
        })
    apply(spec)


if __name__ == "__main__":
    main()
