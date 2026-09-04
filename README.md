# IHMR Engine

**Where we test whether our ideas actually hold up.**

This is the working half of [IHMR](https://github.com/ihmrlabs/ihmr), the India Health
Maintenance Rail. The other repository holds our research and arguments. This one holds the
code that tries to break them.

It exists for one reason: to stop the project becoming a very well written essay.

---

## The rule this repository enforces

> **If a number appears anywhere in our published work and cannot be traced to a run you could
> reproduce, it should not be there.**

Every figure we publish should be reproducible from something here. Please hold us to that. If
you find a claim we cannot back with a run, that is a bug and we would like to know.

## What is here

| Folder | What is inside |
|:--|:--|
| [`apps/`](apps/) | Things that run: the ingest tool, simulators, models |
| [`packages/`](packages/) | Shared pieces those apps are built from |
| [`rules/`](rules/) | Clinical and eligibility rules, written as data you can read |
| [`simulations/`](simulations/) | Named, versioned runs and their results |
| [`datasets/`](datasets/) | Inputs, with provenance and licences recorded |
| [`experiments/`](experiments/) | One-off investigations |
| [`docs/`](docs/) | How to run things, and how they work |
| [`infra/`](infra/) | Deployment and environment |

## Two things worth knowing before you look around

### Rules are data, not code

Screening intervals, risk thresholds and eligibility criteria live in [`rules/`](rules/) as
files you can read, not as logic buried inside a program.

This matters more than it might sound. **A clinician should be able to read a rule, disagree
with it, and propose a change without reading a line of code.** That is where clinical review
actually attaches to this system, rather than being a formality after the fact.

Every rule records where it came from, which guideline it follows, its version, and whether it
has been reviewed.

### Simulations are reproducible or they do not count

Each run in [`simulations/`](simulations/) records its inputs, rule set, random seed, outputs,
and the exact commit it ran at. Our research cites simulation IDs the way it cites papers.

## Where we are starting

Early, and honestly so. The first job is not a prototype of the rail. It is to **put numbers on
the problem**: how much of India's disease burden is undetected, how many outstanding needs a
maintenance layer would surface, and what capacity it would take to resolve them.

That work supports our first piece of research, and it is a better first use of this repository
than a toy version of a system we have not finished designing.

### `apps/ingest`

Converts source material into clean Markdown with its provenance kept intact: where it came
from, when we fetched it, who published it, and under what licence.

Everything in the research repository is Markdown, but source material arrives as government
PDFs, survey reports and papers. This tool is the bridge, and it is genuinely useful whether or
not the rest of IHMR ever exists.

## Contributing

We would love the help, particularly from anyone who wants to prove us wrong with data.

- **Break our models.** Find the assumption that does not survive contact with reality.
- **Challenge a rule.** If a clinical rule in [`rules/`](rules/) is wrong or outdated, please
  say so. You do not need to write any code to do this.
- **Improve a simulation.** Better methods, better validation, better honesty about uncertainty.
- **Tell us a number looks wrong.** Even just a hunch is useful. We would rather check and find
  it was fine.

See [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## How we use AI

We use AI throughout this project, including in writing this code. Every published artefact
says how, and a named person signs off on it. See
[how we use AI](https://github.com/ihmrlabs/ihmr/blob/main/about/how-we-use-ai.md).

## Licence

**Apache 2.0**, see [LICENSE](LICENSE). We chose it partly for the explicit patent grant, which
matters for something meant to become shared infrastructure.

Datasets keep their own licences, recorded per file.

## Related work

| Repository | What it is for |
|:--|:--|
| [`ihmr`](https://github.com/ihmrlabs/ihmr) | Our research, proposals, questions and decisions |
| **`ihmr-engine`** | This one. Simulations, models, rules and tooling |

---

[projectihmr.org](https://projectihmr.org) · hello@projectihmr.org

Maintained by [Tejas Parthasarathi Sudarshan](https://tejassuds.com)
