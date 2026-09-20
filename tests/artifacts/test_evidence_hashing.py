"""Evidence hashing: one shared primitive, timezone-aware timestamps."""

from dataclasses import replace
from datetime import datetime, timezone

import pytest

from framework.artifacts.enums import EvidenceLevel
from framework.artifacts.evidence import EvidenceRecord
from framework.artifacts.primitives import canonical_digest

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

# Captured from the previous implementation, which ran its own SHA256 and JSON
# serialization inside EvidenceRecord.create. Routing evidence through the
# shared primitive in framework/artifacts/primitives.py must not change any
# existing hash. If this value moves, historical evidence stopped verifying.
PINNED_DIGEST = "97cffee5cc6407e9241d5fe21b831ce98c7f7dd3952f52f409458edfea9758c8"


def _record(**overrides):
    fields = {
        "source": "baseline",
        "methodology": "pin",
        "level": EvidenceLevel.HISTORICAL,
        "confidence": 1.0,
        "provenance": "6 observations",
        "timestamp": FIXED_TIME,
    }
    fields.update(overrides)
    return EvidenceRecord.create(**fields)


def test_evidence_hash_is_unchanged_by_the_shared_primitive():
    assert _record().hash == PINNED_DIGEST


def test_evidence_and_artifact_hashing_share_one_implementation():
    record = _record()

    assert canonical_digest(record.canonical_payload()) == record.hash


def test_evidence_hash_is_deterministic():
    assert _record().hash == _record().hash


def test_changed_evidence_produces_a_different_hash():
    assert _record(confidence=0.5).hash != _record().hash


def test_evidence_verifies_against_its_own_contents():
    assert _record().verify() is True


def test_forged_evidence_hash_is_detected():
    # The validator only checks the hash field is non-empty, so a forged record
    # passes it. verify() is what catches this.
    forged = replace(_record(), confidence=0.01)

    assert forged.verify() is False


def test_empty_evidence_hash_does_not_verify():
    assert replace(_record(), hash="").verify() is False


def test_naive_timestamp_is_rejected():
    # No timezone means nothing in the value says which clock produced it, and
    # the timestamp goes straight into the hash.
    with pytest.raises(ValueError, match="timezone-aware"):
        _record(timestamp=datetime(2026, 1, 1))


@pytest.mark.parametrize("confidence", [42.0, -3.0, 1.5, -0.0001])
def test_confidence_outside_zero_to_one_is_rejected(confidence):
    """constitution/Operational_Constraints.md: confidence is probabilistic.

    42.0 and -3.0 were both accepted and stored before 2026-07-26.
    """
    with pytest.raises(ValueError, match="probability"):
        _record(confidence=confidence)


@pytest.mark.parametrize("confidence", [0.0, 0.5, 1.0])
def test_valid_probabilities_are_accepted(confidence):
    assert _record(confidence=confidence).confidence == confidence


def test_default_timestamp_is_timezone_aware():
    assert _record(timestamp=None).timestamp.tzinfo is not None
