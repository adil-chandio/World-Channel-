#!/usr/bin/env python3
"""Keyframed PNG-element compositor for vertical shorts (v7 — subject-safe).

Creative motion-graphics layer: analytic rings AROUND the subject (never covering),
spotlight isolation, lock-on brackets, margin callout arrows, draw-on underlines,
edge chrome (timestamp/REC/corners/progress/credit), micro flashes + shakes.

Subject-safety rule: elements encircle/point/frame the subject; they NEVER overlay
the subject's own pixels. Everything is keyframed (fades, eased slides, staged
timing, pulses, growth chunks) — no static copy-paste stickers.

Usage:
    python3 tools/keyframe_elements.py spec.json

Element kinds: timestamp, rec, corners, bar, progress (growth chunks), credit_bar,
ring_analytic, bracket (dir TL/TR/BL/BR), arrow, triangle, spotlight, vignette, flash.
Animation fields: at, dur, x, y, fade_in, fade_out, x_from, y_from, x_drift,
blink, enable_raw, w_px, chunks, color, alpha.
Spec-level: shakes:[{at,dur,amp}], flashes:[{at,dur,alpha}].
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


def png_credit_bar(path: Path, text: str) -> None:
    im, d = _canvas(660, 62)
    d.rounded_rectangle([0, 0, 659, 61], radius=12, fill=(8, 8, 12, 105))
    d.text((22, 16), text, font=_font(SANS_B, 26), fill=(235, 235, 240, 215))
    im.save(path)


def png_bar(path: Path, color: tuple[int, int, int, int], w: int = 1080) -> None:
    im = Image.new("RGBA", (w, 8), color)
    im.save(path)


def png_ring_analytic(path: Path, size: int = 355) -> None:
    im, d = _canvas(size, size)
    c = size // 2
    d.ellipse([10, 10, size - 10, size - 10], outline=(255, 255, 255, 150), width=3)
    d.ellipse([26, 26, size - 26, size - 26], outline=(230, 72, 58, 225), width=7)
    glow = im.filter(ImageFilter.GaussianBlur(10))
    im = Image.alpha_composite(glow, im)
    d = ImageDraw.Draw(im)
    tick = 16
    for x0, y0, x1, y1 in ((c - 2, 4, c + 2, 4 + tick),
                           (c - 2, size - 4 - tick, c + 2, size - 4),
                           (4, c - 2, 4 + tick, c + 2),
                           (size - 4 - tick, c - 2, size - 4, c + 2)):
        d.rectangle([x0, y0, x1, y1], fill=(255, 255, 255, 190))
    im.save(path)


def png_bracket(path: Path, dir_: str = "TL") -> None:
    size, th = 68, 5
    im, d = _canvas(size, size)
    col = (255, 255, 255, 210)
    d.rectangle([0, 0, size, th], fill=col)
    d.rectangle([0, 0, th, size], fill=col)
    d.rectangle([th + 3, th + 3, th + 9, th + 9], fill=(230, 70, 58, 235))
    if dir_ == "TR":
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    elif dir_ == "BL":
        im = im.transpose(Image.FLIP_TOP_BOTTOM)
    elif dir_ == "BR":
        im = im.transpose(Image.ROTATE_180)
    im.save(path)


def png_arrow(path: Path) -> None:
    im, d = _canvas(240, 110)
    white, red = (255, 255, 255, 238), (230, 70, 58, 235)
    d.line([(18, 55), (178, 55)], fill=white, width=7)
    d.polygon([(170, 26), (232, 55), (170, 84)], fill=white)
    d.ellipse([2, 43, 26, 67], fill=red)
    glow = im.filter(ImageFilter.GaussianBlur(5))
    im = Image.alpha_composite(glow, im)
    im.save(path)


def png_triangle(path: Path) -> None:
    im, d = _canvas(120, 110)
    tri = [(60, 8), (112, 100), (8, 100)]
    d.line(tri + [tri[0]], fill=(235, 200, 80, 245), width=7, joint="curve")
    d.text((52, 36), "!", font=_font(SANS_B, 56), fill=(235, 200, 80, 255))
    im.save(path)


def png_spotlight(path: Path, cx: int = 417, cy: int = 827, rx: int = 215, ry: int = 265) -> None:
    import numpy as np
    yy, xx = np.mgrid[0:H, 0:W].astype("float64")
    r = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
    a = np.clip((r - 0.92) * 320, 0, 118).astype("uint8")
    img = np.zeros((H, W, 4), dtype="uint8")
    img[..., 3] = a
    Image.fromarray(img, "RGBA").save(path)


def png_ring_arc(path: Path, seg: int = 0, size: int = 355) -> None:
    im, d = _canvas(size, size)
    start = -90 + seg * 45
    d.arc([26, 26, size - 26, size - 26], start=start, end=start + 47,
          fill=(230, 72, 58, 235), width=7)
    glow = im.filter(ImageFilter.GaussianBlur(8))
    im = Image.alpha_composite(glow, im)
    im.save(path)


def png_tick(path: Path) -> None:
    im, d = _canvas(10, 16)
    d.rounded_rectangle([2, 1, 8, 15], radius=3, fill=(255, 255, 255, 165))
    im.save(path)


def png_sweep(path: Path) -> None:
    im, d = _canvas(360, 2100)
    d.rectangle([110, 0, 250, 2100], fill=(255, 255, 255, 55))
    im = im.filter(ImageFilter.GaussianBlur(60))
    im = im.rotate(-16, expand=True, resample=Image.BICUBIC)
    im.save(path)


def png_badge(path: Path, text: str = "0.5x  SLOW") -> None:
    im, d = _canvas(210, 78)
    d.rounded_rectangle([0, 0, 209, 77], radius=14, fill=(8, 8, 12, 130))
    d.rounded_rectangle([0, 0, 8, 77], radius=4, fill=(230, 72, 58, 225))
    d.text((22, 24), text, font=_font(MONO_B, 32), fill=(245, 245, 248, 235))
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
    "credit_bar": lambda p, e: png_credit_bar(p, e.get("text", "")),
    "bar": lambda p, e: png_bar(p, tuple(e.get("color", [255, 255, 255, 170])), int(e.get("w_px", 1080))),
    "progress": lambda p, e: png_bar(p, tuple(e.get("color", [255, 255, 255, 185])), int(e.get("w_px", 1080))),
    "ring_analytic": lambda p, e: png_ring_analytic(p, int(e.get("size", 355))),
    "ring_arc": lambda p, e: png_ring_arc(p, int(e.get("seg", 0)), int(e.get("size", 355))),
    "tick": lambda p, e: png_tick(p),
    "sweep": lambda p, e: png_sweep(p),
    "badge": lambda p, e: png_badge(p, e.get("text", "0.5x  SLOW")),
    "bracket": lambda p, e: png_bracket(p, e.get("dir", "TL")),
    "arrow": lambda p, e: png_arrow(p),
    "triangle": lambda p, e: png_triangle(p),
    "spotlight": lambda p, e: png_spotlight(p),
    "vignette": lambda p, e: png_vignette(p),
}


def build_pngs(elements: list[dict], gfx: Path) -> list[Path]:
    gfx.mkdir(parents=True, exist_ok=True)
    out = []
    for i, el in enumerate(elements):
        kind = el["kind"]
        if kind == "flash":
            p = gfx / f"el_{i:03d}_flash.png"
            png_flash(p, int(el.get("alpha", 70)))
        else:
            tag = el.get("dir", kind)
            p = gfx / f"el_{i:03d}_{kind}_{tag}.png"
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
        t_in = min(0.5, max(d * 0.25, 0.2))
        if "x_from" in el:
            xf = int(el["x_from"])
            p = f"min(max((t-{at})/{t_in},0),1)"
            pe = f"({p})*({p})*(3-2*({p}))"
            xexpr = f"{x}+({xf}-{x})*(1-{pe})"
        else:
            xexpr = str(x)
        if "x_drift" in el:
            xexpr = f"{xexpr}+{float(el['x_drift'])}*(min(max((t-{at}),0),{d})/{max(d, 0.1)})"
        if "y_from" in el:
            yf = int(el["y_from"])
            p = f"min(max((t-{at})/{t_in},0),1)"
            pe = f"({p})*({p})*(3-2*({p}))"
            yexpr = f"{y}+({yf}-{y})*(1-{pe})"
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


def expand(elements: list[dict]) -> list[dict]:
    """Expand progress/underline growth elements into discrete keyframe chunks."""
    out: list[dict] = []
    for el in elements:
        if el.get("kind") == "progress":
            n = int(el.pop("chunks", 24))
            at, dur = float(el["at"]), float(el["dur"])
            x = int(el.get("x", 0))
            y = int(el.get("y", 0))
            col = el.get("color", [255, 255, 255, 185])
            full = int(el.get("w_px", 1080))
            for k in range(n):
                t0 = at + dur * k / n
                t1 = at + dur * (k + 1) / n
                out.append({
                    "kind": "bar", "color": col,
                    "w_px": max(2, int(full * (k + 1) / n)),
                    "at": t0, "dur": t1 - t0, "x": x, "y": y,
                    "fade_in": 0, "fade_out": 0,
                    "enable_raw": f"between(t,{t0:.3f},{t1 + 0.25:.3f})",
                })
        else:
            out.append(el)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("spec")
    args = ap.parse_args()
    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    spec["elements"] = expand(spec.get("elements", []))
    for fl in spec.get("flashes", []):
        spec.setdefault("elements", []).append({
            "kind": "flash", "alpha": fl.get("alpha", 70),
            "at": fl["at"], "dur": fl["dur"],
            "x": 0, "y": 0, "fade_in": 0.04, "fade_out": fl["dur"] - 0.06,
        })
    apply(spec)


if __name__ == "__main__":
    main()
