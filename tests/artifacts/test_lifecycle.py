"""Lifecycle transitions for both governed subjects. See ADR-003."""

import pytest

from framework.artifacts.enums import ArtifactLifecycle, StrategyLifecycle
from framework.artifacts.validator import ArtifactValidator

# constitution/Paper_First_Capital_Doctrine.md, reproduced exactly in README.md.
DOCTRINE_STAGES = [
    "Idea",
    "Research",
    "Validation",
    "Paper Trading",
    "Promotion Review",
    "Micro Capital",
    "Limited Capital",
    "Production",
]

# Knowledge/ArtifactLifecycle.md.
ARTIFACT_STAGES = [
    "Draft",
    "Review",
    "Approved",
    "Active",
    "Archived",
    "Historical",
]

# The maturity ladder: the eight doctrine stages in order, with RETIRED removed.
#
# RETIRED is declared last in StrategyLifecycle — index 8, above PRODUCTION at 7
# — but the doctrine places retirement outside the sequence rather than at the
# end of it. Comparing positions over list(StrategyLifecycle) would therefore
# score every retirement as the deepest promotion in the system. RETIRED is
# removed before any position is compared, never classified by one. ADR-004.
LADDER = [stage for stage in StrategyLifecycle if stage is not StrategyLifecycle.RETIRED]


# The forward moves only. The ten legal demotions are pinned as a set in
# tests/test_governance_conformance.py, against the table in ADR-004.
@pytest.mark.parametrize(
    "current,target",
    [
        (StrategyLifecycle.IDEA, StrategyLifecycle.RESEARCH),
        (StrategyLifecycle.RESEARCH, StrategyLifecycle.VALIDATION),
        (StrategyLifecycle.VALIDATION, StrategyLifecycle.PAPER_TRADING),
        (StrategyLifecycle.PAPER_TRADING, StrategyLifecycle.PROMOTION_REVIEW),
        (StrategyLifecycle.PROMOTION_REVIEW, StrategyLifecycle.MICRO_CAPITAL),
        (StrategyLifecycle.MICRO_CAPITAL, StrategyLifecycle.LIMITED_CAPITAL),
        (StrategyLifecycle.LIMITED_CAPITAL, StrategyLifecycle.PRODUCTION),
        (StrategyLifecycle.PRODUCTION, StrategyLifecycle.RETIRED),
    ],
)
def test_valid_strategy_transitions(current, target):
    assert ArtifactValidator().validate_transition(current, target)


@pytest.mark.parametrize(
    "current,target",
    [
        (StrategyLifecycle.PRODUCTION, StrategyLifecycle.IDEA),
        (StrategyLifecycle.RETIRED, StrategyLifecycle.PRODUCTION),
        # Skipping the micro capital tier: an expanded allocation without ever
        # having traded a minimal one.
        (StrategyLifecycle.PROMOTION_REVIEW, StrategyLifecycle.LIMITED_CAPITAL),
        (StrategyLifecycle.PAPER_TRADING, StrategyLifecycle.MICRO_CAPITAL),
    ],
)
def test_invalid_strategy_transitions(current, target):
    with pytest.raises(ValueError):
        ArtifactValidator().validate_transition(current, target)


@pytest.mark.parametrize("stage", list(StrategyLifecycle))
def test_retirement_is_reachable_from_every_stage(stage):
    """Paper_First_Capital_Doctrine.md: retirement may occur at any stage.

    Strategy_Retirement.md lists six causes, several of which — persistent
    underperformance, invalid assumptions, excessive drawdown — are most likely
    to appear well before production.
    """
    if stage is StrategyLifecycle.RETIRED:
        pytest.skip("already retired")

    assert ArtifactValidator().validate_transition(stage, StrategyLifecycle.RETIRED)


@pytest.mark.parametrize(
    "current,target",
    [
        (ArtifactLifecycle.DRAFT, ArtifactLifecycle.REVIEW),
        (ArtifactLifecycle.REVIEW, ArtifactLifecycle.APPROVED),
        (ArtifactLifecycle.APPROVED, ArtifactLifecycle.ACTIVE),
        (ArtifactLifecycle.ACTIVE, ArtifactLifecycle.ARCHIVED),
        (ArtifactLifecycle.ARCHIVED, ArtifactLifecycle.HISTORICAL),
    ],
)
def test_valid_artifact_transitions(current, target):
    assert ArtifactValidator().validate_transition(current, target)


@pytest.mark.parametrize(
    "current,target",
    [
        (ArtifactLifecycle.HISTORICAL, ArtifactLifecycle.DRAFT),
        (ArtifactLifecycle.DRAFT, ArtifactLifecycle.APPROVED),
        (ArtifactLifecycle.ACTIVE, ArtifactLifecycle.REVIEW),
    ],
)
def test_invalid_artifact_transitions(current, target):
    with pytest.raises(ValueError):
        ArtifactValidator().validate_transition(current, target)


def test_lifecycles_cannot_be_mixed():
    """An artifact cannot be moved into a capital stage.

    This is the defect ADR-003 exists to prevent, made unrepresentable: before
    the split, a drawdown report's legal future states included Micro Capital.
    """
    with pytest.raises(ValueError, match="different lifecycles"):
        ArtifactValidator().validate_transition(
            ArtifactLifecycle.DRAFT, StrategyLifecycle.RESEARCH
        )


def test_strategy_lifecycle_matches_the_doctrine():
    """The constitution defines the sequence; the enum must follow it."""
    values = [stage.value for stage in StrategyLifecycle]

    assert values[: len(DOCTRINE_STAGES)] == DOCTRINE_STAGES
    assert values[-1] == "Retired"


def test_artifact_lifecycle_matches_knowledge_documentation():
    assert [stage.value for stage in ArtifactLifecycle] == ARTIFACT_STAGES


def test_forward_path_walks_every_stage_in_order():
    """Following forward moves from Idea must visit all eight doctrine stages.

    strategies/Lifecycle.md: "Strategies never skip stages."

    This used to follow the only available move, and could say so. Before
    ADR-004 every non-RETIRED successor was a promotion, so filtering RETIRED
    left exactly one step, and PRODUCTION's row emptied to end the walk. The
    table now carries demotions as well, so the step is chosen by ladder
    position rather than by being the last one standing.

    The walk is bounded by the number of stages. An unbounded version of this
    test does not fail against a bad table — it hangs, silently and without
    output, because RETIRED is the only row with no successors and it is
    filtered out before the walk can reach it.
    """
    validator = ArtifactValidator()
    walked = [StrategyLifecycle.IDEA]

    for _ in range(len(LADDER)):
        here = LADDER.index(walked[-1])
        forward = [
            stage
            for stage in validator.STRATEGY_TRANSITIONS[walked[-1]]
            if stage is not StrategyLifecycle.RETIRED and LADDER.index(stage) > here
        ]
        if not forward:
            break
        assert len(forward) == 1, f"{walked[-1].value} has more than one forward move"
        walked.append(forward[0])

    assert [stage.value for stage in walked] == DOCTRINE_STAGES


def test_artifact_path_walks_every_stage_in_order():
    validator = ArtifactValidator()
    walked = [ArtifactLifecycle.DRAFT]

    while nxt := validator.ARTIFACT_TRANSITIONS[walked[-1]]:
        walked.append(nxt[0])

    assert [stage.value for stage in walked] == ARTIFACT_STAGES
