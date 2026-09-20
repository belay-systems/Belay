# Strategy Lifecycle

Every strategy follows the same institutional lifecycle.

Research

↓

Hypothesis

↓

Validation

↓

Paper

↓

Promotion Review

↓

Micro Capital

↓

Limited Capital

↓

Production

↓

Retirement

Strategies may move backward.

Strategies never skip stages.

Strategies remain observable throughout their lifetime.

Retirement preserves history.

Deletion is prohibited.

---

> **Retirement is not the ninth rung of this ladder. ADR-007 rule 3.**
>
> The nine entries above are joined by `↓` arrows, and the last of them — from
> `Production` to `Retirement` at lines 33-37 — is the one that misleads. It presents
> retirement as the stage a strategy reaches by surviving Production, which is the
> reading both ADR-007 rule 3 and ADR-004 deny. **Retirement is outside the sequence
> and reachable from every stage**, exactly as `constitution/Paper_First_Capital_Doctrine.md:51-53`
> writes it: "Demotion may occur at any stage. Retirement may occur at any stage."
> A strategy retired out of Paper Trading has climbed nothing.
>
> This has a live cost in code, which is why it is worth recording here rather than
> only in the ADR. `RETIRED` is the highest ordinal in `StrategyLifecycle` — index 8,
> above `PRODUCTION` at 7 — so anything that compares stage positions must use
> `STRATEGY_LADDER` from `framework/artifacts/enums.py`, which excludes it, and must
> classify retirement *before* taking a position. Under a bare ordinal comparison
> every retirement reads as the deepest promotion in the system. This document is
> what makes that mistake look reasonable.
>
> **The lifecycle is the doctrine's eight stages** — `Idea, Research, Validation,
> Paper Trading, Promotion Review, Micro Capital, Limited Capital, Production` — and
> that is the sequence `StrategyLifecycle` implements. Beside them this list diverges
> four ways: it omits `Idea` and opens at `Research`, it inserts `Hypothesis` (which
> is `Promotion_Pipeline.md`'s maturity vocabulary, not a capital stage), it writes
> `Paper` where the doctrine writes `Paper Trading`, and it appends `Retirement`. So
> it is not the doctrine plus a ninth entry: the first two rungs differ as well. From
> `Validation` onward the order is identical.
>
> **Nothing above is deleted, and two lines below the sequence are load-bearing.**
> `Strategies may move backward` at line 39 is one of the five citations ADR-004 rests
> its demotion ruling on, and `Strategies never skip stages` at line 41 is quoted in
> the comment above `STRATEGY_TRANSITIONS` in `framework/artifacts/validator.py` and in
> three test docstrings. Both survive intact, and this note is annotation rather than
> rewriting for that reason — Immutable Law VII, and the same treatment already given
> to `constitution/Promotion_Pipeline.md`, `Validation/CapitalReview.md` and
> `strategies/PromotionCriteria.md`.
