# Tooling Review — Repo Landscape Verdicts

> Reviewed 2026-10-23. Every repo checked live (metadata, license, activity, README).
> Verdicts: **ADOPT** (integrated now) · **ADOPT-OPTIONAL** (wired in, ready when needed) ·
> **REFERENCE** (concepts only — license or scope) · **SKIP** (wrong fit for this channel).

## Legend of what got integrated

| Integrated into | From |
|---|---|
| `skills/researcher/` | last30days-skill, Agent-Reach, gpt-researcher, scraping landscape |
| `skills/script-humanizer/` + `tools/humanize_check.py` | blader/humanizer |
| `skills/editor/` | claude-code-video-toolkit, video-shotcraft, video-talkcraft*, director |
| `skills/motion-graphics/` + `tools/make_animation.py` | manim, hyperframes, LeetCodeAnimation, shotcraft |
| `skills/youtube-ops/` | MoneyPrinterTurbo, youtube-automation-agent |
| `tools/stock_broll.py` | MoneyPrinterTurbo (stock-fetch stage) |

\* video-talkcraft is PolyForm **Noncommercial** — for a monetised channel only its *ideas*
are usable (anti-PPT layers, word-level VO sync), never its code/assets.

---

## Video production

| Repo | Stars | License | Verdict | Notes |
|---|---:|---|---|---|
| [calesthio/OpenMontage](https://github.com/calesthio/OpenMontage) | 71K | **AGPL-3.0** | REFERENCE | 700+ agent skills, 12 pipelines — the largest skill zoo. AGPL: use as installed tool/inspiration only, never copy into this repo. |
| [Vincentwei1021/video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft) | 13K | Apache-2.0 | ADOPT-OPTIONAL | 152 shot recipe cards + motion vocab (Remotion). Concepts distilled into `skills/editor`; full install when we do Remotion motion segments. |
| [Vincentwei1021/video-talkcraft](https://github.com/Vincentwei1021/video-talkcraft) | 1.7K | **PolyForm NC** | REFERENCE | Voiceover-driven explainer system: word-level VO sync, anti-PPT shot layers, recipe-card taxonomy. Ideas adopted; code NOT usable commercially. |
| [digitalsamba/claude-code-video-toolkit](https://github.com/digitalsamba/claude-code-video-toolkit) | 2.3K | MIT | **ADOPT** | Skills/commands structure (ffmpeg, moviepy, voiceover, thumbnail, publish) — mirrored in `skills/editor` + `skills/youtube-ops`. |
| [s1dashu/director](https://github.com/s1dashu/director) | 820 | MIT | **ADOPT** | Mode-based directing (Animated Explainer / Storytime / Cinematic) — brief structure adopted. |
| [3b1b/manim](https://github.com/3b1b/manim) | 95K | MIT | ADOPT-OPTIONAL | T2 motion tier in `skills/motion-graphics`. Needs pango/LaTeX for full power. |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | 70K | Apache-2.0 | ADOPT-OPTIONAL | "Write HTML. Render video. Built for agents." — T3 tier when we want design-system graphics. |
| [harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | 134K | MIT | **ADOPT (concepts)** | Stock-fetch stage → `tools/stock_broll.py`; assembly loop studied. Faceless-slideshow output refused (reused-content risk). |
| [darkzOGx/youtube-automation-agent](https://github.com/darkzOGx/youtube-automation-agent) | 4.5K | MIT | REFERENCE | End-to-end agent skeleton (research→script→render→upload) matches our pipeline stages. |
| [storytold/filmcraft](https://github.com/storytold/filmcraft) | 16K | Apache-2.0 | SKIP | Full Rust NLE (desktop app). Our FFmpeg EDL pipeline already covers assembly. |
| [OpenShot/openshot-qt](https://github.com/OpenShot/openshot-qt) | 6.7K | GPL | SKIP | GUI editor for humans; agent pipeline doesn't need it. |
| [renezander030/capcut-cli](https://github.com/renezander030/capcut-cli) | 942 | MIT | SKIP | Edits CapCut/JianYing project files; we don't use CapCut. |
| [leancoderkavy/premiere-pro-mcp](https://github.com/leancoderkavy/premiere-pro-mcp) | 428 | MIT | SKIP | Requires Adobe Premiere. |
| [hypit-ai/hypit](https://github.com/hypit-ai/hypit) | 25K | — | **REFUSE** | Viral cloning incl. face swap — misleading synthetic realism; against our brand + monetisation safety. |
| [KlingAIResearch/LivePortrait](https://github.com/KlingAIResearch/LivePortrait) | 19K | — | SKIP | Portrait reenactment; wrong niche (we work real wildlife footage). |
| [krillinai/OpenCreator](https://github.com/krillinai/OpenCreator) | 14K | Apache-2.0 | SKIP (revisit) | Video translation/dubbing — revisit only if we launch non-English channels. |
| [Anil-matcha/Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) | 31K | MIT | SKIP | Gen-video studio directory. Our product is REAL footage + commentary. |
| [MisterBooo/LeetCodeAnimation](https://github.com/MisterBooo/LeetCodeAnimation) | 76K | none | REFERENCE | Step-reveal pacing study only. |
| [juliangarnier/anime](https://github.com/juliangarnier/anime) | 74K | MIT | SKIP | Web/JS animation engine — not a video renderer. |
| [motiondivision/motion](https://github.com/motiondivision/motion) | 34K | MIT | SKIP | React/web motion — channel-site work only. |
| [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos) | 9.7K | MIT | REFERENCE | Prompt/storytelling gallery — mine for narrative structures. |

## Scraping / discovery

| Repo | Stars | License | Verdict | Notes |
|---|---:|---|---|---|
| [Panniantong/Agent-Reach](https://github.com/Panniantong/agent-reach) | 101K | MIT | **ADOPT** | One CLI for Reddit/X/YouTube transcripts — core of `skills/researcher`. |
| [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | 195K | **AGPL-3.0** | ADOPT-OPTIONAL | Agent-grade web data; run as a service (AGPL — no vendoring). |
| [browser-use/browser-use](https://github.com/browser-use/browser-use) | 119K | MIT | ADOPT-OPTIONAL | Real-browser agent for login-walled/interactive sources. |
| [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | 89K | BSD-3 | ADOPT-OPTIONAL | Anti-bot-friendly Python scraping — pick over Scrapy for hard pages. |
| [scrapy/scrapy](https://github.com/scrapy/scrapy) | 65K | BSD-3 | ADOPT-OPTIONAL | Classic crawler for recurring source monitoring (news stations). |
| [apify/crawlee](https://github.com/apify/crawlee) | 26K | Apache-2.0 | SKIP (default) | Great Node crawler; only if we build a hosted pipeline. |

## Research / writing

| Repo | Stars | License | Verdict | Notes |
|---|---:|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer) | 60K | MIT | **ADOPT** | 26-pattern system → `skills/script-humanizer` + `tools/humanize_check.py`. |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 65K | MIT | **ADOPT** | Cross-platform attention search (Reddit/X/YT/HN) → trend discovery in `skills/researcher`. |
| [assafelovic/gpt-researcher](https://github.com/assafelovic/gpt-researcher) | 30K | Apache-2.0 | **ADOPT (pattern)** | Decompose→parallel-search→cross-check→cite = our claims-check loop. |
| [khoj-ai/khoj](https://github.com/khoj-ai/khoj) | 38K | AGPL | SKIP | Self-hosted second brain; heavier than our needs. |
| [microsoft/qlib](https://github.com/microsoft/qlib) | 49K | MIT | SKIP | Quant finance — unrelated. |
| [google-research/google-research](https://github.com/google-research/google-research) | 39K | Apache | SKIP | Research monorepo, not a tool. |

---

## Decision summary

**Integrated now (8):** humanizer, last30days-skill, Agent-Reach, claude-code-video-toolkit,
director, MoneyPrinterTurbo (stock stage), gpt-researcher (pattern), video-shotcraft (concepts).

**Ready on demand (6):** manim, hyperframes, Scrapling, Scrapy, Firecrawl, Browser Use.

**Refused on principle (1):** hypit-style face-swap/viral cloning — our channel sells trust.

**Everything else:** wrong medium, wrong license, or redundant with the pipeline already built.
