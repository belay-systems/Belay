# Belay Engineering Roadmap

This document sequences engineering work. It defines no policy, no thresholds, and
no promotion authority — those live in `constitution/` and are frozen by ADR-002.
Where this document refers to a gate or a criterion, it is citing the constitution,
not extending it.

Last verified: 2026-07-31

---

# Verified Current State

Everything below was confirmed by running or reading the repository, not inferred.

**`scripts/status.py` re-derives all of it on every run and is the figure to
trust.** The numbers here are a dated snapshot and had gone badly stale before
2026-07-31 — this section still read "46 passing" through four sessions and two
hundred new tests.

Test suite:
388 passing, 5 xfail, 1 skipped. Run `pytest` from the repository root. This read
387 until 2026-07-31 and was stale by one — see `docs/HANDOFF.md`.

What actually exists as working code:

- `framework/artifacts/` — the Artifact contract. Immutable artifact record,
  evidence records, lifecycle enum, deterministic integrity hashing, factory,
  validator, YAML serializer, filesystem repository, review decision record.
- `framework/metrics/` — seven modules. Under ADR-011: `drawdown.py`,
  `returns.py` (CAGR), `volatility.py`, `risk_adjusted.py` (Sharpe, Sortino) and
  `reporting.py`, which turns a computed number into a signed Artifact and
  refuses to emit one without the four disclosures `Validation/Backtesting.md`
  requires. Under ADR-012: `distributions.py` (Student's t, implemented rather
  than imported, pinned against a published table) and `statistics.py`
  (significance, confidence intervals, and how large a sample an observed effect
  would need).
- `framework/identifiers.py` — the eight documented identifier prefixes, with
  format validation at creation.

What does not exist:

- No market data layer
- No backtester
- No risk engine
- No strategy implementation
- The ten files under `framework/services/` average four lines and are placeholders

The asymmetry ADR-002 identifies still holds: the governance layer is
substantially more complete than the mechanics layer. This roadmap exists to
close that gap in a defined order.

---

# The Sequencing Principle

`constitution/Promotion_Pipeline.md` states that promotion shall consider seven
things:

1. Statistical performance
2. Risk-adjusted returns
3. Drawdown behavior
4. Regime robustness
5. Execution quality
6. Liquidity
7. Operational consistency

That list is the engineering backlog. Each item names evidence that some component
must be able to compute, and today **four of the seven have nothing behind
them** — down from six on 2026-07-31, when `Risk-adjusted returns` gained
`framework/metrics/risk_adjusted.py` (ADR-011) and `Statistical performance`
gained `framework/metrics/statistics.py` (ADR-012). A gate that cannot be
evaluated is not a gate.

**The four that remain are blocked on data rather than on arithmetic, and that
is a change of kind rather than of degree.** `Regime robustness` needs regime
classification and returns segmented by regime. `Execution quality` and
`Liquidity` need order and fill records — nothing in Belay has ever placed an
order. `Operational consistency` needs a run history to be consistent across.
Every one of them waits on Stage 2 or later, so **no further metrics ADR moves
this figure.**

Note that `scripts/status.py` grades a file `built` on twenty non-blank lines
without looking inside it. Four expected paths are still empty, and putting
anything at one of them turns a criterion green while nothing satisfies it.

Work is therefore ordered by which promotion criterion it makes computable, and by
what each step must exist before.

---

# Sequence

## Stage 0 — Artifact contract (complete)

The contract between mechanics and governance is in place and enforced.

- Immutable artifacts, evidence provenance, eight lifecycle states with validated
  transitions
- Deterministic SHA256 integrity via one shared primitive
- Signing is automatic in `ArtifactFactory`; unsigned artifacts fail validation
- Timezone-aware timestamps throughout

Status: closed. Both P1 findings and the timestamp finding in `docs/HANDOFF.md`
are resolved.

## Stage 1 — Metrics against supplied data (in progress)

Components that take a series of numbers and return an honest measurement, with
no dependency on where the data came from. These are cheap, testable by hand, and
each one retires a criterion from "nothing computes this".

`Validation/Backtesting.md` specifies the minimum metric set for a backtest to
count as evidence at all. It is the better-specified target than the promotion
criteria, because it is an explicit list rather than a set of categories:

