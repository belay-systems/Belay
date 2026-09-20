from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import ArtifactType
from framework.artifacts.integrity import ArtifactIntegrity


def test_integrity_hash_is_deterministic():
    artifact = Artifact(id="RPT-0001", title="Test", type=ArtifactType.REPORT)

    first = ArtifactIntegrity.calculate_hash(artifact)
    second = ArtifactIntegrity.calculate_hash(artifact)

    assert first == second


def test_integrity_detects_modified_artifact():
    artifact = Artifact(id="RPT-0001", title="Test", type=ArtifactType.REPORT)
    tampered = Artifact(id="RPT-0001", title="Changed", type=ArtifactType.REPORT)

    artifact_hash = ArtifactIntegrity.calculate_hash(artifact)

    assert artifact_hash != ArtifactIntegrity.calculate_hash(tampered)
