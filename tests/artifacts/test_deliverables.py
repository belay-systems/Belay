"""ADR-010: `ArtifactType` is a coarse type with a constrained subtype.

The finding was open from 2026-07-26 and routed around three times. It rested on
an estimate — "roughly twenty deliverables" — that nobody had counted. Counted on
2026-07-31 across all 31 departmental and workflow documents: eleven declare
deliverables under an explicit heading, 34 entries, 25 distinct. Twenty-four
after `Knowledge Update` is excluded as an effect rather than an artifact.

**The subtype is an enum, never free text.** That is the whole risk of this shape:
a free string would re-open the exact hole the finding was raised about, where an
orphaned draft passed `artifact_type="UniverseReport"` and nothing refused it.

Written before the implementation and run against the unchanged code first.
"""

from __future__ import annotations

import dataclasses
from datetime import datetime, timezone

import pytest

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import (
    DELIVERABLE_ARTIFACT_TYPE,
    ArtifactType,
    DeliverableType,
    StrategyLifecycle,
)
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.serializer import ArtifactSerializer
from framework.artifacts.validator import ArtifactValidator

MOMENT = datetime(2026, 7, 31, 9, 30, tzinfo=timezone.utc)


def a_deliverable(**overrides) -> Artifact:
    arguments = dict(
        identifier="RPT-0217",
        title="Universe report",
        artifact_type=ArtifactType.REPORT,
        deliverable=DeliverableType.UNIVERSE_REPORT,
        content=(("value", 1),),
        created=MOMENT,
        updated=MOMENT,
    )
    arguments.update(overrides)
    return ArtifactFactory().create(**arguments)


# --------------------------------------------------------------- rule 9


def test_every_documented_deliverable_resolves_to_a_pair():
    """ADR-010 rule 9, and the reason the old watcher could not be strengthened.

    The question the finding asked — closed enum that must grow, or coarse enum
    plus a subtype — determined what this test should assert. A closed enum meant
    "every deliverable has an `ArtifactType` member"; the ruling means "every
    deliverable resolves to a `(ArtifactType, DeliverableType)` pair". Those are
    different tests, and writing one before the ruling would have been guessing.
    """
    for deliverable in DeliverableType:
        assert deliverable in DELIVERABLE_ARTIFACT_TYPE, (
            f"{deliverable.value} has no ArtifactType"
        )
        assert isinstance(DELIVERABLE_ARTIFACT_TYPE[deliverable], ArtifactType)


def test_the_mapping_covers_the_vocabulary_and_nothing_else():
    """Total and closed. A member with no type, or a type keyed by something that
    is not a member, would both make the pair in rule 9 unreliable."""
    assert set(DELIVERABLE_ARTIFACT_TYPE) == set(DeliverableType)


# ------------------------------------------------- the subtype is constrained


def test_an_unknown_deliverable_is_refused():
    """The hole this finding was raised about.

    `artifact_type="UniverseReport"` passed once because nothing constrained the
    value. A free-text subtype would have made that legal rather than fixing it,
    which is why ADR-010 rule 3 requires an enum.
    """
    forged = dataclasses.replace(a_deliverable(), deliverable="UniverseReport")

    with pytest.raises(ValueError):
        ArtifactValidator().validate(forged)


def test_a_deliverable_must_match_its_artifact_type():
    """ADR-010 rule 9 makes the pair meaningful, so a mismatched pair is a defect.

    A universe report declared as a `STRATEGY` is not a typo the system should
    keep — `ArtifactType` is what a promotion gate reads first.
    """
    mismatched = dataclasses.replace(
        a_deliverable(), type=ArtifactType.STRATEGY, deliverable=DeliverableType.UNIVERSE_REPORT
    )

    with pytest.raises(ValueError):
        ArtifactValidator().validate(mismatched)


def test_an_artifact_need_not_be_a_deliverable():
    """Rule 7. Most artifacts are not workflow deliverables — a strategy
    specification is not one and a review record is not one. `None` means "not a
    documented deliverable", which is a real state rather than an unset field."""
    artifact = a_deliverable(
        identifier="STRAT-0001",
        title="Covered premium",
        artifact_type=ArtifactType.STRATEGY,
        # Required of every STRATEGY independently of ADR-010 —
        # `strategies/Registry.md`: "Every strategy exists in exactly one
        # lifecycle stage." IDEA because the factory is the birth path and a
        # strategy is born at zero capital; the stage is incidental to what
        # this test is about, which is `deliverable=None`.
        strategy_stage=StrategyLifecycle.IDEA,
        deliverable=None,
    )

    assert artifact.deliverable is None
    assert ArtifactValidator().validate(artifact)


# ------------------------------------------------------------- inside the hash


def test_the_deliverable_is_covered_by_the_signature():
    """Rule 8, and the reasoning ADR-005 applied to `confidence`.

    Every field a governance gate reads must be inside the signature. A promotion
    gate that accepts a critique report must not accept an artifact whose
    `deliverable` was changed to `CRITIQUE_REPORT` after it was signed.
    """
    artifact = a_deliverable()
    forged = dataclasses.replace(artifact, deliverable=DeliverableType.CRITIQUE_REPORT)

    assert ArtifactIntegrity.verify_hash(artifact)
    assert not ArtifactIntegrity.verify_hash(forged)


def test_the_deliverable_survives_a_round_trip_as_an_enum():
    """`load()` is a second place that has to know the schema. ADR-009 recorded
    that a field added to one and not the other is dropped in silence — and a
    bare string would not compare equal to a `DeliverableType` member."""
    serializer = ArtifactSerializer()
    artifact = a_deliverable()

    restored = serializer.load(serializer.dump(artifact))

    assert restored.deliverable is DeliverableType.UNIVERSE_REPORT
    assert ArtifactIntegrity.verify_hash(restored)


# ------------------------------------------------------ what the ruling excludes


def test_effects_are_not_deliverables():
    """Rule 5, stated where it is applied rather than left as a silent filter.

    `Knowledge Update` appears in three Deliverables lists, but
    `workflows/WorkflowEngine.md` makes "Update Knowledge" a step in the execution
    model of every workflow, and `Events/StrategyPromotion.md` lists `Repository
    Update` and `Knowledge Graph Update` as workflow steps. They are effects on
    stored state, not documents produced. Giving them members would make this enum
    name things that are not artifacts.
    """
    names = {member.value for member in DeliverableType}

    for effect in ("Knowledge Update", "Repository Update", "Knowledge Graph Update"):
        assert effect not in names, f"{effect} is an effect, not a deliverable"
