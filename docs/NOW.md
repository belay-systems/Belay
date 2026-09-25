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

Written 2026-09-25, for `main` as it stands once #14, #24, #31 and #32 have
merged, in that order. #32 is the last of them.

- **Suite:** 704 passed, 1 skipped, 5 xfailed (`python -m pytest -q`). That was
  the result of the merge rehearsal on a scratch copy of `main`.
- **`python scripts/status.py`:** exits 0, 40 open findings. F-019 closed with
  #24.
- **ADRs on `main`:** 14 (`grep -c "^## ADR-" docs/DECISIONS.md`).
  ADR-015 (#7) and ADR-016 (#20) are drafts on branches, neither ratified.
- **Owner rulings on `main`:** Parts 1-19, 21 and 23-31. Part 20 (#22) is not
  adopted (Part 30), and #22 is closed. Part 22 is on #20.
- **Review gate:** `python scripts/review_due.py` gives the next finding
  number. The highest number in use anywhere is F-030.
- **Contributors help and never gate** (Part 30). Work lands on the owner's
  word, through the Owner bypass.

Re-derive with: `git fetch origin`, `git log --oneline -10 origin/main`, the
open pull requests and Issues on GitHub, `python -m pytest -q`,
`python scripts/status.py`, `python scripts/review_due.py`.

## In flight

| PR | What | State |
|---|---|---|
| #7 | ADR-015: a strategy's stage is carried, not asserted (F-007, F-014) | The final text round: item 1 below |
| #20 | ADR-016 draft, Part 22, the ADR-012 amendment draft (`docs/proposals/ADR-016-evidence-bar-DRAFT.md`) | Moves with ADR-015 |
| #33 | Parts 32-34 and the final-text-round session close | Open |
| #36 | F-032 to F-036 fixes, Parts 35-36, ADR-017's draft (grade from provenance) | **The fourth pass broke attempt three** (four blocking). Not to be ratified; attempt four is owed |
| #37 | Parts 37-39 (ADR-017 promises option A; price fingerprint; results name their record), the fourth pass's session record | Merge after #36 |

Both merge cleanly onto this `main` and pass (704), except that each one
appends to the end of `docs/OwnerDecisions.md` or `docs/OperatorChecklist.md`.
There, keep `main`'s text first and add the branch's text after it.

## Highest Priority Next Task

1. **ADR-017 (#36): put the two follow-ups, then build attempt four.**
   - The fourth independent pass broke attempt three three ways, all posted on #36:
     the repository and store it trusts are folders the caller picks, record paths
     escape them with `..`, and prices are not bound to the record.
   - The owner chose option A (Part 37): guard against honest
     mistakes and make faking visible in review; not "impossible".
   - The owner then ruled both follow-ups: Level C needs the series to match a
     fingerprint of the prices the fetch received (Part 38), and every Level C
     metric artifact names the fetch record behind its grade (Part 39).
   - **Next:** attempt four on #36, built to Parts 37-39 and to the fourth pass's
     findings; then its own independent pass; then ratification. Not before.
2. **Finish the evidence bar the way Part 28e rules.**
   - **Step 1, the final text round on #7 and #20, with no redesign:**
     - fix the fourth pass's two blocking findings (F4-3 and F4-1, Issue #21,
       2026-09-25 01:28 UTC);
     - apply 28a-28d, which Part 31 confirms as recorded;
     - settle the three open readings in the notes after Part 28: 25g against
       26e and 27f, 25h and 26b against 18e, and 28e against 18g. Put each to
       the owner as one question with a recommendation.
   - **Step 2, build the current-stage read as code.** Every attack from the
     passes on Issue #21 becomes a test that passes only when the attack is
     refused. The plan is **waiting on the owner's "go"**:
     - the tests are written by a separate model from the review findings,
       not from the code;
     - a fresh review then attacks the code;
     - the ADR text is updated to match what the code does;
     - it goes on its own branch, for example `claude/stage-read`, as a draft
       pull request, and is not merged until the owner ratifies the ADRs;
     - not in this first slice: the save-side checks, and ADR-016's evidence
       checks (report binding, the trial cap).
   - **The independent pass** on each step is a fresh session told to
     falsify (Part 30). A different AI is welcome, never waited on.
3. **Small, when convenient:**
   - the gate items #29 left: `fullmatch` on report names, surviving an
     invalid date, and ASCII digits in `REPORT` (`scripts/review_due.py`);
   - a sentence in the review skill (owner-only) saying to write every finding
     number in full ASCII (`F-NNN`), because the gate cannot read other shapes;
   - phase 2 of the file split, for `docs/DECISIONS.md`,
     `docs/OwnerDecisions.md`, `docs/OperatorChecklist.md` and `CHANGELOG.md`,
     once #7 and #20 have landed (`docs/proposals/growing-files.md`).

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