| Metric | Status |
|---|---|
| Drawdown | built — `framework/metrics/drawdown.py` |
| CAGR | built — `framework/metrics/returns.py` |
| Sharpe | built — `framework/metrics/risk_adjusted.py` |
| Sortino | built — `framework/metrics/risk_adjusted.py` |
| Win rate | blocked on a ruling: a period or a trade? |
| Exposure | blocked: needs position records |
| Trade count | blocked: needs trade records |
| Benchmark comparison | blocked: needs a second return series |
| Tail events | blocked on a ruling: which threshold? |

The first four were computable from a return series alone and are done as of
2026-07-31. **The last five are blocked on inputs or rulings rather than on
effort**, and ADR-011 rule 11 scopes them out by name;
`test_only_the_backtest_metrics_adr_011_scopes_in_are_built` turns the suite red
if a sixth is added without the ruling it needs.

This roadmap's grouping of those five under "require trade-level records" was
close but not exact, and the distinction matters for sequencing: Benchmark
Comparison needs a second *series* rather than trades, and Tail Events needs
only a threshold nobody has stated. Neither depends on Stage 3.

`Validation/Backtesting.md` also requires every backtest to document its
assumptions, data source, sample period and known limitations. **That is
implemented as of 2026-07-31** — `Disclosure` in `framework/metrics/reporting.py`
carries all four, refuses a blank one, and puts them inside the artifact's
integrity hash. `EvidenceRecord` was not widened to hold them: its canonical
payload is pinned by a literal digest, and adding fields would move every
evidence hash ever computed. ADR-011 rules 9 and 10.

Unlocks: the Artifact contract exercised by more than one producer, and the first
evidence a promotion gate could actually read.

Volatility is built alongside these — `framework/metrics/volatility.py` — though
it is not one of the nine. Sharpe and Sortino both divide by a dispersion
measure, so it needed its own module and its own ruling rather than being buried
inside them.

## Stage 2 — Market data (complete)

A defined boundary for obtaining a price series, with provenance recorded on the
resulting evidence. Until this exists, every metric is fed by hand and nothing is
reproducible from a source.

Prerequisite for: any evidence graded above RESEARCH that claims to describe a real
instrument.

**ADR-013 is Accepted as of 2026-07-31 and IMPLEMENTED as of 2026-08-01, in all
ten rules.** `framework/data/` carries the contract, the survivorship disclosure,
the fetch record, the versioned store and two adapters. Suite 388 → 520.

**This stage is complete, and the gap it shipped with is half closed.** The
boundary works, and `disclosure_from` (`framework/data/fetch_record.py`) derives a
metric's `data_source` and `sample_period` from the fetch rather than from the
call site. **No metric emitter requires it.** Every emitter still takes a
caller-built `Disclosure`, and `significance_artifact` still takes a bare
`data_source: str` — which is open finding F-003. So the capability this stage
names exists and nothing obliges a caller to use it:

```
$ grep -rn 'disclosure_from' --include='*.py' . | grep -v '^./tests'
./framework/data/fetch_record.py:446:def disclosure_from(
```

Corrected 2026-09-25 (F-034). This paragraph previously claimed the derivation
was how metrics actually get their disclosure, which would have told a Stage 3
author that provenance arrives from the fetch when it does not.

What it originally did not deliver was *bulk* data: the chosen source's hosted
SQL API serves a novel month-sized query in 35–55 seconds and frequently exceeds
its own ~54s deadline, so a thirteen-year backfill was roughly 6.6 hours per
symbol. That was recorded as finding 14 rather than worked around, and **finding
14 closed the same day** — `framework/data/dolt_clone.py` is a second
implementation of the same injected seam, and it returns three years of daily
bars in **4.4 seconds**. Verified by running it, not by the suite:
`python scripts/verify_clone.py`.

**Two of the ADR's Required Follow-Ups closed against the source, not a
document.** The option database is CC BY-SA 4.0 (its own `LICENSE.md`) and does
retain expired contracts. **And one finding nobody had:** the free equity source
is survivor-only in its *prices* while its symbol table *accumulates* dead
tickers — it fails one half of rule 5's criterion and partly passes the other,
which is the reverse of the expected shape.

**Read its Status block first.** Two verification passes ran, and the independent
one found three defects the author's pass missed — including a rule resting on a
premise no file in the repository contained. All four are corrected and marked
inline, and it was ratified as corrected with no rule amended.

> This read "in eight rules" until the independent pass counted them. The
> miscount originated in the ADR and reached here and `CHANGELOG.md` before it
> was caught.

