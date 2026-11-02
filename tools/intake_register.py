#!/usr/bin/env python3
"""Register a clip: rights-ledger row + forensic stub + ID assignment.

Usage:
    python3 tools/intake_register.py --file media/inbox/bear_door_ringcam.mp4 \
        --source-url "https://..." \
        --rights written-permission \
        --credit "Creator Name" \
        --series too-close \
        --verified 2026-10-23 \
        --notes "doorbell cam, black bear returns x4" \
        [--cleared]        # only after rights evidence is checked in forensics

Rights types: written-permission | licensed-stock | public-domain | cc0 | cc-by |
              creator-submission | owned-footage | pending
Default rights_status is 'pending'; renders refuse non-cleared clips.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vidlib import LEDGER, REPO  # noqa: E402

RIGHTS_TYPES = [
    "written-permission", "licensed-stock", "public-domain", "cc0", "cc-by",
    "creator-submission", "owned-footage", "pending",
]
SERIES = ["too-close", "hidden-tricks", "shorts", "archive"]


def next_id() -> str:
    year = dt.date.today().year
    n = 0
    if LEDGER.exists():
        with LEDGER.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                m = re.match(rf"CLIP-{year}-(\d+)", row.get("clip_id", ""))
                if m:
                    n = max(n, int(m.group(1)))
    return f"CLIP-{year}-{n + 1:03d}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", required=True, help="clip path relative to repo root")
    ap.add_argument("--source-url", default="", help="origin URL of the clip")
    ap.add_argument("--rights", required=True, choices=RIGHTS_TYPES)
    ap.add_argument("--credit", default="", help="required on-screen/description credit")
    ap.add_argument("--series", default="too-close", choices=SERIES)
    ap.add_argument("--verified", default=dt.date.today().isoformat())
    ap.add_argument("--notes", default="")
    ap.add_argument("--cleared", action="store_true",
                    help="mark rights_status='cleared' (only with real evidence)")
    args = ap.parse_args()

    rel = str(Path(args.file).as_posix())
    fpath = REPO / rel
    if not fpath.exists():
        raise SystemExit(f"File not found: {fpath}  (upload/place the raw clip first)")

    cid = next_id()
    status = "cleared" if args.cleared else "pending"
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    is_new = not LEDGER.exists()
    with LEDGER.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["clip_id", "file", "series", "source_url", "rights_type",
                        "rights_status", "date_verified", "required_credit",
                        "raw_backup", "notes"])
        w.writerow([cid, rel, args.series, args.source_url, args.rights,
                    status, args.verified, args.credit, rel, args.notes])

    stub = REPO / "pipeline" / "forensics" / f"{cid}.md"
    stub.parent.mkdir(parents=True, exist_ok=True)
    if not stub.exists():
        stub.write_text(f"""# {cid} — Forensic Report

| Field | Value |
|---|---|
| File | `{rel}` |
| Series | {args.series} |
| Source URL | {args.source_url} |
| Rights type | {args.rights} |
| Rights status | **{status}** |
| Date verified | {args.verified} |
| Required credit | {args.credit} |
| Notes | {args.notes} |

## 1. Provenance
_(origin, uploader, date, raw-original vs re-upload)_

## 2. Beat map (timestamped)
| t | What is visible | What is claimed |
|---|---|---|

## 3. What is really happening
_(species behaviour, body language, context the frame hides)_

## 4. Claims check
| Planned script claim | Source | Verdict |
|---|---|---|

## 5. Edit window
- Best 3-second proof moment (hook):
- In / out:

## 6. Risk flags
_(distress, harm, minors, privacy, advertiser-unfriendly)_

## 7. Rights evidence
_(permission message, licence ID, PD proof, etc.) — attach before setting status='cleared'_
""", encoding="utf-8")

    print(f"Registered {cid}")
    print(f"  ledger : {LEDGER.relative_to(REPO)}  (status={status})")
    print(f"  report : {stub.relative_to(REPO)}")
    print("Next: complete the forensic report, then set rights_status='cleared' in the ledger.")


if __name__ == "__main__":
    main()
