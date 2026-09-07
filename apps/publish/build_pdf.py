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
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from render_charts import render_all  # noqa: E402

CHART_RE = re.compile(r"^\[CHART:\s*([a-z0-9-]+)\s*\|\s*(.+?)\]\s*$", re.M)

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

    # Drop the body's own h1. The metadata block above already sets the title,
    # and leaving both made the document a single section with everything
    # nested inside it.
    body = re.sub(r"^#\s+.*$", "", body, count=1, flags=re.M)

    # The article references its figures rather than containing them, so that a
    # correction to the data corrects the chart. A PDF has to contain them: it
    # travels away from the site, and a copy whose figures are missing is not
    # the same document. Without this the placeholders reached the reader as
    # literal text, which is what they were doing.
    viz = vdir / (entry.get("visualisations") or "visualisations")
    charts = render_all(viz, vdir / "_charts") if viz.is_dir() else {}
    missing = []
    figure_no = [0]

    def figure(m):
        name, caption = m.group(1), m.group(2).strip()
        path = charts.get(name)
        if not path:
            missing.append(name)
            return f"*[Figure not available: {name}]*"
        figure_no[0] += 1
        # No "Figure N." prefix here. Pandoc numbers figures itself, and adding
        # our own produced "Figure 1: Figure 1." on every one of them.
        return f"![{caption}]({path.name}){{width=100%}}\n"

    body = CHART_RE.sub(figure, body)
    if missing:
        print(f"No chart data for: {', '.join(sorted(set(missing)))}", file=sys.stderr)
    print(f"Embedded {figure_no[0]} figures")

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
        "pandoc", tmp.name, "-o", out.name,
        "--resource-path", f".:_charts",
        "--pdf-engine=xelatex", "--toc", "--toc-depth=2",
        "--standalone",
        *TEMPLATE_VARS,
    ]
    try:
        subprocess.run(cmd, check=True, cwd=vdir)
    except FileNotFoundError:
        print("pandoc is not installed. Install pandoc and a LaTeX engine.", file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as e:
        print(f"pandoc failed: {e}", file=sys.stderr)
        return 1
    finally:
        tmp.unlink(missing_ok=True)
        shutil.rmtree(vdir / "_charts", ignore_errors=True)

    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
