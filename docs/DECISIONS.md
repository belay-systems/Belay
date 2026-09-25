# Belay Architectural Decisions

## ADR-001: Artifact Framework Modernization

Status:
Accepted

Date:
2026-07-08

---

## Context

Belay requires a durable evidence-driven communication layer between autonomous components.

The existing Artifact Framework represented the correct architectural boundary but lacked:

- immutable data structures
- lifecycle governance
- evidence provenance
- integrity guarantees

---

## Decision

The existing Artifact Framework will be upgraded rather than replaced.

Artifacts become immutable evidence objects representing validated state transitions.

---

## Consequences

Positive:

- single source of truth for system artifacts
- deterministic artifact evolution
- stronger auditability
- improved reproducibility
- clearer promotion pipeline

Negative:

- existing consumers require migration
- serialization contracts must evolve
- validation becomes more complex

---

## Rejected Alternative

Creating a parallel Artifact system.

Reason:

A second artifact representation would introduce duplicate system truth and increase architectural drift.

---

## Required Follow-Up

- lifecycle validation
- evidence validation
- integrity verification
- complete migration testing

---

## ADR-002: Two-Layer Architecture — Governance and Mechanics

Status:
Accepted

Date:
2026-07-26

---

## Context

Belay is currently described in two different vocabularies.

The first describes an organization: departments, a constitution, a librarian,
an investment intelligence operating system. This vocabulary governs authority —
who may decide, what evidence is required, which gates exist.

The second describes a pipeline: market data, feature store, indicator engine,
signal engine, risk engine, execution engine. This vocabulary governs mechanics —
how an observation becomes a number, and a number becomes an order.

These have been treated as competing descriptions of the same system. They are not.
A fund has both an investment committee and a trading desk. Neither vocabulary is
wrong, and neither replaces the other.

The measurable problem is asymmetry, not ambiguity. As of this date the repository
contains 79 markdown documents and 593 lines of Python, of which 101 lines are tests
and 231 lines are the Artifact Framework. The ten files under `framework/services/`
average four lines each and are empty placeholders.

`constitution/Paper_First_Capital_Doctrine.md` defines eight lifecycle stages.
`strategies/PromotionCriteria.md` defines the thresholds those gates apply.

> **Amended 2026-07-30 by ADR-007.** This sentence read
> "`constitution/Promotion_Pipeline.md` defines eight promotion gates." That
> citation was false: `Promotion_Pipeline.md` contains no group of eight — it
> has seven maturity levels and seven promotion considerations. The groups of
> eight are in `Paper_First_Capital_Doctrine.md` (lifecycle stages) and
> `strategies/PromotionCriteria.md` (evaluation categories). The original text
> is preserved in this note rather than discarded: Immutable Law VII, and the
> error is itself part of the record.
Nothing in the repository computes a single number that any of those gates could
evaluate. The governance layer is fully specified and has nothing to govern.

This is a structural risk rather than a stylistic one. Governance documents are
inexpensive to produce and require no verification to feel complete. A system whose
first principle is evidence over opinion currently has a repository shaped almost
entirely like opinion.

---

## Decision

Belay is defined as two layers joined by a single contract.

The Governance Layer specifies what evidence is required and who may promote.
It comprises `constitution/`, `departments/`, `workflows/`, `Knowledge/`, and the
markdown under `strategies/`. It remains prose. It is frozen: no new governance
documents are added until the mechanics layer can produce evidence for the gates
already written.

The Mechanics Layer produces that evidence. It comprises `framework/`. All new
code belongs here.

The Artifact is the contract between them. Mechanics emit Artifacts. Governance
consumes Artifacts. Neither layer reaches across the boundary by any other means.

Both vocabularies are retained as accurate descriptions of their own layer. The
difference between them is no longer treated as unresolved.

---

## Consequences

Positive:

- every directory has an unambiguous layer and owner
- "which vision is correct" ceases to be an open question
- the Artifact Framework's existing role is confirmed rather than redefined
- new work has an explicit default location
- the governance freeze converts documentation effort into evidence-producing work

Negative:

- the freeze blocks governance writing that currently feels productive
- some existing directories span both layers and must be sorted
- `workflows/` (prose) and `framework/workflows/` (code) remain confusingly named
- the asymmetry becomes visible in every future review until mechanics catch up

---

## Rejected Alternatives

Rewriting the governance documents into service-pipeline language.

Reason:

The governance layer is the most complete and considered work in the repository.
Rewriting it would destroy finished work to resolve a conflict that does not exist,
and would leave the actual gap — absent mechanics — untouched.

Continuing to expand governance documentation before mechanics exist.

Reason:

Additional gates cannot be validated against evidence that nothing produces. This
compounds the existing asymmetry and defers the first real test of the Artifact
Framework's design.

---

## Required Follow-Up (ADR-002)

- build the smallest component that emits one Artifact containing one honestly
  computed number, establishing the mechanics layer and testing the Artifact
  contract against a real payload
- assign each remaining top-level directory to exactly one layer
- resolve the `workflows/` and `framework/workflows/` naming overlap
- record in `docs/Architecture.md` that the four departments are the governance
  layer, not the whole system

---

## ADR-003: One Lifecycle Or Two

Status:
**Accepted.** Option A implemented 2026-07-26.

Date:
2026-07-26

---

## Context

Belay describes two different lifecycles, and the code implements one of them under
the other's name.

`Knowledge/ArtifactLifecycle.md` defines the lifecycle of an artifact:

    Draft → Review → Approved → Active → Archived → Historical

`constitution/Paper_First_Capital_Doctrine.md` defines the lifecycle of a strategy
earning capital:

    Idea → Research → Validation → Paper Trading → Promotion Review →
    Micro Capital → Limited Capital → Production

The `ArtifactLifecycle` enum in `framework/artifacts/enums.py` carries the name of
the first and the contents of the second. Only `Draft` appears in both.

A third appeared on completing the document audit. `docs/ENGINEERING_AGENT.md`
defines a lifecycle for code changes:

    Draft → Research → Validation → Testing → Review → Merged → Production

These describe different subjects. An artifact is a document or a unit of evidence;
it is drafted, reviewed, approved, and eventually archived without ever holding
capital. A strategy is a candidate for allocation; it earns its way through paper
trading into progressively larger exposure. An engineering change is neither; it is
tested and merged.

The question is therefore not "one lifecycle or two" but how many kinds of thing
Belay governs. At least three, and each already has a sequence written for it.

The consequence is visible in the only real producer. `framework/metrics/drawdown.py`
emits a REPORT artifact containing a computed drawdown figure. Its lifecycle field
is `DRAFT`, and the only legal transition from there leads eventually to
`MICRO_CAPITAL` and `PRODUCTION` — capital states, applied to a report about a
number. A drawdown report will never hold capital. It should be reviewed, approved,
and archived.

Nothing breaks today, because only the tests and `drawdown.py` touch the field. The
cost is paid later: every component built before this is settled inherits the
conflation, and each one makes the correction more expensive.

---

## Options

**A. One enum per governed subject.** Rename the existing enum to `StrategyLifecycle`,
matching what it already implements. Add `ArtifactLifecycle` matching
`Knowledge/ArtifactLifecycle.md`, and later `EngineeringChangeLifecycle` matching
`docs/ENGINEERING_AGENT.md` when that layer is built. Artifacts carry the artifact
lifecycle; strategy artifacts additionally carry a strategy stage.

Cost: touches the enum, the validator's transition table, `drawdown.py`, and every
lifecycle test. One transition table per subject.

Benefit: each artifact carries only states that can be true of it. An illegal
question — "is this drawdown report in micro capital?" — stops being representable.
The pattern extends to the engineering layer instead of colliding with it.

**B. One enum, renamed.** Keep a single lifecycle, rename it `StrategyLifecycle`,
and accept that non-strategy artifacts sit permanently in `DRAFT`.

Cost: `Knowledge/ArtifactLifecycle.md` becomes documentation of something the system
does not implement. Reports have no meaningful review or archival state.

Benefit: smallest change; one table.

**C. Artifact lifecycle as metadata.** Keep the enum as the strategy lifecycle and
express document status through the existing `metadata` field.

Cost: unvalidated. `metadata` is an untyped tuple of pairs, so nothing constrains
the values or the transitions between them.

Benefit: no structural change.

---

## Recommendation

Option A, on the grounds that the promotion gates in `constitution/` govern
strategies and the review states in `Knowledge/` govern evidence, and Belay needs
both. Option C is rejected on the same grounds as the pre-existing integrity
findings: a governed concept expressed as unvalidated metadata is not governed.

This is a recommendation, not a decision. The naming affects how every future
component labels its output, which makes it worth deciding deliberately rather
than defaulting into.

---

## Consequences Of Acceptance

Implemented as described. `ArtifactLifecycle` now holds the six editorial states
from `Knowledge/ArtifactLifecycle.md`; `StrategyLifecycle` holds the eight capital
stages, with `IDEA` replacing `DRAFT` to match all three documents that name it.
`Artifact` gained an optional `strategy_stage`.

`ArtifactValidator` carries two transition tables and refuses to move between
lifecycles rather than coercing, so a report can no longer be pointed at a capital
stage. `MICRO_CAPITAL` remains where it was added; the split confirmed it sits on
the strategy sequence, which is where the doctrine puts it.

Two rules followed from the split and are enforced:

- `strategies/Registry.md` states "Every strategy exists in exactly one lifecycle
  stage", so a STRATEGY artifact without a `strategy_stage` is rejected.
- The converse is also rejected. A report claiming a capital stage asserts something
  untrue of it.

`EngineeringChangeLifecycle` is not implemented. It should follow the same pattern
when `docs/ENGINEERING_AGENT.md` is built, rather than reusing either existing enum.

Conformance is held by `tests/test_governance_conformance.py` and
`tests/artifacts/test_lifecycle.py`: if either enum drifts from the document that
defines it, the suite goes red.

---

## ADR-004: Demotion — Depth, Floor, Authority And Evidence

Status:
**Accepted.** Rule 4 amended and ratified 2026-07-28. Rules 1 through 3
implemented 2026-07-28: both tests rewritten first, then the ten transitions
added. Rule 4 is unimplementable until review decisions are recorded somewhere,
and the classification helper is deliberately still deferred — see the note at
the end of Required Follow-Up.

Date:
2026-07-27

---

## Context

Five documents require a strategy to be able to move backward. Three treat
`Demote` as a formal decision outcome, listed beside `Promote`, `Remain` and
`Retire`:

- `constitution/Paper_First_Capital_Doctrine.md` — "Demotion may occur at any stage"
- `strategies/Lifecycle.md` — "Strategies may move backward"
- `strategies/ReviewTemplate.md` — Recommendation: Promote / Remain / **Demote** / Retire
- `Validation/CapitalReview.md` — Outcomes include **Demote**
- `workflows/Monthly/StrategyPromotion.md` — Decisions include **Demote**

Every transition in `STRATEGY_TRANSITIONS` moves forward. Three review processes
therefore produce a decision the system cannot record, and a strategy degrading at
limited capital can only be left alone or retired outright — the choice demotion
exists to avoid.

The blockage was never code. How far a strategy may fall in one step, on whose
authority, and requiring what evidence is written nowhere in the repository.

---

## The Doctrine Does Not Pre-Decide This

The doctrine states two rules in identical form:

    Demotion may occur at any stage.
    Retirement may occur at any stage.

Retirement has exactly one destination. Read consistently, "may occur at any
stage" therefore constrains the stage a strategy may fall **from**, not the stage
it may fall **to**. This is an interpretation, but it is the only one under which
the two sentences mean the same thing, and it leaves the depth question open
rather than silently answered.

---

## Decision

**1. Depth — any distance downward.** A demotion names one destination and moves
there in a single act. Promotion steps one stage at a time because each stage
proves something and a skipped proof cannot be claimed. Falling proves nothing, so
the constraint does not bind downward. Governance is asymmetric by design: a rung
is hard to climb and easy to lose. This is what "Capital is a privilege. Never an
entitlement" asserts.

**2. Floor — `PAPER_TRADING`.** A demoted strategy may lose every unit of capital
and be sent back to rebuild its live-behaviour record. It may not be sent below
that. `VALIDATION`, `RESEARCH` and `IDEA` are stages of construction rather than
operation; a strategy whose statistical proof is falsified has not been demoted, it
has been refuted, and refutation is retirement with history preserved.

**3. Authority — a review outcome, never automatic.** A demotion is recorded when
one of the three review processes above produces a Demote decision. No threshold
breach, drawdown trigger or risk signal demotes a strategy on its own.
`Governance.md` places authority in process rather than hierarchy, and demotion
changes what a strategy has *earned* — a deliberative judgment, not a reflex.

**4. Evidence — written justification, no numeric gate.** `ReviewTemplate.md`
requires "Justification. Evidence only." `Governance.md` requires that all
decisions be documented. Requiring a promotion-grade score to *withdraw* a
privilege would invert the doctrine: it would make capital something Belay must
prove a strategy no longer deserves.

Rule 4 originally read "a demotion satisfies both and needs nothing further".
That sufficiency claim was withdrawn and replaced on 2026-07-28, having been
asserted without checking `constitution/Capital_Authority.md`, which states that
capital "shall be determined using" six named inputs — confidence, statistical
edge, regime compatibility, portfolio exposure, correlation, drawdown limits — and
which outranks this ADR under Immutable Law X.

**Stage and allocation are different decisions, and a demotion is the first of
two.** `Capital_Authority.md` is titled Capital *Allocation* Authority and states
"Allocation does not imply maximum allocation". A strategy's stage is the
*ceiling* it has earned; its allocation is the sum it actually holds, at or below
that ceiling. Demotion lowers the ceiling. The six inputs size the position
underneath whichever ceiling applies.

They therefore run in sequence rather than competing:

1. **The demotion.** Governed by rule 4. Written justification citing evidence, no
   score, no threshold. This is a judgment about what the strategy has earned.
2. **The re-sizing.** Governed by `Capital_Authority.md`. A demotion triggers a
   fresh allocation determination using the six inputs, sizing the strategy inside
   its new lower ceiling.

**The six inputs may never gate the demotion itself.** `Capital_Authority.md` also
states "Capital preservation overrides return maximization. Whenever conflict
exists: Capital preservation wins. Always." A demotion is a capital-preservation
act, so a reading under which an unavailable input delays one is forbidden by the
same document that names the inputs. If step 2 cannot be completed, step 1 still
stands and the strategy sits at its new stage.

Step 2 has no implementation. There is no position-sizing or portfolio layer, and
four of the six inputs do not exist as computed values — `strategies/PositionSizing.md`
and `Research/RegimeDetection.md` are both carried in the `docs/ROADMAP.md`
inventory of specified-but-unbuilt work. Until that exists, step 2 is performed by
the reviewer in prose. This does not block rules 1 through 3.

---

## Resulting Transitions

Ten moves become legal. Every one is a demotion; no forward transition changes.

| From | May be demoted to |
|---|---|
| `PRODUCTION` | `LIMITED_CAPITAL`, `MICRO_CAPITAL`, `PROMOTION_REVIEW`, `PAPER_TRADING` |
| `LIMITED_CAPITAL` | `MICRO_CAPITAL`, `PROMOTION_REVIEW`, `PAPER_TRADING` |
| `MICRO_CAPITAL` | `PROMOTION_REVIEW`, `PAPER_TRADING` |
| `PROMOTION_REVIEW` | `PAPER_TRADING` |

The two zero-capital destinations are not interchangeable. `PROMOTION_REVIEW`
means the capital is withdrawn but the strategy remains a candidate, to be
re-decided at the next review. `PAPER_TRADING` means it is no longer a candidate
and must build a fresh record before it is one again.

A demoted strategy re-earns every stage through the normal gates. This follows
from the forward transitions being left untouched; no fast lane exists.

---

## Consequences

**Demotion exists only at or above `PROMOTION_REVIEW`.** Below the floor there is
no capital privilege to withdraw, so the four lower stages have no demotion
transitions at all. This narrows the literal text of "Demotion may occur at any
stage" and the narrowing is deliberate. It is also the safe direction to be wrong
in: lowering the floor later only adds transitions and invalidates no recorded
history, whereas raising it would orphan strategies already sitting below it.

**Two passing tests must change, and they must change *before* the table does.**
Both use "everything except `RETIRED`" as a proxy for "forward", and that proxy
stops being true the moment backward moves share the table.

`test_no_strategy_stage_may_be_skipped` (`tests/test_governance_conformance.py`)
filters `RETIRED` out of each tuple and asserts the remainder is exactly the next
stage. It fails loudly on a correct table — the easy case. Note that its loop is
bounded to `ordered[:-2]`, so it never examines `PRODUCTION` or `RETIRED`: the
stage gaining the most new transitions is precisely the one this test does not
check.

**`RETIRED` is the highest ordinal in `StrategyLifecycle`, and that is a trap.**
The enum declares it last, at index 8, above `PRODUCTION` at 7. "Compare stage
ordering directly" must therefore NOT be implemented as a bare position
comparison over `list(StrategyLifecycle)` — under one, every retirement reads as
the deepest promotion in the system. Retirement is not on the ladder at all; the
doctrine places it outside the sequence. Any ordering helper must exclude
`RETIRED` from the ladder first and classify it separately, before comparing
positions. This applies to both rewritten tests and to the classifier below.

`test_promotion_path_walks_every_stage_in_order` (`tests/artifacts/test_lifecycle.py`)
is the dangerous one. It walks the table from `IDEA` in a `while True` loop whose
only exit is a stage having no non-`RETIRED` successor. Today `PRODUCTION` maps to
`(RETIRED,)` alone, so the filter empties it and the walk terminates. Once
`PRODUCTION` gains four demotion targets, every reachable stage keeps a
non-`RETIRED` successor, and `RETIRED` — the only row with an empty tuple — is
filtered out before it can ever be appended. The loop never exits and its
accumulator grows without bound. No ordering of the new entries avoids this.

Nothing bounds it: there is no `conftest.py`, and `pytest-timeout` is not a
dependency. `pytest` produces no output and does not return. Anyone who changes
the table first will see a hang with no failing test to explain it, which is a far
worse signal than a red suite.

**Legality and justification are separate concerns.** A transition table can rule
that a move is possible; it cannot know whether a justification was written. Rule 4
therefore has no home in `ArtifactValidator` and must be enforced wherever review
decisions are recorded, which does not exist yet.

**Belay has no halt mechanism, and rule 3 makes that visible.** A strategy
breaching a hard risk limit needs to stop trading in seconds. Demotion runs at the
speed of a monthly review. Keeping the two on separate axes is correct — what a
strategy has earned is not the same question as whether it is trading right now —
but it means the fast path is unbuilt rather than merely slow. Recorded as a new
finding in `docs/HANDOFF.md`.

---

## Rejected Alternatives

**One rung at a time, symmetric with promotion.** Rejected because the symmetry is
superficial. A degrading `PRODUCTION` strategy would need three consecutive monthly
reviews to reach zero capital, and the exposure during those three months is
precisely the harm demotion exists to prevent.

**Automatic demotion on a hard risk breach.** Rejected because it conflates the
emergency brake with the maturity ladder, which would leave the brake running at
committee speed. The correct fix is a halt mechanism on its own axis.

**Threshold-gated demotion, requiring a named metric to cross a named line.**
Rejected on two grounds. It inverts the burden of proof described above, and the
thresholds are set by the Investment Committee against data Belay does not yet
have — so adopting it would have re-blocked this finding behind a second decision
that cannot be made until the metrics layer exists.

---

## Required Follow-Up

Order matters. Both tests must be rewritten before the table changes, or the suite
hangs instead of failing.

- Rewrite `test_no_strategy_stage_may_be_skipped` to compare stage ordering rather
  than filtering `RETIRED`
- Rewrite `test_promotion_path_walks_every_stage_in_order` to take the single
  forward successor by enum ordering rather than `onward[0]`, and bound the walk
  by the number of stages. Its name and docstring also stop being true: it is no
  longer following "the only available move", it is following the forward one
- Only then add the ten transitions to `STRATEGY_TRANSITIONS` in
  `framework/artifacts/validator.py`
- Remove the `xfail` from `test_a_strategy_can_be_demoted` and extend it to cover
  the floor: `PAPER_TRADING` has no demotion target, and no demotion reaches
  `VALIDATION` or below
- Extend the demotion test to pin the table to exactly the ten tabulated
  transitions, so a later extra or missing demotion is caught rather than assumed
- Update the comment above `STRATEGY_TRANSITIONS` in
  `framework/artifacts/validator.py`. It currently reads "One stage at a time",
  which the new table contradicts
- Add a helper that classifies a legal transition as promotion, demotion or
  retirement, so the review layer has something to attach a justification to.
  Specify it before writing it: `RETIRED` must be classified before any ordinal
  comparison (see the trap above), and the three names do not cover everything the
  helper will be handed — artifact-lifecycle transitions, and self-transitions,
  which are the documented "Remain" outcome and are currently rejected by
  `validate_transition`. Defer the helper rather than guess its contract
- On completion, update `docs/HANDOFF.md`: close finding 1, correct the open-finding
  count, and correct the "Highest Priority Next Task" entry

---

## Implementation Record (ADR-004)

Done 2026-07-28, in the order above.

Both tests were rewritten first and run against the *unchanged* table to confirm
they fail rather than hang: two failures in 0.18s, no timeout needed. The table
was changed only after that. Suite: 115 passed / 8 xfail → 118 passed / 7 xfail.

`test_no_strategy_stage_may_be_skipped` now compares ladder positions and keeps
only the moves that climb, and its loop covers `PRODUCTION`.
`test_promotion_path_walks_every_stage_in_order` was renamed
`test_forward_path_walks_every_stage_in_order`, selects the forward successor by
ladder position, and is bounded by the stage count. Both files derive the ladder
as `[s for s in StrategyLifecycle if s is not RETIRED]` and carry the trap
warning at the definition, so no ordinal comparison ever sees `RETIRED`.

The ten transitions are pinned as a set by
`test_the_demotion_table_is_exactly_what_adr_004_tabulates`, and the floor by
`test_demotion_goes_no_lower_than_paper_trading`, which asserts the
`PAPER_TRADING` row directly as well as by rule — a rule quantified over an
empty set of demotions would otherwise pass against a table with none.

**Still deferred, deliberately: the promotion/demotion/retirement classifier.**
Its contract is still unsettled for exactly the reasons the follow-up gives —
artifact-lifecycle transitions and self-transitions are outside the three names,
and "Remain" remains an open finding. Nothing in `framework/` performs an ordinal
comparison over `StrategyLifecycle` today, so the `RETIRED` trap is currently
confined to the two test modules that guard against it. It becomes live the
moment this helper is written.

**Rule 4 is not enforced anywhere and cannot yet be.** Neither the written
justification nor the re-sizing step that follows a demotion has a home: there is
no layer that records review decisions. The transition table rules legality only,
and the comment above it says so.

---

## ADR-005: Artifact-Level Confidence, And The Absent Schema Fields

Status:
**Accepted.** Ratified 2026-07-30. Rule 5 amended the same day: `Evidence Level`
was originally left undecided, and is now ruled — see the amendment under
Decision. Implemented 2026-07-30.

Date:
2026-07-30

---

## Context

`Knowledge/Schema.md` lists **thirteen** required fields at lines 7-31, with
`Optional Fields` beginning at line 35. The figure of fourteen carried in
`docs/HANDOFF.md` was wrong and had propagated into a test docstring; it was
counted by hand on 2026-07-30 and corrected.

`Artifact` covers nine of the thirteen outright. Three are absent: **Tags**,
**Summary**, **Current Confidence**. A fourth, **Evidence Level**, is not clearly
either — the schema asks for an artifact-level grade and `Artifact` carries
`evidence`, a tuple of `EvidenceRecord`, which is a different thing.

Four documents require an adjustable artifact-level confidence:

- `Knowledge/Schema.md:31` — `Current Confidence`, a required field
- `strategies/Registry.md:23,25` — `Current Confidence`, worked example `38%`
- `strategies/ReviewTemplate.md:37-43` — `Confidence Adjustment`: Increase,
  Decrease, No Change
- `Knowledge/Search.md:19` — `Confidence` is a primary search filter

`Knowledge/Search.md:3` states "Belay retrieves information through metadata",
and `Search.md:37` states "Search always prefers summaries before opening full
artifacts" — so Summary is not decoration, it is what search reads first.

Confidence exists today only on `EvidenceRecord`, which is frozen: fixed at
creation, never revisable. `strategies/RegimeCompatibility.md:17` requires that
"Belay continuously updates compatibility confidence using observed evidence",
which is impossible as things stand.

The open question was whether a revision produces a new version or alters an
existing one. `Knowledge/Versioning.md` answers it: revisions are corrections,
corrections are a Patch (line 15), "Knowledge records every version" (line 23),
and "No version is overwritten" (line 25).

---

## Decision

**1. Add `tags`, `summary` and `confidence` to `Artifact`.** The schema requires
them and `Knowledge/Search.md` queries them. `tags: tuple[str, ...]`,
`summary: str`, `confidence: float | None`.

**2. `Artifact` remains frozen. A confidence revision produces a new version.**
Adjusting confidence means constructing the next version of the artifact with the
new figure and saving it alongside the old. This is what `Versioning.md` requires,
and it is now workable rather than theoretical: `ArtifactRepository.latest()` was
added on 2026-07-30 and orders versions semantically, so "the current confidence"
is a question with a correct answer.

An in-place mutable field is rejected. It would destroy the prior figure, and the
revision history of a confidence estimate *is* the evidence trail — a strategy
whose confidence fell from 0.6 to 0.3 over four reviews is a different object from
one that has always been 0.3.

**3. Confidence is stored as a fraction in 0-1, and rendered as a percentage.**
`EvidenceRecord.confidence` is already bounded to 0-1, and two representations of
one quantity would eventually disagree. `Registry.md`'s `38%` is presentation.

**4. Confidence is optional (`None`) rather than defaulted.** A default of 0.5
would be a fabricated estimate that nothing distinguishes from a real one — the
silent-fallback failure this repository has already been bitten by twice. `None`
means "not yet assessed" and says so.

**5. `Evidence Level` is a stored field, derived as the strongest grade present,
and never set by hand.** *(Amended 2026-07-30. This rule originally declined to
decide, pending a derivation rule. The derivation is below.)*

`constitution/Evidence_Standards.md` defines four classes: **A** live validated,
**B** paper validated, **C** historical simulation, **D** hypothesis. Each
`EvidenceRecord` already carries one. An artifact carries a tuple of records, so
the artifact-level grade has to be derived from a set.

**The strongest grade present, not the weakest.** `Evidence_Standards.md:41`
states "Hypotheses do not invalidate production evidence." Taking the minimum
would mean one Level D hypothesis attached to a well-evidenced artifact
downgraded it — which is exactly a hypothesis invalidating production evidence,
and is forbidden. The rule corroborates independently: the grade then tracks the
capital ladder, since a strategy in research carries hypotheses (D), a backtested
one simulation (C), a paper-traded one paper validation (B) and a live one live
validation (A).

**Stored rather than derived at read time**, because `Knowledge/Search.md:3`
states "Belay retrieves information through metadata" and filters on Evidence
Level at line 15. A value computed at read time is not metadata and cannot be
filtered.

**Computed by `ArtifactFactory`, verified by `ArtifactValidator`** — the same
split already used for the integrity hash. A hand-set evidence grade is an
opinion, and a four-class hierarchy exists precisely so that it is not one. The
validator recomputes and rejects a mismatch, so a forged grade fails the gate.

**`None` when there is no evidence**, on the same anti-fabrication ground as
confidence: an artifact with no evidence has no grade, and inventing `D` for it
would make "unevidenced" indistinguishable from "hypothesis".

Known consequence, accepted: one Level A record among ten Level D records reads
as Level A. Storing the distribution instead was considered and rejected —
`Schema.md` asks for one field, and the constitution's rule is about which grade
wins, which is a maximum.

---

## Consequences

Positive:

- three required schema fields stop being absent
- confidence becomes revisable, which `RegimeCompatibility.md` requires
- the revision history of an estimate is preserved rather than overwritten
- `Knowledge/Search.md`'s filters have fields to filter on

Negative:

- every confidence adjustment costs a version, and `RegimeCompatibility.md`'s
  "continuously updates" could mean a great many versions
- `ArtifactValidator.REQUIRED` still lists three of thirteen fields; closing that
  gap is separate work
- adding fields changes `canonical_payload` and therefore every future integrity
  hash

On the version-count tension: `RegimeCompatibility.md` governs *compatibility*
confidence, held per regime, which is plausibly a different quantity from the
artifact-level `Current Confidence` of `Schema.md`. If they are the same, the
per-version cost needs a ruling. **Scoped out of this ADR deliberately** — it
should not be settled in passing.

---

## Required Follow-Up (ADR-005)

- add the three fields, with `confidence` bounded to 0-1 and defaulting to `None`
- strengthen `test_confidence_can_be_adjusted` before implementing: it currently
  asserts only that a `confidence` field exists, which adding an immutable field
  would satisfy, so closing finding 1 would silently mark finding 2 closed too
- rule on `Evidence Level` separately
- decide whether compatibility confidence and Current Confidence are one quantity

---

## ADR-006: Which Promotion Criteria List Governs

Status:
**Accepted.** Ratified 2026-07-30. Not yet implemented — the follow-ups edit
three departmental documents and add a conformance test.

Date:
2026-07-30

---

## Context

Five documents state promotion criteria and no two agree. Counts: seven
(`constitution/Promotion_Pipeline.md:75-81`), eight
(`strategies/PromotionCriteria.md:7-21`), six
(`Validation/CapitalReview.md:15-25`), seven
(`workflows/Monthly/StrategyPromotion.md:11-23`) and nine minimum metrics
(`Validation/Backtesting.md:15-31`).

**No criterion appears in all five.** `Drawdown` comes closest at four of five and
is absent from `PromotionCriteria.md` — the one document that defines a Promotion
Score.

Shared concepts are named inconsistently in ways that are not cosmetic:

- `Regime robustness` (three documents) versus `Regime Compatibility`
  (`StrategyPromotion.md:21`). Robustness means surviving a regime change;
  compatibility means suiting a regime. These are different claims.
- `Operational consistency` / `Operational Stability` / `Operational readiness`
  across four documents. Readiness is a precondition; consistency is a track
  record.
- `Risk-adjusted returns` (`Promotion_Pipeline.md:76`) versus bare `Risk`
  (two documents). Return per unit of risk is not exposure to loss.

`workflows/Monthly/StrategyPromotion.md` is the workflow that actually runs
promotion reviews, and it omits Liquidity, Execution and Statistical Performance —
all three of which the Constitution requires promotion to consider.

The `Promotion Score` at `PromotionCriteria.md:25-27` has a range of 0-100, no
weights, no mapping from the eight categories, and defers its threshold entirely
(`line 29`: "Promotion thresholds are determined by the Investment Committee").
It is uncomputable from the documents as written.

`scripts/status.py:48-56` and `docs/ROADMAP.md:47-56` are both built solely on the
constitutional seven, while `docs/ROADMAP.md:221-222` warns that "no code change
should rest on `Promotion_Pipeline.md` alone" — which is exactly what the
dashboard does, and `ROADMAP.md:210-211` concedes "The choice of seven is a
working assumption".

---

## Decision

**1. The constitutional seven govern.** `constitution/Promotion_Pipeline.md:75-81`
is the authoritative promotion criteria list. `constitution/Governance.md:7` states
"The Constitution possesses authority", and Immutable Law X ranks it above
departmental documents. The dashboard's existing choice is ratified and stops being
a working assumption.

**2. The five lists are not five rivals. They sit at three altitudes.**

- `Promotion_Pipeline.md` states the *criteria* — what promotion must consider.
- `Validation/Backtesting.md` states *instruments* — the nine metrics that measure
  some of those criteria. A metric list and a criteria list do not compete; they
  intersect at one word (`Drawdown`) because that is the only criterion currently
  named identically in both.
- `CapitalReview.md` and `StrategyPromotion.md` are *departmental checklists*
  operating the constitutional criteria. Where they diverge, they are wrong, not
  authoritative.

**3. The constitutional wording is canonical where documents disagree on a name.**
`Regime robustness`, not compatibility. `Operational consistency`, not stability or
readiness. `Risk-adjusted returns`, not bare `Risk`.

**4. The 0-100 Promotion Score is suspended, not adopted.** A score with no weights
and no threshold cannot be computed, and a number that looks computed but is not is
worse than no number. It becomes live when the Investment Committee supplies both.

**5. The departmental omissions are defects to be corrected, not permitted
narrowings.** `StrategyPromotion.md` must consider Liquidity, Execution quality and
Statistical performance, because the Constitution requires it.

---

## Consequences

Positive:

- `scripts/status.py`'s "1 of 7 computable" becomes a governed figure
- the naming collisions stop being silent disagreements
- the uncomputable score stops being a pending obligation

Negative:

- three departmental documents need editing, and the governance layer is frozen by
  ADR-002 — though the freeze bars *adding* documents, not correcting existing ones
- ratifying seven criteria does not make six of them computable

---

## Required Follow-Up (ADR-006)

- update `ROADMAP.md:210-211,221-222` to record the seven as ruled rather than
  assumed
- reconcile the three departmental lists to the constitutional wording
- add a conformance test asserting `scripts/status.py`'s `PROMOTION_CRITERIA`
  equals `Promotion_Pipeline.md:75-81`, parsed from the document

---

## ADR-007: The Lifecycle Sequence, And An Amendment To ADR-002

Status:
**Accepted.** Ratified 2026-07-30. The amendment to ADR-002 was applied the same
day; the original false sentence is preserved in the amendment note rather than
discarded.

Date:
2026-07-30

---

## Context

Four documents state a promotion sequence: eight stages in
`constitution/Paper_First_Capital_Doctrine.md:13-41`, the same eight in
`README.md:43`, seven maturity levels in `constitution/Promotion_Pipeline.md`,
and nine in `strategies/Lifecycle.md`, which adds Retirement.

Divergence is confined to the first two stages, whether a promotion review exists,
and whether retirement is a stage. **From Validation onward all four agree**, and
every source that mentions capital tiers includes Micro Capital.

Separately, and materially: **ADR-002 contains a false citation.**
`docs/DECISIONS.md:102` states "`constitution/Promotion_Pipeline.md` defines eight
promotion gates." That file contains no group of eight. It has seven maturity
levels and seven promotion considerations. The documents that do contain a group
of eight are `Paper_First_Capital_Doctrine.md` (eight lifecycle stages) and
`strategies/PromotionCriteria.md` (eight evaluation categories) — the latter cited
in ADR-002's very next sentence for a different purpose.

ADR-002 is Accepted and has never been amended, so the error stands inside a
ratified decision while `ROADMAP.md`, `HANDOFF.md` and `CHANGELOG.md` each
separately record that it is wrong.

---

## Decision

