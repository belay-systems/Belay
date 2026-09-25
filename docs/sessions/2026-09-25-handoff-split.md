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
  `python scripts/review_due.py` still gives the number after F-030 as the next one.
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
- **The independent pass on #32** found one blocking defect. This record had
  written the gate's next number out in full, so the gate answered one higher
  on every branch. It now says "the number after F-030", and the gate is back.
  The pass also found eight defects, all fixed with a test that goes red on
  the pass's own mutation:
  - a register row could be deleted silently;
  - a priority could drift from the archive;
  - one test was vacuous;
  - the Closed heading was not checked;
  - the next-task heading check was too narrow;
  - session records had no date or byte check;
  - the citation scan read untracked files;
  - a Part number was wrong.

## The other open pull requests (owner: "leave nothing for [the second contributor]")

Fresh-context falsification passes ran on #31, #24 and #14. The one on #22
was stopped, because Part 30 supersedes it.
- **#14:** nothing blocking. Four statements said more than their evidence;
  17a labels them, and family wording is redacted as in Part 11a.
- **#24:** every guard mutation and deletion turned exactly its own test red.
  The missing hash-half test for `orphan_versions` is added, a misleading
  comment is corrected, and `main` is merged in.
- **#31:** the recommendations answered "aligned" in Parts 25-28 are not on
  file. A notes block labels each line that goes beyond the record, for the
  owner to confirm.
- **#20:** its `docs/HANDOFF.md` appendix moved word for word to
  `docs/sessions/2026-09-22-adr-016-and-sample-adequacy.md`.

**Part 30** records the owner's rule that contributors help and never gate.

## Corrections to the archive

- `docs/HANDOFF.md:5768` and `:5842` list the `markdown-it-py` decision as
  pending. It is ruled: Part 24, on #31.
- Branch `claude/nice-fermat-pdyywp` (closed #28) appends 50 lines to the
  archive. All 43 non-blank lines of it are already on `main`
  (`git diff origin/main...origin/claude/nice-fermat-pdyywp`, with each line
  checked against the archive). The branch is left in place.

## Open

- #20 and #22 append to `docs/HANDOFF.md`. Whichever lands second adapts; the
  freeze test's message says how.
- The rule that a session record is never edited after it merges is not
  enforced yet. It needs git history in CI, which is Issue #9's mechanism.
- Phase 2 waits for #7, #20 and #31 to land.
