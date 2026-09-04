# India boundaries

**Read this before building any map of India.**

## The problem

Most freely available boundary data draws India incorrectly. Natural Earth, the default basemaps
in most mapping libraries, and a great many GeoJSON collections show the de facto line of
control rather than India's claimed boundary, and omit or differently attribute Jammu and
Kashmir, Ladakh, and Aksai Chin.

For this project that is not a cosmetic issue. Publishing such a map would be a legal exposure
under Indian law, and it would discredit the work with precisely the audience it is trying to
reach: a civil servant or a state health official who sees a wrong map stops reading, and they
are right to.

## The rule

**Boundary geometry must come from a Survey of India compliant source**, showing Jammu and
Kashmir and Ladakh as part of India.

If no compliant file is available for something we want to map, we do not publish the map. The
site's map component is built to refuse: it renders an explanation and the underlying table
instead of drawing anything. An absent map is recoverable. A wrong one is not.

## What goes in this folder

| File | What it is |
|:--|:--|
| `boundaries.geojson` | The compliant boundary file |
| `SOURCE.md` | Where it came from, when, under what licence, and who verified it |
| `state-names.json` | Canonical state and union territory names, so data joins cleanly |

`SOURCE.md` must record a named person who checked the boundaries, not just a URL. This is one
of the few places in the project where a human eye is the control.

## State names

Data from different sources spells states differently: Odisha and Orissa, Uttarakhand and
Uttaranchal, Puducherry and Pondicherry, NCT of Delhi and Delhi. `state-names.json` holds the
canonical form and every alias we have encountered, so a join never silently drops a state.

A dropped state in a health map is not a rendering bug. It reads as a claim that we have no data
for those people.
