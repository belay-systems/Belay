"""Relationship types. Eleven are documented; every string used to be legal.

`framework/artifacts/relationships.py` declared a `Relationship` dataclass that
nothing imported, and which was the only unfrozen model in `framework/`. The
vocabulary it existed to carry lived only in prose, so `Artifact.relationships`
accepted anything at all.
"""

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from framework.artifacts.enums import ArtifactType
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.relationships import (
    RELATIONSHIP_TYPES,
    Relationship,
    RelationshipType,
)
from framework.artifacts.validator import ArtifactValidator

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _artifact(**kwargs):
    kwargs.setdefault("created", FIXED_TIME)
    kwargs.setdefault("updated", FIXED_TIME)
    return ArtifactFactory().create(
        identifier="RPT-0001",
        title="Max drawdown",
        artifact_type=ArtifactType.REPORT,
        **kwargs,
    )


def test_every_documented_type_is_accepted():
    artifact = _artifact(
        relationships=tuple(
            (member.value, ("RPT-0002",)) for member in RelationshipType
        )
    )

    assert ArtifactValidator().validate(artifact) is True


def test_an_undocumented_relationship_type_is_refused():
    """A typo used to succeed, creating a twelfth kind of edge.

    Nothing else would ever match it, so the relationship existed without
    connecting anything — the failure mode Knowledge/Relationships.md is
    guarding against when it says relationships create intelligence.
    """
    artifact = _artifact(relationships=(("Cites", ("RPT-0002",)),))

    with pytest.raises(ValueError, match="Unknown relationship type"):
        ArtifactValidator().validate(artifact)


def test_the_documented_capitalisation_is_the_one_that_counts():
    """`supports` and `Supports` would be two unconnected edges, not one."""
    artifact = _artifact(relationships=(("supports", ("RPT-0002",)),))

    with pytest.raises(ValueError, match="Unknown relationship type"):
        ArtifactValidator().validate(artifact)


def test_a_malformed_relationship_entry_is_refused():
    artifact = _artifact(relationships=(("Supports",),))

    with pytest.raises(ValueError, match="Malformed relationship entry"):
        ArtifactValidator().validate(artifact)


def test_an_artifact_may_have_no_relationships():
    assert ArtifactValidator().validate(_artifact()) is True


def test_relationship_is_frozen_like_every_other_model():
    """It was the only unfrozen dataclass in framework/.

    An edge could be repointed after construction while the artifact that
    described it kept the integrity hash computed before the change.
    """
    edge = Relationship(
        source="RPT-0001",
        target="RPT-0002",
        relationship=RelationshipType.SUPPORTS,
    )

    with pytest.raises(FrozenInstanceError):
        edge.target = "RPT-0003"


def test_the_vocabulary_constant_is_derived_from_the_enum():
    """One source of truth, so the two cannot fall out of step."""
    assert RELATIONSHIP_TYPES == {member.value for member in RelationshipType}
