# SHORT-03 — "At 3 AM, He Opens The Door Anyway (Caught on Camera)"

Status: FINAL build pending render + verify. Source clip **user-approved** (PICK #1, 2026-10-23).

## Source clip (CLIP-2026-006)
- **What:** Woodland Park, Colorado. Just before 3 AM (Friday 2023-06-02; posted 2023-06-05).
  Black bear walks up to a parked truck, stands on hind legs, opens the door by the
  handle, glances toward the surveillance camera, pauses, and continues. CPW confirms
  **no food was inside** — learned behavior.
- **Source:** CPW SE Region (Colorado Parks & Wildlife) official X post —
  https://x.com/CPW_SE/status/1665762810909847552 (thread 1/2, video)
- **File:** `pipeline/produce/S03-clips/woodland_raw_720p.mp4` — 1280x720 h264 29.97fps,
  31.55s, AAC stereo (surveillance audio). RAW agency post: **no watermark, no text overlay**
  (verified: corner strips carry no static bright text band across frames).
- **Provenance notes:** Freeze/stall at 26.0–27.5s (surveillance frame drop) — styled as the
  "he pauses" beat in the hook. Real clip, non-AI: agency-origin + multiple independent
  newsroom descriptions (KKTV, Idaho Statesman, fox21, NBC Washington) match frame content.

## Forensic beat map (from motion/brightness analysis of raw clip)
| t (raw) | event |
|---|---|
| 0–5s | bear approaches past camera zone (IR scene bright, slow drift) |
| 6–12s | bear close to camera, moving toward truck (dark mass, high motion) |
| 14–19s | transit + standing at truck (large jump cut at 14s = camera frame gap) |
| 20–27.5s | handle work → door opens → **26.0–27.5s frozen pause (camera-glance moment)** |
| 28–31.5s | at/inside the vehicle (darkest, largest dark mass) |

## Edit (blur-pad 1080x1920, full frame always visible)
1. **s1_hook 22.0–27.5** — handle pull → pause. Captions: "NO FOOD INSIDE." / "HE OPENS THE DOOR ANYWAY."
2. **s2_approach 6.0–12.0** — rewind: how he arrives. "3 AM. COLORADO." / "THIS ISN'T HIS FIRST TIME."
3. **s3_handle 14.0–19.5** — working the door. "BEARS LEARN WHERE THE FOOD IS." / "THEY NEVER FORGET."
4. **s4_inside 27.5–31.5** — the warning. "ONE DAY: THE WRONG DOOR."
5. End card: "FULL STORY ON MONARCH CAM" (1.5s)

## VO (voice-00, ~49 words)
> A parked truck. No food inside. He opens the door anyway. Three in the morning,
> Colorado. He has done this before. Bears learn where the food is, and they never
> forget. Wildlife officers warn: one day, he'll meet an occupied car. And pay the
> ultimate price.

Facts sourced from CPW's own statements (no overclaim): "learned to open car doors",
"repeat the behavior even when no food is inside", "enter an occupied car or home and it
will pay the ultimate price".

## Rights (honest)
| id | credit | status |
|---|---|---|
| CLIP-2026-006 | Colorado Parks & Wildlife — CPW SE Region (@CPW_SE / @COParksWildlife) | **pending** — public agency post with safety message; credited in package; confirm repost terms before monetized use |

Render uses `--skip-rights-check` (disclosed). Preserve raw frame as-is (no source
watermarks exist to preserve — agency original).
