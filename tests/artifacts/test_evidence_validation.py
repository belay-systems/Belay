from datetime import datetime, timezone

import pytest

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import ArtifactType, EvidenceLevel
from framework.artifacts.evidence import EvidenceRecord
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.validator import ArtifactValidator


def test_valid_evidence_record_passes_validation():
    evidence = EvidenceRecord.create(
        source="test",
        methodology="unit test",
        level=EvidenceLevel.RESEARCH,
        confidence=0.9,
        provenance="pytest",
        timestamp=datetime.now(timezone.utc),
    )

    # Built through the factory, which signs. An artifact assembled by hand is
    # unsigned and no longer passes validation — see test_validator.py.
    artifact = ArtifactFactory().create(
        identifier="RPT-0001",
        title="Evidence Test",
        artifact_type=ArtifactType.REPORT,
        evidence=(evidence,),
    )

    assert ArtifactValidator().validate(artifact)


def test_missing_evidence_hash_fails_validation():
    evidence = EvidenceRecord(
        source="test",
        methodology="unit test",
        level=EvidenceLevel.RESEARCH,
        confidence=0.9,
        provenance="pytest",
        timestamp=datetime.now(timezone.utc),
        hash="",
    )

    artifact = Artifact(
        id="RPT-0001",
        title="Evidence Test",
        type=ArtifactType.REPORT,
        evidence=(evidence,),
    )

    with pytest.raises(ValueError):
        ArtifactValidator().validate(artifact)