**1. The doctrine's eight stages are the lifecycle.** `Idea, Research, Validation,
Paper Trading, Promotion Review, Micro Capital, Limited Capital, Production`.
`StrategyLifecycle` already implements exactly this and is ratified unchanged.

**2. `Promotion_Pipeline.md`'s seven levels are a maturity model, not the
lifecycle.** They describe how proven a strategy is; the lifecycle describes what
capital it has earned. Two axes, not two competing sequences.

**3. Retirement is not a stage.** Already ruled by ADR-004 and by the doctrine,
which places retirement outside the sequence and reachable from anywhere.
`strategies/Lifecycle.md`'s ninth entry is a state, not a rung.

**4. ADR-002 is amended.** The sentence at `DECISIONS.md:102` is corrected to cite
`constitution/Paper_First_Capital_Doctrine.md` for the eight stages. The amendment
is recorded rather than the text silently edited, because ADR-002 is Accepted and
`Governance.md:11` requires that all decisions be documented.

---

## Consequences

Positive:

- the enum stops being defensible only by inference
- an error inside an Accepted ADR is corrected rather than annotated in three
  other documents
- "which sequence is right" ceases to be an open question

Negative:

- amending a ratified ADR sets a precedent that must be used sparingly
- `strategies/Lifecycle.md` and `Promotion_Pipeline.md` still read as sequences and
  will mislead until edited

---

## Required Follow-Up (ADR-007)

- amend `DECISIONS.md:102` with a dated amendment note
- add a conformance test parsing the doctrine's eight stages and asserting
  `StrategyLifecycle` matches, `RETIRED` excluded
- record in `Promotion_Pipeline.md` that its levels are a maturity model

---

## ADR-008: Remain Is An Outcome, Not A Transition

Status:
**Accepted.** Ratified 2026-07-30. Unimplementable until review decisions are
recorded somewhere, which is the same blockage as ADR-004 rule 4. Rule 4 below
(`Reject`) was sharpened on ratification — see the note there.

Date:
2026-07-30

---

## Context

Three documents list `Remain` as a formal review outcome, and all three name it
differently:

- `strategies/ReviewTemplate.md:51` — `Remain`, under `Recommendation`
- `Validation/CapitalReview.md:33` — `Remain Current Stage`, under
  `Possible Outcomes`
- `workflows/Monthly/StrategyPromotion.md:31` — `Remain Current Stage`, under
  `Possible Decisions`

`CapitalReview.md:31` adds a fifth outcome, `Reject`, which appears in no other
list, is never defined, and is never distinguished from `Retire`.
`PromotionCriteria.md:35` nonetheless requires "Every rejection requires written
justification" — an obligation attached to an outcome the monthly workflow cannot
produce.

`constitution/Governance.md:11` requires "All decisions require documentation",
and `StrategyPromotion.md:37` requires "Every decision requires written
justification". A review that holds a strategy at Limited Capital has made a
decision.

`ArtifactValidator.validate_transition` rejects every self-transition, because no
stage appears in its own successor tuple. So a documented decision to Remain is
currently indistinguishable from no review having taken place.

---

## Decision

**1. `Remain` is a review outcome. It is not a lifecycle transition, and no
self-transition is added.** The transition table rules the legality of *movement*;
Remain is the absence of movement. Adding `X -> X` rows would make the table a
record of decisions, which the comment above it explicitly denies — "Legality
only" — and would still not distinguish "reviewed and held" from "never reviewed",
because a legal move is not a performed one.

**2. Remain is recorded where review decisions are recorded.** That layer does not
exist. This ADR rules what Remain *is* so that the layer can be built correctly,
rather than bending the lifecycle to absorb it. ADR-004 rule 4 and the re-sizing
step are blocked on the same missing layer; this is a third obligation on it, and
the three should be built together.

**3. The canonical name is `Remain Current Stage`.** Two of three documents use
it, and it is unambiguous where bare `Remain` is not.

**4. `Reject` and `Remain Current Stage` are one event named from two sides.**
*(Sharpened on ratification, 2026-07-30. The original text called `Reject` a
synonym without saying why only one document carries both.)*

`Validation/CapitalReview.md` is the only document listing both, and its own
framing explains that: lines 7 and 9 state "Capital Review does not allocate
capital. Capital Review **recommends** promotion." It processes a *request*.
`Reject` names the decision on the request; `Remain Current Stage` names the
effect on the strategy. Rejecting a promotion leaves the strategy where it is.
The other two documents list only the state-side name because neither is framed
as handling an application.

A competing reading is recorded rather than dismissed: `Reject` could mean
rejected *as a candidate* — dropped out of `PROMOTION_REVIEW` back to
`PAPER_TRADING` — which ADR-004 already distinguishes ("falling out of it means
it is no longer a candidate"). Under that reading `Reject` is a specific
demotion, not a synonym. The document supports both readings and the code
supports neither, so the ruling above is adopted and `CapitalReview.md` must
state it explicitly rather than leave it inferable.

---

## Consequences

Positive:

- the four outcomes become one vocabulary across three documents
- the lifecycle table stays a statement about legality
- the missing review-decision layer acquires a third, specified obligation

Negative:

- nothing is implementable until that layer exists, so the finding stays open in
  practice even once this is ratified
- ruling `Reject` a synonym may be wrong if it was meant to carry a distinct
  meaning nobody wrote down

---

## Required Follow-Up (ADR-008)

- specify the review-decision record, carrying at minimum: artifact identifier,
  version reviewed, reviewer, date, outcome, written justification
- correct `ReviewTemplate.md` to `Remain Current Stage`
- correct or define `Reject` in `CapitalReview.md`
- only then revisit the promotion/demotion/retirement classifier ADR-004 defers —
  it needs the outcome vocabulary this ADR settles

---

## ADR-009: The Review Decision Record

Status:
**Accepted.** Ratified 2026-07-31 and implemented the same day, as drafted — no
rule was amended on ratification. See the Implementation Record at the end for
three decisions taken during implementation that the ruling did not cover.

Date:
2026-07-31

---

## Context

Three ratified obligations block on one missing component, and nothing else in
the repository has that property:

- **ADR-004 rule 4** — a demotion requires written justification. ADR-004's own
  implementation record states it "is not enforced anywhere and cannot yet be",
  because "there is no layer that records review decisions".
- **ADR-004's re-sizing step** — a demotion triggers a fresh allocation
  determination, performed by the reviewer in prose until a position-sizing layer
  exists. Nowhere records that prose.
- **ADR-008** — `Remain Current Stage` is a review outcome, "recorded where review
  decisions are recorded. That layer does not exist."

`constitution/Governance.md:11` states "All decisions require documentation."
`strategies/ReviewTemplate.md` specifies the form of a review — identifier,
reviewer, date, version, confidence adjustment, recommendation, justification —
and no code holds it. A review that decides to hold a strategy at Limited Capital
has made a decision, and today it is indistinguishable in the system's state from
no review having happened.

**Written justification is required by four documents, and between them they
cover all four outcomes:**

- `strategies/PromotionCriteria.md:33` — "Every promotion requires written justification."
- `strategies/PromotionCriteria.md:35` — "Every rejection requires written justification."
- `constitution/Governance.md:15` — "All retirements require justification."
- `workflows/Monthly/StrategyPromotion.md:37` — "Every decision requires written justification."
- ADR-004 rule 4 — demotion.

ADR-008 cited only `PromotionCriteria.md:35`. **Line 33 exists and was not cited**;
it places the same obligation on promotion. Opened and read on 2026-07-31, not
carried over from ADR-008.

The outcome vocabulary, as the three documents write it:

| Document | Heading | Outcomes |
|---|---|---|
| `strategies/ReviewTemplate.md:47-55` | Recommendation | Promote, Remain, Demote, Retire |
| `Validation/CapitalReview.md:29-39` | Possible Outcomes | Reject, Remain Current Stage, Promote, Demote, Retire |
| `workflows/Monthly/StrategyPromotion.md:27-35` | Possible Decisions | Promote, Remain Current Stage, Demote, Retire |

ADR-008 rule 3 rules `Remain Current Stage` canonical. Rule 4 rules `Reject` the
decision-side name for the same event.

---

## Decision

**1. The review decision record is an Artifact of type `REVIEW`.**

Not a parallel record type. Five reasons, in order of weight:

- **It inherits signing and integrity.** A decision record that can be altered
  after the fact documents nothing. `Governance.md:11` requires decisions be
  documented, and an unsigned, unversioned file is not a record of one. This alone
  would decide it.
- **`ArtifactType.REVIEW` already exists.** No new member is added, so this does
  not touch the open `ArtifactType` finding — see the boundary below.
- **`Knowledge/Identifiers.md:39-41` already assigns `REV` to Review**, with the
  worked example `REV-0048` at line 17. The identifier space was reserved for this
  before any code existed.
- **ADR-002 permits no second channel.** "Mechanics emit Artifacts. Governance
  consumes Artifacts. Neither layer reaches across the boundary by any other
  means." A review decision is consumed by governance.
- **It satisfies `Governance.md:19-25`** — identifier, version, author, date,
  status — on machinery that already exists and is already tested.

**This routes around the `ArtifactType` finding. It does not settle it.** That
finding asks whether `ArtifactType` is a closed enum that must grow or a coarse
enum plus a subtype, and asks that members not be added without deciding which.
This ADR needs no new member, so it does not force the answer and must not be read
as having supplied one.
`test_artifact_type_can_name_the_documented_deliverables` stays `xfail`.

Noted because it will confuse someone: `ArtifactType.REVIEW` and
`ArtifactLifecycle.REVIEW` are different enums that share a name. A review
artifact awaiting approval is `type=REVIEW, lifecycle=REVIEW`. That is correct and
reads like a mistake. ADR-003 split these deliberately; the collision is the price.

**2. The record carries its subject in typed fields, separate from its own identity.**

`ReviewTemplate.md:3-9` opens with `Identifier`, `Reviewer`, `Date`, `Version`.
Read as the review's own identity, the template names no subject at all — nothing
else in the file says which strategy was reviewed, which cannot be right. Read as
the subject's, the template is self-consistent. ADR-008's follow-up reads it the
same way, independently: "artifact identifier, version reviewed".

But the record is an Artifact, so `id` and `version` are already spoken for by
`Governance.md:19-25`. The subject therefore needs its own fields:

- `subject_id` — the identifier of the artifact reviewed
- `subject_version` — the version of it that was reviewed

`subject_version` is not bookkeeping. Under ADR-005 a confidence revision produces
a *new version*, so recording which version was in front of the reviewer is the
difference between a decision about the artifact they read and a decision about an
artifact that has since changed underneath it.

**3. Four outcomes. `Reject` is not a fifth.**

`PROMOTE`, `REMAIN_CURRENT_STAGE`, `DEMOTE`, `RETIRE`, spelled as ADR-008 rule 3
rules. `Reject` is documented on the enum as the decision-side name for
`REMAIN_CURRENT_STAGE`, per ADR-008 rule 4, and is not a member. One event with two
names must not become two members — that is the drift this vocabulary exists to
stop, and `CapitalReview.md` listing five where the other two list four is the drift
already in progress.

**4. Written justification is mandatory for every outcome, and is enforced.**

Four documents require it; `StrategyPromotion.md:37` requires it of every decision
without qualification. A record whose justification is empty or blank is refused at
construction.

This is where ADR-004 rule 4 finally lands. The transition table rules that a move
is legal; the record rules that a reason was written. ADR-004 said exactly this —
"Rule 4 therefore has no home in `ArtifactValidator` and must be enforced wherever
review decisions are recorded".

The check is on non-blank content, because whitespace is not a justification.

**5. The record names the resulting stage, and the outcome must agree with it.**

- `REMAIN_CURRENT_STAGE` — the resulting stage equals the stage at review. This is
  precisely what makes a held strategy distinguishable from an unreviewed one,
  which is ADR-008's entire purpose.
- `RETIRE` — the resulting stage is `RETIRED`.
- `PROMOTE` — the resulting stage is higher on the ladder, and legal under
  `STRATEGY_TRANSITIONS`.
- `DEMOTE` — the resulting stage is lower on the ladder, and legal under
  `STRATEGY_TRANSITIONS`.

`RETIRED` is removed from the ladder before any position is compared. It is
declared at index 8, above `PRODUCTION` at 7, so a bare ordinal comparison reads
every retirement as the deepest promotion in the system. ADR-004 flagged this trap
and warned it "becomes live the moment this helper is written". This is the first
code outside the two guarded test modules to compare stage positions, so the trap
is now live and is handled the same way both test modules handle it.

**This is not the classifier ADR-004 defers, and does not discharge it.** The
deferred classifier derives a *name* from a transition, and must cope with inputs
this never sees. `Draft → Review → Approved` is not a promotion, a demotion or a
retirement, and `ArtifactLifecycle` still has no vocabulary for what it is. ADR-008
settled self-transitions; it left artifact-lifecycle transitions untouched, and it
must not be read as clearance.

What this rules is the inverse and strictly narrower: given an outcome the reviewer
**declared**, and a stage pair they **declared**, are the two consistent? It is only
ever handed `StrategyLifecycle` values, and it is never asked to name a transition
nobody named. No general `classify(current, target)` helper is added to
`framework/`, and ADR-004's follow-up stays open.

**6. Confidence adjustment is a recorded direction; the resulting figure is optional.**

`ReviewTemplate.md:37-43` lists `Increase` / `Decrease` / `No Change` as a decision
the review makes, so it is recorded as one: required, with no default. A default
would be a fabricated decision — the failure ADR-005 rule 4 already ruled against
for confidence itself, where 0.5 "would be a fabricated estimate that nothing
distinguishes from a real one".

The resulting figure is optional. ADR-005 rules that a confidence revision produces
a new version of the **subject** artifact; deciding to adjust and producing that
version are separate acts, and the second may not have happened yet. Where a figure
is supplied it is bounded to 0-1, like every other confidence in the system.

**7. The re-sizing note is optional, and that is a ruling rather than an omission.**

ADR-004 sequences a fresh allocation determination after a demotion, and records
that it has no implementation: "Until that exists, step 2 is performed by the
reviewer in prose."

It must not be required. `constitution/Capital_Authority.md` states "Capital
preservation overrides return maximization... Capital preservation wins. Always",
and ADR-004 concludes from it: "If step 2 cannot be completed, step 1 still stands
and the strategy sits at its new stage." A **required** re-sizing field would let a
missing input block the recording of a demotion — the exact reading ADR-004
forbids. The reason is written here so that a later session does not "tighten" this
into a defect.

**8. The template's six prose sections are content, not typed fields.**

Operational Summary, Observed Behavior, Expected Behavior, Performance Summary,
Risk Assessment and Regime Compatibility are narrative. Nothing computes on them.
They are carried in the artifact's existing `content` field.

Typing them would add six fields with no consumer, and `Artifact` fields are inside
the integrity hash — every one added is permanent, and ADR-005 already recorded
that adding fields "changes `canonical_payload` and therefore every future
integrity hash". If a component later needs to compute on Risk Assessment or Regime
Compatibility, promoting one to a typed field is a schema change to be ruled then,
on evidence that a consumer exists.

**9. `ArtifactSerializer` gains `load()`.**

It implements `dump` and nothing else, so an artifact can be written and never read
back. A decision record that cannot be read back cannot inform the next review,
which is most of why it exists — and `Knowledge/Search.md:3` builds retrieval
entirely on reading stored metadata.

**The acceptance test is the round trip through integrity, not through equality:**
`dump`, then `load`, then `ArtifactIntegrity.verify_hash` returns `True`. A loader
that reconstructs every field but produces a different canonical payload has
silently broken every signature it touches. Field-by-field equality would not catch
a value that renders to the same text and hashes differently, which is the failure
mode that matters here.

`load()` does not sign. An artifact read from disk keeps the hash it was stored
with, exactly as `Artifact` keeps whatever hash it is given: re-signing on load
would hand every tampered file a fresh valid signature, which is the reasoning
already recorded for `dataclasses.replace()` and guarded by
`test_replace_does_not_resign_an_artifact`.

**10. Nothing is enforced about who may review.**

`Governance.md:3` places authority in process rather than hierarchy, and no
document in the repository names reviewer roles or an authority list. `reviewer` is
required and non-empty; nothing checks it against a roster, because no roster is
written. Inventing one would be writing doctrine, which ADR-002's freeze and
ADR-004's "specify it before writing it" both forbid.

---

## Consequences

Positive:

- three ratified obligations acquire the single home they were all waiting on
- ADR-004 rule 4 becomes enforceable for the first time since it was ratified
- a strategy held at a stage stops being indistinguishable from an unreviewed one
- artifacts become readable, closing a gap that has been noted in `HANDOFF.md`
  since 2026-07-30 without ever being recorded as a finding

Negative:

- `ArtifactType.REVIEW` acquires a specific meaning it did not carry before, and
  the open `ArtifactType` question is routed around rather than answered
- `load()` is a second place that must know the artifact schema. A field added to
  `Artifact` and not to the loader would be silently dropped on read — pinned by a
  test that compares the loader against `dataclasses.fields(Artifact)` rather than
  against a transcribed list
- the record can attest that a justification was written. It can never attest that
  the justification is any good, and no test should be written implying otherwise

---

## Rejected Alternatives

**A separate `ReviewDecision` type outside the artifact system.**

Reason: it would need its own persistence, integrity and versioning, all three of
which already exist and are tested. ADR-001 rejected a parallel artifact
representation because it "would introduce duplicate system truth and increase
architectural drift", and this would be one.

**Adding a `REVIEW_DECISION` member to `ArtifactType`.**

Reason: `REVIEW` already exists and fits. Adding a member would take a position on
the open `ArtifactType` finding as a side effect of unrelated work — precisely what
that finding asks not to be done.

**Recording the subject through a relationship rather than typed fields.**

Reason: `Knowledge/Relationships.md` defines eleven types and none means "reviews".
`Derived From` is the closest and is a stretch. Relationship targets are bare
identifiers with no version, so `subject_version` — the field that makes the record
precise — would have nowhere to live. A twelfth relationship type may later be
right, but it is new doctrine and should be ruled deliberately rather than
introduced to serve one field of one record.

**Requiring justification only for demotion and rejection, which is what ADR-004
and `PromotionCriteria.md:35` say literally.**

Reason: `StrategyPromotion.md:37` requires it of every decision, and
`PromotionCriteria.md:33` and `Governance.md:15` extend it to promotion and
retirement. Implementing only the narrow rules would leave the broadest one
unimplemented while appearing to have satisfied the requirement.

---

## Required Follow-Up (ADR-009)

Not to be started before ratification.

- add `ReviewOutcome` and `ConfidenceAdjustment` to `framework/artifacts/enums.py`
- add the review decision record, built through `ArtifactFactory` so it is signed
  like everything else
- enforce: non-empty justification, non-empty reviewer, outcome/stage agreement,
  confidence bounds, and the `RETIRED`-off-the-ladder rule
- add `ArtifactSerializer.load()`, with the dump/load/verify round trip as its
  acceptance test
- pin the loader against `dataclasses.fields(Artifact)`, so a future field cannot
  be silently dropped on read
- add a conformance test parsing the outcome lists from all three documents and
  asserting `ReviewOutcome` covers them, `Reject` mapped per ADR-008 rule 4
- correct `strategies/ReviewTemplate.md:51` to `Remain Current Stage` — an ADR-008
  follow-up this unblocks
- correct or define `Reject` in `Validation/CapitalReview.md` — likewise
- do **not** write the promotion/demotion/retirement classifier. ADR-004's
  follow-up stays open, and rule 5 above is not it

---

## Implementation Record (ADR-009)

Done 2026-07-31, in the order of the follow-up list. Tests were written first and
run against the unchanged code to prove they fail rather than pass vacuously: the
round-trip module gave 11 failed, the review module failed at collection because
`ReviewOutcome` did not exist, and the outcome conformance test failed on the
import. Suite 168 → 211 passed, 4 xfail, 1 skipped.

`framework/artifacts/review.py` holds the record. `ReviewOutcome`,
`ConfidenceAdjustment` and `STRATEGY_LADDER` are in
`framework/artifacts/enums.py`; `ArtifactSerializer.load()` is in
`serializer.py`.

**The `ArtifactType` watcher was verified still `xfail`, not assumed to be.**
Rule 1 claimed this ADR adds no enum member and therefore does not answer the
open `ArtifactType` finding. `test_artifact_type_can_name_the_documented_deliverables`
remains among the four xfails after implementation, so the claim holds.

**ADR-004's `RETIRED` trap is now live and is handled.** `_check_outcome_matches_movement`
branches on `RETIRE` and on a `RETIRED` destination *before* taking any ladder
position, and `STRATEGY_LADDER` has `RETIRED` removed so `.index()` raises rather
than lying if one reaches it. Two tests pin it: a retirement recorded as a
promotion and one recorded as a demotion are both refused. Under a bare ordinal
comparison the first would have been accepted as the deepest promotion in the
system.

**Legality is delegated, not re-decided.** The record asks
`ArtifactValidator.validate_transition` whether the move is legal rather than
carrying its own view. ADR-004 rules the ten demotions and the `PAPER_TRADING`
floor; a second opinion here would eventually disagree with it. So a promotion
that skips a stage and a demotion below the floor are refused by the existing
table.

### Three decisions the ruling did not cover

**`subject_version` must be a semantic version.** Not in the ruling. It applies
an invariant the repository already holds — `ArtifactRepository.save()` refuses a
non-semantic version because append-only storage could never correct such a
filename. A review naming `v2` could not be matched against any stored version of
its subject, so the field would record a decision about nothing. Recorded here
rather than left implicit, since it is a constraint a future reviewer will hit.

**`review_fields()` refuses a hollow record rather than returning `None`s.** An
artifact typed `REVIEW` but not built by `review_artifact` carries no decision,
and a dict of `None`s would let it pass for one. This is the silent-fallback
failure that left the dashboard reporting no priorities at all for two sessions,
so it raises.

**`ArtifactSerializer.dump` now renders timestamps as `isoformat` strings rather
than native YAML timestamps.** This goes beyond "add `load()`" and is the one
change to existing behaviour, so it is recorded rather than buried.

The reason as first written was wrong and is corrected here. The comment claimed
PyYAML converts an offset timestamp to UTC and returns it naive; **checked
directly, the installed version round-trips `+05:00` to an identical isoformat.**
So this fixes no live bug. What it removes is a dependency:
`ArtifactIntegrity.canonical_payload` hashes `created.isoformat()`, which makes
the exact rendering of a timestamp signature-critical, while PyYAML's timestamp
construction is library behaviour Belay does not control and has not pinned —
and older releases did return naive UTC. `canonical_digest`'s own docstring
already asks callers to pass "a timestamp as `.isoformat()`". Nothing pinned the
dump format and no artifacts are stored in the repository, so the change costs
nothing today.

`load()` refuses a stored timestamp with no offset rather than assuming UTC, for
the same anti-fabrication reason `EvidenceRecord` refuses naive timestamps: a
value whose meaning depends on an assumption is not reproducible evidence.

### Still open, deliberately

**The promotion/demotion/retirement classifier is not written.** Rule 5 is not
it, and no `classify(current, target)` is exported. ADR-004's follow-up stays
open: `Draft → Review → Approved` is still not a promotion, a demotion or a
retirement, and `ArtifactLifecycle` still has no vocabulary for what it is.

**`ArtifactRepository` still cannot return an artifact.** `load()` exists on the
serializer, but `latest()` returns a version string and no `get()` was added —
that is a repository change ADR-009 did not rule and no caller yet needs. It is
now a small piece of work rather than a blocked one.

**The re-sizing step remains prose.** `resizing_note` is a free-text field
because there is no position-sizing layer and four of the six inputs
`Capital_Authority.md` names do not exist as computed values. ADR-004 says step 2
is performed by the reviewer in prose until then, and rule 7 keeps it optional so
a missing input can never block the recording of a demotion.

~~**`ArtifactRepository` still cannot return an artifact.**~~ Closed 2026-07-31.
`get()` exists, delegates to `latest()` when no version is named, and verifies
integrity on read. The reasoning is in the method.

---

## ADR-010: ArtifactType Is A Coarse Type With A Constrained Subtype

Status:
**Accepted.** Ratified 2026-07-31 as drafted; no rule was amended on
ratification. Implemented the same day. `DeliverableType` carries the
twenty-four members the eleven documents declare,
`test_artifact_type_can_name_the_documented_deliverables` is rewritten to rule 9
and its `xfail` marker is removed.

**Implementation surfaced one thing the ADR did not anticipate**, recorded as a
new finding rather than fixed by widening this ruling: `ArtifactType` and
`Knowledge/Identifiers.md` are two vocabularies that should agree and do not.
`PORTFOLIO` and `FAILURE` are enum members with no identifier prefix, and `DOC`
is a prefix with no member. Rule 9's mapping assigns three deliverables to
`PORTFOLIO` and one to `FAILURE`, so those artifacts have no prefix to carry.
See `docs/HANDOFF.md`.

Date:
2026-07-31

---

## Context

`ArtifactType` has nine members. `docs/HANDOFF.md` has recorded since 2026-07-26
that the departmental and workflow documents name "roughly twenty" deliverables
the enum cannot name, and asked for a ruling: **closed enum that must grow, or
coarse enum plus a subtype.** Every session since has routed around it. ADR-009
routed around it deliberately and said so.

**The figure was an estimate and is now counted.** Every document under
`departments/`, `Research/`, `Validation/`, `Operations/` and `workflows/` was
read on 2026-07-31 — 31 documents, 13,049 characters. Eleven of them declare
deliverables under an explicit `Output`, `Outputs`, `Deliverable` or
`Deliverables` heading:

| Document | Entries |
|---|---|
| `departments/Research/README.md` | 5 |
| `Research/ChiefScientist.md` | 1 |
| `Research/ResearchAnalyst.md` | 1 |
| `Research/UniverseDiscovery.md` | 1 |
| `Validation/Critic.md` | 1 |
| `Validation/README.md` | 5 |
| `Operations/README.md` | 4 |
| `workflows/Daily/MarketClose.md` | 4 |
| `workflows/Daily/MarketOpen.md` | 5 |
| `workflows/Monthly/InvestmentCommittee.md` | 3 |
| `workflows/Weekly/WeeklyResearch.md` | 4 |

**34 entries, 25 distinct** once singular and plural are treated as one name.
Four more are named only in prose — `Portfolio Snapshot`
(`Operations/PortfolioManager.md`, "Generate daily portfolio snapshots"),
`Exception Report` (`workflows/Daily/MiddayReview.md`), `Portfolio Summary`
(`workflows/Weekly/WeeklyPortfolioReview.md`) and `Historical Summary`
(`workflows/Events/StrategyRetirement.md`). **29 in total, against nine enum
members.** So "roughly twenty" was an undercount, not a rough count.

Four properties of that list decide this ADR, and none of them was visible from
the estimate.

**1. The enum can already *type* almost all of them. What it cannot do is
*distinguish* them.** Sixteen of the 25 are report-shaped — ten end in `Report`,
plus `Daily Summary`, `Investment Committee Minutes`, `Research Digest`,
`Literature Review`, `Promotion Review` and `Paper Trade Log`. Every one of those
is honestly an `ArtifactType.REPORT` today. The finding's title is exact: the enum
cannot *name* them. It has never been unable to type them.

**2. The same deliverable is produced by different producers at different
cadences.** Seven of the 25 are declared by more than one document. `Universe
Report` is declared three times — as a Research *department* deliverable, as the
output of a Research *function* (`Research/UniverseDiscovery.md`), and as a
*daily workflow* deliverable of `MarketOpen`. `Regime Report`, `Research Memo`,
`Research Digest`, `Critique Report` and `Performance Report` are each declared
twice. A closed enum has to decide whether the daily universe report and the
departmental universe report are one member or two, and nothing in any document
suggests they are different documents.

**3. Three of the entries are not artifacts at all.** `Knowledge Update` appears
in three Deliverables lists — `MarketClose`, `MarketOpen`, `InvestmentCommittee`
— but `workflows/WorkflowEngine.md` lists "Update Knowledge" as a step in the
execution model of *every* workflow, and `workflows/Events/StrategyPromotion.md`
lists `Repository Update` and `Knowledge Graph Update` as workflow steps. These
are effects on stored state, not documents produced. Growing the enum to cover
the Deliverables lists literally would make `ArtifactType` name things that are
not artifacts.

**4. Three names plausibly denote one thing, and this ADR does not know.**
`Research Memo` (`Research/ResearchAnalyst.md`: Hypothesis, Expected Mechanism,
Supporting Evidence, Risks, Required Tests, Confidence, Open Questions),
`Research Proposal` (`Research/ChiefScientist.md`: Motivation, Hypothesis,
Expected Edge, Validation Plan, Potential Failure Modes, Estimated Research
Value) and `Experiment Proposal` overlap heavily. Both documented structures are
"a testable hypothesis with an expected edge and a validation plan."

---

## The Precedent Already Exists

This shape has been chosen here once already. **ADR-009 made a review decision an
`Artifact` of type `REVIEW` carrying its subject in typed content fields rather
than in its own identity**, and its Rejected Alternatives explicitly refused to
add a member: adding one "would take a position on the open `ArtifactType`
finding as a side effect of unrelated work — precisely what that finding asks not
to be done."

So the coarse-type-plus-typed-detail pattern is not being invented here. It is
being generalised from a ratified decision, which is the difference between
applying a ruling and extending one.

---

## Decision

**1. `ArtifactType` stays closed and coarse. It is not grown to name
deliverables.** Its nine members describe what *kind of thing* an artifact is.
Twenty-nine members would make it a list of documents rather than a type, and it
would have to grow every time a workflow document names an output.

**2. A second field carries the specific kind.** `Artifact` gains
`deliverable: DeliverableType | None`. `ArtifactType` answers "what kind of thing
is this"; `deliverable` answers "which documented output is this". A universe
report is `(REPORT, UNIVERSE_REPORT)`.

**3. The subtype is a constrained enum, never free text.** This is the whole risk
of the coarse-plus-subtype shape and the reason it cannot be waved through: a free
string re-opens exactly the hole that produced the finding, where an orphaned
draft passed `artifact_type="UniverseReport"` and nothing refused it.
`DeliverableType` is an enum and `ArtifactValidator` refuses anything else — the
same treatment `RelationshipType` received.

**4. The vocabulary is derived from the documents, never transcribed.** A
conformance test parses the `Output`/`Outputs`/`Deliverable`/`Deliverables`
sections of the eleven declaring documents and asserts `DeliverableType` equals
what they declare. A list copied into code would drift from the documents exactly
as silently as the code has drifted before — and the drift is the thing being
guarded against, so the documents have to be the input. **No new governance
document is created**, so ADR-002's freeze is untouched: the vocabulary lives in
code and is checked against documents that already exist.

**5. Effects are not deliverables.** `Knowledge Update`, `Repository Update` and
`Knowledge Graph Update` get no member. They are steps in
`workflows/WorkflowEngine.md`'s execution model, performed by every workflow, and
an artifact is not produced. The parser in rule 4 must exclude them by name, and
the exclusion must be stated where it is applied rather than left as a silent
filter.

**6. A deliverable declared by several documents is one member.** Cadence and
producer are not part of a deliverable's identity. `Universe Report` is one
member whether Research produces it on request or `MarketOpen` produces it daily.
The producing workflow is already recoverable from the artifact's author and
timestamps, and duplicating it into the type would put the same fact in two
places.

**7. `deliverable` is optional and defaults to `None`.** Most artifacts are not
workflow deliverables — a strategy specification is not one, and a review record
is not one. `None` means "not a documented deliverable", which is a real state and
must not be confused with an unset field. It is refused as a caller-supplied value
on artifacts whose type cannot carry one.

**8. It is inside the integrity hash.** Every field a governance gate reads must
be covered by the signature, which is the reasoning ADR-005 applied to
`confidence` and `evidence_level`. A promotion gate that accepts a critique report
must not accept an artifact whose `deliverable` was changed to `CRITIQUE_REPORT`
after signing.

**9. The watcher is rewritten to assert the pair, not the member.** Once this is
ratified and implemented,
`test_artifact_type_can_name_the_documented_deliverables` asserts that **every
deliverable declared by the eleven documents resolves to a
`(ArtifactType, DeliverableType)` pair**, and its `xfail` marker is removed. That
sentence is the answer to the question the finding has been holding open, and it
is why the test could not honestly be strengthened before now.

**10. The three overlapping research names are NOT merged by this ADR.**
`Research Memo`, `Research Proposal` and `Experiment Proposal` each get their own
member, and whether they are one concept is left open. Merging them is a
departmental ruling about what Research produces, and it would be made here as a
side effect of a typing decision — which is the failure mode ADR-004 named and
ADR-009 refused. Recorded as an open question rather than resolved quietly.

---

## Consequences

Positive:

- the longest-open P2 finding gets an answer rather than another routing-around,
  and the last weak `xfail` watcher gets a specification
- `ArtifactType` stops needing to grow whenever a workflow document names an
  output, which is what would have made it unstable
- twenty-nine deliverables become nameable and, more importantly,
  *distinguishable* — sixteen of them are indistinguishable `REPORT`s today
- the vocabulary is checked against the documents, so a deliverable added to a
  departmental document without a corresponding member turns the suite red

Negative:

- every artifact now carries two type fields, and callers must learn which
  question each answers. Mitigated by rule 7's `None` default: code that does not
  care never sees it
- `DeliverableType` is a second enum that must track eleven documents rather than
  one, so its parser has eleven places to break. `RelationshipType` tracks one
- rule 6 asserts that a daily universe report and a departmental universe report
  are the same kind of document. That is a reading of the documents, not
  something any document states
- three research deliverables are given separate members that may later merge,
  and members are hard to remove once artifacts carry them

---

## Rejected Alternatives

**Growing `ArtifactType` to twenty-nine members.**

Reason: it would have to grow again whenever any workflow document names an
output, and three of the twenty-nine are not artifacts. It also forces a decision
this ADR avoids — whether `MarketOpen`'s universe report and Research's universe
report are the same member — where the coarse-plus-subtype shape lets producer
and cadence stay out of identity entirely.

**A free-text `subtype` string.**

Reason: it re-opens the exact hole the finding was raised about. An orphaned draft
passed `artifact_type="UniverseReport"` and nothing refused it; a free string
would make that legal rather than fixing it.

**A new governance document listing the deliverables, parsed as one vocabulary.**

Reason: ADR-002 freezes the addition of new governance documents until the
mechanics layer can feed the gates already written, and this would be one. Rule 4
achieves the same result against the eleven documents that already declare
deliverables.

**Leaving it open until the workflow layer is built.**

Reason: the finding has been open since 2026-07-26 and has been routed around
three times. The evidence needed to rule it is in documents that already exist and
has now been gathered; waiting would not improve it. Nothing here depends on the
workflow layer, because the deliverables are declared by departmental documents as
well as workflow ones.

---

## Required Follow-Up (ADR-010)

- add `DeliverableType` to `framework/artifacts/enums.py`, parsed-and-checked
  rather than transcribed
- add `deliverable` to `Artifact`, to `ArtifactIntegrity.canonical_payload`, and
  to `ArtifactSerializer.load`'s enum reconstruction — `load()` is a second place
  that must know the schema, and ADR-009 recorded that a field added to one and
  not the other is dropped in silence
- `ArtifactValidator` refuses an unknown `deliverable`, and refuses one on an
  artifact type that cannot carry it
- a conformance test parsing the eleven declaring documents against
  `DeliverableType`, excluding the three effects by name
- rewrite `test_artifact_type_can_name_the_documented_deliverables` to rule 9 and
  remove its `xfail` marker
- record the `Research Memo` / `Research Proposal` / `Experiment Proposal` overlap
  as an open departmental question in `docs/HANDOFF.md`

---

### Still open, deliberately

**Whether the three research deliverables are one concept.** Rule 10. It is a
question about what the Research department produces, not about typing, and it
should be ruled by whoever rules on `Research/ChiefScientist.md` versus
`Research/ResearchAnalyst.md`.

**Which deliverables the nine `ArtifactType` members map to.** Rule 9 requires
every deliverable to resolve to a pair, but this ADR does not tabulate the
mapping. Sixteen are plainly `REPORT`; `Market Snapshot` and `Portfolio Summary`
are arguably `PORTFOLIO`; `Failure Investigation` is arguably `FAILURE`. The
tabulation belongs with the implementation, where each choice can be tested
rather than asserted in prose.

---

## ADR-011: Metric Conventions Are Stated, Never Defaulted

Status:
**Accepted.** Ratified 2026-07-31 as drafted; no rule was amended on
ratification. Implemented the same day — `returns.py`, `volatility.py`,
`risk_adjusted.py` and `reporting.py` under `framework/metrics/`, with
`drawdown.py` migrated onto the same helper per rule 13.

**Every citation below was re-checked against the files by a second reader
before any code was written** — the check that caught the `Knowledge/Schema.md`
miscount on 2026-07-30. Twenty claims, **four wrong**, all four corrected in
place and marked rather than quietly rewritten:

- the document is forty-nine lines, not fifty
- its nine metric names sit on lines 15-31 on alternating lines, not 13-31 one
  per line; line 13 is the heading
- the claim that `risk-free`, `target return` and `standard deviation` appear in
  **no** document was false and self-refuting — this ADR contains `risk-free`
  seventeen times. Narrowed to "no document outside `docs/`", which is the claim
  the ruling actually rests on and which does hold
- the `Risk-adjusted returns` entry is `scripts/status.py:50`, not `:52` — line
  52 is `Regime robustness`

None of the four touches a rule. The reason for recording them is that the
drafting error rate on this ADR was one citation in five, and the next session
should size its own trust in a first draft accordingly.

Date:
2026-07-31

---

## Context

`Validation/Backtesting.md` names **nine minimum metrics** and one of them is
built. The document was opened and read in full — it is forty-nine lines, and the
nine names sit on lines 15-31, on alternating lines under the `Minimum Metrics`
heading at line 13. **It gives a name and nothing else: no formula, no parameter,
no convention.**

Four of the nine are not determined by their names.

- **Sharpe** requires a risk-free rate. The document does not give one. Every
  markdown file in the repository was searched — 101 of them — and **`risk-free`
  appears in no document outside `docs/`**, which is to say in no specification
  and no governance document. The only hits are inside this ADR and the
  `docs/HANDOFF.md` brief that asked for it.
  `strategies/StrategyTemplate.md:81` has an `Expected Sharpe` field and defines
  nothing.
- **Sortino** requires a target return. The same silence, and the same scope:
  `target return` appears in no document outside `docs/`.
- **CAGR** is a Compound *Annual* Growth Rate, so it requires knowing how many
  periods a year holds. Nothing in a sequence of floats says whether they are
  daily, weekly or monthly, and `252`, `trading days` and `periodicity` appear
  nowhere outside `docs/` either.
- **Volatility**, which Sharpe and Sortino both divide by, requires a choice
  between the sample and population standard deviation and a choice of
  annualization. `standard deviation` is in no specification document.

> The scoping in those four bullets is a correction. They were drafted claiming
> the strings appear "in no document at all", which the verification pass showed
> to be false and, as written, self-refuting: the ADR that says `risk-free`
> appears nowhere contains the word seventeen times. The substantive claim — that
> **no document Belay governs itself by defines any of these conventions** —
> survives intact, and it is the claim the ruling rests on. Recorded rather than
> silently reworded, because a citation that had to be narrowed is exactly the
> kind of thing a later session should be able to see.

So four of the nine minimum metrics **cannot be computed at all** without a
decision the constitution does not make. Making those decisions inside a function
body, where no reviewer would see them, is what this ADR exists to prevent.

`docs/HANDOFF.md` anticipated exactly this and asked for a ruling rather than a
convention. This is that ruling, widened by two things found while checking its
brief.

---

## Two Claims In The Brief Are Wrong

Both were checked by opening the files rather than inherited, which is the
discipline `docs/HANDOFF.md` closes with. Recorded here because the second one
changes what Stage 1 can honestly contain.

**1. `EvidenceRecord` does not have fields for the four required disclosures.**

`docs/HANDOFF.md:1287` states that `Validation/Backtesting.md`'s requirement to
record Assumptions, Data Source, Sample Period and Known Limitations is covered
because "`EvidenceRecord` already has fields for it". Opened:
`framework/artifacts/evidence.py` declares `source`, `methodology`, `level`,
`confidence`, `provenance`, `timestamp` and `hash`. `Data Source` is `source`.
**`Assumptions`, `Sample Period` and `Known Limitations` have no field.**

`docs/ROADMAP.md:107-109` states this correctly — "`EvidenceRecord` has
`methodology` and `provenance` but no structure for these four". The two
documents disagree and the roadmap is right.

**2. Two of the four metrics the brief calls computable are not computable.**

`docs/HANDOFF.md:5321` states that "CAGR, Win Rate, Exposure and Trade Count are
computable from a return series alone."

- **Trade Count cannot be.** A return series contains no trades. Nothing in a
  sequence of period returns says how many positions were opened, and a series
  produced by one position held for a year is identical to one produced by
  weekly turnover.
- **Exposure cannot be.** A period return of `0.0` is indistinguishable between
  "no position was held" and "a position was held and the price did not move".
  Exposure is the fraction of time capital was deployed, and the series does not
  carry it.
- **Win Rate is not wrong so much as undetermined.** The fraction of *periods*
  that were positive and the fraction of *trades* that were profitable are
  different numbers, and `Validation/Backtesting.md:23` says only `Win Rate`.

`docs/ROADMAP.md:104-105` has it right: "The first four are computable from a
return series alone... The last five require trade-level records, so they depend
on Stage 3." Its first four are Drawdown, CAGR, Sharpe and Sortino. (Its reason
for grouping `Benchmark Comparison` with the trade-level metrics is loose — that
one needs a second *series*, not trades — but on the three that decide this ADR
it is correct and HANDOFF is not.)

**The consequence is that the honest Stage 1 slice against a return series is
CAGR, volatility, Sharpe and Sortino — four metrics, not the wider set the brief
implies.** That is smaller because the brief was wrong, not because scope was
cut. Rule 11 records what is excluded and why.

---

## Decision

**1. No convention is defaulted. Every parameter the document leaves open is a
required argument.** `sharpe_ratio` takes `risk_free_rate` with no default;
`sortino_ratio` takes `target_return` with no default; every annualized figure
takes `periods_per_year` with no default. ADR-005 rule 4 refused to default
`confidence` to 0.5 because a fabricated figure is indistinguishable from a real
one. A Sharpe silently computed at a risk-free rate of zero is the same defect
wearing a number: at a promotion gate it looks exactly like a rate somebody
chose.

**2. The convention travels with the number, inside the integrity hash.** A
Sharpe of 1.4 computed at `rf = 0.00` and a Sharpe of 1.4 computed at
`rf = 0.04` are two different claims about two different strategies. Every
parameter that entered a computation is recorded in the artifact's `content`,
which is already covered by the signature — `framework/artifacts/integrity.py:55`
is the line that puts it in the payload, confirmed by a second reader.
A number whose assumptions can be edited after signing is not evidence, which is
the reasoning ADR-005 applied to `confidence` and ADR-010 rule 8 to `deliverable`.

**3. Returns are simple period returns; growth is geometric.**
`r_t = P_t / P_(t-1) - 1`, and CAGR compounds them:
`(prod(1 + r_t)) ** (periods_per_year / n) - 1`. Log returns are not used.
`Validation/Backtesting.md:15` asks for a *Compound* Annual Growth Rate, and the
arithmetic mean of log returns is not the compound growth rate — carrying both
conventions would let two Belay components disagree about what a return is.

**4. Volatility is the sample standard deviation, `n - 1`, annualized by
`sqrt(periods_per_year)`.** A backtest series is a sample of a process, not the
population of it: the population is every return the strategy will ever produce,
most of which has not happened. `n - 1` is the estimator that does not understate
dispersion — and understating dispersion inflates every risk-adjusted number
computed from it, in the direction that flatters a strategy. Where two
conventions are both defensible, Belay takes the one that cannot flatter.

**5. A series shorter than two observations is refused, not answered.** One
observation has no dispersion, and returning `0.0` would report a strategy with
no variance rather than a series that cannot answer the question. This is the
refusal `max_drawdown` already makes for an empty series
(`framework/metrics/drawdown.py:36-39`) and for the same stated reason: unusable
input must not reach a promotion gate looking like evidence.

**6. Sharpe is the annualized mean excess return over annualized volatility.**
`mean(r_t - rf_period) * periods_per_year / (stdev(r_t) * sqrt(periods_per_year))`.
The risk-free rate is supplied as an **annual** rate and divided by
`periods_per_year` inside the function, because that is how a risk-free rate is
quoted everywhere and demanding a per-period rate invites a silent
factor-of-252 error that nothing would catch.

Recorded as a choice rather than a fact: **this is not `(CAGR - rf) / volatility`**.
The two differ whenever returns are volatile, because compounding is not linear.
The arithmetic form is used because its numerator and denominator are computed
from the same sample in the same way.

**7. Sortino divides by downside deviation about the target, over the full
sample.** Deviations are `max(0, target_period - r_t)`, squared, summed, and
divided by `n - 1` **over the whole series** — not by the count of below-target
periods. Dividing by the below-target count shrinks the denominator along with
the numerator, so a strategy with one bad period in a hundred scores like one
with fifty. Both conventions are in use, the choice is invisible in the result,
and this is the one that stays comparable across series.

**8. Sortino's target is the target in both places.** The numerator is the mean
return in excess of the same `target_return` that defines the downside, not in
excess of a risk-free rate. Mixing the two produces a number that is neither a
Sortino ratio nor a Sharpe ratio and is labelled as one of them.

**9. The four disclosures are mandatory on a metric artifact, and a blank one is
refused.** `Validation/Backtesting.md:35-43`: "Backtests must document —
Assumptions, Data Source, Sample Period, Known Limitations." That is a
requirement, and this repository's recurring defect is a requirement nothing
enforces. They are recorded in `content` under fixed keys, covered by the
signature under rule 2, and a metric artifact cannot be emitted with any of the
four empty.

**10. The disclosures are NOT added to `EvidenceRecord`.** Two reasons, one hard
and one structural.

Hard: `EvidenceRecord.canonical_payload` is pinned by a literal digest at
`tests/artifacts/test_evidence_hashing.py:18`, whose comment states the rule —
"If this value moves, historical evidence stopped verifying." Adding fields to
that payload moves every evidence hash ever computed, and
`Knowledge/Versioning.md:25` forbids rewriting history. An evidence record that
stops verifying is worse than one missing a field.

Structural: the four describe **the run**, not one record of it. A backtest
carrying three evidence records has one sample period, and putting it on each
record puts the same fact in three places where they can disagree.

**11. `Win Rate`, `Exposure`, `Trade Count`, `Benchmark Comparison` and `Tail
Events` are out of scope, and stay out.** Not by preference. `Trade Count` and
`Exposure` need an input a return series does not carry; `Win Rate` needs a
ruling on what a win counts; `Benchmark Comparison` needs a second series; `Tail
Events` needs a threshold no document states. Building any of them today means
inventing the missing input, which is the failure this ADR exists to prevent.

**12. Every metric artifact carries `deliverable = BACKTEST_REPORTS`.** ADR-010
rule 2 gave artifacts a subtype and metric artifacts are the case it was built
for: without it a drawdown, a Sharpe and a universe report are three
indistinguishable `REPORT`s. `Backtest Reports` resolves to `ArtifactType.REPORT`
and `REPORT` has the `RPT` prefix — **checked by running it, not read off the
table**, so the open `PORTFOLIO`/`FAILURE` identifier finding does not bite here.

**13. `framework/metrics/drawdown.py` is brought onto this ruling, not left
beside it.** It predates ADR-010 and this ADR, so it carries no `deliverable` and
none of the four disclosures. `AGENTS.md` forbids parallel implementations, and
the only worked example being the one example that does not follow the rules is
how a convention dies in a repository this size.

---

## Consequences

Positive:

- four of the nine minimum metrics become computable, and `Risk-adjusted returns`
  — one of the constitutional seven — gets a component behind it for the first
  time. The dashboard moves 1 of 7 to 2 of 7
- every metric number carries the assumptions that produced it, signed, so a
  review reads a claim rather than a figure
- `Validation/Backtesting.md`'s documentation requirement becomes executable
  rather than aspirational, which is the difference between the constitution
  being obeyed and being quoted
- two wrong claims in `docs/HANDOFF.md` are corrected in the record instead of
  being carried into the code that implements them

Negative:

- every metric function has more required arguments than its textbook form, and
  no Sharpe can be computed without somebody deciding a risk-free rate. That is
  the intent and it will read as friction
- rule 6 picks one of two defensible Sharpe formulations. A future session
  comparing a Belay Sharpe against an externally quoted one may find a small
  difference and has to check which form the other used
- rule 9 admits no draft exemption, so an exploratory number cannot be emitted as
  an artifact without four sentences of prose behind it
- the disclosures are free text in `content`. Nothing checks that a `Sample
  Period` string denotes a period, only that it is not empty. A stronger type is
  possible later and is not attempted here
- rule 13 changes the integrity hash of every drawdown artifact. Nothing has been
  stored, so nothing breaks today — but this is the last moment at which that is
  true, and the ADR is deliberately taking it now rather than later

---

## Rejected Alternatives

**Defaulting the risk-free rate to zero, and saying so in a docstring.**

Reason: it is the most common convention in the industry and it would be
defensible. But a docstring is not the artifact, and the artifact is what a
promotion gate reads. A zero rate silently applied is indistinguishable, at the
gate, from a rate somebody chose — which is the exact shape ADR-005 rule 4
refused for `confidence`.

**Deriving `periods_per_year` from the series length, or from timestamps.**

Reason: a bare return series has no timestamps, and inferring "252 observations
means daily" is a guess that is wrong for every strategy with under a year of
history. The market data boundary that would carry real timestamps is Stage 2 and
does not exist. Guessing the frequency would make the annualization silently
wrong rather than absent.

**Adding `assumptions`, `sample_period` and `known_limitations` to
`EvidenceRecord`.**

Reason: rule 10. It moves a pinned hash that the test guarding it says must never
move, and it puts run-level facts onto record-level objects.

**Building `Win Rate` as the fraction of positive periods.**

Reason: it is one of two readings of a word the document leaves undefined.
Choosing quietly between two readings is exactly how the five-way
promotion-criteria divergence happened, and it needs its own ruling.

**Waiting for the market data boundary so the disclosures can be filled
automatically.**

Reason: it inverts the dependency. The disclosure block is what makes a
hand-supplied series **honest** — "supplied by hand, carries no provenance" is a
Known Limitation, and recording it on every artifact matters more before Stage 2
than after.

---

## Required Follow-Up (ADR-011)

- `framework/metrics/returns.py` — period returns from a price series, and CAGR
- `framework/metrics/volatility.py` — sample standard deviation and annualization
- `framework/metrics/risk_adjusted.py` — Sharpe and Sortino. **The path is not
  cosmetic**: `scripts/status.py:50` names exactly that file as the expected
  component for `Risk-adjusted returns`. (Drafted as line 52, which is
  `Regime robustness`. Corrected by the verification pass.)
- one shared helper that builds a metric artifact and refuses a blank disclosure,
  so rule 9 is enforced in a single place rather than remembered in four
- `framework/metrics/drawdown.py` migrated onto that helper — rule 13
- tests written first and run against the unchanged code to prove they fail
- **nothing to change in `scripts/status.py`.** `PROMOTION_CRITERIA` already names
  `framework/metrics/risk_adjusted.py`, and
  `test_promotion_criteria_match_the_constitution` holds the criterion *names* to
  `Promotion_Pipeline.md`, not the paths. The figure moves on its own when the
  file lands
- **`framework/metrics/statistics.py` is deliberately NOT created**, and this is a
  ruling rather than an omission. It is what the dashboard expects for
  `Statistical performance`, and `implementation_state()` grades a file `built` on
  twenty non-blank lines with no view of what is inside them. Putting CAGR there
  would turn a criterion green that nothing satisfies — statistical performance is
  significance and sample adequacy, not a growth rate. `scripts/status.py`'s own
  docstring says it exists to prevent "a reassuring half-truth", and this would be
  one
- correct the two claims in `docs/HANDOFF.md` identified above

---

### Still open, deliberately

**What a `Win Rate` counts.** Periods or trades. The trade reading needs Stage 3
either way, but the ruling can be made before it.

**`Tail Events`' threshold.** Worst *k*, beyond *n* standard deviations, or a
quantile. The document names the metric; no document names the cut.

**Whether the disclosure block belongs to the metric or to the backtest.** Rule 9
puts it on the metric artifact because that is the only artifact that exists.
When Stage 3 emits a backtest producing several metrics at once, the four may
belong on the backtest with the metrics inheriting them.

---

## ADR-012: Statistical Review — Significance, Sample Adequacy, And What Belay Refuses To Conclude

Status:
**Accepted.** Ratified 2026-07-31 as drafted; no rule was amended on
ratification. Implemented the same day — `framework/metrics/statistics.py`,
carrying the Student's t distribution, the significance test, and rule 8's
sample-adequacy calculation.

Every citation was re-checked against the files by a second reader before
implementation, the practice that caught four wrong citations in ADR-011 a few
hours earlier. Any correction is marked inline below.

Date:
2026-07-31

---

## Context

**Seven documents demand statistical validity. Not one of them defines it.**

| Document | What it says |
|---|---|
| `constitution/Promotion_Pipeline.md:27` | maturity Level 2, `Validated`, **is** "Passed statistical review." |
| `constitution/Promotion_Pipeline.md:75` | `Statistical performance` — first of the seven authoritative criteria |
| `constitution/Capital_Authority.md:11-14` | "Capital shall be determined using: ... `Statistical edge`" |
| `Validation/README.md:23` | "Evaluate statistical significance." — a departmental responsibility |
| `Validation/Workflow.md:15` | `Statistical Review`, a step between Backtesting and Capital Review |
| `strategies/PromotionCriteria.md:7` | `Statistical Performance` heads its eight categories |
| `constitution/Mission.md:16` | "Discover statistically valid investment opportunities." |

Two of those are unusually load-bearing. `Promotion_Pipeline.md:27` defines a
maturity level **as** the passing of this test — the only one of the seven levels
defined that way. And `Capital_Authority.md:11-14` makes `Statistical edge` one
of six inputs that *determine capital*, so the number this ADR rules is not
merely reported to a review: it sizes positions.

**All 101 markdown files in the repository were searched for the vocabulary that
would define any of it.** `p-value`, `confidence interval`, `sample size`,
`t-test`, `hypothesis test`, `null hypothesis`, `significance level`, `degrees of
freedom`, `out-of-sample` and `overfit` return **exactly one hit outside this
ADR's own text, and it is not a definition**: `docs/ROADMAP.md:72`, a sentence
added earlier the same day observing that Belay computes none of this.

> **This paragraph was drafted wrong and is corrected here, not silently.** It
> claimed three hits, "two of them the version string `v1.0.0-alpha`". The
> version string contains none of the ten terms enumerated above — `alpha` on its
> own is not one of them — so the count could only have been reached by a search
> whose terms differed from the list the sentence gives. **That is precisely the
> defect ADR-011 recorded a few hours earlier**, where a bullet claimed
> `risk-free` appeared in no document while sitting inside an ADR containing it
> seventeen times. Two ADRs in one day, the same error: a search was run, its
> terms were then written down from memory, and the two drifted. The lesson is
> narrower and more useful than "check citations" — **paste the query, do not
> paraphrase it.**

So this is ADR-011's situation with the stakes raised. ADR-011's metrics
*describe* a series. This one draws a **conclusion** from one, and
`Capital_Authority.md` routes that conclusion into position sizing.

### Two Immutable Laws bear on this directly

**Law IV — "Past performance is evidence. It is never proof."**
(`constitution/Immutable_Laws.md:29-33`.) That is a precise statement of what a
significance test does and does not establish, and it is therefore a constraint
on what this module is allowed to say. A p-value is the formalisation of Law IV;
a pass/fail verdict presented without one is its violation.

**Law II — "Every investment decision must be explainable. Black-box reasoning
is prohibited."** (`constitution/Immutable_Laws.md:13-17`.) This constrains the
*implementation*, not only the output. It is the reason rule 5 rejects a
dependency in favour of code a reviewer can check against a printed table.

---

## Decision

**1. The question is "is this distinguishable from luck", never "is this good".**
The module computes the probability of observing a track record at least this
strong if the strategy had no edge whatsoever. It does not score a strategy, and
it does not rank one against another.

**2. The null hypothesis is supplied, never assumed.** `null_return` is a
required argument with no default. Testing against zero is the conventional
choice and it is still a choice: a strategy that beats zero but not the
risk-free rate has no edge worth capital, and `Capital_Authority.md` makes that
distinction load-bearing. ADR-011 rule 1, applied to a second silent convention.

**3. Alpha is supplied, never defaulted.** No Belay document states a
significance level. 0.05 is convention, and strategy selection is precisely the
setting where convention is argued to be far too loose — many candidates are
screened, and the loosest defensible threshold is the one that lets the most
luck through. Belay does not pick a number nobody wrote down.

**4. The test is a two-sided one-sample Student's t-test on the mean period
return, with n-1 degrees of freedom.** Two-sided rather than one-sided: a
one-sided test encodes the assumption that the edge is positive, which is the
assumption under examination, and it halves the p-value for free.
`Validation/README.md:11` — "Validation seeks flaws."

**5. The t-distribution is implemented in this repository, not imported.**
`scipy` is neither installed nor declared in `pyproject.toml`; adding it for one
function is a large dependency for a small need. The regularized incomplete beta
is about thirty-five lines of standard numerical code, and it is pinned in tests
against **published t-table critical values** rather than against another
implementation — a number a reviewer can check by opening a textbook is
explainable in the sense Law II means; one produced by an opaque dependency is
not. Verified before this ADR was written: the implementation reproduces the
published two-sided critical values at df 10, 20, 30 and the normal limit to five
decimal places.

**6. `numpy` is not adopted either.** Same reasoning, plus one more: it is
present today only as a transitive dependency of `pandas` and appears nowhere in
`pyproject.toml`. Building on a package nobody declared is the 2026-07-26 defect
in the other direction — there, `pyyaml` was declared but not installed, and
`ArtifactRepository.save()` had never once executed while the suite reported 46
passing.

**7. The parametric assumptions are recorded on every artifact as Known
Limitations, never buried.** The t-test assumes returns are independent and
identically distributed. Financial returns are neither — they are
autocorrelated, heteroskedastic, and fatter-tailed than the t distribution
allows. **The consequence has a direction and must be stated: a p-value computed
on real returns is optimistic. It understates the probability that a track
record is luck.** ADR-011 rule 9 already makes the four disclosures mandatory;
this rule fixes what the `assumptions` and `known_limitations` strings must say
for a significance artifact, so it is impossible to emit one that does not admit
this.

**8. Sample adequacy is a separate question with its own answer.** "Is this
significant?" and "is this sample large enough to conclude anything?" are
different questions, and a short sample can return a significant p-value by
chance. `minimum_observations_for_significance` answers the second directly:
given the observed effect size, how many observations would be needed to reach
the stated alpha. **A sample below that number has not failed the test — it has
not taken it**, and reporting those two states identically is the failure this
rule exists to prevent.

**9. Fewer than two observations computes nothing.** ADR-011 rule 5 extended: a
standard error needs at least two observations, and a t-statistic on one is
undefined rather than zero.

**10. Multiple-testing and data-snooping corrections are deliberately out of
scope.** Deflated Sharpe, Bonferroni and White's Reality Check all require the
number of strategies that were tried, and **Belay records that nowhere** —
`strategies/Registry.md` is a stub and the experiment queue is unbuilt.
Correcting against an unknown trial count produces a number that looks adjusted
and is not, which is worse than an unadjusted number that says so. Rule 7's
disclosure names it explicitly.

**11. The module reports whether the caller's threshold was met. It does not
decide promotion.** `significant` is `p < alpha` and nothing further.
`Promotion_Pipeline.md:27` makes "Passed statistical review" a maturity level and
it is tempting to write that gate here — but a gate is a governance decision.
ADR-009 rule 5 drew this exact line for review outcomes, and the same line holds:
comparing a computed number to a declared threshold is not deciding what follows
from it. Promotion remains a review outcome recorded through
`framework/artifacts/review.py`.

**12. The artifact is a `Validation Report`, not a `Backtest Report`.**
`Validation/README.md:37` declares `Validation Reports` among the department's
outputs, and `Validation/Workflow.md:15` places Statistical Review as a step
distinct from Backtesting. `DeliverableType.VALIDATION_REPORTS` already exists
and maps to `ArtifactType.REPORT`, so no enum member is added and ADR-010's
vocabulary is untouched.

**13. ADR-011's scope watcher has a false positive, and this ADR fixes it.**
`test_only_the_backtest_metrics_adr_011_scopes_in_are_built` tokenises `Tail
Events` as the substring `tail`. A two-sided test is naturally implemented as a
function with `two_tailed` in its name, which would make that watcher report
`Tail Events` as built — **one day after the watcher was written, by the very
next piece of work.** The token is tightened to `tail_event`. A watcher that
reports a gap as closed when it is open is the "reassuring half-truth"
`scripts/status.py` exists to prevent, and it is worse than no watcher.

---

## Consequences

Positive:

- `Statistical performance` — the **first** of the seven constitutional criteria
  — becomes computable. The dashboard moves to 3 of 7, honestly this time
- `Promotion_Pipeline.md:27`'s "Passed statistical review" becomes something that
  can be evaluated rather than asserted, which is what a maturity level defined
  by a test requires
- Law IV becomes operational rather than aspirational: the module's entire output
  is a statement about evidence rather than proof, and rule 7 forces the caveat
  onto every artifact that carries the number
- no new runtime dependency, and rule 5's implementation is checkable against a
  printed table by anyone who doubts it

Negative:

- Belay now maintains about thirty-five lines of numerical code. Pinning against
  published tables rather than another implementation mitigates it; it does not
  make it free
- **the t-test is the weakest defensible test for this purpose.** It ignores
  autocorrelation, fat tails and multiple testing, every one of which makes it
  optimistic. Rule 7 discloses this and does not fix it, which is the honest
  arrangement but leaves a real bias in place
- rule 10 leaves the largest known bias in strategy evaluation unaddressed. A
  strategy that survived a hundred variations before passing at p = 0.04 has
  demonstrated nothing, and Belay currently cannot tell that from a single
  pre-registered test
- rules 2 and 3 make the function harder to call than any textbook version.
  Deliberate, and it will read as friction exactly as ADR-011's did

---

## Rejected Alternatives

**Defaulting alpha to 0.05.**

Reason: the same objection ADR-011 raised to a silently-zero risk-free rate. It
is convention rather than doctrine, and this is the setting where a selection
process should be *stricter* than convention rather than equal to it. A default
would also be indistinguishable, at a promotion gate, from a threshold somebody
chose.

**A one-sided test.**

Reason: it assumes the sign of the edge, which is the thing under examination,
and it halves the p-value at no cost. `Validation/README.md:11` says Validation
seeks flaws; a test tuned to find fewer of them is the wrong instrument for the
department that owns it.

**Adding `scipy`.**

Reason: rule 5. A large dependency for one function, and a less explainable one
than thirty-five lines pinned to a published table. Law II is about
explainability, and "the library said so" is the answer it prohibits.

**Using the normal distribution instead of Student's t.**

Reason: `statistics.NormalDist` is in the standard library and would have cost
nothing — and it is wrong precisely where this ADR cares most. At small n the
normal approximation understates the p-value enough to change a conclusion, and
the whole sample-adequacy half of this ruling is about small samples.

**Computing the 0-100 Promotion Score.**

Reason: ADR-006 rule 4 suspended it — no weights, no mapping, threshold deferred
to the Investment Committee. Reviving it as a side effect of a statistics module
is exactly the failure ADR-004 named and ADR-009 and ADR-010 each refused.

**Writing the "Passed statistical review" gate.**

Reason: rule 11. The arithmetic belongs here; the decision does not.

---

## Required Follow-Up (ADR-012)

- `framework/metrics/statistics.py` — standard error, t-statistic, two-sided
  p-value, confidence interval, and rule 8's minimum-observations calculation
- the Student's t distribution, pinned in tests against **published critical
  values** at several degrees of freedom including the normal limit, never
  against another implementation
- `significance_artifact`, emitting a `Validation Report` through ADR-011's
  `metric_artifact` so the disclosure rules apply unchanged
- rule 7's fixed assumption and limitation strings, so the i.i.d. caveat cannot
  be omitted from an artifact
- rule 13: tighten the ADR-011 watcher's `Tail Events` token to `tail_event`
- tests written first and run against the unchanged code
- `docs/HANDOFF.md`, `docs/ROADMAP.md` and the dashboard

---

### Still open, deliberately

**Multiple-testing correction.** Rule 10. It needs a trial count Belay does not
record, and it becomes possible when the experiment queue or a real strategy
registry exists. Until then the disclosure is the whole of the answer.

**Whether the null should be zero or the risk-free rate as a matter of
doctrine.** Rule 2 makes the caller state it. Which one a *promotion review*
must use is a governance question about what "edge" means, and it belongs with
whoever rules on `Capital_Authority.md`'s six inputs.

**What minimum sample Belay requires.** Rule 8 computes how many observations an
observed effect would need. No document says how many Belay *demands* before a
strategy may be promoted, and `Promotion_Pipeline.md:27` makes that a real gap:
a maturity level is defined by passing a review whose sample requirement nobody
has written down.

---

## ADR-013: The Data Boundary — Provenance, Two Contracts, And What A Fetched Series Is

Status:
**Accepted and implemented.** Ratified 2026-07-31 by the repository owner, **as
corrected** — no rule was amended on ratification. **Implemented 2026-08-01 in
all ten rules**, as ROADMAP Stage 2; see the Required Follow-Up below for what
that pass established, closed and opened.

> **This block read "Not implemented" for one commit after implementation
> landed**, so the ADR contradicted its own Required Follow-Up inside a single
> file — one commit after `0a6d5f7`, whose entire subject was closing two stale
> ADR-013 statuses found by a close-out sweep. Caught by the implementation's
> independent verification pass, which is the third consecutive pass on this ADR
> to find something the author's own reading did not.

**Ratified after two verification passes, not one**, and the corrections the
second pass forced were material rather than cosmetic — rule 6's premise was
unrecorded anywhere in the repository until it was fixed. **Read the scorecard
below before building on any rule here.**

Every citation was read in the drafting session rather than carried from
`docs/EndState.md` or `docs/HANDOFF.md`; where a claim in either did not survive
being opened, it is corrected inline and marked. **Two claims in this ADR's own
first draft did not survive either, and are marked the same way.**

**Two passes ran on this draft, and the second one is the reason to trust the
first one less.**

**The author's pass found one defect** — rule 2 cited a law by the wrong number
while its line number was right, which made the draft contradict its own Rejected
Alternatives. Corrected inline and marked.

**An independent pass then ran with no knowledge of the drafting, and found three
more defects and six imprecisions across 71 distinct claims.** All three defects
are corrected and marked inline below. They were:

- **rule 6 rested on a premise no file in this repository contained.** The owner's
  answer that Belay trades equities and options was given but never written down,
  and this ADR cited `docs/OwnerDecisions.md` for it. The fact was asserted in
  three files all written in one commit, each pointing at the others. **Fixed at
  the root:** `docs/OwnerDecisions.md` Part 4 question 5 now records it.
- **"five of eight" was a miscount; there are ten rules**, and it had already
  propagated into `docs/ROADMAP.md`, `CHANGELOG.md` and a commit subject.
- **rule 7's supporting bullet was carried near-verbatim from `docs/EndState.md`
  and re-attributed** — the exact thing the sentence below claims this draft did
  not do.

**The honest scorecard, with the denominator this block originally lacked: 71
claims checked, 11 wrong or questionable — 4 defect-grade. The author's own pass
caught 1 of the 4.** The earlier version of this block claimed "twenty-two
citations checked, one wrong", a figure that could not be reproduced under any
counting rule and that flattered the draft using a denominator nobody could audit.
Reporting a good error rate against a made-up denominator is the shape ADR-012
rule 10 refuses — a number that looks adjusted and is not.

For comparison, and stated more carefully than the earlier version did:
`docs/HANDOFF.md` records four wrong citations in ADR-011's first draft, of which
**one** was self-refuting, and one wrong in twenty for ADR-012. The earlier text
here called both "self-refuting", which overstates ADR-011's record.

**The verification practice, not the draft, is what this record vindicates.**

Date:
2026-07-31

---

## Context

ROADMAP Stage 2's entire deliverable is *"A defined boundary for obtaining a
price series, with provenance recorded on the resulting evidence"*
(`docs/ROADMAP.md`, Stage 2). **A boundary is an adapter contract**, so Stage 2
cannot be built without answering what shape the thing behind it has and whether
there can be more than one. **ADR-011's central holding, extended rather than
applied**, makes avoiding the question uncomfortable: a single hard-coded fetcher
does not dodge the ruling, it *makes* it — silently — that there is only ever one
source, and that its properties are whatever they happen to be.

> **Named as an extension by the independent pass, and the distinction is one this
> repository has recorded three times.** ADR-011 rules that *metric conventions*
> are never defaulted — a risk-free rate, a target return, a period count. Source
> multiplicity is not a metric parameter, so this is reasoning by analogy from an
> existing ruling rather than the ruling applying on its own terms.
> `docs/EndState.md` calls extending a document rather than applying one "the
> failure this repository has now recorded three times", so the analogy is kept
> and labelled instead of being dressed as precedent. **Rule 2 does not depend on
> it** — Law VI carries that ruling alone.

Everything Belay has computed to date was fed in by hand. Stage 2 is what makes
that sentence false.

> **A stronger claim was removed here rather than softened.** This read "and every
> artifact says so inside its own signature." The independent pass showed it is
> not true in two ways: **no artifacts are stored anywhere** (rule 7 relies on the
> same fact), and the "supplied by hand" wording exists only as a caller-supplied
> string in five test modules. `framework/metrics/reporting.py` requires
> `data_source` to be non-blank and requires nothing about what it says.
> Inherited from `docs/HANDOFF.md`, which overstates it the same way.

**Four facts settled since `docs/EndState.md` was written**, recorded in
`docs/OwnerDecisions.md`, all of which this ADR is drafted against:

- Belay trades **equities and options, depending on the strategy**.
- Positions are held **days to months**, decided once a day on **daily bars**.
- The market-data budget is **effectively zero** to start.
- **The repository is private**, verified. Committing a fetched series is no
  longer publication, so row 13 becomes a design question rather than a bar.

  > **Note added 2026-09-20, outside the ADR.** The bullet above is reproduced
  > exactly as ratified. Its premise no longer holds: Belay is to be public, so
  > committing a fetched series would be publication again. The ADR is not
  > amended — only the owner may do that — see `docs/OwnerDecisions.md` 14h.

### What the governing documents require

Read in full for this ADR rather than quoted from a prior document:

- **`Validation/Backtesting.md:35-43`** — "Backtests must document / Assumptions
  / Data Source / Sample Period / Known Limitations", closing at `:47` with
  "Outputs become evidence."
- **`constitution/Immutable_Laws.md:45`** (Law VI) — "Research and execution
  remain independent."
- **`constitution/Immutable_Laws.md:51`** (Law VII) — "Institutional knowledge
  shall never be intentionally discarded."
- **`constitution/Operational_Constraints.md:5`** — "Belay shall maintain
  accurate records."
- **`constitution/Operational_Constraints.md:9-17`** — "Belay shall distinguish:
  Facts / Assumptions / Predictions / Opinions."
- **`constitution/Operational_Constraints.md:25-27`** — "Belay shall remain
  strategy-agnostic. No asset class, security, or investment methodology
  possesses inherent preference."
- **`constitution/Operational_Constraints.md:29`** — "Tradable universes must be
  discovered through evidence."
- **`Knowledge/Versioning.md:23-27`** — "Knowledge records every version. No
  version is overwritten. Historical versions remain searchable."
- **`Research/UniverseDiscovery.md:7`**, **`:17`** "Evaluate option market
  quality", **`:25`** "Evaluate survivability."
- **ADR-002 Decision** — "Mechanics emit Artifacts. Governance consumes
  Artifacts. Neither layer reaches across the boundary by any other means."

### Three things found by reading that no prior document records

**1. `constitution/Operational_Constraints.md:29` makes the survivorship
argument constitutional rather than departmental.** `docs/EndState.md` rested it
on `Research/UniverseDiscovery.md:7`, a departmental document. The identical
sentence — "Tradable universes must be discovered through evidence" — is in the
constitution, and `constitution/Governance.md:7` reads, in full, "The Constitution
possesses authority." **The argument was stronger than the document making it
knew.**

> The scope gloss "authority over everything" was removed by the independent
> pass. Line 7 does not say "over everything" — that reading comes from line 5,
> "Departments possess responsibility", sitting beside it. Defensible, and it was
> presented as what the line says. ADR-006 rule 1 cites the same line correctly,
> pairing it with Immutable Law X to rank the constitution above departmental
> documents, which is the argument this sentence was reaching for.

**2. `constitution/Operational_Constraints.md:25-27` decides the
equities-versus-options question, and it decides it against an equities-only
boundary.** "No asset class, security, or investment methodology possesses
inherent preference." A contract that can only express an equity price series
does not merely *omit* options — it gives equities inherent preference by
construction, because a strategy needing option data could not be expressed at
all. This line has never been cited in any ADR.

**3. `constitution/Evidence_Standards.md` has no class for observed market data.**
Its four levels — A live-validated, B paper-validated, C historical *simulation*,
D hypothesis — are each a statement about how well a **strategy** has been
tested. A fetched price is none of them; nothing was simulated. Grading it C
because C is nearest would be exactly the unstated convention ADR-011 refuses.
**The constitution has the right vocabulary elsewhere:**
`Operational_Constraints.md:9-17` distinguishes Facts from Assumptions,
Predictions and Opinions, and a price observation is a Fact in that sense.

### Two claims in prior documents that did not survive being opened

**`docs/EndState.md` Part 5 lists five things this ADR must settle. It is five of
ten.** The five it does not name are the identity question (rule 3), the
instrument-shape question (rule 6), the evidence-grade question (rule 8), the
refusal of an unstating source (rule 9) and the `Market Snapshot` exclusion
(rule 10). None was visible without opening `Knowledge/Identifiers.md`,
`framework/artifacts/enums.py` and `constitution/Evidence_Standards.md` together,
which is the pass this ADR ran and that document did not.

> **Corrected by the independent verification pass. This read "five of eight" and
> named three.** The Decision section has ten numbered rules; 5 + 3 left rules 9
> and 10 unaccounted for, and both are substantive — rule 9 adds a
> construction-time refusal rule 5 does not require, and rule 10 excludes a
> specific `DeliverableType`. **The miscount had already propagated into
> `docs/ROADMAP.md`, `CHANGELOG.md` and a commit subject before it was caught**,
> which is the same shape as the `Knowledge/Schema.md` miscount of 2026-07-30 that
> reached a test docstring. Counted by listing the numbered headings, not by
> re-reading the sentence.

**The sixth item `docs/HANDOFF.md` added — where the halt lives — is removed from
this ADR deliberately.** It was added earlier the same day and it is wrong to
keep. Rule 2 holds that market data and execution are two contracts because
designing the dangerous one in the language of the safe one is how the vocabulary
for danger goes missing. Ruling an execution-safety property inside a
data-boundary ADR would commit that error inside the document ruling against it.
Finding 11 stays open for a Stage 6/7 ruling.

---

## Decision

**1. Provenance is one obligation and it covers everything that crosses into
Belay from outside.** Every fact Belay did not compute itself arrives with a
recorded source, and that record sits inside the consuming artifact's signature.
This is the one thing that genuinely generalises across market data, a broker and
any future outside party. It is already half-built: `Disclosure.data_source` at
`framework/metrics/reporting.py:125` is enforced non-blank and is inside the
integrity hash.

> **This read `:58` and was correct until the implementation moved it.**
> Implementing rule 7 inserted `SamplePeriod` above `Disclosure`, so `:58-59`
> now fall inside a docstring. Repointed to `:125` and `:132` on 2026-08-01,
> and recorded rather than silently repaired because **an edit invalidating a
> citation in the document it is implementing is a failure mode this repository
> had not previously named** — the citation was accurate when written and was
> broken by work done in obedience to it. `Backtesting.md:39` requires it, `Operational_Constraints.md:5`
requires accurate records, and Law VII requires Belay to keep its own copy rather
than rely on someone else's system to remember.

**2. Market data and execution are two contracts, not one, and no shared base
class joins them.** Three independent reasons, the third constitutional:

- **Direction, and the cost of being wrong.** Market data is a read. An execution
  adapter writes to the world and the write moves money irreversibly. An
  interface designed for reads has no vocabulary for idempotency, partial fills,
  cancel-in-flight, or a halt path.
- **Opposite failure policies.** Retrying is *how* a data fetch recovers from a
  dropped connection. A retried order submit doubles a position. A shared base
  class must pick one default and be wrong for the other.
- **Law VI at `Immutable_Laws.md:45`** — "Research and execution remain
  independent." Market data feeds research; the broker *is* execution. A shared
  abstraction is a shared dependency across a boundary the constitution declares
  independent.

  > **Corrected during this ADR's own verification pass, marked rather than
  > quietly rewritten.** The draft read "Law VII at `Immutable_Laws.md:45`". The
  > line number is right and the law number was wrong — `Immutable_Laws.md:43` is
  > `## Law VI`; Law VII is at `:49-51` and is the retention law rule 1 rests on.
  > **The draft therefore cited two different laws by one name and contradicted
  > its own Rejected Alternatives section**, which had it right. Third ADR
  > running in which the verification pass caught a citation defect in a draft
  > written by someone who had opened every file.

