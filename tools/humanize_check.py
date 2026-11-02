#!/usr/bin/env python3
"""Humanize-check: lint narration scripts for AI-writing tells + brand banned phrases.

Adapted from the pattern system of blader/humanizer (MIT, https://github.com/blader/humanizer)
— Wikipedia "Signs of AI writing" — extended with Monarch Cam blueprint tone rules.

Usage:
    python3 tools/humanize_check.py pipeline/scripts/BRIEF-01_LONG.md [--min-score 70]

Exit codes: 0 = pass, 2 = score below --min-score.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# (id, category, severity, pattern, message)
# severity: strong = fix on sight | weak = fix when it clusters | info
RULES: list[tuple] = [
    # ── Humanizer §1: Not X but Y ────────────────────────────────────────────
    ("H1a", "staging", "strong", r"\bnot (just|only|merely)\b[^.!?]{0,80}\bbut\b",
     "Not-X-but-Y contrast — state the point directly."),
    ("H1b", "staging", "strong", r"\bit'?s not\b[^.!?]{2,60},\s*it'?s\b",
     "It's-not-X-it's-Y — say what it IS."),
    ("H1c", "staging", "weak", r"\bno guessing\b|\bno doubt\b|\bno brainer\b",
     "Clipped negative tail — just remove."),
    # ── §2: One-line closers / dramatic fragments ────────────────────────────
    ("H2a", "staging", "strong", r"\b(let that sink in|read that again|that is the real win|"
     r"that distinction matters|the message was clear|the lesson here|and that says it all)\b",
     "One-line closer — cut or replace with a new fact."),
    ("H2b", "staging", "weak", r"\b(this shows the importance|this proves once again|"
     r"it was a lesson in)\b",
     "Explaining your own example — the viewer already saw it."),
    ("H2c", "staging", "weak", r"\b\w+\. \w+\. \w+\.(\s|$)",
     "Fragment row (No x. No y. No z.) — merge into a real sentence."),
    # ── §3: Sayings that sound deep ─────────────────────────────────────────
    ("H3", "staging", "strong", r"\b(at its core|the real question is|what really matters is|"
     r"fundamentally|the heart of the matter|the deeper (issue|truth)|by its very nature|"
     r"the (language|currency|architecture) of)\b",
     "Fake-deep saying — replace with the specific claim."),
    # ── §4: Staged run-ups ──────────────────────────────────────────────────
    ("H4", "staging", "strong", r"\b(let'?s dive in|let'?s explore|let'?s break this down|"
     r"here'?s what you (need to know|should know)|without further ado|buckle up|"
     r"real talk|sit back and)\b",
     "Staged run-up — start at the point."),
    ("H4b", "staging", "weak", r"(^|\.\s+)(Honestly\?|Here'?s the thing\.|The thing is,|Look,)",
     "Staged candor opener — cut the run-up."),
    # ── §5: Arguing with no one ─────────────────────────────────────────────
    ("H5", "staging", "weak", r"\b(i'?m not saying|don'?t get me wrong|to be clear,|"
     r"this isn'?t (really )?about|some might say|one might be tempted|a tempting approach)\b",
     "Arguing with nobody — state the claim instead."),
    # ── Stock AI words ──────────────────────────────────────────────────────
    ("W1", "stock-words", "weak", r"\b(delve|delves|delving|tapestry|testament to|boasts|"
     r"meticulous|meticulously|pivotal|seamless|seamlessly|leverage|elevates?|unleash)\b",
     "Stock AI vocabulary — use the plain word."),
    ("W2", "stock-words", "weak", r"\b(in today'?s (fast-paced |modern )?world|in the (world|realm) of|"
     r"in an era (of|where)|a game[- ]changer|unlock(ing)? the (power|potential))\b",
     "Inflated framing — get to the wildlife."),
    # ── Monarch Cam brand bans (blueprint §12) ───────────────────────────────
    ("B1", "brand", "strong", r"\b(pure wild attitude|silent death|no mercy|absolute nightmare|"
     r"mind[- ]blown|beast mode|apex predator of)\b",
     "BANNED phrase (blueprint §12) — natural English only."),
    ("B2", "brand", "strong", r"\b(will (terrify|shock) you|you won'?t believe|"
     r"but it gets (crazier|wilder)|what happens next will)\b",
     "BANNED hype phrase — calibrated language only."),
    ("B3", "brand", "strong", r"(^|\.\s+)Imagine\b",
     "'Imagine...' opener banned — show proof first."),
    ("B4", "brand", "strong", r"\b(attack(s|ed|ing)?)\b",
     "Verify before calling it an 'attack' — see forensics claims check."),
    # ── Rhythm / density (info) ─────────────────────────────────────────────
    ("R1", "rhythm", "info", r"—",
     "Em-dash — narration rarely needs these (see also dash density)."),
]

TRIAD_RE = re.compile(r"\b(\w{3,}), (\w{3,}),? and (\w{3,})\b")
CAPS_RE = re.compile(r"\b[A-Z]{3,}\b")


def scan(text: str) -> tuple[list[dict], dict]:
    issues = []
    lines = text.splitlines()
    for i, line in enumerate(lines, 1):
        if line.lstrip().startswith(("|", "#", ">", "```")):
            continue
        for rid, cat, sev, pat, msg in RULES:
            for m in re.finditer(pat, line, re.IGNORECASE if rid != "R1" else 0):
                if rid == "B4" and re.search(r"(never|don'?t call|only when|not an)", line, re.I):
                    continue  # meta-discussion about the word is fine
                issues.append({"rule": rid, "cat": cat, "sev": sev, "line": i,
                               "match": m.group(0)[:60], "msg": msg})
    words = len(re.findall(r"\b\w+\b", text))
    triads = len(TRIAD_RE.findall(text))
    caps = len(CAPS_RE.findall(text))
    excl = text.count("!")
    stats = {"words": words, "triads": triads, "caps_words": caps, "exclamations": excl,
             "triads_per_100w": round(triads * 100 / max(words, 1), 2)}
    return issues, stats


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("script")
    ap.add_argument("--min-score", type=int, default=70)
    args = ap.parse_args()

    path = Path(args.script)
    if not path.exists():
        raise SystemExit(f"File not found: {path}")
    text = path.read_text(encoding="utf-8")
    issues, stats = scan(text)

    strong = [x for x in issues if x["sev"] == "strong"]
    weak = [x for x in issues if x["sev"] == "weak"]
    info = [x for x in issues if x["sev"] == "info"]
    score = max(0, 100 - 6 * len(strong) - 2 * len(weak))

    print(f"═══ humanize_check: {path.name} ═══")
    print(f"words={stats['words']}  score={score}/100  "
          f"(strong={len(strong)} weak={len(weak)} info={len(info)})")
    if stats["triads_per_100w"] > 4:
        print(f"  ! forced-triad density high: {stats['triads_per_100w']} per 100 words")
    if stats["exclamations"] > max(2, stats["words"] // 150):
        print(f"  ! exclamation marks: {stats['exclamations']} — mature TV audience wants calm confidence")
    if stats["caps_words"] > 3:
        print(f"  ! ALL-CAPS words: {stats['caps_words']}")

    for group, label in ((strong, "STRONG (fix on sight)"),
                         (weak, "WEAK (fix when clustered)"),
                         (info, "INFO")):
        if not group:
            continue
        print(f"\n── {label} ──")
        for x in group[:20]:
            print(f"  L{x['line']:>4} [{x['rule']}] “{x['match']}” → {x['msg']}")

    if score < args.min_score:
        print(f"\nFAIL: score {score} < {args.min_score}. Rewrite before VO.")
        sys.exit(2)
    print(f"\nPASS: score {score} ≥ {args.min_score}.")


if __name__ == "__main__":
    main()
