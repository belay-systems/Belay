"""The review decision record — ADR-009.

Nothing in Belay recorded that a review happened. `strategies/ReviewTemplate.md`
specified the form of one and no code held it, so a review that decided to hold a
strategy at Limited Capital was indistinguishable in the system's state from no
review having taken place — while `constitution/Governance.md:11` requires that
all decisions be documented.

Three ratified obligations were waiting on this one component, and nothing else
in the repository had that property:

- **ADR-004 rule 4** — a demotion requires written justification. The transition
  table can rule that a move is legal; it cannot know whether a reason was
  written. This module is where that check finally lives.
- **ADR-004's re-sizing step** — a demotion triggers a fresh allocation
  determination, performed by the reviewer in prose until a position-sizing layer
  exists. `resizing_note` is where that prose goes.
- **ADR-008** — `Remain Current Stage` is an outcome rather than a lifecycle
  transition, to be recorded wherever review decisions are recorded.

The record is an Artifact of type REVIEW rather than a new kind of object. An
Artifact arrives signed, versioned and append-only, and a decision record that
can be altered after the fact documents nothing. `ArtifactType.REVIEW` and the
`REV` identifier prefix both already existed, so no enum member is added and the
open `ArtifactType` finding is routed around rather than answered by accident.

**Rule 5 below is not the promotion/demotion/retirement classifier ADR-004
defers.** That classifier derives a *name* from a transition and has to cope with
inputs this never sees — `Draft -> Review -> Approved` is not a promotion, a
demotion or a retirement, and `ArtifactLifecycle` still has no vocabulary for what
it is. This is the inverse and strictly narrower: given an outcome the reviewer
*declared* and a stage pair they *declared*, are the two consistent? It only ever
sees `StrategyLifecycle` values. No general `classify(current, target)` is
exported, and ADR-004's follow-up stays open.
"""

from __future__ import annotations

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import (
    STRATEGY_LADDER,
    ArtifactType,
    ConfidenceAdjustment,
    ReviewOutcome,
    StrategyLifecycle,
)
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.primitives import is_semantic_version
from framework.artifacts.validator import ArtifactValidator
from framework.identifiers import validate as validate_identifier

# The keys under which the typed review fields are carried in the artifact's
# `content`. Named here so `review_artifact` and `review_fields` cannot drift
# apart — a record that can be written under one spelling and read under another
# is exactly the failure a decision record exists to prevent.
FIELDS = (
    "subject_id",
    "subject_version",
    "reviewer",
    "outcome",
    "stage_at_review",
    "resulting_stage",
    "justification",
    "confidence_adjustment",
    "resulting_confidence",
    "resizing_note",
)


def review_artifact(
    identifier: str,
    subject_id: str,
    subject_version: str,
    reviewer: str,
    outcome: ReviewOutcome,
    stage_at_review: StrategyLifecycle,
    resulting_stage: StrategyLifecycle,
    justification: str,
    confidence_adjustment: ConfidenceAdjustment,
    resulting_confidence: float | None = None,
    resizing_note: str | None = None,
    sections: dict[str, str] | None = None,
    **kwargs,
) -> Artifact:
    """Record a review decision as a signed Artifact.

    `identifier` is the review's own (`REV-NNNN`). `subject_id` and
    `subject_version` name what was reviewed: under ADR-005 a confidence revision
    produces a new version, so which version was in front of the reviewer is the
    difference between a decision about the artifact they read and one about an
    artifact that has changed underneath them since.

    `stage_at_review` and `resulting_stage` are both required even though one is
    redundant for `REMAIN_CURRENT_STAGE`. The redundancy is the point: it is what
    makes the outcome checkable against the movement.

    `sections` carries the six prose sections of `ReviewTemplate.md` — Operational
    Summary, Observed Behavior, Expected Behavior, Performance Summary, Risk
    Assessment, Regime Compatibility. ADR-009 rule 8 keeps them as content rather
    than typed fields: nothing computes on them, and `Artifact` fields are inside
    the integrity hash, so every field added is permanent.

    Raises ValueError if the record would not be a valid decision. Every check
    below refuses at construction rather than at validation, because an
    unjustified decision is not an artifact with a defect — it is not a decision.
    """
    validate_identifier(subject_id)

    # `ArtifactRepository.save()` already refuses a version that is not
    # MAJOR.MINOR.PATCH, because append-only storage could never correct such a
    # filename afterwards. A review naming `v2` cannot be matched against any
    # stored version, so the field would record a decision about nothing.
    if not is_semantic_version(subject_version):
        raise ValueError(
            f"subject_version {subject_version!r} is not a semantic version; "
            "it cannot be matched against any stored version of the subject"
        )

    # constitution/Governance.md:19-25 requires every artifact to possess an
    # author. Nothing checks the name against a roster: ADR-009 rule 10 — no
    # document in the repository names reviewer roles, and inventing one would be
    # writing doctrine rather than implementing it.
    if not reviewer.strip():
        raise ValueError("reviewer is required; a decision has someone who made it")

    # ADR-009 rule 4, and the first enforcement of ADR-004 rule 4 since it was
    # ratified. Required for every outcome, not only the unfavourable ones:
    # PromotionCriteria.md:33 and :35, Governance.md:15, and
    # StrategyPromotion.md:37 — "Every decision requires written justification."
    # Whitespace is not a justification.
    if not justification.strip():
        raise ValueError(
            f"{outcome.value} requires written justification. "
            "workflows/Monthly/StrategyPromotion.md:37: "
            "'Every decision requires written justification.'"
        )

    if resulting_confidence is not None and not 0.0 <= resulting_confidence <= 1.0:
        raise ValueError(
            "resulting_confidence must be a probability between 0 and 1, "
            f"got {resulting_confidence}"
        )

    _check_outcome_matches_movement(outcome, stage_at_review, resulting_stage)

    recorded = {
        "subject_id": subject_id,
        "subject_version": subject_version,
        "reviewer": reviewer.strip(),
        "outcome": outcome.value,
        "stage_at_review": stage_at_review.value,
        "resulting_stage": resulting_stage.value,
        "justification": justification.strip(),
        "confidence_adjustment": confidence_adjustment.value,
        "resulting_confidence": resulting_confidence,
        "resizing_note": resizing_note,
    }

    content = tuple((key, recorded[key]) for key in FIELDS)
    for heading, prose in (sections or {}).items():
        content += ((f"section:{heading}", prose),)

    # No strategy_stage. The review is not the strategy, and ArtifactValidator
    # refuses a capital stage on anything that is not a STRATEGY artifact: a
    # record claiming a stage would assert something untrue of itself. The stages
    # under review are statements about the subject and live in content.
    return ArtifactFactory().create(
        identifier=identifier,
        title=f"Review of {subject_id} {subject_version}: {outcome.value}",
        artifact_type=ArtifactType.REVIEW,
        author=reviewer.strip(),
        content=content,
        **kwargs,
    )


