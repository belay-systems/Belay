"""`ArtifactSerializer.load()` — ADR-009 rule 9.

The serializer implemented `dump` and nothing else, so an artifact could be
written and never read back. A decision record that cannot be read back cannot
inform the next review, which is most of why it exists, and `Knowledge/Search.md:3`
builds retrieval entirely on reading stored metadata.

**The acceptance test is the round trip through integrity, not through equality.**
A loader that reconstructs every field but produces a different canonical payload
has silently broken every signature it touched. Field equality would not catch a
value that renders to the same text and hashes differently — which is exactly what
a timezone dropped in transit does.

Written before the implementation and run against the unchanged code first.
"""

from __future__ import annotations

import dataclasses
from datetime import datetime, timezone

import pytest

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import (
    ArtifactLifecycle,
    ArtifactType,
    EvidenceLevel,
    StrategyLifecycle,
)
from framework.artifacts.evidence import EvidenceRecord
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.serializer import ArtifactSerializer
from framework.artifacts.validator import ArtifactValidator

MOMENT = datetime(2026, 7, 31, 9, 30, tzinfo=timezone.utc)


def an_artifact(**overrides) -> Artifact:
    evidence = EvidenceRecord.create(
        source="daily closes, 2019-2026",
        methodology="peak-to-trough maximum drawdown",
        level=EvidenceLevel.HISTORICAL,
        confidence=1.0,
        provenance="1760 observations",
        timestamp=MOMENT,
    )

    arguments = dict(
        identifier="RPT-0217",
        title="Maximum drawdown",
        artifact_type=ArtifactType.REPORT,
        evidence=(evidence,),
        tags=("drawdown", "risk"),
        summary="Worst peak-to-trough decline over the observed series.",
        confidence=0.8,
        lifecycle=ArtifactLifecycle.REVIEW,
        content=(("metric", "max_drawdown"), ("value", 0.2534), ("observations", 1760)),
        metadata=(("desk", "research"),),
        relationships=(("Derived From", ("STRAT-0001",)),),
        created=MOMENT,
        updated=MOMENT,
        parent_hash="abc123",
    )
    arguments.update(overrides)
    return ArtifactFactory().create(**arguments)


def round_trip(artifact: Artifact) -> Artifact:
    serializer = ArtifactSerializer()
    return serializer.load(serializer.dump(artifact))


# ------------------------------------------------------------ the acceptance test


def test_dump_then_load_preserves_the_signature():
    """The whole point. If this fails, storage has been silently destroying
    signatures and every stored artifact is unverifiable."""
    restored = round_trip(an_artifact())

    assert ArtifactIntegrity.verify_hash(restored)


def test_a_loaded_artifact_still_passes_validation():
    assert ArtifactValidator().validate(round_trip(an_artifact()))


def test_a_loaded_strategy_keeps_its_capital_stage():
    """`strategy_stage` is inside the hash and is the field a promotion gate
    reads. A stage that came back as a bare string would not be comparable to a
    `StrategyLifecycle` member at all.

    Built the way a strategy at LIMITED_CAPITAL actually comes to exist: born at
    IDEA, then moved and re-signed. The factory refuses to mint one already
    standing at a later stage — `constitution/Paper_First_Capital_Doctrine.md:5`,
    "every strategy begins with zero capital" — so the earlier version of this
    test, which asked the factory for LIMITED_CAPITAL directly, was exercising a
    creation path that should never have existed. The round trip is what is
    under test here, and a stage that was earned still has to survive it.
    """
    born = an_artifact(
        identifier="STRAT-0001",
        title="Covered premium",
        artifact_type=ArtifactType.STRATEGY,
        strategy_stage=StrategyLifecycle.IDEA,
    )
    promoted = ArtifactIntegrity.sign(
        dataclasses.replace(born, strategy_stage=StrategyLifecycle.LIMITED_CAPITAL)
    )

    restored = round_trip(promoted)

    assert restored.strategy_stage is StrategyLifecycle.LIMITED_CAPITAL
    assert ArtifactIntegrity.verify_hash(restored)


# ----------------------------------------------------------------- field fidelity


