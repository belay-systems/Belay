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

Written 2026-09-25, for `main` as it stands once #33 has merged. #33 carries
this file, Parts 32-34, and the session record
`docs/sessions/2026-09-25-final-text-round.md`.

- **Suite:** 704 passed, 1 skipped, 5 xfailed (`python -m pytest -q`), on
  `main`, on #7 and on #20.
- **`python scripts/status.py`:** exits 0, 40 open findings.
- **ADRs on `main`:** 14 (`grep -c "^## ADR-" docs/DECISIONS.md`).
  ADR-015 (#7) and ADR-016 (#20) are drafts on branches, neither ratified.
- **Owner rulings on `main`:** Parts 1-19, 21 and 23-31. Parts 32-34 are
  on #33. Part 22 is on #20. Part 20 is not adopted (Part 30).
- **Review gate:** `python scripts/review_due.py` says a review is **due**
  (the last one is `2026-09-11-review.md`) and gives F-031 as the next finding
  number. Nothing above F-030 is in use.
- **Contributors help and never gate** (Part 30). Work lands on the owner's
  word, through the Owner bypass.

Re-derive with: `git fetch origin`, `git log --oneline -10 origin/main`, the
open pull requests and Issues on GitHub, `python -m pytest -q`,
`python scripts/status.py`, `python scripts/review_due.py`.

## In flight

| PR | What | State |
|---|---|---|
| #33 | Parts 32-34, this file, the session record | Ready to merge once green: owner rulings and docs only |
| #7 | ADR-015: a strategy's stage is carried, not asserted (F-007, F-014) | Step 1 of 28e is done (see below); up to date with `main` |
| #20 | ADR-016 draft, Part 22, the ADR-012 amendment draft | Same as #7; moves with it |

#7 and #20 are drafts and stay unmerged until the owner ratifies both ADRs.
Each still appends to the end of `docs/OwnerDecisions.md` or
`docs/OperatorChecklist.md`; when `main` moves, keep `main`'s text first and add
the branch's text after it.

## Highest Priority Next Task

1. **Step 2 of Part 28e: build the current-stage read as code.** It is
   **waiting on the owner's "go"** (33a).
   - **Step 1 is finished, and the text rounds are over** (Parts 33a and 34).
     The text is ADR-015 at `c11bf59` (#7) and ADR-016 at `6388254` (#20).
     - The fifth pass found two blocking holes (F5-2, F5-5), answered by
       Part 33.
     - A sixth pass, on this session's own edits, found five more, several of
       them the author's errors. The owner ruled Part 34: fix those errors,
       then stop.
     - The last fixes have had no pass; they say so.
   - **Put five owner questions first**, one at a time, before any code.
     They are in ADR-016's Required Follow-Up, item 19. The first asks
     whether 33c's "file" covers a stored `Demote` or `Retire` review.
   - **The tests:** every attack from the Issue #21 passes, F5-1 to F5-12 and
     the open F6 findings included, becomes a test that passes only when the attack
     is refused. They are written by a separate model from the findings, not
     from the code.
   - **Settle in code, then write into the ADR:** how rule 8's backtest report
     is bound beside the seven records (33b), and rule 10 judging every read by
     today's bar (32a).
   - **Then:** a fresh review attacks the code, the ADRs are conformed to what
     the code does, and a fresh pass attacks the exact text to be ratified,
     right before the owner ratifies (32c). A different AI is welcome, never
     waited for (30b).
   - It goes on its own branch, for example `claude/stage-read`, as a draft
     pull request, and is not merged until the owner ratifies the ADRs.
   - **Not in this first slice:** the save-side checks, and ADR-016's evidence
     checks (report binding, the trial cap).
2. **The scheduled adversarial review is due.** Run it by
   `.claude/skills/belay-review/SKILL.md`, starting at F-031.
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
