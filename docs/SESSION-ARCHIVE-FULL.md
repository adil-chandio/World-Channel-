# MONARCH CAM — COMPLETE SESSION ARCHIVE (Day 0 → v8)
### Session era: 2026-10-22 → 2026-10-24 (Asia/Karachi) · Branch: `arena/4cb3e8a5-world-channel`
### Purpose: ek nayi chat/session is file padh ke BILKUL isi workflow, quality bar, mindset
### aur response standard se aage badhe — koi detail miss nahi.

---

# PART A — AGAR TUM NAYI CHAT HO TO PEHLE YEH PADHO (HANDOVER)

1. **Language**: User Roman Urdu/Hindi me baat karta hai — USI me reply karo. Video content ki language = natural English (TV-heavy 55+ bear-watchers audience).
2. **Quality bar (non-negotiable)**: "best perfect high quality", premium, top-notch, ZERO cheap/cringe, ZERO copy-paste stickers, creative keyframed editing, subject/frame kabhi block nahi hona chahiye, lekin elements LAANE hain (rings/effects/animations) — creatively adjust karke. "bagair kisi kami ke galati ke flaws ke bagair kuch chore miss kiye".
3. **Approval gate**: har nayi clip ke liye pehle LINK share karo, user ka explicit "haan" aane ke baad hi build karo.
4. **Raw only**: raw real viral footage, NO watermark, NO burned-in text/captions/branding (jo video me pehle se ho). News packages = disqualified.
5. **CTA rule**: long video ABHI NAHI bani → kisi short me long-video CTA/link MAT do. Current CTA: "SUBSCRIBE - MONARCH CAM".
6. **Rights**: har clip ka rights ledger entry + credit. CLIP-2026-006 = PENDING (CPW) — monetized publish se pehle clear karna hai.
7. **SFX/music**: premium, engaging, hooked, NON-irritating ("kanon ko chubne wale" nahi). Music style v2+ user-approved.
8. **Verification mandatory**: har render ke baad pixel-level checks (frames + numpy), audio spectral stats, subject-safety diff — phir hi deliver karo.
9. **Environment (har turn fresh)**: `bash` shells fresh hote hain; `tools/_vendor` + `output/` + `pipeline/forensics/frames/` turn boundaries pe WIPE hote hain (gitignored). Har turn: `pip install --quiet --target tools/_vendor imageio-ffmpeg pillow numpy` + har python/ffmpeg call me `PYTHONPATH=tools/_vendor`. ffmpeg binary: `tools/_vendor/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2`.
10. **Git**: sirf branch `arena/4cb3e8a5-world-channel` pe kaam, wahi push. Snapshot restores local git refs rewind kar sakti hain → `git fetch origin && git reset --mixed origin/arena/4cb3e8a5-world-channel` phir commit+push. Final GFX deliverable = `output/SHORT-03_FINAL_GFX.mp4` (base render = `output/SHORT-03_FINAL.mp4`).
11. **Clip download**: bash curl x.com/video.twimg.com BLOCKED hai — sirf GitHub Actions downloader (`ops/clip-fetch-request.yml` edit → push → run `fetch-clip.yml` → `git pull`) se clip aati hai. `api.fxtwitter.com/status/<id>` se tweet/video URL extraction hota hai (fetch_page se).
12. **Mindset**: "next level lejake" — har round me enhance/improve karo, tools banao (reusable), pixel-proof do, package ready rakho.

---

# PART B — PROJECT IDENTITY

