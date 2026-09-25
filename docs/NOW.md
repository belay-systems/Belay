# Belay Now

**Start here.** This file is what is true now: where things stand, the one
current next-task list, and how to work with the owner. It is **rewritten** at
every session close, so it stays short enough to read in one pass. What it
said before lives in `docs/sessions/` and in git history
(`docs/OwnerDecisions.md` Part 29).

- **History** is in `docs/sessions/`, one file per session, and in
  `docs/HANDOFF.md`, the archive, which is frozen as of 2026-09-25.
- **Open findings** are in `docs/FINDINGS.md`.
- **Trust commands over prose**, including this file. Re-derive the state
  below before acting on it.

## Where things stand

Written 2026-09-25 against `origin/main` at `1c8eb1c`.

- **Suite:** 685 passed, 1 skipped, 5 xfailed (`python -m pytest -q`).
- **`python scripts/status.py`:** exits 0, 41 open findings.
- **ADRs on `main`:** 14 (`grep -c "^## ADR-" docs/DECISIONS.md`).
  ADR-015 (#7) and ADR-016 (#20) are drafts on branches, neither ratified.
- **Owner rulings on `main`:** Parts 1-15, 18, 19 and 23. Parts 16-17, 20-22 and
  24-28 are on open pull requests' branches. Part 29 is on this change's branch.
- **Review gate:** `python scripts/review_due.py` gives the next finding
  number. On this commit, and on every branch, the highest number in use is
  F-030.

Re-derive with: `git fetch origin`, `git log --oneline -10 origin/main`, the
open pull requests and Issues on GitHub, `python -m pytest -q`,
`python scripts/status.py`, `python scripts/review_due.py`.

## In flight

As listed on GitHub at 2026-09-25. Each pull request's own description is the
record of what it needs.

| PR | What | Waiting on |
|---|---|---|
| #7 | ADR-015: a strategy's stage is carried, not asserted (F-007, F-014) | Blocking findings F4-1 and F4-3 from the fourth pass on Issue #21, then the owner's questions |
| #20 | ADR-016 draft (the evidence bar), Part 22, the ADR-012 amendment draft | ADR-015 first; the different-AI pass on Issue #21 |
| #31 | Parts 24-28: `markdown-it-py`, and the evidence-bar principles | Second contributor's review |
| #22 | Part 20: no one merges alone; removes the Owner bypass | Second contributor's review, then the owner's apply steps in `docs/OperatorChecklist.md` |
| #24 | F-019: seven regression tests for guards on the capital path | Second contributor's review |
| #14 | Records the second contributor's access (Parts 16-17) | Second contributor's review |
| this one | Splits the handoff: this file, `docs/FINDINGS.md`, `docs/sessions/` (Part 29) | Owner review |

**Merge conflicts to expect.** Every open branch that adds a Part appends to the
end of `docs/OwnerDecisions.md`, so each one conflicts with the others there.
Resolve by keeping both blocks, in Part order. #20 and #22 append to
`docs/HANDOFF.md`, which is now frozen. After this change is on `main`, their
appended text moves to a `docs/sessions/` record, and anything still current
moves into this file. The freeze test says so when it fails.

## Highest Priority Next Task

1. **Owner, quick decisions.** Review this change, because it alters how every
   session starts. Then #31, #14 and #22, which wait on the second
   contributor's review.
2. **Finish the evidence bar the way Part 28e rules** (on #31's branch):
   first, one final text round on #7 and #20. It fixes the fourth pass's two
   blocking findings (F4-3 and F4-1, Issue #21, 2026-09-25 01:28 UTC) and
   applies 28a-28d, with no redesign. Then build the current-stage read as
   code, with every attack from the passes on Issue #21 written as a test that
   must fail. The plan for the code step, from the session "Belay threads
   status", is **waiting on the owner's "go"** (not yet given):
   - build the code and tests, with the tests written by a separate model from
     the review findings, not from the code, so the author doesn't grade itself;
   - a fresh review then attacks the code;
   - the ADR text is updated to match what the code does;
   - it opens as a draft pull request for the second contributor, on its own
     branch (for example `claude/stage-read`), not on #31. It is not merged
     until the owner ratifies the ADRs;
   - not in this first slice: the save-side checks, and ADR-016's evidence
     checks (report binding, the trial cap). Those follow once it is solid.
3. **Issue #21: the different-AI pass is still owed** by the second
   contributor, and runs in parallel (28e). Four same-provider passes do not
   replace it. Its scope covers ADR-015, ADR-016 and the ADR-012 amendment
   draft on #20.
4. **#24 (F-019)**, once reviewed.
5. **Small, when convenient:**
   - the gate items #29 left: `fullmatch` on report names, surviving an
     invalid date, and ASCII digits in `REPORT` (`scripts/review_due.py`);
   - a sentence in the review skill (owner-only) saying to write every finding
     number in full ASCII (`F-NNN`), because the gate cannot read other shapes;
   - phase 2 of the file split, for `docs/DECISIONS.md`,
     `docs/OwnerDecisions.md`, `docs/OperatorChecklist.md` and `CHANGELOG.md`.
     It waits until #7, #20 and #31 have landed (`docs/proposals/growing-files.md`).

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
