#!/usr/bin/env python3
"""
Draw a work's charts as vector PDFs, for embedding in the printed version.

The site draws these as SVG at request time. A PDF cannot do that: it has to
carry the figures inside it, because it travels away from the site entirely and
a copy whose charts are missing is not the same document.

Vector rather than raster, so a figure stays sharp when someone zooms in on a
value or prints the page - which, for a document whose whole argument is that
the numbers matter, is the difference between evidence and decoration.
"""
import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# The site's palette, which is Okabe-Ito: chosen so the series stay
# distinguishable to a reader with colour vision deficiency.
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7",
           "#E69F00", "#56B4E9", "#8C6D1F", "#3D3D3D"]
INK, MUTED, GRID = "#0F1721", "#55606E", "#DDE3EA"


def fmt(n: float) -> str:
    """Indian units. A reader here thinks in crore and lakh, not millions."""
    a = abs(n)
    if a >= 1e7:
        return f"{n / 1e7:.1f} cr"
    if a >= 1e5:
        return f"{n / 1e5:.1f} L"
    if a >= 1000:
        return f"{n / 1000:.0f}k"
    return f"{n:g}"


def _panels(series):
    """Group series that can honestly share a y-axis.

    Some of these charts carry a population count, a percentage and a median
    age in one file. On a shared linear axis the counts fill the frame and
    everything else is a flat line on zero - which is not a hard-to-read chart,
    it is a chart that hides most of its data.

    Series are grouped by order of magnitude, and a group only splits off when
    it differs by more than about fiftyfold. Anything closer than that reads
    fine together and is better compared side by side.
    """
    scaled = []
    for s in series:
        peak = max((abs(v) for v in s["values"]), default=0) or 1e-9
        scaled.append((peak, s))
    scaled.sort(key=lambda x: -x[0])

    groups, current, ceiling = [], [], None
    for peak, s in scaled:
        if ceiling is None or ceiling / peak <= 50:
            current.append(s)
            ceiling = ceiling or peak
        else:
            groups.append(current)
            current, ceiling = [s], peak
    if current:
        groups.append(current)
    return groups


def draw(data: dict, out: pathlib.Path) -> bool:
    cats = [str(c) for c in data.get("categories", [])]
    series = data.get("series", [])
    if not cats or not series:
        return False

    groups = _panels(series)

    longest = max((len(c) for c in cats), default=0)
    rotate = longest > 8 or len(cats) > 8
    width = min(11.0, max(6.5, len(cats) * 0.62))
    per_panel = 3.4 if len(groups) > 1 else 4.2
    height = per_panel * len(groups) + (min(longest, 34) * 0.055 if rotate else 0)

    fig, axes = plt.subplots(len(groups), 1, figsize=(width, height), dpi=200,
                             sharex=True, squeeze=False)
    axes = [a[0] for a in axes]

    colour = {id(s): PALETTE[i % len(PALETTE)] for i, s in enumerate(series)}
    xs = range(len(cats))

    for ax, group in zip(axes, groups):
        n = len(group)
        span = 0.8
        bar_w = span / n
        for i, s in enumerate(group):
            offset = -span / 2 + bar_w * (i + 0.5)
            ax.bar([x + offset for x in xs], s["values"], width=bar_w * 0.92,
                   label=s.get("label", ""), color=colour[id(s)],
                   edgecolor="none", zorder=3)

        ax.tick_params(axis="y", labelsize=8, colors=MUTED, length=0)
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: fmt(v)))
        ax.grid(axis="y", color=GRID, linewidth=0.7, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.spines["bottom"].set_color(GRID)
        if n > 1 or len(groups) > 1:
            ax.legend(fontsize=7.5, frameon=False, labelcolor=MUTED,
                      ncol=min(n, 3), loc="upper left", bbox_to_anchor=(0, 1.02))

    last = axes[-1]
    last.set_xticks(list(xs))
    last.set_xticklabels([c if len(c) <= 34 else c[:33] + "\u2026" for c in cats],
                         rotation=38 if rotate else 0,
                         ha="right" if rotate else "center", fontsize=8, color=MUTED)
    if data.get("unit") and len(groups) == 1:
        axes[0].set_ylabel(data["unit"], fontsize=8, color=MUTED)

    fig.tight_layout()
    # Format follows the extension, so the same drawing can be checked as a
    # PNG and shipped as vector.
    fig.savefig(out, format=out.suffix.lstrip(".") or "pdf",
                bbox_inches="tight", transparent=True)
    plt.close(fig)
    return True


def render_all(viz_dir: pathlib.Path, out_dir: pathlib.Path) -> dict:
    """Every chart in a version's visualisations folder. Returns name -> path."""
    out_dir.mkdir(parents=True, exist_ok=True)
    built = {}
    for f in sorted(viz_dir.glob("*.json")):
        if f.stem == "dashboard":
            continue
        try:
            data = json.loads(f.read_text())
        except json.JSONDecodeError:
            continue
        target = out_dir / f"{f.stem}.pdf"
        if draw(data, target):
            built[f.stem] = target
    return built
