# Monarch Cam — Full Production Pipeline

> **Concept:** *Caught on Camera — Explained.* We take real wildlife close-encounter clips and turn
> them into story-led, forensic-style explainer videos: what happened, what the camera actually
> shows, and why the animal did it. Long-form (7–9 min) and Shorts (9:16) from the same material.
>
> This pipeline is the operating system behind
> [`docs/MONARCH_WORLD_CHANNEL_MASTER_BLUEPRINT.md`](docs/MONARCH_WORLD_CHANNEL_MASTER_BLUEPRINT.md).

---

## 0. Who does what

| Job | Owner |
|---|---|
| Content planning, video briefs, content calendar | **Agent** |
| Finding clips (clip request lists, sources, rights status) | **Agent** |
| Downloading clips and uploading them to Google Drive | **You** |
| Pulling clips from Drive, registering, rights ledger | **Agent** |
| Deep forensic study of every clip (frame-by-frame, beat map, behaviour science) | **Agent** |
| Script (storytelling + explainer commentary, natural English) | **Agent** |
| Narration VO, edit decision list, assembly edit, captions, title cards | **Agent** |
| Shorts cutdowns (9:16, burned captions) | **Agent** |
| Titles, thumbnail, description, chapters, pinned comment, end screen | **Agent** |
| Final review, channel upload, community replies | **You** (agent preps everything) |
| Metrics tracking + iteration decisions | **Agent** |

One rule at the centre of everything: **the finished video must be a Monarch Cam original
product** — narration, storyline, factual context, selection and sequencing — not a clip dump.

---

## 1. PIPELINE STAGES

### Stage 1 — PLAN (agent)
- `ops/content-calendar.md` drives what gets made and when.
- Every video starts as a **brief** in `pipeline/briefs/` (idea, promise, structure, required clips).
- Launch run follows the blueprint: 3–4 × `Too Close: Wildlife in Human Space`, then 1 ×
  `Nature's Hidden Tricks`, then back. Never random mixing.

### Stage 2 — FIND (agent finds, you download)
- Agent maintains `pipeline/finding/CLIP_REQUESTS.md`: exactly which moments we need, per brief,
  with source leads and rights-first sourcing order (permission → licensed → PD/CC → submissions).
- Discovery + verification method: [`skills/researcher/SKILL.md`](skills/researcher/SKILL.md)
  (Reddit/X/YouTube-transcript search via Agent-Reach, attention-scored trends, rights tracing).
- Rights-clean b-roll gaps: `python3 tools/stock_broll.py search "<query>"` (Pexels/Pixabay,
  credits auto-recorded in `media/broll/credits.csv`).
- **You** download the clips.
- **You** upload raw clips to the Drive intake folder (see §3).

### Stage 3 — INTAKE (you → Drive, agent → register)
- Agent pulls files from Drive, stores raw copies in `media/inbox/` (never edited — these are the
  raw backups required by the rights ledger).
- `tools/intake_register.py` assigns a `CLIP-YYYY-NNN` ID and writes a row in `ops/rights-ledger.csv`
  and a forensic stub in `pipeline/forensics/`.
- **A clip with `rights_status = pending` can never reach a render.** The render tool refuses it.

