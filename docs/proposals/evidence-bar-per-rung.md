# PROPOSAL — A Minimum Evidence Bar Per Rung

**Status: PROPOSAL, awaiting the owner's ruling. Dated 2026-09-19. Nothing here is
doctrine and no code changes with it.** Requested by the owner on 2026-09-19
(selection: "Research a bar first") as a precondition for ratifying ADR-015, whose
own Still-Open section names this the first thing the owner should look at. A second
owner selection the same day — "Evidence for everything" — rules that every
lifecycle move, up or down, carries an evidence record; section 5 is this document's
reading of what that honestly means downward.

> **Revised 2026-09-19 after an independent verification pass, which found 17
> defects — 4 of them blocking.** All 17 are applied and listed in the appendix, so
> the record shows what changed (Law VII, `constitution/Immutable_Laws.md:49-51`).
> The first revision said its 83 `path:line` citations had been checked only by
> their own author and asked to be attacked. It was, and it lost four claims that
> would have changed a capital rule:
>
> 1. **The candidate tables were keyed by `(from → to)`; ADR-015 rule 4's table is
>    keyed by destination alone.** Four destinations are *both* a climb destination
>    and a demotion destination, so a floor ruled for the climb would have silently
>    become a floor on an emergency demotion. Fixed in both documents, and ADR-015
>    rule 4 now carries an explicit direction clause. **That is the only change this
>    revision makes to ADR-015.**
> 2. **Section 9 claimed every grade in the recommendation "is derived from a
>    document rather than chosen". It is not.** No document maps a stage to a grade —
>    section 2 of this very document says so. The mapping is an *inference from
>    names*, and section 9 now says that in those words.
> 3. **Sections 6 and 9 understated what the recommendation closes.** It closes every
>    rung above `Validation` until a Backtester exists, and two of them additionally
>    depend on unscoped roadmap stages.
> 4. **Question 1 omitted the status quo.** "No floor at all" is a real option with a
>    real cost, and the owner was not being offered it.
>
> **The independent reviewer's recommendation differs from this document's author's.**
> Both are now set out side by side in section 9, with each one's reasoning and cost
> and no winner declared. Section 10's questions are ordered to be asked one at a
> time.

**This document has now had one independent verification pass, not two.** Every ADR
in `docs/DECISIONS.md` that has had a *second* reader lost claims to it, and ADR-015
itself lost five blocking defects across two passes that its author had not found.
One pass is better than none. It is not enough to read section 4's grades and
section 9's two recommendations as checked fact.

ADR-015 is cited by description only. It lives on `origin/adr/015-stage-is-carried`
and is not on `main`, so no line of it is cited by path.

---

## Why this exists, in plain words

The strategy lifecycle is a ladder of eight stages. ADR-015 proposes that a strategy
may only climb a rung if it carries a signed REVIEW artifact that granted it, and that
the review must carry at least one evidence record. That closes a real hole. But an
**evidence record** in Belay is a small signed note saying "here is a source, here is
a method, here is how good this is" — and the "how good" is a letter the author picks.
A record graded **D — hypothesis** is a perfectly well-formed record. So as ADR-015
stands, one self-written Level D note buys a promotion into **Micro Capital**, the
first stage where real money is at risk. No Belay document says which letter is needed
for which rung. That is the gap.

---

## 1. The ladder and the four letters, as the repository defines them

**The eight stages** are declared at `framework/artifacts/enums.py:85-92`, from
`constitution/Paper_First_Capital_Doctrine.md:13-41`. The ninth member, `Retired`
(`framework/artifacts/enums.py:93`), **is not a stage**: the doctrine places
retirement outside the sequence, and `STRATEGY_LADDER`
(`framework/artifacts/enums.py:107-109`) drops it for exactly that reason. The
comment above it, `framework/artifacts/enums.py:96-109`, records why: `RETIRED` sits
positionally above `PRODUCTION`, so any ordinal comparison that forgets to classify
it first reads a retirement as the deepest promotion in the system.

**The legal moves** are `framework/artifacts/validator.py:57-102`: forward one stage
at a time (`strategies/Lifecycle.md:41`, "Strategies never skip stages"), backward any
distance down to a `Paper Trading` floor, and `Retired` from anywhere. Seven forward
rungs exist; the fifth, `Promotion Review → Micro Capital`, is the one that releases
real money (`framework/artifacts/enums.py:75-79`).

**The four evidence classes** are `constitution/Evidence_Standards.md:7-35`,
implemented as `EvidenceLevel` at `framework/artifacts/enums.py:4-13`, described
again at `Knowledge/EvidenceRegistry.md:5-45`:

| Level | Constitution | Evidence Registry |
|---|---|---|
| A | "Live validated." `constitution/Evidence_Standards.md:9` | "Observed using real capital." `Knowledge/EvidenceRegistry.md:9` |
| B | "Paper validated." `constitution/Evidence_Standards.md:17` | "Observed through simulated execution." `Knowledge/EvidenceRegistry.md:19` |
| C | "Historical simulation." `constitution/Evidence_Standards.md:25` | "Requires validation." `Knowledge/EvidenceRegistry.md:31` |
| D | "Hypothesis." "Research only." `constitution/Evidence_Standards.md:31-35` | "Academic literature. Theoretical reasoning." `Knowledge/EvidenceRegistry.md:41-43` |

Two rules already bind the letters: `constitution/Evidence_Standards.md:39` —
"Evidence hierarchy may never be reversed" — and `Knowledge/EvidenceRegistry.md:49-51`
— "Evidence only moves upward through validation."

---

## 2. What the documents already say, and where they stop

