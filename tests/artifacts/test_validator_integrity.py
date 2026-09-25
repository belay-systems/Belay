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


# --------------------------------------- F-019: the stage checks, each on its own
#
# `reports/review/2026-09-04-review.md:89` (F-019). Disabling either check below
# left the whole suite green, because no test built a STRATEGY without a stage or
# a REPORT with one; `ArtifactFactory` refuses neither, so this is the only check. These
# build the artifact directly and sign it, so the validator is the only thing
# that can refuse it. Owner ruling: `docs/OwnerDecisions.md` Part 21.


def _signed(**fields) -> Artifact:
    from framework.artifacts.integrity import ArtifactIntegrity

    return ArtifactIntegrity.sign(Artifact(**fields))


def test_a_signed_strategy_with_no_stage_fails_validation():
    """`strategies/Registry.md`: every strategy exists in exactly one lifecycle
    stage. A strategy with none cannot be placed on the ladder at all."""
    artifact = _signed(id="STRAT-0001", title="Test", type=ArtifactType.STRATEGY)

    with pytest.raises(ValueError, match="must carry a strategy_stage"):
        ArtifactValidator().validate(artifact)


def test_a_signed_report_claiming_a_capital_stage_fails_validation():
    """A report has no capital stage. One claiming `PRODUCTION` asserts something
    untrue of itself, and it would be signed and storable."""
    from framework.artifacts.enums import StrategyLifecycle

    artifact = _signed(
        id="RPT-0001",
        title="Test",
        type=ArtifactType.REPORT,
        strategy_stage=StrategyLifecycle.PRODUCTION,
    )

    with pytest.raises(ValueError, match="Only STRATEGY artifacts carry a strategy_stage"):
        ArtifactValidator().validate(artifact)