### Stage 4 — FORENSICS (agent) — the "microscope"
For every clip, `pipeline/forensics/CLIP-*.md` records:
- provenance (origin, uploader, date, whether it's the raw original or a re-upload)
- second-by-second beat map (timestamps, what is visible, what is claimed)
- what is **really** happening (species behaviour, body language, context the frame hides)
- claims check: every factual statement we plan to voice, with a source or "not verifiable — cut"
- usable window (in/out), best 3-second proof moment for the hook
- risk flags (distress, harm, minors, private property, advertiser-unfriendly)
- `tools/extract_frames.py` produces the frame set used for the study.

### Stage 5 — SCRIPT (agent)
- `pipeline/templates/SCRIPT_LONG.md` / `SCRIPT_SHORT.md` enforce the blueprint tone rules:
  natural mature English, one promise, proof in the first 3 seconds, a new beat every 20–40
  seconds, calibrated language (no "attack" overclaiming, no "silent death" cheese).
- Humanize pass: [`skills/script-humanizer/SKILL.md`](skills/script-humanizer/SKILL.md) +
  `python3 tools/humanize_check.py <script>` must **PASS** (score ≥ 70) before VO.
- Every script line that states a fact cites the forensic report; anything unsourced is cut.
- Short script is **not** a recap — it is one moment, one question, one payoff, plus the
  "full story" cue.

### Stage 6 — PRODUCE (agent)
1. Narration VO generated per script segment (`narration/` folder).
2. `edl.json` written: segments, in/out, clip gain, captions, title card, end screen
   (schema: `tools/README.md`). Editing craft rules:
   [`skills/editor/SKILL.md`](skills/editor/SKILL.md) — anti-PPT, cut-on-action, VO sync.
3. Explainer beats that need animation: `tools/make_animation.py` (text_pop / bar_reveal /
   zoom_callout) or custom tier per
   [`skills/motion-graphics/SKILL.md`](skills/motion-graphics/SKILL.md) — animations under
   `media/animations/` are owned footage and auto-cleared.
4. `tools/render_long.py` builds the 1920×1080 master: trim → scale/pad → captions →
   VO over ducked clip audio → title card → end screen → optional music bed.
5. `tools/render_shorts.py` builds 1080×1920 Shorts: center 9:16 crop, big burned captions,
   1-second "Full story on Monarch Cam" end cue.

### Stage 7 — PACKAGE (agent)
`pipeline/package/<VIDEO-ID>-PACKAGE.md` delivers the upload-ready kit per
[`skills/youtube-ops/SKILL.md`](skills/youtube-ops/SKILL.md):
- 3 title options (standalone — never "Part 2"), thumbnail brief + generated thumbnail,
  description with first-line long-video link, chapters, pinned comment, end-screen plan
  (spoken handoff + one relevant video + one playlist + subscribe).

### Stage 8 — UPLOAD & TRACK (you click, agent watches)
- Upload checklist: `ops/upload-checklist.md` (all boxes before publish).
- Metrics logged in `ops/metrics-dashboard.md` at 1h / 24h / 7d with the blueprint diagnostic rules.

---

## 2. Two formats, one material

| | Long-form | Short |
|---|---|---|
| Length | 7–9 min | 25–55 s |
| Promise | The full story + the explainer | One moment + one question |
| Structure | Hook proof → story → forensic explainer → context → handoff | Hook → payoff → "full story" cue |
| Audio | Narration-led, clip audio ducked | Clip audio + music, captions carry the story |
| Destination | End screen + playlist | Pinned comment + description line → long video |

Every Short is cut from a long-form story (or is the teaser for an upcoming one). No orphan Shorts.

---

## 3. Folder conventions

### Google Drive (you upload here)
```
Monarch Cam Production/
  01-Clips-Inbox/          ← YOU drop raw clips here (name them: topic_source_date.mp4)
  02-Finished/             ← agent puts ready-to-upload masters here
  03-Thumbnails/           ← agent puts final thumbnails here
  04-Package-Notes/        ← titles, description, checklist per video
```

### Local repo (agent works here)
```
media/inbox/               raw clips, untouched (rights-ledger raw backup)
media/clips/               cleared working copies
pipeline/briefs/           video briefs
pipeline/finding/          clip request lists
pipeline/forensics/        per-clip forensic reports + frames/
pipeline/scripts/          long + short scripts
pipeline/produce/          per-video edl.json + narration/
pipeline/package/          upload kits
output/                    rendered masters (git-ignored)
ops/                       rights ledger, calendar, dashboard, checklists
tools/                     intake / forensics / render tooling
```

---

## 4. Rights, monetisation, and reused-content guardrails

These are not bureaucracy — they are what protects a **monetised** channel:

1. **Rights ledger first.** Every clip needs source URL, rights type, verification date, credit,
   and a kept raw copy (`ops/rights-ledger.csv`). A copyright disclaimer is not clearance.
2. **Render is locked to cleared clips.** `render_long.py` / `render_shorts.py` read the ledger and
   refuse anything not `cleared-*`.
3. **Transformation is the product.** Each video must visibly add: original narration, an editorial
   storyline, substantive cut/sequencing, sourced factual context, and visual explanation.
   This is exactly the standard YouTube applies at channel level for reused content
   ([policy](https://support.google.com/youtube/answer/1311392)).
4. **Calibrated language.** "Attack", "charged", "aggressive" only when the footage supports it.
5. **Distress & harm.** No animal-harm shock compilations; flag distress clips in forensics and
   use them only with editorial justification, non-graphic framing.
6. **AI disclosure.** If synthetic realism is ever used, follow
   [YouTube's altered-content rules](https://support.google.com/youtube/answer/14328491).
   Routine edits/captions/narration do not need the label.

## 5. Quality bar (from the master blueprint)

- **0:00–0:03** show the strongest visual proof. No logo intro. No "Imagine..." open.
- New visual or insight every 20–40 seconds.
- TV-safe: big clean 16:9, legible text, narration above music.
- Every video ends with a spoken next-video handoff + end screen + playlist + pinned comment.
- Titles standalone, one promise, natural English. Never "Part 2/3/4".
- Run at least 4 adjacent wildlife long videos before judging results.

## 6. Skills layer

Agent skills loaded for each stage (adapated from the open-source landscape — see
[`docs/TOOLING_REVIEW.md`](docs/TOOLING_REVIEW.md) for full verdicts):

| Skill | Stage | Origin |
|---|---|---|
| `skills/researcher/` | 2–4 | last30days-skill, Agent-Reach, gpt-researcher |
| `skills/script-humanizer/` | 5 | blader/humanizer (MIT) + blueprint tone rules |
| `skills/editor/` | 6 | claude-code-video-toolkit, shotcraft/talkcraft concepts, director |
| `skills/motion-graphics/` | 6 | manim, hyperframes, recipe-card method |
| `skills/youtube-ops/` | 7–8 | MoneyPrinterTurbo (concepts), youtube-automation-agent |

## 7. Tool reference

See [`tools/README.md`](tools/README.md) for CLI usage of:
`intake_register.py`, `extract_frames.py`, `render_long.py`, `render_shorts.py`,
`humanize_check.py`, `make_animation.py`, `stock_broll.py`.
