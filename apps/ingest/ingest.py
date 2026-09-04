#!/usr/bin/env python3
"""
Convert a source document into Markdown with provenance.

    python3 ingest.py --url https://example.gov.in/report.pdf \
        --publisher "Ministry of Health and Family Welfare" \
        --title "National Health Profile 2025" \
        --period "2024" \
        --licence "Government Open Data Licence India" \
        --out ../../../ihmr/sources/mohfw/national-health-profile-2025.md

Extraction is mechanical. Judgement is not: every converted source still needs a
person to read it before anything is cited from it, and the front matter says so
until someone fills in `verified_by`.
"""
import argparse
import hashlib
import datetime
import pathlib
import sys
import urllib.request


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "IHMR ingest (projectihmr.org)"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def extract(raw: bytes, url: str) -> str:
    """Best effort. Falls back to saying it could not, rather than inventing text."""
    if url.lower().endswith(".pdf"):
        try:
            import pdfplumber  # type: ignore
            import io
            out = []
            with pdfplumber.open(io.BytesIO(raw)) as pdf:
                for i, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ""
                    if text.strip():
                        out.append(f"## Page {i}\n\n{text.strip()}")
            return "\n\n".join(out)
        except ImportError:
            return ("> Extraction skipped: pdfplumber is not installed.\n>\n"
                    "> Install it and re-run, or paste the relevant text manually. "
                    "Do not summarise from memory.")
    try:
        html = raw.decode("utf-8", errors="replace")
        try:
            import html2text  # type: ignore
            h = html2text.HTML2Text()
            h.ignore_images = True
            h.body_width = 0
            return h.handle(html)
        except ImportError:
            return "> Extraction skipped: html2text is not installed."
    except Exception as e:  # noqa: BLE001
        return f"> Extraction failed: {e}"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--url", required=True)
    p.add_argument("--publisher", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--period", required=True, help="The period the data covers, not the publication year")
    p.add_argument("--published", default="", help="Publication year")
    p.add_argument("--licence", required=True)
    p.add_argument("--redistributable", default="unknown", choices=["yes", "no", "unknown"])
    p.add_argument("--out", required=True)
    args = p.parse_args()

    raw = fetch(args.url)
    checksum = hashlib.sha256(raw).hexdigest()
    today = datetime.date.today().isoformat()

    body = (
        extract(raw, args.url)
        if args.redistributable == "yes"
        else ("> This source is not redistributable under its licence, so only its provenance is "
              "recorded here. Retrieve it from the URL above to read it.")
    )

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f"""---
id: IHMR-SRC-000
type: source
title: {args.title}
status: evidence
created: {today}
updated: {today}
publisher: {args.publisher}
source_url: {args.url}
retrieved: {today}
data_period: "{args.period}"
published_year: "{args.published}"
licence: {args.licence}
redistributable: {args.redistributable}
checksum_sha256: {checksum}
verified_by:
ai_disclosure: none
license: CC-BY-4.0
lang: en
---

# {args.title}

> **Not yet verified.** Extraction is mechanical. Someone needs to read this against the
> original before anything is cited from it, and put their name in `verified_by`.

**Publisher:** {args.publisher}
**Source:** <{args.url}>
**Retrieved:** {today}
**Data covers:** {args.period}
**Licence:** {args.licence}

---

{body}
""")
    print(f"Wrote {out}")
    print(f"Checksum {checksum}")
    print("Assign a real IHMR-SRC id and fill in verified_by before citing anything from this.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