Note what rules 1 and 2 do together: **the obligation is shared and the contract
is not.** "A swappable adapter" is two decisions wearing one name.

**3. A fetched series is not an Artifact. The fetch record is, and it carries the
series' fingerprint rather than its contents.**

This is the structural ruling, and it is forced by the existing vocabulary rather
than chosen. `Knowledge/Identifiers.md:27-57` defines eight prefixes — STRAT,
EXP, RS, REV, RPT, REGIME, WF, DOC — and **none names market data**.
`ArtifactType` carries nine members and none names it either. A price series has
no honest identity under the vocabulary Belay has, and manufacturing one means
editing `Knowledge/`, which widens the open finding that those two vocabularies
already disagree (`docs/HANDOFF.md` finding 4).

The resolution is to notice that **the data is an input, not evidence.** What Law
VII requires Belay to retain is the knowledge of *what was obtained, from where,
when, covering what, and what it cannot be trusted to mean* — a record, not a
table of numbers. So:

- The fetch record is an `Artifact` of type `REPORT`, which holds the `RPT`
  prefix. ADR-010's principle applies unchanged: the type describes what the
  artifact **is**, and this one reports what was obtained.
- It carries **`deliverable = None`**. Verified by opening
  `framework/artifacts/artifact.py:29-36`, whose comment already states the
  needed meaning — *"None means 'not a documented deliverable' — a real state,
  not an unset field."* No governance document declares a data fetch among any
  department's deliverables, and ADR-010 rule 4 scopes that vocabulary to what
  the documents declare. **No enum member is added and ADR-010 is untouched.**
