# 🚀 HANDOVER — NAYI SESSION YAHAN SE START KARO

**Pehle yeh padho**: `docs/SESSION-ARCHIVE-FULL.md` — poora session (har prompt, har
response, har result, recipes, mistakes, IDs) wahan hai. Yeh file sirf QUICK START hai.

## Kaunsa channel / kaam?
**Monarch Cam** (monetized YouTube) · Series: **"Caught on Camera — Explained"**
Agent khud clips dhoondhta hai → link share karta hai → user ka explicit **"haan"** aane
ke baad hi video build hoti hai (APPROVAL GATE). User Roman Urdu me baat karta hai — usi
me reply karo. Video content = natural English (55+ TV audience).

## ABHI KA STATE (2026-10-24)
- **SHORT-03 v8 DELIVERED** (Pick #1 = CPW Woodland Park bear) — `output/SHORT-03_FINAL_GFX.mp4`
  (27.4s, 1080×1920). Drive: `1RotQI4n8UK4H8r2uDpvTSoaha1TeDW6R`. User verdict PENDING.
- Upload kit (title/desc/tags/pinned) + category (**Pets & Animals**) already diya ja chuka hai.
- Git tip: `6309665`+ on branch **`arena/4cb3e8a5-world-channel`** (sirf isi branch pe kaam+push).
- Rights: CLIP-2026-006 = **PENDING** (credit CPW) — monetized publish se pehle clear karo.
- **NEXT**: (1) v8 ka verdict; (2) LONG video (render_long.py + make_animation.py) —
  lekin **kisi short me long-video CTA/link NAHI jab tak woh banti nahi**; (3) agli clips
  approval gate se.

## QUALITY QANOON (har render me)
1. RAW real footage only — NO watermark/GIF/low-res/news-package.
2. Subject/frame **kabhi block nahi** — elements creatively encircle/point karein,
   keyframed hon (smoothstep slides, draw-ons, staged timings) — **ZERO cheap stickers**.
3. SFX/BG premium + non-irritating (music style user-approved). VO = **voice-01**.
4. **Har render ke baad pixel-verify** (frames + numpy + zoom-matched base diff +
   audio spectral stats) → ALL PASS → deliver.
5. "bagair kisi kami ke" — zero-defect, kuch chore miss nahi.

## TECH (har turn fresh shell!)
```
pip install --quiet --target tools/_vendor imageio-ffmpeg pillow numpy
export PYTHONPATH=tools/_vendor   # har python/ffmpeg call me
FF=tools/_vendor/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
```
- `output/`, `tools/_vendor/`, `pipeline/forensics/frames/` = gitignored + turn pe WIPE.
- Clips download: sirf GitHub Actions downloader (`ops/clip-fetch-request.yml`) — bash curl
  x.com/video.twimg.com BLOCKED. `api.fxtwitter.com` se tweet/video URL nikalta hai.
- Git rewind ho jaye to: `git fetch origin && git reset --mixed origin/arena/4cb3e8a5-world-channel`.
- GFX apply hamesha BASE render (`output/SHORT-03_FINAL.mp4`) pe — GFX output pe nahi.
- Same file ko parallel edit_file mat karo (race) — SEQUENTIAL.

## KEY TOOLS
| Tool | Kaam |
|---|---|
| `tools/render_shorts.py` | EDL → vertical short (captions, VO, music, CTA) |
| `tools/sound_design.py` | cinematic audio bed (ticks/subdrop/heartbeats/risers/duck/drive) |
| `tools/keyframe_elements.py` | keyframed PNG motion-graphics compositor (spec JSON) |
| `tools/extract_frames.py` + numpy | verification |
| `tools/intake_register.py` | clip + rights ledger entry |
| `tools/render_long.py` + `make_animation.py` | LONG video (abhi pending) |

## SPEC FILES (SHORT-03)
- EDL + audio: `pipeline/produce/SHORT-03/v2/{edl,audio_plan}.json`, `vo.mp3` (voice-01, 23.38s)
- GFX spec: `pipeline/produce/SHORT-03/v2/gfx_spec.json` (78 elements — v8)
- Master clip: `pipeline/produce/S03-clips/woodland_master_1440p.mp4`
- Package: `pipeline/package/SHORT-03-PACKAGE.md`

> Full detail, prompts, recipes, error log = `docs/SESSION-ARCHIVE-FULL.md` me. Wahan
> sab kuch hai — miss mat karna.
