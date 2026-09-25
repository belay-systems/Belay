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

Written at the close of 2026-09-25, for `main` once #37 has merged. #37 carries
no code: Parts 37-40, this session's record and this file.

- **Suite:** 704 passed, 1 skipped, 5 xfailed on `main` (`python -m pytest -q`).
- **`python scripts/status.py`:** exits 0.
- **ADRs on `main`:** 14 (`grep -c "^## ADR-" docs/DECISIONS.md`). ADR-015 (#7),
  ADR-016 (#20) and ADR-017 (#36) are drafts on branches, none ratified.
- **Owner rulings on `main`:** Parts 1-19, 21, 23-31 and 37-40. Part 20 is not
  adopted (Part 30). Part 22 is on #20, Parts 32-34 on #33, Parts 35-36 on #36;
  each is a proposal until it merges. Parts 37-40 refer to Parts 35-36 and read
  fully once #36 lands.
- **Review gate:** `python scripts/review_due.py` gives the next finding number
  and is the only authority on it. Do not restate its answer here.
- **Contributors help and never gate** (Part 30). Work lands on the owner's
  word, through the Owner bypass.

Re-derive with: `git fetch origin`, `git log --oneline -10 origin/main`, the
open pull requests and Issues on GitHub, `python -m pytest -q`,
`python scripts/status.py`, `python scripts/review_due.py`.

## In flight

| PR | What | State |
|---|---|---|
| #36 | F-032 to F-036 fixes, Parts 35-36, ADR-017's draft (grade from provenance) | **Attempt three was broken by the fourth pass** (four blocking). Not to be merged or ratified as it stands: attempt four goes here (item 1) |
| #33 | Parts 32-34 and the final-text-round session close | Open. Goes red against #36's finding-number test if #36 merges first (#36's `docs/NOW.md` says how to fix it) |
| #7 | ADR-015: a strategy's stage is carried, not asserted (F-007, F-014) | The final text round: item 2 below |
| #20 | ADR-016 draft, Part 22, the ADR-012 amendment draft | Moves with ADR-015 |

**Merging any of these into `main`:** for `docs/OwnerDecisions.md` and
`docs/OperatorChecklist.md`, keep both sides. **Not for `docs/NOW.md`**, which each
rewrites: keeping both sides gives two next-task lists and fails the build. Take
`main`'s `docs/NOW.md` and carry over what is still true.

## Highest Priority Next Task

1. **ADR-017 attempt four, on #36.** Start from
   `docs/proposals/ADR-017-attempt-four-session-brief.md`, which has the phases,
   the tests to write first, and the owner questions to expect.
   - The fourth independent pass on #36 broke attempt three three ways: the
     repository and store it trusts are folders the caller picks, record paths
     escape them with `..`, and prices are not bound to the record.
   - The owner ruled what attempt four must meet: option A, guard against honest
     mistakes and make faking visible in review (Part 37); Level C only on the
     prices the fetch received (Part 38); every metric artifact over a fetch names
     its record (Part 39); attempt four picks how the prices are bound, and its
     independent pass checks the choice (Part 40).
   - **Read Part 40's "What the owner was told that was wrong" before choosing a
     method.** The owner was twice told something wrong while deciding.
   - Then its own independent pass; then the owner ratifies or rejects. Not before.
2. **Finish the evidence bar the way Part 28e rules.**
   - **Step 1, the final text round on #7 and #20, with no redesign:**
     - fix the two blocking findings of Issue #21's fourth pass (F4-3 and
       F4-1, 2026-09-25 01:28 UTC) — not the fourth pass on #36 in item 1;
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
