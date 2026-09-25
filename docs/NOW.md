# Belay Now

**Start here.** This file is what is true now: where things stand, the one
current next-task list, and how to work with the owner. It is **rewritten** at
every session close, so it stays short enough to read in one pass. What it
said before lives in `docs/sessions/` and in git history
(`docs/OwnerDecisions.md` Part 29).

- **History** is in `docs/sessions/`, one file per session, and in
  `docs/HANDOFF.md`, the archive, frozen as of 2026-09-25.
- **Open findings** are in `docs/FINDINGS.md`.
- **Trust commands over prose**, including this file. Re-derive the state below
  before acting on it.

## Where things stand

Written at the close of 2026-09-25. `main` is `95e5a4a`. Everything below is on
**PR #36** (`claude/brave-pascal-e7401x`, Issue #35), which is green and mergeable
and **not merged**.

- **Suite:** 720 passed, 1 skipped, 5 xfailed on #36. `main` is 704.
- **`python scripts/status.py`:** exit 0, 45 open findings.
- **The 2026-09-25 review merged** (#34), raising **F-032 to F-036**. All five were
  independently attacked and all five survived; they are registered in
  `docs/FINDINGS.md` under Open. **None is marked closed** — closure waits on a pass
  and a merge, the precedent `bdeffe8` set for F-019.
- **Owner rulings on `main`:** Parts 1-19, 21, 23-31. **Parts 35 and 36 are on #36**;
  Parts 32-34 are on #33. Part 20 is not adopted.
- **ADRs:** 14 on `main`. ADR-015 (#7), ADR-016 (#20) and **ADR-017 (#36)** are
  drafts, none ratified.
- **Review gate:** `python scripts/review_due.py` gives the next finding number and
  is the only authority on it. `SKIP` until 2026-10-07.
- **Contributors help and never gate** (Part 30).

Re-derive with: `git fetch origin`, `git log --oneline -10 origin/main`, the open
pull requests and Issues, `python -m pytest -q`, `python scripts/status.py`,
`python scripts/review_due.py`.

## What #36 contains, and the one thing to understand about it

Fixes for F-032, F-034 and F-035; the owner's Parts 35 and 36; and ADR-017's draft.
F-033 and F-036 were owner rulings and are implemented. F-036 removed `pandas`,
`jinja2` and `python-dateutil`.

**The part worth reading before touching any of it.** F-033 — "every metric artifact
is graded Level C whatever produced it" — took **three implementations**. The first
two were each broken by an independent pass, and both times the code did not deliver
the ruling while the documents claimed it did:

| attempt | enforced | broken by |
|---|---|---|
| 1 | came through `disclosure_from` | `DailyBarSeries` is caller-buildable — typed bars + a real source gave Level C with that vendor's name |
| 2 | the caller's record validates | `Fetch` is caller-buildable and `ArtifactIntegrity.sign` is **public over an unkeyed hash** — a caller signed its own record and got Level C claiming a licensed vendor and no survivorship bias |
| 3 | the record is **in the repository** | standing, and **unreviewed** |

**The ceiling, which is permanent without keyed signing:** nothing in the code can
prove a record came from `fetch_record` rather than from a caller. The guarantee is
"this record is on disk where it says it is, these are its bytes, this is its series"
— not "it came from the vendor". Written into ADR-017 rather than papered over. Do
not write "signed" as though it meant authenticity; that error ran through two
implementations and four documents here.

## In flight

| PR | What | State |
|---|---|---|
| #36 | This branch: F-032/F-034/F-035 fixed, Parts 35-36, ADR-017 draft | Green, mergeable. **Owner: ratify ADR-017; a fourth pass is owed first** |
| #33 | Parts 32-34 and a session close | Open. **Will go red against #36's finding-number test** — it names the burned F-031 in four places under `docs/`; the fix is to write "the number after F-030", or the bracketed form when quoting |
| #7 | ADR-015: a strategy's stage is carried, not asserted | The final text round |
| #20 | ADR-016 draft, Part 22, the ADR-012 amendment draft | Moves with ADR-015 |

## Highest Priority Next Task

1. **A fourth independent pass on #36, then the owner ratifies or rejects ADR-017.**
   Three passes ran and each broke the implementation it was given; attempt three has
   had none, and its absence is not evidence. Where to aim: find a route to a Level C
   disclosure that does not involve `fetch_and_record` running and its output staying
   intact; mutate all eight guards in `disclosure_from` one at a time (**commit
   first** — a harness here destroyed an uncommitted implementation with
   `git checkout --`); check Part 36 and ADR-017 claim nothing more than the owner
   ruled.
2. **Close F-032 to F-036** once #36 merges — move their rows to Closed with the date
   and the pull request. Not before: the register says closure follows a pass and a
   merge.
3. **Finish the evidence bar the way Part 28e rules** (#7 and #20). Step 1 is the
   final text round; step 2 is the current-stage read as code and is **waiting on the
   owner's "go"**. Whoever picks it up should read **Part 35b** first: every metric
   artifact is Level D until the fetch path is wired, which under ADR-016's draft
   floor would block promotion above `Paper Trading`.
4. **Small, when convenient:**
   - **F-003 is now load-bearing.** Nothing calls `disclosure_from` in production, so
     no Level C artifact can exist at all. It blocks more than it did.
   - A full tautological-test survey: 59 of 146 `pytest.raises` calls carry no
     `match=`. Two of this session's own tests were vacuous and only mutation caught
     them.
   - `scripts/verify_clone.py` has not run for five consecutive reviews for want of
     `dolt`, so the live data path is unverified.
   - The gate items #29 left (`scripts/review_due.py`), and phase 2 of the file split
     once #7 and #20 land.

## Working Agreement

Copied unchanged from `docs/HANDOFF.md`'s "Working Agreement".

The repository owner is not a developer; Belay is their first coding project, and
they are learning alongside the work.

Explain what a component is and why Belay needs it before writing it, in plain
language, without dropping the specifics or the real numbers. Unpack jargon on first
use.

Confirm scope before large reads or long runs. Show the proposed work before doing
it. Stop and report when something fails rather than adjusting it unasked — a test
rewritten to pass is worth less than a failure that gets read.

Do not accept a claim about what a governing document says without opening it. Two
errors this session came from exactly that.

**Independent verification is not optional polish and it does not go last.** Four
sessions running, a fresh-context pass has found defect-grade errors that the
author's own review of the same work found none of — 4, 6, 6, then 19. It is not
a matter of reading more carefully: the defects live in the prose asserting the
code is right, and re-reading re-derives the reasoning that produced them. Budget
for the pass up front, and run it **before** anything irreversible lands — a
signed artifact, a permanent identifier, a committed history.

## Closing a session

`AGENTS.md`, "Files that grow", has the rules and the reasons. In short:

1. Write `docs/sessions/YYYY-MM-DD-short-name.md`: what was asked, what was
   done, what was verified and how, and what is open. Never edit it after it
   merges.
2. **Rewrite** this file. Update "Where things stand" and "In flight", and
   replace the next-task list. Keep one list, under one heading.
3. Update `docs/FINDINGS.md` for any finding opened or closed, and
   `docs/OperatorChecklist.md` for anything only the owner can do.

`tests/test_handoff_files.py` fails the build if this file goes over 200 lines
or 16,000 bytes, or grows a second next-task heading.
