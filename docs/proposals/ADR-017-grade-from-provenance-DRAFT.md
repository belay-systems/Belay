---
id: ADR-017-DRAFT
title: "ADR-017 (PROPOSED): A Computed Number Is Level C Only When Its Series Came From A Recorded Fetch"
type: Proposal
status: Proposed
version: 1.0.0
author: Belay
created: 2026-09-25
updated: 2026-09-25
evidence: D
---

# ADR-017 (PROPOSED): a computed number is Level C only when its series came from a recorded fetch

**PROPOSED, not ratified. Only the owner ratifies an ADR** (`AGENTS.md`, "What only
the owner may change"). It sits under `docs/proposals/` because ADR-015 (#7) and
ADR-016 (#20) are still drafts on branches and `docs/DECISIONS.md` on `main` ends at
ADR-014.

**The number 017 is claimed, not allocated.** ADR-015 is on #7 and ADR-016 on #20,
both unmerged, so 017 is the next free number *given those two land*. There is no gate
for ADR numbers as there is for finding numbers (`scripts/review_due.py`), which is
the same collision shape F-035 describes. If #7 or #20 is abandoned, renumber this.

## Status

Proposed 2026-09-25. **The substance is ruled** — `docs/OwnerDecisions.md` Part 35,
where the owner answered "Aligned to recommendations" to the question put in
`docs/OperatorChecklist.md`. What is *not* ruled is this document's wording, and
ratification is the owner's act.

## Context

`reports/review/2026-09-25-review.md` raised **F-033**: every metric artifact was
graded `EvidenceLevel.HISTORICAL` — Level C, "historical simulation" — whatever
produced its numbers. The grade was hardcoded in `metric_artifact`, the single
function every metric emitter routes through.

Constructed against `main` at `84eed17`, and reproduced by the independent pass:

```
validates:         True
evidence_level:    EvidenceLevel.HISTORICAL   <- Level C
signed:            7e437f18dba84f62
data_source:       I made these up
known_limitations: none
sample_period:     1990-01-01 -> 2026-01-01
```

Eight figures typed by hand, a `Disclosure` whose `data_source` says so, and a signed,
valid Level C artifact carrying a Sharpe ratio over a declared 36-year window.

**Why this is the grade that matters.** `constitution/Evidence_Standards.md:25`
defines Level C as historical simulation and `:33-35` defines Level D as "Hypothesis.
Research only." `:39` says the hierarchy may never be reversed, and the review
procedure's own checklist names the test:

```
$ sed -n '85,88p' .claude/skills/belay-review/references/red-team-checklist.md
**B5. Evidence level inflation.** `constitution/Evidence_Standards.md:39` — the
hierarchy may never be reversed. Look for anything labelled B (paper validated)
whose support is actually C (historical simulation), or C whose support is
really D. The label is a claim and needs a citation like any other.
```

"C whose support is really D" was in committed code. The grade is the one field on an
artifact that a promotion gate is entitled to trust without reading the content, and
it was the one field nothing verified.

**Two prior passes and what each got wrong.** `reports/review/2026-08-21-review.md:801-810`
examined the same line under checklist item B5 and declined to raise it, on the
reasoning that Level C is "correct for a computation over a supplied series" — a
sentence containing the unexamined premise that the series had been supplied by
something. The 2026-09-25 falsification pass then argued that `:39` was about
precedence between classes rather than grade assignment, and so that F-033's citation
was wrong; **the independent pass on that work refuted it from the checklist above,
and both objections were withdrawn** (`docs/sessions/2026-09-25-review-falsification.md`).
Recorded here because Law VIII makes a documented error an asset, and because the
error was made twice in the same direction: toward the comfortable reading.

**Nothing has been decided on such an artifact.** No strategy and no capital exist.
The cost arrives at Stage 3, when the backtester's first job is to emit exactly these
artifacts and `constitution/Capital_Authority.md:13-18` makes statistical edge one of
six inputs determining capital.

## Decision

**A computed number carries Level C only when its input series came from a stored
fetch record. Otherwise it carries Level D.** Ruled as Part 35a and, after the gap
below, again as **Part 36** — "yes require the stored fetch record".

`disclosure_from` takes a `Fetch`: the parsed series, the stored bytes, and the signed
record over them. It refuses unless

1. the record validates — signed and untampered;
2. its signed content carries every provenance key `fetch_record` writes, so a REPORT
   of another kind cannot pass as a fetch record;
3. the bytes the record names are on disk and hash to what it is signed over;
4. the vendor name, covered window and survivorship answer are read from that record.

Each failure **refuses**. A caller reaching the function is claiming a fetch, and
handing back Level D instead would flatter the caller while hiding a broken store.

**This document's first draft ruled the same sentence and built something weaker**, and
the history is kept because Law VIII makes it an asset: the first implementation took a
`MarketDataSource` and a `DailyBarSeries` and enforced only "came through
`disclosure_from`". A `DailyBarSeries` is a frozen dataclass any caller can build, so
eight bars typed into a Python file with a real source produced a Level C artifact
carrying that vendor's name and CC BY-SA attribution — the grade and the source string
agreeing, and both wrong. It was **worse than the F-033 it fixed**, whose artifact at
least read `data_source: I made these up`. An independent pass found it; the author did
not. The owner then ruled the stronger form rather than letting the ruling be softened
to fit the code.

The grade is read from the disclosure's provenance rather than stamped by the emitter:

1. `Disclosure` gains an `evidence_level` **property** returning
   `EvidenceLevel.RESEARCH`. Hand-built is the default and answers Level D.
2. `FetchedDisclosure(Disclosure)` overrides it with `EvidenceLevel.HISTORICAL`.
3. `framework.data.fetch_record.disclosure_from` — which takes a `MarketDataSource`
   and the series that actually arrived, so neither the source name nor the window
   can be typed at the call site — returns a `FetchedDisclosure`. It is the only
   thing in Belay that builds one.
4. `metric_artifact` reads `disclosure.evidence_level` instead of hardcoding a grade.

### Why a property and a subclass rather than a fifth field

This is forced, not stylistic. `tests/test_governance_conformance.py` asserts set
*equality* between `dataclasses.fields(Disclosure)` and the four things
`Validation/Backtesting.md` requires a backtest to document:

```python
fields = {field.name for field in dataclasses.fields(Disclosure)}
assert {name.lower().replace(" ", "_") for name in documented} == fields
```

That document is frozen by ADR-002. **A fifth field on `Disclosure` would turn the
constitution's own validation conformance red**, and the only ways round that are to
change a frozen document or to weaken the test — neither of which an agent may do.
Carrying the provenance on the type instead satisfies the test literally, and no new
field enters an artifact's `content`.

**Correcting a false claim an earlier draft made here.** It said "every artifact's
integrity hash is byte-identical to what it was before this change". That is wrong.
`content` is unchanged — verified, `a.content == b.content` — but the grade is
deliberately *inside* the integrity hash: `ArtifactIntegrity.canonical_payload` covers
`artifact.evidence_level` and each `evidence.hash`, and `EvidenceRecord.hash` covers
`level`. The comment beside those lines says why, and it was put there by ADR-005 on
purpose. The same artifact over a hand-built disclosure, built under each commit with a
fixed timestamp:

```
PRE  (cbc4d20)  f31a486f…  Level C
POST (0367c46)  b21db6ed…  Level D
```

**Consequence, which is the reason this correction matters:** any artifact built before
this change over a hand-built disclosure no longer reproduces its stored hash. Nothing
in the repository is affected today — `git ls-files artifacts/` holds one record and it
is a fetch record, not a metric — but a stored metric artifact would have been
invalidated silently, and the false sentence would have been the reason nobody looked.

This constraint was **not** surfaced when the recommendation was put to the owner. The
recommendation described "`Disclosure` gains a constructor split" without checking
what held `Disclosure`'s shape. The ruled substance is unaffected — grade from
provenance — but the owner agreed to a mechanism that could not have been built as
described, and that is recorded rather than quietly reshaped.

## Consequences

**Accepted, and the owner accepted it knowingly** (it was stated in the question):

- **Every metric artifact Belay emits today becomes Level D.** Nothing calls
  `disclosure_from`; it has no non-test caller, which is open finding **F-003**. Until
  the fetch path is wired through, no Level C artifact exists.
- **Under ADR-016's draft evidence floor that would block promotion above
  `Paper Trading`.** That is a real gate, not a formality. It is also arguably correct
  — evidence before capital — but ADR-016 is itself unratified, and whoever finishes
  it should read this consequence rather than discover it.
- `significance_artifact` takes a bare `data_source: str`
  (`framework/metrics/statistics.py`), builds a `Disclosure` from it, and so answers
  Level D. That is F-003 made visible in the grade rather than a new defect.

**Two tests changed, and both had encoded the defect.** The test formerly named
`test_the_evidence_is_graded_historical` — renamed by this change to
`test_a_hand_built_disclosure_is_graded_research`, so the old name is findable only in
git — asserted Level C on a fixture whose own `data_source` reads "unit test fixture,
supplied by hand". `tests/metrics/test_drawdown.py` did the same. Both now assert Level D
and say in their docstrings what they used to claim.

**`significance_artifact`'s Level D is asserted by nothing.** The consequence above is
true today and held by no test: `grep -n "EvidenceLevel\|\.level" tests/metrics/test_significance.py`
returns nothing. That is the shape of F-019 and F-032 and it is owed a test, which this
document should not be ratified without.

## The hole that is closed, and the one that remains

**Closed by Part 36.** The route described in this document's first draft — a real
`MarketDataSource` plus hand-typed bars — no longer exists: `disclosure_from` takes
neither argument. Verified against the implementation:

```
the old attack (source= + series=)        -> TypeError: unexpected keyword argument 'source'
a Fetch forged around a signed non-record -> ValueError: is not a fetch record
a genuine stored fetch                     -> FetchedDisclosure, EvidenceLevel.HISTORICAL
the stored bytes tampered after signing    -> ValueError: is not the one this record describes
the stored bytes deleted                   -> ValueError: no file at ...
the record tampered after signing          -> ValueError: integrity ... mismatch
```

**What remains, stated precisely.** A caller can construct a `FetchedDisclosure`
directly. That is narrower than what Part 36 closed, and different in kind: it is an
explicit claim, greppable by class name, rather than something that happens by using
the ordinary function. It is recorded here rather than fixed because closing it means
making the class private or binding it to a record too, and neither is worth the
coupling for a line that announces itself.

**One honest limit on the "stored" check.** It proves the bytes on disk match what the
record is signed over *at the moment the disclosure is built*. It does not prove the
bytes came from the vendor rather than being written by whoever also wrote the record —
that would need a signature from the source, which Belay has no way to obtain. What it
does close is every route that does not involve running `fetch_and_record` and keeping
its output intact.

## Alternatives rejected

- **Leave the grade and rely on the disclosure text.** Rejected: the grade is what a
  gate reads without opening the content. That is the whole defect.
- **Add a fifth `Disclosure` field.** Rejected — it breaks the constitution's
  validation conformance, as above.
- **Take an explicit `evidence_level` parameter on `metric_artifact`.** Rejected: it
  moves the unverified claim to the caller, which is where it already was.
- **A module-level registry of fetched disclosures.** Rejected: hidden mutable state,
  against `AGENTS.md`'s determinism rules and its "no hidden shared state" architecture
  rule.

## Verification

**Discharged by the independent pass of 2026-09-25 16:35 UTC** (on #36), which ran what
this section previously listed as owed:

- **The mutation.** `disclosure_from` returning a plain `Disclosure` turns the suite red
  with **exactly one** extra failure,
  `test_a_derived_disclosure_grades_the_metric_historical_and_a_hand_built_one_does_not`.
  The guard is asserted, not assumed.
- **Vacuity.** Reverting `metric_artifact` to `level=EvidenceLevel.HISTORICAL` fails both
  changed tests. Neither passes vacuously.
- **The conformance claim.** A real fifth field (`from_fetch: bool = False`) added to
  `Disclosure` does fail
  `test_the_disclosure_block_names_everything_a_backtest_must_document`. The
  property/subclass design is forced, as claimed.
- **Round-trip and copies.** `ArtifactSerializer.dump`/`load`, `dataclasses.replace`,
  `pickle` and `deepcopy` all preserve the grade; the subclass loses no inherited
  validation.
- **The suite.** 710 passed, 1 skipped, 5 xfailed at `9d91870`.

**Part 36's five guards are each asserted by their own test.** Every guard in
`disclosure_from` mutated one at a time against the committed tree: **each turns the
suite red on exactly one test, and it is that guard's test.** 715 passed at baseline.

```
MUTANT record validation removed      -> FAILED test_a_disclosure_is_refused_when_the_record_was_tampered_with
MUTANT returns a plain Disclosure     -> FAILED test_a_derived_disclosure_grades_the_metric_historical_and_a_hand_built_one_does_not
MUTANT provenance shape check removed -> FAILED test_a_disclosure_cannot_be_derived_from_a_record_that_is_not_a_fetch_record
MUTANT bytes-missing check removed    -> FAILED test_a_disclosure_is_refused_when_the_stored_bytes_are_gone
MUTANT bytes-changed check removed    -> FAILED test_a_disclosure_is_refused_when_the_stored_bytes_changed_under_the_record
                                         (1 failed, 714 passed, 1 skipped, 5 xfailed — each)
```

**One of those tests exists only because the mutation found it missing.** The record
validation guard originally survived its own removal at 714 passing — a guard asserted by
nothing, in code written by the session whose whole subject was guards asserted by
nothing. It was caught by mutating the new code rather than by reading it, which is the
argument for doing that on every guard rather than trusting a green suite.

**Still owed before ratification:**

- **A test for `significance_artifact`'s Level D**, which nothing asserts.
- **An independent pass over this revision.** Part 36's implementation and this
  document's rewrite have had none.
