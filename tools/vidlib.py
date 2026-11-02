#!/usr/bin/env python3
"""Shared helpers for the Monarch Cam production tools."""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

# vendored deps (tools/_vendor) — kept inside the repo so they persist
sys.path.insert(0, str(Path(__file__).resolve().parent / "_vendor"))
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "ops" / "rights-ledger.csv"

BG = (14, 22, 32)          # deep charcoal-navy
GOLD = (201, 162, 39)      # warm restrained gold
WHITE = (255, 255, 255)
GREY = (168, 178, 190)

FONT_CANDIDATES_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]
FONT_CANDIDATES_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def ffmpeg_exe() -> str:
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(cmd: list[str], quiet: bool = False) -> None:
    """Run a command, printing the ffmpeg tail on failure."""
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        tail = proc.stderr.decode(errors="replace").splitlines()[-15:]
        print("COMMAND FAILED:", " ".join(cmd[:12]), "...", file=sys.stderr)
        print("\n".join(tail), file=sys.stderr)
        raise SystemExit(proc.returncode)
    if not quiet:
        err = proc.stderr.decode(errors="replace")
        for line in err.splitlines()[-3:]:
            if line.strip():
                print("  ", line.strip())


def probe_duration(path: str | Path) -> float:
    """Return media duration in seconds (via ffmpeg banner parse)."""
    proc = subprocess.run([ffmpeg_exe(), "-i", str(path)],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.?\d*)", proc.stderr.decode(errors="replace"))
    if not m:
        raise ValueError(f"Cannot read duration of {path}")
    h, mnt, sec = m.groups()
    return int(h) * 3600 + int(mnt) * 60 + float(sec)


def load_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    for cand in (FONT_CANDIDATES_BOLD if bold else FONT_CANDIDATES_REG):
        if Path(cand).exists():
            return ImageFont.truetype(cand, size)
    return ImageFont.load_default()


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
          max_width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_card(path: str | Path, text: str, sub: str = "",
              footer: str = "MONARCH CAM", size=(1920, 1080)) -> None:
    """Title / end card: charcoal-navy base, gold accent, white type."""
    w, h = size
    img = Image.new("RGB", size, BG)
    d = ImageDraw.Draw(img)
    font_big = load_font(112)
    font_sub = load_font(46, bold=False)
    font_foot = load_font(40)

    lines = _wrap(d, text, font_big, int(w * 0.82))
    line_h = 128
    total = len(lines) * line_h
    y = (h - total) // 2 - (40 if sub else 0)

    bar_w = 220
    d.rectangle([(w - bar_w) // 2, y - 60, (w + bar_w) // 2, y - 46], fill=GOLD)

    for ln in lines:
        tw = d.textlength(ln, font=font_big)
        d.text(((w - tw) // 2, y), ln, font=font_big, fill=WHITE)
        y += line_h

    if sub:
        y += 18
        for ln in _wrap(d, sub, font_sub, int(w * 0.75)):
            tw = d.textlength(ln, font=font_sub)
            d.text(((w - tw) // 2, y), ln, font=font_sub, fill=GOLD)
            y += 58

    if footer:
        fw = d.textlength(footer, font=font_foot)
        d.text(((w - fw) // 2, h - 90), footer, font=font_foot, fill=GREY)
    img.save(path)


def make_caption(path: str | Path, text: str, size=(1920, 1080),
                 y_frac: float = 0.80, font_size: int = 58) -> None:
    """Transparent caption PNG with white bold type + black stroke."""
    w, h = size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = load_font(font_size)
    lines = _wrap(d, text, font, int(w * 0.80))
    line_h = int(font_size * 1.28)
    y = int(h * y_frac) - (len(lines) * line_h) // 2
    for ln in lines:
        tw = d.textlength(ln, font=font)
        d.text(((w - tw) // 2, y), ln, font=font, fill=WHITE,
               stroke_width=max(3, font_size // 14), stroke_fill=(0, 0, 0))
        y += line_h
    img.save(path)


def rights_status(clip_path: str | Path) -> str | None:
    """Return rights status for a clip from the ledger, or None if unregistered."""
    if not LEDGER.exists():
        return None
    target = str(Path(clip_path).as_posix())
    with LEDGER.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if str(Path(row.get("file", "")).as_posix()) == target:
                return row.get("rights_status", "").strip()
    return None


def assert_cleared(clip_path: str | Path, skip: bool = False) -> None:
    """Hard-fail unless the clip is registered and cleared in the rights ledger.

    Exception: files under media/animations/ are agent-generated owned footage
    (make_animation.py outputs) and are auto-cleared.
    """
    if skip:
        print(f"  !! RIGHTS CHECK SKIPPED for {clip_path} (test/owned footage only)")
        return
    rel = str(Path(clip_path).as_posix())
    if rel.startswith("media/animations/"):
        return
    status = rights_status(clip_path)
    if status is None:
        raise SystemExit(
            f"RIGHTS BLOCK: '{clip_path}' is not in ops/rights-ledger.csv.\n"
            f"Register it first:  python3 tools/intake_register.py --file '{clip_path}' ...")
    if status != "cleared":
        raise SystemExit(
            f"RIGHTS BLOCK: '{clip_path}' has rights_status='{status}' (must be 'cleared').\n"
            f"Verify rights in the forensics report, then set status to 'cleared' in the ledger.")
