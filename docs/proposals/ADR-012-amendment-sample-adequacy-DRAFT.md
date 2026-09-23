# DRAFT — Amendment to ADR-012: rules 3 and 8, and what "enough data" means

Status:
**PROPOSED amendment, drafted from owner rulings, not ratified. Not implemented
in any part.** ADR-012 itself stays **Accepted** as ratified on 2026-07-31. Only
the owner changes an ADR's text or status (`AGENTS.md`, "What only the owner may
change").

Date:
2026-09-23

---

> **What the owner ruled, and what the drafter chose.** Every rule below carries
> one of two marks:
>
> - **RULED**: the owner's ruling, cited to `docs/OwnerDecisions.md` Part 22,
>   where the owner's words are quoted.
> - **DRAFTER**: a choice this draft makes to turn a ruling into something code
>   can check. The owner has not seen or ruled it. Each one is listed again
>   under "Put to the owner at ratification".
>
> Nothing marked DRAFTER may be read as ruled.

> **Nothing here has had an independent pass.** `AGENTS.md` (How work is
> claimed and landed, point 4) requires one before anything is called verified.
> The next step is that pass, told to falsify this draft.

> **Source.** The corrected sample-adequacy proposal on pull request #7's
> branch (`adr/015-stage-is-carried`), not the uncorrected copy on `main`,
> and the owner's ten rulings on it, `docs/OwnerDecisions.md` 22a–22j.

---

## Context

**ADR-012 rule 8 says sample adequacy is its own question, and the code
answers it with the significance test again.** `sample_adequate` is
`len(returns) >= needed` (`framework/metrics/statistics.py:303`), where
`needed` is the smallest `n` at which the *observed* effect would clear the
critical value. That is the significance test restated, so `sample_adequate`
and `significant` can never disagree (F-004). ADR-012's own Still-Open section
names what was missing: "No document says how many Belay *demands* before a
strategy may be promoted."

**ADR-012 rule 3 leaves the significance level to the caller, with no floor.**
Under Part 19 the caller is a user's AI, and 19c rules that Belay sets minimums
that users may only raise.

**F-027 rides on the same lines.** When no sample size can establish the
effect, `significance()` substitutes `_MAX_OBSERVATIONS` (1,000,000) for
`needed` (`framework/metrics/statistics.py:284-289`) so that `sample_adequate`
stays computable, the very number the refusal at `:231-236` exists not to
emit. The proposal's §9 requires F-027 to land in the same change as these
numbers. Nothing has been signed yet: `significance_artifact` has no caller
outside the tests.

---

## Rule 3, amended

**Present text** (`docs/DECISIONS.md:2190-2194`): "Alpha is supplied, never
defaulted. … Belay does not pick a number nobody wrote down."

**Amended text, RULED (22h):**

> **3. Alpha is supplied, never defaulted, and never looser than a critical
> value of 3.0.** The caller still states the level. Belay refuses one whose
> critical value is below 3.0, in the significance test and in the adequacy
> calculation alike. A caller may be stricter, never looser. The number is
> now written down, with its source: Harvey, Liu and Zhu, NBER Working Paper
> 20592 (2014), "a newly discovered factor needs to clear a much higher
> hurdle, with a t-ratio greater than 3.0", because in finance many
> candidates are tried, and Belay's users' AIs will try more (Part 18e).

**DRAFTER, the check:**

- **Refused, not raised to the floor.** `significance()` raises when the
  two-sided critical value for the caller's `alpha` is below 3.0. It does not
  quietly substitute a stricter one, because a silent substitution hides from
  the caller that their setting did nothing. This matches ADR-016 draft rule 7.
- **Measured at the sample's own degrees of freedom** for the test,
  `t_critical_value(alpha, n - 1) >= 3.0` (`framework/metrics/distributions.py:148`),
  and at the normal limit for the
  adequacy formula (rule 8, condition (b)). A t critical value is never below
  the normal one at the same alpha, so an alpha that clears 3.0 at the normal
  limit clears it at every sample size. **In practice the check is on the
  normal limit:** a two-sided alpha of at most about 0.0027.

---

## Rule 8, amended

**Present text** (`docs/DECISIONS.md:2231-2238`) is kept whole, and its
principle is unchanged: "A sample below that number has not failed the test —
it has not taken it." What changes is *which number*.

