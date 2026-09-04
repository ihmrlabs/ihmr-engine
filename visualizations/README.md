# visualizations

Chart and map definitions, generated from data in [`datasets/`](../datasets/) and never drawn by
hand.

That is an architectural rule, not an aesthetic preference. A chart built from a committed
dataset carries provenance exactly as a sentence does: a reader who doubts a figure can go and
check it, and correcting the data corrects the chart. A chart drawn by hand is an assertion
wearing a picture.

## How this connects to the research

Each visualisation is built here, then copied into the version folder of the research it belongs
to, so that a published version carries its own figures and stays reproducible even if the
dataset later changes:

```text
ihmr-engine/visualizations/<viz-id>/          built here
ihmr/research/<work>/vN/visualisations/       copied there on publication
```

A published version is never edited, so its charts are frozen with it. A later version rebuilds
from the newer data and says what changed.

## Definition format

Each visualisation is a JSON file the site renders as server-side SVG. No charting library runs
in the browser.

```json
{
  "title": "Adults with hypertension: aware, treated, controlled",
  "unit": "million people",
  "categories": ["Have it", "Know it", "Treated", "Controlled"],
  "series": [{ "label": "Adults 18 and over", "values": [0, 0, 0, 0] }],
  "source": "",
  "sourceUrl": "",
  "dataPeriod": "",
  "note": ""
}
```

`source` and `dataPeriod` are required. A chart without them does not get published, because a
figure with no provenance is not evidence.

## Maps

See [`../datasets/india-boundaries/`](../datasets/india-boundaries/) before building any map of
India. **This matters more than it will seem.**
