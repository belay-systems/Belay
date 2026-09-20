"""Sharpe and Sortino. ADR-011 rules 1, 2, 6, 7 and 8.

**Sharpe** asks: for every unit of swing a strategy put you through, how much
return above cash did it hand back? A strategy returning 12% a year while
lurching 30% either way is not obviously better than one returning 6% while
barely moving, and Sharpe is the number that compares them.

**Sortino** asks the same question counting only the *downward* swing. Upside
volatility is not a risk anybody needs compensating for, and Sharpe penalises it
identically to a loss.

**This file is `risk_adjusted.py` because `scripts/status.py:50` says so.**
`Risk-adjusted returns` is one of the seven promotion criteria that
`constitution/Promotion_Pipeline.md` requires promotion to consider — ruled
authoritative by ADR-006 — and the dashboard names exactly this path as the
component expected to make it computable. Before this file existed the dashboard
reported one of seven criteria computable. The filename is part of the
deliverable, not a preference.

Neither ratio is computable from `Validation/Backtesting.md` alone. It names
both, on lines 17 and 19, and defines neither: no risk-free rate, no target
return, no annualization. ADR-011 rule 1 rules that those are required arguments
rather than defaults, because a rate applied silently is indistinguishable at a
promotion gate from a rate somebody chose. ADR-005 rule 4 refused the same shape
when it declined to default `confidence` to 0.5.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import datetime

from framework.artifacts.artifact import Artifact
from framework.metrics.reporting import Disclosure, metric_artifact
from framework.metrics.volatility import downside_deviation, standard_deviation

SHARPE_METHODOLOGY = (
    "annualized mean excess return over annualized sample volatility; "
    "risk-free rate supplied as an annual rate and converted to the "
    "observation frequency"
)

SORTINO_METHODOLOGY = (
    "annualized mean excess return over annualized downside deviation about "
    "the same target, with the full sample as divisor; target supplied as an "
    "annual rate and converted to the observation frequency"
)


def _check_series(returns: Sequence[float], periods_per_year: float) -> None:
    """The two refusals both ratios share, so neither can forget one."""
    if len(returns) < 2:
        raise ValueError(
            f"a risk-adjusted ratio needs at least two observations, got "
            f"{len(returns)}; a single observation has no spread to measure"
        )
    if periods_per_year <= 0:
        raise ValueError(f"periods_per_year must be positive, got {periods_per_year}")


def sharpe_ratio(
    returns: Sequence[float],
    risk_free_rate: float,
    periods_per_year: float,
) -> float:
    """Return the annualized Sharpe ratio of `returns` — ADR-011 rule 6.

        mean(r - rf_period) * periods_per_year
        --------------------------------------
          stdev(r) * sqrt(periods_per_year)

    **`risk_free_rate` is an ANNUAL rate** and is divided by `periods_per_year`
    here. That is how a risk-free rate is quoted everywhere, and demanding a
    per-period rate would invite a silent factor-of-252 error: a daily rate of
    0.04 where an annual one was meant understates the excess return by about
    ten percentage points a year and still produces a plausible-looking number.

    Recorded as a choice rather than a fact: **this is not
    `(CAGR - rf) / volatility`.** The two differ whenever returns are volatile,
    because compounding is not linear. The arithmetic form is used because its
    numerator and denominator are computed from the same sample in the same way.

    A series with no volatility is refused rather than scored. The ratio is
    undefined there, and returning `inf` would read at a promotion gate as the
    best strategy ever measured.
    """
    _check_series(returns, periods_per_year)

    dispersion = standard_deviation(returns)
    if dispersion == 0.0:
        raise ValueError(
            "the series has no volatility, so a risk-adjusted ratio is undefined; "
            "every period returned the same figure"
        )

    per_period_rate = risk_free_rate / periods_per_year
    mean_excess = sum(value - per_period_rate for value in returns) / len(returns)

    return (mean_excess * periods_per_year) / (dispersion * math.sqrt(periods_per_year))


def sortino_ratio(
    returns: Sequence[float],
    target_return: float,
    periods_per_year: float,
) -> float:
    """Return the annualized Sortino ratio of `returns` — ADR-011 rules 7 and 8.

        mean(r - target_period) * periods_per_year
        -----------------------------------------
        downside_deviation(r) * sqrt(periods_per_year)

    **The target appears in both places** (rule 8). The common mistake is to
    measure excess return against a risk-free rate while measuring downside
    against the target; that produces a number which is neither a Sortino ratio
    nor a Sharpe ratio and then gets labelled as one.

    `target_return` is an **annual** rate, converted here for the same reason
    `sharpe_ratio` converts its risk-free rate — one conversion, one place.

    A series that never fell short of its target is refused rather than scored.
    That case is not exotic: any strategy which beat its target in every single
    period lands there, and those are exactly the ones a promotion gate is most
    likely to be looking at.
    """
    _check_series(returns, periods_per_year)

    per_period_target = target_return / periods_per_year
    downside = downside_deviation(returns, target=per_period_target)
    if downside == 0.0:
        raise ValueError(
            "the series never fell short of its target, so the Sortino ratio is "
            "undefined; there is no downside deviation to divide by"
        )

    mean_excess = sum(value - per_period_target for value in returns) / len(returns)

    return (mean_excess * periods_per_year) / (downside * math.sqrt(periods_per_year))


def sharpe_artifact(
    identifier: str,
    title: str,
    returns: Sequence[float],
    risk_free_rate: float,
    periods_per_year: float,
    disclosure: Disclosure,
    timestamp: datetime | None = None,
) -> Artifact:
    """Compute the Sharpe ratio and return it as a signed Artifact.

    ADR-011 rule 2: the risk-free rate and the period count are recorded in the
    artifact's content, inside the integrity hash. A Sharpe of 1.4 at a 0% rate
    and a Sharpe of 1.4 at 4% are two different claims about two different
    strategies, and an artifact carrying only the number cannot tell them apart.
    """
    return metric_artifact(
        identifier=identifier,
        title=title,
        metric="sharpe_ratio",
        value=sharpe_ratio(
            returns,
            risk_free_rate=risk_free_rate,
            periods_per_year=periods_per_year,
        ),
        observations=len(returns),
        methodology=SHARPE_METHODOLOGY,
        disclosure=disclosure,
        parameters=(
            ("risk_free_rate", risk_free_rate),
            ("periods_per_year", periods_per_year),
        ),
        timestamp=timestamp,
    )


def sortino_artifact(
    identifier: str,
    title: str,
    returns: Sequence[float],
    target_return: float,
    periods_per_year: float,
    disclosure: Disclosure,
    timestamp: datetime | None = None,
) -> Artifact:
    """Compute the Sortino ratio and return it as a signed Artifact.

    The target return is recorded for the reason the risk-free rate is: it is
    part of what the number means rather than a detail of how it was obtained.
    """
    return metric_artifact(
        identifier=identifier,
        title=title,
        metric="sortino_ratio",
        value=sortino_ratio(
            returns,
            target_return=target_return,
            periods_per_year=periods_per_year,
        ),
        observations=len(returns),
        methodology=SORTINO_METHODOLOGY,
        disclosure=disclosure,
        parameters=(
            ("target_return", target_return),
            ("periods_per_year", periods_per_year),
        ),
        timestamp=timestamp,
    )