**Four of its parameters were open until 2026-07-31 and are now answered by the
owner.** See `docs/OwnerDecisions.md` Part 4. They do not scope the stage — the
ruling does that — but they remove the guesswork from what it is built against:

- **Daily bars.** Holding periods are days to months, so there is no intraday or
  real-time requirement, and no per-exchange fee or professional-status question
  arises. This is the cheapest tier of data and the one most likely to have
  usable free coverage.
- **A free or near-free source first**, because the market-data budget is
  effectively zero to start.
- **Which makes the survivorship disclosure mandatory rather than conditional.**
  A free source will almost certainly answer "no" to one or both survivorship
  questions, so under ADR-012 rule 10 — refuse to produce a number that "looks
  adjusted and is not", and disclose instead — the fact and its **direction** are
  a fixed module constant on every artifact derived from that source, not a
  caller-supplied string.
- **And the adapter contract must carry both survivorship questions from day
  one** — delisted *prices* and delisted *universe membership* — even though the
  first implementation answers "no" to both. **This is the concrete argument for
  ruling the boundary before writing the fetcher:** a contract that cannot
  express "this source does not know past universe membership" cannot record the
  answer on the day a better source does.

**Stage 2's close-out, as of 2026-09-25.** Both of the gaps this section used to
name as open are closed.

