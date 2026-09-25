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

Written 2026-09-25, for `main` at `95e5a4a`, plus this branch
(`claude/brave-pascal-e7401x`, Issue #35) which is not yet merged.

- **Suite:** 709 passed, 1 skipped, 5 xfailed (`python -m pytest -q`) on this
  branch. `main` at `95e5a4a` is 704.
- **`python scripts/status.py`:** exits 0, 45 open findings on this branch.
- **The 2026-09-25 review has merged** (#34) and raised F-032 to F-036. All
  five were independently attacked on this branch and **all five survive**;
  none was overturned. They are now registered in `docs/FINDINGS.md`, and
  **none is marked closed** — closure waits on an independent pass over this
  branch, the precedent `bdeffe8` set for F-019.
- **ADRs on `main`:** 14 (`grep -c "^## ADR-" docs/DECISIONS.md`).
  ADR-015 (#7) and ADR-016 (#20) are drafts on branches, neither ratified.
- **Owner rulings on `main`:** Parts 1-19, 21 and 23-31. Part 20 (#22) is not
  adopted (Part 30), and #22 is closed. Part 22 is on #20.
- **Review gate:** `python scripts/review_due.py` gives the next finding
  number. It is the only authority on that; this file does not restate its
  answer (F-035). It returns `SKIP` until 2026-10-07.
- **Both owner rulings have landed.** "Aligned to recommendations",
  `docs/OwnerDecisions.md` **Part 35**: a computed number is Level C only when its
  series came from a recorded fetch (F-033, drafted as ADR-017, **not ratified**),
  and `pandas`/`jinja2`/`python-dateutil` are removed with `numpy` not declared
  (F-036). Both are implemented on this branch.
- **F-033's suite run is incomplete.** The sandbox blocked `python -m pytest`
  after the test edits, so **CI on #36 is the first full verification** of it.
  F-036 was verified in a fresh virtual environment (709 passing with none of the
  four packages installed). See
  `docs/sessions/2026-09-25-owner-rulings-f033-f036.md`.
- **Contributors help and never gate** (Part 30). Work lands on the owner's
  word, through the Owner bypass.

Re-derive with: `git fetch origin`, `git log --oneline -10 origin/main`, the
open pull requests and Issues on GitHub, `python -m pytest -q`,
`python scripts/status.py`, `python scripts/review_due.py`.

## In flight

| PR | What | State |
|---|---|---|
| #7 | ADR-015: a strategy's stage is carried, not asserted (F-007, F-014) | The final text round: item 2 below |
| #20 | ADR-016 draft, Part 22, the ADR-012 amendment draft | Moves with ADR-015 |
| #33 | Parts 32-34 and the final-text-round session close | Open; see the warning below |
| Issue #35 | This branch: the pass on the 2026-09-25 review, and its fixes | Needs an independent pass before it lands |

**#33 will go red against this branch's new test, and that is the test working.**
`test_no_doc_names_a_finding_number_above_the_register` forbids any `.md` under
`docs/` from naming a finding number above the highest registered in
`docs/FINDINGS.md`. #33's branch names the burned number in four places, in
`docs/NOW.md` and its session record. The fix on that branch is to write "the
number after F-030" instead, or the bracketed `F-[NNN]` form when quoting. It was
not edited from here: one Issue, one branch, one claimant.

## Highest Priority Next Task

1. **An independent pass on Issue #35's branch, before it merges.** A fresh
   session told to falsify it. The pass already run covered `cbc4d20`; **the
   Part 35 work is later and has had none**, and it is the first production code
   in this workstream. Where to aim:
   - `framework/metrics/reporting.py` and `framework/data/fetch_record.py`: does
     the grade actually come from provenance, and can a caller still get Level C
     without a fetch?
   - **Run the mutation ADR-017 requires and has not had:** `disclosure_from`
     returning a plain `Disclosure` must turn the suite red. If it does not, the
     new guard is asserted by nothing, which is F-032's shape.
   - The full suite after the two test edits, which was never run locally.
   - Whether ADR-017's draft claims anything it has not checked.
   - The earlier work: whether the three F-032 tests isolate their guards
     (re-apply each mutation, confirm exactly one test fails), whether the two new
     conformance tests can be satisfied without fixing what they check, and
     whether the rewritten `docs/ROADMAP.md` Stage 2 prose is true.
2. **Finish the evidence bar the way Part 28e rules.**
   - **Step 1, the final text round on #7 and #20, with no redesign:** fix the
     fourth pass's two blocking findings (F4-3 and F4-1, Issue #21); apply
     28a-28d; settle the three open readings in the notes after Part 28, each
     as one question to the owner with a recommendation.
   - **Step 2, build the current-stage read as code**, once the owner says
     "go": tests written by a separate model from the review findings, a fresh
     review attacking the code, the ADR text updated to match what the code
     does, on its own branch as a draft, not merged until the ADRs are
     ratified. Not in this slice: the save-side checks, ADR-016's evidence
     checks.
3. **Two guards found by this session's pass, awaiting a finding number.**
   Both survive the suite at `704 passed`, and neither has a number because the
   gate allocates none until 2026-10-07 — inventing one is the mistake F-035 is
   about. Written up in `docs/sessions/2026-09-25-review-falsification.md`:
   - `framework/data/dolt_clone.py:376` — with the `isinstance(body, dict)`
     check removed, a bare `null` envelope from `dolt` yields a signed
     `FetchedSeries` with zero bars asserting success. The failure that
     function's own docstring says the module exists to prevent.
   - `framework/data/contract.py:244` — the inverted-window check on
     `fetch_daily_bars`.
4. **Small, when convenient:**
   - a full tautological-test survey over `tests/`; 22 of 143 `pytest.raises`
     calls are bare `pytest.raises(ValueError)` with no `match=`, 14 of them in
     `tests/artifacts/test_review_decision.py`;
   - the gate items #29 left: `fullmatch` on report names, surviving an
     invalid date, and ASCII digits in `REPORT` (`scripts/review_due.py`);
   - a sentence in the review skill (owner-only) saying to write every finding
     number in full ASCII (`F-NNN`), because the gate cannot read other shapes;
   - phase 2 of the file split, for `docs/DECISIONS.md`,
     `docs/OwnerDecisions.md`, `docs/OperatorChecklist.md` and `CHANGELOG.md`,
     once #7 and #20 have landed (`docs/proposals/growing-files.md`);
   - `scripts/verify_clone.py` has not run for five consecutive reviews for
     want of `dolt`, so the live data path is still unverified. (It refuses
     correctly with exit 1 when there is no clone; an earlier draft of this
     line said otherwise and was wrong.)

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
