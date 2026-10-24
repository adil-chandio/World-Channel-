---
name: youtube-ops
description: |
  Monarch Cam channel operations — packaging, upload wiring, Shorts-to-long funnel, and the
  honest take on YouTube-automation tools. Use when a video enters package stage, when
  planning publishing order, or when evaluating automation/shortcut tooling.
---

# YouTube Ops — publish like a system

## The automation landscape (what to adopt, what to refuse)

| Project | Verdict | Why |
|---|---|---|
| **harry0703/MoneyPrinterTurbo** (MIT) | Adopt concepts | Stock-fetch (→ our `tools/stock_broll.py`), TTS→subtitle→assemble loop. Do NOT ship its faceless slideshow output — that's the reused-content trap. |
| **darkzOGx/youtube-automation-agent** (MIT) | Reference | End-to-end agent loop (research→script→render→upload) is the right skeleton; our skills cover each stage with better quality gates. |
| Face-swap "viral clone" tools (e.g. hypit) | **Refuse** | Misleading synthetic realism + policy/monetisation risk. YouTube requires altered-content disclosure; trust is our product. |
| Uploaders/SEO spam packs | **Refuse** | Titles/tags can't save weak packaging; the algorithm reads satisfaction. |

## Packaging rules (blueprint §11)

- **Title:** standalone, one promise, title case, natural English. Never "Part 2".
- **Thumbnail:** one subject (55–70% of frame), one emotion, 0–3 words, legible at 98×98.
- **Description:** line 1 = the payoff; then story context; credits (from rights ledger);
  playlist + next video links; chapters.
- **Pinned comment:** the next destination (or the question the video asks).

## The Shorts → long funnel (every Short, no exceptions)

1. Description line 1: `Full story: <long URL>`
2. Pinned comment: `The full breakdown is here → <long URL>`
3. Burned end cue: `FULL STORY ON MONARCH CAM`
4. Publish 0–2 days from its long video.

## End-screen system (Bear P3 earned 14.3% views from end screens)

Last 20 s of every long video:
1. Spoken handoff line naming the NEXT story ("if this surprised you, watch what happened at
   the next house").
2. One highly relevant end-screen video element (never a random upload).
3. One playlist element (Too Close / Hidden Tricks).
4. Subscribe element.

## Publishing cadence (ops/content-calendar.md)

- 1 long/week + 2 Shorts, series-ordered: 3–4 × Too Close → 1 × Hidden Tricks → repeat.
- Long-form: 4–6 pm US/CA (TV-heavy 55+ audience). Shorts: mobile peaks (12 pm / 7 pm).
- After publish: pin comment immediately, reply to early comments within 2 hours, log 1 h
  metrics in `ops/metrics-dashboard.md`.

## Pre-publish

Run `ops/upload-checklist.md` top to bottom. It is the only authority for "ready to publish" —
if a box won't tick, the video doesn't ship.

## Monetisation guardrails (reused-content + rights)

- The channel-level product is *commentary + story + forensic insight* — never clip uploads.
- Every clip `cleared` in `ops/rights-ledger.csv` (renders refuse otherwise).
- AI narration/edits don't need the altered-content label; synthetic realistic media does.
- Policy links: [reused content](https://support.google.com/youtube/answer/1311392),
  [altered content](https://support.google.com/youtube/answer/14328491).
