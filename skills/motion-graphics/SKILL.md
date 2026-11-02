---
name: motion-graphics
description: |
  Design and render motion-graphics segments for Monarch Cam explainers — data reveals,
  callout zooms, text pops, diagrams. Use when a script beat needs an animation instead of
  (or over) a clip, or when building thumbnail/end-card art.
---

# Motion Graphics — explainer animation on demand

## Tier system

| Tier | What | Tool | When |
|---|---|---|---|
| **T0 (default)** | text_pop, bar_reveal, zoom_callout | `tools/make_animation.py` | Most explainer beats — ships in seconds |
| **T1** | Custom PIL frame animations (diagrams, maps, arrows, timelines) | PIL → ffmpeg (same frame pattern) | The concept needs a picture no clip shows |
| **T2** | Code-drawn cinematic animations | **3b1b/manim** (MIT, pip) | Math/physics-grade motion (rare for this niche) |
| **T3** | HTML/CSS scenes rendered to video | **heygen-com/hyperframes** (Apache) | When we want design-system-level graphics (next phase) |

Web animation libraries (**juliangarnier/anime**, **motiondivision/motion**) build web/UI
motion — use them only for channel site/asset work, never for video render.

## Brand motion language (blueprint §10)

- Base: charcoal-navy `#0E1620`. Accent: gold `#C9A227`. Type: white/grey, DejaVu Bold.
- Motion: ease-out settles (arrive, stop) — no bounce, no spin, no neon.
- One idea per animation. If it needs two, make two segments.
- Everything renders 30 fps, `yuv420p`, silent AAC track (so it drops into any EDL).
- Long-form safe area: keep text inside 82% width. Shorts captions: y≈30%, stroke ≥4 px.

## Recipes that already work

```bash
# Hook/intro card
python3 tools/make_animation.py text_pop --text "HE CAME BACK" \
  --sub "Four visits. One camera. One pattern." --duration 3 \
  --out media/animations/b01_hook.mp4

# Forensic data reveal (e.g. blueprint's own evidence)
python3 tools/make_animation.py bar_reveal --title "Same title formula. Different result." \
  --bars "Bear original|952" --bars "Shark copycat|7.7" --unit "K views" \
  --duration 4.5 --out media/animations/b04_bars.mp4

# "Microscope" moment on a frame from the clip
python3 tools/make_animation.py zoom_callout \
  --image pipeline/forensics/frames/CLIP-001/frame_0002.00.jpg \
  --label "Paw on the handle" --at 0.62,0.55 --duration 4 \
  --out media/animations/b02_callout.mp4
```

Then reference the file as a normal `clip` segment in `edl.json` (`media/animations/...` is
auto-cleared owned footage).

## T1 pattern (custom diagrams)

1. Design static PNG first — approve the composition before animating.
2. Animate one parameter per beat (position, alpha, or reveal-mask), eased.
3. `ffmpeg -framerate 30 -i f_%04d.png -f lavfi -i anullsrc=r=48000:cl=stereo ...` (same
   recipe as make_animation).
4. Total motion-graphics share of a long-form video: **≤15% of runtime**. Footage + story lead.

## Ideas worth stealing (references)

- **3b1b/manim** — build intuition by animating the *mechanism* (why a bear's route repeats).
- **MisterBooo/LeetCodeAnimation** — proof that step-reveal pacing teaches (our forensics
  beats: reveal → pause → explain).
- **video-shotcraft/talkcraft recipe cards** — treat each animation as a named recipe card in
  this skill so quality is repeatable.
