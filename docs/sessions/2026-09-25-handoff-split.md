# 2026-09-25 — The handoff is split: current state apart from history

Branch `claude/festive-faraday-p077fv`, from `origin/main` at `1c8eb1c`. This
is the first record in `docs/sessions/`.

## What the owner asked

First: "is there any precedent or known first principles about capped or other
structure for our handoff and other growing files to be more better?" Then,
after the answer: "write it all up, and implement it accordingly … surgical
implementation" (`docs/OwnerDecisions.md` Part 29). Mid-session, the owner
also asked this session to take over the other open session, "Belay threads
status", which drives #31, #7 and #20.

## What was done

- **The write-up:** `docs/proposals/growing-files.md`. It covers the evidence,
  the precedents, the principles, phase 1 as built, and phase 2 as proposed.
- **New files:**
  - `docs/NOW.md`, the current state, capped at 200 lines;
  - `docs/FINDINGS.md`, the register, with 41 open rows built by script from
    the archive, so every title and priority is copied rather than retyped;
  - `docs/sessions/` and its `README.md`;
  - `tests/test_handoff_files.py`.
- **`docs/HANDOFF.md` is frozen in place.** Only line 1, the title, changed,
  and it changed in place, so the file is still 5,857 lines. A SHA-256 pin
  holds the freeze.
- **`scripts/status.py` reads the register from `docs/FINDINGS.md`.**
  `tests/test_status_dashboard.py` now checks the table against the archive's
  section titles, and counts rows by a route other than the parser's own
  pattern.
- **`tests/test_session_handoff.py`** reads the next-task list from
  `docs/NOW.md`, and reads closures from both the archive and the register.
- **Instructions repointed, each with its line count unchanged:**
  - `AGENTS.md` steps 3 and 13, its start-up paragraph and "Current
    Priority". "Files that grow" is appended to it;
  - `CLAUDE.md`, `README.md`, `docs/README.md` and `CONTRIBUTING.md`;
  - the review skill's reading list and red-team item E5;
  - the Issue and PR templates.
- **Part 29** is appended to `docs/OwnerDecisions.md`.

## The other session

"Belay threads status" was idle, waiting on the owner's "go" for a code plan:
Part 28e step 2 on #31's branch, building the current-stage read as code.
This session has no channel to a cloud session and cannot read that session's
chat. Its pushed state is on #31, #7 and #20 and on Issue #21. The owner pasted
its last message, the plan, into this session. The plan is carried into
`docs/NOW.md` item 2, still waiting on the owner's "go".

## Verified, and how

- **Baseline on `1c8eb1c`:** `python -m pytest -q` gave 685 passed, 1 skipped,
  5 xfailed, and `python scripts/status.py` exited 0.
- **On this branch:** 693 passed, 1 skipped, 5 xfailed. `status.py` exits 0
  and lists 41 findings, the same titles and priorities as before.
  `python scripts/review_due.py` still gives F-031 as the next number.
- **Line citations:** 241 citations point into the five large files
  (`git grep -h -o -E "<Name>\.md:[0-9]+" | wc -l`). Not one moved, because
  every edited line was replaced in place and every addition was appended.
  The same holds for the code and tests, checked by diffing each against
  `HEAD` by line position. The exceptions are the code this change rewrites
  on purpose:
  - `scripts/status.py` lines 183-212 (`open_findings`), where lines 1-182 and
    213 on are unchanged;
  - `tests/test_status_dashboard.py` after line 79, the replaced tests.

  Citations into those regions (`:187-213` and `:198-199` of `status.py`,
  `:99` and `:116` of the dashboard tests) are in dated records, and they
  describe the code as it was.
- An independent fresh-context pass ran before pushing. Its findings and what
  was done about each are on the pull request.

## Open

- #20 and #22 append to `docs/HANDOFF.md`. Whichever lands second adapts; the
  freeze test's message says how.
- The rule that a session record is never edited after it merges is not
  enforced yet. It needs git history in CI, which is Issue #9's mechanism.
- Phase 2 waits for #7, #20 and #31 to land.
