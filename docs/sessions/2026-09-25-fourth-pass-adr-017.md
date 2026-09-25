# 2026-09-25 — the fourth falsification pass on ADR-017, and Part 37

## What was asked

"Lets do the fourth falsification pass before ADR-017's ratification." That pass
was item 1 of the next-task list on #36 (`claude/brave-pascal-e7401x`), with three
aims:

1. find a route to Level C that does not need `fetch_and_record` to run and its
   output to stay intact;
2. mutate all eight guards in `disclosure_from` one at a time, on a committed tree;
3. check that Part 36 and ADR-017 claim nothing more than the owner ruled.

Then, after the pass, the owner asked for help choosing between the two threat
models it raised, and chose option A (Part 37).

## What was done

**The pass**, on #36's head `f9d6a64`, in a scratch clone. Posted in full on #36:
<https://github.com/belay-systems/Belay/pull/36#issuecomment-5838006269>. Nothing
was pushed to #36's branch.

Four blocking findings:

- **B1.** Level C with no fetch of any kind. `disclosure_from` takes its
  `repository` and `store` as arguments, and both take any folder. A forged record
  saved into a temporary folder produced a signed, validating Level C metric
  artifact claiming a licensed vendor and no survivorship bias.
- **B2.** Pinning the default folders does not close B1. Neither the record
  identifier nor the record's `store_path` is kept inside its root, `repository.get`
  does not check that the file it loaded carries the identifier asked for, and
  `Fetch` checks no types.
- **B3.** Prices are not bound to the record. The series is checked by bar count
  and first and last date only. A genuine fetch with its closes replaced (1.00 then
  900.00, relabelled GME) was still Level C as DoltHub AAPL. This one needs no
  adversary: a backtest that adjusts prices after the fetch does the same.
- **B4.** The owner-facing ratification question on #36 states a guarantee — "on
  disk in the repository where it says it is, these are its bytes, this is its
  series" — that B1-B3 show false in every clause.

Five defects: a correction recorded as made in `54ce3be`'s message but never applied
to ADR-017's Decision section (D1); Part 36's "What it settles" still holding the
mechanism, the guarantee and "35a is delivered" beyond the owner's words (D2); a
Level C metric artifact naming no fetch record, so its grade can never be
re-checked (D3); code comments still stating attempt two's guarantees (D4); the
owner-facing "Done" entry for Part 36 describing attempt two (D5).

**Aim 2 held in full.** All eight guards reproduce ADR-017's Verification block
exactly: seven fail one test each and the repository re-read fails the two named.
Four further mutations were also caught. The holes are checks that do not exist,
which mutation cannot find.

**The owner's decision.** Put as one question with a recommendation, A. The owner
asked first whether a blockchain or web3 design would help; the answer given was no,
for this problem, with the reasons recorded in Part 37. The owner then said "A - per
your recommendations". Recorded as Part 37, with "per your recommendations" read as
covering A only, since the two follow-ups had not yet been put with their costs.

**Follow-up 1, put on its own.** Should a fetch record store a fingerprint of the
prices, with Level C requiring the series to match it? Recommended yes, with the
cost stated: prices adjusted after the fetch are Level D until the adjustment is
recorded. The owner said "yes to fingerprint". Recorded as Part 38, together with a
consequence not stated when it was put: `RPT-0001` has no fingerprint and cannot
back Level C until re-fetched.

**Follow-up 2, put on its own.** Should every result name the fetch record behind
its grade — identifier, version and fingerprint — so the grade can be re-checked
later? Recommended yes, on the existing `provenance` line. The owner said "yes".
Recorded as Part 39, with the placement kept as a session reading and one
consequence not stated when it was put: the change alters the integrity hash of
every metric artifact built after it (none is stored).

## Files changed

- `docs/OwnerDecisions.md` — Parts 37, 38 and 39.
- `docs/OperatorChecklist.md` — the question as put (Done), the two follow-ups
  (Open), and ratification (Later).
- `docs/NOW.md` — "In flight" and the next-task list.
- This record.

No code changed.

## How it was verified

In a scratch clone of #36's head, before any attack:

```
$ python -m pytest -q          720 passed, 1 skipped, 5 xfailed
$ python scripts/status.py     exit 0, 45 open findings
$ python scripts/review_due.py SKIP, next due 2026-10-07 (exit 1)
```

Each attack was a script run against unmutated code; the outputs quoted on #36 are
pasted, not paraphrased. Each mutation was applied to a committed tree, the full
suite run with `__pycache__` cleared, the file restored, and `git status` checked
clean before the next. Every line citation in the posted pass was re-read against
the file after writing; one (`reporting.py`) was wrong by a line and was corrected
before posting.

On this branch, the suite was run after the edits (see the pull request).

**Independent pass on this record and Part 37:** see the pull request. Part 37 is
the kind of text three passes on #36 caught claiming more than the owner said, so it
was checked for exactly that.

## What is open

- **Attempt four of ADR-017**, on #36, built to Parts 37-39 and the fourth pass's
  findings, then its own independent pass. Not before.
- **Left open by Parts 38 and 39:** how an adjustment is recorded; refusal or
  Level D on a mismatch; what a later re-check does when a named record is missing
  or has changed.
- **Merge order.** Parts 37-39 refer to Parts 35 and 36, so this branch should merge
  after #36. Both edit the end of `docs/OwnerDecisions.md` and
  `docs/OperatorChecklist.md`, and both edit `docs/NOW.md`: keep `main`'s text first
  and add this branch's after it.