- It carries a **content hash of the bytes returned**, inside the integrity hash.

The hash is what makes the arrangement work. Reproducibility becomes checkable
rather than asserted — re-fetch, hash, compare. And if the data store is lost,
the artifacts still record what was fetched and what it hashed to, which is the
institutional knowledge Law VII protects as distinct from the bytes.

**4. The series is stored, versioned, never overwritten — and kept out of git.**

`Knowledge/Versioning.md:23-27` is load-bearing here and has never been cited for
it. **Data vendors restate history.** Splits, dividend adjustments and corrected
prints mean the same ticker over the same dates can return different numbers next
month. That is normal vendor behaviour, not a fault. Two consequences:

- **A backtest run against a series nobody kept is not reproducible**, and its
  irreproducibility is silent. Law VII and `Versioning.md:25` — "No version is
  overwritten" — therefore require the series to be kept.
- **A re-fetch that differs is a new version, not a correction.** It gets its own
  fetch record and both remain, because `Versioning.md:27` requires historical
  versions to remain searchable, and because *which* restatement a result was
  computed against is part of the result.

**Out of git, and that is a ruling rather than an omission.** Three reasons, the
third deciding:

- Git retains every version of every file permanently by design. A
  daily-refreshed series makes repository growth unbounded with no prunable path,
  and append-only history means the mistake cannot be undone later.
- A vendor licence may restrict retention independently of visibility. Removing
  data from a git history is effectively impossible; removing a directory is not.
- **Rule 3 already covers the integrity requirement.** The artifact carries the
  content hash, so the record of what was fetched is signed and permanent whether
  or not the bytes are under version control. Committing them adds no guarantee
  rule 3 does not already provide.

The store is a versioned directory, and the `.gitignore` entry is the enforcement
rather than a convention someone has to remember.

**5. Survivorship is a Stage 2 acceptance criterion in two halves, and the answer
is a fixed constant on every artifact derived from the source.**

Two different questions, and a source can pass one and fail the other:

- **Delisted prices** — can the source return a history for an instrument that no
  longer trades, if you already know to ask for it?
- **Delisted universe membership** — does the source know which instruments were
  in a universe *on a past date*, as opposed to which are in it today?

**The second is the one that causes the damage**, and
`Research/UniverseDiscovery.md` makes Belay universe-driven by design. So the
criterion is not "does the source have delisted data" but **"can the adapter
answer both questions, and is the answer recorded rather than assumed?"**

**`constitution/Operational_Constraints.md:29` makes this constitutional** — a
universe drawn from a survivor-only source has been selected on the outcome under
prediction, so it was not discovered through evidence in the sense that line
means. `Research/UniverseDiscovery.md:25` requires Belay to "Evaluate
survivability", which cannot be done honestly from a dataset that has already
removed everything which failed to survive.

The disclosure follows ADR-012 rule 7's shape exactly: a **fixed module
constant**, not a caller-supplied string, naming the bias **and its direction**.
The direction is worse than the usual single-sided case — survivorship **inflates
every return measure and deflates drawdown and tail measures simultaneously**, so
it flatters the return and understates the risk in one breath. ADR-012 rule 10
already settled the response to a bias that cannot be corrected: refuse to produce
a number that "looks adjusted and is not", and disclose instead.

**6. The contract expresses equities and options both. Neither gets inherent
preference, and implementation order is not preference.**

`constitution/Operational_Constraints.md:25-27` decides it: "No asset class,
security, or investment methodology possesses inherent preference." **A contract
that can only express an equity price series gives equities inherent preference by
construction**, because a strategy needing option data could not be expressed at
all.

**They are two shapes, not one shape with a flag.** A price series is one
instrument over time. An option chain is, for each date and underlying, many
contracts each with a strike, an expiry, a right, and its own quotes and open
interest. One is a sequence; the other is a sequence of sets.

**And survivorship means something different for an option, which is the part
most likely to be got wrong.** An option **expires by design** — its
disappearance is the instrument working correctly, not an instrument failing. So
the two halves restate rather than transfer:

- Does the source retain chains for **expired** contracts, or only live ones?
- Does it know the **underlying's** universe membership historically?

The same `Disclosure` machinery records both. **Nothing about rule 5's mechanism
changes; only the questions it asks do.**

Implementation order is equity daily bars first, on cost and coverage rather than
on preference.

> **This paragraph originally read "Free sources do not carry historical option
> chains, so `Research/UniverseDiscovery.md:17`'s 'Evaluate option market quality'
> is unsatisfiable until that is bought." That is false, and it was asserted from
> general knowledge rather than checked** — flagged by the independent
> verification pass as an unsourced external claim, and independently falsified by
> going and looking. It is corrected rather than deleted because **an ADR whose
> rules 5 and 9 forbid a vendor from asserting coverage it has not established
> must not do the same thing itself.**

Checked: **`post-no-preference/options` on DoltHub** is a free, daily-updated,
version-controlled option chain database carrying bids, asks, implied volatilities
and greeks — roughly 2,098 option symbols, 2019 to present, about 6 GB as CSV. So
option data is *reachable* at a zero budget.

**Two properties remain unestablished, and rule 9 governs them exactly as it
governs any vendor:**

- **Whether expired contracts are retained.** This is rule 6's first survivorship
  half, and it is documented nowhere located. An option **expires by design**, so
  a source keeping only live chains is not obviously defective — it is simply
  unusable for a backtest, and the difference must be established rather than
  hoped for.
- **The licence.** DoltHub states most of its data is Creative Commons; that was
  not confirmed for this database, and rule 4's storage ruling depends on it.

**Two facts also constrain what the data can support, and both are disclosures
rather than blockers.** History begins in 2019, which is short: ADR-012 rule 8's
sample-adequacy question decides whether a given effect can be concluded from it,
and that is a per-strategy answer rather than a property of the source. And the
symbol coverage is a subset rather than the market.

**A free path exists for the harder half too.** Point-in-time index membership can
be approximated from a tracking ETF's monthly holdings disclosures, published free
back to 2006. **It is survivorship-*reduced*, not survivorship-free** — the ETF
commits only to holding "at least 90%" of assets in index securities, some
companies drop out for missing price data, and ticker renames are mapped by hand.
**That is a legitimate answer under rule 9 and an honest artifact under ADR-012
rule 10**, where a universe silently built from today's constituents is neither.

**7. `sample_period` becomes two dates, not prose. Now, before any artifact
carrying the prose form is signed.**

