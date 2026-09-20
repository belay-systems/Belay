"""Sharpe and Sortino. ADR-011 rules 1, 6, 7 and 8.

Sharpe asks: for every unit of swing a strategy put you through, how much return
above cash did it hand back? Sortino asks the same question counting only the
*downward* swing, because upside volatility is not a risk anyone needs
compensating for.

Neither is computable from `Validation/Backtesting.md` alone. The document names
both on lines 17 and 19 and defines neither, so the risk-free rate and the
target return are arguments with no defaults. That is ADR-011 rule 1, and the
tests at the bottom of each section assert it against the signature rather than
trusting a docstring to say it.

This module is `framework/metrics/risk_adjusted.py` on purpose:
`scripts/status.py:50` names exactly that path as the component expected to make
`Risk-adjusted returns` — one of the seven constitutional promotion criteria —
computable. The filename is part of the deliverable.
"""

from __future__ import annotations

import math
import statistics
from datetime import date, datetime, timezone

import pytest

from framework.artifacts.integrity import ArtifactIntegrity
from framework.metrics.reporting import Disclosure, SamplePeriod
from framework.metrics.risk_adjusted import (
    sharpe_artifact,
    sharpe_ratio,
    sortino_artifact,
    sortino_ratio,
)
from framework.metrics.volatility import downside_deviation

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

DISCLOSURE = Disclosure(
    assumptions="No transaction costs, no slippage, no financing charges.",
    data_source="unit test fixture, supplied by hand",
    # ADR-013 rule 7: two dates, not prose. Five consecutive trading days.
    sample_period=SamplePeriod(start=date(2024, 1, 2), end=date(2024, 1, 8)),
    known_limitations="The series carries no provenance and describes no real instrument.",
)

# Mean 0.008 per period. Sample standard deviation sqrt(0.00037) ~ 0.019235.
# Downside deviation about zero is exactly 0.01 — see test_volatility.py.
RETURNS = (0.01, -0.02, 0.03, 0.00, 0.02)
PERIODS = 252

# The annual rate whose per-period equivalent is exactly the mean return:
# 0.008 * 252. Used to drive both numerators to zero, which is the sharpest
# available check that the annual-to-period conversion happens at all.
MEAN_MATCHING_ANNUAL_RATE = 0.008 * PERIODS


# --------------------------------------------------------------------- Sharpe


def test_sharpe_is_annualized_excess_return_over_annualized_volatility():
    """ADR-011 rule 6, stated as arithmetic rather than as prose."""
    expected = (statistics.fmean(RETURNS) * PERIODS) / (
        statistics.stdev(RETURNS) * math.sqrt(PERIODS)
    )

    assert sharpe_ratio(RETURNS, risk_free_rate=0.0, periods_per_year=PERIODS) == (
        pytest.approx(expected)
    )


def test_the_risk_free_rate_is_supplied_as_an_annual_rate():
    """ADR-011 rule 6: the rate is annual and is divided by `periods_per_year`
    inside the function.

    This is where a silent factor-of-252 error would live, and it would be
    almost invisible: a daily rate of 0.04 instead of an annual one understates
    the excess return by about ten percentage points a year, and the result is
    still a plausible-looking number.

    Driven to an exact zero rather than compared to a second computed figure. An
    annual rate of 0.008 * 252 is exactly the mean per-period return, so the
    excess return is zero and so is Sharpe — which can only happen if the
    division by 252 took place.
    """
    assert sharpe_ratio(
        RETURNS,
        risk_free_rate=MEAN_MATCHING_ANNUAL_RATE,
        periods_per_year=PERIODS,
    ) == pytest.approx(0.0)


def test_a_higher_risk_free_rate_lowers_sharpe():
    """The economic content: a strategy is only worth its risk if it beats cash."""
    at_zero = sharpe_ratio(RETURNS, risk_free_rate=0.0, periods_per_year=PERIODS)
    at_four = sharpe_ratio(RETURNS, risk_free_rate=0.04, periods_per_year=PERIODS)

    assert at_four < at_zero


def test_a_series_with_no_volatility_is_refused_rather_than_scored():
    """ADR-011 rule 5 applied at the ratio.

    Dividing by a zero denominator would raise `ZeroDivisionError` at best and
    return `inf` at worst — and an infinite Sharpe reads at a promotion gate as
    the best strategy ever measured, when what actually happened is that the
    ratio is undefined.
    """
    with pytest.raises(ValueError, match="no volatility"):
        sharpe_ratio((0.01, 0.01, 0.01), risk_free_rate=0.0, periods_per_year=PERIODS)


@pytest.mark.parametrize("returns", [(), (0.01,)])
def test_sharpe_rejects_fewer_than_two_observations(returns):
    with pytest.raises(ValueError, match="at least two"):
        sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=PERIODS)


def test_sharpe_has_no_default_risk_free_rate():
    """ADR-011 rule 1, and the single most likely way to get this session wrong.

    Zero is the industry's most common convention and it would be perfectly
    defensible — but applied silently it is indistinguishable, at the gate, from
    a rate somebody chose. ADR-005 rule 4 refused the same shape for
    `confidence` defaulting to 0.5.
    """
    with pytest.raises(TypeError):
        sharpe_ratio(RETURNS)

    with pytest.raises(TypeError):
        sharpe_ratio(RETURNS, risk_free_rate=0.0)


# -------------------------------------------------------------------- Sortino


