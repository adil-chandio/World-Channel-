#!/usr/bin/env python3
"""Synthesize a cinematic audio bed (music + SFX) with automatic VO ducking.

Usage:
    python3 tools/sound_design.py plan.json --vo vo.mp3 --out bed.wav

Event types: impact | riser | whoosh | heartbeat | pulse | pluck | tick | subdrop
Design rules: dark/warm, soft transients, high-end rolled off — never harsh.
Master: tanh soft-clip glue + peak normalize.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

SR = 48000
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vidlib import ffmpeg_exe  # noqa: E402


def _t(dur: float) -> np.ndarray:
    return np.arange(int(dur * SR)) / SR


def spectral_tilt(x: np.ndarray, cutoff: float, order: float = 2.0) -> np.ndarray:
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X *= 1.0 / (1.0 + (f / max(cutoff, 1.0)) ** order)
    return np.fft.irfft(X, n)


def bandpass(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    ramp = 512.0
    edge = np.clip(np.minimum((f - lo) / ramp, (hi - f) / ramp), 0, 1)
    X *= edge
    return np.fft.irfft(X, n)


def make_impact(dur: float, freq: float, rng: np.random.Generator) -> np.ndarray:
    """Deep cinematic hit: sub body + soft air, tiny soft click (never sharp)."""
    t = _t(dur)
    sweep = freq * np.exp(-t * 1.1) * 0.5 + freq * 0.6
    ph = 2 * np.pi * np.cumsum(sweep) / SR
    body = np.sin(ph) * np.exp(-t * 2.3)
    sub = np.sin(2 * np.pi * 30 * t) * np.exp(-t * 1.7) * 0.55
    air = spectral_tilt(rng.standard_normal(len(t)), 170, 1.6) * np.exp(-t * 6.5) * 0.55
    click = spectral_tilt(rng.standard_normal(len(t)), 1100, 2.2) * np.exp(-t * 60) * 0.06
    return body + sub + air + click


def make_riser(dur: float, rng: np.random.Generator) -> np.ndarray:
    """Smooth tension lift — airy, not hissy."""
    t = _t(dur)
    env = (t / dur) ** 2.2
    noise = rng.standard_normal(len(t))
    low = bandpass(noise, 100, 600)
    high = bandpass(noise, 600, 3000)
    xfade = t / dur
    nz = low * (1 - xfade) + high * xfade
    sweep = 150 * (1 + 3.0 * (t / dur) ** 1.6)
    ph = 2 * np.pi * np.cumsum(sweep) / SR
    tone = np.sin(ph) * 0.28
    return (nz * 0.75 + tone) * env


def make_whoosh(dur: float, rng: np.random.Generator) -> np.ndarray:
    t = _t(dur)
    env = np.sin(np.pi * t / dur) ** 1.8
    nz = bandpass(rng.standard_normal(len(t)), 180, 2800)
    return nz * env * 0.9


def make_heartbeat(gain_env: float = 1.0) -> np.ndarray:
    out = np.zeros(int(0.85 * SR))
    for at, g in ((0.0, 1.0), (0.24, 0.72)):
        t = _t(0.42)
        thump = np.sin(2 * np.pi * 44 * t) * np.exp(-t * 15) * g
        sub = np.sin(2 * np.pi * 29 * t) * np.exp(-t * 10) * 0.35 * g
        i = int(at * SR)
        out[i:i + len(thump)] += thump + sub
    return out * gain_env


def make_pulse(dur: float, freq: float) -> np.ndarray:
    t = _t(dur)
    return np.sin(2 * np.pi * freq * t) * np.exp(-t * 5.5)


def make_pluck(dur: float, freq: float) -> np.ndarray:
    t = _t(dur)
    x = (np.sin(2 * np.pi * freq * t)
         + 0.35 * np.sin(2 * np.pi * 2 * freq * t)
         + 0.12 * np.sin(2 * np.pi * 3 * freq * t))
    return x * np.exp(-t * 5.0)


def make_tick() -> np.ndarray:
    """Soft caption-cue blip: warm, quiet, zero ear-poke."""
    t = _t(0.10)
    x = np.sin(2 * np.pi * 980 * t) * np.exp(-t * 65)
    x += np.sin(2 * np.pi * 1470 * t) * np.exp(-t * 80) * 0.35
    x += spectral_tilt(np.random.default_rng(3).standard_normal(len(t)), 2400, 2.0) * np.exp(-t * 90) * 0.18
    return x * 0.45


def make_subdrop(dur: float = 1.0) -> np.ndarray:
    """Deep sub sweep for the freeze/payoff moment."""
    t = _t(dur)
    sweep = 60 * np.exp(-t * 1.5) + 26
    ph = 2 * np.pi * np.cumsum(sweep) / SR
    return np.sin(ph) * np.exp(-t * 2.0)


def make_chord(dur: float, notes: list[float]) -> tuple[np.ndarray, np.ndarray]:
    t = _t(dur + 0.6)
    l = np.zeros_like(t)
    r = np.zeros_like(t)
    atk, rel = 0.35, 0.6
    env = np.ones_like(t)
    a = int(atk * SR)
    env[:a] = np.linspace(0, 1, a) ** 1.4
    rl = int(rel * SR)
    env[-rl:] = np.linspace(1, 0, rl) ** 1.2
    lfo = 1 + 0.06 * np.sin(2 * np.pi * 0.13 * t)
    for f in notes:
        vib = 1 + 0.0016 * np.sin(2 * np.pi * (0.21 + 0.017 * f % 3) * t)
        l += (np.sin(2 * np.pi * f * t * vib) + 0.30 * np.sin(2 * np.pi * 2.002 * f * t)
              + 0.10 * np.sin(2 * np.pi * 3 * f * t))
        r += (np.sin(2 * np.pi * f * 1.0025 * t * vib) + 0.30 * np.sin(2 * np.pi * 1.998 * f * t)
              + 0.10 * np.sin(2 * np.pi * 3.004 * f * t))
    return l * env * lfo * 0.12, r * env * lfo * 0.12


def vo_envelope(vo_path: Path) -> np.ndarray:
    proc = subprocess.run(
        [ffmpeg_exe(), "-i", str(vo_path), "-f", "s16le", "-ac", "1",
         "-ar", str(SR), "-"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return np.frombuffer(proc.stdout, dtype=np.int16).astype(np.float64) / 32768.0


def duck_curve(x: np.ndarray, n: int, amount: float, attack: float, release: float) -> np.ndarray:
    win = max(int(0.05 * SR), 1)
    pad = (win - len(x) % win) % win
    xr = np.pad(x, (0, pad)).reshape(-1, win)
    rms = np.sqrt((xr ** 2).mean(axis=1) + 1e-12)
    ref = np.percentile(rms, 92) + 1e-9
    env = np.clip(rms / ref, 0, 1)
    sm = np.empty_like(env)
    cur = 0.0
    a = np.exp(-win / (attack * SR))
    r = np.exp(-win / (release * SR))
    for i, v in enumerate(env):
        coef = a if v > cur else r
        cur = coef * cur + (1 - coef) * v
        sm[i] = cur
    gain_steps = 1.0 - amount * sm
    gain = np.repeat(gain_steps, win)
    if len(gain) < n:
        gain = np.concatenate([gain, np.ones(n - len(gain))])
    return gain[:n]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("plan")
    ap.add_argument("--vo", default=None)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    dur = float(plan["duration"])
    n = int(dur * SR)
    rng = np.random.default_rng(7)
    left = np.zeros(n)
    right = np.zeros(n)

    for ch in plan.get("chords", []):
        at = int(float(ch["at"]) * SR)
        l, r = make_chord(float(ch["dur"]), [float(f) for f in ch["notes"]])
        g = float(ch.get("gain", 1.0))
        seg = min(len(l), n - at)
        left[at:at + seg] += l[:seg] * g
        right[at:at + seg] += r[:seg] * g

    for ev in plan.get("events", []):
        at = int(float(ev["at"]) * SR)
        g = float(ev.get("gain", 0.5))
        typ = ev["type"]
        if typ == "impact":
            s = make_impact(float(ev.get("dur", 1.6)), float(ev.get("freq", 52)), rng) * g
        elif typ == "riser":
            s = make_riser(float(ev.get("dur", 0.9)), rng) * g
        elif typ == "whoosh":
            s = make_whoosh(float(ev.get("dur", 0.5)), rng) * g
        elif typ == "heartbeat":
            s = make_heartbeat() * g
        elif typ == "pulse":
            s = make_pulse(float(ev.get("dur", 0.5)), float(ev.get("freq", 55))) * g
        elif typ == "pluck":
            s = make_pluck(float(ev.get("dur", 0.7)), float(ev.get("freq", 440))) * g
        elif typ == "tick":
            s = make_tick() * g
        elif typ == "subdrop":
            s = make_subdrop(float(ev.get("dur", 1.0))) * g
        else:
            raise SystemExit(f"unknown event type: {typ}")
        pan = float(ev.get("pan", 0.0))
        gl = np.sqrt(0.5 * (1 - pan))
        gr = np.sqrt(0.5 * (1 + pan))
        seg = min(len(s), n - at)
        left[at:at + seg] += s[:seg] * gl
        right[at:at + seg] += s[:seg] * gr

    if args.vo:
        duck = plan.get("duck", {"amount": 0.62, "attack": 0.1, "release": 0.45})
        vo = vo_envelope(Path(args.vo))
        m = min(len(vo), n)
        gain = duck_curve(vo[:m], n, float(duck.get("amount", 0.62)),
                          float(duck.get("attack", 0.1)), float(duck.get("release", 0.45)))
        left *= gain
        right *= gain

    peak = float(plan.get("peak", 0.62))
    cur = max(np.abs(left).max(), np.abs(right).max(), 1e-9)
    left *= peak / cur
    right *= peak / cur
    drive = float(plan.get("drive", 1.25))
    left = np.tanh(left * drive) / np.tanh(drive) * peak
    right = np.tanh(right * drive) / np.tanh(drive) * peak
    cur = max(np.abs(left).max(), np.abs(right).max(), 1e-9)
    left *= peak / cur
    right *= peak / cur

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    stereo = np.stack([left, right], axis=1)
    pcm = (np.clip(stereo, -1, 1) * 32767).astype(np.int16).tobytes()
    subprocess.run(
        [ffmpeg_exe(), "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
         "-c:a", "pcm_s16le", str(out)],
        input=pcm, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    print(f"[sound_design] {out} ({dur:.2f}s, peak {peak}, drive {drive}, events "
          f"{len(plan.get('events', []))}, chords {len(plan.get('chords', []))})")


if __name__ == "__main__":
    main()
