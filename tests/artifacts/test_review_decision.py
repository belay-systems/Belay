"""The review decision record — ADR-009.

Nothing in Belay recorded that a review happened. `strategies/ReviewTemplate.md`
specifies the form of one and no code held it, so a review that decided to hold a
strategy at Limited Capital was indistinguishable in the system's state from no
review having taken place. `constitution/Governance.md:11` requires that all
decisions be documented.

Three ratified obligations were waiting on this single component: ADR-004 rule 4
(written justification for a demotion), ADR-004's re-sizing step, and ADR-008's
`Remain Current Stage`.

These tests were written before the implementation and run against the unchanged
code to prove they fail rather than pass vacuously.
"""

from __future__ import annotations

import dataclasses

import pytest

from framework.artifacts.enums import (
    ArtifactType,
    ConfidenceAdjustment,
    ReviewOutcome,
    StrategyLifecycle,
)
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.review import review_artifact, review_fields
from framework.artifacts.validator import ArtifactValidator

REVIEW_ID = "REV-0048"
SUBJECT = "STRAT-0001"


def a_review(**overrides):
    """A minimal valid review: a strategy held at its current stage."""
    arguments = dict(
        identifier=REVIEW_ID,
        subject_id=SUBJECT,
        subject_version="1.2.0",
        reviewer="Investment Committee",
        outcome=ReviewOutcome.REMAIN_CURRENT_STAGE,
        stage_at_review=StrategyLifecycle.LIMITED_CAPITAL,
        resulting_stage=StrategyLifecycle.LIMITED_CAPITAL,
        justification="Paper performance steady; drawdown within limits.",
        confidence_adjustment=ConfidenceAdjustment.NO_CHANGE,
    )
    arguments.update(overrides)
    return review_artifact(**arguments)


# ------------------------------------------------- ADR-009 rule 1: it is an Artifact


def test_a_review_decision_is_a_signed_artifact_of_type_review():
    """ADR-009 rule 1. Not a parallel record type.

    A decision record that can be altered after the fact documents nothing, and
    signing is the property an Artifact brings. `ArtifactType.REVIEW` already
    existed, so no enum member is added — the open ArtifactType finding is
    routed around rather than answered by accident.
    """
    artifact = a_review()

    assert artifact.type is ArtifactType.REVIEW
    assert artifact.integrity_hash is not None
    assert ArtifactIntegrity.verify_hash(artifact)
    assert ArtifactValidator().validate(artifact)


def test_a_review_carries_no_strategy_stage_of_its_own():
    """The review is not the strategy. It reviews one.

    `ArtifactValidator` refuses a `strategy_stage` on anything that is not a
    STRATEGY artifact, because a report claiming a capital stage asserts
    something untrue of itself. The stages under review live in the record's
    content, which is a statement about the subject rather than about the record.
    """
    assert a_review().strategy_stage is None


# ------------------------------------------------ ADR-009 rule 2: the subject


def test_the_record_names_the_subject_and_the_version_reviewed():
    """ADR-009 rule 2. The record has its own identity *and* a subject.

    Under ADR-005 a confidence revision produces a new version, so recording
    which version was in front of the reviewer is the difference between a
    decision about the artifact they read and one about an artifact that has
    changed underneath them since.
    """
    artifact = a_review()
    fields = review_fields(artifact)

    assert artifact.id == REVIEW_ID
    assert fields["subject_id"] == SUBJECT
    assert fields["subject_version"] == "1.2.0"


def test_a_subject_identifier_that_is_not_an_identifier_is_refused():
    with pytest.raises(ValueError):
        a_review(subject_id="DD-0001")


def test_a_subject_version_that_cannot_be_ordered_is_refused():
    """`ArtifactRepository.save()` already refuses a non-semantic version.

    A review naming `v2` cannot be matched against any stored version, so the
    field would record a decision about nothing.
    """
    with pytest.raises(ValueError):
        a_review(subject_version="v2")


# ---------------------------------- ADR-009 rule 4: justification is mandatory