def test_the_loader_restores_every_field_the_artifact_declares():
    """Pinned against `dataclasses.fields`, not against a transcribed list.

    `load()` is a second place that has to know the artifact schema. A field
    added to `Artifact` and not to the loader would be silently dropped on read,
    and a list copied into this test would go stale exactly as the schema field
    count did.
    """
    original = an_artifact()
    restored = round_trip(original)

    for field in dataclasses.fields(Artifact):
        assert getattr(restored, field.name) == getattr(original, field.name), (
            f"{field.name} did not survive the round trip"
        )


def test_enums_come_back_as_enums():
    restored = round_trip(an_artifact())

    assert restored.type is ArtifactType.REPORT
    assert restored.lifecycle is ArtifactLifecycle.REVIEW
    assert restored.evidence_level is EvidenceLevel.HISTORICAL


def test_timestamps_come_back_timezone_aware():
    """A naive timestamp is not reproducible evidence — nothing in it says which
    clock produced it, which is why `utc_now()` exists and why naive evidence
    timestamps are rejected outright.

    This is also the likeliest way to break the signature: `canonical_payload`
    hashes `created.isoformat()`, and a dropped timezone changes that string
    while leaving every field looking correct.
    """
    restored = round_trip(an_artifact())

    assert restored.created.tzinfo is not None
    assert restored.updated.tzinfo is not None
    assert restored.created == MOMENT


def test_a_stored_timestamp_without_a_timezone_is_refused():
    """Not assumed to be UTC.

    A file can be placed by hand, and older PyYAML releases returned naive UTC
    from a native timestamp. Assuming would produce a working-looking artifact
    whose signature no longer covers its own timestamp — a silent fallback, which
    is the failure mode this repository has been bitten by three times. Refusing
    is loud.
    """
    serializer = ArtifactSerializer()
    text = serializer.dump(an_artifact()).replace(MOMENT.isoformat(), "2026-07-31T09:30:00")

    with pytest.raises(ValueError):
        serializer.load(text)


def test_tuples_do_not_come_back_as_lists():
    """`Artifact` declares tuples, and it is frozen so that its contents cannot
    be edited after signing. A list would make the payload mutable again."""
    restored = round_trip(an_artifact())

    assert isinstance(restored.tags, tuple)
    assert isinstance(restored.evidence, tuple)
    assert isinstance(restored.content, tuple)
    assert all(isinstance(entry, tuple) for entry in restored.content)
    assert isinstance(restored.relationships[0][1], tuple)


def test_evidence_records_come_back_verifiable():
    """The artifact hash covers only each record's `hash` field, so a mangled
    evidence timestamp would not fail `verify_hash` — it fails here instead."""
    restored = round_trip(an_artifact())

    assert all(record.verify() for record in restored.evidence)
    assert restored.evidence[0].level is EvidenceLevel.HISTORICAL


def test_an_absent_optional_field_stays_absent():
    """`None` means "not assessed" and must not come back as a value."""
    restored = round_trip(an_artifact(confidence=None, parent_hash=None))

    assert restored.confidence is None
    assert restored.parent_hash is None


# ------------------------------------------------------------- loading is not signing


def test_loading_a_tampered_artifact_does_not_resign_it():
    """`Artifact` keeps whatever hash it is given.

    Signing on load would hand every altered file a fresh valid signature and
    turn tamper detection off — the same reasoning that keeps signing out of the
    constructor, guarded by `test_replace_does_not_resign_an_artifact`.
    """
    serializer = ArtifactSerializer()
    text = serializer.dump(an_artifact()).replace(
        "Worst peak-to-trough decline", "Best peak-to-trough decline"
    )

    restored = serializer.load(text)

    assert restored.summary.startswith("Best")
    assert not ArtifactIntegrity.verify_hash(restored)
    with pytest.raises(ValueError):
        ArtifactValidator().validate(restored)


def test_an_unsigned_artifact_loads_and_still_fails_the_gate():
    """Reading is not vouching. The loader returns what is on disk; the
    validator is what refuses it."""
    serializer = ArtifactSerializer()
    unsigned = dataclasses.replace(an_artifact(), integrity_hash=None)

    restored = serializer.load(serializer.dump(unsigned))

    assert restored.integrity_hash is None
    with pytest.raises(ValueError):
        ArtifactValidator().validate(restored)
