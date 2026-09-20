# Capital Review

Purpose

Determine whether a validated strategy has earned progression.

Capital Review does not allocate capital.

Capital Review recommends promotion.

---

Promotion considers

Evidence quality

Drawdown

Regime robustness

Consistency

Operational consistency

Paper performance

---

Possible Outcomes

Reject

Remain Current Stage

Promote

Demote

Retire

---

> **Reconciled to the Constitution 2026-07-31 by ADR-006.** `Operational readiness`
> became `Operational consistency`: ADR-006 rule 3 makes the constitutional wording
> canonical and names this rename explicitly — "not stability or readiness".
> `Regime robustness` and `Drawdown` already matched and are unchanged.
>
> **Two things this reconciliation did not settle, recorded rather than guessed:**
>
> `Consistency` above now sits beside `Operational consistency` and may be the same
> concept twice. ADR-006 analysed the naming collision but did not rule on this
> document carrying both, so neither line is removed here.
>
> This list omits four constitutional criteria — `Statistical performance`,
> `Risk-adjusted returns`, `Execution quality` and `Liquidity`. ADR-006 rule 5 rules
> departmental omissions to be defects, but enumerates only
> `workflows/Monthly/StrategyPromotion.md`'s three. Adding four criteria to a review
> whose stated purpose is narrower — lines 7 and 9: "Capital Review does not allocate
> capital. Capital Review recommends promotion." — expands a department's remit, and
> that is a ruling to make deliberately rather than in passing.

---

> **`Reject` defined, 2026-07-31, per ADR-008 rule 4.** It appeared in this list
> and nowhere else in the repository, was never defined, and was never
> distinguished from `Retire`.
>
> **`Reject` and `Remain Current Stage` are one event named from two sides.**
> This document is the only one carrying both, and its own lines 7 and 9 explain
> why: "Capital Review does not allocate capital. Capital Review recommends
> promotion." It processes a *request*. `Reject` names the decision on the
> request; `Remain Current Stage` names the effect on the strategy. Rejecting a
> promotion leaves the strategy where it is. The other two documents list only
> the state-side name because neither is framed as handling an application.
>
> In code there are four outcomes, not five: `ReviewOutcome` in
> `framework/artifacts/enums.py` carries `Promote`, `Remain Current Stage`,
> `Demote` and `Retire`, and `Reject` resolves to `Remain Current Stage`. One
> event with two names must not become two members.
>
> A competing reading is recorded rather than dismissed: `Reject` could have
> meant rejected *as a candidate* — dropped out of Promotion Review back to Paper
> Trading — which ADR-004 already treats as a distinct move. Under that reading
> `Reject` is a specific demotion rather than a synonym. This document supported
> both readings and the code supported neither, so ADR-008 adopted the ruling
> above and required it be stated here rather than left inferable.
>
> `Every rejection requires written justification` — `strategies/PromotionCriteria.md:35`.
> Under this ruling that obligation attaches to `Remain Current Stage` too, which
> is why ADR-009 makes justification mandatory for every outcome.
