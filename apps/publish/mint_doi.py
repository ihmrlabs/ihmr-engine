#!/usr/bin/env python3
"""
Reserve and publish a Zenodo DOI for a research version.

    # Step one: reserve, before the PDF exists
    python3 mint_doi.py reserve --work <path> --version 1

    # Step two, after building the PDF with the DOI in it
    python3 mint_doi.py publish --work <path> --version 1

Set ZENODO_API_TOKEN. Set ZENODO_SANDBOX=1 until you are certain:
a published DOI cannot be deleted.
"""
import argparse
import json
import os
import pathlib
import sys
import urllib.request

SANDBOX = os.environ.get("ZENODO_SANDBOX") == "1"
BASE = "https://sandbox.zenodo.org/api" if SANDBOX else "https://zenodo.org/api"


def api(method: str, path: str, body=None, token=None):
    url = f"{BASE}{path}"
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read() or b"{}")


def upload(bucket_url: str, path: pathlib.Path, token: str):
    with path.open("rb") as f:
        req = urllib.request.Request(
            f"{bucket_url}/{path.name}", data=f.read(), method="PUT",
        )
        req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read())


def load(work: pathlib.Path, version: int):
    manifest = json.loads((work / "manifest.json").read_text())
    entry = next(v for v in manifest["versions"] if v["version"] == version)
    return manifest, entry


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("action", choices=["reserve", "publish"])
    p.add_argument("--work", required=True)
    p.add_argument("--version", type=int, required=True)
    args = p.parse_args()

    token = os.environ.get("ZENODO_API_TOKEN")
    if not token:
        print("ZENODO_API_TOKEN is not set", file=sys.stderr)
        return 1
    if not SANDBOX:
        print("Running against LIVE Zenodo. A published DOI cannot be deleted.", file=sys.stderr)

    work = pathlib.Path(args.work)
    manifest, entry = load(work, args.version)
    vdir = work / f"v{args.version}"
    state_file = vdir / ".zenodo.json"

    if args.action == "reserve":
        dep = api("POST", "/deposit/depositions", {
            "metadata": {
                "upload_type": "publication",
                "publication_type": "report",
                "title": f"{manifest['title']} (version {args.version})",
                "description": manifest.get("summary", ""),
                # Contributors are people. Never an AI tool.
                "creators": [{"name": "Sudarshan, Tejas Parthasarathi"}],
                "access_right": "open",
                "license": "cc-by-4.0",
                "keywords": ["India", "public health", "health policy", "population health"],
                "prereserve_doi": True,
            },
        }, token)
        doi = dep["metadata"]["prereserve_doi"]["doi"]
        state_file.write_text(json.dumps({"id": dep["id"], "bucket": dep["links"]["bucket"], "doi": doi}, indent=2))
        print(f"Reserved {doi}")
        print("Now write it into the Markdown front matter, then build the PDF, then publish.")
        return 0

    if not state_file.exists():
        print("No reservation found. Run `reserve` first.", file=sys.stderr)
        return 1
    state = json.loads(state_file.read_text())

    md = vdir / entry["document"]
    pdf = vdir / entry["pdf"] if entry.get("pdf") else None
    if not pdf or not pdf.exists():
        print("The PDF does not exist. Build it before publishing: it is the deposited artefact.", file=sys.stderr)
        return 1
    if state["doi"] not in md.read_text():
        print("The DOI is not in the Markdown front matter, so the PDF cannot be carrying it.", file=sys.stderr)
        print("Write it in, rebuild the PDF, then publish.", file=sys.stderr)
        return 1

    upload(state["bucket"], pdf, token)
    upload(state["bucket"], md, token)
    api("POST", f"/deposit/depositions/{state['id']}/actions/publish", None, token)
    print(f"Published {state['doi']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
