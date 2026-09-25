# PROPOSAL — What "Enough Data" Means: A Definition Of Sample Adequacy For F-004

**Status: PROPOSAL awaiting owner ruling. Dated 2026-09-19, revised 2026-09-19 after an independent pass (15 defects, 5 blockers), revised again after Issue #6 (second independent falsification pass).** Nothing here is doctrine and no code changes with it. Every figure is **NUMBER NOT RULED**. The appendices record what changed and why, per Immutable Law VII (`constitution/Immutable_Laws.md:49-51`, "Institutional knowledge shall never be intentionally discarded").

Requested by the owner's F-004 ruling of 2026-09-19, recorded here as selections and nothing more:

> **F-004 → "b now"** — define adequacy against something independent of the observed effect.
> **Shape → "aligned"** with the recommendation: **adequacy = a minimum number of observations AND a minimum time span, both required, neither depending on the observed effect.**
> **Regime coverage → deferred**, because Belay cannot measure regimes yet, and recorded as an open gap.
> **The numbers** are to be proposed by research with real citations, attacked by an independent reviewer, and ruled by the owner next session, together with the evidence bar.

Later the same day the owner made further selections in chat, **now recorded at `docs/OwnerDecisions.md:1464` (Part 10f) and `:1487` (Part 10g)** [*repointed by the committer of `records/2026-09-19-rulings`, 2026-09-19 — the text below still describes these as chat selections because that is what they were when this document was first drafted; the record referenced no longer needs to be "pending"*]: **(i)** F-006's narrow fix is **authorised** — every coverage statement carries its observation count beside the span — to be built at step 4 of the Part 9a blocker order; **(ii)** a trading-calendar **proposal** is to be written first, no code and no library chosen; **(iii)** once a calendar exists, an **unexplained gap fails closed** — the fetch is refused, not stored with a warning — while a gap explained by the calendar or by a recorded reason such as a halt is allowed and disclosed. Section 10's question 4 is rewritten around (iii).

**This document has now had two independent adversarial passes.** The first found 5 blockers and 10 lesser defects; all 15 were checked against source by this author and all 15 were applied (Appendix B). **Issue #6 is the second pass**; its dispositions are Appendix C. Read section 8 as a proposal whose Candidate 2H recommendation is **unresolved pending the flat-count / frequency ruling**, not as settled doctrine.