@pytest.mark.parametrize("justification", ["", "   ", "\n\t "])
def test_a_review_without_written_justification_is_refused(justification):
    """ADR-009 rule 4, and the first enforcement of ADR-004 rule 4.

    Four documents require it and between them they cover all four outcomes:
    `PromotionCriteria.md:33` and `:35`, `Governance.md:15`, and
    `StrategyPromotion.md:37` — "Every decision requires written justification."

    Whitespace is not a justification.
    """
    with pytest.raises(ValueError):
        a_review(justification=justification)


def test_a_demotion_without_justification_is_refused():
    """ADR-004 rule 4 specifically. The transition table rules that a move is
    legal; it cannot know whether a reason was written. This is where that lands."""
    with pytest.raises(ValueError):
        a_review(
            outcome=ReviewOutcome.DEMOTE,
            stage_at_review=StrategyLifecycle.PRODUCTION,
            resulting_stage=StrategyLifecycle.MICRO_CAPITAL,
            justification="",
        )


@pytest.mark.parametrize("reviewer", ["", "   "])
def test_a_review_without_a_reviewer_is_refused(reviewer):
    """`Governance.md:19-25` requires every artifact to possess an author.

    Nothing checks the name against a roster: ADR-009 rule 10, because no
    document in the repository names reviewer roles and inventing one would be
    writing doctrine.
    """
    with pytest.raises(ValueError):
        a_review(reviewer=reviewer)


# --------------------------- ADR-009 rule 5: the outcome must match the movement


def test_remain_current_stage_records_a_decision_and_no_movement():
    """ADR-008's entire purpose.

    A held strategy must stop being indistinguishable from an unreviewed one.
    The record exists and says `Remain Current Stage`; the stage did not move.
    """
    fields = review_fields(a_review())

    assert fields["outcome"] == ReviewOutcome.REMAIN_CURRENT_STAGE.value
    assert fields["stage_at_review"] == fields["resulting_stage"]


def test_remain_that_moves_the_stage_is_refused():
    with pytest.raises(ValueError):
        a_review(
            outcome=ReviewOutcome.REMAIN_CURRENT_STAGE,
            stage_at_review=StrategyLifecycle.LIMITED_CAPITAL,
            resulting_stage=StrategyLifecycle.MICRO_CAPITAL,
        )


def test_a_demotion_moves_down_the_ladder():
    artifact = a_review(
        outcome=ReviewOutcome.DEMOTE,
        stage_at_review=StrategyLifecycle.PRODUCTION,
        resulting_stage=StrategyLifecycle.MICRO_CAPITAL,
        justification="Two consecutive months outside the drawdown limit.",
    )

    fields = review_fields(artifact)
    assert fields["resulting_stage"] == StrategyLifecycle.MICRO_CAPITAL.value


def test_a_demotion_that_climbs_is_refused():
    with pytest.raises(ValueError):
        a_review(
            outcome=ReviewOutcome.DEMOTE,
            stage_at_review=StrategyLifecycle.MICRO_CAPITAL,
            resulting_stage=StrategyLifecycle.PRODUCTION,
        )


def test_a_demotion_below_the_floor_is_refused():
    """ADR-004 rule 2: `PAPER_TRADING` is the floor.

    Below it there is no capital privilege to withdraw, and a strategy whose
    statistical proof is falsified has not been demoted but refuted. The record
    checks the transition table rather than re-deciding this.
    """
    with pytest.raises(ValueError):
        a_review(
            outcome=ReviewOutcome.DEMOTE,
            stage_at_review=StrategyLifecycle.PRODUCTION,
            resulting_stage=StrategyLifecycle.VALIDATION,
        )


def test_a_promotion_climbs_one_stage():
    artifact = a_review(
        outcome=ReviewOutcome.PROMOTE,
        stage_at_review=StrategyLifecycle.MICRO_CAPITAL,
        resulting_stage=StrategyLifecycle.LIMITED_CAPITAL,
        justification="Six months at micro capital within every limit.",
    )

    assert review_fields(artifact)["outcome"] == ReviewOutcome.PROMOTE.value


