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

`disclosure_from` trusts nothing the caller hands in but the record's identifier:

1. the record is **re-read from the repository** (`repository.get`, which verifies
   integrity on read). A record that exists only in the caller's hands is refused;
2. its signed content must carry every provenance key `fetch_record` writes;
3. the bytes are resolved from **`store.root` and the record's own signed
   `store_path`** — never the caller's `fetch.stored.path` — and must exist and hash
   to what the record is signed over;
4. the series must be the record's own, by observation count and by covered window;
5. the vendor name, window and survivorship answer are read off that stored record.

Each failure **refuses**. A caller reaching the function is claiming a fetch, and
handing back Level D instead would flatter the caller while hiding a broken store.
**Refusal is this session's choice, not the owner's** — the ruling settled what
Level C requires, not what happens when it is not met.

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

## What is closed, what is not, and the ceiling

**Two implementations were broken here before this one.** Both by independent
passes, both in the flattering direction:

| attempt | what it enforced | how it fell |
|---|---|---|
| 1 | came through `disclosure_from` | `DailyBarSeries` is caller-buildable: eight typed bars + a real source → Level C with that vendor's name |
| 2 | the caller's record validates | `Fetch` is caller-buildable and `ArtifactIntegrity.sign` is **public and unkeyed** → Level C claiming a licensed vendor, 25 years, no survivorship bias, with `MarketDataSource` never instantiated |

**Verified against this implementation:**

```
a hand-built Fetch never saved to the repository -> ValueError: in the repository at ...
a stored REPORT with no provenance keys          -> ValueError: is not a fetch record
a genuine record re-signed with a new vendor     -> ignored; the STORED name is used
the caller's stored.path repointed at a decoy    -> ignored; resolved from store_path
the record's own bytes deleted                   -> ValueError: no file at ...
the record's own bytes rewritten                 -> ValueError: not the one the record describes
the series swapped (count, and window)           -> ValueError, both ways
a GENUINE stored fetch                           -> FetchedDisclosure, HISTORICAL
```

**The ceiling, and it is the honest part.** The integrity hash is unkeyed and
`sign` is public, so **nothing here can prove a record came from `fetch_record`**.
What this raises is the cost: faking provenance now means writing a permanent,
discoverable record into the repository rather than constructing an object in
memory. That is a real cost that leaves evidence, and it is the best available
without keyed signing.

Keyed signing was sized and **rejected for this purpose**: it collides with
`AGENTS.md`'s "the same inputs must give the same outputs, on any machine", needs an
amendment to ADR-005 (Accepted and Implemented), touches 26 test files — and
decisively, **it would not stop the adversary here.** Every forgery above was
written by a caller in this process, which can reach a key as easily as the code
can. It defends against an outsider, which is a different threat.

**Limits that remain, and there is more than one** — an earlier draft called one of
these "the one honest limit":

- Authenticity, as above.
- A caller can construct a `FetchedDisclosure` directly, or subclass `Disclosure`
  and override `evidence_level`. The earlier draft excused the first as "greppable
  by class name"; the subclass route is not, so that mitigation is weaker than
  claimed.
- The byte check is at build time. It says nothing about the file a minute later.

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

**Every guard mutated one at a time, against a committed tree.** Baseline 719
passed, 1 skipped, 5 xfailed. Eight guards, and each turns the suite red:

```
repository re-read -> caller's record   FAILED …needs_a_record_that_is_actually_in_the_repository
                                        FAILED …tampered_record_handed_in_by_the_caller_is_ignored
provenance shape check removed          FAILED …stored_record_that_is_not_a_fetch_record_is_refused
bytes from the caller's path            FAILED …bytes_are_resolved_from_the_records_own_signed_path
bytes-missing check removed             FAILED …stored_bytes_are_gone
bytes-changed check removed             FAILED …stored_bytes_changed_under_the_record
series count check removed              FAILED …records_window_but_extra_bars_is_refused_by_count
series window check removed             FAILED …right_length_but_the_wrong_window_is_refused
returns a plain Disclosure              FAILED …grades_the_metric_historical_and_a_hand_built_one_does_not
```

Seven fail exactly one test. **The repository re-read fails two, and that is
correct rather than sloppy:** it is the guard that both refuses the forgery and
makes the caller's record irrelevant, so two distinct claims rest on it. Contorting
the tests to make it one would hide that.

**Two of those tests were vacuous when first written, and the mutation is what
caught them.** The path-resolution test wrote the *same* bytes to its decoy, so it
passed whichever path was read; the count test used bars outside the record's
window, so the window check caught it first. Both survived their own mutation at 719
passing. They are rewritten — the decoy now holds different bytes, and the count
test adds a bar *inside* the window using a fixture whose bars are eight days apart,
because the ordinary fixture's adjacent days leave no date to insert.

**Reverting the production code with the tests left in place** fails every touched
test, so none passes vacuously now.

**Still owed before ratification:**

- **A test for `significance_artifact`'s Level D**, which nothing asserts.
- **An independent pass over this revision.** Three have run; each broke the
  implementation it was given. This one has had none.