**Citation caveat, updated by the committer.** All `docs/HANDOFF.md` and `docs/OwnerDecisions.md` line numbers below were valid at `origin/main` **3080848** when first drafted. **Re-verified and repointed by content, 2026-09-19 (evening), by the committer of `records/2026-09-19-rulings`, against that branch** — the register commit anticipated above has since landed (PR #9 as `2f44c19`, PR #11 as `3080848` onto `main`), and `docs/HANDOFF.md` and `docs/OwnerDecisions.md` moved further still on this branch and in this pull request. Every citation below reflects `records/2026-09-19-rulings` as of this pull request, not `origin/main` at the date above.

**The regime deferral is verified, not assumed.** `framework/services/regime.py:1-10` is a ten-line placeholder whose `run()` prints `"Analyzing market regime..."`; `docs/ROADMAP.md:75-81` states `Regime robustness` is blocked on regime classification and on returns segmented by regime.

---

## Why this exists, in plain words

`sample_adequate` is a true/false flag on every statistical review Belay produces. It is meant to answer a question the p-value cannot: **"is there enough data here to conclude anything at all?"** — because "we tested it and found nothing" and "we could not test it" are different answers, and only one of them means the strategy failed.

Today the flag is computed from the same arithmetic as `significant`, so it can never disagree with it. It answers no second question. This proposes what the second question should be.

---

## 1. What the code does today, and why the flag is empty

`minimum_observations_for_significance` searches for the smallest `n` at which **the observed effect** would clear the critical value: `clears(n)` is `effect * sqrt(n) >= t_critical_value(alpha, n - 1)` (`framework/metrics/statistics.py:228-229`). That predicate **is** the significance test and is monotone in `n`, so `n >= needed` is the same proposition as `p < alpha`, and `sample_adequate` (`:303`) is `significant` (`:301`) written twice. `docs/HANDOFF.md:3563-3567` records 60 random trials producing 0 mismatches.

The test that should have caught it asserts the opposite: `tests/metrics/test_significance.py:226-239` asserts only the one-way implication and concedes the mechanism in its own docstring; `docs/HANDOFF.md:1141-1143` repeats the concession as though it were a design choice.

ADR-012 rule 8 is the rule being defeated (`docs/DECISIONS.md:2231-2238`): "**A sample below that number has not failed the test — it has not taken it**, and reporting those two states identically is the failure this rule exists to prevent." The ADR's own Still-Open section already names the hole (`docs/DECISIONS.md:2382-2386`): "**What minimum sample Belay requires.** ... No document says how many Belay *demands* before a strategy may be promoted."

---

## 2. What "observations" and "span" mean for Belay's data

**An observation is one element of the return series the test is run on**, not one row of market data. Belay's unit is a `DailyBar` (`framework/data/contract.py:73-89`) inside a `DailyBarSeries` whose bars are validated strictly increasing (`:107-112`). A daily strategy's observations are daily returns; a monthly strategy's are monthly. **A count floor stated in bars is therefore not frequency-neutral** — section 6 treats that as a defect of the simplest candidate rather than hiding it.

**A span is `period()`, first bar to last bar** (`framework/data/contract.py:114-127`). That is F-006 (`docs/HANDOFF.md:3590-3619`): two bars three years apart disclose three years.

**For a dense daily series, a count floor and a span floor are one constraint, not two.** 756 observations *is* three years at 252 trading days a year. The count only bites independently at non-daily frequency, or on a series with holes. That is not an argument against stating both — it is the reason the pair alone does not do the work people assume it does.

**Interaction with F-006.** F-006's narrow fix — record observation count beside span, now **authorised** (`docs/OwnerDecisions.md:1464`, Part 10f) and confirmed by `docs/OwnerDecisions.md:926-932` as not blocked on a trading calendar — makes the two numbers *visible together*. This proposal makes them *jointly binding*. Complementary: F-006 stops a disclosure lying about coverage; this stops a review calling a thin record adequate.

**The pair does not close the sparse case.** 760 observations spread over 20 years satisfies "756 observations AND 3 years" while covering **10.4%** of the calendar days in its own window (760 / (20 × 365.25); on a trading-day basis, 15.1%). A dense daily series sits at 252/365.25 = **0.690** on the calendar-day measure. Whether a third condition should catch this is **the owner's reserved question**, not research's — see section 10, question 4, which is rewritten around the owner's "fails closed" selection.

---

## 3. What Belay's documents say about how much data — and where they stop

They demand evidence and never quantify it.

- `constitution/Promotion_Pipeline.md:27` — maturity Level 2, `Validated`, **is** "Passed statistical review." `:75-81` lists the seven promotion criteria, first `Statistical performance`.
- `constitution/Capital_Authority.md:11-14` — "Capital shall be determined using: ... `Statistical edge`." The conclusion sizes positions.
- `constitution/Immutable_Laws.md:29-33` — Law IV, "Past performance is evidence. It is never proof."
- `Validation/Backtesting.md:13-31` — nine minimum metrics, of which `Trade Count` (`:27`) is the only count of anything; `:35-43` requires a documented `Sample Period`; `:47-49`, "Outputs become evidence. Not guarantees."
- `Validation/Workflow.md:15` — `Statistical Review` is its own step. `Validation/Critic.md:23` — "Could randomness explain the result?"; `:17` — "What market regimes break this?", the deferred half of this ruling.
- `Validation/CapitalReview.md:13-25` — promotion considers `Evidence quality` first and `Paper performance` last. Neither is given a length.
- `strategies/PromotionCriteria.md:7` heads its categories with `Statistical Performance`; `:29` refers promotion thresholds to the Investment Committee; `:46-50` records the 0-100 Promotion Score as **suspended, not adopted**, for want of weights and a threshold.

**Nothing states a minimum count, span, or track-record length.** The only in-repo figure of that shape is operational: `docs/HANDOFF.md:171` records three years of AAPL as 754 daily bars.

**Two precedents govern how a number may enter here.** ADR-012 rule 3 (`docs/DECISIONS.md:2190-2194`) refuses to default alpha because no Belay document states one. ADR-012 **rule 2** (`docs/DECISIONS.md:2184-2188`) refuses to default the null: `null_return` "is a required argument with no default. Testing against zero is the conventional choice and it is still a choice." **Both bind this proposal** — see the treatment of the reference Sharpe `c` in section 5.

---

## 4. Outside literature, retrieved this session

Belay's documents outrank these. Offered for their formulas and as evidence the field takes these quantities seriously — never as authority.

1. **Harvey, Liu and Zhu, ". . . and the Cross-Section of Expected Returns", NBER Working Paper 20592, October 2014** — https://www.nber.org/papers/w20592 — abstract: "The estimation of our model suggests that a newly discovered factor needs to clear a much higher hurdle, with a t-ratio greater than 3.0," and "We argue that most claimed research findings in financial economics are likely false." **Relevance: the hurdle, not the sample.** A t-hurdle of 3.0 rather than 1.96 multiplies every sample requirement by (3.0/1.96)² ≈ 2.343.
2. **Bailey and López de Prado, "The Sharpe Ratio Efficient Frontier", Journal of Risk 15(2), 2012** — Minimum Track Record Length. Formula as rendered by Portfolio Optimizer, https://portfoliooptimizer.io/blog/the-probabilistic-sharpe-ratio-bias-adjustment-confidence-intervals-hypothesis-testing-and-minimum-track-record-length/ : `MinTRL(c) = (1 − κ·SR + (γ−1)·SR²/4) · (z₁₋α / (SR − c))²`, κ skewness, γ kurtosis, SR the Sharpe ratio, c the reference threshold, z the normal critical value; its worked example needs 184 monthly observations against 136 available. The R reference, https://rdrr.io/cran/PerformanceAnalytics/man/MinTrackRecord.html , states the question as "How long should a track record be in order to have a p-level statistical confidence that its Sharpe ratio is above a given threshold?", cites the same paper, and documents its `refSR` argument as needing to be "in the same periodicity as the returns (non-annualized)" — which is why section 5 writes the conversion down. **Relevance: this is the sample-size formula, and its only strategy-specific inputs are a Sharpe ratio and a reference — both of which can be declared rather than observed.**
3. **NBER, US Business Cycle Expansions and Contractions** — https://www.nber.org/research/data/us-business-cycle-expansions-and-contractions — average contraction 10.3 months and average expansion 64.2 months over 1945-2020 (17.0 and 41.4 over 1854-2020), and the full table of peak and trough dates. **Relevance: the span argument — and, recomputed, the refutation of the obvious version of it.** See section 5.
4. **Against the n ≥ 30 convention** — Yangzhuoran Fin Yang, "30 isn't a reliable cutoff for a 'large' sample", https://yangzhuoranyang.com/posts/n30/ — "It could be 30, it could be 3000", arguing 30 describes when the t-distribution resembles the normal, not a Central Limit Theorem guarantee. **Relevance: the cheap answer — "require n ≥ 30" — has no defensible grounding.**

**What none of them authorizes.** Each needs an input Belay does not hold or has not declared: a trial count, a target Sharpe, a reference, a regime classifier.

---

## 5. The arithmetic, stated so it can be checked

### 5a. The span: an average is not a containment, and the first draft confused them

**The first draft of this document claimed three years "reliably contains more than one average post-war contraction." That is false and is withdrawn.** An average duration of 10.3 months says nothing about how often a window of a given length overlaps one.

Recomputed this session from NBER's post-1945 peak/trough dates, over every rolling window in Nov 1945 – Apr 2020 (894 months):

| Window | Windows | Containing ≥1 recession month | Share |
|---|---|---|---|
| 1 year | 883 | 245 | **27.7%** |
| 3 years | 859 | 475 | **55.3%** |
| 5 years | 835 | 611 | **73.2%** |
| 6.17 years (74 months) | 821 | 667 | **81.2%** |
| 10 years | 775 | 765 | **98.7%** |

**Provenance of these percentages (Issue #6).** The original research pass reported that it **recomputed** them from NBER's published peak/trough table (link in §4). **No frozen copy of that table lives in this repository**, so Issue #6 did **not** independently reproduce the rolling-window shares from repository-contained evidence alone. They remain **externally sourced / UNVERIFIED as repository-reproducible**, not false. The qualitative claim they support — that a span floor is a *probabilistic* guard, not a structural one — does not depend on any one cell.

**The longest recession-free stretch is 128 months — July 2009 through February 2020**, which is ten and a half years containing no contraction month at all. So **no span short of eleven years guarantees regime variety**, and a span floor is a *probabilistic* guard, not a structural one.

**Consequence: the span floor is a JUDGEMENT CALL, not a derivation.** It is the owner's to make, on the percentages above (with the provenance caveat). This document recommends one and labels it as judgement.

### 5b. The count: the conversion, and the reference that may not be defaulted

MinTRL takes a **per-period** Sharpe, not an annual one. The conversion, written down because `framework/metrics/statistics.py:84-95` exists precisely to stop a silent factor-of-252 error:

> `SR_period = SR_annual / sqrt(periods_per_year)` — ÷√252 for daily, ÷√12 for monthly. `c` converts the same way.

**`c` may not be silently zero.** ADR-012 rule 2 (`docs/DECISIONS.md:2184-2188`) makes `null_return` a required argument with no default, on the reasoning that "a strategy that beats zero but not the risk-free rate has no edge worth capital." Setting `c = 0` inside an adequacy rule re-introduces exactly the default that rule forbids. **Proposed: `c` is the caller's own `null_return`, converted to a per-period Sharpe by the same division — one value, two uses, so the significance test and the adequacy floor cannot disagree about what "no edge" means.** The tables below print `c = 0` only because that is the null the illustration uses, and it is labelled, not assumed.

### 5c. The table, at c = 0, κ = 0, γ = 3, ceilings applied

| Declared target Sharpe (annual) | z = 1.645 | z = 1.96 (two-sided 5%) | t = 3.0 (Harvey-Liu-Zhu) |
|---|---|---|---|
| 0.50 | 2,730 bars / 10.83 yr | 3,875 / **15.38 yr** | 9,077 / 36.02 yr |
| 0.75 | 1,214 / 4.82 yr | 1,723 / **6.84 yr** | 4,037 / 16.02 yr |
| 1.00 | 684 / 2.71 yr | 971 / **3.85 yr** | 2,273 / 9.02 yr |
| 1.50 | 305 / 1.21 yr | 433 / **1.72 yr** | 1,013 / 4.02 yr |
| 2.00 | 172 / 0.68 yr | 244 / **0.97 yr** | 572 / 2.27 yr |

**The requirement is quadratic in the target**: halving the ambition quadruples the data. **Non-normality barely matters at daily frequency**: at target 1.0 and z = 1.96, moving from (κ=0, γ=3) to (κ=−0.5, γ=6) takes 971 bars to 1,004 — +3.44%, because the per-day Sharpe is tiny. At monthly frequency it matters far more.

### 5d. The finding that decides question 2: MinTRL under Candidate 2 is not MinTRL under Candidate 2H

Against a 756-observation flat floor, the declared target at which MinTRL falls below it **for a daily series**:

| Hurdle | Crossover declared target |
|---|---|
| z = 1.645 | **0.951** |
| z = 1.96 | **1.133** |
| t = 3.0 | **1.737** |

**Under unrestricted Candidate 2** (MinTRL alone, no flat `max`): any declared target above the daily crossover makes the MinTRL count smaller than 756, so for a **daily** series Candidate 2 collapses into Candidate 1's count. **At monthly frequency, Candidate 2 is frequency-adaptive.** Independently recomputed (`z = 1.96`, `κ = 0`, `γ = 3`, `c = 0`): target 1.0 → **49 observations ≈ 4.08 years**; target 0.75 → 84 ≈ 7.00 years; target 0.5 → **187 ≈ 15.58 years**. Those monthly figures are what Candidate 2 *would* require.

**Under Candidate 2H** (`N_MIN = max(756, ceil(MinTRL(...)))` with a **universal** flat floor of 756 **observations**): those monthly MinTRL results are **overridden**. Independently recomputed:

```text
max(756, 49)  = 756 monthly observations = 63.00 years
max(756, 187) = 756 monthly observations = 63.00 years
```

For ordinary declared targets, **Candidate 2H therefore inherits Candidate 1's frequency problem** — a monthly strategy still needs 756 monthly bars (63 years) or a waiver — even though unrestricted Candidate 2 would have given 49 or 187. **The hard floor and frequency adaptation are in tension.** That tension is owner question 2 / question 3 material; it is not resolved by preferring 2H on gaming grounds alone.

### 5e. What the formula is actually computing, said precisely

Substituting a **declared** target for the observed Sharpe turns MinTRL into an *a-priori power calculation*: **"if the realised Sharpe, skewness and kurtosis land exactly on the declared values, how many observations would distinguish them from `c` at 1−α?"** That is independent of the observed effect — which is what the ruling demands — but `N` is a function of a **chosen** target. It is not "derived" in the sense of being read off a document; it is derived *conditional on a choice*. Every reading of the tables above carries that conditional.

### 5f. Cost in calendar time

A three-year daily backtest series is ~754 bars and, per `docs/HANDOFF.md:171`, fetching one took 4.4 seconds. A three-year **paper** track record takes three years. **Any bar set here is nearly free on the backtest side of the ladder and expensive on the paper side** — the two are different quantities, and section 7 stops conflating them.

### 5g. When the proposed formula does not yield a valid minimum

The MinTRL-style expression proposed here is

`N = (1 − κ·SR + (γ−1)·SR²/4) · (z₁₋α / (SR − c))²`

with `SR` and `c` in **per-period** units. It does **not** produce an honest finite sample requirement when:

1. **`SR == c`** — the denominator is zero; the expression is undefined.
2. **The leading factor is non-positive** — `1 − κ·SR + (γ−1)·SR²/4 ≤ 0` (possible under extreme declared skew/kurtosis relative to `SR`). A non-positive leading factor does not mean "zero observations suffice"; it means the formula has left the domain in which it answers the sample-size question.

**Such cases must not silently become 0, 756, 1_000_000, or any other fabricated integer.** Belay's existing significance path refuses rather than invents when no sample size can establish an effect (`framework/metrics/statistics.py:222-226`, mean indistinguishable from the null; `:231-236`, effect too small to clear within `_MAX_OBSERVATIONS`). That is the nearest precedent for **refusal**. Whether an adequacy rule under this proposal should refuse the review, refuse only the MinTRL branch and fall back to a flat floor, or take another path is **unresolved** — an owner/implementation question, not something this document invents. Until ruled: **inputs in this domain do not yield a valid computed `N_MIN` under the proposed formula.**

---

## 6. Four candidate definitions

All four leave `minimum_observations_for_significance` in place as a reported number and replace only the boolean.

### Candidate 1 — Flat floor

`sample_adequate = (observations >= N_MIN) and (span >= S_MIN)`, both constants fixed for all strategies. Proposed: **N_MIN = 756 observations, S_MIN = 3 calendar years. NUMBERS NOT RULED, and the span is a judgement call (5a).** For a dense daily series these are the same constraint stated twice (756 = 3 × 252); the count exists to bite at other frequencies and on sparse series.

- **Protects against:** the short-sample false positive, which is the whole of rule 8.
- **Costs:** three years of history — seconds for a backtest, three wall-clock years for paper. Buys a 55.3% chance the window contains a recession month.
- **Fails:** not frequency-neutral. A monthly strategy would need 756 monthly returns (63 years), or a waiver, and a waiver is a hole. It ignores how hard the claimed edge is to detect.
- **Gamed by:** running at the highest frequency that satisfies the count. Resample a monthly signal to daily and the count arrives 63 times sooner — though the span floor still binds.

### Candidate 2 — Declared-target floor

`N_MIN = ceil(MinTRL(declared target, alpha, declared skew, declared kurtosis, c = the caller's null))` at the series' own frequency; `S_MIN` fixed at **3 calendar years. NUMBERS NOT RULED.** The target is **pre-declared**, recorded before the test and inside the artifact's integrity hash. Inputs outside the formula's domain (§5g) do not yield a valid computed minimum.

- **Protects against:** everything Candidate 1 does, plus the frequency hole — MinTRL converts the target to the series' own periodicity, so a monthly strategy gets a monthly answer (target 1.0 → 49 observations ≈ 4.08 years under the illustration in 5d).
- **Costs:** one new required input per strategy, and a modest ambition makes the bar enormous (monthly target 0.5 → 15.6 years).
- **Fails, and this is decisive for daily series:** **for daily series it is largely inert.** Above a declared target of 1.133 (z = 1.96) the MinTRL count sits below 756 and a separate flat floor would govern anyway (5d). The extra machinery buys almost nothing at Belay's actual data frequency **unless** it is left unrestricted (no `max` with 756).
- **Gamed by:** declaring a high target to shrink the count. The first draft claimed the mitigation was that the strategy "must then be judged against 2.0" — **that mitigation does not exist anywhere in Belay, no test asserts it, and the integrity hash proves only that the declaration was not edited.** The claim is withdrawn.

### Candidate 2H — Declared target as a *raise only* (the reviewer's variant)

Candidate 2 with one added rule: **`N_MIN = max(flat_count, ceil(MinTRL(...)))`.** A declared target may only **raise** the requirement, never lower it below the flat count. Proposed illustration still uses **`flat_count = 756 observations`** (NUMBER NOT RULED) — the same universal observation count as Candidate 1, **not** a frequency-normalised equivalent of three years.

- **Protects against:** the gaming route in Candidate 2, structurally rather than by promise. Declaring a high target buys nothing below the flat floor.
- **Costs:** the same as Candidate 1 for daily series, plus one declared input; it is strictly stricter than both 1 and 2 **where MinTRL exceeds the flat count**.
- **Fails — and Issue #6 makes this the decisive failure:** with a universal flat floor of 756 **observations**, Candidate 2H is **not frequency-neutral**. The monthly MinTRL figures that unrestricted Candidate 2 would give (49 / 187 at targets 1.0 / 0.5) become `max(756, ·) = 756` monthly bars = **63 years** (5d). Frequency adaptation and the hard floor are in tension; choosing 2H with this flat count re-opens Candidate 1's monthly hole while closing the gaming route. It also makes a cautious declaration expensive while making an ambitious one free of consequence below the flat floor. It is a floor, not an incentive. **No frequency-normalised substitute (e.g. 36 monthly bars) is invented here** — that would be a threshold ruling.

### Candidate 3 — Cycle floor (most conservative)

Candidate 2H with `S_MIN` = **74 months ≈ 6.17 years (NUMBER NOT RULED)**.

- **Protects against:** a record measured entirely inside one expansion — the commonest way a strategy looks good and is not. Raises containment from 55.3% to **81.2%**.
- **Costs:** closes paper promotion for six years; in practice a decision not to promote on paper evidence this decade.
- **Fails:** 81.2% is not coverage. The July 2009 – February 2020 stretch is 128 recession-free months, so even 6.17 years can be entirely inside one expansion.
- **Gamed by:** choosing a start date. Nothing in Belay pins the window.

### Candidate 4 — Drop the boolean (excluded by the ruling, recorded)

The other half of F-004's option set (`docs/HANDOFF.md:3571-3573`): report `minimum_observations` and the span, and let a human judge. The owner selected "b now", so this is not live. Recorded because it is the cheapest correct answer and a reviewer attacking this document should weigh it: a flag nobody can define well is worse than two honest numbers.

### Does a pre-declared target satisfy the ruling? — flagged, not decided

The ruling is that adequacy must not depend on **the observed effect**. Candidates 2 and 2H depend on a **declared** effect — fixed before the data and unmoved when the data moves, so `sample_adequate` can no longer be a restatement of `significant`. Mechanically the ruling is satisfied, and the test in section 9 proves it by construction. **But a stricter reading is available**: the owner may have meant "adequacy must not depend on anything the strategy's author controls", under which only Candidate 1 or 3 qualifies. That is owner question 2.

---

## 7. Two different quantities, and how they interlock with the evidence bar

**Backtest sample adequacy and a paper-trading track record are not the same question.** Adequacy on a historical series costs a fetch — seconds (`docs/HANDOFF.md:171`). Adequacy on a paper track record costs wall-clock years, because the observations do not exist until time passes. A number that is trivial for the first is a multi-year gate on the second.

`docs/proposals/evidence-bar-per-rung.md` on **public PR #7 / `adr/015-stage-is-carried`** asks the paper-trading version as its **Question 4** ("How much paper trading is enough?"), records that **no Belay document gives a number**, and states that **its independent reviewer recommends referring the number to the Investment Committee**, on the existing precedent of `strategies/PromotionCriteria.md:29` ("Promotion thresholds are determined by the Investment Committee"). That recommendation exists and the owner should see it. [Historical Atlas archive referred to an earlier carrier as draft PR #10 and revision `8e3edb2`; those IDs are intentionally preserved for provenance and do not resolve as live public Belay locators.]

Two coherent arrangements, presented neutrally as question 7:

- **One ruling serves both.** This document's definition is the quantity; the evidence bar cites it per rung rather than naming a second number. Buys one answer to "how much data is enough" and no drift.
- **Rule them separately.** Backtest adequacy is ruled here; the paper-trading length goes to the Investment Committee. Buys a right-sized answer for each, at the cost of two places where "enough" is defined.

---

## 8. Recommendation, with the uncertainty it deserves — and the dissent

**Prior text recommended Candidate 2H.** Issue #6 showed that recommendation rested on false arithmetic: the monthly MinTRL figures used to justify allowing a declared target **do not apply under 2H** when `flat_count = 756` observations (5d). **Preserving that recommendation would preserve the error.**

**Author recommendation after Issue #6: unresolved pending the flat-count / frequency ruling.** The gaming reason to prefer a raise-only hard floor remains real. The frequency cost of pairing that hard floor with a universal 756-observation count is also real. Choosing among unrestricted Candidate 2, Candidate 2H with this flat count, Candidate 1 alone, or a later frequency-normalised floor (not invented here) is for the owner at questions 2 and 3 — not for this author to paper over.

**Stated with the uncertainty it deserves.** The count floor under Candidates 2 / 2H is *conditional on a chosen target* (5e), not derived from a document. The span floor is a judgement on the percentages in 5a (externally sourced; not repository-reproducible — see 5a's provenance note): three years buys a reported 55.3% chance of containing a recession month, and no achievable span buys certainty. And for daily series — Belay's only data today — 2H and Candidate 1 are the same rule on the count side (5d), so the declared target is machinery that, under 2H with flat 756, also fails to deliver the monthly adaptation the earlier text advertised.

**Where this author and the independent reviewer differ, both are shown rather than resolved.** Issue #6 does not invent agreement where the arithmetic broke:

| Question | This author (after Issue #6) | Independent reviewer (first pass) |
|---|---|---|
| Q1 span | 3 years, labelled judgement | **Agrees** — 3 years, but only if the owner is shown 55.3 / 73.2 / 81.2% and chooses on them (percentages externally sourced; see 5a) |
| Q2 declared target | **Unresolved** — unrestricted Candidate 2 keeps monthly MinTRL (and can be gamed); 2H with flat 756 blocks gaming and re-opens the monthly frequency hole (5d). No frequency-normalised floor invented here | First pass agreed conditionally with 2H; that agreement assumed the monthly MinTRL story still applied under 2H — which Issue #6 showed it does not |
| Q3 flat count | 756 still the daily illustration; owner must hear that under 2H it is also a 63-year monthly floor | First pass agreed on 756 for daily — provided the owner is told 756 is the span floor restated for daily data, not a second guard |
| Q4 density floor | Useful as a stopgap for the all-explained-but-still-thin case | **Agrees only after** the owner is shown the Part 7 → Part 10g history (question 4) |
| Q5 hurdle | Keep caller-supplied alpha; formula domain per 5g | **Agrees** on alpha |
| Q6 venue | Amend ADR-012 rule 8 | **Agrees** |
| Q7 one ruling or two | One ruling serves both | **Differs — rule separately.** Backtest adequacy and paper length are different quantities, and the evidence-bar reviewer already recommended the Investment Committee route for the paper number |

**The open gap this ruling records rather than closes: regime coverage.** `Validation/Critic.md:17` asks what regimes break a strategy; `constitution/Promotion_Pipeline.md:78` makes `Regime robustness` a promotion criterion; `constitution/Capital_Authority.md:15` makes `Regime compatibility` a capital input. Belay can measure none of it (`framework/services/regime.py:1-10`, `docs/ROADMAP.md:75-81`). **5a is the quantified case for the deferral**: a span floor is a weak probabilistic proxy for regime coverage, and the 128-month recession-free stretch is the proof. Record it so the definition is reopened when regime classification exists, rather than assumed complete.

---

## 9. Implementation sketch for a later session (not code)

**`framework/metrics/statistics.py`.** `sample_adequate` (`:303`) stops being derived from `needed` and becomes `observations >= count_floor and span >= span_floor`, both floors supplied by the ruling and never derived from `returns`. `significance()` gains the span as a `SamplePeriod` (`framework/metrics/reporting.py:42-44`, ADR-013 rule 7 — two dates, already the type `Disclosure` demands at `framework/metrics/reporting.py:148-155`) rather than a day count, because the caller already holds one from `DailyBarSeries.period()`. If a declared-target candidate is ruled, the declared target, skew, kurtosis and the per-period `c` are arguments with **no defaults**, per ADR-012 rules 2 and 3; inputs outside §5g's domain must not be coerced into a fabricated `N_MIN`. If Candidate 2H is ruled **with a universal observation flat count**, the implementation must apply `max(flat_count, MinTRL)` in observation units as written — and tests must assert the monthly override (`max(756, 49) == 756`), not the unrestricted MinTRL figure. `SignificanceResult` (`framework/metrics/statistics.py:84-95`) gains the floors applied and the span measured: a floor that is not reported cannot be checked.

**F-027 in the same change, not after it.** `significance()` catches the refusal from `minimum_observations_for_significance` and substitutes `_MAX_OBSERVATIONS` (`framework/metrics/statistics.py:284-289`, constant at `:71`) — the exact number the refusal at `:231-236` exists to avoid emitting. That substitution exists **only** to keep `sample_adequate` computable at `:303`. Once adequacy no longer depends on `needed`, it has no purpose and can be deleted: `minimum_observations` becomes `int | None` with the reason carried beside it, the unruled fix proposed at `docs/HANDOFF.md:4467-4469` (the problem statement is at `:4230-4266`). Doing it here avoids signing an artifact whose `parameters` (`:375-376`) carry a fabricated 1,000,000 — `framework/metrics/reporting.py:219-232` places those inside the integrity hash and `Knowledge/Versioning.md:25` ("No version is overwritten") means the first wrong one cannot be corrected. `significance_artifact` has no non-test caller today, so nothing has been signed yet.

**The Disclosure block needs no new field.** `SamplePeriod` carries the span; `metric_artifact`'s `observations` argument carries the count (`framework/metrics/reporting.py:168-179`). What changes is that both floors and the measured span join `parameters`, so "this sample was adequate" sits inside the signature next to the rule that produced it.

**ADR-012: amendment, not a new ADR** (question 6). Rule 8 is the rule being repaired. The amendment states the two-part definition, the ruled numbers, the treatment of `c` under rule 2, and the deferred regime gap with 5a's percentages.

**The tests that would prove the boolean is now independent.**

1. **The load-bearing one.** The mutation that must turn it red is restoring `sample_adequate = len(returns) >= minimum_observations_for_significance(...)`. So the test needs a series whose count is **below its own `needed`** while clearing the ruled floors — which must report `adequate is True` — **and** the converse, a series whose count exceeds its own `needed` while failing a floor, reporting `adequate is False`. A test that only holds count and span fixed while varying the effect is insufficient: it can pass under the old formula.
2. **All four outcomes exist.** One case each for (significant, adequate), (significant, not adequate), (not significant, adequate), (not significant, not adequate). Two are unreachable today; naming all four states that rule 8's distinction is real.
3. **Each floor binds alone.** A series clearing the count and failing the span, and one clearing the span and failing the count, both report `False` — otherwise "AND" has been implemented as "OR".
4. **F-027's three states are distinguishable.** A series whose mean sits exactly on the null (`[0.01, -0.01, 0.02, -0.02]`, per `docs/HANDOFF.md:4438-4451`) must not report `minimum_observations = 1000000`.
5. **F-017 while the file is open.** `docs/HANDOFF.md:4181-4188` records that removing the `abs()` at `framework/metrics/statistics.py:221` passes the entire suite. One below-null series through `significance()` closes it. Different finding, different commit — but the session should know it is there.

---

## 10. The questions only the owner can answer, in order

Ask one at a time. Each says what the thing is and why Belay needs it before asking.

**Question 1 — the span floor.** A "span" is the stretch of calendar time a track record covers, first observation to last. Belay needs one because a record measured entirely inside a calm market has not been tested by anything. **The numbers reported in 5a** (the original pass recomputed them from NBER's post-war recession dates; externally sourced; **not frozen in this repository** — Issue #6 did not reconstruct the exact rolling-window percentages from repo evidence alone): of every possible window in 1945-2020, the share containing at least one recession month is reported as **27.7% at 1 year, 55.3% at 3 years, 73.2% at 5 years, 81.2% at 6.2 years, 98.7% at 10 years** — and the longest recession-free stretch on record is 128 months (July 2009 – February 2020), so **no realistic span guarantees a downturn**. The cost, for a daily strategy: on historical data, any of these is seconds of fetching; on a paper track record, the span *is* the wait — 3 years, 5 years, 6.2 years of real time before anything can be called adequate. Options: **(a) 3 years**; **(b) 5 years**; **(c) 6.2 years**; **(d) no span floor**. *Both first-pass recommendations were (a) — as a judgement call, not a derivation: it is the shortest window with better-than-even odds of containing a downturn on those reported percentages, and each longer option buys ~18 percentage points for years of delay.*

**Question 2 — may the count floor depend on a number the strategy declares about itself?** A "target Sharpe ratio" is a strategy's stated ambition — roughly, how much return per unit of risk it claims. Let it be declared in advance and the required sample size follows from a published formula that adapts correctly to daily versus monthly strategies **when MinTRL is used alone**. It is not the *observed* result, so it does not re-create F-004 — but it is a number the author picks.

**The arithmetic the owner must see before choosing (Issue #6):**

| Rule | Daily, target ≳ 1.13 | Monthly, target 1.0 | Monthly, target 0.5 |
|---|---|---|---|
| Unrestricted Candidate 2 (MinTRL alone) | MinTRL often **below** 756 — frequency-adaptive but **gameable** by declaring a high target | **49 obs ≈ 4.1 yr** | **187 obs ≈ 15.6 yr** |
| Candidate 2H = `max(756, MinTRL)` | Same as flat 756 | **`max(756,49)=756` months = 63 yr** | **`max(756,187)=756` months = 63 yr** |

So: unrestricted Candidate 2 keeps the monthly MinTRL answers and can be gamed downward; Candidate 2H with a universal 756-observation flat floor blocks that game and **re-imposes Candidate 1's 63-year monthly hole** for ordinary targets. **Those two goals are in tension.** No frequency-normalised flat floor (e.g. converting 756 daily bars into 36 monthly bars) is proposed here — that would be inventing a threshold.

Options: **(a) yes, raise-only (Candidate 2H) with a universal observation flat floor** — then hear that monthly MinTRL figures like 49/187 do **not** become the requirement; **(b) yes, unrestricted Candidate 2** — frequency-adaptive, and declaring a high target shrinks the bar with nothing later holding the strategy to its declaration; **(c) no, one fixed count for everything (Candidate 1)**. *After Issue #6 the author recommendation among (a)/(b)/(c) is unresolved; the first pass had recommended (a) under the false assumption that monthly MinTRL still applied under 2H.*

**Question 3 — the flat count itself.** Options: **(a) 756 observations**; **(b) 1,260**; **(c) refer it to the Investment Committee**, as `strategies/PromotionCriteria.md:29` already refers promotion thresholds. *For a dense daily series 756 is the three-year span restated (3 × 252), not a second independent guard. Under Candidate 2H it is also the monthly floor (63 years of months) unless a different, frequency-aware flat count is ruled later — not invented here. First pass recommended (a) for daily; Issue #6 requires the owner to hear the monthly coupling before adopting (a) together with 2H.*

**Question 4 — a sparse record: does anything still need to catch it, now that gaps will fail closed?** A record can satisfy both floors and still be full of holes: 760 observations spread over 20 years passes "756 AND 3 years" while covering about 10% of the calendar days in its own window. **History of the gap ruling, stated accurately:** Part 7 (`docs/OwnerDecisions.md:914-916`) originally left "what a detected gap then does" unruled. **Part 10g (`:1487`) later answered the unexplained-gap case:** once a trading calendar exists, an **unexplained gap fails closed** — the fetch is refused rather than stored with a warning — while a gap explained by the calendar or by a recorded reason such as a halt is allowed and disclosed (Part 7 carries an in-place correction at `:917-922` saying so). **If that holds, a series with unexplained holes cannot reach a statistical review at all**, so a density floor is redundant for *that* failure mode. What remains for this question is the case Part 10g does **not** settle: a series whose gaps are *all explained* — a long halt, a delisting, a market that genuinely did not trade — which fails closed nowhere and can still be too thin to conclude from. Options: **(a) no density floor — the data layer is the right place, and the calendar ruling covers unexplained gaps**; **(b) a density floor as a stopgap until the calendar exists, expiring when it does**; **(c) a permanent density floor, to catch the all-explained-but-still-thin case.** *This author leans (b); the first-pass reviewer treated density as the owner's question rather than research's — still fair for the remaining thin-but-explained case.*

**Question 5 — how strict is the hurdle inside the formula?** The conventional critical value is 1.96. Harvey, Liu and Zhu argue a newly discovered factor needs a t-ratio above 3.0 because so many are tried; using 3.0 multiplies every sample requirement by about 2.34. Options: **(a) keep alpha as the caller already supplies it** — ADR-012 rule 3 already refuses to default it; **(b) fix a stricter hurdle for adequacy specifically.** *Both recommend (a) — a second threshold in the same module is a second place to disagree.* **Related and not optional:** the formula also needs a reference point `c` — "better than what?" — and ADR-012 **rule 2** forbids defaulting that to zero. Proposed: `c` is the null the caller already supplies, converted to the same per-period units. Confirm, or name a different reference.

**Question 6 — where does this live?** Options: **(a) amend ADR-012 rule 8**, keeping one decision about one module; **(b) a new ADR-016**, so the numbers can be revised later without reopening the significance test. *Both recommend (a).*

**Question 7 — one ruling, or two?** There are two different questions wearing the same words. **Backtest adequacy** asks how much *history* a statistical review needs — it costs seconds to fetch. **Paper-trading length** asks how long Belay must run a strategy on live prices with fake money — it costs that much real time, because the data does not exist until it passes. Options: **(a) one ruling — this definition is the quantity, and the evidence bar cites it per rung**; **(b) two — rule backtest adequacy here, and send the paper-trading length to the Investment Committee**, which is where `strategies/PromotionCriteria.md:29` already sends promotion thresholds. **The two reviews differ.** *This author recommends (a), so Belay has one answer to "how much data is enough" rather than two that can drift apart. The independent reviewer recommends (b), because the quantities differ by orders of magnitude in cost and because the evidence-bar proposal's own independent reviewer already recommended the Investment Committee route for the paper number.* **Note the interaction with question 1:** under (a), whatever span you set at question 1 also governs the paper track record — so choosing 3 years there means **no strategy reaches real capital for three years**.

---

## Appendix A — what could not be checked

- **The owner's rulings were not in the repository when this document was first drafted.** `docs/OwnerDecisions.md:988` (Part 8) and `:1099-1102` (Part 9a) both carry a dated 2026-09-19 (evening) correction, and Part 10 (10e-g, `:1411`-`:1515`) is now the record: F-004 is ruled as to shape, its numbers are not; F-006's narrow fix is authorised and its wide question is ruled as a calendar-first proposal with gaps failing closed. **This document still authorizes no work** — it proposes the numbers; it does not rule them.
- **Nothing in Belay was executed.** No code was run and no test was run. The F-027 behaviour is read from `framework/metrics/statistics.py:284-289` and from `docs/HANDOFF.md:4438-4451`, which records having re-executed it.
- **MinBTL was sought and not retrieved.** Bailey, Borwein, López de Prado and Zhu's minimum-backtest-length formula bears on the evidence bar's trial-count question; both PDFs reachable this session were image-only and SSRN returned 403. **No MinBTL claim is made anywhere above.**
- **The MinTRL leading-constant caveat is now closed, except for the primary paper.** Both retrieved sources give the leading term as `1 − κ·SR + (γ−1)·SR²/4`; under κ=0 and γ=3 that equals `1 + SR²/2`, so the "1 +" rendering seen elsewhere is the same expression, and the effect on section 5c is zero. **Only the Journal of Risk paper itself remains unread.**
- **ADR-012's citation to `docs/ROADMAP.md:72` has rotted.** `docs/DECISIONS.md:2142-2144` cites line 72 as "a sentence ... observing that Belay computes none of this"; line 72 today reads "gained `framework/metrics/statistics.py` (ADR-012)." Noted, not fixed — it belongs in the register.
- **The working tree was not clean when this document was drafted.** Every citation was originally read via `git show origin/main:<path>` at `3080848`, never from the working copy. [**Committer's note, 2026-09-19 (evening).** The register commits have since landed (PR #9 as `2f44c19`, PR #11 as `3080848` onto `main`) and this branch carries further changes on top; every citation above was re-read against `records/2026-09-19-rulings` and repointed by content where it had moved.]

---

## Appendix B — what changed in this revision, and why (Law VII)

All 15 reviewer defects were re-verified against source by this author; **all 15 were confirmed and applied, none rejected.** One correction to the reviewer, noted rather than silently absorbed: the longest recession-free stretch is **July 2009 – February 2020**, not "Jun 2009 – Jan 2020"; the count of 128 months is right and the endpoints were off by one month each.

| # | Defect | What changed |
|---|---|---|
| 1 | **BLOCKER** — span derivation false | Claim withdrawn in 5a and replaced by the recomputed containment table (55.3 / 73.2 / 81.2%) and the 128-month stretch; the span floor is relabelled a judgement call throughout; question 1 now shows the percentages and the cost side |
| 2 | **BLOCKER** — `c = 0` silently defaulted against ADR-012 rule 2 | 5b makes `c` the caller's own null converted to per-period units, with rule 2 cited at `docs/DECISIONS.md:2184-2188`; added to question 5 and to the §9 signature |
| 3 | **BLOCKER** — Candidate 2's gaming line wrong, crossover missing | 5d added: crossovers 0.951 / 1.133 / 1.737, the collapse into Candidate 1 for daily series, and the monthly figures; Candidate 2's "fails" bullet rewritten around it |
| 4 | **BLOCKER** — unbuilt anti-gaming mitigation | The "judged against 2.0" claim is withdrawn in Candidate 2; **Candidate 2H** added (declared target may only raise `N_MIN`) and adopted in the recommendation; question 2 gains it as option (a) |
| 5 | **BLOCKER** — Q4 ruled a reserved question | Question 4 rewritten around the owner's fails-closed selection, framed as their reserved question with `docs/OwnerDecisions.md:914-916` cited, and now asks whether a density floor is redundant, a stopgap, or permanent |
| 6 | 6 table cells floored not ceiled | Whole table recomputed with ceilings (2,730 / 684 / 305 / 3,875 / 971 / 433) and the non-normality figure moved to 971 → 1,004 |
| 7 | "derived rather than chosen" overclaimed | 5e added, naming it an a-priori power calculation conditional on a chosen target; the recommendation repeats the conditional |
| 8 | ÷√252 conversion unstated | Written out in 5b, with the `refSR` non-annualised quote added to §4 |
| 9 | Leading-constant caveat closeable | Appendix A caveat replaced with the algebraic identity; only the primary paper remains unread |
| 10 | §7/Q7 conflated two quantities | §7 rewritten to separate backtest adequacy from paper length and to surface the evidence-bar reviewer's Investment Committee recommendation (historical Atlas archive revision `8e3edb2` on the then-private carrier; live navigation is now public PR #7 Question 4); question 7 now presents both neutrally |
| 11 | Q1×Q7 interaction buried | Stated at the end of question 7 |
| 12 | F-027 fix cited at the wrong lines | Corrected to `docs/HANDOFF.md:4467-4469`, with the problem statement at `:4230-4266` |
| 13 | Density denominators inconsistent | §2 now uses the calendar-day basis (10.4%) and shows the trading-day figure (15.1%) beside it |
| 14 | §9 test 1 insufficient | Test 1 rewritten around the mutation it must catch, requiring a below-`needed` case and its converse |
| 15 | 756 and 3 years are one constraint for daily | Stated in §2, in Candidate 1, and in question 3 |
| — | Dissent not recorded | §8 gains a side-by-side table of both recommendations, attributed, including the Q7 disagreement |

---

## Appendix C — Issue #6 second independent falsification pass

Append-only. Does not erase Appendix B. Issue #6 is not a scheduled full-repository `/belay-review` and allocates no F-NNN numbers.

| Finding | Class | Disposition | Correction |
|---|---|---|---|
| Candidate 2H arithmetic vs monthly MinTRL story | **BLOCKER** (defect) | Accepted | §5d, Candidate 2/2H, §8, Q2, Q3, §9 sketch rewritten; author 2H recommendation withdrawn as unresolved pending flat-count/frequency ruling; no frequency-normalised floor invented |
| MinTRL undefined when `SR == c` or leading factor ≤ 0 | Defect | Accepted | §5g states those inputs do not yield a valid computed minimum; refuse-vs-fallback left unresolved; cites `statistics.py` refusal precedent |
| Q4 cited Part 7 as still "explicitly left unruled" without Part 10g | Defect | Accepted | Q4 now records Part 7 reserved → Part 10g answered unexplained gaps; remaining question is all-explained-but-still-thin |
| Evidence-bar locator as PR #10 / `8e3edb2` | Defect (live locator) | Accepted | §7 points at public PR #7 / `adr/015-stage-is-carried` Question 4; Atlas IDs retained as historical provenance only |
| Rolling NBER containment percentages | Unverified external claim | Narrowed, not called false | §5a / Q1 provenance note: externally sourced; not reconstructible from repository-frozen evidence |

**Not treated as defects requiring redesign here:** owner choices among Candidates 1 / 2 / 2H once the arithmetic is honest; span years as judgement; Q7 one-vs-two ruling; whether declared targets are allowed under a stricter reading of F-004.
