# How this repository was made (Florida)

This file is written by the build on 2026-11-13, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Online Sunshine: The Florida Constitution and the 2026 Florida Statutes (The Florida Legislature) | <https://www.leg.state.fl.us/statutes/> | 2026-10-30 | Statute text is not copyrightable (Georgia v. Public.Resource.Org, 2020). The Legislature publishes the Florida Statutes and the Constitution for free public use; its footer reads "Copyright 1995-2026 The Florida Legislature" and no annotations are taken. |
| Online Sunshine: every title of the 2026 Florida Statutes (The Florida Legislature) | <https://www.leg.state.fl.us/statutes/index.cfm?Mode=View%20Statutes&Submenu=1&Tab=statutes> | 2026-11-03 | Statute text is not copyrightable (Georgia v. Public.Resource.Org, 2020). The Legislature publishes the Florida Statutes and the Constitution for free public use; its footer reads "Copyright 1995-2026 The Florida Legislature" and no annotations are taken. |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of the State of Florida | 1 | 2026-10-29 to 2026-10-29 |

The build made 1 commits:

| Commits | Kind |
| ---: | --- |
| 1 | baseline texts where the record starts |
| 0 | named laws, court decisions and treaties |
| 0 | changes no amendment note explains, credited to the publisher |
| 0 | corrections to the existing record |
| 0 | printing or layout changes |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-11-13.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 0 laws in the record.
- 1 tags.

## Dates

Each commit is dated at noon (America/New_York) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Fla. Stat. 11.2421: the Florida Statutes are adopted annually; a session law takes effect on the date it states, otherwise on the 60th day after the legislature adjourns (Fla. Const. art. III, s. 9); this first build holds only the 2026 Florida Statutes as published, dated by the day before retrieval https://www.leg.state.fl.us/statutes/

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `4a3013dd0a92a01071955ac9b173fe218755f27e92e2f45e24142473e5b755af` (433057 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `63170edd89e92292ac248dae17d79e486e4e9f19`, `check.py` `e340718c28cd5b0edbe37bdeab1aac31427ada66`, `on.py` `4a8aa1c9a5e6bd8cc831b90a6e68c5a6f448a13c`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- First build: only the Constitution and Titles XXXVI (business organizations), XL (real and personal property) and XLVI (crimes) of the 2026 Florida Statutes, as retrieved on 2026-10-30. Each act has one version, credited to the publisher as the oldest version available.
- The version is dated 2026-10-29, the last full day before retrieval, so that no commit is dated ahead of the build; the site prints no edition date.
- Each section keeps its History line (the session laws behind it) and any editors' Note the Legislature prints inside the section; no annotations are taken.
- Wave 3 (2026-11-03): every other title of the 2026 Florida Statutes is added, one act per title, parsed as in the first build.
- Each new title is dated by the retrieval day (2026-11-03) and credited to the publisher as the oldest version available: the History lines give session-law numbers, not in-force days, so the latest amendment's in-force day is not given by the source.

## What AI did and did not do

The source readers and builders were developed under Lexifina's direction with coding assistants, including Claude Code and Codex.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- none
