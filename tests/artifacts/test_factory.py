"""ArtifactFactory is the sanctioned creation path: everything it emits is signed."""

from datetime import datetime, timezone

import pytest

from framework.artifacts.enums import ArtifactType, StrategyLifecycle
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.validator import ArtifactValidator

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _create(**kwargs):
    # Timestamps are pinned because they are part of the hash. Two artifacts
    # built a microsecond apart are different artifacts and hash differently,
    # which is the point of covering `created` — see canonical_payload.
    kwargs.setdefault("created", FIXED_TIME)
    kwargs.setdefault("updated", FIXED_TIME)
    return ArtifactFactory().create(
        identifier="RPT-0001",
        title="Test",
        artifact_type=ArtifactType.REPORT,
        **kwargs,
    )


def test_factory_signs_what_it_creates():
    artifact = _create()

    assert artifact.integrity_hash is not None
    assert ArtifactIntegrity.verify_hash(artifact) is True


def test_factory_rejects_a_caller_supplied_hash():
    # A hash handed in from outside is a signature nobody checked. The factory
    # computes it or refuses, rather than trusting a value it did not produce.
    with pytest.raises(ValueError, match="integrity_hash"):
        _create(integrity_hash="deadbeef")


def test_identical_inputs_produce_an_identical_hash():
    assert _create().integrity_hash == _create().integrity_hash


def test_different_content_produces_a_different_hash():
    first = _create(content=(("value", 1),))
    second = _create(content=(("value", 2),))

    assert first.integrity_hash != second.integrity_hash


@pytest.mark.parametrize(
    "field,forged",
    [
        ("author", "Somebody Else"),
        ("created", datetime(2020, 1, 1, tzinfo=timezone.utc)),
        ("updated", datetime(2020, 1, 1, tzinfo=timezone.utc)),
        ("parent_hash", "0" * 64),
    ],
)
def test_rewriting_provenance_breaks_verification(field, forged):
    """Authorship, timestamps and lineage are inside the signature.

    Until 2026-07-26 none of these were covered. An artifact's author could be
    changed and its creation date moved by years while verify_hash still
    returned True — the signature proved what an artifact said, but not who
    produced it or when. constitution/Governance.md requires every artifact to
    possess identifier, version, author, date and status.
    """
    from dataclasses import replace

    artifact = _create(author="Research Dept")
    assert ArtifactIntegrity.verify_hash(artifact) is True

    assert ArtifactIntegrity.verify_hash(replace(artifact, **{field: forged})) is False


def test_same_content_at_a_different_time_is_a_different_artifact():
    early = _create(created=FIXED_TIME, updated=FIXED_TIME)
    late = _create(
        created=datetime(2026, 6, 1, tzinfo=timezone.utc),
        updated=datetime(2026, 6, 1, tzinfo=timezone.utc),
    )

    assert early.integrity_hash != late.integrity_hash


def test_factory_passes_through_other_fields():
    artifact = _create(author="Research", version="2.0.0")

    assert artifact.author == "Research"
    assert artifact.version == "2.0.0"
    # Signing must not disturb what the caller asked for.
    assert ArtifactIntegrity.verify_hash(artifact) is True


# ------------------------------------------------------- capital is not granted


def _create_strategy(**kwargs):
    kwargs.setdefault("created", FIXED_TIME)
    kwargs.setdefault("updated", FIXED_TIME)
    return ArtifactFactory().create(
        identifier="STRAT-0001",
        title="Covered premium",
        artifact_type=ArtifactType.STRATEGY,
        **kwargs,
    )


@pytest.mark.parametrize(
    "stage",
    [stage for stage in StrategyLifecycle if stage is not StrategyLifecycle.IDEA],
)
def test_a_strategy_cannot_be_born_past_idea(stage):
    """constitution/Paper_First_Capital_Doctrine.md:5 — "Every strategy begins
    with zero capital. No exceptions."

    The guard was on movement, not on birth. `validate_transition` refuses
    IDEA -> Micro Capital and IDEA -> Validation, but the factory passed
    `strategy_stage` straight through and `_validate_lifecycle` checked only
    that it *was* a `StrategyLifecycle`, never *which* — so a strategy signed
    into existence at PRODUCTION validated True. It would carry no VALIDATION
    artifact and no PAPER_TRADING history, because it never occupied those
    stages, and the REVIEW records that would expose this are not missing so
    much as nonexistent: no review ever happened. Downstream, the promotion
    gate and the demotion floor read the stage as established fact and size
    real money against it.

    Parametrized over the whole enum rather than PRODUCTION alone: RETIRED is
    also unreachable at birth, because a strategy must exist before it can be
    retired.
    """
    with pytest.raises(ValueError, match="stage"):
        _create_strategy(strategy_stage=stage)


def test_a_strategy_may_be_born_at_idea():
    """The other half of the refusal. IDEA is zero capital, which is where the
    doctrine says every strategy starts — the factory must still mint one."""
    artifact = _create_strategy(strategy_stage=StrategyLifecycle.IDEA)

    assert artifact.strategy_stage is StrategyLifecycle.IDEA
    assert ArtifactValidator().validate(artifact) is True
    assert ArtifactIntegrity.verify_hash(artifact) is True
