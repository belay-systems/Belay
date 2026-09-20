"""Volatility and downside deviation. ADR-011 rules 1, 4, 5 and 7.

Volatility is how far a return series swings around its own average. It is not
one of the nine metrics `Validation/Backtesting.md` names, which is exactly why
it needs its own module and its own ruling: Sharpe and Sortino both divide by
it, so the convention chosen here decides both of their values, and the document
is silent on that convention.

The oracle for the sample-versus-population question is `statistics.stdev` from
the standard library rather than a figure this suite computed the same way the
implementation does. A test that re-implements the code it is testing proves
only that the author repeated themselves.
"""

from __future__ import annotations

import math
import statistics

import pytest

from framework.metrics.volatility import (
    annualized_volatility,
    downside_deviation,
    standard_deviation,
)

# Mean 0.008. Deviations from it: 0.002, -0.028, 0.022, -0.008, 0.012.
RETURNS = (0.01, -0.02, 0.03, 0.00, 0.02)


def test_standard_deviation_is_the_sample_estimator():
    """ADR-011 rule 4: divide by n-1. `statistics.stdev` is the sample form."""
    assert standard_deviation(RETURNS) == pytest.approx(statistics.stdev(RETURNS))


def test_standard_deviation_is_not_the_population_estimator():
    """The half of rule 4 that actually bites.

    The two estimators differ by sqrt(n / (n-1)) and both look entirely
    plausible in isolation. Asserting only the sample value would still pass on
    a long series if someone switched to the population form, because the gap
    shrinks with n — so the population form is refused by name.

    The sample estimator is the LARGER of the two. Understating dispersion
    inflates every risk-adjusted number computed from it, in the direction that
    flatters a strategy, and that is the direction rule 4 refuses.
    """
    assert standard_deviation(RETURNS) != pytest.approx(statistics.pstdev(RETURNS))
    assert standard_deviation(RETURNS) > statistics.pstdev(RETURNS)


def test_a_constant_series_has_zero_dispersion():
    assert standard_deviation((0.01, 0.01, 0.01)) == pytest.approx(0.0)


@pytest.mark.parametrize("returns", [(), (0.01,)])
def test_fewer_than_two_observations_is_rejected(returns):
    """ADR-011 rule 5. One observation has no dispersion to measure, and
    returning 0.0 would report a strategy with no variance rather than a series
    that cannot answer the question — the difference between an answer and the
    absence of one."""
    with pytest.raises(ValueError, match="at least two"):
        standard_deviation(returns)


def test_annualization_scales_by_the_square_root_of_the_period_count():
    assert annualized_volatility(RETURNS, periods_per_year=252) == pytest.approx(
        statistics.stdev(RETURNS) * math.sqrt(252)
    )


def test_annualizing_at_one_period_a_year_changes_nothing():
    assert annualized_volatility(RETURNS, periods_per_year=1) == pytest.approx(
        standard_deviation(RETURNS)
    )


def test_annualized_volatility_has_no_default_period_count():
    """ADR-011 rule 1, same reasoning as CAGR's."""
    with pytest.raises(TypeError):
        annualized_volatility(RETURNS)


# --------------------------------------------------------- downside deviation


def test_downside_deviation_counts_only_shortfalls():
    """Hand-calculable on purpose.

    Against a target of 0.0, exactly one of the five returns falls short:
    -0.02. Squared that is 0.0004; over n-1 = 4 that is 0.0001; the square root
    is exactly 0.01.
    """
    assert downside_deviation(RETURNS, target=0.0) == pytest.approx(0.01)


def test_downside_deviation_divides_by_the_full_sample():
    """ADR-011 rule 7, and why it is a rule rather than an implementation detail.

    Dividing by the count of below-target periods instead of the full sample
    gives sqrt(0.0004 / 1) = 0.02 — double the answer. Worse than being double,
    it shrinks the denominator along with the numerator, so a strategy with one
    bad period in five would score identically to one with five out of five.

    Both conventions are in use in the literature and the choice is invisible in
    the result, which is precisely why the losing one is named here rather than
    left to be re-decided by whoever edits this next.
    """
    assert downside_deviation(RETURNS, target=0.0) == pytest.approx(0.01)
    assert downside_deviation(RETURNS, target=0.0) != pytest.approx(0.02)


def test_upside_is_not_risk():
    """The whole distinction between Sortino and Sharpe.

    A series that only ever rises has real volatility and no downside deviation
    at all. Sortino exists to say that such a strategy is not risky, and Sharpe
    cannot say it.
    """
    rising = (0.01, 0.02, 0.03)

    assert downside_deviation(rising, target=0.0) == pytest.approx(0.0)
    assert standard_deviation(rising) > 0.0


def test_a_higher_target_turns_more_periods_into_shortfalls():
    assert downside_deviation(RETURNS, target=0.05) > downside_deviation(
        RETURNS, target=0.0
    )


@pytest.mark.parametrize("returns", [(), (0.01,)])
def test_downside_deviation_rejects_fewer_than_two_observations(returns):
    with pytest.raises(ValueError, match="at least two"):
        downside_deviation(returns, target=0.0)


def test_downside_deviation_has_no_default_target():
    """ADR-011 rule 1. A target of zero is the most common convention and is
    still a decision no Belay document has made."""
    with pytest.raises(TypeError):
        downside_deviation(RETURNS)
