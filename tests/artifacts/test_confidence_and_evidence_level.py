"""Artifact-level confidence and the derived evidence grade. ADR-005.

Confidence existed only on `EvidenceRecord`, which is frozen, so the figure four
documents require Belay to revise was fixed at creation. `Knowledge/Schema.md`
also requires an artifact-level evidence grade, which had no home at all.
"""

from dataclasses import replace
from datetime import datetime, timezone

import pytest

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import ArtifactType, EvidenceLevel
from framework.artifacts.evidence import EvidenceRecord
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.validator import ArtifactValidator

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _evidence(level: EvidenceLevel, confidence: float = 0.5) -> EvidenceRecord:
    return EvidenceRecord.create(
        source=f"source-{level.value}",
        methodology="unit test",
        level=level,
        confidence=confidence,
        provenance="test",
        timestamp=FIXED_TIME,
    )


def _artifact(**kwargs):
    kwargs.setdefault("created", FIXED_TIME)
    kwargs.setdefault("updated", FIXED_TIME)
    return ArtifactFactory().create(
        identifier="RPT-0001",
        title="Max drawdown",
        artifact_type=ArtifactType.REPORT,
        **kwargs,
    )


# ------------------------------------------------- the derived evidence grade


def test_the_strongest_grade_wins_not_the_weakest():
    """`Evidence_Standards.md`: "Hypotheses do not invalidate production evidence."

    Taking the minimum would let a single Level D record drag down an artifact
    carrying Level A, which is that sentence's exact prohibition.
    """
    artifact = _artifact(
        evidence=(
            _evidence(EvidenceLevel.RESEARCH),
            _evidence(EvidenceLevel.LIVE),
            _evidence(EvidenceLevel.RESEARCH),
        )
    )

    assert artifact.evidence_level is EvidenceLevel.LIVE


@pytest.mark.parametrize(
    "levels,expected",
    [
        ((EvidenceLevel.RESEARCH,), EvidenceLevel.RESEARCH),
        ((EvidenceLevel.RESEARCH, EvidenceLevel.HISTORICAL), EvidenceLevel.HISTORICAL),
        ((EvidenceLevel.HISTORICAL, EvidenceLevel.PAPER), EvidenceLevel.PAPER),
        ((EvidenceLevel.PAPER, EvidenceLevel.LIVE), EvidenceLevel.LIVE),
    ],
)
def test_every_rung_of_the_hierarchy_orders_correctly(levels, expected):
    artifact = _artifact(evidence=tuple(_evidence(level) for level in levels))

    assert artifact.evidence_level is expected


def test_an_unevidenced_artifact_has_no_grade():
    """None, not D. Defaulting would make unevidenced read as hypothesis."""
    assert _artifact().evidence_level is None


def test_the_grade_cannot_be_supplied():
    """A caller-provided grade is an assertion nobody checked."""
    with pytest.raises(ValueError, match="evidence_level is derived"):
        _artifact(evidence_level=EvidenceLevel.LIVE)


def test_a_forged_grade_is_refused_by_the_validator():
    """`Artifact()` can be called directly, so the validator re-derives.

    Without this an artifact could claim Level A while carrying nothing but
    hypotheses — and that claim is what a promotion gate reads.
    """
    forged = ArtifactIntegrity.sign(
        Artifact(
            id="RPT-0001",
            title="Max drawdown",
            type=ArtifactType.REPORT,
            evidence=(_evidence(EvidenceLevel.RESEARCH),),
            evidence_level=EvidenceLevel.LIVE,
        )
    )

    with pytest.raises(ValueError, match="does not match the"):
        ArtifactValidator().validate(forged)


# ------------------------------------------------------------------ confidence


def test_confidence_is_revised_by_producing_a_new_version():
    """ADR-005: `Knowledge/Versioning.md` forbids overwriting a version.

    The prior figure survives, which is the point — the history of an estimate
    is the evidence trail.
    """
    original = _artifact(version="1.0.0", confidence=0.4)
    revised = _artifact(version="1.0.1", confidence=0.7)

    assert original.confidence == 0.4
    assert revised.confidence == 0.7


def test_confidence_defaults_to_none_rather_than_a_figure():
    """0.5 would be a fabricated estimate nothing distinguishes from a real one."""
    assert _artifact().confidence is None
    assert ArtifactValidator().validate(_artifact()) is True


@pytest.mark.parametrize("value", [42.0, -3.0, 1.01])
def test_confidence_outside_zero_to_one_is_refused_at_creation(value):
    with pytest.raises(ValueError, match="probability between 0 and 1"):
        _artifact(confidence=value)


def test_confidence_outside_zero_to_one_is_refused_by_the_validator():
    """The factory is not the only construction path, so the gate checks too."""
    forged = ArtifactIntegrity.sign(
        Artifact(
            id="RPT-0001",
            title="Max drawdown",
            type=ArtifactType.REPORT,
            confidence=42.0,
        )
    )

    with pytest.raises(ValueError, match="probability between 0 and 1"):
        ArtifactValidator().validate(forged)


@pytest.mark.parametrize("value", [0.0, 1.0])
def test_the_bounds_themselves_are_legal(value):
    assert _artifact(confidence=value).confidence == value


# --------------------------------------------- the signature covers the fields


def test_altering_confidence_breaks_the_signature():
    """The figure a promotion gate reads must be inside the hash.

    Left outside it, a strategy's confidence could be raised from 0.3 to 0.9
    while verification still returned True — the same defect that let authorship
    and dates be rewritten before 2026-07-26.
    """
    artifact = _artifact(confidence=0.3)
    tampered = replace(artifact, confidence=0.9)

    assert ArtifactIntegrity.verify_hash(artifact) is True
    assert ArtifactIntegrity.verify_hash(tampered) is False


def test_altering_tags_or_summary_breaks_the_signature():
    artifact = _artifact(tags=("drawdown",), summary="Max drawdown for Q1.")

    assert ArtifactIntegrity.verify_hash(replace(artifact, tags=())) is False
    assert ArtifactIntegrity.verify_hash(replace(artifact, summary="")) is False


def test_tags_and_summary_round_trip():
    artifact = _artifact(tags=("drawdown", "risk"), summary="Max drawdown for Q1.")

    assert artifact.tags == ("drawdown", "risk")
    assert artifact.summary == "Max drawdown for Q1."
    assert ArtifactValidator().validate(artifact) is True
