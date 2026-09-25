# 2026-09-25 — the fourth falsification pass on ADR-017, and Parts 37-40

## What was asked

"lets do the fourth falsification pass before ADR-017's ratification." That pass
was item 1 of the next-task list on #36 (`claude/brave-pascal-e7401x`), with three
aims:

1. find a route to Level C that does not need `fetch_and_record` to run and its
   output to stay intact;
2. mutate all eight guards in `disclosure_from` one at a time, on a committed tree;
3. check that Part 36 and ADR-017 claim nothing more than the owner ruled.

Then, after the pass, the owner asked for help choosing between the two threat
models it raised, chose option A (Part 37), answered the two follow-ups (Parts 38
and 39), and, once told the fingerprint was not the only method, left the method to
attempt four (Part 40).

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
covering A only: the follow-ups' costs had been stated, but the session had said it
would bring them one at a time and had asked only "do you choose A?".

**Follow-up 1, put on its own.** Should a fetch record store a fingerprint of the
prices, with Level C requiring the series to match it? Recommended yes, with the
cost stated: prices adjusted after the fetch are Level D until the adjustment is
recorded. The owner said "yes to fingerprint". Recorded as Part 38.

**Follow-up 2, put on its own.** Should every result name the fetch record behind
its grade — identifier, version and fingerprint — so the grade can be re-checked
later? Recommended yes, on the existing `provenance` line. The owner said "yes".
Recorded as Part 39, with the placement kept as a session reading and one
consequence not stated when it was put: the change alters the integrity hash of
every metric artifact built after it (none is stored).

## Files changed

- `docs/OwnerDecisions.md` — Parts 37 to 40.
- `docs/OperatorChecklist.md` — five Done entries (option A, the two follow-ups,
  the method, and keeping Part 40), and ratification (Later).
- `docs/NOW.md` — rewritten at close for `main` once #37 has merged.
- `docs/proposals/ADR-017-attempt-four-session-brief.md` — the next session's brief.
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

Part 39's claim that the `provenance` text is inside the evidence hash was checked
by building two evidence records that differ only in it: the hashes differ.

On this branch after every change: `704 passed, 1 skipped, 5 xfailed`, and CI green
on #37.

## The independent pass on these records, and what it changed

A fresh agent was told to falsify Parts 37-38 and these records against a verbatim
transcript of the owner exchange. It edited nothing. It found 2 blocking, 7 defects
and 11 notes; every item checked here was real. The ones that changed a ruling's
record or what the owner must hear:

- **The fingerprint is not the only method.** The owner was told it was "the only
  thing that catches" changed prices. Re-parsing the stored bytes, already
  hash-checked, is a second method that changes no fetch record. Verified: each
  source has a parser (`_parse` in `framework/data/dolthub.py` on #36). Recorded in
  Part 38 and put back to the owner, who left the method to attempt four and its
  independent pass (Part 40).
- **Re-fetching does not give `RPT-0001` a fingerprint.** Identical bytes return the
  existing record (ADR-014 rule 5, and `fetch_and_record` on #36), and changing a
  saved record's signed content is a migration under ADR-014. The ADR-014 cost was
  not stated to the owner. Recorded in Part 38.
- **The reason for reading "per your recommendations" narrowly was false** (costs
  had been stated); the true reason and the ambiguity are now in Part 37.
- **Option A depends on Parts 38 and 39**, and on the named record being committed;
  Part 37 had presented them as add-ons.
- **The blockchain answer was wrong about B3**, which is a genuine record with prices
  changed afterwards. The conclusion stands; the correction is in Part 37.
- **The merge rule for `docs/NOW.md` was wrong.** Keeping both sides gives two
  next-task lists and fails the build (`2 failed, 718 passed` in its rehearsal on
  top of #36). Corrected here and in `docs/NOW.md`.

Also fixed: 37a in the future tense rather than as delivered; 38b says "prices",
not "series"; a claim that the Part 36 recommendation had already named the ADR-014
cost (it had named it for metric artifacts, not fetch records); stale checklist and
`docs/NOW.md` text after Part 38; the #33 row's missing warning; a stale
finding-number sentence in `docs/NOW.md`; the owner's quote, which begins "lets".

Every correction to a ruling's record says so in the Part itself ("Corrected before
merge"), rather than being edited away.

## The second independent pass, and what it changed

A second fresh agent reviewed Part 39, the fixes above and Part 40 against the same
transcript, and rehearsed the merge onto #36 (`720 passed`). It found no blocking
item, 5 defects and 6 notes; each defect was checked here before acting. The ones
that mattered reached the owner's decisions:

- **Re-parsing is not available as DoltHub's data is stored** (one JSON document per
  month joined by newlines; `_parse` reads one). Confirmed by reading
  `framework/data/dolthub.py` on #36; its own comment says "re-parsing is not this
  hash's job". The first pass's "verified: each source has a parser" had checked only
  that `_parse` exists.
- **The parser-change weakness was given to the wrong method**, and the owner was
  shown it backwards when deciding Part 40. Confirmed from `fetch_and_record`'s
  existing-record path, which returns a freshly parsed series beside the old record.
- **The migration of `RPT-0001` was overstated.**

Recorded in Parts 38 and 40 and put back to the owner as one question: keep Part 40,
or go back to the stored fingerprint (recommended). The owner said "aligned - keep
part for", which read both ways, so the session asked which was meant; the owner
chose "Keep Part 40". Recorded in Part 40, with the recommendation noted as not
taken. Also fixed:
Part 37's blockchain note misstated what the owner was told about B2; 39a narrowed
"every result" to Level C inside "What it settles" (moved to a reading, which now
keeps adjusted-price results naming their record); quote marks around words the
owner did not say; a count without its command; and the `docs/NOW.md` merge rule,
which said "add" where it must say "replace" (superseded at close; see below).

## What is open

- **Attempt four of ADR-017**, on #36, built to Parts 37-40 and the fourth pass's
  findings. It picks the method that binds the prices and says which weakness it
  accepts; its own independent pass checks that choice. Ratification after, not
  before.
- **Left open by Parts 38 and 39:** how an adjustment is recorded; refusal or
  Level D on a mismatch; what a later re-check does when a named record is missing
  or has changed; that the named record is committed.
- **Merge order, reversed at close.** The records above said #37 merges after #36.
  At close the owner said "merge approved if needed", and #37 was merged first: the
  owner's rulings bind only once on `main` (the review procedure treats a Part on an
  unmerged branch as a proposal), and the next session starts from `main`. #36 was
  **not** merged: the fourth pass's blocking findings stand against it, and attempt
  four is built there. When #36 later merges `main`, keep both sides in
  `docs/OwnerDecisions.md` (placing Parts 35-36 before Part 37) and
  `docs/OperatorChecklist.md`, and take `main`'s `docs/NOW.md`. The brief says so.
- **Set up for the next session:** `docs/proposals/ADR-017-attempt-four-session-brief.md`,
  named from `docs/NOW.md`'s item 1.
