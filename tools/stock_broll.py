#!/usr/bin/env python3
"""Rights-clean stock b-roll finder (Pexels + Pixabay) with automatic credits record.

Concept adapted from harry0703/MoneyPrinterTurbo (MIT) stock-fetch stage, wired into the
Monarch Cam rights ledger workflow. Stock licences allow commercial use — this is the
fastest RIGHTS-CLEAN way to fill context/b-roll gaps while waiting for user clips.

Setup (free keys):
    export PEXELS_API_KEY=...      # https://www.pexels.com/api/
    export PIXABAY_API_KEY=...     # https://pixabay.com/api/docs/

Usage:
    python3 tools/stock_broll.py search "black bear forest" --out media/broll
    python3 tools/stock_broll.py search "campsite night camera" --provider pexels --limit 3

Downloads go to media/broll/<query-slug>/ and every download appends a row to
media/broll/credits.csv so required attribution stays recorded. Register downloaded clips
with tools/intake_register.py --rights licensed-stock before use in an EDL.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import urllib.parse
import urllib.request
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vidlib import REPO  # noqa: E402

UA = {"User-Agent": "MonarchCam-Broll/1.0"}


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40]


def http_json(url: str, key: str | None = None) -> dict:
    headers = dict(UA)
    if key:
        headers["Authorization"] = key  # Pexels style
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def search_pexels(query: str, limit: int, key: str) -> list[dict]:
    data = http_json(f"https://api.pexels.com/videos/search?query={urllib.parse.quote(query)}"
                     f"&per_page={limit}", key=key)
    out = []
    for v in data.get("videos", [])[:limit]:
        files = sorted(v.get("video_files", []), key=lambda f: f.get("height") or 0, reverse=True)
        best = next((f for f in files if (f.get("height") or 0) >= 720), files[0] if files else None)
        if best:
            out.append({"provider": "pexels", "id": v["id"], "url": v.get("url", ""),
                        "download": best.get("link"), "credit": v.get("user", {}).get("name", ""),
                        "license": "Pexels License (commercial OK, no attribution required)"
                       })
    return out


def search_pixabay(query: str, limit: int, key: str) -> list[dict]:
    data = http_json(f"https://pixabay.com/api/videos/?key={key}&q="
                     f"{urllib.parse.quote(query)}&per_page={limit}")
    out = []
    for v in data.get("hits", [])[:limit]:
        best = (v.get("videos", {}).get("large") or v.get("videos", {}).get("medium") or {})
        if best.get("url"):
            out.append({"provider": "pixabay", "id": v["id"], "url": v.get("pageURL", ""),
                        "download": best["url"], "credit": v.get("user", ""),
                        "license": "Pixabay Content License (commercial OK)"})
    return out


def main() -> None:
    import urllib.parse  # noqa: F401  (used in f-strings above via module attr)
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("command", choices=["search", "setup"])
    ap.add_argument("query", nargs="?", default="")
    ap.add_argument("--provider", choices=["pexels", "pixabay", "both"], default="both")
    ap.add_argument("--limit", type=int, default=4)
    ap.add_argument("--out", default="media/broll")
    args = ap.parse_args()

    if args.command == "setup" or not os.environ.get("PEXELS_API_KEY"):
        print("Stock b-roll setup:")
        print("  export PEXELS_API_KEY=...   <- free at https://www.pexels.com/api/")
        print("  export PIXABAY_API_KEY=...  <- free at https://pixabay.com/api/docs/")
        if args.command == "setup":
            return
        if not os.environ.get("PEXELS_API_KEY") and not os.environ.get("PIXABAY_API_KEY"):
            raise SystemExit("No API keys in environment — set at least one (see above).")

    if not args.query:
        raise SystemExit("Give a search query, e.g.: stock_broll.py search \"black bear forest\"")

    results: list[dict] = []
    pk, xk = os.environ.get("PEXELS_API_KEY"), os.environ.get("PIXABAY_API_KEY")
    if args.provider in ("pexels", "both") and pk:
        try:
            results += search_pexels(args.query, args.limit, pk)
        except Exception as e:
            print(f"pexels error: {e}", file=sys.stderr)
    if args.provider in ("pixabay", "both") and xk:
        try:
            results += search_pixabay(args.query, args.limit, xk)
        except Exception as e:
            print(f"pixabay error: {e}", file=sys.stderr)
    if not results:
        raise SystemExit("No results (check keys/network/provider).")

    outdir = REPO / args.out / slugify(args.query)
    outdir.mkdir(parents=True, exist_ok=True)
    credits = REPO / args.out / "credits.csv"
    new = not credits.exists()
    with credits.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["file", "provider", "asset_id", "source_page", "credit", "license",
                        "downloaded_for"])
        for i, r in enumerate(results):
            fname = f"{r['provider']}_{r['id']}_{i:02d}.mp4"
            dest = outdir / fname
            print(f"↓ {r['provider']}/{r['id']}  {r['download'][:70]}...")
            try:
                req = urllib.request.Request(r["download"], headers=UA)
                with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as o:
                    o.write(resp.read())
                w.writerow([str(dest.relative_to(REPO)), r["provider"], r["id"], r["url"],
                            r["credit"], r["license"], args.query])
                print(f"  saved {dest.relative_to(REPO)}  ({r['license'][:30]}...)")
            except Exception as e:
                print(f"  download failed: {e}", file=sys.stderr)
    print(f"\nCredits recorded in {credits.relative_to(REPO)}")
    print("Next: python3 tools/intake_register.py --file <clip> --rights licensed-stock ...")


if __name__ == "__main__":
    main()