def test_sortino_divides_by_downside_deviation_not_by_volatility():
    """ADR-011 rule 7. The denominator is 0.01, not sqrt(0.00037)."""
    expected = (statistics.fmean(RETURNS) * PERIODS) / (0.01 * math.sqrt(PERIODS))

    assert sortino_ratio(RETURNS, target_return=0.0, periods_per_year=PERIODS) == (
        pytest.approx(expected)
    )


def test_sortino_exceeds_sharpe_when_the_downside_is_the_smaller_half():
    """A direct consequence of the two denominators, and a check that the
    functions are not accidentally the same function.

    This series swings 0.019 in total and only 0.01 of that is downward, so
    ignoring the upside makes it look better — which is the correction Sortino
    exists to make.
    """
    sharpe = sharpe_ratio(RETURNS, risk_free_rate=0.0, periods_per_year=PERIODS)
    sortino = sortino_ratio(RETURNS, target_return=0.0, periods_per_year=PERIODS)

    assert sortino > sharpe


def test_the_target_return_is_used_in_the_numerator_as_well():
    """ADR-011 rule 8, and it is a real trap rather than a hypothetical one.

    The common mistake is to measure excess return against the risk-free rate
    while measuring downside against the target. That produces a number which is
    neither a Sortino ratio nor a Sharpe ratio, and it gets labelled as one.

    Same zero-driving technique as the risk-free-rate test: an annual target of
    0.008 * 252 is exactly the mean per-period return, so the numerator vanishes
    and the ratio is zero. If the numerator used a risk-free rate of zero
    instead, it would be positive and large.
    """
    assert sortino_ratio(
        RETURNS,
        target_return=MEAN_MATCHING_ANNUAL_RATE,
        periods_per_year=PERIODS,
    ) == pytest.approx(0.0)

    # The denominator is genuinely non-zero at that target, so the zero above is
    # the numerator vanishing rather than an error being swallowed.
    assert downside_deviation(RETURNS, target=0.008) > 0.0


def test_a_series_that_never_falls_short_is_refused_rather_than_scored():
    """Zero downside deviation makes the ratio undefined, not infinite.

    This case is not exotic: any strategy that beat its target in every single
    period lands here, and those are exactly the ones a promotion gate is most
    likely to be looking at.
    """
    with pytest.raises(ValueError, match="never fell short"):
        sortino_ratio((0.01, 0.02, 0.03), target_return=0.0, periods_per_year=PERIODS)


@pytest.mark.parametrize("returns", [(), (0.01,)])
def test_sortino_rejects_fewer_than_two_observations(returns):
    with pytest.raises(ValueError, match="at least two"):
        sortino_ratio(returns, target_return=0.0, periods_per_year=PERIODS)


def test_sortino_has_no_default_target_return():
    """ADR-011 rule 1. `Validation/Backtesting.md:19` says `Sortino` and stops."""
    with pytest.raises(TypeError):
        sortino_ratio(RETURNS)

    with pytest.raises(TypeError):
        sortino_ratio(RETURNS, target_return=0.0)


# ------------------------------------------------------------- as artifacts


def test_the_sharpe_artifact_records_the_rate_it_was_computed_against():
    """ADR-011 rule 2, and the single most important thing on a Sharpe artifact.

    A Sharpe of 1.4 at a risk-free rate of 0% and a Sharpe of 1.4 at 4% describe
    two different strategies. A promotion gate reading the number without the
    rate is reading a figure, not a claim.
    """
    artifact = sharpe_artifact(
        identifier="RPT-0003",
        title="Sharpe ratio, sample series",
        returns=RETURNS,
        risk_free_rate=0.04,
        periods_per_year=PERIODS,
        disclosure=DISCLOSURE,
        timestamp=FIXED_TIME,
    )
    content = dict(artifact.content)

    assert content["metric"] == "sharpe_ratio"
    assert content["risk_free_rate"] == pytest.approx(0.04)
    assert content["periods_per_year"] == PERIODS
    assert content["observations"] == len(RETURNS)
    assert content["value"] == pytest.approx(
        sharpe_ratio(RETURNS, risk_free_rate=0.04, periods_per_year=PERIODS)
    )
    assert ArtifactIntegrity.verify_hash(artifact) is True


def test_the_sortino_artifact_records_its_target_return():
    artifact = sortino_artifact(
        identifier="RPT-0004",
        title="Sortino ratio, sample series",
        returns=RETURNS,
        target_return=0.0,
        periods_per_year=PERIODS,
        disclosure=DISCLOSURE,
        timestamp=FIXED_TIME,
    )
    content = dict(artifact.content)

    assert content["metric"] == "sortino_ratio"
    assert content["target_return"] == pytest.approx(0.0)
    assert content["periods_per_year"] == PERIODS
    assert ArtifactIntegrity.verify_hash(artifact) is True


def test_two_sharpe_artifacts_at_different_rates_do_not_share_a_hash():
    """The parameters are inside the signature, so the two are distinguishable
    records rather than the same record twice. Same series, same timestamp,
    same title — only the rate differs."""
    common = {
        "identifier": "RPT-0003",
        "title": "Sharpe ratio, sample series",
        "returns": RETURNS,
        "periods_per_year": PERIODS,
        "disclosure": DISCLOSURE,
        "timestamp": FIXED_TIME,
    }

    at_zero = sharpe_artifact(**common, risk_free_rate=0.0)
    at_four = sharpe_artifact(**common, risk_free_rate=0.04)

    assert at_zero.integrity_hash != at_four.integrity_hash
