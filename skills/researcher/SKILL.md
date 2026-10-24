---
name: researcher
description: |
  Find trending caught-on-camera wildlife moments, source clips, and fact-check every claim
  for Monarch Cam videos. Use when starting a brief (clip requests), verifying footage
  provenance, researching behaviour/science claims, or checking what's resonating in the niche.
---

# Researcher — clip discovery + claim verification

Two jobs: (1) find the moments worth making videos about, (2) prove every sentence the
narrator will say. Both feed the rights ledger and the forensic report.

## 1. Trend & moment discovery

Search where real audiences vote with attention — not where editors publish.

| Source | What it gives | How |
|---|---|---|
| Reddit (r/bears, r/wildlife, r/HumansAreMetal, r/NatureIsFuckingLit, local city subs) | Raw moments + "is this real?" debates | `agent-reach reddit search "<species> <moment>"` or web search `site:reddit.com` |
| X/Twitter | Breaking wildlife moments, news-station clips | `agent-reach twitter search ...` |
| YouTube | What already gets views in the niche (titles, thumbnails, transcripts) | `agent-reach youtube search/transcript ...` or channel pages |
| Local/news stations | Rights-clearable ring-cam & interview footage | web search `<city> bear ring camera news` |
| Google News / aggregators | The week's wildlife story cycle | web search, last-30-days window |
| Polymarket/HN (via last30days pattern) | Attention scoring across platforms | cross-check which angle people argue about |

**Scoring a candidate moment** (all must be yes before it enters a brief):
1. Is there a clear, readable CONCEPT in one sentence? (engine: proximity or hidden-tricks)
2. Is there a strong still frame that tells the story? (thumbnail proof)
3. Can it be framed accurately without "attack" overclaiming?
4. Is there an EXPLAINER angle — a "why" we can source? (behaviour, conditioning, physics)
5. Rights path available? (permission / licensed / PD / submission)

## 2. Heavy scraping — when to reach for real tools

For one-off research our web search + page fetch is enough. For a **recurring crawler**
(news stations, category pages), the tool landscape:

- **Agent-Reach** (MIT) — `pip install agent-reach`; one CLI for Reddit/X/YouTube
  transcripts/Bilibili. Best default for social/video sources.
- **Scrapling** (BSD) / **Scrapy** (BSD) — Python crawling frameworks; Scrapling handles
  anti-bot pages better, Scrapy is the stable classic.
- **Crawlee** (Apache) — Node/Python, good for browser + queue crawling at scale.
- **Firecrawl** (AGPL) / **Browser Use** (MIT) — agent-grade web access; Browser Use when
  the page needs real interaction (login walls, infinite scroll). Firecrawl is AGPL — use as
  a service, do not vendor code into this repo.

Rule: prefer official APIs/RSS first, polite scraping second, never re-host stolen uploads.

## 3. Claim verification (feeds forensics §4 + script sources)

Pattern adapted from **gpt-researcher** (Apache): decompose → parallel searches →
cross-source agreement → cite → mark conflicts.

For every behavioural claim ("bears return for food conditioning", "they smell 18 miles"):
1. Find a primary or institutional source (state/provincial wildlife agency, university,
   peer-reviewed summary, park service). YouTube description = never a source.
2. Log: claim, source URL, verdict (supported / weak / unverifiable).
3. **Unverifiable claims are cut from the script** — never softened and kept.

## 4. Output artefacts

- `pipeline/finding/CLIP_REQUESTS.md` — updated per brief (what to download, from where).
- `pipeline/forensics/CLIP-*.md` — provenance + claims check filled in.
- `pipeline/scripts/*` — every `[[n]]` source marker resolves to a real URL.

## Watch-outs

- Viral re-uploads are almost never the rights holder — trace to the origin poster.
- "Same animal came back" needs evidence (same property/date window, markings, uploader
  statement), else phrase honestly.
- Animal-harm/disaster content: flag in forensics, don't build the brief around it.
