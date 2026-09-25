from datetime import date, datetime, timezone

import pytest

from framework.artifacts.enums import ArtifactType, DeliverableType, EvidenceLevel
from framework.artifacts.integrity import ArtifactIntegrity
from framework.metrics.drawdown import drawdown_artifact, max_drawdown
from framework.metrics.reporting import Disclosure, SamplePeriod

# Peak is 120. The lowest subsequent point is 60, a 50% fall.
# The later dip to 80 is only 33%, so it must not win.
SERIES = [100.0, 120.0, 90.0, 110.0, 60.0, 80.0]
EXPECTED = 0.5

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

# ADR-011 rule 13. This function used to take a bare `source` string, because it
# predates both ADR-010 and ADR-011 and was the only metric in the repository.
# It now goes through the same helper as every other metric, so the four things
# `Validation/Backtesting.md` requires a backtest to document are recorded here
# too rather than on the metrics written after it.
DISCLOSURE = Disclosure(
    assumptions="No transaction costs, no slippage, no financing charges.",
    data_source="unit test fixture, supplied by hand",
    # ADR-013 rule 7: two dates, not prose. Six consecutive trading days for the
    # six observations below. The series is still synthetic — `known_limitations`
    # says so — but a window is now a window rather than a sentence about one.
    sample_period=SamplePeriod(start=date(2024, 1, 2), end=date(2024, 1, 9)),
    known_limitations="The series carries no provenance and describes no real instrument.",
)


def test_max_drawdown_matches_hand_calculation():
    assert max_drawdown(SERIES) == pytest.approx(EXPECTED)


def test_rising_series_has_no_drawdown():
    assert max_drawdown([100.0, 110.0, 120.0]) == 0.0


def test_single_observation_has_no_drawdown():
    assert max_drawdown([100.0]) == 0.0


def test_deepest_decline_wins_over_a_later_shallower_one():
    # Falls 50% early, then only 20% from a lower peak. The 50% must survive.
    assert max_drawdown([100.0, 50.0, 100.0, 80.0]) == pytest.approx(0.5)


def test_empty_series_is_rejected():
    with pytest.raises(ValueError, match="empty"):
        max_drawdown([])


def test_non_positive_price_is_rejected():
    with pytest.raises(ValueError, match="non-positive"):
        max_drawdown([100.0, 0.0, 50.0])


def _artifact():
    return drawdown_artifact(
        identifier="RPT-0001",
        title="Max drawdown, sample series",
        prices=SERIES,
        disclosure=DISCLOSURE,
        timestamp=FIXED_TIME,
    )


def test_artifact_carries_the_computed_value():
    content = dict(_artifact().content)
    assert content["metric"] == "max_drawdown"
    assert content["value"] == pytest.approx(EXPECTED)
    assert content["observations"] == len(SERIES)


def test_artifact_is_signed_and_verifies():
    artifact = _artifact()
    assert artifact.integrity_hash is not None
    assert ArtifactIntegrity.verify_hash(artifact) is True


def test_tampering_with_the_value_breaks_verification():
    artifact = _artifact()
    from dataclasses import replace

    forged = replace(
        artifact,
        content=(("metric", "max_drawdown"), ("value", 0.01), ("observations", 6)),
    )
    assert ArtifactIntegrity.verify_hash(forged) is False


def test_artifact_over_a_hand_built_disclosure_is_graded_research():
    """F-033, owner ruling Part 35: Level D unless the series came from a fetch.

    Asserted `HISTORICAL` until 2026-09-25, on a disclosure built in this file.
    """
    evidence = _artifact().evidence
    assert len(evidence) == 1
    assert evidence[0].level is EvidenceLevel.RESEARCH
    assert evidence[0].hash


def test_artifact_type_and_lifecycle_default_to_report_draft():
    artifact = _artifact()
    assert artifact.type is ArtifactType.REPORT
    # A freshly computed metric has not been promoted anywhere yet.
    assert artifact.lifecycle.value == "Draft"


def test_identical_inputs_produce_an_identical_hash():
    assert _artifact().integrity_hash == _artifact().integrity_hash


def test_different_prices_produce_a_different_hash():
    other = drawdown_artifact(
        identifier="RPT-0001",
        title="Max drawdown, sample series",
        prices=[100.0, 95.0],
        disclosure=DISCLOSURE,
        timestamp=FIXED_TIME,
    )
    assert other.integrity_hash != _artifact().integrity_hash


# ---------------------------------------------------- ADR-011 rule 13 migration


def test_the_drawdown_artifact_names_itself_a_backtest_report():
    """ADR-010 landed after this module was written, so drawdown artifacts were
    untyped `REPORT`s indistinguishable from every other report in Belay."""
    assert _artifact().deliverable is DeliverableType.BACKTEST_REPORTS


def test_the_drawdown_artifact_carries_the_four_required_disclosures():
    """ADR-011 rule 13, and the reason the migration was not deferred.

    `framework/metrics/drawdown.py` is described in `docs/HANDOFF.md` as "the
    only worked example and the pattern to follow". Leaving the one worked
    example as the one component that does not follow the rule would have made
    the rule optional in practice on the day it was ratified.
    """
    content = dict(_artifact().content)

    assert content["assumptions"] == DISCLOSURE.assumptions
    assert content["data_source"] == DISCLOSURE.data_source
    assert content["sample_period_start"] == DISCLOSURE.sample_period.start.isoformat()
    assert content["sample_period_end"] == DISCLOSURE.sample_period.end.isoformat()
    assert content["known_limitations"] == DISCLOSURE.known_limitations


def test_the_drawdown_artifact_cannot_be_built_without_disclosing():
    """The `source=` string this function used to take is gone rather than
    deprecated. A second accepted signature would leave the old pattern legal,
    which is what `AGENTS.md` means by parallel implementations."""
    with pytest.raises(TypeError):
        drawdown_artifact(
            identifier="RPT-0001",
            title="Max drawdown, sample series",
            prices=SERIES,
            source="unit test fixture",
        )
