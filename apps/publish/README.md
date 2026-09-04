# publish

Turns a finished research version into a published artefact: a PDF, a DOI, and the R2 objects
that the site and any citation will resolve against.

## The order is not arbitrary

```text
1  version reaches evidence or decision
2  create the Zenodo deposition
3  reserve the DOI                      ← before anything is built
4  write the DOI into the Markdown front matter
5  generate the PDF from that Markdown
6  upload the PDF and the Markdown source
7  publish the deposition
```

**Step 3 has to precede step 5.** The PDF is what Zenodo holds and what someone gets when they
resolve the DOI, and a PDF travels away from the site entirely: emailed, printed, filed, opened
eighteen months later by someone who has never seen projectihmr.org.

So it has to carry its own identifier. If the DOI were issued at publication in the ordinary
way, every downloaded copy would be missing the one thing needed to cite it.

## Use the sandbox first

`sandbox.zenodo.org` until you are certain. **A published DOI cannot be deleted.**

## What the PDF carries

Everything needed to stand alone: the citation block, the AI disclosure, the provenance line,
the licence, the version number, and its own DOI.
