# Register rebuild, then F-007 — session brief

**Status: authorized work, not a proposal.** The register rebuild follows from the
owner's 2026-08-26 approval of the 2026-08-21 findings; F-007 was ruled for fix by
the owner 2026-08-14 (`docs/OwnerDecisions.md` Part 8).

This brief exists so the session doing the work starts from settled facts rather
than re-deriving them, and so starting that session needs one sentence rather
than a pasted prompt. It follows the pattern of
`docs/proposals/F-007-session-brief.md`.

**Work the phases in order. Stop after each and report in under ten lines.** Do
not batch them. The pacing is deliberate — it keeps the session's cost visible
and interruptible.

---

## Do not start until these are merged

`main` must contain all four:

- `reports/review/2026-08-14-review.md`
- `docs/OwnerDecisions.md` Part 8
- `reports/review/2026-08-21-review.md`
- `.github/workflows/conformance.yml`

If any is missing, stop and say which. The register cannot be rebuilt correctly
before the 2026-08-14 findings are on `main`.

---

## The one fact that governs everything below

**Two reviews collided over finding numbers.** The 2026-08-14 review claimed
F-007..F-012 and its ruling registered F-013. The 2026-08-21 review could not see
them — they sat on unmerged branches — and reused F-007..F-015. Its report now
carries a correction block with the authoritative mapping.

**The durable series is:**

| Range | Source | State |
|---|---|---|
| F-001..F-006 | 2026-08-01 review | F-001, F-002, F-005 closed |
| F-007..F-013 | 2026-08-14 review | all ruled for fix |
| F-014..F-018 | 2026-08-21 review | approved 2026-08-26 |

Four findings in the 2026-08-21 report are **withdrawn as duplicates** and must
never be registered: its F-008, F-009, F-010 and F-012 restate the 2026-08-14
review's F-007, F-012, F-008 and F-011 respectively.

---

## Standing rules

1. **Branch, never `main`.** CI gates `main` once the ruleset in
   `docs/OperatorChecklist.md` is set, and a direct push is refused regardless.
2. `pip install -e ".[dev]"` before anything — pytest is an optional extra at
   `pyproject.toml:26`. Baseline: **626 passed, 1 skipped, 5 xfailed**.
3. **`docs/HANDOFF.md`'s Open Findings summary table and its `## ` sections must
   stay in lockstep** — same count, same order, same wording after
   normalisation. `tests/test_status_dashboard.py:99` and `:116` enforce both and
   will turn the suite red. Edit one, edit the other.
4. **`tests/test_session_handoff.py` polices the handoff itself**, and this
   session edits exactly what it watches. Six checks, added 2026-08-27, each
   confirmed to fail against a deliberately broken copy. Two will bite here if
   the work is done carelessly:
   - **Closing a finding while the next-task list still names it** turns
     `test_the_next_task_list_does_not_name_a_finding_that_is_already_closed`
     red. Phase 8 moves F-007 to `# Closed Findings`; if "Highest Priority Next
     Task" still says F-007, the suite fails. That is the test working. Update
     both in the same commit.
   - **A session brief nothing references** turns
     `test_no_session_brief_is_orphaned` red. It already caught one real orphan
     on its first run — this very brief, twenty minutes after it was committed.
     If a new brief is written, point a document at it.

   It also checks that every ``path:line`` citation in tracked prose resolves to
   a line that exists, so moving code moves the citations that name it.
4. **The independent verification pass runs before a change lands, not after.**
   This repository has lost a session's work to getting that ordering wrong.
5. Close the session per `AGENTS.md` steps 13 and 14 — rewrite `docs/NOW.md`,
   and record anything only the owner can do in `docs/OperatorChecklist.md`.
   These are no longer honour-system: rule 4's tests fail when they are skipped.

---

## Phase 1 — Ground truth

Confirm the four merges. Install, then run `python -m pytest -q` and
`python scripts/status.py`. Report the open-findings count the dashboard prints.
**Stop.**

## Phase 2 — Rebuild the register

Branch `register/2026-08-21-corrected`. `main` now carries F-007..F-013. Add the
five that stand — prose is reusable from the blocked PR #4's comments, minus its
wrong numbers:

| Number | Finding | Severity | Priority |
|---|---|---|---|
| **F-014** | A promotion can be recorded with no evidence whatsoever | Critical | P1 |
| **F-015** | `belay doctor` cannot fail | High | P2 |
| **F-016** | `is_clean` decides whether the survivorship warning prints, and has no test | Medium | P2 |
| **F-017** | The significance test's two-sidedness is asserted by nothing | Low | P3 |
| **F-018** | "Searched all 101 documents" has rotted to 107 | Low | P3 |

