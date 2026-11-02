---
name: editor
description: |
  Edit caught-on-camera storytelling/commentary videos for Monarch Cam — shot selection,
  pacing, narration sync, captions, title/end cards. Use when building an EDL, assembling a
  long-form master or Short, or reviewing a cut before package.
---

# Editor — commentary video craft

Editing is where a clip dump becomes a Monarch Cam product. Reference craft distilled from
**digitalsamba/claude-code-video-toolkit** (MIT, ffmpeg/moviepy skill structure),
**Vincentwei1021/video-shotcraft** (Apache, 152 shot recipe cards),
**Vincentwei1021/video-talkcraft** (PolyForm Noncommercial — concepts only: word-level VO
sync, "anti-PPT" layered shots), and **s1dashu/director** (MIT, mode-based directing).

## Our render stack (already built)

| Tool | Job |
|---|---|
| `tools/render_long.py` | 1920×1080 master from `edl.json` (cards, captions, VO mix, end screen) |
| `tools/render_shorts.py` | 1080×1920 Short (9:16 crop, burned captions, CTA card) |
| `tools/make_animation.py` | Motion-graphics segments (owned footage, auto-cleared) |
| `tools/extract_frames.py` | Frame grabs for forensics / thumbnail stills |

## The anti-PPT rule (from talkcraft's philosophy)

A commentary video dies when it becomes slides over footage. Every segment must have at least
ONE moving element: real clip motion, a slow push (zoom_callout), a caption change, or a
graph element arriving. Text is never naked on screen without visual proof beside it.

## Shot grammar for caught-on-camera storytelling

| Beat | Visual treatment |
|---|---|
| Hook (0:00–0:03) | Strongest 3 seconds of raw clip, full frame, no text yet (or 1 punch caption) |
| Story beats | Clip 5–15 s windows, cut on action; caption = the story line, not the transcript |
| Explainer beats | `zoom_callout` on the exact detail ("watch his ears"), `bar_reveal`/`text_pop` for data |
| Tension peak | Slow the pace (longer windows), drop caption count, lift raw audio |
| Handoff | Endcard + spoken next-video line |

## Pacing rules (blueprint §11–12)

- New visual or insight every 20–40 s. If an EDL segment runs >40 s without a change, split it.
- VO drives the timeline: each script beat = one EDL segment; `vo` laid at segment start.
- Clip audio ducked to `clip_gain ≈ 0.2` under narration; raw audio up to 0.6–1.0 for
  tension peaks where the raw sound IS the story.
- Caption windows: 2–3 s, ≤3 words for Shorts, ≤7 words for long-form.
- Cuts land on motion (a head turn, a step, a door) — never mid-stillness.

## VO sync discipline

1. Generate VO first, measure duration (`probe_duration`), then fit the clip window.
2. If VO runs long, trim the SCRIPT — never stretch a stale clip window with dead air.
3. Silence >1.2 s under narration = a beat is missing; fill with insight or cut.

## Quality gate before package

- [ ] Opens with proof, no logo intro
- [ ] Every caption grammatically complete (no dangling words)
- [ ] No banned phrases in any text-on-screen (run humanize_check on caption text too)
- [ ] Audio: VO clear above everything; no clipping; consistent loudness
- [ ] End screen: spoken handoff + card + 20 s window for YouTube end elements
- [ ] Rights: every segment is `cleared-*` in the ledger or `media/animations/` owned
