# Promotion Pipeline

Every strategy possesses a maturity level.

---

Level 0

Idea

Research only.

---

Level 1

Hypothesis

Formal specification.

---

Level 2

Validated

Passed statistical review.

---

Level 3

Paper Trading

No real capital.

---

Level 4

Micro Capital

Minimal financial exposure.

Primary objective:

Operational validation.

---

Level 5

Limited Capital

Expanded allocation.

Primary objective:

Scaling validation.

---

Level 6

Production

Eligible for standard capital allocation.

---

Promotion Requirements

Promotion shall consider:

- Statistical performance
- Risk-adjusted returns
- Drawdown behavior
- Regime robustness
- Execution quality
- Liquidity
- Operational consistency

Promotion shall never depend upon profitability alone.

---

> **These seven levels are a maturity model, not the lifecycle. ADR-007 rule 2.**
>
> They describe how *proven* a strategy is. The lifecycle describes what *capital* it
> has earned, and that is the eight stages of
> `constitution/Paper_First_Capital_Doctrine.md` — the sequence `StrategyLifecycle`
> implements. Two axes, not two competing sequences. This document has no promotion
> review and begins `Idea, Hypothesis`; the doctrine has a promotion review and begins
> `Idea, Research`. Read as rival sequences they disagree; read as two axes they do
> not.
>
> Recorded because the confusion has already cost something. ADR-002 cited this
> document for "eight promotion gates" — a group of eight it does not contain — and
> that false citation stood inside an Accepted decision until ADR-007 amended it.
>
> **The seven criteria above at lines 75-81 are the authoritative promotion criteria.
> ADR-006 rule 1**, on the authority of `constitution/Governance.md:7`, "The
> Constitution possesses authority". Their wording is canonical where the departmental
> documents disagree on a name. `tests/test_governance_conformance.py` parses this
> list and holds `scripts/status.py` to it.
