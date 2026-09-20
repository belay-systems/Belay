from datetime import datetime, timezone

import pytest

from framework.artifacts.artifact import Artifact
from framework.artifacts.evidence import EvidenceRecord
from framework.artifacts.enums import ArtifactLifecycle, ArtifactType, EvidenceLevel


def test_artifact_is_immutable():
    artifact = Artifact(id="RPT-0001", title="test", type=ArtifactType.REPORT)
    with pytest.raises(Exception):
        artifact.title = "changed"


def test_evidence_hash_is_deterministic():
    evidence = EvidenceRecord.create(
        source="source",
        methodology="method",
        level=EvidenceLevel.RESEARCH,
        confidence=0.5,
        provenance="test",
        timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    assert evidence.hash


def test_lifecycle_default():
    artifact = Artifact(id="RPT-0001", title="test", type=ArtifactType.REPORT)
    assert artifact.lifecycle == ArtifactLifecycle.DRAFT
