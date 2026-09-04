# datasets

Inputs, with provenance recorded: where each came from, when we retrieved it, who published it,
what period it covers, and under what licence.

## Layout

```text
datasets/
└── <dataset-id>/
    ├── SOURCE.md      provenance, licence, retrieval date, and any caveats
    ├── data.csv       the data, tidy and unmodified except where SOURCE.md says otherwise
    └── notes.md       optional: how we cleaned it, and what we chose not to fix
```

## Rules

**Never store real personal health data.** Synthetic populations are generated; where we
validate them, it is against published aggregates, never individual records.

**Where a dataset cannot be redistributed**, keep `SOURCE.md` and a retrieval script rather than
the data itself. Third-party licences are respected and recorded.

**Record the period the data covers, separately from when it was published.** These get confused
constantly, and the confusion is material: NFHS-5 was published in 2021 but its fieldwork ran
2019-21. A figure presented as current when it describes 2019 is misleading even if every digit
is correct.

**Record what you cleaned.** If a row was dropped, a name normalised, or a unit converted, say
so in `notes.md`. Someone should be able to get back to the original.

## What a SOURCE.md contains

```markdown
# <Dataset title>

Publisher:
Source document:
URL:
Retrieved:
Period covered:
Licence:
Redistributable: yes / no
Verified by:

## Caveats
```

`Verified by` names a person. Automated retrieval is fine; unverified publication is not.
