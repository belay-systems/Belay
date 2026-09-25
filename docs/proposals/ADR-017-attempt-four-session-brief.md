# ADR-017 attempt four — session brief

**Status: authorised work, not a proposal.** The owner ruled what attempt four must
meet on 2026-09-25, in `docs/OwnerDecisions.md` Parts 37, 38, 39 and 40. This brief
exists so the session doing the work starts from those rulings and the fourth pass's
findings rather than re-deriving them. It follows the pattern of
`docs/proposals/register-rebuild-session-brief.md`.

**Work the phases in order. Stop after each and report in under ten lines.** The
owner is not a developer: explain what each change is for before making it, and put
any decision that is the owner's as one question with a recommendation (`AGENTS.md`,
"Asking the owner").

---

## Before anything: synchronize

Follow `AGENTS.md`'s session workflow. Then confirm:

- `main` carries Parts 37-40 (`grep -n "^# Part 40" docs/OwnerDecisions.md`). If not,
  stop and say so: they are the specification.
- #36 (`claude/brave-pascal-e7401x`) is still open and unmerged. The work goes on
  that branch: it is Issue #35's, and it holds attempt three, Parts 35-36 and
  ADR-017's draft (`docs/proposals/ADR-017-grade-from-provenance-DRAFT.md` on that
  branch).

## The three facts that shape everything

1. **Attempt three's guards all work; its premise does not.** The fourth independent
   pass (<https://github.com/belay-systems/Belay/pull/36#issuecomment-5838006269>)
   mutated all eight guards and every one turned the suite red. What broke was what
   they are checked *against*: a repository and a store the caller chooses, paths
   that escape them, and prices bound by count and end dates only. Mutation cannot
   find a guard that does not exist; attacks can.
2. **The threat model is ruled (Part 37, option A).** Guard against honest mistakes
   in Belay's code, and make faking *visible in review*. Do not promise that code
   inside Belay cannot fake a Level C result — ADR-017's own argument shows no
   in-process check can, and three attempts failed by implying one could.
3. **The unkeyed hash is not authenticity.** `ArtifactIntegrity.sign` is public over
   an unkeyed hash. Never write "signed" as though it meant "came from the vendor".
   That error ran through two earlier attempts and four documents.

---

## Phase 1 — bring #36 up to `main`

Merge `main` into #36's branch (a merge commit; never rebase or force-push). Expect
conflicts in three files:

- `docs/OwnerDecisions.md` — keep every Part from both sides. Place #36's Parts 35
  and 36 immediately before Part 37, so the file reads in number order. No text
  changes.
- `docs/OperatorChecklist.md` — keep both sides, `main`'s text first.
- `docs/NOW.md` — **do not keep both sides**: two next-task lists fail
  `tests/test_handoff_files.py`. Take `main`'s file and carry over any fact from
  #36's "Where things stand" that is still true; this session rewrites it at close.

Run `python -m pytest -q`. Report the count and stop.

## Phase 2 — fix the documents the fourth pass found wrong

On #36's branch, against the pass's numbering:

- **B4** — `docs/OperatorChecklist.md`, "Open — ratify or reject ADR-017": the
  guarantee it gives the owner ("on disk in the repository where it says it is,
  these are its bytes, this is its series") is false in every clause. Replace it
  with what attempt four actually guarantees, once it does.
- **D1** — ADR-017's Decision item 3 still describes attempt one's signature.
- **D2** — Part 36's "What it settles" (36a-36c) holds the mechanism, the guarantee
  and "35a is delivered", beyond the owner's words "yes require the stored fetch
  record". Move them to "Session readings" with a "Corrected" note; do not delete.
- **D4** — docstrings in `framework/metrics/reporting.py` (`Disclosure.evidence_level`,
  `FetchedDisclosure`) and `framework/data/fetch_record.py` (`disclosure_from`'s
  "Five checks") still state attempt two's guarantees.
- **D5** — the checklist's "Done" entry for the Part 36 question describes attempt two.

Report and stop.

## Phase 3 — write the tests first, from the findings, not from the code

Each attack becomes a test that passes only when the attack is refused. Where
possible, have a separate model or session write them from the pass's text.

- **B1** — a forged record saved into a repository and store in a temporary folder
  of the caller's choosing must not yield Level C.
- **B2** — with the repository's own roots, an identifier or `store_path` containing
  `..` must be refused; so must a loaded record whose identifier differs from the one
  asked for, and a `Fetch` whose `record` is not an `Artifact`.
- **B3** — a genuine fetch with any price changed on the same dates must not yield
  Level C. Also a changed symbol.
- **D3 / Part 39** — a metric artifact computed over a fetch must name the record's
  identifier, version and what binds its prices; the name must resolve to that record.

All must fail against attempt three. Show that, then stop.

## Phase 4 — build attempt four to Parts 37-40

- **Roots are not parameters.** Read records only from the repository's own
  `artifacts/` and bytes only from `data/market/`. Resolve every joined path and
  require it to stay under its root.
- **Bind the prices (Parts 38 and 40).** Choose the method and write down why and
  which weakness is accepted. **Read Part 40's "What the owner was told that was
  wrong" first.** In short:
  - *re-parsing the stored bytes* changes no record, but needs new code (DoltHub
    joins one JSON document per month with newlines and `_parse` reads one) and
    passes a parser change **silently**;
  - *a stored fingerprint* adds a field to future fetch records (an ADR-014
    change), fails **loudly** on a parser change, and cannot recover without
    revisiting ADR-014 rule 5, which writes no new record for identical bytes.
    `RPT-0001` need not be migrated; it cannot back Level C in any case.
  The owner chose to leave this to you and your independent pass, knowing the
  session recommended the fingerprint.
- **Name the record (Part 39).** On every metric artifact computed over a fetch,
  including Level D ones on adjusted prices. The evidence record's `provenance`
  line is the described place; the four `Disclosure` fields must not change
  (`tests/test_governance_conformance.py`).
- Then mutate each new guard one at a time on a **committed** tree and show exactly
  one test goes red. A harness here once destroyed an uncommitted implementation
  with `git checkout --`.

## Owner questions this work will raise — ask, do not decide

- **Refuse or grade Level D on a mismatch.** Part 38 points to Level D; Part 36's
  reading chose refusal. If the build needs one, put it as one question.
- **What a later re-check does** when a named record is missing or changed
  (Part 39, not settled).
- **That the named record is committed** wherever the metric artifact is. Part 37's
  readings show "visible in review" needs it; it was not asked.
- **Any ADR-014 change** the chosen method needs.

## Phase 5 — the independent pass, then stop

Update ADR-017's draft to say exactly what the code does and no more. Then a fresh
session, told to falsify, attacks attempt four: new routes to Level C, the method
chosen under Part 40, and every claim in ADR-017 and Parts 35-40 against the code.
Fix what it finds. **Ratification is the owner's, after that pass, not before.**

## Do not

- ratify ADR-017, change an ADR's status, or edit `constitution/`;
- restate `python scripts/review_due.py`'s next finding number anywhere;
- merge #36 without the owner's word;
- call anything verified on the strength of your own review.
