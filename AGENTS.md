# AGENTS.md

Instructions for AI agents working in the `ihmr-engine` repository.

`CLAUDE.md` carries the same content. If you are a person, `README.md` and `.github/CONTRIBUTING.md`
are friendlier places to start.

## What this repository is

The working half of [IHMR](https://github.com/ihmrlabs/ihmr), the India Health Maintenance
Rail. Simulations, models, clinical rules and tooling.

It exists to **test** the project's claims rather than assert them. Research and arguments live
in the `ihmr` repository; this one holds the code that tries to break them.

## Tone - this matters

**The writing here is warm and inviting.** This is a deliberate choice, not an accident of
style. The project depends on domain experts - clinicians, civil servants, community health
workers - choosing to engage, and most of them are not going to push through a document that
reads like a compliance manual.

Write as a knowledgeable person genuinely glad the reader turned up:

- Address the reader directly. Prefer "we" and "you" over the passive voice.
- Explain *why* a rule exists rather than just stating it.
- Make invitations feel like invitations.
- Acknowledge the reader's scepticism generously; it is well earned.

Warm is **not** the same as promotional. No hype, no inflated claims, no manufactured
certainty, no marketing register. The tone to aim for is closer to a good research
publication than to either a standards document or a landing page.

British spelling: *organised, fulfilment, programme, prioritise, behaviour, artefact.*

## Hard rules

- **Reproducibility is not optional.** Every simulation records inputs, rule set, random seed,
  outputs, and the commit it ran at. A result nobody can reproduce is not a result.
- **If a number is published anywhere, it must be traceable to a run here.** This is the rule
  the repository exists to enforce.
- **Never commit real personal health data.** Synthetic populations only, validated against
  published aggregates rather than individual records.
- **Rules are data, not code.** Clinical thresholds, intervals and eligibility criteria live in
  `rules/` as readable files so a clinician can review them without reading code. Never bury a
  clinical decision inside program logic.
- **State what a model does not capture.** Every model is wrong about something; the useful
  question is what.
- **Never imply IHMR is a Government of India programme**, or that any institution has endorsed,
  funded, or partnered with it. This applies to drafts as much as to published text.
- **Never write clinical guidance.** Clinical claims need named clinical review; flag and stop.
- **Never include personal health information**, or identify anyone who has not consented.
- **Never silently rewrite a published claim.** Mark it `superseded`, keep the original, record
  what replaced it and why, and add an entry to `updates/`.
- **AI output is never evidence.** It helps locate sources; it never replaces reading them.
  This applies to your own output.

## AI disclosure

Set `ai_disclosure` on anything you draft or substantially edit, and **leave `signed_off_by`
blank** - only a named human can sign off. If you are between two tiers, declare the higher
one. Never list an AI as an author. Never write that AI verified anything.

See `about/how-we-use-ai.md`.

## Where things go

| Content | Folder |
|---|---|
| Something that runs | `apps/` |
| Shared pieces | `packages/` |
| Clinical and eligibility rules, as data | `rules/` |
| A named, reproducible run | `simulations/` |
| Inputs, with provenance | `datasets/` |
| A rough one-off investigation | `experiments/` |
| How to run things | `docs/` |
| Environment and deployment | `infra/` |

Read the folder's `README.md` before adding to it.

## Results feed the research repository

A simulation that produces a figure used in published research creates an obligation: if the
result changes, the document citing it must be updated or an issue opened against `ihmr`.

Simulations are cited by ID the way papers are cited. That only works if the IDs are stable and
the runs stay reproducible.

## Negative results are results

A run that failed to show what we hoped gets written up exactly like one that succeeded. Often
it is more useful. Do not quietly drop an inconvenient result.

## When you are unsure

Say so, and leave the uncertainty visible in the document rather than resolving it quietly.
Recording an open question is a contribution. Guessing and presenting it as settled is exactly
the failure this project is built to avoid.