def test_a_promotion_that_skips_a_stage_is_refused():
    """`strategies/Lifecycle.md`: "Strategies never skip stages"."""
    with pytest.raises(ValueError):
        a_review(
            outcome=ReviewOutcome.PROMOTE,
            stage_at_review=StrategyLifecycle.PROMOTION_REVIEW,
            resulting_stage=StrategyLifecycle.LIMITED_CAPITAL,
            justification="Skipping micro capital.",
        )


def test_a_retirement_lands_on_retired():
    artifact = a_review(
        outcome=ReviewOutcome.RETIRE,
        stage_at_review=StrategyLifecycle.PRODUCTION,
        resulting_stage=StrategyLifecycle.RETIRED,
        justification="Edge no longer present; hypothesis refuted.",
    )

    assert review_fields(artifact)["resulting_stage"] == StrategyLifecycle.RETIRED.value


def test_retirement_is_never_read_as_a_promotion():
    """ADR-004's trap, and this is the code that makes it live.

    `RETIRED` is declared at index 8, above `PRODUCTION` at 7, so any bare
    ordinal comparison over `list(StrategyLifecycle)` reads a retirement as the
    deepest promotion in the system. ADR-004 warned this "becomes live the moment
    this helper is written". Retiring a strategy while claiming it was promoted
    must be refused.
    """
    with pytest.raises(ValueError):
        a_review(
            outcome=ReviewOutcome.PROMOTE,
            stage_at_review=StrategyLifecycle.PRODUCTION,
            resulting_stage=StrategyLifecycle.RETIRED,
            justification="Claiming a retirement is a promotion.",
        )


def test_a_retirement_recorded_as_a_demotion_is_refused():
    """The other half of the same trap: RETIRED is not the bottom of the ladder
    either. It is not on the ladder at all."""
    with pytest.raises(ValueError):
        a_review(
            outcome=ReviewOutcome.DEMOTE,
            stage_at_review=StrategyLifecycle.PRODUCTION,
            resulting_stage=StrategyLifecycle.RETIRED,
            justification="Claiming a retirement is a demotion.",
        )


# ------------------------------- ADR-009 rules 6 and 7: confidence and re-sizing


def test_the_confidence_adjustment_is_recorded():
    """`ReviewTemplate.md:37-43` lists Increase / Decrease / No Change as a
    decision the review makes, so it is recorded as one."""
    artifact = a_review(confidence_adjustment=ConfidenceAdjustment.DECREASE)

    assert review_fields(artifact)["confidence_adjustment"] == "Decrease"


def test_a_resulting_confidence_outside_zero_to_one_is_refused():
    with pytest.raises(ValueError):
        a_review(resulting_confidence=42.0)


def test_the_resulting_confidence_is_optional():
    """ADR-009 rule 6. Deciding to adjust and producing the new version of the
    subject are separate acts, and the second may not have happened yet."""
    assert review_fields(a_review())["resulting_confidence"] is None


def test_a_demotion_records_without_a_resizing_note():
    """ADR-009 rule 7, and it is a ruling rather than an omission.

    `Capital_Authority.md` holds that capital preservation wins whenever conflict
    exists, and ADR-004 concludes: "If step 2 cannot be completed, step 1 still
    stands." A required re-sizing field would let a missing input block the
    recording of a demotion, which is the exact reading ADR-004 forbids.
    """
    artifact = a_review(
        outcome=ReviewOutcome.DEMOTE,
        stage_at_review=StrategyLifecycle.PRODUCTION,
        resulting_stage=StrategyLifecycle.LIMITED_CAPITAL,
        justification="Drawdown breach in two consecutive months.",
    )

    assert review_fields(artifact)["resizing_note"] is None


def test_a_resizing_note_is_recorded_when_supplied():
    artifact = a_review(
        outcome=ReviewOutcome.DEMOTE,
        stage_at_review=StrategyLifecycle.PRODUCTION,
        resulting_stage=StrategyLifecycle.LIMITED_CAPITAL,
        justification="Drawdown breach in two consecutive months.",
        resizing_note="Re-sized to 40% of the limited-capital ceiling.",
    )

    assert "40%" in review_fields(artifact)["resizing_note"]


# --------------------------------------- ADR-009 rule 8: prose stays in content