**Amended text, RULED (22a–22g, 22i):**

> **8. Sample adequacy is a separate question with its own answer, and the
> answer does not depend on the observed effect.** For historical (backtest)
> data, a sample is adequate only when **all** of the following hold:
>
> **(a) Span.** The observations cover at least **10 calendar years**, first
> to last. (22b)
>
> **(b) Observations.** The number of observations is at least the minimum
> track record length (Bailey and López de Prado, *The Sharpe Ratio Efficient
> Frontier*, Journal of Risk 15(2), 2012) for the target the strategy
> **declared before the test**, at the series' own frequency:
>
> `N = (1 − κ·SR + (γ−1)·SR²/4) · (z / (SR − c))²`
>
> where `SR` is the declared target Sharpe ratio, `κ` and `γ` the declared
> skewness and kurtosis, all per period, `z` the critical value of rule 3,
> and `c` the test's own null (rule 2), converted to the same per-period
> units. Because (a) must also hold, the requirement is whichever is longer,
> the 10 years or `N`. **No declaration can lower it below 10 years.**
> (22c, 22i)
>
> **(c) No flat count.** There is no fixed minimum number of observations
> beyond (b). (22d)
>
> **(d) Completeness.** At least **95%** of the observations expected in the
> window are present. Explained gaps (a halt, a delisting) count as missing
> for this purpose. Part 10g decides whether a gap is allowed; this condition
> decides whether what remains is enough. (22e, 22f)
>
> **(e) No long gap.** In daily data, no two consecutive observations are
> more than **7 calendar days** apart. (22g)
>
> **(f) A formula with no answer fails closed.** If `SR = c`, or the leading
> factor `1 − κ·SR + (γ−1)·SR²/4` is zero or negative, the sample is **not
> adequate**, with the reason recorded. The result is never turned into a
> number and never falls back to (a) alone. (22i)
>
> **Paper-trading length is not this rule.** It is referred to the Investment
> Committee, and `Micro Capital` stays closed until it is set (Part 18d, 22a).
>
> `minimum_observations_for_significance` stays as a reported number: how many
> observations the **observed** effect would need. It no longer decides
> `sample_adequate`.

**DRAFTER, how each condition is measured:**

1. **The dates travel with the returns.** Conditions (a), (d) and (e) need the
   date of every observation. `significance()` receives only `returns` today.
   It gains a required `dates` argument, one date per return in strictly
   increasing order, and derives the span, completeness and gaps from it. It
   does not take a separately supplied span, because a span stated apart from
   the data is the F-006 failure, where two bars ten years apart would
   "disclose" ten years.
2. **"10 calendar years"** means the last date is on or after the first date
   plus 10 years, same month and day, with 29 February read as 28 February.
3. **The expected count in (d)**, until a trading calendar exists (Part 10g):
   for daily data, the calendar days in the window × 252 / 365.25. Once a
   calendar exists, its count for the window replaces the estimate. The
   estimate is recorded as an estimate on the artifact.
4. **A target at or below the reference is outside the formula's range.**
   22i names `SR = c`. Below `c` the formula still returns a finite number,
   because the denominator is squared, but a strategy claiming *less* than the
   null has nothing to demonstrate. This draft treats `SR ≤ c` as (f), not
   adequate. **This extends 22i and needs the owner's confirmation.**
5. **`z` in (b)** is the two-sided normal critical value for the caller's
   alpha, the same two-sided convention as rule 4, which rule 3 now bounds at
   3.0 or more.
6. **The declared target, skewness and kurtosis are required arguments with
   no defaults**, recorded inside the artifact's signature, per rules 2 and 3.
   Normal tails (`κ = 0`, `γ = 3`) are a declaration like any other, never
   assumed.