Expected end state: **33 open findings** [**scope note added 2026-09-19** — true
for Phase 2 as PR #9 (`register/2026-08-21-corrected`) lands it. The stacked PR
#11 (`register/2026-09-reviews`) registers twelve more immediately after,
bringing the count to **43**. Original wording left standing under Law VII]
[**further corrected 2026-09-19, at that same PR #11's own close-out** — PR
#11 also closes F-022 in its close-out commit, so the count it actually leaves
the register at, once it lands, is **42**, not 43. Both prior notes left
standing under Law VII; this is the count to expect once PR #11 has landed]
[**corrected once more 2026-09-19** — the pull request
`fix/review-skill-numbering` closes F-025 as well, so once it and PR #11 have
both landed the register stands at **41**, not 42. All three prior notes left
standing under Law VII; this is the count to expect then].
Add the `## ` sections *and* the
matching summary-table rows — standing rule 3. The count `scripts/status.py`
prints must read 33 [**as above** — 42 once PR #11 has landed, corrected
2026-09-19 from the 43 first written here, and **41** once
`fix/review-skill-numbering` has landed too]. Also point
"Highest Priority Next Task" at this brief, so the
next session after this one needs no prompt either. Commit, push, open a PR.
**Stop.**

## Phase 3 — Read F-007's brief before touching code

`docs/proposals/F-007-session-brief.md` starts from executed evidence. Read it
plus `framework/artifacts/factory.py`, `framework/artifacts/integrity.py`,
`framework/artifacts/repository.py`, `tests/artifacts/test_factory.py`. Reproduce
the defect and paste the output. **Stop.** Report whether it reproduces and what
the brief already settles.

## Phase 4 — Rule it, only if the brief says a ruling is owed

The brief flags F-007's definition of "birth" as the part a fresh reader should
attack. If closing it needs a decision no document has made, draft **ADR-015** in
`docs/DECISIONS.md` (ADR-014 is the highest) and **stop for the owner's
ratification**. If the brief settles it, say so and skip to Phase 5.

**One conclusion no ADR here may reach:** that a strategy may exist past `IDEA`
without having climbed there. `constitution/Paper_First_Capital_Doctrine.md:5-7`
is unconditional — "Every strategy begins with zero capital. No exceptions." If a
rule permitting it seems forced, stop and name what is forcing it. That is a
constraint the owner needs to see, not a conclusion to adopt.

## Phase 5 — Tests first, run red

Write them for the ratified shape. Run them **red** against unchanged code and
paste the failures. **Stop.**

## Phase 6 — Implement, minimally

Smallest change that closes it. Full suite green. **Stop.**

## Phase 7 — Independent verification, before committing

Attack the change with fresh eyes and without trusting Phase 6's reasoning:

- Can a STRATEGY artifact still reach a capital stage by *any* path —
  `ArtifactFactory`, bare `Artifact(...)` + `ArtifactIntegrity.sign()`,
  `ArtifactSerializer.load()`, a hand-edit that is re-hashed?
- Does any new test pass for the wrong reason? A bare `pytest.raises(TypeError)`
  passes on a misspelled keyword — this repository has shipped that shape twice.
- Do the new docstrings assert anything the mechanism does not deliver?
- Did any prose citation elsewhere just become wrong?

Report every defect with executed evidence before touching git. **Stop.**

## Phase 8 — Land it

Fix what Phase 7 found. Update `CHANGELOG.md`, and move F-007 to
`# Closed Findings` in `docs/HANDOFF.md` — removing its summary-table row,
renumbering the rows below it, count 33 → 32 (standing rule 3)
[**scope note added 2026-09-19** — if the stacked PR #11 has landed by the time
Phase 8 runs, the register already carries 43 open findings, not 33, and this
becomes count 43 → 42. Original arithmetic left standing for the case PR #11 has
not yet landed] [**further corrected 2026-09-19, at PR #11's own close-out** —
PR #11 closes F-022 in the same close-out commit that this note was already
anticipating, so if PR #11 has landed by the time Phase 8 runs, the register
carries **42** open findings, not 43, and closing F-007 then becomes count
**42 → 41**. Both prior notes left standing under Law VII] [**corrected once
more 2026-09-19** — `fix/review-skill-numbering` closes F-025 too, so with both
that pull request and PR #11 landed the register carries **41**, and closing
F-007 then becomes count **41 → 40**. All three prior notes left standing under
Law VII]. Push, open a PR,
confirm CI green. **Stop before merging.**

---

## Carried, not in scope here

- **F-014 is Critical and unruled.** A promotion to `MICRO_CAPITAL` can be
  recorded with no evidence at all; `constitution/Paper_First_Capital_Doctrine.md:45-47`
  — "Promotion requires evidence. Never confidence alone" — is implemented
  nowhere and tested nowhere. **Time-sensitive:** `artifacts/RPT-0001/1.0.0.yaml`
  is still the only artifact in the history, so no REVIEW record exists and the
  one-way door on its `content` shape is open. It closes the first time a REV is
  signed. This wants an owner ruling, then its own session.

  **Corrected 2026-09-19.** The sentence above read "ADR-014 rule 6's one-way
  door on its `content` shape", and rule 6 rules nothing about REVIEW artifacts.
  `docs/DECISIONS.md:3375-3393` is about the **fetch record's** signed content
  gaining the source key, the store version and the store-relative path. What
  carries across to REVIEW is rule 6's *reasoning* at `docs/DECISIONS.md:3387-3393`
  — changing signed content is free only while nothing is stored — not its
  ruling. The door is real and open; no rule names it. Registered with the same
  correction in `docs/HANDOFF.md`'s F-014 section.
- **The 2026-08-14 review has been attacked by nobody.** The 2026-08-21 pass
  believed 2026-08-01 was the prior report and reviewed that instead. Phase 4 of
  the next `/belay-review` owes it a meta-review.
- **Two owner-only actions** are queued in `docs/OperatorChecklist.md`.