`Disclosure.sample_period` at `framework/metrics/reporting.py:132` (`:59` when
this was written — see rule 1's note) was a free-form `str` validated only as
non-blank, so "last five years" satisfied it. Three things now depend on it being
machine-readable:

- **Tax years are calendar-bounded** (`docs/EndState.md:546-547`) **and the
  taxable branch is live** (`docs/OwnerDecisions.md` Part 4 question 2, not row
  6). Deriving a tax year by parsing prose is the defect
  `docs/DocumentStandard.md:42` exists to prevent — "index every document
  deterministically without parsing prose."

  > **Corrected by the independent verification pass, and this one is the
  > embarrassing kind.** The bullet originally attributed both halves to
  > `docs/OwnerDecisions.md` row 6, which contains neither, and was near-verbatim
  > `docs/EndState.md:546-550` — **carried from a prior document and
  > re-attributed, which is precisely what this ADR's Status block claims it did
  > not do.** The claim is true; the sourcing was not. Same class as the Law
  > VI/VII defect, and the reason the Status block's error rate is now stated with
  > a denominator rather than a boast.
- **Rule 4's versioning must compare coverage** between two fetches of the same
  instrument. Two prose strings cannot be compared.
- **Reproducibility.** A backtest that cannot state its exact window cannot be
  re-run.

**The cost of doing this now is zero, and that was verified rather than assumed.**
A search for stored artifacts across the repository returns none, so no signature
exists to break. After Stage 2 signs its first artifact this becomes a migration
of permanent append-only records, which `Versioning.md:25` forbids rewriting.

**8. A fetch record carries no evidence grade, and this changes nothing about
metrics.**

`constitution/Evidence_Standards.md` grades how well a **strategy** has been
tested: live, paper, simulation, hypothesis. A price observation is on none of
those axes, and grading it C — "historical simulation" — would assert that
something was simulated when nothing was.

**The machinery already produces the right answer and needs no change.**
`ArtifactFactory.create` derives `evidence_level` via `strongest_evidence_level`,
which returns `None` for an artifact carrying no `EvidenceRecord`s, and
`framework/artifacts/artifact.py:38-44` states the reasoning — *"an unevidenced
artifact has no grade, and inventing D for it would make 'unevidenced' read as
'hypothesis'."* A fetch record carries no evidence records, so it carries no
grade, and that is honest rather than incomplete.

**Metrics computed from the series stay Level C, exactly as today.** That grade
was always about the simulation, never about the prices. Nothing in
`framework/metrics/` changes.

**No new evidence level is proposed.** `Evidence_Standards.md` is in the frozen
governance layer, and rule 3 means Belay does not need a grade for a thing it has
ruled is not evidence. The gap is recorded as a finding instead of patched.

**9. A source that cannot state its survivorship properties is refused, not
assumed clean.** The adapter requires both answers at construction. "Unknown" is
a legitimate answer and must be *stated* as unknown, which then travels into
`known_limitations` — the same shape as ADR-011 rule 5 and ADR-012 rule 9, where
unusable input is refused rather than answered. A source silently assumed
survivor-free is the failure this rule set exists to prevent, and it fails in the
direction that flatters.

**10. A fetch record is not a `Market Snapshot`.**
`DeliverableType.MARKET_SNAPSHOT` exists and is tempting. It is a daily *workflow*
deliverable describing the state of the market, and a ten-year historical
backfill is not a snapshot of anything. Recorded because the wrong mapping is
easy, cheap to make, and permanent once signed. Rule 3's `deliverable = None` is
the answer.

---

## Consequences

Positive:

- Stage 2 is unblocked, and the thing blocking it is ruled rather than defaulted
- one provenance obligation covers market data, brokers and anything else that
  crosses in, so the generalisation that is real is made once
- the two contracts that must not be merged are kept apart on a constitutional
  ground rather than an aesthetic one
- no new identifier prefix, no new `ArtifactType`, no new `DeliverableType`, no
  new governance document — ADR-002's freeze and ADR-010's vocabulary are both
  untouched and open finding 4 is not widened
- reproducibility becomes checkable rather than asserted, via rule 3's hash
- a free data source becomes usable *honestly*, because rule 5 makes the
  resulting bias a signed, undeletable property of every number derived from it
- `sample_period` is fixed at the only moment it is free to fix

Negative:

- **universe-driven strategies cannot be honestly evaluated at a zero budget**,
  and rule 5 makes that visible on every artifact rather than letting it pass.
  Correct, and still a real limit on what Belay can conclude
- **option-based strategies are blocked on a data purchase**, and rule 6 names it
  rather than deferring the discovery to Stage 3
- rule 7 changes `Disclosure`, which is inside the integrity hash — free today,
  and only today
- rule 3 means the price data is not itself governed by the artifact lifecycle;
  its integrity rests on a hash rather than on the store being trustworthy
- rule 4's store grows without bound, and this ADR does not rule a retention
  policy because Law VII points away from one and no document sets a limit

---

## Rejected Alternatives

**One adapter interface covering both market data and execution.**
Reason: rule 2. Their correct retry defaults are opposites, and Law VI puts them
on opposite sides of a boundary the constitution declares independent. The economy
is apparent rather than real.

**Making the price series itself an Artifact.**
Reason: it has no honest identifier and no honest type under
`Knowledge/Identifiers.md` and `ArtifactType`, and manufacturing one widens open
finding 4. It would also put a large, restatement-prone dataset inside a contract
designed for immutable signed records.

**Committing the fetched series now that the Atlas archive is private.**
Reason: permitted is not wise. Rule 4's third argument decides it — the artifact
already carries the content hash, so committing the bytes adds no guarantee while
making repository growth unbounded and irreversible.

**Adding a fifth evidence level for observed data.**
Reason: `Evidence_Standards.md` is in the frozen governance layer, and rule 3
means Belay does not need a grade for a thing it has ruled is not evidence. The
gap is recorded as a finding instead.

**Equities-only for Stage 2, with options deferred to a later contract.**
Reason: `constitution/Operational_Constraints.md:25-27`. An equities-only contract
gives equities inherent preference by construction. Deferring the
*implementation* is fine and is what rule 6 does; deferring the *expressibility*
is not.

**Writing one hard-coded fetcher and calling Stage 2 done.**
Reason: ADR-011's central holding. It does not avoid the ruling, it makes it
silently — that there is only ever one source, and that its survivorship
properties are whatever they happen to be.

---

## Required Follow-Up (ADR-013)

- ~~ratify or amend~~ — **done 2026-07-31, Accepted as corrected, no rule
  amended.** Implementation deliberately deferred to a later session
- ~~implement; tests written first and run against unchanged code~~ — **done
  2026-08-01, all ten rules.** `framework/data/` holds the contract, survivorship
  disclosure, fetch record, versioned store and two adapters. Every test was
  written first and run against unchanged code; each failed at import before the
  module it names existed. Suite 388 → 520.

  > **Rule 7 could not be implemented as written and the workaround is a
  > finding.** Splitting `sample_period` into two fields turns the suite red:
  > `tests/test_governance_conformance.py` parses `Validation/Backtesting.md` and
  > holds `Disclosure`'s field **names** to the document. The rule changes the
  > field's **type** instead — `sample_period: SamplePeriod` — and the dates are
  > rendered into `content` as encoded ISO strings, because `canonical_digest`'s
  > docstring asks callers not to rely on its `default=str` backstop. The rule's
  > three stated purposes are all met. Cost was zero as predicted:
  > `git ls-files "*.yaml"` still returns nothing
- ~~a second reader re-opens every file cited above and checks each claim at the
  stated line, before implementation~~ — **done, 2026-07-31. 71 claims checked,
  11 wrong or questionable, 4 of them defect-grade.** All four are corrected and
  marked inline above. See the Status block for the scorecard and for why the
  author's own pass is not a substitute
- ~~establish, before implementation rather than during it, whether the chosen
  option-data source retains expired contracts, and under what licence~~ —
  **both done 2026-08-01, established against the source rather than from a
  document.** DoltHub's web page is JavaScript-rendered and yielded nothing, so
  both were answered through its SQL API.

  **Licence: Creative Commons Attribution-ShareAlike 4.0 International**, from
  the repository's own `LICENSE.md` via `SELECT doc_name, doc_text FROM
  dolt_docs`. Section 4 grants the right to "extract, reuse, reproduce, and Share
  all or a substantial portion of the contents of the database", so **rule 4's
  storage ruling rests on unbounded repository growth alone rather than on a
  licence bar**. ShareAlike binds only on *sharing* adapted material, which a
  private research repository does not do; attribution attaches regardless and is
  carried in the adapter's `name`, which lands inside the integrity hash.

  **Expired contracts are retained**, established empirically rather than from
  prose. `SELECT date, expiration, act_symbol FROM option_chain ORDER BY date ASC
  LIMIT 3` returns a contract observed 2019-02-09 expiring 2019-02-15, still
  present in a database whose newest row is 2026-07-31; a full chain across
  strikes and both rights for an expiry of 2019-03-15, observed 2019-03-02, is
  also still queryable. A live-chains-only source would have dropped these in
  2019. **Options are therefore backtestable at a zero budget**, and rule 6's
  first survivorship half is answered `Retained` for this source

- **NEW, and it belongs here rather than in a finding alone: the *equity* source
  is survivor-only in its prices.** Rule 9 applied to Belay's own choice a second
  time, and the answer is the reverse of the expected shape. `SELECT date,
  act_symbol, close FROM ohlcv WHERE act_symbol='COH' AND date BETWEEN
  '2015-01-05' AND '2015-01-16'` returns zero rows, while the same query for AAPL
  over 2017-10-16..2017-10-26 returns three — Coach, Inc. traded actively until
  October 2017 and has no history in the price table at all. Meanwhile `SELECT
  act_symbol, security_name, last_seen FROM symbol ORDER BY last_seen ASC`
  returns COH with `last_seen` 2017-10-26, in a table of 23,827 rows against
  roughly 6,000 currently-listed US stocks. **The source fails the
  delisted-prices half and partly passes the delisted-universe half** — precisely
  the "a source can pass one and fail the other" case rule 5 sets out, arriving
  in the direction nobody predicted. Recorded as `SURVIVORS_ONLY` / `PARTIAL` in
  `framework/data/dolthub.py`, which under rule 9 is an established answer rather
  than an unknown one
- ~~record the `Evidence_Standards.md` gap as a finding~~ — done in the same
  commit as this ADR; `docs/HANDOFF.md` finding 12
- ~~record the option-data blocker as a finding~~ — done, and then **rewritten**,
  because its premise was false: option data is reachable at a zero budget. See
  rule 6's correction and `docs/HANDOFF.md` finding 13
- ~~a conformance test holding the survivorship disclosure constants to ADR-012
  rule 7's shape~~ — **done.** `tests/data/test_survivorship.py` asserts
  `inflates`, `deflates` and `simultaneous` on the constant and on the artifact's
  `known_limitations`, mirroring ADR-012's assertion of "optimistic". It also
  asserts the converse — a clean source must *not* carry the warning, or the
  warning stops distinguishing the sources it exists to distinguish
- ~~`.gitignore` gains the data store path, as rule 4's enforcement~~ — **done,
  before the first byte landed.** `data/market/`, and
  `test_the_default_store_root_is_ignored_by_git` asks `git check-ignore` itself
  rather than reading `.gitignore` for a string, because a rule in the wrong
  section or shadowed by a later negation would read correctly and behave wrongly
- ~~`docs/ROADMAP.md` Stage 2 updated to cite this ADR once ratified~~ — **done**,
  and updated again on implementation
- **NEW: the hosted SQL API cannot serve a backfill, and the fix is a transport
  rather than a ruling.** Measured 2026-08-01: a novel month-sized query takes
  35–55s and frequently exceeds the server's ~54s deadline (3/3 attempts at three
  months, 2/2 at one novel month); the same month in weekly chunks succeeded but
  cost 111 seconds. Thirteen years is roughly 6.6 hours per symbol. The adapter
  chunks on calendar months — boundaries derived from the requested window alone,
  so the content hash stays comparable, which a tunable chunk size would have
  broken. **Dolt's intended path is `dolt clone`**, and the adapter's transport is
  already an injected `Callable[[str], bytes]`, so this is a second
  implementation of an existing seam. `docs/HANDOFF.md` finding 14. **No rule of
  this ADR is affected**

### Deliberately not settled here

**Where the halt lives.** Removed from scope on the reasoning in the Context
section. `docs/HANDOFF.md` finding 11.

**A retention policy for the data store.** Rule 4 grows it without bound. Law VII
points away from deletion and no document sets a limit, so inventing one here
would be the failure ADR-011 names.

**Which vendor is implemented first.** A licence and coverage question to settle
against a current price list at implementation time, not a doctrine question.
Rule 2 makes it reversible, which is the point of ruling the contract first.

> **Settled 2026-08-01: DoltHub `post-no-preference/stocks`, free, CC BY-SA 4.0,
> survivor-only in its prices and disclosed as such.** A second adapter,
> `framework/data/ibkr.py`, was written alongside it to test whether the contract
> is genuinely a contract rather than one implementation wearing a general name;
> it required no change to `MarketDataSource` despite a structurally different
> wire format. **It has never been run against the live IBKR API** and records
> that inside its own survivorship basis, so the admission travels onto every
> artifact derived from it.
>
> **IBKR was considered and does not solve the problem.** Its own documentation
> states "the API always requires Level 1 streaming real time data to return
> historical data" — so historical data is not included with an account — and
> "if data is not available for a specific instrument, data type, or period
> within a TWS chart it will also not be available from the API", where a
> delisted instrument has no chart. **It costs money and buys the same
> survivorship limitation.** The fee is waivable above a monthly commission
> threshold, which a paper-first system generating no commissions cannot reach.
>
> **Using the broker as the data source would not violate rule 2**, and it is
> worth stating because the opposite reading is natural. Rule 2 forbids a shared
> *abstraction* — one interface for reads and writes, which must pick one retry
> default and be wrong for the other. The vendor behind each contract is not what
> the rule is about. `MarketDataSource` carries no order vocabulary and
> `test_the_contract_has_no_execution_vocabulary` asserts it never acquires one.

**When survivorship-free data must be bought, and the distinction that decides
it.** Recorded here because the ADR's Consequences section states the limit
without stating the trigger. **Survivorship bias is not "this data is wrong"; it
is "selecting from this data is wrong".** A backtest of an instrument named in
advance is unbiased for that instrument, which survived. The bias enters when
instruments are *chosen* by screening a survivor-only universe, because
everything that failed was removed before anyone looked. So the free source is
adequate for named-instrument work and inadequate the moment Belay screens —
which rule 6's own scoping already defers to Stage 3. **The trigger is the first
time Belay selects instruments rather than being handed them**, and nothing
before that point justifies the purchase.

---

## ADR-014: Where Artifacts Live — Persistence, What Git Tracks, And What A `.gitignore` May Claim

Status:
**Accepted and implemented, 2026-08-02, in all nine rules.** Ratified the same
day by the repository owner as drafted; no rule was amended on ratification.

> **This block read "Accepted. Not implemented in any part." for one commit after
> implementation landed** — the same defect ADR-013's Status block carries a note
> about, in the ADR that cites that note. Found by the independent pass, not by
> the implementer.

**The verification pass this ADR requires ran AFTER implementation, not before,
and that breaches its own Required Follow-Up.** The item below reads "before
implementation"; `docs/HANDOFF.md`'s START HERE, written by the same author in the
same session, placed it after step 6, and the implementer followed the weaker of
the two. Two governance documents gave opposite orderings for one mandatory step.
**The cost is not hypothetical: the pass found 19 defect-grade errors across 93
claims, eight of them in code already committed**, and rule 6's one-way door —
signed content, free to change only while nothing is stored — had already closed.
Recorded rather than quietly fixed, because the sequencing is the whole reason
that follow-up item exists. Drafted the same day in
response to F-002 (`reports/review/2026-08-01-review.md`). **No code, no
`.gitignore` edit and no directory was created by the session that wrote or
ratified this**, deliberately: F-002 is a ruling about where artifacts live and
what a tracked file may assert, and wiring a persistence layer first would settle
it by accident. Implementation is deferred to a later session, on the same
separation ADR-013 used.

**Ratification does not make the rules true of the repository.** Every rule below
describes a state Belay is not yet in. `.gitignore:46-49` still carries the false
claim rule 9 refuses, `fetch_and_record` still returns a record nobody stores, and
the AAPL bytes still have none — until the Required Follow-Up is worked through in
its stated order.

**Read this before building on it: it has had no independent verification pass.**
Every ADR in this file that has had one lost claims to it — ADR-011 four, ADR-012
one in twenty, ADR-013 eleven of seventy-one with four defect-grade, and in each
case the author's own pass caught at most one. This draft's citations were opened
and read at the stated line in the drafting session, which is exactly what the
authors of those three drafts could also have said.

**Three findings opened while drafting this**, before any of it was ratified.
They are in `docs/HANDOFF.md` and each is a fact about the repository as
committed rather than a consequence of this ruling: the fetch record cannot name
the bytes it records; the identifier space cannot fund one record per fetch; and
an identifier reused at a new version is silently mis-filed. **The second of
those blocks rule 4** and is called out in the Required Follow-Up rather than
ruled here.

Date:
2026-08-02

---

## Context

**F-002 in one sentence: `fetch_and_record` builds the signed record ADR-013 rule
3 requires, returns it, and nothing in Belay has ever written one to disk.**
`framework/data/fetch_record.py:203` returns `Fetch(...)`; `git ls-files` returns
no artifact of any type; `ArtifactRepository` is constructed nowhere outside its
own module and the test suite; and the only production caller of
`fetch_and_record` is `scripts/verify_clone.py:67`, which builds its store in
`tempfile.mkdtemp` (`:61`), `rmtree`s it (`:177`) and drops the record.

**What that falsifies is not a comment, it is an argument.** `.gitignore:46-49`
gives the reason the fetched bytes are not committed: "Nothing is lost by this.
Rule 3 already covers the integrity requirement: the fetch record artifact
carries the content hash, so the record of what was obtained is signed and
permanent whether or not the bytes are under version control."
`framework/data/store.py:21-23` makes the same argument from the other side, and
ADR-013 rule 4's third bullet — the one its own text calls "deciding" — is that
argument. The record was neither signed into anything durable nor permanent, so
the third leg of a ruling in this file rested on a fact that has never been true.

**This is a structural question and not a missing call to `save()`.** Answering
it requires deciding where artifacts live, which of them git tracks, whether
persistence belongs to the fetch or to its caller, what becomes of the one series
Belay already holds, and what a `.gitignore` comment is allowed to assert about a
subsystem it does not control. Each of those has a consequence that is permanent
once a signed record lands, which is why the ruling comes first.

### Nothing in this repository says where an artifact goes

Checked rather than assumed, because it decides how rule 1 has to be worded.
`Knowledge/` was read for a storage location — `ArchiveManager.md`,
`ArtifactLifecycle.md`, `Librarian.md`, `MemoryIndex.md`, `Search.md`,
`KnowledgeGraph.md`, `Schema.md`, `Versioning.md`, `Identifiers.md` — together
with `docs/Architecture.md` and `AGENTS.md`. **They specify identity, indexing,
ordering, retention and lifecycle, and not one of them names a directory.**
`Knowledge/MemoryIndex.md` says every artifact is indexed by ten fields;
`Knowledge/Search.md` says retrieval is through metadata. Both describe a
searchable store without saying where it is.

`ArtifactRepository.__init__` (`framework/artifacts/repository.py:25-27`) takes
`root` as a required argument with no default, so every caller has always chosen
one and no two callers had to agree. Compare `framework/data/store.py:35-39`,
where `STORE_ROOT = Path("data") / "market"` is a module constant with the reason
written beside it — "so the store travels with a clone while its contents do
not". The data store answered this question in its first commit. The artifact
repository never has.

**So rule 1 is a choice, and it is labelled as one.** `docs/EndState.md` names
extending a document rather than applying one as "the failure this repository has
now recorded three times", and inventing a location and then citing
`Knowledge/Librarian.md` for it would be that failure. What the documents supply
is the *constraints* — permanent, never deleted, searchable, indexed by
identifier — and those decide the shape of the answer without deciding the path.

### What the governing documents do require

Read in full for this ADR at the lines given:

- **`constitution/Governance.md:27`** — "Institutional memory is mandatory."
- **`constitution/Immutable_Laws.md:51`** (Law VII) — "Institutional knowledge
  shall never be intentionally discarded."
- **`constitution/Operational_Constraints.md:5`** — "Belay shall maintain
  accurate records."
- **`constitution/Operational_Constraints.md:9-17`** — "Belay shall distinguish:
  Facts / Assumptions / Predictions / Opinions."
- **`Knowledge/ArtifactLifecycle.md:27`**, **`:29`** — "No artifact is deleted.
  Artifacts become historical evidence."
- **`Knowledge/ArchiveManager.md:7`**, **`:11`** — "Archives are immutable.
  Belay never deletes evidence."
- **`Knowledge/Identifiers.md:3-5`** — "Identifiers are permanent. They are never
  reused."
- **`Knowledge/Versioning.md:23-27`** — "Knowledge records every version. No
  version is overwritten. Historical versions remain searchable."

**Law VII does not cleanly reach F-002 and the review said so.** Law VII forbids
knowledge being *intentionally* discarded, and no persistence layer was ever
wired up, so this is a gap rather than a decision. `Governance.md:27` is
unambiguous and carries the breach on its own. That distinction is kept here
because it also decides rule 2: mandatory institutional memory is a statement
about what must survive the machine, not about what must be hashed.

### Four things measured for this draft rather than argued

Every figure below was produced by running the thing, against the repository as
committed. They are here because rules 2, 5 and 8 turn on magnitudes, and this
file's own ADR-013 rule 6 records what happens when a size claim is asserted from
general knowledge instead of checked.

**1. A fetch record is 2,869 bytes of YAML**, built through `fetch_record()` from
`DoltHubStocksSource` and dumped through `ArtifactSerializer`. **1,680 of those
bytes are the survivorship `known_limitations` constant**, identical in every
record that source will ever produce.

> **Both figures were wrong when this was drafted and both are corrected here.**
> The draft said 2,732 and 1,535. 2,732 reproduces only with a whole-second
> timestamp — `utc_now()` carries microseconds, which adds 7 bytes to each of
> `created` and `updated` — and the draft then projected growth for the *post*-
> rule-6 world using a *pre*-rule-6 measurement, while rule 6 is in this same ADR
> and adds three fields. 1,535 was the Python string length rather than its
> serialised size; escaped and folded into YAML the same constant occupies 1,680.
> **2,869 is the record that actually shipped**, measured as the git blob of
> `artifacts/RPT-0001/1.0.0.yaml`. Every ratio below is recomputed against it and
> every one of them moved. It cannot be deduplicated: ADR-013 rule 5
exists so the caveat travels *on* the artifact and inside its signature, and a
record pointing at a shared copy of its own disclosure would be the substitution
that rule refuses.

**2. The one series Belay holds is 4,462 bytes.**
`data/market/dolthub-stocks/AAPL/0001-a7dbcaf3fb6aba2d.bin`, 28 bars, and its
full SHA256 is `a7dbcaf3fb6aba2dc179ca482986bdc7e8887f609c0ca3a3cc25a73c145272a6`
— the filename carries the first 16 hex characters of it, as
`framework/data/store.py:41-49` specifies. Its record is 64.3% of its size (61% in the draft, against the pre-rule-6 record).

**3. The payload is two JSON documents joined by a newline, and the envelope
costs 633 bytes each.** (The draft said "concatenated", and its two document
sizes sum to 4,461 against a 4,462-byte file; the missing byte is the separator.) The adapter chunks on calendar months (ADR-013's Required Follow-Up
on the transport ceiling), so the stored bytes for 2024-01-02 to 2024-02-09 are
one document of 3,028 bytes carrying 21 rows and one of 1,433 carrying 7. Rows
cost about 114 bytes each.

**4. Therefore, at the cadence Belay has actually chosen, the record is larger
than the data it records.** `docs/OwnerDecisions.md:733` settles that positions
are held days to months and `:737` that Stage 2 fetches daily bars, so the
steady-state fetch is one trading day: roughly **747 bytes** of payload (one envelope, one
row) against a **2,869-byte** record. **The tracked half is 3.84 times the size of
the ignored half** (3.7 in the draft). For a thirteen-year backfill the ratio inverts completely —
about 472 KB of payload against one 2,869-byte record — and both facts are true
at once, which is precisely why `.gitignore:46-49`'s "nothing is lost by this"
cannot be repaired by rewording it. It compares the wrong two quantities.

---

## Decision

**1. Artifacts are persisted under one root, `artifacts/` at the repository root,
and the root is a module constant rather than a caller's argument.**

The constant is what makes the question answerable by anything other than a
person. `framework/data/store.py:35-39` already carries the pattern and the
reason — a relative module constant, so the store travels with a clone while its
contents do not, where "an absolute path would make the store machine-specific
and silently empty everywhere else". Every word of that applies here.
`ArtifactRepository(root)` keeps its argument, because tests and diagnostics must
be able to write somewhere else; what changes is that there is a default and it
is named in code.

**Not under `data/`.** ADR-013 rule 3 rules that the fetched series is an *input*
and the record is not; `data/` holds two trees that are both inputs and both
ignored (`.gitignore:53`, `:69`). Filing the records beside them would put the
one permanent thing inside the directory whose two entries exist to say "this is
not permanent".

**The layout is the one `ArtifactRepository` already implements** —
`{root}/{identifier}/{version}.yaml`, from `repository.py:29-37` — so this rule
adds a location and changes no behaviour.

**2. Every artifact under that root is tracked by git, and `.gitignore` gains no
entry for it.**

`Governance.md:27` makes institutional memory mandatory and a file on one machine
is not institutional memory — that is the whole of F-002's failure paragraph. The
asymmetry with ADR-013 rule 4 is deliberate and rests on three differences that
are properties of the things themselves rather than preferences:

- **Size.** Measured above. A record is kilobytes where a backfill is hundreds of
  kilobytes per symbol and a clone is gigabytes.
- **Reproducibility, and it runs the opposite way.** ADR-013 rule 4 keeps the
  bytes out of git partly because they can be re-obtained. **A fetch cannot.** The
  bytes a vendor returned on a date, and the fact that Belay asked on that date,
  are not re-observable once the vendor restates — which is the same premise rule
  4 uses to argue the series must be *versioned*, arriving here as an argument
  that the record must be *committed*.
- **Licence.** `.gitignore:42-43` names vendor retention terms as a reason to
  keep the bytes prunable. A record carries a hash and a coverage window, not the
  vendor's data.

**The repository already distinguishes these two classes and this rule copies
it.** `.gitignore:34` ignores `reports/generated/`, which the dashboard rebuilds
on every run, while `reports/review/2026-08-01-review.md` is tracked because it is
a record. Derived output is ignored; records are committed.

**3. The root is the boundary between an experiment and a record, and nothing
enforces it but the choice of root.**

A run that does not mean to record permanently passes its own root and gets a
temporary one. `scripts/verify_clone.py` already does exactly this
(`tempfile.mkdtemp` at `:61`, `rmtree` at `:177`) and **must keep doing it after
rule 4 lands** — it hardcodes the identifier `RPT-9001` at `:68`, and a
diagnostic that wrote into the tracked root would mint a permanent institutional
record every time somebody checked the clone still worked. Stated as a rule
because the natural reading of rule 4 is that everything now persists, and that
reading is wrong.

**4. `fetch_and_record` persists the record. The repository is a required
argument, exactly as the store already is.**

**The argument is the function's own docstring, applied to the half it left
out.** `framework/data/fetch_record.py:159-172` explains why fetching and storing
are one call: "These are one act, and separating them is how the failure goes
silent" — because until 2026-08-01 `SeriesStore` had no caller, so "every signed
record carried a `content_hash` pointing at bytes nobody kept". F-002 is the same
sentence with the two halves swapped: every stored byte belongs to a fetch nobody
recorded. The fix that closed the first one is the fix for the second.

**The order is forced and is not a preference.** Fetch, store the bytes, sign the
record over their hash, save the record. The record cannot precede the payload it
hashes. The gap between the two writes is where `docs/HANDOFF.md`'s "A Fetch
Stores Its Bytes Before Discovering The Series Is Empty" already lives, and rule 7
names the check that makes such a gap visible rather than silent.

**Rejected, and it is the review's own proposal:** a thin `scripts/fetch.py` that
saves the returned record. See Rejected Alternatives — persistence would then be a
property of one script rather than of the act, and every other caller would have
to remember. F-002 is what remembering looks like when it fails.

**5. One record per stored series version, not one per fetch.**

`framework/data/store.py:137-141` already rules the parallel case and gives the
reason: a re-fetch whose bytes are identical returns the existing version rather
than writing a second copy, because "nothing was restated, so there is no new
fact to record". `fetch_and_record` builds a record unconditionally, so today the
two halves of one function disagree about what a new fact is. Under this rule a
fetch that produced no new store version produces no new record, and a fetch that
differs produces both.

**What this rule costs, stated rather than buried: the fact that Belay asked
again on a later date and the answer was unchanged is not retained anywhere.**
That fact is real, and Law VII has a claim on it. It is left unsettled below
rather than answered here, with the arithmetic attached, because both available
answers are bad in a way the numbers decide: recording confirmations as artifact
versions costs about 723 KB per symbol per year of permanently tracked YAML, and
not recording them loses a fact about what Belay checked and when.

**6. The record must be able to name the bytes it is a record of. The signed
content gains the source key, the store version and the store-relative path.**

Today it cannot. `fetch_record.py:88-108` writes `("data_source", source.name)`
and nothing else that identifies the file, while `fetch_record.py:191` files the
bytes under `source.key` — and `framework/data/contract.py:199-206` says in terms
why those two are separate: the display name "carries the licence attribution CC
BY-SA requires" and is expected to be edited, where the key is "short, lowercase,
and never changed once data exists". **So the one identifier the record carries is
the one the store deliberately does not use.** The join survives only through the
content hash, and only by hashing every file in the store until one matches.

**This rule is in this ADR because of when it is free.** ADR-013 rule 7 changed
`Disclosure` on the explicit ground that "the cost of doing this now is zero, and
that was verified rather than assumed" — no artifact was stored, so no signature
existed to break. That window is still open and rule 4 closes it: the first saved
record makes every later change to the signed content a migration of permanent
append-only records, which `Knowledge/Versioning.md:25` forbids rewriting. **Rules
4 and 6 must land in that order or not at all.**

**7. A stored version with no record is a state Belay can name and detect.**

Rule 4 makes the pairing the normal case; it does not make the unpaired case
impossible, and finding 13 is a live path to one. The check is mechanical and
follows `tests/data/test_store.py:216`'s shape of asking the tool rather than
reading a file for a string: for every version in the store, hash the file and
require a committed fetch record whose `content_hash` equals it. Anything left
over is an orphan and is reported as one.

**This is also what makes rule 8's claim checkable rather than asserted**, which
is the property `.gitignore:46-49` has been missing since it was written.

**8. The one series Belay already holds: nothing is fabricated and nothing is
deleted.**

`data/market/dolthub-stocks/AAPL/0001-a7dbcaf3fb6aba2d.bin` stays exactly where it
is. **No retroactive record is written for it.** Its fetch timestamp is not
recoverable, and a record is signed over `created`; inventing one would file an
Assumption under Facts, which `constitution/Operational_Constraints.md:9-17`
separates precisely so that it cannot happen. Until it has a record the file is
an unprovenanced input and is not eligible to feed anything that produces
evidence.

**The path back is a re-fetch, and it costs nothing.** Under rule 4, re-fetching
the same window either returns identical bytes — in which case
`framework/data/store.py:145-148` returns the *existing* version 1 and the new
record's `content_hash` proves it describes the file already on disk, so the
orphan is adopted without anything being asserted that was not observed — or
returns different bytes, in which case the vendor restated: the new bytes land as
version 2 with a record, and version 1 stays on disk permanently unprovenanced,
which is a true statement about it rather than a loss.

**So the first act after ratification is a fetch, not a migration.** That is the
cheapest moment this will ever be, and it is cheap only because Belay holds 4,462
bytes of data.

**9. What a `.gitignore` comment is permitted to assert.**

A comment may state what its own entry enforces. It may state a fact about
another subsystem **only where something checkable holds that fact true** — and
the check must interrogate the system, not the prose. `.gitignore:46-49` asserted
a property of the artifact layer, nothing held it, and it was false from the
moment it was written; it read exactly as it would have read if it were true,
which is the failure mode this repository has recorded against a dashboard
parser, an `xfail` marker and a test docstring already.

Concretely:

- **Until rule 7's check exists, `.gitignore:46-49` must say what is true** — that
  the record layer is ruled and not yet built, and that the bytes are therefore
  currently ignored on the size and licence arguments alone. Those two arguments
  are unaffected by F-002 and survive on their own.
- **Once it exists**, the claim may be restated, and must then name the tracked
  directory rather than gesture at "the fetch record artifact".
- **The "nothing is lost by this" sentence does not come back in any form.** The
  measurement above shows it compares the wrong two quantities: at Belay's chosen
  daily cadence the tracked record is 3.7 times the ignored payload, so whatever
  is true about committing the bytes, it is not that the arrangement is free.

---

## Consequences

Positive:

- F-002's breach of `Governance.md:27` closes, and closes at the point where the
  bytes and the record are produced rather than in a script somebody has to
  remember to run
- the third leg of ADR-013 rule 4 becomes true for the first time, and rule 7's
  check makes it *checkable* — which is what rule 3 claimed for it all along
- `ArtifactRepository`, written across three sessions and exercised only by its
  own tests, acquires its first production caller
- the record gains the fields that let it name its own bytes, in the last window
  where changing signed content is free
- the AAPL series is recoverable without anything being fabricated, and the ruling
  says so with the mechanism rather than with an intention

Negative:

- **git growth becomes unbounded in exactly the way ADR-013 rule 4 refused for the
  bytes.** Measured: 2,869 bytes per record, of which 1,680 is a constant that
  rule 5 forbids deduplicating. At 50 symbols on a daily cadence that is about
  **36 MB per year**, permanent and unprunable; at a 6,000-symbol universe it is
  about **4.3 GB per year**. The first is survivable for years and the second is
  not, and this ADR does not rule a retention policy — Law VII points away from
  one and no document sets a limit, which is the same ground on which ADR-013
  declined to rule one for the store. **The trigger to revisit is the same trigger
  ADR-013 already named for buying data: the first time Belay selects instruments
  rather than being handed them.** Named here so it is a decision rather than a
  discovery
- rule 6 changes the signed content of every fetch record, and after rule 4 lands
  that becomes a migration of append-only records rather than an edit
- rule 5 loses the fact that a re-fetch was performed and matched. Left open below
- rule 3 is enforced by nothing but the choice of root. A caller that passes the
  default root by mistake writes a permanent record, and the repository will
  accept it because it is a valid signed artifact
- the artifact round trip is now load-bearing where it was not. **Established
  rather than assumed for this shape:** a fetch record built through
  `fetch_and_record`, saved, and read back through `ArtifactRepository.get()`
  returned identical `content` and an identical integrity hash on the repository
  as committed. No defect there — recorded because a round trip that had never
  been run against this artifact shape is not evidence that it works

---

## Rejected Alternatives

**A thin `scripts/fetch.py` that saves the returned record, as F-002 proposes.**
Reason: it makes persistence a property of one script instead of a property of
the act. Every other caller — the test harness, a Stage 3 backfill, a scheduler,
the next session's throwaway — would have to remember, and F-002 exists because
remembering failed for the entire life of the module. Rule 4 puts persistence
where `fetch_record.py:159-172` already put storage, on the same argument that
docstring makes.

**Writing a retroactive record for the existing AAPL bytes.**
Reason: rule 8. The fetch timestamp is unrecoverable and the record is signed over
it. A signed artifact whose `created` is a guess is an Assumption filed as a Fact,
and `constitution/Operational_Constraints.md:9-17` is the line that separates
them. The re-fetch costs seconds and asserts nothing.

**Deleting the unprovenanced bytes and starting clean.**
Reason: `Knowledge/ArchiveManager.md:11` — "Belay never deletes evidence" — and
`Knowledge/ArtifactLifecycle.md:27`. Deleting is also unnecessary: rule 8's
re-fetch either adopts the file or leaves it standing beside a version 2 that has
a record, and both outcomes are honest.

**Putting the artifact root under `data/`.**
Reason: rule 1. `data/` is where inputs live and both of its entries are ignored;
the records are the one permanent thing in the arrangement.

**Ignoring the artifact root, and treating records as machine-local.**
Reason: this is the current state, and it is the finding. `Governance.md:27`
requires institutional memory, and a record that exists on one machine is a record
that a reimage destroys — which is F-002's failure paragraph exactly.

**Ruling a retention or pruning policy for records now.**
Reason: ADR-013 declined the identical question for the store, on the ground that
Law VII points away from deletion and no document sets a limit. Inventing one here
would be the defaulting failure ADR-011 names. The growth is recorded with a
trigger instead.

**Widening the identifier pattern as part of this ADR.**
Reason: it is a separate ruling with a separate blast radius —
`Knowledge/Identifiers.md` is governance and `framework/identifiers.py:33-35` is
the code that turned its examples into a rule. It is a **prerequisite** to rule 4
rather than a part of it, and it is recorded as a finding so that it is settled on
its own terms.

---

## Required Follow-Up (ADR-014)

- ~~ratify or amend~~ — **done 2026-08-02, Accepted as drafted, no rule amended.**
  The owner's call covered rule 1 (a new tracked top-level directory), rule 2
  (permanent git growth accepted with a stated trigger) and rule 5 (a fact
  deliberately not retained). Implementation deliberately deferred to a later
  session
- ~~settle the identifier ruling first~~ — **done, and it needed no governance
  amendment.** `Knowledge/Identifiers.md` states no digit count and its seven
  examples all stay valid, so `framework/identifiers.py` widened to
  `[0-9]{4}|[1-9][0-9]{4,}` and nothing in `Knowledge/` changed. An alternation
  rather than `[0-9]{4,}`, which would admit `RPT-00217` beside `RPT-0217` as two
  directories for one number. **`[0-9]` rather than `\d` and `\Z` rather than
  `$` came from the independent pass**, which found three Unicode digit forms and
  a trailing newline reaching `save()` through the first version of the widening.
- **superseded, kept because the reasoning is the record:** `docs/HANDOFF.md`, "The Identifier Space
  Cannot Fund One Record Per Fetch". Rule 4 mints permanent identifiers, and
  `Knowledge/Identifiers.md:3-5` makes them permanent and never reused, so a
  wrong answer here cannot be corrected afterwards. **This blocks rule 4 and
  nothing else in this ADR**
- ~~a second reader re-opens every file cited above and checks each claim at the
  stated line~~ — **done, and late: after implementation rather than before, which
  the Status block records as a breach. 93 claims checked, 23 wrong, 19
  defect-grade.** Eight were in committed code and are fixed, each with a
  regression test confirmed red against the pre-fix implementation; the rest were
  citations and arithmetic in this document, corrected and marked inline above.
  **The author's own review of the same work found none of the nineteen** —
  fourth consecutive session with that result
- **implement rules 6 and 4 in that order**, tests written first and run against
  unchanged code. Reversing them makes rule 6 a migration
- **rule 7's check**, in the shape `tests/data/test_store.py:216` uses — ask the
  system, not the prose
- **re-fetch the AAPL window under rule 4** and record which of the two outcomes
  in rule 8 occurred. If the bytes differ, that is a vendor restatement observed
  in the wild and it is worth its own note
- **rewrite `.gitignore:46-49` twice**: once now, to say what is true, and once
  after rule 7's check exists, to name the directory. **The interim rewrite was
  deliberately not made by the session that drafted this** — it is rule 9's to
  authorise, and editing it first would have been the ADR settling itself
- **`docs/ROADMAP.md` and `CHANGELOG.md` on ratification**, and not before. ADR-013
  records a miscount that propagated into both plus a commit subject before anyone
  caught it

### Deliberately not settled here

**Whether a re-fetch that changed nothing is recorded at all, and where.** Rule 5
declines to mint an artifact for it and does not claim the fact is worthless. The
three candidate homes are: a new version of the existing record (about 723 KB per
symbol per year of tracked YAML, at 252 confirmations a year against a 2,869-byte
record); an unsigned log, which Law VII would not obviously accept as
institutional knowledge; or nothing, which is rule 5 as written. **It is the same
open question `docs/HANDOFF.md` records for an empty fetch** — "refusing to write
bytes is not the same as refusing to record that the source was asked and said
nothing" — and the two should be settled together rather than twice.

**The upstream database revision.** `framework/data/dolt_clone.py:81-85` excludes
the clone's commit hash from the payload for a good reason: `dolt pull` advances
it whenever upstream moves, so every unchanged series would hash differently and
produce a phantom restatement. That ruling is about the *payload*. The record's
`content` is a different place, where the same value would cost nothing and would
answer "which revision of a version-controlled database said this" — a question
rule 3's re-fetch-hash-compare cannot answer when the comparison fails. Not ruled
here because it is a fourth field on top of rule 6's three and belongs with
whoever verifies this draft.

**A retention policy for artifacts.** See Rejected Alternatives. The growth is
recorded with a trigger instead of a limit.

**Whether artifacts other than fetch records need anything beyond rules 1 to 3.**
Rules 1, 2, 3 and 9 are written for artifacts generally, because F-002's evidence
is that *no* artifact of any type has ever been committed. Rules 4 to 8 are
specific to fetch records, since that is the only producer in the repository with
a caller. A metric artifact, a review record and a strategy will each raise the
question of who calls `save()` and when, and nothing here answers it.
## ADR-015: A Strategy's Stage Is Carried, Not Asserted — And A Stage Move Without Evidence Is Not A Review

Status:
**PROPOSED — revised 2026-09-25 after a second falsification pass and the owner's Parts 25 and 26. Not ratified. Not implemented in any part.**

Date:
2026-09-19 (revised 2026-09-24, 2026-09-25)

---

> **Where this revision stands (2026-09-25). Read this before the older blocks below;
> where they differ, this one is current.**
>
> - **A second falsification pass found this ADR still not ready** (Issue #21, the
>   comment "Second supplementary pass: the redrafts, ADR-015 at `94815a2` (#7) and
>   ADR-016 at `bad17de` (#20), read against Part 25", 2026-09-24). It found two
>   new blocking holes in how the current-stage read treats a downward step (N1, N2),
>   should-fix findings N3, N4 and N10-N12 against this ADR, and three nits. It ran
>   its attacks as an executable model.
> - **The owner then ruled six more principles, Part 26 (26a-26f)**, 2026-09-24:
>   "Aligned". **Parts 25 and 26 are recorded on branch `claude/kind-knuth-9g7xlr`
>   and are not yet on `main`.** Every rule below that cites 25x or 26x rests on that
>   record; if it does not reach `main` as written, those rules revert to DRAFTER.
> - **This revision** rewrites the current-stage read (rule 3h) so that a downward
>   rung can only lower a stage that is already established (N1), reads stored
>   downward reviews through a subject index (N2), and flags a downward rung whose
>   review does not resolve for a human to repair (26a, N4). It checks rule 3c's
>   condition 5 against the version that appended the last rung (N3), has rule 3c
>   resolve the last review's bound reports and apply ADR-016 rule 8 (26e, N12),
>   requires a recorded human authorization for a confidence change on a capital
>   stage (26c, N10), and compares data windows in rule 4(f) (26d, N11). Where each
>   landed is in "Revision history" below. The scratch model that checked these rules
>   is described there too.
> - **What blocks ratification now:** Parts 25 and 26 reaching `main`; a fresh
>   independent pass told to falsify both ADRs together (the owner's chosen
>   different-AI pass on Issue #21 is still owed); and the owner's ratification of
>   both.
>
> **The rest of this block is the 2026-09-24 revision's, kept as history, except the
> marking legend at its end, which is current and was updated for this revision.**
>
> - **The bar is ruled, and lives in ADR-016.** The owner ruled the evidence bar on
>   2026-09-22 (`docs/OwnerDecisions.md` Part 18, 18a-18g, on `main`) and put it in a
>   separate record, ADR-016 (18g). ADR-016 is a PROPOSED draft on pull request #20's
>   branch (`claude/pensive-hypatia-nu6j3j`), ADR-016-evidence-bar-DRAFT.md under
>   docs/proposals/, not on `main`. Rule 4's table below now points at it.
> - **A falsification pass found this ADR not ready** (Issue #21, the comment
>   "Supplementary falsification pass on ADR-015 (#7) and ADR-016 (#20), taken
>   together", 2026-09-24): three blocking findings against this ADR (B1, B2, B3),
>   one shared with ADR-016 (B7), and should-fix findings S2, S3, S10-S13. The owner
>   then ruled ten principles, **Part 25 (25a-25j)**, 2026-09-24: "aligned to all 10
>   recommendations". **Part 25 is recorded on branch `claude/kind-knuth-9g7xlr` and
>   is not yet merged to `main`.** Every rule below that cites 25x rests on that
>   record; if it does not reach `main` as written, those rules revert to DRAFTER.
> - **This revision** applies 25c (rule 3g), 25d (rules 3b, 3e, 3h), 25i (rule 4(f)),
>   ADR-016's changes to this ADR (B7: rule 4, rule 5, tests 21-23b, Rejected
>   Alternatives, Required Follow-Up, Still Open), and the should-fix findings. Where
>   each finding landed is listed in "Revision history" below.
> - **What blocks ratification now:** Part 25's record reaching `main`; ADR-016's
>   revision; a fresh independent pass told to falsify both ADRs together (the
>   owner's chosen different-AI pass on Issue #21 is still owed, 25 "What it does not
>   settle"); and the owner's ratification of both.
>
> **How each rule is marked in this revision.**
>
> - **RULED (Part n)** — an owner ruling in `docs/OwnerDecisions.md`, whose words are
>   quoted there. Only Parts 18, 19, 22, 23, 25 and 26 are cited as RULED. Parts 18,
>   19 and 23 are on `main`; Part 22 is on pull request #20's branch; Parts 25 and 26
>   are on `claude/kind-knuth-9g7xlr` (above). None of 22, 25 or 26 is on `main`
>   yet. Part 9e, on `main`, is cited as SELECTED, never as RULED.
> - **SELECTED (9e)** — one of the six shape selections of Part 9e. The owner chose
>   the shape; 9e says in terms that it is "shape only" and ratifies no text. The
>   wording that implements it is the drafter's.
> - **DRAFTER** — a choice this draft makes to turn a ruling or selection into
>   something code can check. The owner has not ruled it.
>
> Nothing marked SELECTED or DRAFTER may be read as ruled.

> **What blocked ratification until 2026-09-22 (kept as history; superseded by the
> block above).** On 2026-09-19 the owner was asked what this ADR
> should do about promotions into capital stages given that no document defines a
> minimum evidence quality per rung, and selected **"Research a bar first"**: a
> separate research task is to propose a minimum evidence grade for each rung, and
> the owner rules on that proposal **before** ADR-015 is ratified. Rule 4 below
> carries a marked, empty slot for that table and says exactly how it will consume
> it. **No grade is invented here.**
>
> **That proposal now exists: `docs/proposals/evidence-bar-per-rung.md`, on this
> branch.** It offers four options for the floor, and carries **two recommendations
> that differ** — the author's and an independent reviewer's — each with its own
> reasoning and cost, with no winner declared. It ends with seven questions only the
> owner can answer, ordered to be asked one at a time. **Ratification of this ADR is
> blocked on the owner's ruling on them.**
>
> **Independent passes on the evidence-bar proposal.** A first pass (2026-09-19)
> found 17 defects, 4 of them blocking; the proposal was revised that day and lists
> them in its own appendix. **One of those blockers reached this ADR**, and rule 4's
> table is where it landed: the table is keyed by destination alone, four
> destinations are both a climb and a demotion destination, and a floor read off
> the destination would have gated emergency demotions. Rule 4 now carries a
> direction clause. The table is still empty. **Issue #6 is a second independent
> falsification pass** on the same proposal as carried by public PR #7; its defects
> and the attacks it rejected are recorded in that proposal's Issue #6 appendix.
> Neither pass ratifies this ADR.

> **The owner has selected shape, six times. The owner has ratified no text.**
>
> 2026-09-19, first set:
> 1. For F-007 — **"Carry proof + check storage."** The strategy carries a link to
>    the signed review that authorized each rung, **and** the repository refuses to
>    save or load a rung unless the previous rung is actually stored.
> 2. **"Rule them together."** One ADR covers F-007 and F-014.
>
> 2026-09-19, second set, after the second independent pass:
> 3. **"Yes, check on load."** Reading a strategy also confirms that the previous
>    version and the last rung's review are really stored. Two extra reads, bounded.
>    → rule 3c.
> 4. **"Research a bar first."** Above. → rule 4's slot, and this Status block.
> 5. **"Evidence for everything."** Every stage move, up or down, needs an evidence
>    record and not only a written reason. → rule 4, which is no longer
>    `Promote`-only.
> 6. **"Yes, longest history wins."** A new version's ladder must extend or equal
>    the longest stored ladder under that identifier; a mistaken save is corrected
>    by appending a correcting rung with its own review, never by going back.
>    → rule 3e, which replaces the first revision's "forks are left legal".
>
> Every rule below is this draft's reading of those six selections. The wording,
> the field names, the component boundaries and every open item are the drafter's.
> No owner prose is quoted, because none was given.

> **Revision history, kept because it is the honest measure of how much attacking
> this needed.** Draft SHAs below are **historical Atlas archive revision IDs**;
> Belay's public provenance intentionally preserves them and they will not resolve
> in public Belay. They are not current `adr/015-stage-is-carried` / PR #7 HEADs.
>
> - **First draft (historical Atlas archive revision `2717e76`).** Reviewed
>   independently: every citation and every measurement correct; **three blocking
>   defects in the rule text.** Rule 3 never tied `strategy_stage` to the ladder,
>   so one honest first rung bought a dishonest Production; a rung named a review
>   without its version, so the first ADR-005 revision of any review would have
>   made every citing strategy unreadable; and one review could buy two rungs.
> - **Second draft (historical Atlas archive revision `13d188d`).** Reviewed
>   independently again: **two more blocking defects, both demonstrated by
>   execution.** `get()` did not resolve anything, so a single hand-written
>   re-signed YAML with a seven-rung ladder naming reviews that do not exist was
>   returned as `PRODUCTION`; and the Revision branch let a version built on an
>   older ancestor silently undo a demotion, or un-retire a retired strategy. Five
>   further weaknesses, including that scoping the repository's validation by
>   `artifact.type` let the *forger* choose the scope.
> - **Third draft.** All fixed below, each named where it was fixed. Live carrier
>   for navigation: public PR #7 / `adr/015-stage-is-carried`.
> - **This revision (2026-09-24).** A falsification pass on this ADR and ADR-016
>   together (Issue #21) found three more blocking defects here, none found by the
>   author: a Revision could swap a funded strategy's rules for another's (B1);
>   deleting one review file undid a demotion (B2); and reading a strategy's stage
>   never checked the evidence bar (B3). Where each finding is resolved:
>
>   | Finding | Resolved in | Rests on |
>   |---|---|---|
>   | B1 | rule 3b condition 3, rule 3g; tests 39-43 | 25c, ADR-005 rule 2 |
>   | B2 | rules 3e ("Which stored versions count"), 3h; tests 44-47 | 25d |
>   | B3 (this ADR's half) | rules 3c, 3f; tests 48-51 | 25d, 25e, 18d |
>   | B7 (this ADR's half) | rule 4 (table, 4(a), 4(b), `Remain`), rule 5, tests 21-23b, Rejected Alternatives, Consequences, Required Follow-Up, Still Open | 18a-18g |
>   | S2 | rule 3b ("A downward append"), rule 3h; test 46 | 25d, 18b |
>   | S3 | rule 4(f); test 52 | 25i |
>   | S10 | rule 4, "This amends ADR-004 rule 4" | 9e(v), 18b |
>   | S11 | rule 8 | 25d, 25j |
>   | S12 | Required Follow-Up, first bullet | the record on PR #7 |
>   | S13 | rule 2 step 6 | — |
>   | N1 | Context (F-014), rule 4(a) | — |
>   | N3 | rule 5, "Keys that do not apply to an outcome" | — |
>   | N4 | rule 4, the note under the table; ADR-016 test 13 | 25g |
>   | N6 | rule 1, "What the edge means" | — |
>
>   N5 (both branches conflicted with `main`) was resolved by merging `main` into this
>   branch as a merge commit before this revision.
>
> - **This revision (2026-09-25).** A second pass on the redraft (Issue #21, named in
>   the Status block) found two more blocking defects here, again none found by the
>   author. A downward last rung counted without its review, so one hand-signed file
>   with no reviews on disk read as `Limited Capital` (N1). Deleting the demoted
>   *version* file, rather than its review, still undid a demotion (N2). **The second
>   pass reused the labels N1-N7 for new findings, so in the table below its
>   findings are written "2N1" to "2N13"**; plain N1-N7 above are the first pass's
>   nits.
>
>   | Finding | Resolved in | Rests on |
>   |---|---|---|
>   | 2N1 | rule 3h steps 3-4 ("the base"); rule 3e ("Which stored versions count"); tests 53-55 | 25d |
>   | 2N2 | rule 3h step 5 (stored downward reviews); Required Follow-Up (the subject index); test 56 | 25d |
>   | 2N3 | rule 3c, the second read ("against the version that appended the last rung"); test 57 | — |
>   | 2N4 | rule 3h step 6 (the repair flag); rule 3e; rule 4(f) ("the demotion index"); test 58 | 26a |
>   | 2N10 | rule 3g ("Confidence on a capital stage"); rule 5; test 59 | 26c, 25f |
>   | 2N11 | rule 4(f), second check (data windows); test 60 | 26d, 25i |
>   | 2N12 | rule 3c (bound reports and ADR-016 rule 8); rule 3f; test 48; the residual removed from rule 3f and the residual-risk count | 26e |
>   | nit, 3e's first clause labeled RULED | rule 3e ("Which stored versions count"), now marked | — |
>   | nit, stale "Two independent passes" | the paragraph below | — |
>   | nit, F-007 cited at `docs/HANDOFF.md:3365` | Context; repointed to `:3788`, the heading "A Strategy Can Still Be Signed Into Existence At Production (F-007)" | — |
>
>   2N5-2N9 and 2N13 are against ADR-016 and are resolved there. 26b and 26f are
>   ADR-016's too; rule 4's table points at them.
>
>   **How this revision was checked.** The second pass's executable model (scenarios
>   A, B, C, C2, D, E and F) was extended to encode this revision's rules as worded,
>   using the real `Artifact`, `EvidenceRecord`, `ArtifactIntegrity.sign`,
>   `ArtifactValidator`, `ArtifactRepository` and `student_t_two_sided_p`. It is a
>   scratch model, not a test, and it is not in the repository. A model written by
>   the author is not an independent pass. What it showed is written down as tests
>   53-60, which the implementing change must run red first. **It found one
>   defect in this revision's first wording**, recorded at rule 3h: "the nearest
>   version that passes 3c" let a genuine Demote review stacked on a forged version
>   supply `Limited Capital` (scenario C3), so the base must also end upward.
>
> **Four independent passes, ten blocking defects against this ADR, none found by
> the author** (3, 2, 3 and 2, in the order above; B7, shared with ADR-016, is not
> counted). That is the pattern this repository has recorded for every session that
> has attacked this ADR, and it is why the Required Follow-Up asks for another pass
> rather than treating this revision as settled.

> **Nothing here is ratified.** No framework or other implementation code was
> written for ADR-015. The public carrier PR #7 (`adr/015-stage-is-carried`) also
> carries the evidence-bar proposal and associated checklist/record material; this
> ADR text is not the only file on that branch.

---

## Context

**Two findings, one hole.** Both are live against `main` at `cc80866` and both were
re-executed for this draft rather than taken from their reports.

**F-007 — a strategy can be signed into existence at Production.**
`docs/HANDOFF.md:3788`, ruled for fix by the owner 2026-08-14
(`docs/OwnerDecisions.md:935`, guarantee at `:952`). `ArtifactFactory.create()`
refuses to mint a STRATEGY past `IDEA` (`framework/artifacts/factory.py:61-71`) and
`ArtifactIntegrity.sign()` (`framework/artifacts/integrity.py:71-80`) is a public
classmethod that will hash anything handed to it. Re-run for this draft:

```
F-007 verify_hash : True
F-007 validates   : True
F-007 reloaded    : StrategyLifecycle.PRODUCTION
```

Three further paths reach the same place and were opened:
`ArtifactSerializer.load()`, which returns `Artifact(**values)` at
`framework/artifacts/serializer.py:134`; a hand-edit followed by a re-sign; and
`dataclasses.replace()` followed by a sign. Three paths are closed: the factory
guard above, a hand-edit *without* a re-hash
(`framework/artifacts/repository.py:179-190`), and `validate_transition`
(`framework/artifacts/validator.py:114-131`) — which guards *movement* and is never
consulted about *birth*.

**F-014 — a promotion can be recorded with no evidence whatsoever.** The durable
number for the finding that `reports/review/2026-08-21-review.md:125` heads
"F-007"; that report's correction block is authoritative and its headings are not.
`review_artifact()` takes `stage_at_review` as a declared parameter and takes no
evidence at all (`framework/artifacts/review.py:70-84`); it checks justification
only (`:131-136`); and it requires no evidence: `**kwargs` would forward an
`evidence=` argument to the factory (`:83`, `:167-174`), but nothing asks for one and
nothing refuses its absence. *(Corrected 2026-09-24, finding N1: this sentence said
"passes no evidence", which `**kwargs` makes false.)* Re-run — a
`PROMOTE` from `Promotion Review` to `Micro Capital` justified `"Looks good."`:

```
F-014 evidence    : () level: None
F-014 validates   : True
```

`constitution/Paper_First_Capital_Doctrine.md:45-47` — "Promotion requires
evidence. Never confidence alone" — is enforced nowhere in `framework/`.

**Why they are one ruling.** A REVIEW artifact becomes the currency that buys a
rung. If that currency can be minted in one call with no evidence, the ladder is
decoration. Ruling F-007 without F-014 would move the hole rather than close it.

### The version test for "birth" is rejected on executed evidence

The 2026-08-14 proposal named *version `1.0.0` with no `parent_hash`* as the test
for creation rather than advancement. `docs/OwnerDecisions.md:976-981` declined to
rule it and told the next reader to attack it. Attacked three ways:
`version="2.0.0", parent_hash="0"*64` on a STRATEGY at `PRODUCTION` validates
`True`; `git grep -n "parent_hash=" -- framework/ scripts/` returns no matches, so
no production code sets the field; and no document in `constitution/`, `Knowledge/`
or `strategies/` names it.

The finding survives intact, as `docs/OwnerDecisions.md:980` said it would — only
the shape changes. **The shape is a ladder, not a version number.** `parent_hash`
returns in rule 3a in a different role: not a test for birth, but the link saying
*which* stored version a new version supersedes. That is the job
`framework/artifacts/integrity.py:25-27` already assigns it — "it binds an artifact
to the version it superseded, and an unprotected link can be repointed" — and the
reason it is inside the signature at `framework/artifacts/integrity.py:63`.

### The precedent this copies is one file over

`framework/artifacts/validator.py:226-238` re-derives `evidence_level` and refuses
a mismatch, for the reason its own comment gives: without it, an artifact built by
calling `Artifact()` directly could claim Level A while carrying nothing but
hypotheses, "and that claim is what a promotion gate reads". `strategy_stage` is
the same kind of claim read by the same kind of gate, and `_validate_lifecycle`
(`framework/artifacts/validator.py:145-169`) checks only that it *is* a
`StrategyLifecycle` — never *which*, and never *how it got there*.

### What the governing documents require, read in full for this draft

- **`constitution/Paper_First_Capital_Doctrine.md:5-7`** — "Every strategy begins
  with zero capital. No exceptions." Unconditional, and the constraint this ADR may
  not conclude around.
- **`constitution/Paper_First_Capital_Doctrine.md:45-47`** — "Promotion requires
  evidence. Never confidence alone."
- **`constitution/Immutable_Laws.md:23-25`** (Law III) — "No strategy is entitled
  to capital. Capital must be earned."
- **`constitution/Immutable_Laws.md:39`** (Law V) — "No department may bypass
  validation."
- **`constitution/Evidence_Standards.md:7-35`** — the four evidence classes,
  implemented as `EvidenceLevel` at `framework/artifacts/enums.py:4-13` and ranked
  at `framework/artifacts/enums.py:21-26`.
- **`constitution/Evidence_Standards.md:45`** — "Every conclusion must reference
  supporting evidence." **This is the sentence owner selection 5 applies.**
- **`constitution/Promotion_Pipeline.md:71-83`** — the seven promotion criteria,
  ruled canonical by ADR-006 rule 1.
- **`strategies/Lifecycle.md:39`**, **`:41`** — "Strategies may move backward."
  "Strategies never skip stages."
- **`strategies/Registry.md:43`** — "Every strategy exists in exactly one lifecycle
  stage."
- **`workflows/Monthly/StrategyPromotion.md:43`** — "Every decision requires written
  justification." **Cited at `:43` knowingly:** nine tracked locations cite `:37`,
  where the word is `Demote`. F-020 of `reports/review/2026-09-04-review.md:155`,
  not this branch's to fix.

**What none of them say, checked rather than assumed: no document maps a lifecycle
stage to a required evidence class.** That gap is what owner selection 4 sends to
research, and it is why rule 4 carries a slot instead of a number.

---

## Decision

### Rule 1 — A post-`IDEA` STRATEGY artifact carries its ladder, in signed content

Under the `content` key `ladder`, oldest rung first. **The key appears exactly
once.** `content` is a tuple of pairs and nothing forbids a duplicate key;
`dict(artifact.content)` silently keeps the last — verified,
`dict((("ladder","A"),("ladder","B")))` is `{'ladder': 'B'}` — so two `ladder` keys
would give a reader one history and a checker another.

**A rung is exactly five strings**, in this order:

`(from_stage, to_stage, review_id, review_version, review_integrity_hash)`

- `from_stage`, `to_stage` — a `StrategyLifecycle` **value**, one of the nine
  strings at `framework/artifacts/enums.py:85-93` (`"Idea"`, `"Paper Trading"`, …).
  Not member names, not free text. Values because that is what
  `ArtifactIntegrity.canonical_payload` already stores for `strategy_stage`
  (`framework/artifacts/integrity.py:33-35`) and what the serializer reconstructs
  members from (`framework/artifacts/serializer.py:43-49`).
- `review_id` — valid under `framework/identifiers.py`, `REV` prefix.
- `review_version` — a semantic version, as `is_semantic_version` defines it
  (`framework/artifacts/primitives.py`). **Without it, rule 3 would resolve a review
  through `get(id)`, which answers with `latest()`
  (`framework/artifacts/repository.py:168-169`)**, so the first ADR-005 revision of
  any review would make every strategy citing it unreadable.
- `review_integrity_hash` — that review *version's* `integrity_hash`, 64 lowercase
  hex. The hash and not merely the id, because a name can be repointed.

**In `content` rather than a new `Artifact` field.** ADR-009 rule 8's reasoning:
`Artifact` fields are inside the integrity hash, so every field added is permanent.
`content` is inside the hash too (`framework/artifacts/integrity.py:55`).

**The artifact also carries a `Validated By` relationship** whose targets are the
ladder's `review_id`s, **in ladder order**, and **the key `Validated By` appears at
most once in `relationships`**. `relationships` is a tuple of pairs like `content`
(`framework/artifacts/artifact.py:63`), so the same duplicate-key hole exists there
and is closed the same way. `Validated By` already exists
(`framework/artifacts/relationships.py:35`); no twelfth type is invented, which is
the constraint `Knowledge/Relationships.md` and the validator's vocabulary check
(`framework/artifacts/validator.py:171-190`) impose.

**The edge is required and it is compared — rule 2 step 8.** It is kept rather than
dropped because `relationships` is what a graph traversal reads and `content` is
not. It is a coarser projection by design: it names the review, the ladder names
the exact version.

**What the edge means, including on the way down (DRAFTER; finding N6).** A
`Validated By` target is a review that *decided* one of this strategy's stage moves,
whichever way it went. A `Demote` or `Retire` review is on the edge too, because the
edge mirrors the ladder, and the ladder records every move. "Validated" is read as
"the move was validated by a review", not "the strategy was approved". This reads
oddly for a demotion. The alternatives are a second edge per direction, using
`Rejected By` (`framework/artifacts/relationships.py:36`) for downward rungs, or a
twelfth type, which rule 1 refuses. Put to the owner at ratification; until then,
one edge in ladder order.

**Rule 1 is SELECTED (9e(i), "Carry proof + check storage").** The five-string
rung, the `content` key and the edge are DRAFTER.

### Rule 2 — `ArtifactValidator` re-derives the stage from the ladder

For `ArtifactType.STRATEGY`, in `_validate_lifecycle`, in this order. **Every step
is checkable from the artifact alone and performs no I/O.**

1. `content` carries the key `ladder` **at most once**.
2. **`strategy_stage is IDEA` if and only if the ladder is absent or empty.** Both
   directions.
3. Every rung is a sequence of **exactly five** elements, **each of them a string**.
   `from_stage` and `to_stage` each equal one of the nine values at
   `framework/artifacts/enums.py:85-93`; `review_id` valid under
   `framework/identifiers.py`; `review_version` a semantic version;
   `review_integrity_hash` 64 lowercase hex characters.
4. Rung 0's `from_stage` is `"Idea"`.
   `constitution/Paper_First_Capital_Doctrine.md:5-7` is the whole of this line.
5. **Chaining, between rungs.** For every `i > 0`, rung `i`'s `from_stage` equals
   rung `i-1`'s `to_stage`.
6. **Legality, within each rung.** For **each rung individually**,
   `validate_transition(StrategyLifecycle(from_stage), StrategyLifecycle(to_stage))`
   passes (`framework/artifacts/validator.py:114-131`). Asked rather than
   re-decided, on the ground `framework/artifacts/review.py:277-282` already gives.
   **The strings are converted to members first, with `StrategyLifecycle(value)`.**
   Passing the rung's strings directly does not work: `_table_for`
   (`framework/artifacts/validator.py:133-138`) tests `isinstance` against the two
   enum classes, and a plain `str` is neither, so `validate_transition("Idea",
   "Research")` raises "Not a lifecycle stage" (finding S13, executed). Step 3 has
   already refused any string that is not one of the nine values, so the conversion
   cannot raise here.
7. The **last** rung's `to_stage` equals `strategy_stage`. **This is the
   re-derivation**, the same factory-computes / validator-verifies split already
   used for the integrity hash and for `evidence_level`
   (`framework/artifacts/validator.py:226-238`). The last rung and not the highest:
   see rule 3d.
8. `relationships` carries `Validated By` at most once, and its targets, as a
   sequence, equal the ladder's `review_id`s in ladder order.

A bare `Artifact(..., strategy_stage=PRODUCTION)` carries no ladder and is refused
at step 2.

**What the validator alone cannot check.** It receives one artifact and no
repository. **It cannot resolve an identifier.** A ladder of seven well-formed rungs
naming seven reviews that were never written passes every step above. Rules 3b and
3c are where the record is checked.

**Rule 2 is DRAFTER**, implementing SELECTED 9e(i). Every step is internal
consistency; none is an owner ruling.

### Rule 3 — The repository runs rule 2, and checks what rule 2 cannot

**Marks.** Checking storage on save is SELECTED (9e(i)); checking on load is
SELECTED (9e(iii)); "longest history wins" is SELECTED (9e(vi)). The fixed
specification (3g) is RULED on capital stages (25c) and DRAFTER below them. Failing
toward less capital (3b's downward append, 3e's counting rule, 3h) is RULED (25d);
the mechanisms are DRAFTER. That an unresolved downward step lowers the read and
does nothing more, and is flagged for a human, is RULED (26a); the flag's shape is
DRAFTER. That reading a stage re-checks its evidence (3c) is RULED (26e); which
checks, DRAFTER. That a confidence change on a capital stage needs a recorded human
yes (3g) is RULED (26c); the mechanism, DRAFTER. Everything else in rule 3 is
DRAFTER.

**3.0 — the repository validates, and the scope is not the forger's to choose.**

`ArtifactValidator` is imported nowhere in `framework/artifacts/repository.py`; it
appears only in docstring prose, at `:140` and at `:156-160`, where `get()` argues
it is "not a second gate reimplementing the first" and that `ArtifactValidator`
"still owns identifiers, relationships, evidence grades and lifecycle rules, and
callers that need those still run it." **`framework/artifacts/repository.py:156-160`
is amended: the repository is a caller that needs those rules.**

`save()` and `get()` run `ArtifactValidator().validate()` for any artifact that is
**of type `STRATEGY`, or of type `REVIEW`, or carries a `strategy_stage` that is not
`None`** — whatever its declared type.

**The third clause is the fix for a defect found by execution.** Scoping on
`artifact.type` alone lets the forger opt out by mis-declaring the type. Run for
this draft against `main`: an artifact declared `ArtifactType.REPORT` and carrying
`strategy_stage=StrategyLifecycle.PRODUCTION` saved through `ArtifactRepository` and
came back from `get()` still carrying `PRODUCTION`. `ArtifactValidator` would have
refused it — `framework/artifacts/validator.py:165-169` forbids a `strategy_stage`
on a non-STRATEGY — but under a type-scoped rule the validator is never called. The
capital claim is the trigger, not the label on it.

**`type` is immutable across the versions of one identifier.** `save()` refuses an
artifact whose `type` differs from that of any stored version of the same
identifier. Run for this draft: today `STRAT-9200` version `1.0.0` can be a
`STRATEGY` and version `2.0.0` a `REPORT`, and both save and read back. Without
this rule an identifier could shed its type at a later version and step out of every
check above. **This rule binds every artifact type, not only the three in scope
above**, because the hole it closes is the ability to leave the scope.

**Scoped rather than universal, and the cost is stated.** Validating every artifact
on every read would change the behaviour of `artifacts/RPT-0001/1.0.0.yaml` and the
fetch-record round trip ADR-014 settled. **An unevidenced REPORT with no capital
claim still saves and still reads back.** That is the status quo, not an
improvement.

**Cost of the amendment itself:** `validate()` raises rather than returning False,
so `save()` and `get()` acquire a failure mode they did not have, on the path a
promotion gate sits on.

**3a — the predecessor: named by `parent_hash`, found by a scan that cannot be
poisoned**

For an artifact in scope, `parent_hash` is the `integrity_hash` of the stored
version this one supersedes. **`P` is the stored version of the same identifier
whose `integrity_hash` equals `artifact.parent_hash`, and `P.type` must be
`ArtifactType.STRATEGY`.**

- **Ladder empty, nothing stored under this identifier** — a birth at `IDEA`:
  `parent_hash` must be `None`.
- **Ladder empty, a version already stored** — an `IDEA`-stage revision, which
  ADR-005 permits as readily as any other: `parent_hash` must be set and must name a
  stored version that is itself at `IDEA` with an empty ladder.
- **Ladder non-empty**: `parent_hash` must be set and exactly one stored version
  must carry that `integrity_hash`.

**How the scan works, because leaving it undefined bricks identifiers.** The scan
reads each `{root}/{id}/*.yaml` through `ArtifactSerializer.load()` and compares the
**stored** `integrity_hash` field. **It does not call `get()` on siblings and it
raises on none of them.** A sibling that will not parse, or whose hash does not
verify, is skipped and reported, not raised on. This matters because under rule 3.0
`get()` *raises* on an invalid artifact, so a scan built on `get()` would let one bad
file in the directory make every future save of that identifier impossible — and
storage is append-only, so the bad file could never be removed and the identifier
(permanent and never reused, `Knowledge/Identifiers.md`) would be dead forever.
**Only the one version the scan selects is then fetched through `get()`**, which is
where it is verified and validated.

**Why `parent_hash` and not "the highest stored semantic version below this one".**
The field exists for this and says so (`framework/artifacts/integrity.py:25-27`,
inside the signature at `:63`). Inferring from version order is a guess where an
explicit link exists, and `framework/artifacts/repository.py:86-113` records that
reading version order to answer a capital question is the mistake `latest()` was
written to stop. **This requires `parent_hash` to be written by production code for
the first time** — a narrow widening of a field the schema and the signature already
carry, and **not** the rejected birth test, which asked whether the field was
*absent* rather than what it points at.

**3b — what `save()` requires beyond rule 3.0**

Let `L` be the new artifact's ladder and `r = L[-1]` its last rung. **Conditions 1
to 5 below govern a non-empty `L`.** Where `L` is empty the artifact is at `IDEA`,
rule 3a governs it alone, and the only branch of condition 3 that is defined is
Revision — `L[-1]` does not exist, so Append and condition 5 do not apply. A birth
has no predecessor; an `IDEA`-stage revision has one and reaches it through rule
3a. *(Stated because an earlier revision left the empty-ladder case to inference,
and walking the honest histories against the text is what surfaced it.)*

1. `P` resolves per rule 3a, and is fetched through `get(artifact.id, P_version)` —
   so `P` is integrity-verified, fully validated and rule-3c-checked on the way in.
   **Except for a downward append**, below.
2. **`P` is at the frontier** — rule 3e.
3. **Exactly one of these two holds:**
   - **Append.** `P`'s ladder equals `L[:-1]` exactly, **and** `P.strategy_stage ==
     r.from_stage`, **and** the artifact's specification equals `P`'s (rule 3g).
   - **Revision.** `P`'s ladder equals `L` exactly, **and** `artifact.strategy_stage
     == P.strategy_stage`, **and**, when `L` is non-empty, the artifact differs from
     `P` only in the fields rule 3g makes revisable. *(Finding B1: this clause is
     new. Without it a Revision needed only an equal ladder and an equal stage, so
     strategy B's rules could be saved as a Revision of strategy A at Limited
     Capital, with no review.)*

   *(Named **Append** and not "Climb" deliberately: it covers demotion and
   retirement rungs identically, so nobody reads "climb" and skips condition 5 for a
   move that goes downward.)*
4. No `(review_id, review_version)` pair appears in more than one rung of `L`.
5. In the **Append** case, the review resolves. `get(r.review_id, r.review_version)`
   must return `R` with:
   - `R.type is ArtifactType.REVIEW`;
   - `R.integrity_hash == r.review_integrity_hash`;
   - `review_fields(R)["subject_id"] == artifact.id`;
   - `review_fields(R)["stage_at_review"] == r.from_stage` and
     `["resulting_stage"] == r.to_stage`;
   - `review_fields(R)["subject_version"] == P_version` **and**
     `["subject_integrity_hash"] == P.integrity_hash`;
   - `review_fields(R)["subject_ladder_length"] == len(L) - 1`.

**Condition 4 and the last two bullets of condition 5 stop one review buying two
rungs.** `STRATEGY_TRANSITIONS` (`framework/artifacts/validator.py:94-100`) admits
`Production → Paper Trading` and the forward moves admit a climb back, so a ladder
can legally hold two rungs with an identical stage pair.

**The Revision branch exists because ADR-005 requires it**: a confidence revision
produces a new version, so a STRATEGY must gain a version without gaining a rung.
The two branches are exclusive and exhaustive — **a new version either exactly
reproduces the ladder of the version it supersedes, or appends exactly one rung to
it.** A shorter ladder, a rewritten rung, a stage change with no new rung, and a new
rung with the stage left behind are all refused, and each has a named test below.

**A downward append needs only integrity, rule 2 and the frontier check — RULED
(25d, "It never refuses in a way that would block a demotion"; 18b); mechanism
DRAFTER; finding S2.** An Append whose new rung is downward — `r.to_stage` is
`"Retired"`, or its `STRATEGY_LADDER` position is below `r.from_stage`'s, classified
exactly as rule 4's direction clause does — is saved when:

- `P` is read by rule 3a's scan and passes integrity and `ArtifactValidator` (which
  includes rule 2), **without** rule 3c. If `P`'s own last review has been damaged
  or deleted, the demotion still saves. Under the previous draft `P` was fetched
  through `get()`, whose rule 3c refused, so a damaged review made every Demote and
  Retire of that strategy impossible, which contradicts 18b;
- the frontier check of rule 3e holds **with `P` counted on integrity and the
  validator alone**, so an honest `P` that lost its review is still the frontier;
- conditions 3 and 4 hold, and condition 5 holds for the **new** rung's review. That
  review is written by the person demoting, and carries at least one evidence
  record and no grade floor (rule 4, 18b). It is the record of the demotion itself,
  so it cannot be damaged before it exists.

Nothing about the old record is re-checked on the way down. What a damaged record
cannot do is carry a strategy *up*: an upward append still fetches `P` through
`get()` with rule 3c.

**3c — what `get()` does: one level, non-recursive, and why the previous draft's
claim was false**

Owner selection 3. For an in-scope artifact, `get()` performs the integrity check it
already performs, runs rule 2, and then **a bounded number of extra reads, each
named below, and no more**:

- **The predecessor exists and is a legal one.** For a STRATEGY with a non-empty
  ladder: the version named by `parent_hash` is stored under this identifier, is
  `ArtifactType.STRATEGY`, is integrity-verified, passes rule 2, and satisfies rule
  3b condition 3 — Append or Revision — against this artifact, including rule 3g's
  confidence condition (26c).
- **The last rung's review exists and says what the rung claims.** `(review_id,
  review_version)` is stored, is integrity-verified, is typed `REVIEW`, carries
  `integrity_hash == review_integrity_hash`, **passes the full
  `ArtifactValidator().validate()`**, **and satisfies every sub-check of rule 3b
  condition 5.** Re-running those sub-checks rather than only matching the hash
  is deliberate: matching the hash proves the file is the one named, and the
  sub-checks prove the named file is *about this rung*.
- **Condition 5 is checked against the version that appended the last rung, not
  against this artifact's predecessor (DRAFTER; second-pass finding 2N3).** The
  review of rung `r = L[-1]` was written about the version that `r` was appended
  to. For an Append that is this artifact's predecessor. For a Revision it is not:
  the predecessor carries the same ladder `L`, and a review of it would need
  `subject_ladder_length == len(L)`, which condition 5 refuses. Worded against the
  predecessor, as the previous revision was, **every honest confidence Revision after
  the first rung failed rule 3c**. So in both cases the review's subject is located
  by rule 3a's scan: the stored version of this identifier whose stored
  `integrity_hash` equals the review's `subject_integrity_hash`. It must be
  integrity-verified, carry version `subject_version`, and carry ladder exactly
  `L[:-1]`. For an Append this is the predecessor already read, so it costs nothing.
  For a Revision it is one more read.
- **The last review's bound reports resolve, and ADR-016 rule 8 holds — RULED (26e):
  "The current-stage read resolves the last review's bound reports and applies
  ADR-016 rule 8, not only the validator."** Second-pass finding 2N12. When the last
  rung is upward, every report the review binds under ADR-016 rule 3 is resolved and
  checked as ADR-016 rule 3 checks 2-6 and rule 2 checks 5-6 define (resolution
  through a read that recomputes the hash, type, grade, subject, disclosures, the
  allowlist and the grade its producing module writes), and ADR-016 rule 8 is
  applied to the bound significance report. Which checks: DRAFTER. One read per bound
  report: none for a rung below `Paper Trading`, at least one at `Paper Trading`, and
  at least seven on a capital rung (ADR-016 rule 2). A downward rung binds no reports
  (ADR-016 rule 3), so a demotion adds no read here.
- **A confidence authorization, where rule 3g requires one (26c).** One more read:
  the review named by the Revision's `confidence_review`.

**Every read above uses an internal one-level read — load, integrity-verify, and the
full `ArtifactValidator().validate()` — and calls `get()` on nothing.** *(Finding B3:
the previous draft read "load, integrity-verify, rule 2", so the review's own
checks — rule 4(c)'s evidence requirement and every check ADR-016 adds — ran only
when the review itself was saved or fetched. Three hand-written files, a
predecessor, a review with no evidence and a strategy at `Micro Capital`, then read
back as `MICRO_CAPITAL` while `MINIMUM_PAPER_TRADING` was `None`.)* **The validator
performs no I/O**, so this adds no read: on the review it runs rule 4(c) and every
ADR-016 check that needs nothing but the review itself — the grade floor, the
per-criterion shape, the rung closures (`MINIMUM_PAPER_TRADING` and the live-rung
minimums, 18d and 25e), the recorded human authorization (25f), `variants_tried`
and `bar_version` (25g, 25h). **Resolving the bound reports and rule 8 are now in
this read too (26e, the fourth bullet above).** The ADR-016 checks that read *other*
reviews or the whole store — rule 3 check 7 (every report considered is listed),
rule 6 checks 3-4, rule 10's non-decreasing `bar_version`, and rule 4(f) — still run
only in `save()` and in rule 3f's sweep. If any read called `get()`, reading a
strategy at `PRODUCTION` would walk seven predecessors and seven reviews and each
review would want its subject. `framework/artifacts/repository.py:129-166` argues
for a bounded read path and says it is "not a second gate reimplementing the
first"; a count fixed by the last rung is bounded, a traversal is not.

**Cost, stated against 9e(iii)'s "Two extra reads, bounded".** The owner selected
two. 26e is the later ruling and requires more: on a capital rung, the predecessor,
the review, and at least seven reports; on a Revision, one more for the review's
subject. The number is still fixed by the last rung and never grows with the length
of the history.

**The second draft said `save()` having checked every link "guarantees that every
rung in a stored ladder went through `save()`". That sentence was false and is
withdrawn.** It was disproved by execution: one hand-written, re-signed YAML at
`<root>/STRAT-0001/8.0.0.yaml` — stage `Production`, a seven-rung ladder naming
`REV-9001` to `REV-9007`, `parent_hash` of `"f"*64`, a matching `Validated By` edge
— was returned by `get()` as `PRODUCTION` with all eight rule-2 steps passing and
**zero reviews on disk**. Nothing a write-time check does constrains a file that
never went through the write path. That is what owner selection 3 fixes, and it is
what this rule now does.

**An `IDEA`-stage revision's parent link is checked by `save()` (rule 3a) and is not
re-checked on read**, because no rung and therefore no capital claim depends on it.
The reads above are spent where a stage is being asserted.

**What `get()` still does not catch, stated exactly.** It checks one level: the
immediate predecessor and the *last* rung's review. It does **not** check rungs `0`
to `n-2`, their reviews, or the predecessor's own predecessor. A strategy whose
seventh-from-last review was deleted still reads back. That is the chain sweep's job
— rule 3f.

**3d — backward moves, and they are not an exception**

Read from `STRATEGY_TRANSITIONS` (`framework/artifacts/validator.py:57-102`) rather
than guessed: backward moves of any distance down to a `PAPER_TRADING` floor, plus
`RETIRED` from anywhere; ADR-004 ruled those ten demotions. **A demotion is a rung
like any other.** It appends `("Production", "Paper Trading", "REV-00NN", "1.0.0",
<hash>)`; ADR-004 rule 4's written justification is already enforced at
`framework/artifacts/review.py:131-136`; and under owner selection 5 it now also
carries evidence — rule 4. **The ladder is a history, not a path**: it never shrinks,
and a demoted strategy's ladder is *longer* than a never-demoted one's, which is why
rule 2 step 7 reads the last rung rather than the highest. A strategy at `RETIRED`
has a final rung and no legal successor, because `STRATEGY_TRANSITIONS[RETIRED]` is
empty. `strategies/Lifecycle.md:39` and `:41` are satisfied by delegating rather than
re-deciding.

**3e — longest history wins; there are no forks, and a mistake is corrected forward**

Owner selection 6. **This replaces the first revision's "forks are left legal",
which the second pass showed was not merely untidy but exploitable.**

**The frontier.** Among the *counted* stored versions of an identifier (defined
below), let `Lmax` be the longest ladder. **A version is at the frontier when its
ladder equals `Lmax`.** Rule 3b condition 2 requires `P` to be at the frontier, and
with rule 3b condition 3 that gives exactly:

- **Append:** `L[:-1] == Lmax`, so `len(L) == len(Lmax) + 1` and `Lmax` is a proper
  prefix of `L`.
- **Revision:** `L == Lmax`.

Therefore **`Lmax` must be a prefix of `L`, and `len(L) - len(Lmax)` must be 0 or
1.** Read off the consequences rather than left to inference:

- A ladder **shorter** than `Lmax` is refused **even when it is an honest prefix of
  it**. History does not get shorter.
- A ladder of **equal length but different content** is refused: equal length with
  different content means `Lmax` is not a prefix.
- A ladder **longer by two or more** is refused.
- **Revising the latest version stays legal**, which it must — ADR-005 mandates that
  a confidence change produces a new version. The Revision branch is exactly that
  case.
- **Revising an older version is now refused.** Its ladder is a strict prefix of
  `Lmax`, so it is not at the frontier. **This is a real loss and it is stated
  rather than buried:** a mistake recorded three versions ago cannot be corrected in
  place. Owner selection 6 is the ruling that it should not be — **a mistaken save
  is corrected by appending a correcting rung with its own review, never by going
  back** — and that is consistent with what this repository already does everywhere
  else with superseded prose: annotate forward, never rewrite
  (`strategies/Lifecycle.md:51-59` is the pattern).
- **The second pass's B2 forgery dies here** (not the 2026-09-24 pass's B2, which is
  rule 3e's counting rule below). Honest `4.0.0` at `Production`, honest demotion
  `5.0.0` to `Paper Trading` (so `len(Lmax) = n+1`), then `6.0.0` with
  `parent_hash = hash(4.0.0)` and `4.0.0`'s ladder: `P` is `4.0.0`, whose ladder has
  length `n ≠ len(Lmax)`, so `P` is not at the frontier and the save is refused.
  Under the second draft the Revision branch held, `latest()` returned `Production`,
  and no review was involved. **The same move un-retired a `RETIRED` strategy**,
  which rule 3d forbids in prose and nothing enforced.
- **And one review can no longer be cited for the same rung in two forks**, because
  there are no forks. That closes it without a further rule.

**Several versions may share `Lmax`, and that is not a fork.** Successive same-stage
revisions of the frontier all carry the identical ladder, so all are at the frontier
and any of them may be built on. They are not competing histories — the history is
the same object in each — and the first Append made from any of them advances `Lmax`,
after which every other frontier sibling stops being at the frontier and no second
Append can be made. `latest()` continues to pick one, as it does today. **A fork
requires two *different* ladders of the frontier length, and the prefix rule refuses
the second of those outright.**

**Which stored versions count.** A version counts toward `Lmax` only if it parses,
its integrity hash verifies, it is `ArtifactType.STRATEGY`, it passes
`ArtifactValidator` (which includes rule 2), **and it passes rule 3c** — a version
with an empty ladder passes 3c trivially. A version that fails is **skipped and
reported, never raised on**, as in rule 3a.

**This replaces the previous revision's first clause, which counted a version whose
last rung was downward without rule 3c.** That clause was the drafter's mechanism
for 25d, and the previous revision labeled it RULED; only the principle was ruled
(second-pass nit). It had two effects the rulings do not allow:

- **It let one forged file supply a stage** (second-pass finding 2N1). Rule 3h
  treated such a version as established, so a single hand-signed file climbing to
  `Production` and stepping down to `Limited Capital`, with no review on disk, read
  as `Limited Capital`. Rule 3h's base (below) is the fix; this clause no longer
  feeds it.
- **It let one forged file retire a strategy permanently** (2N4). A counted
  `Retired` version is the frontier, `Retired` has no legal successor
  (`framework/artifacts/validator.py:57-102`), so no honest version could ever be
  saved again. **RULED (26a): "A downward step whose review does not resolve lowers
  the stage read now, and nothing more. It never makes a Retire final and never
  bars earlier evidence under 25i. It is flagged for a human to repair."** So such a
  version does not count toward the frontier, and honest saves continue from the
  last counted version.

**What still stops a deleted review from undoing a demotion (B2).** Not the frontier
any more: the current-stage read. With the demotion review of `v6` deleted, `v6`
fails 3c and stops counting, and `v7`, a Revision of `v5` at `Production`, now saves.
But `v6` is still a readable tip, and rule 3h lowers every tip's stage by every
downward rung after its base, whether that rung's review resolves or not, and flags
it. The read returns `Paper Trading`. If `v6`'s *version* file is deleted instead,
rule 3h step 5 reads the stored `Demote` review through the subject index and
returns `Paper Trading` again (2N2). **Only deleting both files undoes the demotion,
and then only git history shows it** (rule 3h, "The residual").

**The cost, stated.** Anyone who can write one file that passes integrity and the
validator can lower the stage Belay reads: a forged downward rung lowers the read
without its review. That is a denial of capital, not a grant of it, and 25d chose it.
Since 26a it no longer blocks saves, never makes `Retired` final, and never bars
evidence under rule 4(f); it is flagged on every read until a human repairs it.

**A forged file dropped into the directory does not own the identifier for free:**
a long ladder naming reviews that do not exist fails rule 3c and is not counted, so
it neither becomes `Lmax` nor blocks honest saves, whichever way its last rung goes.

**The residual denial of service, admitted rather than argued away.** A forger who
*also* writes the predecessor file and the review file that rule 3c checks can
produce a counted ladder longer than the honest one. Storage is append-only, so it
can never be removed; `Knowledge/Identifiers.md` makes identifiers permanent and
never reused, so the identifier cannot be abandoned and replaced. **The honest
history would then have to continue by appending to the forgery.** This is the price
of "longest history wins", it is real, and the only defences against it are the ones
outside this ADR: write access to the repository, git review of a tracked directory,
and rule 3f's sweep. Named here so it is a decision rather than a discovery.

**3f — the chain sweep**

A repository-wide check: for every stored STRATEGY version, resolve **every** rung's
review and **every** predecessor back to `IDEA`, and report anything unresolvable,
any counted ladder that is not a prefix of `Lmax`, and any identifier with more than
one `Lmax`. **On every rung it runs what rule 3c runs on the last one, and more**
(finding B3): the full `ArtifactValidator` on each version and each review; every
sub-check of rule 3b condition 5; rule 3g's fixed specification on each link;
ADR-016's report resolution for every bound report on every review; and rule 4(f)'s
refusal of evidence reused after a demotion. This is the only thing that catches
what rule 3c's one level does not.
It is the shape ADR-014 rule 7 already rules for orphaned store versions and
`tests/data/test_store.py:238-267` already implements for them, on the convention
`tests/data/test_store.py:206-227` states: ask the system, not the prose. **It is
Required Follow-Up, not a `get()` behaviour**, because its cost is proportional to
the whole store.

**What the sweep adds to rule 3c.** Rule 3c checks the last rung, including its
bound reports and ADR-016 rule 8 (26e). The sweep checks every rung, every
predecessor back to `Idea`, the store-wide checks rule 3c does not make (ADR-016
rule 3 check 7, rule 6 checks 3-4, rule 10's non-decreasing `bar_version`, rule
4(f)), and lists every repair flag rule 3h raises. *(Replaced 2026-09-25, finding
2N12: this paragraph was the residual "a forged review whose bound reports do not
exist passes rule 3c". 26e ruled that 3c resolves them, so the residual is gone,
not reworded.)*

**3g — the specification is fixed once a strategy has climbed; a changed
specification is a new identifier at `Idea`**

**RULED on the capital stages (25c): "A strategy's rules cannot change while it
holds a capital stage. A changed specification is a new strategy with a new
identifier, and it starts at Idea."** Finding B1.

**The revisable fields — DRAFTER, reading ADR-005 rule 2.** ADR-005 makes exactly
one field revisable: "A confidence revision produces a new version"
(`docs/DECISIONS.md:660-665`). A new version must also change the fields that make
it a new version. So, between a version with a non-empty ladder and its successor:

- **May differ on a Revision:** `confidence` (ADR-005 rule 2), subject to the
  condition below on a capital stage; the `confidence_review` entry of `content`,
  which exists only for that condition; and the version's own bookkeeping —
  `version`, `parent_hash`, `integrity_hash`, `created`, `updated`.
- **May also differ on an Append:** `strategy_stage`, the `ladder` entry of
  `content`, and the `Validated By` entry of `relationships` — the three things
  rule 1 says a rung changes.
- **Everything else is the specification and must be equal**, compared over
  `ArtifactIntegrity.canonical_payload` (`framework/artifacts/integrity.py:28-64`)
  with the entries above removed: `title`, `type`, `lifecycle`, `deliverable`,
  `evidence`, `evidence_level`, `tags`, `summary`, `schema_version`, `author`,
  `metadata`, every other `content` entry, and every other `relationships` entry.
  A refusal names the first field that differs.

**Confidence on a capital stage is a capital decision — RULED (26c): "Changing a
funded strategy's confidence needs a recorded human yes, as in 25f."** Second-pass
finding 2N10. Confidence sizes capital (`constitution/Capital_Authority.md:11-14`
names it among the inputs that determine capital), so a Revision that changes
`confidence` while the strategy holds a capital stage moves money without a review.
**DRAFTER — the mechanism.** When `strategy_stage` is `Micro Capital`, `Limited
Capital` or `Production` and a new version's `confidence` differs from its
predecessor's:

- **On a Revision**, `content` carries `confidence_review`: three strings,
  `(review_id, review_version, review_integrity_hash)`, naming a stored REVIEW whose
  outcome is `Remain Current Stage`, whose subject is the predecessor (by
  `subject_version` and `subject_integrity_hash`), whose `stage_at_review` and
  `resulting_stage` both equal the current stage, whose `resulting_confidence`
  equals the new `confidence`, and which carries ADR-016 rule 9's
  `human_authorization`. `save()` refuses the Revision otherwise, and rule 3c
  re-checks it on read (one more read). On every other Revision the key is absent.
- **On an Append**, the rung's own review must record `resulting_confidence` equal
  to the new `confidence` and carry ADR-016 rule 9's `human_authorization`. **A
  demotion is never blocked by this:** the person demoting leaves `confidence`
  unchanged, and then no authorization is asked for (25d). A later Revision can
  lower it with a human yes.

Below the capital stages a Revision may change `confidence` freely (DRAFTER). Today
no strategy can hold a capital stage (ADR-016 rule 5), so this rule binds nothing
until one can; ADR-016's 26f closure applies to it as to every capital authorization.

**DRAFTER: from the first rung, not only on capital stages.** 25c rules the capital
stages. This draft freezes the specification from the first rung, because every
rung below capital was bought with evidence about the specification it was bought
for: a Paper Trading rung earned by one set of rules and kept by another is the
same swap one rung lower. At `Idea` (empty ladder) nothing has been earned and every
field may change. Put to the owner at ratification.

**DRAFTER: the cost, stated.** A post-`Idea` strategy cannot change its title, tags,
summary, author or editorial `lifecycle` (`Draft` to `Approved`, ADR-003) in place.
Correcting a typo in a funded strategy's title means a new identifier. If the owner
wants any of those revisable, each is added to the list above by name, never by a
rule such as "anything outside `content`".

**What a changed specification does instead — DRAFTER mechanism.** It is saved as a
new identifier at `Idea`, with an empty ladder, carrying a `Derived From`
relationship (`framework/artifacts/relationships.py:34`) whose target is the
identifier it came from. The new identifier climbs from `Idea` with its own reviews
and evidence. The old identifier keeps its stage until its own review moves it; a
strategy that should stop trading is demoted or retired by review, as any other.
`Derived From` is what ADR-016's `variants_tried` lineage follows (25h), so a new
identifier cannot reset the count of variants tried.

**3h — the current-stage read: fail toward less capital**

**RULED (25d): "When the record is damaged or the versions disagree, Belay reads the
lowest stage it can establish. It never refuses in a way that would block a
demotion."** The mechanism is DRAFTER. Finding B2.

**The read, and its return value (DRAFTER).** The current-stage read is a new
repository method, `current_stage(id)`, returning a `StageRead`: the `stage` read,
the `version` of the tip it was read from, the tips that `disagree`, and a tuple of
`repairs` (step 6). It returns a stage, not an artifact, because the stage it reads
can be lower than the `strategy_stage` of every stored version (step 4). **`get(id)`
with no version, on an identifier whose stored versions are STRATEGY, raises and
names `current_stage()`**: today it returns whatever `latest()` names
(`framework/artifacts/repository.py:168-171`), which is the version a forger or a
deleted file can choose, and a caller reading its `strategy_stage` would be reading
exactly that. The read:

1. **Readable versions.** Rule 3a's scan: every stored version of the identifier
   that parses, verifies its integrity hash, is `ArtifactType.STRATEGY`, and passes
   `ArtifactValidator`. The rest are skipped and reported.
2. **Tips.** The readable versions whose ladder is not a proper prefix of another
   readable version's ladder. Versions with equal ladders are one tip; `latest()`
   picks among them, as today.
3. **Find each tip's base — second-pass finding 2N1.** Walk back from the tip. A
   version is the **base** when its ladder is empty (`Idea`), or when it passes
   rule 3c **and its last rung is upward**. Otherwise step to the readable version
   its `parent_hash` names, provided that version's ladder is a prefix of the
   current one's, and try again. **If the walk ends without a base — a predecessor
   missing, unreadable, or not a prefix — the read raises** (step 7).
4. **The tip's stage is the lower of the base's stage and every downward rung's
   `to_stage` after the base**, in the tip's own ladder. Upward rungs after the base
   are ignored: their reviews did not establish them. Downward rungs after the base
   lower the stage **whether or not their reviews resolve** — RULED (26a), "A
   downward step whose review does not resolve lowers the stage read now". **A
   downward rung may only lower a stage that is already established; it never
   supplies one.**
5. **Stored downward reviews lower the read too — second-pass finding 2N2.** Through
   the subject index (below), take every stored REVIEW whose `subject_id` is this
   identifier that passes integrity, whose `resulting_stage` is `Retired` or below
   its `stage_at_review` on `STRATEGY_LADDER`, and whose subject — the stored version
   named by `subject_version` and `subject_integrity_hash` — is readable. **It
   applies to a tip when the subject's ladder is a prefix of the tip's ladder** (the
   subject is at or before the tip's position) **and the tip's ladder does not carry
   that review as its rung at the subject's position.** It then lowers that tip's
   stage to the lower of its stage and the review's `resulting_stage`. Integrity
   alone qualifies it, not the validator: a demotion is never refused (25d, 18b). A
   review the tip's ladder does carry is already in the history, and an honest
   re-climb after it is not lowered again.
6. **The repair flag — RULED (26a): "It is flagged for a human to repair."** The
   flag's shape is DRAFTER. `StageRead.repairs` holds one entry per defect this read
   saw, each `(identifier, version, rung_index, review_id, review_version, reason)`,
   with `rung_index`, `review_id` and `review_version` `None` where they do not
   apply, and `reason` one of exactly five codes:
   - `DOWNWARD_REVIEW_UNRESOLVED` — a downward rung after the base whose review is
     not stored, fails integrity, is not a REVIEW, carries another hash, or fails
     rule 3b condition 5. It lowered the read (step 4);
   - `UPWARD_REVIEW_UNRESOLVED` — an upward rung after the base whose review does
     not resolve. It was ignored (step 4);
   - `VERSION_FAILS_3C` — a version the walk stepped past because it failed rule
     3c, with 3c's refusal appended to the code;
   - `STORED_DEMOTION_NOT_IN_LADDER` — a review applied by step 5;
   - `NO_BASE` — the walk found no base (step 7).

   `StageRead.needs_repair` is `True` whenever `repairs` is non-empty. **The flag is
   recomputed from the store on every read. It is never stored, so nothing can clear
   it but a repair of the store itself**: a person restoring a deleted file from git
   history, removing a forged file in a reviewed commit, or appending a correcting
   rung with a review that resolves (owner selection 6). Belay never repairs itself.
   Rule 8 says what a consumer does with a flagged read; rule 3f's sweep lists every
   flag in the store. An honest demotion is never flagged: its rung's review
   resolves.
7. **The result.** **One tip: its stage. More than one: the lowest** — `Retired`
   lowest of all, then by `STRATEGY_LADDER` position — with the disagreeing tips
   named. **If any tip has no base, the read raises**, naming the tip and carrying
   the repairs. **Every consumer of the capital read treats a raise as zero
   capital** (rule 8). A refusal to read never keeps capital deployed.

**Why the base must end upward, found by execution while drafting this revision.**
The first wording of step 3 was the pass's: "the nearest version that passes 3c". The
model then built this: an honest strategy at `Paper Trading` (`v4`); a forged `v5`
that climbs, in one file, to `Production`, naming reviews that do not exist; a
**genuine**, integrity-valid `Demote` review of `v5` to `Limited Capital`, which
anyone can write, because a downward review has no grade floor (18b); and `v6`
appending that rung. `v6` passes rule 3c: its predecessor `v5` is stored, readable
and a legal Append, and its last review resolves and satisfies condition 5. Under
that wording `v6` was the base and the read was `Limited Capital`, a capital stage
supplied by a downward rung. With the base required to end upward, the walk passes
`v6` (ends downward) and `v5` (fails 3c) and stops at `v4`: the read is `Paper
Trading`, with the four forged upward rungs flagged.

**Why the walk accepts any stored prefix, not only a predecessor one rung shorter.**
A forged file can add several rungs at once. Requiring exactly one would end the walk
at it and raise, so one forged file would take an honest strategy at `Paper Trading`
to zero. 25d asks for "the lowest stage it can establish", and the honest base is
still there to establish.

**The attacks, as this read answers them** (each executed in the scratch model named
in the revision history):

- **One hand-signed file, seven rungs up to `Production` and one down to `Limited
  Capital`, no reviews and no predecessor on disk** (the second pass's model C). No
  base: the read raises, which is zero capital.
- **A forged extension of an honest `Paper Trading` ladder, ending downward at
  `Micro Capital`** (model C2). Base `v4`; the read is `Paper Trading`, flagged.
- **One forged file stepping `Paper Trading → Retired`** (model D). The read is
  `Retired`, flagged `DOWNWARD_REVIEW_UNRESOLVED`. The forged version is not counted
  (rule 3e), so the frontier is still `v4` and an honest Append saves. `Retired` is
  not final (26a).
- **B2 by deleting the demoted version file** (model F). With the demoting version
  deleted and its `Demote` review still stored, step 5 applies the review to the
  remaining tip, the version at `Production`: the read is `Paper Trading`, flagged
  `STORED_DEMOTION_NOT_IN_LADDER`.
- **B2 by deleting the demotion review** (the previous revision's attack). The
  demoting version is still a tip; its base is the version before it; step 4 lowers
  the read by its downward rung. `Paper Trading`, flagged
  `DOWNWARD_REVIEW_UNRESOLVED`. **An honest re-climb is not a disagreement**: after a
  demotion and later climbs, the demoting version's ladder is a prefix of the newest,
  so there is one tip.

**The residual — stated, not closed.** If **both** the demoting version file and its
`Demote` review are deleted, nothing left in the store records the demotion, and the
read returns the stage before it. The model shows exactly that: `Production`, with
no flag. **Only git history shows it**, because the artifact root is tracked
(ADR-014 rule 2) and a deletion is a commit. Storage is append-only by rule, not by
mechanism; the defence against deleting two files is the same as against any other
edit of a tracked directory: write access and review.

**The subject index — required infrastructure (DRAFTER).** Step 5 needs every stored
review whose subject is this identifier, and the repository lists only one
identifier's versions (`framework/artifacts/repository.py:69-84`). ADR-016 needs the
same index for reports (its rule 3 check 7). **It is derived from the store's
contents, rebuildable by a full scan, and never a separately maintained file**, so
deleting or editing the index cannot hide a review; an index that disagrees with a
scan is a defect the sweep reports. Listed in the Required Follow-Up. Until it
exists, step 5 is a full scan of stored REVIEWs.

**Cost, stated.** The previous draft's read opened two extra artifacts (SELECTED
9e(iii), "Two extra reads, bounded"). This read also lists and parses every stored
version of the one identifier, runs rule 3c's reads (now more than two, rule 3c) on
each version the walk tries — one in the honest case, two when the tip is an honest
demotion — and reads the stored downward reviews of this identifier through the
index. 25d, 26a and 26e are the later rulings; the growth is stated here so the owner
can see it against 9e(iii).

`get(id, version)` with an explicit version is unchanged by 3h: it returns that
version after integrity, the validator and rule 3c, or raises. It is a historical
read, not the capital read.

### Rule 4 — A stage move without evidence is not a review (F-014)

SELECTED (9e(v), "Evidence for everything"), extended to `Remain` by **RULED
(18c)**. **This is no longer `Promote`-only.** `ReviewOutcome` has four members
(`framework/artifacts/enums.py:135-138`): `Promote`, `Remain Current Stage`,
`Demote`, `Retire`.

**Evidence is required for all four outcomes — RULED (18c): "2. Always required -
rejecting a promotion also protects from real money going into play".** 9e(v) named
the three that move a strategy; 18c adds `Remain Current Stage` in both of its
senses, a promotion request rejected (ADR-008 rule 4) and a strategy kept on the
stage it holds. `constitution/Evidence_Standards.md:45` — "Every conclusion must
reference supporting evidence" — is the sentence both apply.

*(Replaced 2026-09-24. The previous draft left `Remain` evidence-optional as the
drafter's judgement and flagged it as open. 18c ruled it; finding B7 listed this
paragraph among those ADR-016 left contradicting the ruling.)*

**This amends ADR-004 rule 4 (`docs/DECISIONS.md:396-400`), and says so — finding
S10.** ADR-004 rule 4 is "Evidence — written justification, no numeric gate": a
demotion needs a written justification citing evidence, and no score. Under this
rule a `Demote` or a `Retire` also carries **at least one verifying evidence
record** (SELECTED 9e(v); RULED 18b: "the record of the observed condition that
triggered it, at the grade that observation was made"). **"No numeric gate" is
kept:** 18b rules "No minimum grade, and none may be added", and the direction
clause below keeps the bar off every downward move. What changes is that a written
reason alone no longer suffices; what does not change is that no score or grade is
ever required to withdraw capital. ADR-004's text is the owner's; on ratification
of this ADR, ADR-004 rule 4 should carry a pointer to this paragraph, as ADR-004
already does for its own 2026-07-28 correction.

**Where each obligation lives.**

- **(a) `review_artifact()` gains a required `evidence` parameter** — DRAFTER,
  following 18c. With evidence required on every outcome, a default of empty has no
  remaining purpose, and a required parameter makes the omission a `TypeError` at
  the call rather than a refusal further in. Today nothing asks for evidence and
  `**kwargs` would forward one if given (`framework/artifacts/review.py:83`,
  `:167-174`); the parameter makes it explicit. *(Replaced 2026-09-24: the previous
  draft defaulted it to empty "so that `Remain` is not forced to pass `()`", and
  said the function "passes no evidence", which N1 corrected.)*
- **(b) `review_artifact()` refuses at construction** when the evidence tuple is
  empty or any record's `verify()` is False, **for every outcome** (18c). At
  construction, on the reason `framework/artifacts/review.py:102-106` already
  gives: an unjustified decision "is not an artifact with a defect — it is not a
  decision".
- **(c) `ArtifactValidator` gains its first REVIEW-specific path**, applying the same
  checks by reading `outcome` out of `content`. It has none today. Needed because a
  construction-time check does not survive `ArtifactSerializer.load()`, which builds
  `Artifact(**values)` directly (`framework/artifacts/serializer.py:134`) — **that
  gap is F-007 itself**, and repeating it for reviews would be digging the same hole
  next door.
- **(d) `save()` and `get()` run (c)** under rule 3.0, and rule 3c runs it on the
  last rung's review when a strategy is read (finding B3). No separate storage
  condition.
- **(e) `save()` reconciles the declared subject fields** — rule 5. That needs the
  store and the validator has none.
- **(f) Evidence gathered before a demotion cannot buy a climb back — RULED (25i):
  "Evidence gathered before a demotion cannot be reused to climb back."** Finding
  S3. **RULED (26d): "25i's 'evidence' means the data. A report computed after a
  demotion over data from before it is still evidence from before the demotion."**
  Mechanism DRAFTER.

  **The demotion index — RULED (26a): an unresolved downward step "never bars
  earlier evidence under 25i".** Let `d` be the index, in the subject's ladder, of
  its most recent downward rung **whose review resolves**: stored, integrity-valid,
  typed REVIEW, carrying the rung's hash, and satisfying rule 3b condition 5 (a
  `Demote`; a `Retire` has no successor). A downward rung whose review does not
  resolve is not in the index, and neither is a stored review applied only by rule
  3h step 5; both lower the read and are flagged, and neither bars evidence
  (second-pass finding 2N4: one unreviewed file used to bar every piece of honest
  evidence from before it). When a review whose outcome is `Promote` is saved,
  `save()` refuses it when:
  - any of its evidence records, compared by `hash`, is also on the review named by
    any rung at index `d` or earlier; or
  - **any report it binds under ADR-016 has a data window that starts on or before
    the demotion's anchor** (second-pass finding 2N11). The window is the report's
    own `sample_period_start`, which `metric_artifact()` writes into `content`, inside
    the report's signature (`framework/metrics/reporting.py:101-105`, `:227-231`). The **anchor** is the
    later of two dates: the `created` date of the review of rung `d`, which the
    rung's integrity hash fixed when the demotion was appended; and the latest
    `sample_period_end` of every report bound by any review at index `d` or
    earlier, so the anchor is never earlier than the data already used. *(Replaced
    2026-09-25. The previous check compared the report's subject version, so a
    report recomputed after the demotion over pre-demotion data, tagged with a
    post-demotion subject version, passed. 26d ruled that the data is what counts.)*

  Both checks read the reviews and reports the ladder already names, so they run in
  `save()` and in rule 3f's sweep, not in rule 3c. A record re-created from the same
  pre-demotion observation has a new hash and passes the first check; the second
  check is what stops it wherever the record is bound to a report, which ADR-016
  requires on every upward move from `Paper Trading` up — and a demotion never lands
  below `Paper Trading` (`framework/artifacts/validator.py:57-102`).

  **What this costs, stated so the owner sees it (DRAFTER reading of 26d).** Read
  literally, 26d bars any data dated on or before the demotion, not only data a
  report used before it. ADR-016 rule 8 requires a significance report whose data
  is adequate under amended ADR-012, which requires at least 10 years (Part 22b).
  **So a strategy demoted from a capital stage cannot re-enter one for at least ten
  years after the demotion.** Paper trading after the demotion is new data and is
  not barred, but it does not shorten the ten-year backtest span. This follows from
  26d and 22b together; the narrower reading, "data a report used before the
  demotion", is put to the owner at ratification rather than chosen here.

  **What the anchor cannot stop.** The `created` date is written by whoever writes
  the demotion review. A demoter who backdates it can let data from between the
  backdated date and the real demotion be reused; the second half of the anchor
  stops only data that was already bound. A demoter who post-dates it bars more
  evidence than 26d requires, which is a denial of capital, not a grant.

**`evidence_level` is re-derived**, which ADR-005 rule 5 already requires and
`framework/artifacts/validator.py:226-238` already does. No new taxonomy:
`Artifact.evidence` exists (`framework/artifacts/artifact.py:37`), is inside the
signature (`framework/artifacts/integrity.py:43`), and carries
`constitution/Evidence_Standards.md`'s four classes through `EvidenceLevel`
(`framework/artifacts/enums.py:4-13`).

**Confidence is not evidence.** A populated `resulting_confidence` or a
`confidence_adjustment` of `Increase` does not satisfy this rule —
`constitution/Paper_First_Capital_Doctrine.md:45-47`, "Never confidence alone", the
only sentence in the constitution naming something that explicitly does *not* count.

**What owner selection 5 costs, stated because the owner was told it and chose it
anyway.** A demotion can no longer be recorded on the strength of a written reason
alone. In an emergency — a live breach, a strategy that must come off capital now —
the reviewer must first construct an `EvidenceRecord`, which requires a source, a
methodology, a level, a confidence and a provenance
(`framework/artifacts/evidence.py:20-30`). **The mitigation is that the evidence for
a demotion is usually already in hand: the record of the observed breach itself** —
the drawdown measurement, the failed check, the deviation report — is exactly a
Level A or B record, and attaching it is recording what was already seen rather than
producing something new. It is still a step between noticing and acting, and on a
day when that matters it will be felt.

#### The minimum evidence grade per rung — the slot SELECTED 9e(iv) reserved, now filled by ADR-016

**RULED (18a, 18b, 18g).** The owner ruled the bar on 2026-09-22 and put it in its
own record, ADR-016 (18g: "ADR-015 rule 4's table stays the interface and points at
ADR-016"). **Every cell below points there, and nothing in this ADR restates a
grade**, so the bar can be amended in ADR-016 without reopening the ladder's rules.
*(Replaced 2026-09-24. The table was "deliberately empty" until the ruling;
finding B7.)*

| Rung reached (`to_stage`) | Minimum `EvidenceLevel` — **upward moves only** |
|---|---|
| Research | ADR-016 rule 1, and its rule 6 check 1 |
| Validation | ADR-016 rule 1, and its rule 6 check 1 |
| Paper Trading | ADR-016 rule 1, and its rules 3, 6 and 8 |
| Promotion Review | ADR-016 rule 1, and its rules 3 and 6 |
| Micro Capital | ADR-016 rules 1-3, 5, 6, 8 and 9 |
| Limited Capital | ADR-016 rules 1-3, 5, 6, 8 and 9 |
| Production | ADR-016 rules 1-3, 5, 6, 8 and 9 |
| Retired | no floor — clause 1 below; ADR-016 rule 1 |

**Which ADR-016 version applies (25g; finding N4 and S1).** A review records the
`bar_version` it was judged under (ADR-016 rule 10). A stored review is validated
against the bar version it records, never re-judged against a later one, and
`save()` accepts only the current version — so a raised bar applies from each
strategy's next step (RULED 25g). **A ladder's reviews never go down in
`bar_version`** (DRAFTER; second-pass finding 2N7, applied in ADR-016 rule 10), so a
hand-written review cannot claim an older, laxer bar. ADR-016 pins each version's constants to its
ratified text with a conformance test; that test, not a grade test, is what catches
a floor that is lowered, including a `D` floor removed outright, which no
promotion test can detect because nothing is below `D`.

**How rule 4 consumes it (DRAFTER).** A ninth step joins rule 4: for a review whose
outcome moves a strategy **upward**, the artifact's `evidence_level` — which is
already the strongest grade present, derived by `strongest_evidence_level`
(`framework/artifacts/enums.py:29-43`) and re-derived by the validator — must be **at
least** the minimum ruled for the rung's `to_stage`, compared through
`EVIDENCE_STRENGTH` (`framework/artifacts/enums.py:21-26`) and never through the
members' declaration order. **That single-grade comparison is only ADR-016 rule 1.**
The strongest grade present says nothing about the other records, so ADR-016's
further rules (per-criterion records, report binding, closures, authorization) run
beside it in the same REVIEW path of the validator, and in `save()` where they need
the store. They are ADR-016's to define; this ADR only says where they run
(rule 3.0, rule 3c, rule 3f).

**The floor binds upward moves only, and the direction is computed, not inferred from
the table.** The table is keyed by destination alone, and four destinations are
*both* a climb destination and a demotion destination — `Paper Trading`, `Promotion
Review`, `Micro Capital` and `Limited Capital` each appear on the right-hand side of
both a forward and a backward entry in `STRATEGY_TRANSITIONS`
(`framework/artifacts/validator.py:57-102`). A floor read off `to_stage` alone would
therefore put the `Validation → Paper Trading` bar onto `Production → Paper Trading`
as well, which is a grade gate on an emergency demotion — exactly what ADR-004 rule 4
(`docs/DECISIONS.md:396-400`) forbids and what rule 4's own cost paragraph above says
must not be added to.

So the ninth step runs **only when the rung is upward**, determined as follows and in
this order:

1. **Retirement is classified first.** If `to_stage` is `"Retired"`, the move is a
   retirement, it is never upward, and the ninth step does not run. `RETIRED` is
   declared last in `StrategyLifecycle` and is therefore *positionally* above
   `PRODUCTION` while being no rung at all — the trap the comment at
   `framework/artifacts/enums.py:96-109` exists to warn about, and the reason
   `STRATEGY_LADDER` drops it. Reading a retirement as the deepest promotion in the
   system would demand the strongest evidence on the fastest capital-preservation act
   Belay has.
2. **Otherwise compare `STRATEGY_LADDER` positions**
   (`framework/artifacts/enums.py:107-109`), never
   `list(StrategyLifecycle)` positions. The move is **upward** when
   `STRATEGY_LADDER.index(to_stage) > STRATEGY_LADDER.index(from_stage)`, and the
   ninth step runs. It is downward or level otherwise, and the ninth step does not.
   **No conversion is needed between a rung's strings and the ladder's members:**
   `StrategyLifecycle` is a `str` enum (`framework/artifacts/enums.py:69`), so
   `tuple.index` matches a value against a member. Verified for this amendment —
   `STRATEGY_LADDER.index("Paper Trading")` is `3`, `.index("Production")` is `7`,
   and `"Retired" in STRATEGY_LADDER` is `False`, which is clause 1's safety net
   rather than a substitute for it: relying on the membership test alone would make
   a retirement raise `ValueError` instead of being classified.

The `Retired` row is kept in the table so the ruling covers it explicitly rather than
by omission; by clause 1 the only value it can carry is *no floor*, and 18b ruled
exactly that.

Rule 4's base obligation is unaffected by direction: a `Demote` or a `Retire` still
carries at least one verifying evidence record, as 9e(v) and 18b require. What
the direction clause removes is a *grade* requirement on the way down, never the
record.

**The three places the ruling had to reach, and where each landed** (finding B7;
these were listed here before the ruling as open):

- **Downward moves.** RULED (18b): no grade floor on `Demote` or `Retire`, and one
  evidence record of the observed condition, "No minimum grade, and none may be
  added". That is what the direction clause above already does.
- **`Remain Current Stage`.** RULED (18c): evidence required. Applied in rule 4 above
  and in rule 4(b). No grade floor on a `Remain`: 18c leaves its grade unruled, and
  ADR-016 puts that to the owner.
- **Where the bar is ruled.** RULED (18g): in ADR-016. This table is the interface.

**The previous sentence here said a single Level D record satisfied rule 4 for a
promotion into real capital "until it is filled". It is filled.** Under ADR-016 an
upward move into `Micro Capital` needs Level B on each of seven criteria (18a), and
is refused outright while `MINIMUM_PAPER_TRADING` is `None` (18d).

#### What rule 4 buys, and what it does not

**`EvidenceRecord.verify()` proves the record has not been edited since it was
created. It proves nothing about whether the evidence is true, adequate or
relevant.** It recomputes the record's own hash over its own fields
(`framework/artifacts/evidence.py:62-84`) — self-consistency, not an external check.
Verified for this draft: a record whose `source` is `"I made this up"`, whose
`methodology` is the empty string and whose `confidence` is `0.99` returns
`verify() -> True`.

**Rule 4 alone buys non-emptiness and tamper-evidence. It does not buy quality.**
ADR-016 is what raises the ceiling: it binds each record on an upward move from
`Paper Trading` up to a stored report, and a record's grade to its report's grade.
Even then a bound report proves that a report exists and is unedited, not that it
is right.

### Rule 5 — The REVIEW `content` shape, settled now

`framework/artifacts/review.py:56-67` records ten keys today.
`artifacts/RPT-0001/1.0.0.yaml` is the only artifact ever committed — verified with
`git log --all --diff-filter=A --name-only -- artifacts/` — so no REVIEW exists and
its signed content is still free to change. After the first is saved, every change
is a migration of permanent append-only records, which `Knowledge/Versioning.md:25`
forbids rewriting. **ADR-014 rule 6 (`docs/DECISIONS.md:3375-3393`) made exactly
this argument about the fetch record and is cited as an analogy only; it rules
nothing about REVIEW content.**

**Three keys are added, and rule 3b condition 5 reads all three** — none is
decorative:

- **`subject_integrity_hash`** — the `integrity_hash` of the exact subject version
  reviewed. `subject_id` and `subject_version` name a *file*; the hash names its
  *contents*.
- **`subject_ladder_length`** — how many rungs the subject carried when reviewed.
  It pins a review to a *position*, which is what stops one review buying two rungs
  after a demotion and re-climb.
- **`evidence_summary`** — one line naming what the evidence records are, for a
  person reading the YAML. Prose; nothing computes on it. Same status ADR-009 rule 8
  gave the six template sections.

**Who writes them.** `review_artifact()`
(`framework/artifacts/review.py:70-84`) gains three parameters of those names, and
the module constant `FIELDS` (`framework/artifacts/review.py:56-67`) grows from ten
entries to thirteen. `review_fields()` reads them back through that same constant,
which is what the constant exists for — its own comment says it is named there so
that writer and reader "cannot drift apart". `subject_integrity_hash` and
`subject_ladder_length` are required; `evidence_summary` defaults to empty.

**ADR-016 adds its own keys to the same constant** (finding B7; the previous draft
stopped at thirteen): `bar_version`, `criterion_evidence`, `evidence_reports`,
`reports_considered`, `variants_tried` and `human_authorization`, defined in ADR-016
rules 2, 3, 6, 9 and 10. With them `FIELDS` has nineteen entries. *(Changed
2026-09-25: eighteen became nineteen when ADR-016 separated the reports a review
considered from those it binds, second-pass finding 2N5.)* They are settled in the same window and
for the same reason: no REVIEW has been stored yet.

**Keys that do not apply to an outcome (DRAFTER; finding N3).** `review_fields()`
requires every key in `FIELDS` to be present (`framework/artifacts/review.py:193-199`),
so an outcome-specific key is always there. **Where it does not apply it holds
`None`, and the validator refuses any other value**: `variants_tried` on anything
but a `Promote`; `criterion_evidence` on anything but an upward move into a capital
rung; `human_authorization` on anything but an upward move into a capital rung or a
review that authorizes a confidence change on a capital stage (rule 3g, 26c);
`evidence_reports` and `reports_considered` on anything but an upward move into
`Paper Trading` or above. A key that carries a value nothing checks would read
as evidence while being none. `resizing_note` keeps its present meaning (ADR-004's
re-sizing prose, `None` where there is none).

**Rule 5 is DRAFTER.** No owner Part rules REVIEW content; 18f leaves "where the
binding lives" to the implementing change.

**Not added: the evidence itself.** It belongs on `Artifact.evidence`, which exists,
is signed, and has a derived grade. Copying it into `content` would be the
duplicated abstraction `AGENTS.md:113` forbids.

**`stage_at_review` stays declared, and is reconciled at the storage boundary.**

*Declared*, because `review_artifact()` is a pure constructor that takes no
repository, and ADR-009 made the record a statement of what the reviewer had in
front of them. A field substituted from disk would stop being that, and would make a
review of a stale artifact indistinguishable from a review of a current one — the
distinction `framework/artifacts/review.py:88-91` says `subject_version` exists to
draw.

*Reconciled*, because a declaration nobody tests is what F-014 is. On `save()` of a
REVIEW the repository resolves `subject_id` at `subject_version` and requires the
stored artifact's `integrity_hash` to equal `subject_integrity_hash`, its
`strategy_stage` to equal `stage_at_review`, and its ladder length to equal
`subject_ladder_length`.

**When the subject does not exist, `save()` refuses** with a message naming the
missing `subject_id` and `subject_version`, and says that a review of an artifact
that is not stored records a decision about nothing. It does **not** return `None`
or save the review unreconciled: a silent fallback indistinguishable from a real
answer is the failure `review_fields()` already refuses at
`framework/artifacts/review.py:188-199`.

**Ordering is forced and there is no cycle.** A review is saved *before* the
strategy version whose rung cites it, because rule 3b condition 5 resolves it; and
the review's own subject is the *predecessor*, which already exists.

**A REVIEW whose subject is not a STRATEGY remains unconstructible, and that is
unchanged and intended.** `review_artifact()` already requires `stage_at_review` and
`resulting_stage` to be `StrategyLifecycle` members
(`framework/artifacts/review.py:70-84`), so a review of a REPORT cannot be built on
`main` today. ADR-009 built this record for strategy reviews and this ADR does not
widen it. Recorded here rather than discovered later; if Belay ever needs to review a
non-strategy artifact, that is a new ruling and not a bug in this one.

### Rule 6 — `ArtifactSerializer` restores tuples all the way down, and no further

`_PAIR_FIELDS` re-tupling at `framework/artifacts/serializer.py:116-118` is exactly
two levels deep. Measured rather than argued: a ladder carried as a nested tuple in
`content` round-trips through `dump()`/`load()` with `verify_hash() -> True` —
`canonical_digest` JSON-encodes and JSON does not distinguish a tuple from a list —
and **comes back as nested lists**. Signatures are unaffected; immutability is not,
and `Artifact` is frozen precisely so a signed payload cannot be edited afterwards,
which `framework/artifacts/serializer.py:53-57` states in those words.

**The recursion is bounded by type, and the bound is the rule.** It converts `list`
to `tuple` and recurses into the elements of a `list`. **Every other type is
returned unchanged and is not descended into** — `str`, `bytes`, `int`, `float`,
`bool`, `None`, and `dict` (whose keys and values are left exactly as loaded).
Strings are named explicitly because a naive "recurse into anything iterable" walks
a string forever. `dict` is left alone because nothing here puts one in `content`,
and widening the conversion would change the fetch-record round trip ADR-014
settled.

### Rule 7 — `ArtifactFactory` keeps its own guard

`docs/OwnerDecisions.md:982` left this a preference. **DRAFTER: this draft keeps it.**
*(Corrected 2026-09-24: the previous text said "It is ruled: keep it", which no owner
Part says.)* It fails earlier and says more, and rule 2 does not make it redundant —
the factory refuses at *issue* and the validator at *read*, and F-007 is precisely
the finding that a check at one of those is not a check at the other. Rule 6 is
DRAFTER too.

### Rule 8 — One capital authority: `current_stage(id).stage`

**Finding S11. DRAFTER, resting on RULED 25d, 25j and 26a.** The current-stage read
of rule 3h, `ArtifactRepository.current_stage(id).stage`, **is the only statement of
a strategy's stage that anything in Belay may act on for capital.** *(Changed
2026-09-25: this was `get(id).strategy_stage`. Rule 3h now reads a stage that can be
lower than any stored version's own, so it returns a stage, and `get(id)` with no
version refuses on a STRATEGY identifier.)*
Every other statement of a stage or an approval is a description, and where it
disagrees with this read, this read wins:

- `strategies/Registry.md:3` calls the Registry "the authoritative inventory of all
  strategies known to Belay". It is authoritative for *which strategies exist*, not
  for what stage any of them holds.
- `Operations/README.md:7` says "Operations executes only approved strategies".
  "Approved" is read as "holding a stage this read returns", never as a status
  written anywhere else, including `ArtifactLifecycle.APPROVED` (ADR-003).
- Any stage in a dashboard, a report, a review's `resulting_stage`, or a
  strategy version other than the one this read returns.

**A read that raises means zero capital** (rule 3h step 7, 25d). No consumer may
fall back to another source when the read refuses.

**A flagged read is acted on at the stage it reads, and shown to a person (26a).**
When `needs_repair` is `True`, the stage read is still the capital stage — it is
already the lowest the record supports — and every consumer that presents the
strategy to a person shows the repairs with it. No consumer may raise the stage
while a flag stands.

Both files above are frozen by ADR-002 and are the owner's. **This rule edits
neither.** It proposes that, on ratification, each carries a one-line pointer to
this rule; until then the precedence is stated here only.

**What this rule cannot reach — RULED (25j): "Trading done outside Belay, for
example by a user's own connected AI, is out of scope for these ADRs."** Rule 8
governs what Belay acts on. It cannot stop a user, or a user's connected AI, from
trading a strategy through an account Belay does not control, whatever stage this
read returns. ADR-016 states the same limitation.

---

## Tests this implies

Behaviours, not code. **Every negative test asserts the specific refusal, never a
bare exception type** — a test asserting `pytest.raises(ValueError)` passes on a
misspelled keyword, and this repository has shipped that shape twice. Where a test
below could pass for a wrong reason, the wrong reason is named.

**The honest histories — the tests that stop the fix being a wall.**
`docs/proposals/F-007-session-brief.md:130-133` names the first as the one most
likely to be forgotten.

1. A strategy climbs `Idea` to `Production` one rung at a time, each rung bought by a
   stored review carrying evidence, and every version round-trips through
   `ArtifactRepository` with its stage and integrity intact.
2. A strategy at `Idea` with no ladder and `parent_hash` of `None` saves and reads
   back.
3. A second version at `Idea` with an empty ladder saves when `parent_hash` names the
   stored `Idea` version; and is refused, naming `parent_hash`, when it is `None`
   while a version is already stored.
4. A strategy is demoted from `Production` to `Paper Trading` **with an evidenced
   `Demote` review** and climbs back; the ladder grows through the demotion, holds
   two rungs with the same stage pair, and each is bought by a different review.
5. A same-stage revision of the **frontier** version that changes only
   `confidence` — ADR-005's confidence change — saves with the ladder and stage
   unchanged and no review required. *(Narrowed 2026-09-24: this said "content
   revision", which is what let B1 through. Tests 39-43 are its negative pairs.)*
6. A review is revised to a second version after a strategy has cited its first; the
   strategy still resolves through `get()`, because the rung names `review_version`.
   Asserts the loaded stage, not merely that no exception was raised.
7. An emergency demotion recorded from a single evidence record describing the
   observed breach saves, reads back, and its `evidence_level` is the record's grade.

**The forgeries — each refused, and the refusal named.**

8. `Artifact(type=STRATEGY, strategy_stage=PRODUCTION)` + `sign()` is refused for
   carrying no ladder while not at `Idea`. *(F-007's reproduction.)*
9. The same through `ArtifactSerializer.load()`, refused identically.
10. The same re-signed after a hand-edit, refused identically.
11. The same via `dataclasses.replace()` + `sign()`, refused identically.
12. An honest `Idea` version plus an honest `Idea → Research` review, then a version
    claiming `strategy_stage = "Production"` with that one rung, refused **naming the
    mismatch between the stage and the last rung's `to_stage`**. *(Blocker 1.)*
13. **A hand-written re-signed YAML with a seven-rung ladder naming reviews that are
    not on disk is refused by `get()`, naming the missing `(review_id,
    review_version)`** — and separately, with the review present but the predecessor
    absent, refused naming the missing `parent_hash` version. *(The second pass's
    blocker B1; two tests. Each must assert the message, because a test that only
    asserts "not `PRODUCTION`" would pass on an unrelated `AttributeError`.)*
14. A version whose `parent_hash` names an older, non-frontier ancestor is refused
    **naming the frontier**, in three forms: undoing a demotion, un-retiring a
    `RETIRED` strategy, and an ordinary revision of a superseded version. *(The
    second pass's blocker B2, owner selection 6.)*
15. A ladder of the same length as `Lmax` but differing in any rung is refused naming
    the prefix rule; so is a ladder shorter than `Lmax` that is an honest prefix of
    it; so is one longer by two.
16. An artifact declared `REPORT` but carrying `strategy_stage=PRODUCTION` is refused
    by both `save()` and `get()`, naming the stage on a non-STRATEGY. *(The executed
    scope-evasion.)*
17. A second version of one identifier declaring a different `type` is refused by
    `save()`, naming both types.
18. A rung naming a review whose stored version differs from the one named is refused
    naming the version; and test 6's positive case is its pair. *(Blocker 2.)*
19. A ladder in which one `(review_id, review_version)` appears in two rungs is
    refused naming the repeated pair. *(Blocker 3.)*
20. A rung whose review's `subject_ladder_length` is not `len(L) - 1` is refused
    **naming both numbers**; and one whose `subject_integrity_hash` names a version
    other than the predecessor used is refused naming both hashes. *(Blocker 3.)*
21. A `Promote`, a `Remain Current Stage`, a `Demote` and a `Retire` review with
    empty evidence are each refused at construction, by the validator, and by
    `save()` — twelve tests, because they are four outcomes across three
    components. *(F-014, 9e(v), 18c.)*
22. A `Remain Current Stage` review with empty evidence is **refused**, in both of
    `Remain`'s senses: a rejected promotion (`Promotion Review` held) and a
    strategy kept on capital (`Limited Capital` held). Each refusal names 18c.
    *(Reversed 2026-09-24: this test pinned the drafter's "optional", which 18c
    overruled.)*
23. A review carrying a record whose hash has been forged is refused naming the
    record's source.

**The direction clause.** The table is filled (18a, 18b, through ADR-016), so both
tests run; neither is `xfail`. *(Changed 2026-09-24. The worked example was `Micro
Capital`; a promotion into it is now refused by `MINIMUM_PAPER_TRADING` being `None`
before any grade is read, so a test there could pass for the wrong reason. `Paper
Trading` is the example instead: its upward floor is `C` (18a), and it is a
demotion destination too.)*

23a. **A demotion into a stage whose upward floor is `C` passes carrying only a Level
    D observed-condition record.** `Micro Capital → Paper Trading` — a legal
    backward move (`framework/artifacts/validator.py:75-80`) — with a single Level D
    record recording a reasoned structural argument saves and reads back, and the
    stored `evidence_level` is `D`. **Asserts the refusal does not happen**, and its
    docstring must name ADR-004 rule 4 (`docs/DECISIONS.md:396-400`) and 18b as
    what it protects, so that a future change to the ninth step cannot silently put
    a floor on an emergency demotion.
23b. **A promotion into that same stage carrying only a Level D record is refused,
    naming both the ruled minimum and the record's grade.** `Validation → Paper
    Trading` with the identical record. The two tests differ only in `from_stage`,
    which is the whole point: the table is keyed by destination and the direction
    clause is what separates them. The refusal asserted is the floor's, not ADR-016
    rule 3's or rule 8's: the test binds a report that satisfies both, so that only
    the grade is short.

**The structural rules.**

24. A ladder not beginning at `"Idea"` is refused naming rung 0's `from_stage`.
25. A ladder with a gap — rung `i`'s `from_stage` unequal to rung `i-1`'s `to_stage`
    — is refused naming both rungs.
26. A ladder containing a rung that skips a stage is refused, **and the refusal comes
    from `validate_transition`**, asserted by matching its message.
27. A strategy at `Idea` with a non-empty ladder is refused; a post-`Idea` strategy
    with an empty ladder is refused. Both directions of step 2.
28. Rung shape, one test each, every refusal naming the offending element: four
    elements; six elements; **an element that is not a string** (an integer, and a
    nested list); a stage that is a member *name* rather than a value; a malformed
    `review_id`; a non-semantic `review_version`; a `review_integrity_hash` of the
    wrong length; one in upper case.
29. A `Validated By` edge whose targets differ from the ladder's `review_id`s, or are
    in a different order, is refused; and `relationships` carrying `Validated By`
    twice is refused.
30. `content` carrying the key `ladder` twice is refused.
31. A non-empty ladder with `parent_hash` of `None`, and a `parent_hash` matching no
    stored version, are each refused by `save()` **naming `parent_hash`** — not
    merely raising, because a missing predecessor could otherwise surface as a
    `None` dereference.
32. **A directory containing one unparseable sibling and one corrupt sibling still
    permits an honest save**, and the refusal-free path is asserted by the save
    succeeding. *(Rule 3a's scan, and the brick-the-identifier failure it exists to
    prevent.)*
33. **A forged long-ladder file dropped into the directory, naming reviews that do
    not exist, does not become `Lmax` and does not block an honest save.** *(Rule
    3e's counting rule.)*
34. A REVIEW whose subject is not stored is refused by `save()` naming the
    `subject_id` and `subject_version`; one whose subject's `integrity_hash`,
    `strategy_stage` or ladder length disagrees with the declared value is refused
    naming the field that disagreed. *(Rule 5's reconcile — four tests, none of which
    existed in the previous draft.)*
35. `save()` and `get()` refuse an invalid STRATEGY and an invalid REVIEW, and still
    accept a REPORT with no capital claim that would not otherwise validate. *(Rule
    3.0, including its stated asymmetry.)*
36. **`get()` opens exactly the extra artifacts rule 3c names and no more** —
    asserted by reading a strategy at `Production` from a repository holding only
    it, its predecessor, its last rung's review and the reports that review binds,
    with every earlier version, review and report absent, and observing that it
    succeeds. *(Changed 2026-09-25: this said "exactly two"; 26e added the bound
    reports.)* **This test asserts the limitation, not a guarantee,
    and its docstring must say so, naming rule 3f as what covers the rest.** *(The
    inverse of the previous draft's test 25, which asserted that `get()` resolved
    nothing.)*
37. A nested list inside `content` comes back as a nested tuple, and a string inside
    `content` comes back as the same string rather than a tuple of characters.
38. `ArtifactFactory.create()` still refuses a post-`Idea` STRATEGY at birth.

**The attacks of the 2026-09-24 falsification pass — one test per attack, each
asserting the named refusal.** *(Added 2026-09-24 for findings B1, B2, B3, S2 and
S3.)*

*B1 — swapping a funded strategy's rules (rule 3b condition 3, rule 3g, 25c):*

39. **The executed attack.** Strategy A climbs honestly to `Limited Capital`. A
    version carrying strategy B's `content` (every entry but `ladder`), with A's
    ladder, A's stage and `parent_hash` naming A's frontier, is refused by `save()`
    as a Revision **naming the first differing field**. A test asserting only "not
    saved" would pass on an unrelated refusal.
40. The same version dropped into the directory by hand is not returned by the
    current-stage read: rule 3c's predecessor check re-runs condition 3 and
    refuses it, and the read walks back to A's frontier version, which it returns.
41. One test per specification field — `title`, `summary`, `tags`, `metadata`,
    `author`, `lifecycle`, `deliverable`, `evidence`, a non-`ladder` `content`
    entry, a non-`Validated By` relationship — each changed alone in a Revision of
    a post-`Idea` version, each refused naming that field. Test 5 is the positive
    pair: `confidence` alone saves.
42. An **Append** that also changes the specification (an honest new rung with its
    review, plus a changed `content` entry) is refused naming the field, so the
    swap cannot ride on a genuine promotion or demotion.
43. The honest route: the changed specification saved under a **new identifier at
    `Idea`**, empty ladder, `parent_hash` of `None`, a `Derived From` edge naming
    A, saves and reads back at `Idea`; A's stage is unchanged. And an `Idea`-stage
    revision (empty ladder) that changes `content` still saves, because 3g binds
    from the first rung.

*B2 — undoing a demotion by deleting one file (rules 3e and 3h, 25d):*

44. **The executed attack, at save.** `v5` at `Production`; `v6` demotes it to
    `Paper Trading` with an evidenced `Demote`; `v6`'s review file is deleted from
    the temporary root. *(Changed 2026-09-25 under 26a.)* `v6` no longer counts
    toward the frontier, so `v7`, a Revision of `v5` at `Production`, **saves**; and
    the current-stage read still returns `Paper Trading`, flagged
    `DOWNWARD_REVIEW_UNRESOLVED` naming `v6`'s rung. Asserts both, so the test
    fails if the save is refused (26a: "nothing more") or if the read rises.
45. **The same attack, by hand.** `v7` is written directly into the directory,
    re-signed. The current-stage read returns `Paper Trading` from tip `v6` and
    reports no disagreement, because `v7`'s ladder is a prefix of `v6`'s. A variant where
    the hand-written `v7` *appends* an upward rung to `v5` with a forged review
    returns the lower of the two tips and reports the disagreement, naming both.
46. **S2: a damaged record does not block a demotion.** A strategy at `Limited
    Capital` whose last review file is deleted (so `get(id, version)` refuses it)
    is demoted to `Paper Trading` and, separately, retired: each downward append
    saves, and the current-stage read returns the lower stage. The failing
    upward-append pair: the same damaged `P` cannot be *promoted*; the refusal
    names rule 3c.
47. **An honest re-climb is not a disagreement.** Demote at `v6`, climb at `v7` to
    `v9`: the current-stage read returns `v9` and reports nothing; and when every
    stored version fails to establish, the read raises rather than returning a
    stage (rule 3h step 7). The honest demotion is not flagged.

*B3 — reading a stage without checking the bar (rules 3c and 3f):*

48. **The executed attack.** Three hand-written, re-signed files: a predecessor at
    `Promotion Review`, a `Promote` review to `Micro Capital` with **no evidence**,
    and a strategy at `Micro Capital` naming both. `get(id, version)` refuses,
    naming the review's missing evidence (rule 4(c)); the current-stage read does
    not return `MICRO_CAPITAL`. **Second-pass finding 2N12, added 2026-09-25:** the
    same three files with an evidenced review at `Paper Trading` whose bound report
    is not stored, and separately one whose bound significance report has
    `significant: false`: rule 3c refuses each, naming the report and, for the
    second, ADR-016 rule 8; the read walks back past it. Before 26e both read back
    as `Paper Trading`.
49. The same with evidence at the floor on all seven criteria: refused, naming
    `MINIMUM_PAPER_TRADING` and 18d; and naming ADR-016's human-authorization
    closure and 26f. The test fails if either closure is moved out of the
    validator.
50. The same pattern one rung up for each live rung, `Micro Capital → Limited
    Capital` and `Limited Capital → Production`: refused, naming the live-duration
    minimum and 25e.
51. **The sweep.** A store holding a strategy at `Paper Trading` whose *second*
    rung's review is a hand-written file with no evidence: rule 3c passes (it reads
    only the last rung), and rule 3f's sweep reports the second rung naming rule
    4(c). Asserts both halves, so the test documents the limit as well as the cover.

*S3 — reusing evidence after a demotion (rule 4(f), 25i):*

52. After a demotion from `Micro Capital` to `Paper Trading`, a `Promote` back to
    `Promotion Review` carrying an evidence record that was on the review of a rung
    at or before the demotion is refused naming 25i and the rung; one binding a
    report whose data window starts on or before the demotion's anchor is refused
    naming both dates (rule 4(f), 26d). The same record with a timestamp moved later
    is still refused, which is what "by ladder position" means.

*The second pass (2N1-2N4, 2N10-2N12; 25d, 26a, 26c, 26d, 26e). Each was run in the
scratch model named in the revision history; each asserts the named result.*

53. **2N1, model C.** One hand-signed file: seven rungs `Idea` to `Production` and
    one down to `Limited Capital`, naming reviews that are not stored, with a
    `parent_hash` naming nothing. The current-stage read **raises**, naming
    `NO_BASE`. Before this revision it returned `LIMITED_CAPITAL`.
54. **2N1, model C2.** An honest strategy at `Paper Trading` (`v4`) and a forged
    `v5` extending it, in one file, up to `Limited Capital` and down to `Micro
    Capital`. The read returns `Paper Trading` from `v4`'s base, flagged: three
    `UPWARD_REVIEW_UNRESOLVED`, one `DOWNWARD_REVIEW_UNRESOLVED`, one
    `VERSION_FAILS_3C`. Before this revision it returned `MICRO_CAPITAL`.
55. **The base ends upward (model C3).** The same honest `v4`; a forged `v5` at
    `Production`; a genuine, stored, integrity-valid `Demote` review of `v5` to
    `Limited Capital`; `v6` appending it. Asserts that `v6` passes rule 3c **and**
    that the read is `Paper Trading`. The first half is what makes the test
    meaningful: it fails if "passes 3c" alone is ever taken as a base again.
56. **2N2, model F.** A strategy demoted `Production → Paper Trading` at `v9`, with
    its `Demote` review stored. Delete `v9`'s file: the read returns `Paper
    Trading`, flagged `STORED_DEMOTION_NOT_IN_LADDER`. Delete the review too: the
    read returns `Production` with no flag, and the test's docstring names this as
    the stated residual that only git history shows, so nobody mistakes the
    assertion for a guarantee. And the honest pair: after a demotion and a re-climb
    whose ladder carries the `Demote` rung, the stored review is not applied again.
57. **2N3.** An honest strategy at `Paper Trading`; a Revision changing only
    `confidence`. Rule 3c passes, with the review's subject found by rule 3a's scan
    as the version with ladder `L[:-1]`; and a second Revision of that Revision
    passes too. Under the previous wording both failed condition 5.
58. **2N4 and 26a, model D.** One forged file stepping `Paper Trading → Retired`
    with no stored review. The read returns `Retired`, flagged
    `DOWNWARD_REVIEW_UNRESOLVED`; the frontier is still the honest `v4`, and an
    honest `Paper Trading → Promotion Review` Append from `v4` saves; and a later
    `Promote` binding evidence from before the forged rung is not refused by rule
    4(f), because the forged rung is not in the demotion index.
59. **2N10 and 26c.** A Revision of a version at `Micro Capital` changing only
    `confidence`, with no `confidence_review`: refused by `save()` and by rule 3c,
    naming 26c. With a `confidence_review` naming a `Remain Current Stage` review
    whose `resulting_confidence` differs: refused naming both values. The same
    Revision at `Paper Trading` saves. (Today no strategy can reach `Micro
    Capital`; the test builds the store by hand, as test 48 does.)
60. **2N11 and 26d.** After a demotion whose anchor is 2026-03-31, a `Promote`
    binding a report computed afterwards over 2016-01-04 to 2026-06-30, tagged with
    a post-demotion subject version, is refused naming the window's start and the
    anchor. The same with a window starting 2026-04-01 is not refused by rule
    4(f).

---

## Consequences

Positive:

- F-007 closes at the point where the claim is *read* as well as where it is
  *issued*, which is the guarantee `docs/OwnerDecisions.md:958` names
- F-014 closes, and `constitution/Paper_First_Capital_Doctrine.md:45-47` acquires an
  implementation for the first time in the project's life
- under 9e(v) and 18c, `constitution/Evidence_Standards.md:45` becomes true of
  every review outcome, including a rejected promotion, rather than only of
  promotions
- a funded strategy's rules cannot be swapped under its identifier (rule 3g, 25c)
- a damaged or deleted record can lower the stage Belay reads, never raise it, and
  never block a demotion (rules 3b, 3e, 3h; 25d)
- a downward step can lower an established stage and never supply one, and a
  downward step whose review does not resolve is flagged for a person and changes
  nothing else (rule 3h; 26a)
- reading a stage re-checks the last step's bound reports and ADR-016 rule 8
  (rule 3c; 26e)
- one read, and only one, states a strategy's capital stage (rule 8)
- the REVIEW record stops being a statement *about* a strategy and becomes a thing
  the strategy must *produce* to move
- the signed content of a REVIEW is settled in the last window where that is free
- `parent_hash` stops being a field nothing writes
- an identifier can no longer shed its type at a later version

Negative:

- **`tests/artifacts/test_serializer_round_trip.py:90-116` must change.** The only
  place in the repository constructing a post-`IDEA` STRATEGY — a grep for
  `strategy_stage=StrategyLifecycle.` above `IDEA` over `tests/`, `framework/` and
  `scripts/` returns exactly one line, `:110`. It jumps `IDEA` to `LIMITED_CAPITAL`
  in one `dataclasses.replace`, skipping three rungs and naming no review. **Its
  subject — that an earned stage survives the round trip — is not weakened; the
  fixture gets longer and more honest.**
- `tests/artifacts/test_review_decision.py` gains evidence at every construction,
  `Remain Current Stage` included (18c), and `review_artifact()`'s signature grows
  by four parameters here (`evidence`, required; `subject_integrity_hash`;
  `subject_ladder_length`; `evidence_summary`) and by ADR-016's five content keys
  (rule 5). *(Corrected 2026-09-24, finding B7: this said `Promote`, `Demote` and
  `Retire` only.)*
- **building a strategy for a test stops being a one-liner.** Reaching
  `MICRO_CAPITAL` legitimately takes five strategy versions and five evidenced
  reviews. A shared climbing fixture is not optional
- **an emergency demotion now needs an evidence record first.** 9e(v) and 18b,
  with the cost and the mitigation stated in rule 4. It needs nothing else: no
  grade, no report binding, no human authorization, and not an intact earlier
  record (rule 3b, S2)
- **a rejected promotion now needs an evidence record too** (18c)
- **a post-`Idea` strategy's title, tags, summary, author and editorial lifecycle
  are frozen** with the rest of its specification (rule 3g, DRAFTER beyond 25c's
  capital stages). A correction means a new identifier
- **anyone who can write one signed file can force the stage Belay reads down**
  (rule 3h), and one file with no base makes the read raise. Accepted under 25d as a
  denial of capital, never a grant. Since 26a such a file no longer blocks saves or
  bars evidence, and it is flagged on every read until a person repairs it
- **a strategy demoted from a capital stage cannot re-enter one for at least ten
  years** under rule 4(f)'s literal reading of 26d with Part 22b (rule 4(f))
- **a funded strategy's confidence cannot change without a recorded human yes**
  (rule 3g, 26c)
- **a mistake three versions back can no longer be revised in place.** Owner
  selection 6; correction is forward-only
- **`get()` is no longer one integrity check.** Extra reads on every in-scope read
  (two, plus one per report the last review binds, plus one on a Revision), and it
  can now refuse a file it used to return. The current-stage read (rule 3h) also
  lists every stored version of the identifier and reads its stored downward
  reviews through a subject index that does not exist yet
- `save()` and `get()` acquire a validation failure mode on the path a promotion gate
  sits on
- committed artifacts per rung, permanent and tracked under ADR-014 rule 2, with no
  retention policy — the ground on which ADR-013 and ADR-014 both declined to rule one
- rules 3 and 5 are checks at a boundary nothing crosses today. Nothing in Belay calls
  `save()` for a STRATEGY or a REVIEW, so a green suite proves the checks work and
  proves nothing about the system using them — ADR-014's position on the day it was
  ratified

### Residual risk, stated rather than buried

**What the cheapest forgery costs, counted rather than asserted.**

- **Against `main` today: one file.** A hand-written, re-signed YAML at
  `<root>/STRAT-0001/8.0.0.yaml` claiming `PRODUCTION`. Executed.
- **Against the second draft of this ADR: still one file.** The same YAML with a
  seven-rung ladder naming `REV-9001`…`REV-9007`, a `parent_hash` of `"f"*64` and a
  matching `Validated By` edge. `get()` returned `PRODUCTION` with zero reviews on
  disk. Executed. That is what owner selection 3 was asked about.
- **Against the third draft: three files.** `get()` checks one level, so the forger
  must also write the predecessor version — whose ladder is `L[:-1]` and which must
  pass rule 2 — and the *last* rung's review, which must be typed `REVIEW`, carry the
  named integrity hash, and satisfy every sub-check of rule 3b condition 5. The
  earlier six rungs' reviews and the predecessor's own ancestors need not exist.
  **The falsification pass of 2026-09-24 showed those three files could carry a
  review with no evidence at all (B3).**
- **Against the 2026-09-24 revision: one file**, if its last rung was downward
  (second-pass finding 2N1). Executed: `LIMITED_CAPITAL` with no review on disk.
- **Against this revision: three files, and the stored reports they bind.** Rule 3c
  runs the full validator on the review, resolves every report it binds and applies
  ADR-016 rule 8 (26e); a downward last rung only lowers a stage the walk has
  already established (rule 3h). **No capital rung can be reached this way today**,
  because each is closed by a `None` constant the validator reads (18d, 25e, 26f).
  **`Paper Trading` cannot either**: its review must bind a stored significance
  report that passes rule 8, which needs the amended ADR-012's recorded conditions,
  and no module writes them. What three files can still buy is `Research` or
  `Validation`, where no report is bound. *(Replaced 2026-09-25: this bullet said
  three files could buy "a zero-capital stage with bound reports that do not exist";
  26e removed that.)*
- **To forge a history that also survives rule 3f's sweep: fifteen files** for a
  strategy at `PRODUCTION` — eight strategy versions and seven reviews, each
  evidenced, each internally consistent, each resolving — plus every report those
  reviews bind, each stored at the grade its producing module writes.

**So `get()` raises the floor from one file to three, and only the sweep raises it to
fifteen.** Stating the three honestly is the point: the previous draft claimed a
guarantee it did not have.

**And none of this stops an insider** — though ADR-016 rule 9 (25f) now requires a
recorded human authorization on every capital rung, and refuses a reviewer declared
as an AI. That is a recorded declaration, not an authenticated identity, **and so
ADR-016 keeps every capital rung closed until a human authorization can be verified,
not only declared (26f)**. `ArtifactIntegrity.sign()`
(`framework/artifacts/integrity.py:71-80`) is a **checksum, not a signature**: SHA256
over the artifact's own contents, no key, so anyone who can call it can produce a
valid hash for any content. Nothing in `framework/` authenticates an author.
`review_artifact()` refuses an empty reviewer string
(`framework/artifacts/review.py:123-124`) and checks the name against no roster —
ADR-009 rule 10, because no document names reviewer roles. ADR-014 rule 3 records the
same class of limit in the same voice: the artifact root "is enforced by nothing but
the choice of root", and a caller passing the default by mistake writes a permanent
record "because it is a valid signed artifact". **What this ADR buys is cost and
visibility, not impossibility.**

**Three further residuals**, each named at its rule and gathered here: the
denial-of-service that "longest history wins" admits (rule 3e); what one-level
checking does not see (rule 3c); and `_validate_evidence`
(`framework/artifacts/validator.py:221-224`), which checks that an evidence hash is
present and never that it is right — rule 4 closes that for REVIEW artifacts only,
and it stays open for every other type and is registered as a finding nowhere.

---

## Rejected Alternatives

**A — the version chain: "birth is version `1.0.0` with no `parent_hash`".** Rejected
on executed evidence, in the Context. This rejects the *birth test*; rule 3a adopts
`parent_hash` for the different job `framework/artifacts/integrity.py:25-27` already
assigns it.

**B — refuse every post-`IDEA` STRATEGY at the validator, full stop.** Closes F-007
and is a wall. `docs/proposals/F-007-session-brief.md:130-133` names legitimate
climbing as the test most likely to be forgotten.

**C alone — carry the proof, add no storage gate.** Rejected by owner selection 1, and
on the merits: rule 2 checks only internal consistency.

**D alone — gate storage, carry no proof.** Rejected by owner selection 1, and on the
merits: after a demotion a strategy occupies the same stage twice, so stage alone does
not identify a rung.

**Adding one condition to `save()` instead of running the validator.** Rejected — rule
3.0. It closes one forgery and leaves the class open.

**Scoping the repository's validation by `artifact.type` alone.** Rejected on executed
evidence — rule 3.0. It lets the forger choose the scope.

**Making `get()` resolve nothing.** This was the second draft's rule and it was
disproved by execution — rule 3c. Rejected by owner selection 3.

**Making `get()` resolve recursively to `IDEA`.** Rejected — unbounded I/O on a read,
against `framework/artifacts/repository.py:129-166`. The middle position, one bounded
level, is what owner selection 3 chose, and what it leaves uncovered is stated rather
than hidden.

**Defining the predecessor as the highest stored semantic version below this one.**
Rejected — rule 3a. A guess where an explicit, signature-covered link exists.

**Building rule 3a's predecessor scan on `get()`.** Rejected — rule 3a. Under rule
3.0 `get()` raises, so one bad sibling would make every future save of that identifier
impossible, permanently, in append-only storage.

**Leaving forks legal, as the first revision did.** Rejected by owner selection 6, and
on the merits: the second pass turned the fork into an executed forgery that undid a
demotion and un-retired a retired strategy.

**~~Requiring `evidence` as a mandatory parameter of `review_artifact()`.~~ No longer
rejected — adopted in rule 4(a).** The previous draft rejected it because it "would
force `Remain` to pass `()` explicitly". 18c requires evidence on `Remain`, so that
reason is gone (finding B7). The rejection is struck through rather than deleted so
the reversal is visible.

**Ruling a minimum evidence class per rung in this ADR.** Rejected by 9e(iv), which
sent it to research first, and then by 18g, which put the ruled bar in ADR-016. The
table in rule 4 is the interface and points there.

**Letting a Revision change anything but its revisable fields, and treating a
changed specification as a demotion.** The pass on Issue #21 offered two fixes for
B1: a new identifier, or a drop down the ladder. 25c chose the new identifier. A
demotion would keep one identifier for two different sets of rules, and the ladder
would then record one strategy's history under the other's name.

**Refusing to read a damaged record.** Rejected by 25d. A refusal on read also
refused the demotion that the damage called for (S2).

**~~Excluding a failed-3c version from the frontier whichever way it went.~~ No
longer rejected — adopted again in rule 3e, 2026-09-25.** The third draft's rule,
rejected in the 2026-09-24 revision on B2's executed evidence. 26a ruled that an
unresolved downward step does "nothing more" than lower the read, and the second
pass showed that counting it made a one-file `Retire` final (2N4). B2 is now stopped
at the read (rule 3h steps 4 and 5), not at the frontier. Struck through rather than
deleted so the reversal is visible.

**Counting a downward last rung without its review, as the 2026-09-24 revision
did.** Rejected by 26a and on the second pass's executed evidence (2N1, 2N4): one
file with no reviews read as `Limited Capital`, and one file retired a strategy
permanently.

**Taking "the nearest version that passes 3c" as the base.** The second pass's own
wording of the fix. Rejected on this revision's executed evidence (rule 3h, model
C3): a genuine `Demote` review stacked on a forged version passes 3c and would
supply `Limited Capital`. The base must also end upward.

**Ignoring a tip that has no base.** It establishes nothing, so ignoring it looks
safe. Rejected because a genuine demotion whose predecessor file was deleted is such
a tip, and ignoring it would read the stage before the demotion. The read raises
instead, which is zero capital (25d).

**A twelfth relationship type, e.g. `Promoted By`.** Rejected.
`framework/artifacts/relationships.py:1-12` records that `Knowledge/Relationships.md`
"is implemented, not extended", and `Validated By`
(`framework/artifacts/relationships.py:35`) already means what is needed.

**Dropping the `Validated By` edge as redundant with the ladder.** Rejected — rule 1. A
graph traversal reads relationships, not content. Made checkable instead.

**A new `Artifact` field, `ladder`.** Rejected on ADR-009 rule 8's reasoning: fields are
permanent and inside the hash, and `content` is inside the hash too.

**Reading `stage_at_review` from the stored subject instead of declaring it.** Rejected
in favour of declare-and-reconcile — rule 5.

---

## Required Follow-Up (ADR-015)

- **the per-rung minimum evidence grade — ruled 2026-09-22 (Part 18) and drafted as
  ADR-016 (18g).** The research is on this branch as
  `docs/proposals/evidence-bar-per-rung.md`; it had **two** independent
  falsification passes (first: 17 defects, 4 blocking, all applied; second: Issue
  #6). PR #15 corrections merged into this carrier with CI green. *(Corrected
  2026-09-24, finding S12. This bullet said they merged "after CI and an independent
  regression check"; nothing on GitHub records such a check. #15, #17 and #18 have
  no reviews, and the second review posted on PR #7 on 2026-09-22 found none. What
  is evidenced is CI, and that later review.)*
- **Parts 25 and 26 on `main`.** The owner's 25a-25j and 26a-26f are recorded on
  branch `claude/kind-knuth-9g7xlr` and not yet merged. Rules here that cite 25x or
  26x rest on that record
- **ratify or amend**, after ADR-016 is revised and a fresh independent pass has
  tried to break both
- **a fresh independent pass, BEFORE implementation, on this ADR and ADR-016
  together.** The owner's chosen different-AI pass on Issue #21 is still owed. Four
  passes have now found ten blocking defects in this ADR, in drafts whose citations
  and measurements were each time correct —
  which is the standing lesson that verifying an ADR's *facts* is not attacking its
  *rules*. ADR-014's Status block records what happened when the ordering was reversed:
  19 defect-grade errors across 93 claims, eight in committed code
- **implement rules 6, 5, 4, 1, 2, 3 in that order**, tests written first and run red
  against unchanged code. **Rule 5 before any REVIEW artifact is committed**, or it
  becomes a migration of append-only records
- **rule 3h's current-stage read, with rule 3b's downward append, landed in the same
  change as rule 3e's counting rule.** Since 26a the frontier no longer stops B2;
  only the read does. Separately, each reopens B2, S2 or 2N4
- **the subject index — required infrastructure for rule 3h step 5 and ADR-016 rule
  3 check 7.** Every stored REVIEW and REPORT, listed by `subject_id`, derived from
  the store and rebuildable by a full scan, never a separately maintained file. It
  lands in the same change as rule 3h, or step 5 runs as a full scan until it does.
  Without step 5, deleting one version file undoes a demotion (2N2)
- **the repair flag reaches a person.** `scripts/status.py` reports every strategy
  whose current-stage read carries `needs_repair`, and rule 3f's sweep lists every
  repair entry (rule 3h step 6, 26a)
- **rule 3f's chain sweep**, in the shape ADR-014 rule 7 and
  `tests/data/test_store.py:238-267` use. It is what rule 3c's one level deliberately
  does not do, and the residual-risk count above depends on it existing
- **a shared test fixture that climbs the ladder**, landed with rule 2 and not after it
- **`docs/HANDOFF.md` and `CHANGELOG.md` on ratification**, and not before
- **`.claude/skills/belay-review/SKILL.md:66` says "the 13 ADRs"** and was already wrong
  by one before this landed. F-025 of `reports/review/2026-09-04-review.md:404`.
  Deliberately not fixed on this branch
- **this ADR cites `workflows/Monthly/StrategyPromotion.md:43` knowingly**, where nine
  tracked locations — including `framework/artifacts/review.py:134`, inside a runtime
  error message — cite `:37`, which is the word `Demote`. F-020 of
  `reports/review/2026-09-04-review.md:155`, not this branch's to fix

### Still open, deliberately

**~~The minimum evidence grade per rung.~~ Settled.** RULED 18a and 18b (option D,
upward only), drafted in ADR-016 (18g). Rule 4's table points there. *(Finding B7:
this item said the table was empty and a Level D record bought real capital.)*

**~~Whether `Remain Current Stage` requires evidence.~~ Settled.** RULED 18c: always.
Rule 4 and test 22 now say so. **What is still open is the grade of a `Remain`
record** (18c "What it does not settle"), which ADR-016 puts to the owner.

**Put to the owner at ratification — DRAFTER choices in this revision, not
rulings:**

1. Freezing the specification from the first rung, not only on capital stages
   (rule 3g).
2. The revisable set: `confidence` and version bookkeeping only; title, tags,
   summary, author and editorial lifecycle frozen with the rest (rule 3g).
3. The current-stage read's cost against 9e(iii)'s "two extra reads" (rule 3h).
4. A raise on the capital read meaning zero capital (rules 3h and 8).
5. ~~Whether rule 3c should also resolve bound reports on a capital rung.~~
   Settled: RULED 26e, for the last rung's review whenever it binds reports
   (rule 3c).
6. One `Validated By` edge covering downward rungs too (rule 1, N6).
7. A pointer from ADR-004 rule 4, `strategies/Registry.md` and
   `Operations/README.md` to this ADR, which only the owner may add (rules 4 and 8).
8. The current-stage read's shape: `current_stage(id)` returning a `StageRead`, and
   `get(id)` with no version refusing on a STRATEGY identifier (rules 3h and 8).
9. The repair flag's five codes, and a flagged read acted on at the stage it reads
   (rules 3h and 8).
10. Rule 4(f)'s anchor (the later of the demotion review's `created` date and the
    latest data end already bound), and the literal reading of 26d that bars any
    data dated before a demotion, at a cost of at least ten years off capital for a
    demoted strategy; the alternative is "data a report used before the demotion"
    (rule 4(f)).
11. Confidence below the capital stages revisable freely, and the
    `confidence_review` shape (rule 3g, 26c).

**What happens to a strategy whose authorizing review is later found to be wrong.**
Owner selection 6 settles the *direction* — correction is forward, by appending a
correcting rung with its own review — and does not settle what that rung looks like
when the fault is in a review rather than in the strategy. `Superseded By`
(`framework/artifacts/relationships.py:39`) exists and nothing here rules its use.

**The denial of service that "longest history wins" admits.** Rule 3e. A forger who
writes three consistent files can own an identifier permanently, because nothing can
be deleted and identifiers are never reused. No mitigation inside this ADR; the
defences are access control, git review and rule 3f. A single forged downward file
no longer owns the identifier (26a, rule 3e): it lowers the read and is flagged
until a person repairs it.

**Who may sign, and whether Belay needs a real signature rather than a checksum.** The
largest question this ADR touches and much wider than F-007 — it reaches every artifact
type and every ADR in this file that says "signed".

**Whether artifacts other than STRATEGY and REVIEW need anything.** The evidence-hash
gap and the validation asymmetry named in rule 3.0 are both general, and nothing here
answers them.
