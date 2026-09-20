"""An unsigned artifact must not pass validation.

This is what closes the P1 finding. Signing in ArtifactFactory narrows the hole;
rejecting unsigned artifacts at the validator means one cannot reach a promotion
gate however it was built.
"""

from dataclasses import replace

import pytest

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import ArtifactType
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.validator import ArtifactValidator


def test_unsigned_artifact_fails_validation():
    # Constructed directly, bypassing the factory. This previously passed.
    artifact = Artifact(id="RPT-0001", title="Test", type=ArtifactType.REPORT)

    assert artifact.integrity_hash is None
    with pytest.raises(ValueError, match="unsigned"):
        ArtifactValidator().validate(artifact)


def test_signed_artifact_passes_validation():
    artifact = ArtifactFactory().create(
        identifier="RPT-0001",
        title="Test",
        artifact_type=ArtifactType.REPORT,
    )

    assert ArtifactValidator().validate(artifact) is True


def test_tampered_artifact_fails_validation():
    artifact = ArtifactFactory().create(
        identifier="RPT-0001",
        title="Test",
        artifact_type=ArtifactType.REPORT,
        content=(("value", 1),),
    )

    # Altered after signing. The hash still travels with it, but no longer matches.
    forged = replace(artifact, content=(("value", 999),))

    with pytest.raises(ValueError, match="mismatch"):
        ArtifactValidator().validate(forged)


def test_replace_does_not_resign_an_artifact():
    """Guards the reason signing lives in the factory rather than in Artifact.

    If Artifact signed itself on construction, dataclasses.replace() would hand
    every altered copy a fresh valid signature and tamper detection would stop
    working silently. The record keeps the hash it was given.
    """
    artifact = ArtifactFactory().create(
        identifier="RPT-0001",
        title="Test",
        artifact_type=ArtifactType.REPORT,
        content=(("value", 1),),
    )

    forged = replace(artifact, content=(("value", 999),))

    assert forged.integrity_hash == artifact.integrity_hash
