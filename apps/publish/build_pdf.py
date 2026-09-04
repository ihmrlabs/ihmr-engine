#!/usr/bin/env python3
"""
Build the PDF for a published version.

    python3 build_pdf.py --work ../../../ihmr/research/IHMR-RSCH-001-state-of-indias-healthcare --version 1

Markdown is the source of truth. This is a rendering, never authored by hand,
and never the only copy of anything. If the two ever disagree, the Markdown is
right and this should be rebuilt.

The PDF travels away from the site, so it carries its own citation, provenance,
licence, AI disclosure and DOI.
"""
import argparse
import json
import pathlib
import subprocess
import sys

TEMPLATE_VARS = [
    "--variable", "documentclass=article",
    "--variable", "geometry:margin=1in",
    "--variable", "fontsize=11pt",
    "--variable", "linkcolor=Blue",
    "--variable", "urlcolor=Blue",
    "--variable", "colorlinks=true",
]


def front_matter(md: str) -> dict:
    if not md.startswith("---"):
        return {}
    end = md.index("\n---", 3)
    out = {}
    for line in md[4:end].split("\n"):
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--work", required=True, help="Path to the work folder")
    p.add_argument("--version", type=int, required=True)
    args = p.parse_args()

    work = pathlib.Path(args.work)
    manifest = json.loads((work / "manifest.json").read_text())
    entry = next((v for v in manifest["versions"] if v["version"] == args.version), None)
    if not entry:
        print(f"Version {args.version} is not in the manifest", file=sys.stderr)
        return 1

    vdir = work / f"v{args.version}"
    md_path = vdir / entry["document"]
    md = md_path.read_text()
    fm = front_matter(md)

    if not fm.get("doi"):
        print("This version has no DOI yet.", file=sys.stderr)
        print("Reserve one first: the PDF has to carry its own identifier, because it travels", file=sys.stderr)
        print("away from the site and a copy without a DOI cannot be cited.", file=sys.stderr)
        return 1

    body = md[md.index("\n---", 3) + 4:] if md.startswith("---") else md

    header = f"""---
title: "{manifest['title']}"
subtitle: "Version {args.version}"
author: "{fm.get('authors', 'IHMR Labs')}"
date: "{entry.get('published', '')}"
---

\\begin{{center}}
\\small
IHMR, the India Health Maintenance Rail \\\\
{manifest['id']} · Version {args.version} · DOI: {fm['doi']} \\\\
Status: {entry.get('status', 'evidence')} \\\\
AI disclosure: {fm.get('ai_disclosure', 'unknown')} · Signed off by {fm.get('signed_off_by') or 'not yet signed off'} \\\\
Licensed CC BY 4.0 · projectihmr.org
\\end{{center}}

\\vspace{{1em}}

\\noindent\\rule{{\\textwidth}}{{0.4pt}}

\\small
\\textbf{{IHMR is not a Government of India programme}}, and is not endorsed by, funded by, or
affiliated with any government body or institution. Nothing in this document is clinical
guidance.
\\normalsize

\\noindent\\rule{{\\textwidth}}{{0.4pt}}

\\vspace{{1em}}

"""

    combined = header + body
    tmp = vdir / "_build.md"
    tmp.write_text(combined)

    out = vdir / (entry.get("pdf") or f"{work.name}-v{args.version}.pdf")
    cmd = [
        "pandoc", str(tmp), "-o", str(out),
        "--pdf-engine=xelatex", "--toc", "--toc-depth=2",
        "--number-sections", "--standalone",
        *TEMPLATE_VARS,
    ]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("pandoc is not installed. Install pandoc and a LaTeX engine.", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as e:
        print(f"pandoc failed: {e}", file=sys.stderr)
        return 1
    finally:
        tmp.unlink(missing_ok=True)

    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