- **Channel**: Monarch Cam (monetized YouTube), series: **"Caught on Camera — Explained"**.
- **Mission (user ke 3 tasks)**:
  1. COMPLETE — "Caught on Camera — Explained" production system banana (monetized channel ke liye).
  2. COMPLETE — User ke ~33 GitHub repos me se SIRF perfect-fitting tools integrate karne the ("perfectly" fitting — evaluate, don't adopt wholesale).
  3. ACTIVE — Agent khud RAW REAL VIRAL clips dhoondhe, link share karke approval le, phir videos banaye.
- **Master blueprint**: `docs/MONARCH_WORLD_CHANNEL_MASTER_BLUEPRINT.md` — rules: no "Part 2/Part 3" headline titles, rights ledger per clip (generic disclaimer ≠ rights clearance), proof-first 3-second openings, natural English 55+ audience, 4 adjacent videos banane se pehle channel reset judge mat karo. EXCEPTION (user ne suspend kiya): "every Short links to a long video" rule — jab tak long video nahi banti.

---

# PART C — COMPLETE TIMELINE (prompt → response → result)

## PHASE 0 — SESSION START (2026-10-22)
**User prompt (mission)**: "Caught on Camera — Explained" production system + ~33 repos se tools integrate + khud clips dhoondhna (verbatim order neeche Phase 5 me hai).
**Agent**: Repo `adil-chandio/World-Channel-` clone hua `/home/user/World-Channel-` me, branch `arena/4cb3e8a5-world-channel` (base commit `2405695f9a13b90c382706a32a953ee38e806a1b`). Repo structure banaya: README.md, PIPELINE.md, docs/ (blueprint + tooling review), skills/, tools/, pipeline/ (produce/package/finding/forensics), ops/, media/inbox/.

## PHASE 1 — PRODUCTION SYSTEM BUILD
**Agent actions**:
- `docs/MONARCH_WORLD_CHANNEL_MASTER_BLUEPRINT.md` — channel strategy, series format, rights policy, tone.
- `PIPELINE.md` — end-to-end production flow (intake → forensics → script → VO → sound → render → verify → package).
- `tools/vidlib.py` — shared ffmpeg helpers (`ffmpeg_exe()`, `run()`).
- `tools/render_shorts.py` — EDL-based vertical shorts renderer. EDL schema: `{id, segments:[{src,in,out,clip_gain}] (src repo-relative), captions:[{text,start,dur}], end_cta:{text,dur}, vo/vo_gain, music/music_gain}`. Captions PIL `make_caption` (y_frac=0.30, font 76). FILL center-crops 16:9 (isliye raw 16:9 kabhi directly mat feed karo — pehle portrait crop/frame banao). Video-only clips pe crash hota hai (mux anullsrc). .mp3 = libmp3lame. PIL cards ke liye fps=30,format=yuv420p. ENC crf18 (v4 se pehle crf20 tha).
- `tools/make_animation.py` + `tools/render_long.py` — LONG video tooling (banned words: attacks/vicious/crazy/monster).
- `tools/stock_broll.py`, `tools/intake_register.py` (CLI: `--file --source-url --rights {…pending} --credit --series shorts --verified --notes`), `tools/extract_frames.py`, `tools/humanize_check.py`.
- `ops/rights-ledger.csv` + `ops/clip-fetch-request.yml` + `.github/workflows/fetch-clip.yml` (reusable clip downloader).
**Result**: Production system READY.

## PHASE 2 — TOOL INTEGRATION (~33 repos review)
**Agent**: `docs/TOOLING_REVIEW.md` me sab repos evaluate kiye; sirf genuinely fitting tools liye (vidlib/render/sound/forensics utilities). Wholesale adoption NAHI kiya. Custom gaps ke liye khud tools likhe (sound_design.py, keyframe_elements.py baad me aaye).

## PHASE 3 — DRIVE SETUP + VOICE-00 + SHORT-01 (V14)
**Agent actions**:
- Google Drive me folders banaye (IDs Part H me). Voice-00 narrator banaya (generate_speech).
- **SHORT-01 = V14 tak iterate** (14 versions!) → final render + package + Drive upload.
**Result**: SHORT-01 delivered. (Baad me SHORT-03 ke liye voice battle hui — neeche.)

## PHASE 4 — SHORT-02 = GIF ROUTE → ❌ REJECTED (2026-10-23)
**Agent**: Tenor/Giphy GIFs + low-res web images se video banaya.
**User verdict**: "**bekar**" + standing order: kabhi GIF/low-res route NAHI. Quality bar = "best perfect high quality" sirf REAL RAW footage se.
**Lesson (LOCKED)**: GIF/Tenor-Giphy/low-res image route = PERMANENTLY BANNED.

## PHASE 5 — CLIP SEARCH WAVES + APPROVAL GATE
**User prompt (verbatim)**: "best perfect high quality wali 1 viral video utao Kahi se bhi internet se Reddit se social media se then mujhse link share Karke approval lo agar clip perfect hui to Aage barhenge ham agar me han kahunga"
**User prompt (verbatim)**: "raw real viral koi watermark text na ho cheezen na ho high quality me or ache se next level lejake"
**User correction (verbatim, 2026-10-23)**: "yeh clip drive se Uthai hena to yeh nhi krna clip dhundke lao" → Drive se clips NAHI uthani, khud web se dhoondhni hai.
**Agent**: Multiple search waves (newsflare, ViralHog, UPI, KTLA, KSL, YouTube raw uploads, X posts). Candidates + provenance notes banaye. AI-fake warnings detect kiye (people.com 11829794 = AI grandma-bear 44M views; VEO "dog brings bear home"; bunny trampoline "Ring" 203M = AI) → mandatory provenance check rule bana.
**Pick #1 presented**: CPW Woodland Park clip `https://x.com/CPW_SE/status/1665762810909847552` — bear car door kholta hai, pause karke camera dekhta hai.
**User verdict (verbatim)**: "Pick 1 approved Aage barho" ✅

## PHASE 6 — CLIP DOWNLOAD + FORENSICS
**Agent actions**:
- fxtwitter extract: `api.fxtwitter.com/status/1665762810909847552` → video id `1665761033024331776`, 1280×720 mp4 `https://video.twimg.com/ext_tw_video/1665761033024331776/pu/vid/1280x720/dQJoscHhWqxV17dU.mp4?tag=12`.
- GitHub Actions downloader run **40025595271** (bash curl blocked!) → `pipeline/produce/S03-clips/woodland_raw_720p.mp4` (**31.551s, 1280×720, 29.97fps, RAW**), commit `04b3ee0`.
- Forensics "microscope": beat map banaya — **6-12s approach, 14-18s truck ki taraf, 20-25.5s door work, 26.0-27.5s FROZEN = camera-glance ("the pause"), 28-31.5s inside**.
- `pipeline/forensics/CLIP-2026-006.md` + `ops/rights-ledger.csv` entry: **CLIP-2026-006 = pending**, credit **Colorado Parks & Wildlife (CPW SE Region)**. Source context: thread 2/2 (`1665762814890479617`) = CPW warning "Eventually, this bear will enter an occupied car or home and it will pay the ultimate price." + kktv.com article "Video courtesy of Colorado Parks and Wildlife" (Woodland Park, camera glance, food-conditioning quotes = LONG video ka base).

## PHASE 7 — SHORT-03 BUILD CHAIN (v1 → v8)

### v1 (commit 307f9a6) — 22.5s first build
**Agent**: beat map se EDL banaya, voice-00 VO, render, package, Drive upload (1cdxBk2awp6SNtLIfCGTolD7YciI1iNqK / 1ffzZuxuvLxzKzCl2h-af5KRtTdsm9PhW).
**User verdict (verbatim)**: "NAHI Maza NAHI arha ha na hi commentary me na hi Voice me na hi editing me or next level enhance improve karo best sound effects bg music ache se hooked engaging bas yaad rakho irritating na ho" ❌
**Standing bar set**: punchy/hooked commentary, engaging VO, dynamic editing, best SFX + BG music, NEVER irritating.

### v2 (commit e64f9e2) — 21.3s enhancement
**Agent**: `tools/sound_design.py` banaya (cinematic bed synthesizer — events: **impact/riser/whoosh/heartbeat/pulse/pluck/tick/subdrop** + `--vo` ducking + tanh `drive` soft-clip; usage: `PYTHONPATH=tools/_vendor python3 tools/sound_design.py <plan.json> --vo vo.mp3 --out bed.wav`). Duck bug fix kiya. Punch-in segments banaye (ffmpeg animated crop x/y expressions — zoompan unreliable hai). voice-00 VO 17.32s. audio_plan v2. Render 21.3s. Verify ALL PASS. Drive upload (1P-2xjt4Q3mO-cT1vDS_wa6cdJ5pz21f4 / 1KyfJ-lnKW5kCj5Ohab0JoxassQH93Bkc).
**Also**: add_voice battle "01" launch (do candidates, user ne suna).

### Voice battle → **voice-01 WINNER** ✅
**User vote**: voice-01 pasand. Ab voice-01 = default narrator (voice-00 = purana default).

### v3 (commit 09865dd) — 27.4s re-time
**Problem**: voice-01 VO = **23.38s** but timeline 21.3s thi → VO cut off! (amix duration=first).
**Fix**: word-proportion map se PURA timeline re-time → **27.4s**. Segments raw se rebuild (crf16): s1a 19.5-26.8 punch 1.5x, s1b 26.0-27.5 SLOW-MO (setpts 1.67 + atempo 0.6) punch 1.65x = "THE PAUSE", s2 5.5-12.5, s3 13.3-19.3, s4 27.3-30.1. sound_design rerun. Render → verify (peak 0.596, bear all frames). Drive upload (1MRqK40aL1XEecGpMptXRF_mQZ9awrvpA / 16Z7dEP7icIzz0p4GrpdGdRuywnp_w8KW).
**User verdict (verbatim)**: "video clip quality ko sound effects ko improve karo baqi music sahi ha premium next level mazedar audience ko rok kar Engaging hooked stuck rakhne wale sound effects na ki irritating kanon ko chubne Wale or ache se editing" → music APPROVED ✅, clip quality + SFX + editing push karo.

### v4 QUALITY-OVERDRIVE (commit 3975498) — 27.4s enhanced master
**Agent**:
- **1440p enhanced master** banaya: raw → `hqdn3d=3:2:4:4,scale=2560:1440:flags=lanczos,unsharp=5:5:0.55:5:5:0.0,eq=contrast=1.08:saturation=1.18:gamma=1.02,cas=0.45` (crf15) = `pipeline/produce/S03-clips/woodland_master_1440p.mp4`.
- sound_design v2: softer impacts/no click, **tick @ har caption onset** (gain 0.26-0.30, pan ±0.25-0.3), **subdrop@7.3** (dur 1.2, gain 0.55), heartbeats@7.9/8.9/9.7, riser@19.4→warning impact@22.75, CTA impact@25.55 freq44, duck {0.66,0.12,0.5}, peak 0.62, drive 1.3.
- **Parallax drift editing**: har segment me blur-pad bg (boxblur 24:6, brightness -0.06) + fg me animated crop x drift (s1a '30*t/7.3', s1b '20*t/2.5', s2 '44*t/7.0', s3 '36*t/6.0', s4 '18*t/2.8').
- CTA change: user order — long video nahi bani → CTA = **"SUBSCRIBE - MONARCH CAM"** (short-only). User verbatim: "Jo cta derhe hen ham long video ka woh nhi Karna ha q ke abhi tak hamne NAHI banai long video … bas Jahan tak ha Wohi rakho short ke hsiab se".
- Verify: peak 0.598, spectral centroid 2083 Hz, <7% energy >8 kHz (non-harsh), bear visible all checked frames. **ALL PASS**.
- Drive: 1wJT4PpKaZUADtbkIF6je290G9RxE4tIX / 1EZIq0bGDKcwYZ6unM-I3N2frQ5qJFxj4.

## PHASE 8 — YOUTUBE UPLOAD KIT + CATEGORY (2026-10-24)
**User prompt (verbatim)**: "Ok ab mujhe yt par upload Karne ke Liye hamare us monetize channel par iske Liye short ke Liye title description lkh ke do viral"
**Agent delivered (COPY-PASTE KIT)**:
- TITLE (recommended): `At 3 AM, He Opens The Door Anyway (Caught on Camera)` (2 more options diye: curiosity variants).
- DESCRIPTION (final): "Three in the morning. Everyone's asleep. Except him. He doesn't break the window. He doesn't force the lock. He opens the door — like he's done it a hundred times. And then he pauses, right at the camera. No food inside. Doesn't matter. Colorado Parks and Wildlife says this bear has LEARNED what cars mean — and he keeps coming back. Once a bear connects cars with food, they never forget. Subscribe to Monarch Cam for more caught-on-camera wildlife moments. 🐻 Footage: Colorado Parks and Wildlife — CPW SE Region (@CPW_SE on X). Original post: https://x.com/CPW_SE/status/1665762810909847552 Used with credit for commentary/education. #shorts #bear #blackbear #caughtoncamera #wildlife #colorado #bearcountry #bears #caughtoncam #monarchcam"
- PINNED COMMENT: "The pause at the camera gets me every time 😳 This is what food conditioning looks like — not hunger, a habit. Source: Colorado Parks & Wildlife. Where should the next caught-on-camera episode come from? 👇"
- TAGS: bear, black bear, bear opens car door, caught on camera, wildlife, colorado, food conditioning, CPW, bear country, ring camera, surveillance, animal video, monarch cam
**User prompt (verbatim)**: "Iski category pets and animals rKhen ya entertainment"
**Agent verdict**: **Pets & Animals** ✅ (Entertainment nahi) — algorithm fit (wildlife ke saath recommend), search/browse traffic, channel identity. Bonus: channel ki main category bhi Pets & Animals set karo (YouTube Studio → Settings → Channel).

## PHASE 9 — GFX / KEYFRAMED ELEMENTS (v5 → v8)

### v5 (commit 2bfaccb) — first GFX layer
**User prompt (verbatim)**: "Acha ab na isme editing lao clip me theek ha clip ko or usme effects editing pngs elements lao unhen keyframing Karke lagao ache se effects ke sath yeh sab isi video me karo is video ko or Enhance improve Karke banao"
**Agent**: `tools/keyframe_elements.py` banaya (keyframed PNG compositor). PIL se PNG elements generate kiye: timestamp "3:02 AM · WOODLAND PARK, CO", REC dot, viewfinder corners, red ring, glow, arrow, warning triangle, credit bar, vignette, flashes + camera shakes. ffmpeg overlay chain se composite (fades, fly-ins, blink, enable windows).
**Bugs mile & fix kiye**: (1) PIL rectangle x1<x0 negative direction crash → sorted coords; (2) polygon width kwarg risky → line outline; (3) **vignette UI ke upar aa gaya** → order fix (vignette first); (4) verification frame-mapping bug.
**Result**: 13 elements. Drive: 1MsouyUvQxCbfMMofHt9Gzrq3Qe0NVdCE / 1j5wIsgtN5KNk_xuJ9gSIRxLMF7lCL78a.

### v6 (commit 3ca6ebd) — CLEAN PREMIUM
**User prompt (verbatim)**: "Theek ha Lekin yaad rakho sab se pehle to cheezen elements wagera main frame me uske upper nhi aani chaiye usse disturb ma Karen ke Sara Maza kahrab hojaye or hamen jitna hosake clean Lekin engaging hooked Wala kaam Karna ha or cheap cringe Pana NAHI tip notch premium high level quality Wala kaam editing animations wagera ach ese to us hsiab se or next level lejake or Enhance improve Karke Aage BAHDO perfectly correctly accurately next level"
**Agent**: saare over-frame elements hata diye (ring/glow/arrow/triangle) → sirf EDGES pe chrome (timestamp, REC, thin corners, animated progress line (30 chunks growth), quiet CPW credit, vignette + micro flashes 3.5px shakes). 
**Bugs fix**: (1) parallel edit_file race on same file = edits lost → SEQUENTIAL edits rule; (2) shake string-concat bug (`"24"+"0+if"` = `"240"` → crop clamped!) → shake strings empty init; (3) `crop:eval` option is ffmpeg build me nahi hai → progress = chunked enable overlays; (4) transform discovered: output = overlay_pos×1.0443−(24,42) (scale+crop ka effect) — har element position isse calibrate karni hoti hai.
**Result**: subject 0px disturbance (pixel-verified). Drive: 1VRmG_9Y4kUR7xTmkprHFio1b1DiyfFJC / 18dzcM50EOOo-evQ2OW2-PnD249Vg2zzZ.

### v7 (commit 4b74957) — CREATIVE FORENSIC
**User prompt (verbatim)**: "Aby NAHI yeh elements wagera laane hen Lekin is Tarah se jese main hamara subject frame kharab na ho bas hamara kaam bhi hojaye and Kuch kahrab bhi na ho ache se adjust Karke animations keyframing ke sath effects ke sath or high level quality editing ke stah na ki seedha uthake Laga diya copy paste Wala kaam nhi Karna creativity editing ache se dikhni ha keyframing wagera perfectly correctly accurately next level bagair kisi kami ke galati ke flaws ke bagair kuch chore miss kiye kisi kami ke"
**Agent**: elements WAPAS laye PAR subject-safe + creative: **analytic ring AROUND subject** (encircle, cover nahi), **spotlight isolation** (dark surround + soft hole around bear = subject POP), **4 staged lock-on brackets** (subject bbox corners pe, 0.04s stagger), **margin callout arrow** (tip subject se 20px pehle rukta hai), slim warning triangle, **draw-on red underlines** (8-chunk growth) key captions ke neeche. Pura tool rewrite (single write_file — race bug avoid).
**Verification**: zoom-matched base (`scale=1128:2005,crop=1080:1920:24:42`) se diff — **bear-zone diff 0.5-1.6 = subject untouched**, ring-band diff 14 = elements exactly gird. 60 elements. Drive: 1W-BZHqnjCubY_lAnXsYH7bZh6Y3s7Rh2 / 1l-GI2kNUOeuK0doIrDXSD-ioPhJqNwGJ.

### v8 (commit 6309665) — NEXT-LEVEL MOTION CRAFT ← CURRENT
**User prompt (verbatim)**: "Han yeh theek ha Lekin or ache se or enhance improve Karke or next level lejake banao"
**Agent upgrades (78 elements)**:
1. **Smoothstep easing** — har slide `p*p*(3-2*p)` curve se (buttery pro motion).
2. **Ring DRAW-ON** — 8 arcs 45° each, 0.05s stagger se ghoom ke draw (3.15→3.5s), phir glow ring bloom + beat-pulse@4.15.
3. **"0.5x SLOW" badge** — freeze pe right-margin se slide-in.
4. **Story beat-ticks** — bottom timeline pe 8 notches (har caption time pe fade-in) = retention structure.
5. **CTA light sweep** — soft diagonal shine (blurred white bar, -16° rotate) end card pe sweep (25.75→27.2).
**Verification**: bear diff 0.5-1.4 (CTA pe 2.0 = sweep intended), arcs partial@3.35 (1211px) → full@3.9 (1357/1371px), badge 2324px, ticks 3008px, sweep delta 4.35. **ALL PASS.**
**Drive**: **1RotQI4n8UK4H8r2uDpvTSoaha1TeDW6R** (video) / **1vcHVpbfYiav-gwhxFqSvq8V_Jd3V6liD** (package).
**User prompt (current)**: poora session archive repo me push karo → yeh document.

---

# PART D — SHORT-03 FINAL STATE (v8) — EXACT SPECS

**Deliverable**: `output/SHORT-03_FINAL_GFX.mp4` — 27.4s · 1080×1920 · 30fps · h264+aac crf18.
**Base render**: `output/SHORT-03_FINAL.mp4` (GFX SPEC KA INPUT — GFX dobara apply karna ho to BASE se karo, GFX output pe nahi!).
**Title**: "At 3 AM, He Opens The Door Anyway (Caught on Camera)".
**Build dir (committed)**: `pipeline/produce/SHORT-03/v2/` — edl.json (id SHORT-03_HANDLE_ANYWAY_V4), audio_plan.json, **vo.mp3 = voice-01, 23.38s**, vo_text.txt, bed.wav, clips/s1a_action.mp4 + s1b_freeze.mp4 + s2_approach.mp4 + s3_handle.mp4 + s4_inside.mp4, gfx_spec.json, gfx/ (sare PNG elements).

**Timeline**: s1a 0-7.3 (raw 19.5-26.8, punch 1.5x + parallax) / s1b 7.3-9.8 (raw 26.0-27.5 SLOW-MO setpts 1.67 + atempo 0.6, punch 1.65x) / s2 9.8-16.8 (raw 5.5-12.5) / s3 16.8-22.8 (raw 13.3-19.3) / s4 22.8-25.6 (raw 27.3-30.1) / CTA 25.6-27.4.

**VO (voice-01, verbatim)**: "Three in the morning. Watch this. He doesn't break the window. He opens the door. Then he pauses. Right at the camera. He has done this before. No food inside. Doesn't matter. Bears learn what cars mean. And they never forget. One day, he'll open the wrong door." (humanize 100/100)

**Captions (8)**: "3 AM. NOBODY AWAKE."(0.3) / "WATCH THE HANDLES."(3.1) / "THE PAUSE."(7.5) / "A HABIT, NOT AN ACCIDENT."(11.4) / "THE CAR WAS EMPTY."(13.6) / "NOT HUNGER. A HABIT."(16.2) / "THE ULTIMATE PRICE."(20.2) / "HE'LL KEEP COMING BACK."(23.2). End card: **"SUBSCRIBE - MONARCH CAM"** (1.8s).

**Audio recipe** (`audio_plan.json`): chords Am/F/Am+9; tick @ caption onsets (0.3/3.1/7.5/11.4/13.6/16.2/20.2/23.2, gain 0.26-0.30, pan ±0.25-0.3), impact@0.1, riser@5.9→whoosh@7.25, **subdrop@7.3** (dur 1.2, gain 0.55), heartbeats@7.9/8.9/9.7, riser@19.4→warning impact@22.75, CTA impact@25.55 freq44; duck {0.66, 0.12, 0.5}, peak 0.62, **drive 1.3**. Music = user-approved.

**GFX element map (v8, output-frame coordinates)**:
- 0.3s: timestamp badge TL, REC TR, viewfinder corners, progress line + beat-ticks (8) bottom
- 3.15→3.5s: **ring arcs draw-on** around subject (center ~(425,835), r~185) + glow bloom 3.58 + beat-pulse 4.15
- 7.25→9.2s: **spotlight isolation** + **4 lock-on brackets** (staged) + **"0.5x SLOW" badge** (right margin)
- 10.3s: CPW credit strip fly-in (bottom)
- 13.7s: margin callout arrow (left, tip stops 20px before subject)
- 20.25s: warning triangle (left margin) + **draw-on red underline** under "THE ULTIMATE PRICE."
- 23.28s: draw-on red underline under "HE'LL KEEP COMING BACK."
- 25.75s: **CTA light sweep** over end card
- Micro flashes @ 0.10/7.32/25.52 (alpha 38/30/36, 0.12s) + micro shakes amp 3.5-4px @ 0.12/7.35/25.55

**Subject zone (OUTPUT coords)**: bear x 345-465, y 770-865; safe bbox (255,665)-(565,975). Elements sirf iske GIRD/margins pe.

---

# PART E — QUALITY RECIPES (REUSABLE)

### 1. Video quality chain (1440p master)
`raw → hqdn3d=3:2:4:4, scale=2560:1440:flags=lanczos, unsharp=5:5:0.55:5:5:0.0, eq=contrast=1.08:saturation=1.18:gamma=1.02, cas=0.45` (crf15) → segments as crisp downscales (crf16).

### 2. Vertical frame: blur-pad + parallax drift
bg: `boxblur=24:6, brightness=-0.06` scale 1080x1920; fg: scale height 1920, **animated crop x** (`'30*t/7.3'` style expressions) — zoompan MAT use karo (unreliable resets).

### 3. Slow-mo freeze ("THE PAUSE")
`setpts=1.67*PTS` + `atempo=0.6` + punch 1.65x.

### 4. Audio (sound_design.py)
VO duck, soft ticks at caption onsets, subdrop into freezes, heartbeats during tension, riser→impact at warnings, tanh drive 1.3 glue. **Non-harsh verify**: spectral centroid ≈ 2.1 kHz, <7% energy >8 kHz, peak 0.55-0.62.

### 5. Motion graphics (keyframe_elements.py)
- Rule 1: **subject/frame kabhi cover nahi** — elements encircle/point/frame karein.
- Rule 2: zero cheap stickers — sab keyframed (fades, smoothstep slides, staged timings, draw-ons, growth chunks, pulses).
- Rule 3: positions = inverse transform `overlay = (output + (24,42)) / 1.0443` (scale+crop effect).
- Rule 4: growth bars = chunked enable overlays (crop:eval available nahi hai).
- Rule 5: parallel edit_file SAME FILE pe kabhi nahi — sequential!

### 6. Verification protocol (MANDATORY)
1. Frames extract @ key beats (tools/extract_frames.py).
2. Audio: peak + spectral centroid + >8kHz energy fraction (numpy FFT).
3. Bear visible in all checked frames (red/bright region stats).
4. Caption bands bright, CTA card clean.
5. GFX: **zoom-matched base diff** (`scale=1128:2005,crop=1080:1920:24:42`) — bear-zone diff < 2 = subject untouched; element zones diff > 0 = present.
6. ALL PASS hone pe hi deliver.

---

# PART F — EXTERNAL SOURCES & PROVENANCE

- **APPROVED CLIP**: `https://x.com/CPW_SE/status/1665762810909847552` (CPW SE Region, 2023-06-05) — video id `1665761033024331776`, 1280×720 `https://video.twimg.com/ext_tw_video/1665761033024331776/pu/vid/1280x720/dQJoscHhWqxV17dU.mp4?tag=12`. Thread 2/2 `1665762814890479617` = photo + CPW "ultimate price" warning. kktv.com/2023/06/05/watch-bear-opens-vehicle-door-woodland-park/ — "Video courtesy of Colorado Parks and Wildlife".
- **api.fxtwitter.com/status/<id>** = fetch_page se WORKS (video URL extractor). x.com direct fetch = text only.
- **Verified raw backup pool**: youtube `Utv6DH7xKfs` (CBS Sacramento 2019 Tahoe, 22s, 1080p; station bug check karna); CPW May 12 2023 truck break-in (@COParksWildlife). **Disqualified**: `5pgIB7gOBcw` Inside Edition (package).
- **Unverified pool**: `DH25y9bH52M` ViralHog Tahoe; `eWg_aFbInSs` Gatlinburg 2026; newsflare.com/video/141625; ksl.com/article/51493495; UPI 2861662668685 Allenspark CO; TMZ Whitefish MT (watermark, likely disqualified); `s7iViTDLTJc` ViralHog Gatlinburg 2022; KTLA La Crescenta Pop-Tarts bear; `TdBMVFRKOfA` CPW trapped-bear (different).
- **AI-fake warnings (provenance mandatory)**: people.com/11829794 (grandma-bear 44M = AI); VEO dog+bear; bunny trampoline "Ring" 203M = AI.

---

# PART G — IDs REGISTRY

### Git chain (all on arena/4cb3e8a5-world-channel)
`2405695` (base) → `51d3e66` → `04b3ee0` (clip) → `307f9a6` (v1) → `e64f9e2` (v2) → `09865dd` (v3) → `3975498` (v4) → `2bfaccb` (v5) → `3ca6ebd` (v6) → `4b74957` (v7) → `6309665` (v8) → [THIS ARCHIVE].

### Google Drive
- Folders: 01-Clips-Inbox `1thEsqpCHe-sy0AEj5X5CylEfQ5kkKukb` · 02-Finished `1mbbV6HlWAobAckccBPymhJWL-EbygIJF` · 03-Thumbnails `1N0q7g4I456JHEmXgqxaoUyuWzXOkyBGn` · 04-Package-Notes `1qJPzwDj2S17dCrbhxlRqGq-ezJub1oCe` · Production `1a2C3rWC1rwiz_2TNFAmpEndc3xKkETyF`
- SHORT-01: `1cdxBk2awp6SNtLIfCGTolD7YciI1iNqK` / pkg `1ffzZuxuvLxzKzCl2h-af5KRtTdsm9PhW`
- SHORT-02: (rejected, GIF era)
- SHORT-03 v1: `1cdxBk2awp6SNtLIfCGTolD7YciI1iNqK`-era (see git+Drive 02-Finished) — v2: `1P-2xjt4Q3mO-cT1vDS_wa6cdJ5pz21f4` / `1KyfJ-lnKW5kCj5Ohab0JoxassQH93Bkc` — v3: `1MRqK40aL1XEecGpMptXRF_mQZ9awrvpA` / `16Z7dEP7icIzz0p4GrpdGdRuywnp_w8KW` — v4: `1wJT4PpKaZUADtbkIF6je290G9RxE4tIX` / `1EZIq0bGDKcwYZ6unM-I3N2frQ5qJFxj4` — v5: `1MsouyUvQxCbfMMofHt9Gzrq3Qe0NVdCE` / `1j5wIsgtN5KNk_xuJ9gSIRxLMF7lCL78a` — v6: `1VRmG_9Y4kUR7xTmkprHFio1b1DiyfFJC` / `18dzcM50EOOo-evQ2OW2-PnD249Vg2zzZ` — v7: `1W-BZHqnjCubY_lAnXsYH7bZh6Y3s7Rh2` / `1l-GI2kNUOeuK0doIrDXSD-ioPhJqNwGJ` — **v8 FINAL: `1RotQI4n8UK4H8r2uDpvTSoaha1TeDW6R` / `1vcHVpbfYiav-gwhxFqSvq8V_Jd3V6liD`**
- Google Drive connector: `list_connector_tools` USI reply me call karo jisme `upload_file` karna hai (warna "Something went wrong").

### Voices
- **voice-01** = WINNER (add_voice battle "01", user vote) — default narrator.
- voice-00 = purana default.

### Clips
- CLIP-2026-006 = Woodland Park CPW (approved, in production). Rights: **PENDING**.

---

# PART H — ERRORS & DEAD ENDS (DO NOT REPEAT)

1. **GIF/Tenor-Giphy/low-res image route** = BANNED forever (SHORT-02 "bekar").
2. **Drive clips se video banana** = BANNED (user: "clip dhundke lao").
3. **News packages** (narration/branding/captions burned) = NOT raw → disqualified.
4. **VO duration ≠ timeline** → VO cut off. Hamesha `ffmpeg -i vo.mp3` duration vs EDL total check karo; word-proportion se re-time.
5. **zoompan** video push-ins ke liye unreliable (per-input-frame resets) → animated crop expressions use karo.
6. **ffmpeg "Error binding filtergraph"** = dangling unmapped label → 0:a directly map karo.
7. **PIL rectangle x1<x0 crash** (negative direction) → sorted() coords. polygon `width=` risky → line+width se outline.
8. **Parallel edit_file on SAME FILE = race, edits lost** → SEQUENTIAL edits.
9. **Shake string-concat bug**: pad_x + "0+if..." = "240" → crop clamped, shake lost. shake strings EMPTY init se start karo.
10. **`crop:eval` is static ffmpeg build me nahi** → animated widths = chunked enable overlays.
11. **GFX transform**: output = overlay×1.0443−(24,42). Element positions inverse se calibrate karo. **Subject-safety check = zoom-matched base diff** (seedha base se diff galat result deta hai).
12. **grad_energy sharpness metric** misleading across resolutions → final output frames + audio spectral stats pe verify karo.
13. **bash curl x.com/video.twimg.com BLOCKED** → GitHub Actions downloader ONLY. reddit.com fetch_page = 403.
14. **tools/_vendor + output/ + forensics/frames/ turn boundaries pe wipe** → har turn `pip install --target tools/_vendor imageio-ffmpeg pillow numpy`.
15. **bash brace `{$FF:+ok}`** = bad substitution. **/tmp NOT persistent**.
16. **render_shorts**: raw 16:9 directly mat feed (center-crop ho jayega); video-only clips pe anullsrc mux; .mp3 = libmp3lame; PIL cards fps=30,format=yuv420p; music looped+static → dynamics sound_design me bake karo.
17. **Snapshot restores git refs rewind karti hain** → `git fetch origin && git reset --mixed origin/arena/4cb3e8a5-world-channel` → recommit → push. Remote = truth.
18. **GFX output pe dobara GFX mat lagao** — input = BASE render.

---

# PART I — RIGHTS STATUS

- CLIP-2026-006 (CPW Woodland Park): **PENDING** — credit "Colorado Parks and Wildlife (CPW SE Region)" video description me hai. **Monetized publish se pehle ideally CPW ko contact karke confirm karo** (render log `--skip-rights-check`, package me disclosure).
- Rule: generic disclaimer ≠ rights clearance. Har clip ka ledger entry mandatory.

---

# PART J — PENDING & NEXT STEPS

1. **User verdict on v8** (current deliverable) — upload ke liye ready.
2. **LONG VIDEO** ("Caught on Camera — Explained") — Pick #1 ka linked long version: `tools/render_long.py` + `make_animation.py` se banana hai (CPW food-conditioning quotes = base). **Jab tak banti nahi, kisi short me long-video CTA/link NAHI** (user order).
3. **Next clips** — approval gate process: dhoondo → LINK share → "haan" → build. Backup pool Part F me.
4. **4 adjacent videos** banane se pehle channel reset judge mat karo (blueprint).
5. Rights: CLIP-2026-006 clear karo publish se pehle.

---

# PART K — PROMPT VOCABULARY (user ke exact phrases ka matlab)

- "next level lejake / enhance improve karo" = har round me visibly better banao, same quality bar.
- "hooked engaging" = retention editing (proof-first 3s, punch-ins, beats, captions).
- "irritating na ho / kanon ko chubne wale nahi" = soft premium SFX, no harsh highs.
- "raw real viral koi watermark text na ho" = clean original footage only.
- "copy paste Wala kaam nhi Karna" = stickers utha ke chipkana nahi — custom keyframed creative work.
- "bagair kisi kami ke galati ke flaws ke bagair kuch chore miss kiye" = zero-defect delivery + verification.
- "haan kahunga" = approval gate — WAIT for it.

---
*Archive generated 2026-10-24. Yeh document har major change ke baad UPDATE karo.*