def test_the_template_prose_sections_are_carried_without_being_typed_fields():
    """ADR-009 rule 8. Nothing computes on them, and `Artifact` fields are inside
    the integrity hash, so every field added is permanent."""
    artifact = a_review(
        sections={
            "Observed Behavior": "Tracked the benchmark within 40bps.",
            "Risk Assessment": "No limit breached.",
        }
    )

    fields = review_fields(artifact)
    assert fields["sections"]["Risk Assessment"] == "No limit breached."
    assert "Observed Behavior" not in {f.name for f in dataclasses.fields(artifact)}


# ---------------------------------------------- ADR-009 rule 9: it can be read back


def test_a_stored_review_can_be_read_back_and_still_verifies():
    """The two halves of ADR-009 joined: rule 1 makes the decision durable, rule
    9 makes it legible.

    This is most of why the record exists. A decision that survives to disk but
    cannot be read back cannot inform the next review, and the reviewer who needs
    it most is the one asking "what did we decide last time, and why?"
    """
    from framework.artifacts.serializer import ArtifactSerializer

    original = a_review(
        outcome=ReviewOutcome.DEMOTE,
        stage_at_review=StrategyLifecycle.PRODUCTION,
        resulting_stage=StrategyLifecycle.LIMITED_CAPITAL,
        justification="Drawdown outside limits in two consecutive months.",
        confidence_adjustment=ConfidenceAdjustment.DECREASE,
        resulting_confidence=0.35,
    )

    serializer = ArtifactSerializer()
    restored = serializer.load(serializer.dump(original))

    assert ArtifactIntegrity.verify_hash(restored)
    assert review_fields(restored) == review_fields(original)
    assert review_fields(restored)["justification"].startswith("Drawdown outside")
    assert review_fields(restored)["resulting_confidence"] == 0.35


def test_reading_review_fields_off_something_that_is_not_a_review_is_refused():
    """A silent fallback is indistinguishable from a real answer — the failure
    that left the dashboard reporting no priorities at all for two sessions."""
    from framework.artifacts.enums import ArtifactType as Type
    from framework.artifacts.factory import ArtifactFactory

    report = ArtifactFactory().create(
        identifier="RPT-0217", title="Drawdown", artifact_type=Type.REPORT
    )

    with pytest.raises(ValueError):
        review_fields(report)


def test_an_artifact_typed_review_but_not_built_here_is_refused():
    """Type alone does not make a record. An empty REVIEW artifact carries no
    decision, and returning a dict of `None`s would let it pass for one."""
    from framework.artifacts.factory import ArtifactFactory

    hollow = ArtifactFactory().create(
        identifier=REVIEW_ID, title="Review", artifact_type=ArtifactType.REVIEW
    )

    with pytest.raises(ValueError):
        review_fields(hollow)


# ------------------------- F-019: outcomes that the stage movement alone cannot catch
#
# `reports/review/2026-09-04-review.md:89` (F-019). In both cases below the
# movement is legal on the ladder, so only the outcome check stands between the
# caller and a signed record that says the opposite of what happened to the
# money. Disabling either check left the whole suite green. Owner ruling:
# `docs/OwnerDecisions.md` Part 21.


def test_a_retirement_that_lands_on_a_capital_stage_is_refused():
    """`Promotion Review -> Micro Capital` is a legal climb. Recorded as `Retire`,
    it would be a signed record of a retirement that funds the strategy."""
    with pytest.raises(ValueError, match="a retirement ends at"):
        a_review(
            outcome=ReviewOutcome.RETIRE,
            stage_at_review=StrategyLifecycle.PROMOTION_REVIEW,
            resulting_stage=StrategyLifecycle.MICRO_CAPITAL,
        )


def test_a_promotion_that_descends_the_ladder_is_refused():
    """`Production -> Paper Trading` is a legal demotion. Recorded as `Promote`,
    it would be a signed record of a promotion that took capital away."""
    with pytest.raises(ValueError, match="a promotion climbs the ladder"):
        a_review(
            outcome=ReviewOutcome.PROMOTE,
            stage_at_review=StrategyLifecycle.PRODUCTION,
            resulting_stage=StrategyLifecycle.PAPER_TRADING,
        )
