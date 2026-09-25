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

**Ruled (Part 35a): a computed number carries Level C only when its input series came
from a recorded fetch. Otherwise it carries Level D.**

**Built, and it is weaker: a computed number carries Level C only when its disclosure
came through `disclosure_from`.** The gap is stated here rather than in a footnote
because an earlier draft of this document asserted the ruled sentence as the built
behaviour, and it is not. See "The hole this does not close" below. The independent pass
on this change found it; its author did not.

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

## The hole this does not close, and it is larger than first admitted

**`disclosure_from` proves nothing about a fetch.** It takes a `DailyBarSeries` — a
frozen dataclass any caller can construct — and never touches a `FetchedSeries`, a
payload, a `content_hash`, a stored version or a fetch record. Reproduced against the
committed code, using Belay's own `DoltHubStocksSource`, no subclass and no network:

```
disclosure type:  FetchedDisclosure
evidence_level:   EvidenceLevel.HISTORICAL   <- Level C
data_source:      DoltHub post-no-preference/stocks (CC BY-SA 4.0)
sample_period:    2024-01-02 -> 2024-01-09
validates:        True
```

Eight bars typed into a Python file. **This is worse than F-033 in one respect:** the
construction that raised F-033 printed `data_source: I made these up`, so the artifact
disclosed its own worthlessness. This one carries a real vendor's name and licence
attribution, so the grade and the source string agree and both are wrong.

It is the same substitution the `source` parameter was explicitly designed to prevent —
`fetch_record`'s docstring says "taking the name rather than the source let a fabricated
disclosure be paired with a real source's identity" — arriving through the unguarded
`series` door.

**An earlier draft's defence of this does not survive.** It admitted only that a caller
could hand-construct a `FetchedDisclosure`, and argued the dishonest path was therefore
"an explicit, greppable claim". The route above never names `FetchedDisclosure` at all.

**What is genuinely bounded.** A hand-built `Disclosure` cannot reach Level C; the grade
survives serialisation, `dataclasses.replace`, pickle and deepcopy; and the mutation
below is asserted by a test. The default is unflattering and every existing caller gets
Level D. What is not bounded is a caller who calls the sanctioned function with invented
bars.

**Closing it, which is an owner question and is open.** Bind the grade to a stored fetch
record's `content_hash`, so Level C cannot be claimed without the bytes that earn it.
That decides what a metric artifact must carry and touches ADR-014's persistence rules,
so it is not an agent's to choose. It is put to the owner in
`docs/OperatorChecklist.md` (2026-09-25, "Level C does not yet mean what Part 35a
rules"). **Until it is answered, this ADR must not be ratified as written**, because
Part 35a rules the stronger thing and this document would otherwise certify a weaker one
as delivering it.

**It does not change `constitution/Evidence_Standards.md`.** The four classes are
untouched. One wrinkle the owner was shown and which is still open: Level D is defined
as "Hypothesis. Research only.", and arithmetic over unsourced numbers is not really a
hypothesis either. Neither class fits it exactly. If the constitution is ever amended
here, the phrasing wanted is closer to "Level D is the floor for a computation whose
inputs have no recorded provenance". **That amendment is the owner's and is not
proposed by this ADR.**

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

**Still owed before ratification:**

- **The owner's answer on the hole above.** Part 35a rules more than this delivers.
- **A test for `significance_artifact`'s Level D**, which nothing asserts.
- An independent pass over *this* revision, since the corrections above were written
  after the pass that found them.
