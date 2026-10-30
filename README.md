# Florida: law history in git

The statute law of Florida as a git repository: one file per section, committed with the official publisher named as author. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law).

**What is in it now (a first build, not complete)**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | Constitution of the State of Florida (214 sections) | 1 | One version: the text as the Florida Legislature publishes it in the 2026 Florida Statutes, retrieved 30 October 2026 |
| `title-36-business-organizations/` | Florida Statutes, Title XXXVI: Business Organizations (970 sections) | 1 | One version: the text as the Florida Legislature publishes it in the 2026 Florida Statutes, retrieved 30 October 2026 |
| `title-40-real-and-personal-property/` | Florida Statutes, Title XL: Real and Personal Property (798 sections) | 1 | One version: the text as the Florida Legislature publishes it in the 2026 Florida Statutes, retrieved 30 October 2026 |
| `title-46-crimes/` | Florida Statutes, Title XLVI: Crimes (985 sections) | 1 | One version: the text as the Florida Legislature publishes it in the 2026 Florida Statutes, retrieved 30 October 2026 |

Nothing else of Florida's law is in it yet.

## Where the text comes from

The text is read from **Online Sunshine**, <https://www.leg.state.fl.us/statutes/>, where the **Florida Legislature** publishes the Constitution and the 2026 Florida Statutes. Each chapter was fetched once through the site's "View Entire Chapter" link and the Constitution as one page, 94 requests in all, about 1.5 seconds apart. Each section keeps its catchline, its text with subsection, paragraph and subparagraph designators, its History line (the session laws behind it) and any Note the Legislature prints inside the section. Footnote markers are dropped.

## Dates

- Each act has **one version**, dated 29 October 2026, the last full day before the pages were retrieved on 30 October 2026 (the site prints no edition date, and no commit is dated ahead of the build). It is the oldest version available in this build: earlier years' statutes exist online (1997 onward) but are not in it.
- The first commit of each act is credited to the Florida Legislature as "oldest version available".
- The session laws in each History line are part of the text, not the commit dates.

## What it does not show

- Any amendment history: the Statutes before the 2026 edition.
- The other 44 titles of the Florida Statutes, the Laws of Florida and regulations.
- Nothing here is an official publication.

## How it is checked

- Every unit is read back from git on its day and compared with the corpus (`tools/check_repo.py`; results in `REPRODUCE.md`).
- Each source file is identified by its sha256, in `data/versions.json`.

## What "author" means

Each commit is authored by the publisher (the Florida Legislature (Online Sunshine)) because this first build holds one version of each act, the oldest version available. The committer is always Lexifina.