def review_fields(artifact: Artifact) -> dict:
    """Read a review decision back out of its artifact.

    This is the half of ADR-009 rule 9 that makes the record useful rather than
    merely durable: a decision that cannot be read back cannot inform the next
    review. `sections` comes back as a mapping under its own key.

    Raises ValueError if `artifact` is not a review record, rather than returning
    a dict of `None`s — a silent fallback is indistinguishable from a real answer,
    which this repository has already been bitten by.
    """
    if artifact.type is not ArtifactType.REVIEW:
        raise ValueError(
            f"{artifact.id} is a {artifact.type.value} artifact, not a review record"
        )

    content = dict(artifact.content)
    missing = [key for key in FIELDS if key not in content]
    if missing:
        raise ValueError(
            f"{artifact.id} is typed REVIEW but carries no {', '.join(missing)}; "
            "it was not built by review_artifact()"
        )

    fields = {key: content[key] for key in FIELDS}
    fields["sections"] = {
        key[len("section:") :]: value
        for key, value in content.items()
        if key.startswith("section:")
    }
    return fields


def _check_outcome_matches_movement(
    outcome: ReviewOutcome,
    stage_at_review: StrategyLifecycle,
    resulting_stage: StrategyLifecycle,
) -> None:
    """Refuse a declared outcome that disagrees with the declared stage change.

    ADR-009 rule 5. The order of these branches is load-bearing.

    **RETIRED is handled first, before any ladder position is taken.** It is
    declared at index 8 in `StrategyLifecycle`, above `PRODUCTION` at 7, so a
    bare ordinal comparison reads every retirement as the deepest promotion in
    the system. ADR-004 flagged this and warned it "becomes live the moment this
    helper is written" — this is that moment. `STRATEGY_LADDER` has `RETIRED`
    removed, so `.index()` raises rather than lying if one slips through, but the
    branch order is what stops it reaching there.
    """
    if outcome is ReviewOutcome.RETIRE:
        if resulting_stage is not StrategyLifecycle.RETIRED:
            raise ValueError(
                f"a retirement ends at {StrategyLifecycle.RETIRED.value}, "
                f"not {resulting_stage.value}"
            )
        return

    if resulting_stage is StrategyLifecycle.RETIRED:
        raise ValueError(
            f"{resulting_stage.value} is not a stage of maturity — the doctrine "
            f"places retirement outside the sequence — so a move to it cannot be "
            f"recorded as {outcome.value}. The outcome is Retire."
        )

    if outcome is ReviewOutcome.REMAIN_CURRENT_STAGE:
        if resulting_stage is not stage_at_review:
            raise ValueError(
                f"{outcome.value} records no movement, but this review moves "
                f"{stage_at_review.value} -> {resulting_stage.value}"
            )
        return

    # Both remaining outcomes are movements, so a self-transition is neither.
    # ADR-008: Remain is the absence of movement and the transition table holds
    # no X -> X row, so validate_transition would reject this anyway — but the
    # clearer error is that the wrong outcome was named.
    if resulting_stage is stage_at_review:
        raise ValueError(
            f"{outcome.value} is a movement, but this review leaves the strategy "
            f"at {stage_at_review.value}. The outcome is "
            f"{ReviewOutcome.REMAIN_CURRENT_STAGE.value}."
        )

    climbed = STRATEGY_LADDER.index(resulting_stage) > STRATEGY_LADDER.index(
        stage_at_review
    )

    if outcome is ReviewOutcome.PROMOTE and not climbed:
        raise ValueError(
            f"a promotion climbs the ladder, but {stage_at_review.value} -> "
            f"{resulting_stage.value} descends it"
        )

    if outcome is ReviewOutcome.DEMOTE and climbed:
        raise ValueError(
            f"a demotion descends the ladder, but {stage_at_review.value} -> "
            f"{resulting_stage.value} climbs it"
        )

    # Legality is the transition table's question, not this module's. A promotion
    # that skips a stage and a demotion below the PAPER_TRADING floor are both
    # refused there, and asking rather than re-deciding keeps one table
    # authoritative — ADR-004 rules the ten demotions, and a second opinion here
    # would eventually disagree with it.
    ArtifactValidator().validate_transition(stage_at_review, resulting_stage)
