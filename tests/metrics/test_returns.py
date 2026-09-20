"""Period returns and CAGR. ADR-011 rules 1, 3 and 5.

A return series is what every other metric in `Validation/Backtesting.md` is
computed from, so the convention that produces one is load-bearing: if two
components disagree about what a return *is*, every number downstream disagrees
with them both and nothing says so.

CAGR is the Compound Annual Growth Rate — the single yearly growth rate that,
compounded over the sample, would have produced the same final capital. It is
not the average of the periodic returns, and the difference is the point.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest

from framework.artifacts.integrity import ArtifactIntegrity
from framework.metrics.reporting import Disclosure, SamplePeriod
from framework.metrics.returns import cagr, cagr_artifact, period_returns

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

DISCLOSURE = Disclosure(
    assumptions="No transaction costs, no slippage, no financing charges.",
    data_source="unit test fixture, supplied by hand",
    # ADR-013 rule 7: two dates, not prose. Two consecutive trading days.
    sample_period=SamplePeriod(start=date(2024, 1, 2), end=date(2024, 1, 3)),
    known_limitations="The series carries no provenance and describes no real instrument.",
)

# 100 -> 110 -> 99. Up 10%, then down 10% from the higher base.
PRICES = [100.0, 110.0, 99.0]
RETURNS = (0.1, -0.1)


def test_period_returns_are_simple_returns():
    """ADR-011 rule 3: r_t = P_t / P_(t-1) - 1, never a log return."""
    assert period_returns(PRICES) == pytest.approx(RETURNS)


def test_a_flat_series_returns_zeros():
    assert period_returns([50.0, 50.0, 50.0]) == pytest.approx((0.0, 0.0))


def test_n_prices_yield_one_fewer_return():
    """The first price has no predecessor, so it produces no return. Off-by-one
    here would shift the whole series against its own sample period."""
    assert len(period_returns([1.0, 2.0, 3.0, 4.0])) == 3


@pytest.mark.parametrize("prices", [[], [100.0]])
def test_fewer_than_two_prices_is_rejected(prices):
    with pytest.raises(ValueError, match="at least two"):
        period_returns(prices)


def test_a_non_positive_price_is_rejected():
    """The refusal `max_drawdown` already makes, for the same stated reason: a
    zero or negative price is bad data rather than a benign edge case, and
    dividing by it would emit a number anyway."""
    with pytest.raises(ValueError, match="non-positive"):
        period_returns([100.0, 0.0, 50.0])


# ----------------------------------------------------------------------- CAGR


def test_cagr_of_two_ten_percent_periods_is_ten_percent():
    """Hand-calculable and exact: 1.1 * 1.1 = 1.21, and 1.21 ** (1/2) - 1 = 0.1."""
    assert cagr((0.1, 0.1), periods_per_year=1) == pytest.approx(0.1)


def test_cagr_compounds_rather_than_averaging():
    """This is the whole reason rule 3 rules geometric growth.

    Up 50% then down 50% leaves 75 of every 100 — a 25% loss. The arithmetic
    mean of +0.5 and -0.5 is zero, so an averaging implementation would report
    that a strategy which lost a quarter of its capital broke even.
    """
    assert cagr((0.5, -0.5), periods_per_year=2) == pytest.approx(-0.25)


def test_a_partial_year_is_scaled_up_to_an_annual_rate():
    """One period that doubles capital, at two periods a year, is a 300% annual
    rate: 2 ** (2/1) - 1 = 3.0. Doubling twice is quadrupling, not doubling."""
    assert cagr((1.0,), periods_per_year=2) == pytest.approx(3.0)


def test_a_flat_series_has_zero_growth():
    assert cagr((0.0, 0.0, 0.0), periods_per_year=252) == pytest.approx(0.0)


def test_a_total_loss_is_minus_one_however_long_the_series():
    """A -100% period wipes the capital out, and nothing after it can recover:
    the growth factor is zero and stays zero. -1.0 is the honest answer rather
    than an error, because the question has a defined result."""
    assert cagr((-1.0, 0.0, 0.0), periods_per_year=1) == pytest.approx(-1.0)


def test_a_return_below_minus_one_hundred_percent_is_rejected():
    """Losing more than the capital committed makes the compound growth factor
    negative, and a fractional power of a negative number is not a real number.
    Refused explicitly rather than returned as a nan that would propagate into
    an artifact and read as a computed figure."""
    with pytest.raises(ValueError, match="below -100%"):
        cagr((-1.5,), periods_per_year=1)


def test_an_empty_return_series_is_rejected():
    with pytest.raises(ValueError, match="empty"):
        cagr((), periods_per_year=252)


@pytest.mark.parametrize("periods_per_year", [0, -1, -252])
def test_periods_per_year_must_be_positive(periods_per_year):
    with pytest.raises(ValueError, match="periods_per_year"):
        cagr((0.01,), periods_per_year=periods_per_year)


def test_periods_per_year_has_no_default():
    """ADR-011 rule 1, asserted as a property of the signature rather than
    described in a docstring.

    Nothing in `Validation/Backtesting.md` says how many periods a year holds,
    and nothing in a list of floats says whether they are daily or monthly. A
    default of 252 would be a decision no document made, applied silently, and
    indistinguishable at a promotion gate from one somebody chose.
    """
    with pytest.raises(TypeError):
        cagr((0.01, 0.02))


# ------------------------------------------------------------ as an artifact


def test_the_cagr_artifact_records_the_period_count_it_annualized_with():
    """ADR-011 rule 2. `periods_per_year` is not a detail of the call, it is part
    of what the number means: the same series at 252 and at 12 produces two
    different annual growth rates, and an artifact carrying only the result
    cannot say which question was asked."""
    artifact = cagr_artifact(
        identifier="RPT-0002",
        title="CAGR, sample series",
        returns=(0.1, 0.1),
        periods_per_year=1,
        disclosure=DISCLOSURE,
        timestamp=FIXED_TIME,
    )
    content = dict(artifact.content)

    assert content["metric"] == "cagr"
    assert content["value"] == pytest.approx(0.1)
    assert content["periods_per_year"] == 1
    assert content["observations"] == 2


def test_the_cagr_artifact_is_signed_and_carries_its_disclosures():
    artifact = cagr_artifact(
        identifier="RPT-0002",
        title="CAGR, sample series",
        returns=(0.1, 0.1),
        periods_per_year=1,
        disclosure=DISCLOSURE,
        timestamp=FIXED_TIME,
    )

    assert ArtifactIntegrity.verify_hash(artifact) is True
    assert dict(artifact.content)["known_limitations"] == DISCLOSURE.known_limitations
