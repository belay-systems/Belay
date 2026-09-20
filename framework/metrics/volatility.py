"""Dispersion of a return series. ADR-011 rules 1, 4, 5 and 7.

Volatility is how far a return series swings around its own average. A strategy
returning 1% every month and one alternating +9% and -7% can reach the same
place with very different journeys, and volatility is the number that tells them
apart.

**It is not one of the nine metrics `Validation/Backtesting.md` names**, which is
exactly why it needs its own module and its own ruling rather than being buried
inside Sharpe. Sharpe and Sortino both divide by a dispersion measure, so the
conventions chosen here decide both of their values — and the document is silent
on those conventions.

Two rulings live here.

**The sample estimator, dividing by n-1** (rule 4). A backtest series is a
sample of a process, not the population of it: the population is every return
the strategy will ever produce, most of which has not happened. The population
estimator understates dispersion, and understating dispersion inflates every
risk-adjusted number computed from it — in the direction that flatters a
strategy. Where two conventions are both defensible, Belay takes the one that
cannot flatter.

**Downside deviation divides by the full sample too** (rule 7), not by the count
of periods that fell short. See `downside_deviation`.

No function here emits an Artifact. Volatility is an ingredient of the
documented metrics rather than one of them, and giving it an artifact emitter
would put a figure into the evidence record that `Validation/Backtesting.md`
never asked a backtest to report.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def standard_deviation(returns: Sequence[float]) -> float:
    """Return the sample standard deviation of `returns` — ADR-011 rule 4.

    Divides by `n - 1`, matching `statistics.stdev`. `tests/metrics/
    test_volatility.py` checks against that function and separately refuses
    `statistics.pstdev`, because the two differ by `sqrt(n / (n-1))` and the gap
    shrinks with n — asserting only the sample value would still pass on a long
    series if someone switched to the population form.

    Fewer than two observations is refused rather than answered (rule 5). One
    observation has no dispersion to measure, and returning 0.0 would report a
    strategy with no variance rather than a series that cannot answer the
    question — the difference between an answer and the absence of one. This is
    the refusal `max_drawdown` already makes for an empty series.
    """
    if len(returns) < 2:
        raise ValueError(
            f"dispersion needs at least two observations, got {len(returns)}; "
            "a single observation has no spread to measure"
        )

    mean = sum(returns) / len(returns)
    variance = sum((value - mean) ** 2 for value in returns) / (len(returns) - 1)
    return math.sqrt(variance)


def annualized_volatility(
    returns: Sequence[float], periods_per_year: float
) -> float:
    """Return the standard deviation scaled to an annual figure.

    Scaled by `sqrt(periods_per_year)` rather than by `periods_per_year`,
    because variance adds across independent periods while standard deviation
    does not — doubling the horizon multiplies the spread by `sqrt(2)`, not by 2.

    `periods_per_year` has no default. ADR-011 rule 1, same reasoning as CAGR's.
    """
    if periods_per_year <= 0:
        raise ValueError(f"periods_per_year must be positive, got {periods_per_year}")

    return standard_deviation(returns) * math.sqrt(periods_per_year)


def downside_deviation(returns: Sequence[float], target: float) -> float:
    """Return the dispersion of `returns` below `target` — ADR-011 rule 7.

    `target` is a **per-period** figure, not an annual one. The annual-to-period
    conversion belongs to the caller that also knows `periods_per_year`, which
    is `sortino_ratio`; doing it in two places would be two chances to get the
    factor wrong.

    Only shortfalls contribute. A period that beat the target contributes zero
    rather than a negative number, which is the whole distinction between this
    and `standard_deviation`: upside volatility is not a risk anyone needs
    compensating for, and a series that only ever rises has real volatility and
    no downside deviation at all.

    **The divisor is `n - 1` over the full series, not over the shortfalls.**
    Both conventions are in use and the choice is invisible in the result, so it
    is stated rather than left to be re-decided. Dividing by the count of
    below-target periods shrinks the denominator along with the numerator, which
    would make a strategy with one bad period in a hundred score like one with
    fifty — the opposite of what the measure exists to show.
    """
    if len(returns) < 2:
        raise ValueError(
            f"dispersion needs at least two observations, got {len(returns)}; "
            "a single observation has no spread to measure"
        )

    shortfalls = [max(0.0, target - value) for value in returns]
    variance = sum(shortfall**2 for shortfall in shortfalls) / (len(returns) - 1)
    return math.sqrt(variance)
