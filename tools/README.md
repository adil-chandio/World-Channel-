# Tools Reference

All tools run from the repo root. Python 3.10+. Dependencies:
`pip install imageio-ffmpeg pillow numpy` (ffmpeg comes bundled with imageio-ffmpeg).

## 1. `intake_register.py` — register a clip (run first, always)

```bash
python3 tools/intake_register.py \
  --file media/inbox/bear_door_ringcam_2025-11-02.mp4 \
  --source-url "https://example.com/original-post" \
  --rights written-permission \
  --credit "Jane Doe / Example Media" \
  --series too-close \
  --verified 2026-10-23 \
  --notes "ring cam, black bear at door, returns x4"
```

- Assigns `CLIP-YYYY-NNN`, writes `ops/rights-ledger.csv` row + forensic stub.
- `--rights` ∈ written-permission, licensed-stock, public-domain, cc0, cc-by,
  creator-submission, owned-footage, pending.
- Status is `pending` by default. Add `--cleared` only after real rights evidence is attached
  in the forensic report (or edit the CSV later).

## 2. `extract_frames.py` — forensics frames

```bash
python3 tools/extract_frames.py media/inbox/clip.mp4 --every 2 --out pipeline/forensics/frames/CLIP-2026-001
python3 tools/extract_frames.py media/inbox/clip.mp4 --at 1.5,3.2,7.0 --out pipeline/forensics/frames/CLIP-2026-001
```

## 3. `render_long.py` — assemble the long-form master

```bash
python3 tools/render_long.py pipeline/produce/BRIEF-01/edl.json
python3 tools/render_long.py pipeline/produce/BRIEF-01/edl.json --out output/custom.mp4
```

- Refuses any clip not `cleared` in the ledger (`--skip-rights-check` only for owned test footage).
- Output: `output/<ID>_long.mp4` (1920×1080, 30 fps, h264/aac).

### EDL schema (`edl.json`)

```json
{
  "id": "BRIEF-01",
  "title": "Why This Bear Kept Coming Back to the Same House",
  "width": 1920, "height": 1080,
  "music": null,
  "music_gain": 0.05,
  "segments": [
    {"type": "card", "text": "HE CAME BACK", "sub": "Monarch Cam", "duration": 2.0},

    {"type": "clip", "src": "media/clips/CLIP-2026-001.mp4",
     "in": 3.0, "out": 9.5,
     "clip_gain": 0.2,
     "vo": "pipeline/produce/BRIEF-01/vo/seg01.mp3",
     "caption": "He was not lost", "caption_start": 0.5, "caption_dur": 2.5},

    {"type": "endcard", "text": "WATCH NEXT: The Doorbell Camera Caught a Bear Learning Something New",
     "vo": "pipeline/produce/BRIEF-01/vo/end.mp3", "duration": 20.0}
  ]
}
```

- `in`/`out` are seconds **in the source clip**. `clip_gain` mixes original audio (0.2 ≈ ducked
  under narration; 1.0 = full raw).
- `vo` is per-segment narration audio, laid at the segment start.
- Caption times (`caption_start`, `caption_dur`) are **segment-local**.
- `card`/`endcard` segments render styled 1920×1080 cards (charcoal-navy + gold, Monarch brand).

## 4. `render_shorts.py` — build a 9:16 Short

```bash
python3 tools/render_shorts.py pipeline/produce/SHORT-01/edl.json
```

### Shorts EDL schema

```json
{
  "id": "SHORT-01",
  "segments": [
    {"src": "media/clips/CLIP-2026-001.mp4", "in": 12.0, "out": 19.5, "clip_gain": 1.0}
  ],
  "captions": [
    {"text": "He came back", "start": 0.3, "dur": 1.8},
    {"text": "FOUR times", "start": 2.1, "dur": 2.0}
  ],
  "end_cta": {"text": "FULL STORY ON MONARCH CAM", "dur": 1.4},
  "music": null, "music_gain": 0.15
}
```

- Caption times are **global** (seconds from the start of the final timeline).
- Captions burn at upper-middle (y≈30%), 76 px bold, mobile-safe.
- Output: `output/<ID>.mp4` (1080×1920, 30 fps).

## Media folders

- `media/inbox/` — raw clips as received (never edited; these are the ledger's raw backups)
- `media/clips/` — cleared working copies referenced by EDLs
- `output/` — rendered masters (git-ignored)

## 5. `humanize_check.py` — script AI-tell linter

```bash
python3 tools/humanize_check.py pipeline/scripts/BRIEF-01_LONG.md --min-score 70
```

- Pattern system adapted from [blader/humanizer](https://github.com/blader/humanizer) (MIT)
  + Monarch Cam blueprint §12 brand bans.
- Flags: Not-X-but-Y, one-line closers, fake-deep sayings, staged run-ups, arguing-with-no-one,
  stock AI words, banned hype phrases, "Imagine" openers, unverified "attack" usage.
- Score ≥ 70 = PASS (exit 0); below = exit 2. Run before every VO.

## 6. `make_animation.py` — motion-graphics segments

```bash
python3 tools/make_animation.py text_pop --text "HE CAME BACK" --sub "Four visits." --out media/animations/a.mp4
python3 tools/make_animation.py bar_reveal --title "..." --bars "Bear|952" --bars "Shark|7.7" --unit "K" --out media/animations/b.mp4
python3 tools/make_animation.py zoom_callout --image frame.jpg --label "The door handle" --at 0.6,0.5 --out media/animations/c.mp4
```

- 30 fps, yuv420p, silent AAC — drops straight into any EDL as a `clip` segment.
- Files under `media/animations/` are agent-owned footage and auto-cleared for renders.

## 7. `stock_broll.py` — rights-clean stock b-roll (Pexels/Pixabay)

```bash
export PEXELS_API_KEY=...   # free: https://www.pexels.com/api/
export PIXABAY_API_KEY=...  # free: https://pixabay.com/api/docs/
python3 tools/stock_broll.py search "black bear forest" --out media/broll
```

- Downloads into `media/broll/<query>/` and appends attribution rows to
  `media/broll/credits.csv`. Register downloads with `intake_register.py --rights licensed-stock`.
