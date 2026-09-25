# 2026-09-25 — The final text round on ADR-015 and ADR-016 (Part 28e, step 1)

Branch `claude/great-turing-v2d0x8` (#33), from `origin/main` at `84eed17`.
The session also pushed to #7 (`adr/015-stage-is-carried`) and #20
(`claude/pensive-hypatia-nu6j3j`) with the owner's permission.

## What the owner asked

"begin from docs/NOW.md". The session found that `docs/NOW.md` was stale on one
point: it listed step 1 of 28e (fix F4-3 and F4-1, apply 28a-28d) as still to do,
but #7 at `ddda627` and #20 at `5714814` already carried that revision, written
before NOW was rewritten. Nobody had yet tried to break it. Asked what this
session should do, the owner chose "Finish step 1 (Recommended)": a fresh attack
pass, `main` merged into #7 and #20, the three open readings put one at a time,
and `docs/NOW.md` corrected.

## What was done

- **#7 and #20 brought up to date with `main`** (`4308d24`, `ffe54a0`). Every
  conflict was an append at the end of a file, resolved as NOW directed: `main`'s
  text first, then the branch's. No line of either side was lost (`git diff
  origin/main -- <file> | grep -c '^-[^-]'` gave 0, and the same against the
  branch). `docs/HANDOFF.md`, `docs/OwnerDecisions.md` and `docs/NOW.md` are
  byte-identical to `main` on #7. On #20, Part 22 now follows Part 31. Nothing
  cites Part 22 by line. `b4c85ac` closes #20's 2026-09-22 checklist item
  "what the owner needs to chase", which events had overtaken. CI passed on both.
- **Part 32**, the three open readings, answered one at a time:
  - **32a:** "Today's bar", against the session's recommendation. It overrules
    25g's "It does not re-judge past steps".
  - **32b:** 25h and 26b amend 18e.
  - **32c:** 18g's fresh pass stands, on the text as ratified.
- **The fifth pass.** A fresh-context agent attacked ADR-015 at `ddda627` and
  ADR-016 at `5714814`. It found both not ready:
  - F5-2 (blocking): two declared-yes repairs together undo a demotion into
    capital;
  - F5-5 (blocking): the capital rungs needed a 10-year paper or live report;
  - nine should-fix findings and one nit.
  - The driving session checked F5-2 and F5-5 against the text before relying
    on them. Posted on Issue #21, comment "Fifth pass".
- **Part 33**, four questions, one at a time, each answered with the
  recommendation:
  - **33a:** small fixes now, and every other attack becomes a step-2 test;
  - **33b:** rule 8's report is a backtest report (F5-5);
  - **33c:** a repair sets aside forgeries only (F5-1);
  - **33d:** a date correction never moves a demotion earlier (F5-7).
- **ADR-015** at `2393ff1` (Part 32), `1c75876` (Part 33 and F5-2, F5-9,
  F5-10, F5-11) and `c11bf59` (Part 34). Every edit replaced lines one for one, so the file stays 6,565
  lines and every line citation into it still resolves.
- **ADR-016** at `daf9234` (Part 32: rule 10, rule 6, item 12), `51e35a3`
  (Part 33: rule 8, test 22a, stale lines, Changes rows 36-47) and `6388254`
  (Part 34: the author's errors, Required Follow-Up item 19, Changes row 48). It
  is repointed to ADR-015 at `c11bf59`.
- **The sixth pass.** A fresh-context agent attacked this session's Part 32
  and Part 33 edits (`4308d24..1c75876`, `b4c85ac..51e35a3`) and the record of
  the two Parts.
  - It found 5 blocking findings. F6-1, F6-2 and F6-5 were the author's
    errors. The session checked F6-1 and F6-2 against the text.
  - It found 15 others, and five questions for the owner.
  - Nothing had been pushed, so no error reached #7 or #20.
- **Part 34.** The owner chose "Fix my errors, then stop (Recommended)". The
  author's errors are fixed. 32a and 33c are corrected in place, before merge,
  to name 25g's first two sentences and to say "file", as the owner's answer
  did. The rest is open (ADR-016 Required Follow-Up, item 19).
- **This record, `docs/NOW.md` rewritten, and a checklist entry.**

## What was verified, and how

- `python -m pytest -q`: 704 passed, 1 skipped, 5 xfailed, on `main`, on both
  merges, and on every commit above. `status.py` exits 0 with 40 open findings.
  `review_due.py` gives F-031.
- ADR-015's line neutrality: `git diff --numstat` gave 30 lines added and 30
  removed for Part 33. A script checked 18 cited lines at `1c75876` for the words
  each row describes. Its one miss was the check's own error: "(30b)" is on line
  6428, inside the cited range 6427-6428.
- **The fifth pass and the sixth are independent of the author.**
  - The sixth pass confirmed that ADR-015 has 6,564 lines at both ends and all
    17 hunks replace lines one for one. It also confirmed that 29 citation
    ranges and Changes rows 36-47 resolve, and that bold markers pair.
  - **The Part 34 fixes have had no pass** (34b). They are line for line too.
    A script found all 19 lines Changes row 48 cites at `c11bf59`, and the
    suite gives 704 passed on both branches.

## What is open

- **Step 2 of 28e waits on the owner's "go"**, and the five questions come
  first (`docs/NOW.md`).
- **The scheduled review is due**, starting at F-031.
- **After step 2:** the fresh pass on the text as ratified (32c), then the
  owner's ratification of both ADRs.
