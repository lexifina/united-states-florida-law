# How this repository was made (Florida)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Online Sunshine: The Florida Constitution and the 2026 Florida Statutes (The Florida Legislature) | <https://www.leg.state.fl.us/statutes/> | 2026-10-30 | Statute text is not copyrightable (Georgia v. Public.Resource.Org, 2020). The Legislature publishes the Florida Statutes and the Constitution for free public use; its footer reads "Copyright 1995-2026 The Florida Legislature" and no annotations are taken. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of the State of Florida | 1 | 2026-10-29 to 2026-10-29 |
| `title-36-business-organizations` | Florida Statutes, Title XXXVI: Business Organizations | 1 | 2026-10-29 to 2026-10-29 |
| `title-40-real-and-personal-property` | Florida Statutes, Title XL: Real and Personal Property | 1 | 2026-10-29 to 2026-10-29 |
| `title-46-crimes` | Florida Statutes, Title XLVI: Crimes | 1 | 2026-10-29 to 2026-10-29 |

The build made 4 commits:

| Commits | Kind |
| ---: | --- |
| 4 | first version of an act |
| 0 | one law on its in-force day |
| 0 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 4 tags.

## Dates

Each commit is dated at noon (America/New_York) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Fla. Stat. 11.2421: the Florida Statutes are adopted annually; a session law takes effect on the date it states, otherwise on the 60th day after the legislature adjourns (Fla. Const. art. III, s. 9); this first build holds only the 2026 Florida Statutes as published, dated by the day before retrieval https://www.leg.state.fl.us/statutes/

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `449147fbaeba9f8650884d910eae745d68c91d901da1fbe7a3866d4fdb2b9b69` (8004896 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- First build: only the Constitution and Titles XXXVI (business organizations), XL (real and personal property) and XLVI (crimes) of the 2026 Florida Statutes, as retrieved on 2026-10-30. Each act has one version, credited to the publisher as the oldest version available.
- The version is dated 2026-10-29, the last full day before retrieval, so that no commit is dated ahead of the build; the site prints no edition date.
- Each section keeps its History line (the session laws behind it) and any editors' Note the Legislature prints inside the section; no annotations are taken.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