7. **Every condition is reported.** `SignificanceResult` gains each floor
   applied, the value measured, and which conditions failed. A floor that is
   not reported cannot be checked (the proposal's §9).
8. **Other frequencies.** Condition (e) is ruled for daily data only (22g).
   A weekly or monthly series is **not adequate until its gap rule is
   ruled**, rather than passing with no gap rule at all.

---

## F-027, in the same change

**DRAFTER, from the proposal's §9:** delete the `_MAX_OBSERVATIONS`
substitution at `framework/metrics/statistics.py:284-289`. It exists only to
keep `sample_adequate` computable, and after rule 8 as amended it has no
purpose. `minimum_observations` becomes "a number, or none, with the reason
beside it". No artifact will ever carry a fabricated 1,000,000 inside its
signature.

---

## Tests this implies

Each is written red first against the unchanged code, and each names the
mutation it must catch.

1. **Adequacy is independent of the observed effect.** A series below its own
   `needed` that meets every condition reports adequate. A series above its
   own `needed` that fails a condition reports not adequate. Mutation: restore
   `sample_adequate = len(returns) >= needed`.
2. **All four combinations exist**: significant and adequate, significant and
   not, not significant and adequate, neither.
3. **Each condition binds on its own.** For each of (a), (b), (d), (e) and
   (f), one series that meets every other condition and fails only that one
   reports not adequate. Mutation: any "and" written as "or".
4. **The 10-year boundary**: exactly 10 years passes, one day short fails,
   and 29 February start dates behave as DRAFTER 2 says.
5. **(b) binds beyond 10 years**: a declared target of 0.5, with the
   critical value at the 3.0 floor, needs more than 10 years of daily data
   and fails at exactly 10.
6. **No declaration lowers the requirement**: a declared target of 5.0 still
   fails with 9 years of data.
7. **Completeness at 95%**: 95.0% passes and 94.9% fails, with an explained
   gap counted as missing.
8. **The gap rule**: a 7-day gap passes, an 8-day gap fails, and a series
   missing 20 February to 23 March 2020 fails even when it is 99% complete.
9. **(f) fails closed**: `SR = c`, `SR < c`, and a non-positive leading factor
   each report not adequate with a reason, and no `N` is emitted.
10. **Rule 3**: an alpha of 0.05 is refused; an alpha whose critical value is
    3.0 or more is accepted, in both the test and the formula.
11. **F-027**: `[0.01, -0.01, 0.02, -0.02]` does not report
    `minimum_observations = 1000000`.
12. **A weekly or monthly series is not adequate** until its gap rule is
    ruled (DRAFTER 8).

---

## Consequences

- **F-004 closes when this is ratified and implemented**, and F-027 with it.
- **Every backtest needs 10 years of daily data.** Belay's data begins
  2011-01-03, so backtests can be adequate today, and instruments listed after
  late 2016 cannot be yet.
- **Fewer strategies pass significance.** A critical value of 3.0 is about a
  two-sided alpha of 0.0027, against the conventional 0.05. The owner chose
  that knowingly (22h).
- **Calling `significance()` gets harder**: dates, a declared target, skewness
  and kurtosis, all required. That's deliberate, and it will read as friction,
  as rules 2 and 3 already do.

### Residual risk, stated rather than buried

- **The span stands in for regime coverage; it doesn't measure it.** The
  longest post-1945 stretch with no contraction was 128 months, longer than 10
  years. Regime classification remains an open gap
  (`framework/services/regime.py`).
- **The window is the author's to choose** (22b does not settle it). A
  strategy could be backtested on a flattering 10 years.
- **The declared target binds nothing afterwards** (22c does not settle it).
  An author who declares high faces only the span.
- **The t-test's assumptions still make the p-value optimistic** (rule 7).
  None of this corrects that.

---

## Put to the owner at ratification — DRAFTER choices, not rulings

1. A weaker alpha is **refused**, not raised to the floor.
2. The dates travel with the returns; there is no separately supplied span.
3. How "10 calendar years" is counted, including 29 February.
4. The expected count before a calendar exists: 252 trading days a year.
5. **A declared target at or below the reference counts as "no answer"**,
   extending 22i beyond `SR = c`.
6. `z` in the formula is the two-sided normal critical value.
7. Weekly and monthly series are not adequate until their gap rule is ruled.
8. F-027's fix rides in the same change, per the proposal's §9.

## Still open, deliberately

- Regime coverage, as above.
- Which window a backtest may use.
- The gap rule for non-daily data.
- Whether the null should be zero or the risk-free rate as a matter of
  doctrine. ADR-012's existing Still-Open item, unchanged.
- **ADR-012's Still-Open item "What minimum sample Belay requires" is answered
  by this amendment** and would be struck through on ratification, with the
  original wording left standing under Law VII.