**They demand evidence, repeatedly, and never grade it.**
`constitution/Paper_First_Capital_Doctrine.md:45-47` ("Promotion requires evidence.
Never confidence alone"); `constitution/Immutable_Laws.md:23-25` (Law III, capital
must be earned), `:9`, `:31-33` ("Past performance is evidence. It is never proof"),
`:39`; `constitution/Evidence_Standards.md:45` ("Every conclusion must reference
supporting evidence"); `constitution/Governance.md:11-15`;
`strategies/PromotionCriteria.md:3`, `:33`, `:35`;
`strategies/ReviewTemplate.md:59-61` ("Justification. Evidence only.").

**Where a bar is implied but never stated as a grade.**

- **The seven promotion criteria**, `constitution/Promotion_Pipeline.md:75-81`,
  canonical under ADR-006 rule 1 (`constitution/Promotion_Pipeline.md:101-105`);
  `:83`, "Promotion shall never depend upon profitability alone."
  `scripts/status.py:48-55` maps each to the module that would compute it and
  `scripts/status.py:397` prints the count. **That is the dashboard's "3 of 7
  computable":** `framework/metrics/statistics.py`, `framework/metrics/risk_adjusted.py`
  and `framework/metrics/drawdown.py` exist; `framework/services/regime.py` and
  `framework/services/performance.py` are ten-line placeholders;
  `framework/services/execution.py` and `framework/services/liquidity.py` do not
  exist.
- **The nine backtest metrics and four disclosures**, `Validation/Backtesting.md:13-31`
  and `:35-43`; `:47-49`, "Outputs become evidence. Not guarantees." The disclosures
  are already enforced — `framework/metrics/reporting.py:142-165` refuses a blank one.
- **The validation sequence**, `Validation/Workflow.md:3-27` — Research Memo, Critic,
  Backtesting, Statistical Review, Capital Review, Recommendation, Operations — with
  "Evidence quality" first among what promotion considers
  (`Validation/CapitalReview.md:13-25`); and the Critic's questions,
  `Validation/Critic.md:21` and `:23` ("Could randomness explain the result?").
- **The precedent for referring a number upward.**
  `strategies/PromotionCriteria.md:29` sends promotion thresholds to the Investment
  Committee, and `:46-50` records that the 0-100 Promotion Score is **suspended, not
  adopted**, because nobody supplied weights or a threshold.

**Where they conflict or leave a hole.**

1. **No document maps a stage to an evidence class.** Checked across `constitution/`,
   `strategies/`, `Validation/`, `workflows/`, `Knowledge/`, `Operations/`,
   `Research/`. They name criteria, and name classes, and never join them. **The
   nearest miss is `strategies/Registry.md:27-29`** — the stub registry record carries
   `Evidence Level` `D` a few lines below `Current Stage` `Hypothesis`
   (`strategies/Registry.md:19-21`), which is the only place in Belay where a stage
   name and a grade sit on one record. **It establishes no rule, for two reasons.** It
   is an illustrative stub — `:25` carries `38%` as a made-up confidence — and
   `Hypothesis` is not a lifecycle stage at all: it is Level 1 of the *maturity* model
   at `constitution/Promotion_Pipeline.md:15-19`, which
   `constitution/Promotion_Pipeline.md:87-95` rules is a different axis from the eight
   stages. A stage-to-grade rule cannot be read off a record whose "stage" is from the
   other axis.
2. **No document states any number.** A sweep of those directories for thresholds,
   durations, percentages and minimums returns only
   `strategies/PromotionCriteria.md:29` (deferred), `strategies/RiskFramework.md:15-19`
   (three thresholds named with no values) and `strategies/Registry.md:25` (`38%`, an
   illustrative figure on a stub). **Every number below is therefore written "NUMBER
   NOT RULED".**
3. **Out-of-sample testing, walk-forward validation and multiple-testing correction
   appear in no Belay document.** The nearest things are `Validation/Critic.md:23` and
   ADR-012 rule 10 (`docs/DECISIONS.md:2244-2251`), which rules those corrections
   *deliberately out of scope* because Belay records the number of strategies tried
   nowhere. **The phrase does exist in shipped code, in one place and as a
   disclosure rather than a rule:** `framework/metrics/statistics.py:61-62` states
   that "No multiple-testing or data-snooping correction is applied, because Belay
   does not record how many strategies were tried". Proposing any of them as a
   requirement is still proposing a new rule.
4. **A live naming conflict, recorded rather than settled.**
   `strategies/PromotionCriteria.md:52-64` records that its list omits `Drawdown
   behavior` and writes `Execution Consistency` for the Constitution's `Execution
   quality`; `Validation/CapitalReview.md:48-60` records that its own list omits four
   constitutional criteria and may carry `Consistency` and `Operational consistency`
   as one idea twice. Any "one record per criterion" bar inherits that and must name
   its list. This document means `constitution/Promotion_Pipeline.md:75-81`.

---

## 3. What each letter can honestly mean today

A bar nobody can meet is a closed door, and closed is the safe default for a capital
rung — but it should be closed knowingly.

| Level | Producible today? |
|---|---|
| **D** | **Yes**, by anyone, by hand. It is a typed note. |
| **C** | **Partly.** `framework/metrics/reporting.py:192-196` grades every metric artifact `HISTORICAL` — Level C — with the four disclosures inside its integrity hash, and `framework/metrics/statistics.py` produces a significance report. But the **Backtester is Stage 3 and is not built** (`docs/ROADMAP.md:240-247`). Belay can produce Level C evidence *about a series handed to it*, not *about a strategy's simulated returns*, because nothing generates those returns. |
| **B** | **No.** `docs/ROADMAP.md:247` states it: Stage 3 "Unlocks: paper-trading evidence, and therefore lifecycle states beyond VALIDATION." |
| **A** | **No.** Execution and the halt mechanism are Stages 6 and 7, both marked unscoped in `docs/ROADMAP.md:286` and `:301`. |

**One structural consequence rules out an obvious answer.** Level A means "Observed
using real capital" (`Knowledge/EvidenceRegistry.md:9`), and `Micro Capital` is the
*first* stage committing real capital (`framework/artifacts/enums.py:75-79`). So **a
rule requiring Level A to enter Micro Capital is not strict, it is a deadlock**: the
evidence it demands can only be produced by the stage it guards. The highest honestly
achievable bar on that rung is **B**. That ceiling is derived, not chosen.

---

## 4. Four options for the floor

All four keep ADR-015's base — evidence present, and passing
`EvidenceRecord.verify()` (`framework/artifacts/evidence.py:77-84`). Three of them
add a floor on top of it.

> **The options were called "Candidate A / B / C" in the first revision.** They are
> renamed here because Belay already uses A, B, C and D as the names of evidence
> *grades*, and "Candidate B requires Level B on two rungs and Level A on two others"
> is a sentence nobody should have to parse twice. The names are now descriptive.

### Every table below is keyed the way ADR-015 rule 4 is keyed, and applies upward only

ADR-015 rule 4's empty table has one row per **destination stage** (`to_stage`) and
no `from_stage` column. Four destinations are reached both by climbing and by falling
— read from `framework/artifacts/validator.py:57-102`:

| Destination | Reached by climbing from | Also reached by falling from |
|---|---|---|
| Paper Trading | Validation | Promotion Review, Micro Capital, Limited Capital, Production |
| Promotion Review | Paper Trading | Micro Capital, Limited Capital, Production |
| Micro Capital | Promotion Review | Limited Capital, Production |
| Limited Capital | Micro Capital | Production |

**So a floor written as "Validation → Paper Trading requires C" and then filed in a
table keyed by destination would also mean "Production → Paper Trading requires C" —
a grade gate on an emergency demotion.** That is the delay section 5 exists to
prevent and that ADR-004 rule 4 (`docs/DECISIONS.md:396-400`) forbids in terms: a
bar on withdrawing a privilege "would make capital something Belay must prove a
strategy no longer deserves".

**The fix, and it is part of what is being ruled:**

> **Any floor ruled below applies only when the move is upward.** Direction is
> computed, in this order: a move whose `to_stage` is `Retired` is a retirement and
> is never upward; otherwise the move is upward when the destination's position in
> `STRATEGY_LADDER` (`framework/artifacts/enums.py:107-109`) is greater than the
> origin's. **`STRATEGY_LADDER` and not `list(StrategyLifecycle)`** — the warning at
> `framework/artifacts/enums.py:96-109` is exactly this trap, and reading `RETIRED`
> by its declared position would demand the system's strongest evidence on its
> fastest capital-preservation act.

ADR-015 rule 4 was amended on this branch to say that, beside its still-empty table.
Nothing else in ADR-015 changed.

### A note on what the tables can and cannot carry

The first revision gave each row a **"Min. count"** and a **"Must carry"** column.
**As ADR-015 rule 4 consumes the table, neither column has a mechanism.** The
consumption rule is a lookup on `to_stage` and a `>=` against the artifact's
`evidence_level`, which `strongest_evidence_level`
(`framework/artifacts/enums.py:29-43`) derives as **the single strongest grade
present**. It cannot see how many records there are, and it cannot see what any of
them is *about*. A ruled "three records" or "must carry the survivorship caveat"
would be prose in an ADR that nothing reads.

**Both columns are therefore dropped from the tables and turned into a choice**
(section 10, question 6): rule the grade now and leave the rest as prose to be
implemented later, or rule section 7's artifact binding as part of the same ruling,
which is the thing that would give "must carry" something to check. The counts are
written `NUMBER NOT RULED` on every row, identically, because `≥1` is itself one of
the options in question 1 and not a ruled number.

### Option 1 — "No floor" (the status quo, and what ADR-015 does if nothing is ruled)

ADR-015's base rule only: a stage move carries at least one evidence record, and the
record verifies. No grade is required anywhere.

**Cost, stated by ADR-015 itself:** "a single Level D record … satisfies it for a
promotion into real capital." One self-written note reading "I think this will work"
buys `Micro Capital`. This is not a hypothetical reading of the rule — it is the
sentence ADR-015 wrote about its own unfilled table, and it is the reason owner
selection 4 blocked ratification on this research. Choosing it is choosing that,
knowingly, and the cost of choosing it is that ADR-015 can be ratified today.

### Option 2 — "Hypothesis floor"

One line: **no rung at or above `Validation → Paper Trading` may be authorized by
Level D evidence alone.** Grades above that, counts and durations are all referred to
the Investment Committee, exactly where `strategies/PromotionCriteria.md:29` already
sends the promotion threshold.

| Destination (`to_stage`), upward only | Min. level | Min. count |
|---|---|---|
| Research | *none beyond ADR-015's base* | NUMBER NOT RULED |
| Validation | *none beyond ADR-015's base* | NUMBER NOT RULED |
| Paper Trading | **above D** | NUMBER NOT RULED |
| Promotion Review | **above D** | NUMBER NOT RULED |
| Micro Capital | **above D** | NUMBER NOT RULED |
| Limited Capital | **above D** | NUMBER NOT RULED |
| Production | **above D** | NUMBER NOT RULED |
| Retired | no floor — never an upward move | NUMBER NOT RULED |
| any downward move | no floor (§5) | NUMBER NOT RULED |

### Option 3 — "Producible-grade floor"

Each destination requires at least one record at the grade the stage being *left* is
defined to produce. The intent is that no rung demands evidence that cannot exist.

| Destination (`to_stage`), upward only | Climbed from | Min. level | Min. count |
|---|---|---|---|
| Research | Idea | D | NUMBER NOT RULED |
| Validation | Research | D | NUMBER NOT RULED |
| Paper Trading | Validation | **C** | NUMBER NOT RULED |
| Promotion Review | Paper Trading | **B** | NUMBER NOT RULED |
| Micro Capital | Promotion Review | **B** | NUMBER NOT RULED |
| Limited Capital | Micro Capital | **A** | NUMBER NOT RULED |
| Production | Limited Capital | **A** | NUMBER NOT RULED |
| Retired | — | no floor — never an upward move | NUMBER NOT RULED |
| any downward move | — | no floor (§5) | NUMBER NOT RULED |

**The one-line principle has an exception, and the exception covers the rung that
releases real money.** Two origin stages produce no evidence of their own:

- **`Idea`** is where a strategy is born; it has produced nothing yet. The
  destination `Research` therefore carries the weakest grade, D.
- **`Promotion Review` is a decision stage, not a producing one.** Nothing runs
  there; a committee reads what `Paper Trading` produced and decides. Yet its
  destination is `Micro Capital` — the rung that releases capital.

**So the rule is: the floor is the grade produced by the last stage on the path that
produces evidence at all.** For `Micro Capital` that is `Paper Trading`, which is why
the row reads B and not "none". This is a *second* inference on top of the first one,
and it is what carries B onto the most consequential row in the table. Section 3's
ceiling independently says B is also the highest grade that row could ever honestly
carry, so the two readings agree there — but they agree by coincidence, not by
derivation, and the owner should know that the most important cell in this table is
the one supported by the least.

**What the dropped "Must carry" column would have said**, kept here as prose because
it is the input to question 6 and not a ruled requirement:

- On `Paper Trading`: the four disclosures of `Validation/Backtesting.md:35-43`,
  already enforced at `framework/metrics/reporting.py:142-165`; and the survivorship
  caveat that `framework/data/survivorship.py:143` says a source "forces onto every
  artifact", whose `basis` `framework/data/survivorship.py:122-127` already refuses
  to leave blank.
- On `Promotion Review` and `Micro Capital`: a paper track record of N sessions —
  **N NOT RULED; no Belay document gives one** (question 4).

### Option 4 — "Criterion coverage"

Option 3, plus on the three capital destinations one record **per promotion
criterion** of `constitution/Promotion_Pipeline.md:75-81` — seven records, each at or
above that destination's floor. **Unmeetable today for four of the seven**, and the
dashboard already says so (`scripts/status.py:397`). Adopting it gates capital on
finishing four service modules first. It also inherits the naming conflict at §2
point 4 and would need to name its list, which this document does above.

---

## 5. Downward moves — what honestly counts, without slowing an emergency

"Evidence for everything" reaches demotion and retirement, and the danger is obvious:
**a bar on the way down is a delay on the way down.** Three things in the repository
settle the shape without anyone guessing.

1. **ADR-004 rule 4 already ruled it for justification** — `docs/DECISIONS.md:396-400`:
   "Requiring a promotion-grade score to *withdraw* a privilege would invert the
   doctrine: it would make capital something Belay must prove a strategy no longer
   deserves."
2. **`docs/DECISIONS.md:424-429`** rules that the six
   `constitution/Capital_Authority.md:13-18` inputs "may never gate the demotion
   itself", on `constitution/Capital_Authority.md:22-27` — "Capital preservation wins.
   Always."
3. **`constitution/Strategy_Retirement.md:11-18`** lists six retirement reasons, and
   for some of them **the worst case is that the only available evidence is
   reasoning, which is Level D.** A structural market change *observed with real
   capital* is Level A and in paper Level B; a falsified backtest assumption is Level
   C — this document's own section 5 wording says so. But "Structural market change"
   and "Invalid assumptions" can also be recognised *before* any of that is
   measurable, which is precisely when retiring is most valuable, and in that case a
   reasoned argument is all there is. **A grade floor on retirement would, in that
   case, block a constitutional retirement reason.**

   *(Corrected in this revision. The first revision claimed those two reasons "may
   only ever be" Level D, which is false and was flagged as a defect. The conclusion
   survives on points 1 and 2 regardless of point 3.)*

**Proposed rule for every downward move, in all four options:**

> A demotion or retirement requires **at least one evidence record describing the
> observed condition that triggered it**, graded at the level of that observation — a
> live breach is A because it was observed with real capital, a paper breach B, a
> falsified backtest assumption C, a reasoned structural argument D. **There is no
> minimum grade, and none may be added.** The record of the breach *is* the evidence;
> producing it adds no work, because the thing that triggered the move is the thing
> being recorded.

This satisfies "Evidence for everything" with zero added latency on a
capital-preservation act. It gives `strategies/RiskFramework.md:21-23` ("Violation of
risk constraints triggers automatic investigation") something to attach to, and feeds
`constitution/Failure_Handling.md:11-23`, whose six steps open with root cause and
evidence review.

**Both recommendations in section 9 agree on this**, and so does ADR-015 rule 4 as
drafted. It is put to the owner as question 2 anyway, because it is a rule about
capital and a rule nobody was asked about is a rule nobody chose.

---

## 6. What each buys, what it costs, what stays forgeable

**Protects against.** All three floors close the hole ADR-015 leaves: one
self-written Level D note buying a real-money rung. The producible-grade floor and
criterion coverage additionally make a rung's evidence *grade* match the kind of
observation the ladder claims, which is what stops a backtest being presented as a
paper track record.

**One thing no floor here touches, and it should be said before the costs.** Under
every option, **a promotion from `Promotion Review` into `Micro Capital` — the rung
that releases real money — requires none of the seven canonical promotion criteria**
of `constitution/Promotion_Pipeline.md:75-81` (canonical under ADR-006 rule 1,
`constitution/Promotion_Pipeline.md:101-105`). One record at the ruled grade buys it.
A grade floor says how *good* one piece of evidence must be; it says nothing about
*what the evidence is about*. Only option 4 closes that, and only by gating capital
on four unbuilt modules.

**Costs, counted against section 3 rather than asserted.**

- **No floor** is free and buys nothing. Its cost is the Level D purchase of real
  capital, in full.
- **Hypothesis floor** requires a grade above D from destination `Paper Trading`
  upward. By section 3, Belay cannot today produce Level C *about a strategy's
  simulated returns* — the Backtester is Stage 3 and is unbuilt
  (`docs/ROADMAP.md:240-247`). **So it closes every rung above `Validation` until
  Stage 3 exists**, and no further: once Stage 3 ships, a Level C backtest record
  could buy every remaining rung including `Micro Capital`.
- **Producible-grade floor** closes the same rungs for the same reason, **and then
  keeps three of them closed for longer**. `Promotion Review` and `Micro Capital`
  require Level B, which `docs/ROADMAP.md:247` says Stage 3 unlocks; `Limited
  Capital` and `Production` require Level A, which needs live execution and the halt
  mechanism — **Stages 6 and 7, both marked unscoped** (`docs/ROADMAP.md:286`,
  `:301`). Stated plainly: **it closes the door to real money until a paper-trading
  engine exists, and closes the two rungs above `Micro Capital` until work that has
  not been scoped is finished.**
- **Criterion coverage** additionally blocks capital on four unbuilt modules and is in
  practice a multi-year gate.

**What stays forgeable under all four — the ceiling, and it is low.**
`EvidenceRecord.verify()` (`framework/artifacts/evidence.py:77-84`) recomputes the
record's hash over its own fields (`framework/artifacts/evidence.py:62-75`). **It
proves the record has not been edited since creation. It proves nothing about whether
the evidence is true, adequate, or of the grade it claims.** `level` is a field the
author sets (`framework/artifacts/evidence.py:12-18`); nothing binds a record graded B
to any paper run that happened. A grade bar buys **declaration discipline, not truth**
— it makes a forgery more specific and more legible, not impossible. That is the same
limit `ArtifactIntegrity.sign()` has, and ADR-015 records it in the same voice.

---

## 7. The strengthening to consider alongside

**Bind an evidence record to a stored, signed artifact by id + version + hash.** A
record's `provenance` is a free string today (`framework/artifacts/evidence.py:12-18`).
Proposed: for any rung at or above `Validation → Paper Trading`, each qualifying
record names a **stored REPORT artifact** by identifier, version and integrity hash,
and storage resolves it. Then a Level C claim is only as good as a real signed
Backtest Report, whose four disclosures `framework/metrics/reporting.py:142-165`
already refuses to leave blank.

**This is also the only mechanism that would make a "must carry" requirement
checkable** — see section 4's note on the dropped columns. Without it, "the record
must carry the survivorship caveat" is prose.

**ADR-015's own machinery can enforce this with no new invention.** Its rule 1 already
defines a three-part reference — review id, version, integrity hash — and its rule 3
already has `save()` resolve it and compare hashes. Pointing the same mechanism at an
evidence record's supporting report is the identical shape one level down.

> **Editor's note, added when this document was committed to the branch — not the
> research author's text.** This section was written against an earlier revision of
> ADR-015. Checked against revision `d734bcb` and it holds, with two refinements
> worth stating so nobody re-derives them:
>
> - The three-part reference is real but it is not the whole rung. A rung in rule 1
>   is **five** strings — `from_stage`, `to_stage`, `review_id`, `review_version`,
>   `review_integrity_hash` — of which the last three are the reference this section
>   means.
> - `save()` is no longer the only place that resolves. Under the owner's
>   "Yes, check on load" selection, ADR-015 rule 3c has `get()` resolve one level as
>   well. So the mechanism this section proposes borrowing is **stronger** than the
>   sentence above describes, not staler.

**One constraint, so it is not discovered late.** `EvidenceRecord` cannot gain a field
cheaply: its canonical payload is pinned by a literal digest at
`tests/artifacts/test_evidence_hashing.py:18`, and `docs/ROADMAP.md:144-146` records
that this is exactly why ADR-011 declined to widen it for the four disclosures. The
binding must live in `provenance` in a parsed format, or on the REVIEW's `content`.

**A cheaper second strengthening: require the trial count to be disclosed.** ADR-012
rule 10 (`docs/DECISIONS.md:2244-2251`) rules multiple-testing corrections out of
scope *because* "Belay records that nowhere". A rung that must state how many strategy
configurations were tried costs one string, corrects nothing, misleads nobody, and is
the missing input any future correction needs.

---

## 8. Outside literature — two retrieved citations, and what they do not authorize

Belay's documents outrank these; they are offered only as evidence that the gaps named
above are ones the field treats as serious.

- Bailey, Borwein, López de Prado and Zhu, "Pseudo-Mathematics and Financial
  Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance",
  *Notices of the AMS*, May 2014 — https://scholarworks.wmich.edu/math_pubs/40/ —
  whose abstract states that high simulated performance is easily achievable after
  backtesting a relatively small number of alternative configurations, and that "most
  financial analysts and academics rarely report the number of configurations tried
  for a given backtest". That is the same missing input ADR-012 rule 10 names.
- `MinTrackRecord`, PerformanceAnalytics (R) reference —
  https://rdrr.io/cran/PerformanceAnalytics/man/MinTrackRecord.html — which states the
  question it answers as "How long should a track record be in order to have a p-level
  statistical confidence that its Sharpe ratio is above a given threshold?", citing
  Bailey and López de Prado, *The Sharpe Ratio Efficient Frontier*, Journal of Risk
  15(2), Winter 2012/13.

**Neither authorizes a number here.** Both need inputs Belay does not record — a trial
count, a target Sharpe, a confidence level — and `docs/DECISIONS.md:2190-2194` already
refused to default a significance level for that reason. **No minimum track-record
length is proposed in this document.**

---

## 9. Two recommendations, which differ

**This section does not declare a winner.** The author of this research and the
independent reviewer who attacked it reached different answers, and the owner is the
one who rules. Both are set out in full, with the reasoning and the cost of each,
attributed.

### The author recommends: the **producible-grade floor** (option 3)

With section 5's downward rule, and with section 7's binding adopted as Required
Follow-Up rather than as part of the same ruling.

**Reasoning.** Each destination's floor is the grade the previous producing stage is
*defined* to produce. It invents no number, and it makes the ladder's claims and the
evidence's grade the same claim — which is what stops a backtest being filed as a
paper track record.

**The honest status of that "definition", corrected in this revision.** The first
revision said every grade in the recommendation "is derived from a document rather
than chosen". **That is false, and it contradicts this document's own section 2.**
`constitution/Evidence_Standards.md:7-35` names four grades and **no stage**;
`framework/artifacts/enums.py:85-92` names eight stages and **no grade**. What the
mapping actually is: **an inference from name-matching the grade definitions against
the stage names.** "Paper validated" (`constitution/Evidence_Standards.md:17`) reads
onto the stage named `Paper Trading`; "Historical simulation" (`:25`) reads onto what
the `Validation` stage does; "Live validated" (`:9`) reads onto the capital stages.
Three near-misses support the inference and none of them states it:

- `constitution/Promotion_Pipeline.md:7-11` — maturity Level 0, `Idea`, "Research
  only." — the exact phrase `constitution/Evidence_Standards.md:35` uses to define
  Level D.
- `constitution/Promotion_Pipeline.md:31-35` — maturity Level 3, `Paper Trading`, "No
  real capital." — which is what Level B means and does not say Level B.
- `Validation/Workflow.md:11` — `Backtesting` sits inside the validation sequence,
  which is why leaving `Validation` is read as producing Level C.

**All three are on the maturity axis or in a departmental workflow, and
`constitution/Promotion_Pipeline.md:87-95` rules the maturity levels a different axis
from the lifecycle stages.** So the inference is reasonable and it is an inference.
An owner who does not accept it should not adopt this option, because the mapping is
the whole content of it.

**Cost, stated exactly (see §6).** It closes every rung above `Validation` until the
Stage 3 Backtester exists (`docs/ROADMAP.md:240-247`), and keeps `Limited Capital`
and `Production` closed until Stages 6 and 7, which are **unscoped**
(`docs/ROADMAP.md:286`, `:301`). **It closes the door to real money for the
foreseeable future.** Under paper-first that is arguably correct rather than a
defect, and it is still a real cost.

**The author's own counter-argument, stated rather than buried:** rules that are
never exercised rot. ADR-015 makes the same admission about its rules 3 and 5; the
mitigation is the same — write the honest-history tests now, so the suite exercises
the rule even while nothing in production does.

### The independent reviewer recommends: the **hypothesis floor** (option 2)

With section 5's downward rule; with `Remain` split (question 3); with the paper
duration referred to the Investment Committee (question 4); with trial-count
disclosure required (question 5); with section 7's binding as follow-up (question 6);
and ruled as a separate **ADR-016** (question 7).

**Reasoning.** The hypothesis floor closes the actual hole — the Level D purchase of
a real-money rung — and closes nothing else. The producible-grade floor closes the
same hole *and additionally* shuts rungs Belay cannot open for years, on a
stage-to-grade mapping **no document states** and which the section above now admits
is an inference. Two objections compound:

1. **A rule that can never be exercised cannot be tested by use.** The author's
   mitigation is to write the tests anyway, and the reviewer agrees they should be
   written — but a test written against a rule nobody has run is a test of the
   drafter's reading of the rule, which is the failure mode this repository has
   recorded four sessions running.
2. **Sequencing is not an evidence rule.** Whether Belay reaches real money before
   Stage 6 is a roadmap decision, and `docs/ROADMAP.md` is where the author's own
   section 4 says sequencing belongs — the argument used there against option 4
   applies with the same force to the A-grade rows of option 3.

**Cost.** It is weaker. Once the Stage 3 Backtester exists, a single Level C
record — a backtest — could buy `Micro Capital`, `Limited Capital` and `Production`
in turn, with no paper track record required by *this* rule at any point. The
reviewer's answer is that paper-first is enforced by the ladder itself (a strategy
must pass through `Paper Trading` to reach `Promotion Review`, and
`framework/artifacts/validator.py:57-102` admits no skip), that ADR-015's base rule
plus section 7's binding is where forgery cost should be raised, and that the
Investment Committee — `strategies/PromotionCriteria.md:29` — is the body Belay has
already designated for exactly this kind of threshold. An owner who thinks the ladder
alone is too thin a guarantee should prefer the author's option.

### Where they agree

Both recommend **no floor on downward moves** (§5); both reject **criterion coverage**
now, for the same reason — it gates capital on four unbuilt modules, which is a
sequencing decision dressed as an evidence rule; both treat section 7's binding as the
only proposal here that raises the *forgery cost* rather than the paperwork; and
neither proposes a track-record length.

---

## 10. The questions only the owner can answer — asked one at a time

**Read one, answer it, then read the next.** Each says what the thing is, why Belay
needs it, the options, what each option costs, and — where the two recommendations
differ — both of them. Nothing here is decided; the rulings fill ADR-015 rule 4's
table and settle what evidence gates real money.

---

### Question 1 — Which floor?

**What this is.** Belay grades every piece of evidence A, B, C or D. **D means
"hypothesis — research only"**: a typed note, no measurement behind it. Today,
ADR-015 requires a promotion to carry *an* evidence record and says nothing about its
grade, so a D note is enough to move a strategy into `Micro Capital`, the first stage
that spends real money. A "floor" is a rule saying which letter is the minimum for
each destination on the ladder.

**Why Belay needs one.** Without it, the rule that a promotion must carry evidence is
satisfied by writing a sentence about yourself. ADR-015 says this about its own
unfilled table, which is why its ratification is blocked on this question.

**The options and what each costs.**

| | What it says | What it costs |
|---|---|---|
| **A. No floor** | ADR-015's base rule only: evidence must be present and unedited, no grade required | **One Level D note buys real capital.** ADR-015 can be ratified today |
| **B. Hypothesis floor** | From `Paper Trading` upward, a grade above D is required | Closes rungs above `Validation` until the Backtester (Stage 3) exists. After that, one backtest could buy every remaining rung |
| **C. Producible-grade floor** | Each destination requires the grade its previous producing stage is defined to produce: C, then B, then B, then A, then A | Closes the door to real money until a paper-trading engine exists, and the top two rungs until Stages 6-7, **which are unscoped**. Rests on a stage-to-grade mapping no document states |
| **D. Criterion coverage** | Option C plus one record per promotion criterion on the capital rungs | Unmeetable for 4 of the 7 criteria today. A multi-year gate |

**The two recommendations differ here.** The **author recommends C**: it makes the
ladder's claim and the evidence's grade the same claim, and paper-first arguably
*should* close real money until paper trading exists. The **independent reviewer
recommends B**: it closes the actual hole and nothing else, whereas C additionally
shuts rungs Belay cannot open for years on an inference no document states, and a
rule that can never be exercised cannot be tested. Section 9 has both in full.

**Whichever is chosen, the floor applies to upward moves only** — see question 2.

---

### Question 2 — Does the floor apply to moves *down* the ladder?

**What this is.** The ladder runs both ways. A strategy can be demoted — moved down —
or retired, and those are how Belay takes money off the table when something goes
wrong. ADR-015 rule 4's table is keyed by *destination*, and four destinations
(`Paper Trading`, `Promotion Review`, `Micro Capital`, `Limited Capital`) are reached
both by climbing and by falling. So unless the rule says otherwise, a floor ruled for
the climb becomes a floor on the fall as well.

**Why this matters.** A grade floor on a demotion is a **delay on a demotion**. If the
only thing you have at the moment you need to act is a reasoned argument (Level D) and
the rule demands Level C, the strategy stays on capital while somebody produces a
document. ADR-004 rule 4 (`docs/DECISIONS.md:396-400`) already ruled the principle:
requiring promotion-grade proof to *withdraw* a privilege "would make capital
something Belay must prove a strategy no longer deserves."

**The options.**

- **Floor applies upward only.** A demotion or retirement still needs an evidence
  record — the record of the breach that triggered it — at whatever grade that
  observation was made. No minimum. Cost: none identified; the evidence is already in
  hand at the moment of the move.
- **Floor applies in both directions.** Cost: emergency demotions can be blocked by
  the evidence rule, and by §5 point 3 a constitutional retirement reason can become
  unusable.

**Both recommendations agree: upward only.** ADR-015 rule 4 was amended on this
branch to compute direction from `STRATEGY_LADDER` with retirement classified first,
so this is the shape already drafted — it is put to the owner because it is a rule
about capital.

---

### Question 3 — Does *not* moving a strategy need evidence?

**What this is.** A review has four possible outcomes. Three move the strategy
(`Promote`, `Demote`, `Retire`). The fourth, `Remain Current Stage`, leaves it where
it is. ADR-015 requires evidence for the three that move and leaves `Remain`
optional — **and ADR-015 flags that as the drafter's judgement, not an owner ruling,
and leaves it open.** This question closes it.

**Why it is not obvious.** `Remain` is two different events wearing one name
(ADR-008 rule 4). It is the answer when a promotion request is **rejected** — and
putting an evidence bar on *saying no* makes refusing capital harder than granting
it. It is also the answer when a strategy **already sitting on real capital** is
reviewed and kept there — and that is a live decision to keep money deployed, which
`constitution/Evidence_Standards.md:45` ("Every conclusion must reference supporting
evidence") arguably reaches.

**The options.**

- **Optional, as drafted.** Cost: a strategy can sit on `Limited Capital` through
  review after review with no evidence ever recorded for keeping it there.
- **Always required.** Cost: rejecting a promotion needs paperwork, which makes
  saying no more expensive than it should be.
- **Split it: not required when the review rejects a promotion; required when the
  strategy holds real capital.** Cost: two cases where there is now one, so the rule
  and its tests get longer.

**The recommendations differ.** The **author's document left this unasked** — that
omission was one of the 17 defects. The **independent reviewer recommends the
split**: no evidence for a rejected promotion, evidence for holding a strategy that
sits on real capital.

---

### Question 4 — How much paper trading is enough?

**What this is.** Paper trading means Belay runs the strategy against live prices with
fake money and records what happens. Evidence from it is graded B. **One week and two
years are both "Level B".** A grade says what *kind* of observation it is, never how
much of it there was.

**Why Belay needs an answer.** If any option above puts Level B on the rung into
`Micro Capital`, a one-day paper run satisfies it. **No Belay document gives a
number** — section 2 point 2 records the sweep that found none.

**The options.**

- **Set a number now.** Cost: it would be invented. Section 8 shows the two outside
  sources that speak to track-record length both require inputs Belay does not
  record, and `docs/DECISIONS.md:2190-2194` already refused to default a statistical
  parameter for exactly that reason.
- **Refer it to the Investment Committee.** Cost: the bar is incomplete until the
  Committee answers. `strategies/PromotionCriteria.md:29` already sends promotion
  thresholds there — "Promotion thresholds are determined by the Investment
  Committee" — so this is the existing route, not a new one.
- **Leave it at "at least one record".** Cost: accept that a one-day paper run
  qualifies for a real-money promotion.

**The reviewer recommends referring it to the Investment Committee**, on the
precedent above. The author's document offered all three without choosing.

---

### Question 5 — Must a promotion state how many strategy variants were tried?

**What this is.** If Belay tries fifty variations of a strategy and keeps the best
one, the best one looks good partly by luck. Statisticians correct for this; the
correction needs one input — **how many were tried**. ADR-012 rule 10
(`docs/DECISIONS.md:2244-2251`) rules those corrections out of scope *because* "Belay
records that nowhere", and `framework/metrics/statistics.py:61-62` ships that
admission inside every significance report it produces.

**Why it is cheap.** Requiring the count is one string on the record. It **corrects
nothing and claims nothing** — that is the point. It records the input that any
future correction would need, and today it simply tells a reader how much salt to
take the number with.

**The options.**

- **Require it.** Cost: one field to fill, and one more thing a promotion can be
  refused for leaving blank.
- **Do not.** Cost: the input stays unrecorded, and ADR-012 rule 10 stays true
  forever by construction.

**The reviewer recommends requiring it.** The author listed it without a
recommendation.

*(A question about requiring out-of-sample testing appeared in the first revision and
is not in this list. It is recorded here rather than dropped: out-of-sample testing
appears in no Belay document at all, so requiring it would be the owner inventing a
validation method rather than ruling on evidence, and the reviewer judged
trial-count disclosure the better-founded of the two because ADR-012 rule 10 is a
live Belay ruling that names the missing input. It remains available to propose.)*

---

### Question 6 — Must an evidence record point at a stored report?

**What this is.** Today an evidence record says "Level C" and gives a free-text note
about where it came from. Nothing checks that note. The proposal in section 7 is that
the record must **name a signed report that is actually on disk, by identifier,
version and hash** — so "Level C" means "here is the backtest report, and here is
proof it has not been edited".

**Why it matters.** Every floor in question 1 buys **declaration discipline, not
truth**: the grade is a letter the author types. This is the only proposal here that
raises the *cost of forging*, and it is also the only mechanism that could make a
"the record must carry the survivorship caveat" rule checkable rather than decorative
(section 4).

**The options.**

- **Rule it now, as part of the same ruling.** Cost: a larger ruling, and ADR-015's
  implementation grows before it is ratified.
- **Rule the grade now and make the binding Required Follow-Up.** Cost: until it
  lands, a grade is an assertion.
- **Do not require it.** Cost: the forgery ceiling stays where section 6 describes it.

**Both recommendations say follow-up**, not part of this ruling.

---

### Question 7 — Rule this inside ADR-015, or as a new ADR-016?

**What this is.** Purely about where the text lives. ADR-015 is the ladder ruling and
has a marked empty table waiting for this answer. The alternative is a separate
decision record that fills that table from outside.

**The options.**

- **Inside ADR-015.** Cost: one ratification, and amending the bar later means
  re-opening the ladder rules with it.
- **Separate ADR-016.** Cost: two documents to keep consistent; the benefit is that
  the bar can be raised or lowered later without touching the rules about how the
  ladder works. Either way the table in ADR-015 rule 4 stays the interface.

**The reviewer recommends ADR-016.** The author listed both without choosing.
ADR-015 explicitly does not answer this and says it is not the drafter's to answer.

---

## Appendix A — what could not be checked

- **ADR-015 is on a branch, not `main`.** Its rules are described, never cited by
  path:line; if the branch is amended before ratification, §7's descriptions may go
  stale. **Editor's note:** §7 was re-checked against revision `d734bcb` when this
  document was committed to that branch, and carries the result inline. Nothing else
  in this document describes ADR-015's machinery in enough detail to go stale.
- **Nothing in Belay calls `save()` for a STRATEGY or a REVIEW today**, so no bar here
  has ever been exercised against a real record. §3's claims about what is producible
  are read from the roadmap and the code, not observed in use.
- **`docs/OwnerDecisions.md` and `docs/HANDOFF.md` changed on disk during the
  original session**, so neither is cited by line.
- **This document has had one independent pass, not two.** Every ADR that had a
  second reader lost claims to it.

---

## Appendix B — the 17 defects the independent pass found, and what changed

Recorded so the revision is auditable rather than asserted (Law VII,
`constitution/Immutable_Laws.md:49-51`). All 17 were verified against this branch
before being applied; none was found to be wrong.

**Blockers (4).**

1. **Candidate tables keyed by `(from → to)`, ADR-015 rule 4's table keyed by
   `to_stage` alone.** Four destinations are both a climb and a demotion destination
   (`framework/artifacts/validator.py:57-102`), so a ruled climb floor would have
   gated emergency demotions, against ADR-004 rule 4
   (`docs/DECISIONS.md:396-400`). **Fixed in both documents:** every table in §4 is
   re-keyed by destination, §4 carries an explicit upward-only direction clause
   computed from `STRATEGY_LADDER` with retirement classified first, and ADR-015 rule
   4's consumption rule was amended to say the same. **ADR-015's table is still
   empty**, and two implied tests were added to its "Tests this implies".
2. **§9 claimed every grade "is derived from a document rather than chosen".** False,
   and it contradicted §2. §9 now says the mapping is an inference from name-matching,
   states that no document makes it, and cites the three near-misses
   (`constitution/Promotion_Pipeline.md:7-11`, `:31-35`, `Validation/Workflow.md:11`)
   with the caveat that all three are on the maturity axis or in a departmental
   workflow.
3. **§6 and §9 understated what the recommendation closes.** Now stated exactly in §6,
   §9 and question 1: it closes every rung above `Validation` until Stage 3
   (`docs/ROADMAP.md:240-247`), and the two rungs above `Micro Capital` need Level A,
   which depends on Stages 6-7 — unscoped (`docs/ROADMAP.md:286`, `:301`).
4. **§10 Q1 omitted the status quo.** "No floor" is now option A in question 1, with
   ADR-015's own statement of its cost: one Level D record satisfies a promotion into
   real capital.

**Should-fix (5).**

5. **§5 point 3 overstated the retirement claim** ("may only ever be" Level D). A
   structural change observed with real capital is A, in paper B; a falsified
   assumption is C. Reworded to the worst case, with the correction marked. The
   conclusion survives on points 1 and 2.
6. **§4's one-line principle failed where the origin stage produces nothing** —
   `Idea`, and `Promotion Review`, which is a decision stage yet sits on the rung that
   releases real money. The exception is now stated: the floor is carried forward from
   the last stage that produces evidence, and §4 says that this is a second inference
   carrying the table's most consequential cell.
7. **"Must carry" and "Min. count" had no mechanism** under ADR-015 rule 4's
   consumption — a lookup and a `>=` on `strongest_evidence_level`
   (`framework/artifacts/enums.py:29-43`), which sees neither counts nor subject
   matter. Both columns dropped, the content kept as prose, and the choice put to the
   owner as question 6.
8. **ADR-015's open item on `Remain Current Stage` was never put to the owner.** Now
   question 3.
9. **§6 never said that a real-money promotion needs none of the seven canonical
   promotion criteria** (`constitution/Promotion_Pipeline.md:75-81`, canonical per
   `:101-105`). Now stated in §6 before the costs.
10. **`scripts/status.py:19-27` was wrong** — `PROMOTION_CRITERIA` is at
    `scripts/status.py:48-55`. Verified and fixed.
11. **`framework/artifacts/enums.py:85-93` was wrong** — the eight stages are `:85-92`;
    `:93` is `RETIRED`, which is not a stage. Fixed in §1 and §9.
12. **`Validation/Workflow.md:11-19` was a slice** — the full sequence is `:3-27`.
    Verified and fixed.

*(Items 10-12 were filed as should-fix by the reviewer; they are citation defects.)*

**Nits (5).**

13. **`framework/data/survivorship.py:114-126`** — the `basis` refusal is `:122-127`.
    Verified and fixed.
14. **"appear nowhere in Belay"** → "appear in no Belay document";
    `framework/metrics/statistics.py:61-62` ships a disclosure string naming
    multiple-testing. Verified and fixed.
15. **§2 point 1 did not name its nearest miss** — `strategies/Registry.md:27-29`,
    `Evidence Level D` on the stub record below `Current Stage Hypothesis`
    (`:19-21`). Added, with why it establishes no rule: it is an illustrative stub,
    and `Hypothesis` is a *maturity* level (`constitution/Promotion_Pipeline.md:15-19`)
    on the other axis (`:87-95`), not a lifecycle stage.
16. **One row read "NUMBER NOT RULED (≥1)"** while others read "NUMBER NOT RULED".
    All rows now read identically; `≥1` is an option in question 1, not a ruled
    number.
17. **Candidates A/B/C collided with evidence Levels A/B/C/D.** Renamed throughout to
    "No floor", "Hypothesis floor", "Producible-grade floor" and "Criterion
    coverage". ADR-015 names no candidate by letter, so only its count of them needed
    updating.

**And the dissent, recorded and not resolved.** The reviewer's recommendation differs
from the author's — §9 now carries both side by side with attribution, reasoning and
cost, and declares no winner.