- **Provenance is durable. F-002 is closed** (`docs/HANDOFF.md`, "No Fetch Record
  Is Ever Written To Disk (F-002) — CLOSED 2026-08-02"). Stage 2 promises
  "provenance recorded on the resulting evidence", and `artifacts/RPT-0001/1.0.0.yaml`
  is a fetch record on disk.
- **ADR-014 is implemented.** `docs/DECISIONS.md`, ADR-014's Status block:
  "Accepted and implemented, 2026-08-02, in all nine rules." It rules where
  artifacts live, which git tracks, that `fetch_and_record` persists, what becomes
  of the one unprovenanced series Belay holds, and what a `.gitignore` comment may
  assert. **The identifier ruling no longer gates a bulk backfill — but the cost
  that gate was holding back has not been paid.** `Every Fetch Reads Every Stored
  Record`, below, is that cost: `records_by_stored_version` integrity-verifies
  every artifact under the root on every call, so a backfill of *n* symbols
  performs O(n²) record reads. The archive calls it "a defensible trade at today's
  scale and not at a universe backfill's". Read that finding before planning one.
  The live path has also never been executed — see Stage 2's note on `dolt` — so
  nothing here is verified against a real backfill.

**What that implementation left open**, all four carried in `docs/FINDINGS.md` and
written up in the archive:

- ADR-014 Rules 5 And 8 Cannot Both Be Executed As Written
- Rule 7's Orphan Check Is Vacuous On Every Machine But The One That Fetched
- The Store's Version Filenames Carry The Four-Digit Cap The Identifiers Shed
- Every Fetch Reads Every Stored Record

Corrected 2026-09-25 (F-034). This block previously cited F-002 as open and denied
ADR-014's implementation outright — both false since 2026-08-02, and both read as
current fact by every session `AGENTS.md` sends here. The identifier ruling it
named as blocking ADR-014 rule 4 is also settled — `docs/HANDOFF.md`, "The
Identifier Space Cannot Fund One Record Per Fetch — CLOSED 2026-08-02".

The old wording is described rather than quoted, because
`test_a_complete_stage_does_not_call_an_implemented_adr_unimplemented` cannot tell
a quotation from a claim. Same reason `scripts/review_due.py` asks for the
bracketed `F-[NNN]` form when a finding number is quoted from outside text.

**Corrected again the same day, by the independent pass on that correction.** The
first rewrite replaced one false absolute with another: it read "Nothing here gates
a bulk backfill" while citing, as evidence, a list containing the finding that does
constrain one. That is precisely F-034's failure mode — a complete stage asserting
something the repository contradicts a few lines below — reintroduced by F-034's
own fix. The bullet above now names the cost instead of denying it.

**One consequence should be visible rather than absorbed.** Point-in-time
universe membership is out of budget, and `Research/UniverseDiscovery.md` makes
Belay universe-driven by design. So universe-driven strategies cannot yet be
evaluated honestly — a gap between what Belay is specified to do and what its
data permits, which is a limitation of the evidence rather than of the code.

## Stage 3 — Backtester

Applies a rule to historical data and produces a result series that Stage 1 metrics
can measure. This is the first component whose output is an opinion about a
strategy rather than a description of data, so its evidence grading and its
assumptions (costs, slippage, look-ahead) matter more than its arithmetic.

Unlocks: paper-trading evidence, and therefore lifecycle states beyond VALIDATION.

## Stage 4 — Risk engine

Position sizing and exposure limits, expressed as artifacts that governance can
evaluate against `constitution/Capital_Authority.md`.

Prerequisite for: any capital allocation, including micro capital.

## Stage 5 — Services layer

The ten placeholders under `framework/services/` are given real implementations,
in the order that earlier stages make possible. Not before: a service with nothing
to orchestrate is another empty file.

The ten are `archive`, `base`, `critic`, `librarian`, `performance`, `portfolio`,
`promotion`, `regime`, `scientist` and `universe`. **Note what is not among
them**: `execution.py` and `liquidity.py`, both of which `scripts/status.py`
expects for constitutional promotion criteria. That is the narrow edge of the gap
the next four stages exist to close.

---

> **Stages 6 to 9 were added on 2026-07-31 and are deliberately unscoped.**
>
> Until that date this roadmap ended at Stage 5. `constitution/Mission.md:5`
> states Belay exists for "evidence-driven **capital allocation**" and line 38
> that it "optimizes for decades—not days" — but no stage deployed capital,
> placed an order, held a position or reported a tax lot. **The plan did not
> reach the mission**, and the omission was invisible because every stage that
> *was* listed is real and well-sequenced.
>
> Found by the repository owner asking how funds, execution and taxes would
> eventually work. Recorded as a finding in `docs/HANDOFF.md`.
>
> **These four are named so the gap is visible. Naming is not scoping.** Each
> needs a ruling before it is worked, and each says which. Do not start one on
> the strength of its title.

## Stage 6 — Execution and broker integration (unscoped)

Placing, cancelling and tracking orders, behind an interface with swappable
broker adapters rather than one hard-coded venue.

Nothing exists: no `execution.py`, no order model, and **no document names a
broker.** Broker-as-adapter is the owner's stated preference and is written down
nowhere, so it is a ruling rather than a design detail.

**Must not land before Stage 7's halt mechanism, or alongside it.** An execution
layer that can open positions faster than Belay can close them is the one
ordering of this work that would be dangerous.

Prerequisite for: anything Immutable Law III means by capital being *earned*.

## Stage 7 — Live position state and the halt mechanism (unscoped)

What Belay actually holds right now, as distinct from what a paper portfolio
says it should hold — and the emergency brake.

**This is `docs/HANDOFF.md` finding 8**, surfaced by ADR-004: a strategy
breaching a hard risk limit "needs to stop within seconds", and Belay's only
mechanisms for reducing exposure are demotion and retirement, both of which run
at the speed of a monthly review. ADR-004 is explicit that this is a missing
*axis*, not a demotion bug: lifecycle stage records earned capital, a halt flag
records whether the strategy is live, and conflating them would make the
emergency brake deliberative.

`strategies/RiskFramework.md` defines eight mandatory per-strategy limits and
none is implemented.

## Stage 8 — The operating loop (unscoped)

The thing that runs every day.

**Already fully specified, and this is the surprise.** `workflows/` holds
**thirteen** workflow documents including `Daily/MarketOpen`,
`Daily/MiddayReview` and `Daily/MarketClose`, and `framework/workflows/registry.py`
is an empty dict. **This is finding 2.** The operating layer is not unspecified —
it is unbuilt and, until now, unsequenced.

Expect a ruling regardless: `docs/HANDOFF.md` records that **not one of the
thirteen documents defines all five things `workflows/README.md` requires of a
workflow**, so whoever implements the base class is writing doctrine rather than
transcribing.

## Stage 9 — Tax awareness and reconciliation (scope narrowed 2026-07-31)

Knowing what a strategy's turnover costs after tax, and checking that what Belay
thinks it holds matches what the broker reported.

> **Superseded wording, preserved rather than deleted.** This stage read "Cost
> basis, lot selection, wash sales, and the records a filing needs" until
> 2026-07-31, when the owner answered that **the broker issues the tax documents
> and Belay needs to be aware of tax implications rather than be the system of
> record.** `docs/EndState.md` had identified two very different stages hiding
> under one name; this is the small one. See `docs/OwnerDecisions.md` row 6.

**In scope:** reconciliation against broker-issued documents, which needs Stage 7
and no new discipline; and tax-*aware evaluation*, so that two strategies with
identical pre-tax returns and different turnover are not compared as equals.
`constitution/Mission.md:7` — "purchasing power", which is an after-tax quantity —
is what makes the second one constitutional rather than a nicety.

**Out of scope:** Belay as the system of record. No per-lot cost basis ledger, no
lot-selection policy, no cross-account wash-sale engine, no filing output.

**The reduction is conditional and the condition must survive into the ADR:**
while Belay trades **one account at one broker**, the broker sees the whole
picture. A second broker or a second account reopens this at the large size,
because in some jurisdictions the rules that matter most are computed *across*
accounts precisely because no single venue sees everything.

**Two constraints on how it gets built, both inherited rather than new.**
Naming a tax concept is not ruling its treatment — Belay records facts and does
not decide law, which is a professional's determination in the operator's
jurisdiction. And a tax rate is a convention no Belay document states, so under
ADR-011's central holding it is a **required argument recorded inside the
artifact's integrity hash**, never a default — the same treatment the risk-free
rate already has.

**Searched all 101 documents: `tax`, `wash sale`, `cost basis` and `1099` return
zero hits.** The constitution is still silent, so this remains a ruling to make
rather than one to apply.

---

# Specified But Not Built

Taken from a full read of every document in the repository on 2026-07-26. These are
not defects — no code contradicts them, because no code attempts them. They are
listed so the size of the gap is visible in one place rather than spread across
forty documents.

Nothing here should be built before the stage that needs it. The point of the list
is to stop the same specification being rediscovered every session.

| Specified in | What it defines | Built |
|---|---|---|
| `Validation/Backtesting.md` | 9 minimum backtest metrics | 4 of 9 |
| `strategies/RiskFramework.md` | 8 mandatory per-strategy risk limits | none |
| `strategies/PositionSizing.md` | 7 sizing inputs, 4 outputs | none |
| `Research/RegimeDetection.md` | regime estimate with probability distribution | none |
| `Research/UniverseDiscovery.md` | universe report, 7 fields | none |
| `strategies/PaperPortfolio.md` | paper portfolio, 10 recorded elements | none |
| `Operations/PortfolioManager.md` | simulated execution, holdings, attribution | none |
| `Operations/StrategyEngine.md` | 7 mandatory strategy definitions | none |
| `strategies/Registry.md` | strategy inventory, 9 fields, 2 rules | stub only |
| `Knowledge/MemoryIndex.md` | index across 10 dimensions | none |
| `Knowledge/KnowledgeGraph.md` | append-only directed graph | none |
| `Knowledge/Search.md` | retrieval across 9 filters | none |
| `Knowledge/Taxonomy.md` | 12 knowledge domains | none |
| `workflows/` | 13 workflows | 0, registry is empty |
| `docs/ENGINEERING_AGENT.md` | 5 engineering agent components | none |

A note on sequencing that the documents make clear and this roadmap previously did
not: `Validation/Workflow.md` runs Research Memo → Critic → Backtesting →
Statistical Review → Capital Review → Recommendation. Backtesting sits in the
middle of a chain, not at the start. The Critic — which exists to falsify a
hypothesis before resources are spent on it — comes first, and is one of the
cheapest components on this list to build.

---

# Open Engineering Items

Carried from `docs/HANDOFF.md`:

- P3 — `departments/validation.py` imports `framework.services.backtesting`, which
  does not exist. `departments/Research/research.py` imports
  `framework.departments.base`, which is not a package. Latent: nothing imports
  either module today.
- `workflows/` (prose) and `framework/workflows/` (code) share a name and different
  layers. Recorded in ADR-002 as required follow-up.
- Each remaining top-level directory needs assigning to exactly one layer. Recorded
  in ADR-002 as required follow-up.

# Settled By The Governance Layer

This section held four open questions. All four were ruled on 2026-07-30 and are
recorded here as answers rather than deleted, because the reasoning is what a
future session needs.

`MICRO_CAPITAL` was missing from the lifecycle and has been added. That gap was
real independent of any interpretation: `Paper_First_Capital_Doctrine.md` lists
eight stages and the code implemented seven.

**ADR-002's "eight promotion gates" was false, not merely unattributed.** It cited
`Promotion_Pipeline.md`, which contains no group of eight — seven maturity levels
and seven promotion considerations. The groups of eight are the eight stages of
`Paper_First_Capital_Doctrine.md` and the eight evaluation categories of
`strategies/PromotionCriteria.md`. **ADR-007 amended it** to cite the doctrine,
preserving the original sentence in the amendment note.

**The seven promotion criteria this roadmap is built on are now ruled, not
assumed. ADR-006.** `constitution/Governance.md:7` states "The Constitution
possesses authority", so `Promotion_Pipeline.md:75-81` governs. The five
documented lists are not five rivals: `Promotion_Pipeline.md` states the
*criteria*, `Validation/Backtesting.md` states *instruments* that measure some of
them, and `CapitalReview.md` and `StrategyPromotion.md` are *departmental
checklists* operating the constitutional criteria. Where a checklist diverges it
is wrong, not authoritative. Reading all five in full: no criterion appears in all
five, and `Drawdown` — closest at four of five — is absent from the one document
defining a Promotion Score.

**The constitution's apparent self-disagreement was a category error, now ruled.
ADR-007.** `Promotion_Pipeline.md` gives seven levels and no promotion review;
`Paper_First_Capital_Doctrine.md` gives eight stages and includes it. These are
not two sequences competing. The doctrine's eight stages are the **lifecycle** —
what capital a strategy has earned. `Promotion_Pipeline.md`'s seven levels are a
**maturity model** — how proven it is. Two axes. `StrategyLifecycle` implements
the doctrine and is ratified unchanged.

The earlier instruction that "no code change should rest on `Promotion_Pipeline.md`
alone" is **withdrawn** — it was correct while the choice was an assumption and is
obsolete now that ADR-006 rules it. `scripts/status.py:48-56` may rest on those
seven.

Demotion is representable: ADR-004 added ten backward transitions. Retirement is
reachable from every stage. `Remain` is ruled by ADR-008 to be a review outcome
rather than a transition, so nothing is added to the table for it.

**Review decisions are recordable as of 2026-07-31.** ADR-009 made the review
decision record an Artifact of type `REVIEW`, discharging the three obligations
that had been waiting on it: ADR-004 rule 4 (written justification for a
demotion), ADR-004's re-sizing step, and ADR-008's `Remain Current Stage`.
`ArtifactSerializer.load()` landed with it, so artifacts can be read back rather
than only written.

**The follow-ups from ADR-006 and ADR-007 are applied**, as of 2026-07-31: three
departmental documents reconciled to the constitutional wording, and two
conformance tests — `PROMOTION_CRITERIA` parsed against
`Promotion_Pipeline.md:75-81`, and the doctrine's eight stages compared to
`StrategyLifecycle` as an ordered sequence.

**Stage 1 was the binding constraint and is now half discharged. ADR-011,
2026-07-31.** Four of the nine backtest metrics compute, `Risk-adjusted returns`
has a component behind it, and the four things a backtest must document are
recorded on every metric artifact and covered by its signature. The governance
layer is no longer *implemented and idle*: a review reading a Sharpe ratio now
finds one, and finds the risk-free rate it was computed against alongside it.

**What ADR-011 changed about how the rest of this roadmap gets built.** The
document names metrics and does not define them, and four of the nine could not
be computed without a convention no Belay document states. The ruling is that
none of those conventions is ever defaulted — they are required arguments,
recorded inside the artifact's integrity hash. Expect the same shape wherever a
later stage meets a specification that names a thing without defining it, which
on the evidence of `strategies/RiskFramework.md` and `strategies/PositionSizing.md`
is most of them.

**The remaining constraint is no longer effort.** Five of the nine metrics are
blocked on a missing input or an unmade ruling, not on time — see the Stage 1
table and `docs/HANDOFF.md`'s ninth finding.

**And `Statistical performance` closed the same day, ADR-012.** That criterion
was the one piece of the promotion pipeline that needed no new data — it asks
whether the record already in hand is distinguishable from luck — which is why
it could be taken immediately after Stage 1's metrics and why nothing else on
the list can be.

`constitution/Promotion_Pipeline.md:27` defines maturity Level 2 **as** "Passed
statistical review", so until 2026-07-31 a level of the constitution's own
maturity model referred to a review Belay could not perform. It can now compute
the number that review reads. **It still does not decide the promotion** —
ADR-012 rule 11 keeps that with a recorded review, and `Promotion_Pipeline.md`'s
levels remain a maturity model rather than the lifecycle (ADR-007 rule 2).

**Stage 2 is now the binding constraint.** Every remaining promotion criterion
needs data Belay cannot obtain: regimes, orders, fills, or a run history. The
metrics layer has gone as far as hand-supplied series allow, and every artifact
it emits says so in its own Known Limitations.
