# Strategy Review

Identifier

Reviewer

Date

Version

---

Operational Summary

---

Observed Behavior

---

Expected Behavior

---

Performance Summary

---

Risk Assessment

---

Regime Compatibility

---

Confidence Adjustment

Increase

Decrease

No Change

---

Recommendation

Promote

Remain Current Stage

Demote

Retire

---

Justification

Evidence only.

---

> **`Remain` became `Remain Current Stage` on 2026-07-31, per ADR-008 rule 3.**
> Two of the three documents listing these outcomes already used the longer form,
> and it is unambiguous where bare `Remain` is not — remain *at what*. The other
> two are `Validation/CapitalReview.md` and
> `workflows/Monthly/StrategyPromotion.md`.
>
> **`Justification` is required for every outcome above, not only for the
> unfavourable ones.** Four documents say so between them:
> `strategies/PromotionCriteria.md:33` (promotion), `:35` (rejection),
> `constitution/Governance.md:15` (retirement) and
> `workflows/Monthly/StrategyPromotion.md:37`, which requires it of every
> decision without qualification. ADR-004 rule 4 adds demotion. This is enforced
> in code as of ADR-009: a review record with an empty justification is refused.
>
> The fields above are held by `framework/artifacts/review.py`. `Identifier` and
> `Version` name the **strategy under review** — ADR-009 rule 2, on the grounds
> that read any other way this template names no subject at all. The review
> record carries its own identifier and version separately, as
> `constitution/Governance.md:19-25` requires of every artifact.
