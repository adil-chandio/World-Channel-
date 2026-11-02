---
name: script-humanizer
description: |
  Rewrite Monarch Cam narration so it sounds like a real, mature wildlife creator — not AI.
  Use after drafting any long-form or Shorts script, before VO. Runs the humanize_check
  linter and edits against the humanizer pattern system plus the blueprint tone rules.
---

# Script Humanizer — narration that sounds human

Adapted from **blader/humanizer** (MIT, https://github.com/blader/humanizer) — pattern system
based on Wikipedia's *Signs of AI writing* — extended with Monarch Cam blueprint §12 tone
rules for a mature, TV-heavy wildlife audience.

## Workflow

1. Draft from the forensic report (story + explainer, sources marked `[[n]]`).
2. Run: `python3 tools/humanize_check.py <script.md> --min-score 70`
3. Fix every STRONG hit, then WEAK clusters. Re-run until PASS.
4. Read the VO lines ALOUD. If a sentence needs a breath mid-clause, split it.

## The tells, strongest first (fix on one sighting)

1. **Not X but Y** — "It's not just a bear, it's a lesson." → say the thing directly.
2. **One-line closers** — "Let that sink in." "That changes everything." → cut, or replace
   with a new fact the viewer doesn't have.
3. **Fake-deep sayings** — "At its core..." "Nature's true language..." → specific claim only.
4. **Staged run-ups** — "Let's break this down." "Honestly?" → start at the point.
5. **Arguing with no one** — "Now, I'm not saying all bears are dangerous..." → delete the
   defense; keep only claims the footage supports.

## Rhythm rules

- **Forced triads** ("raw, relentless, and ruthless") — only when meaning has 3 real parts.
- **Em-dashes** — narration almost never needs them; use commas or new sentences.
- **Exclamation marks** — max 1–2 per 100 words. The bear audience is 55+, TV-first; calm
  confidence beats hype.
- **Sentence length variance** — mix short punches with long observational lines. Real
  narrators rarely speak in uniform sentences.

## Monarch brand bans (blueprint §12 — non-negotiable)

- "pure wild attitude", "silent death", "no mercy", "absolute nightmare", "mind-blown"
- "will terrify/shock you", "you won't believe", "but it gets crazier"
- "Imagine..." openers — show proof in 0:00–0:03 instead.
- "attack" only where the footage and the claims check support it.

## Voice target

A confident US/UK wildlife creator talking to one person on a couch. Specific observation.
Genuine humour when it comes naturally. "Here's what the camera doesn't show" energy —
curious, precise, never breathless. If a line could appear in any channel's video, rewrite it
until it could only be about THIS footage.

## What the linter can't catch (do it by hand)

- Filler transitions every 15 seconds ("now...", "but here's the thing...", "and it gets
  better"). Vary transitions or delete them.
- Overclaiming danger in harmless clips (calibrate verbs: "approaches" ≠ "charges").
- Translated-sounding English — read aloud and simplify anything with nested clauses.
