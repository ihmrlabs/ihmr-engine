# ingest

Converts source material into clean Markdown, with its provenance kept intact.

Everything in the research repository is Markdown, but sources arrive as government PDFs,
survey reports, and journal articles. This is the bridge, and it is genuinely useful whether or
not the rest of IHMR ever exists.

## What it does

```text
a PDF, HTML page, or document
        ↓
extract text, preserving structure where the source has any
        ↓
write Markdown with front matter recording:
  where it came from, when we fetched it, who published it,
  what period it covers, its licence, and a checksum
        ↓
ihmr/sources/<publisher>/<document>.md
```

## Why the checksum matters

Government publications get silently replaced at the same URL more often than you would expect.
A checksum recorded at retrieval means we can tell whether the thing we cited is still the thing
that is there.

If it has changed, that is a finding worth writing up, not a problem to paper over.

## What it will not do

**It will not decide whether a source is any good.** Extraction is mechanical; judgement is not.
Every converted source still needs a person to read it before anything is cited from it.

**It will not redistribute what we are not allowed to redistribute.** Where a licence forbids
it, the tool writes the front matter and a retrieval script, and leaves the body empty with a
note saying why.
