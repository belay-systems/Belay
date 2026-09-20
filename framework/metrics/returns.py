"""Period returns and compound annual growth. ADR-011 rules 1, 3 and 5.

A return is what a price series looks like once the price level is taken out of
it: "the position gained 1.2% over this period" rather than "the price was
104.7". Every metric in `Validation/Backtesting.md` except Drawdown is computed
from returns rather than prices, which makes the convention that produces them
load-bearing — if two components disagree about what a return is, every number
downstream disagrees with them both and nothing says so.

**CAGR** is the Compound Annual Growth Rate: the single yearly rate which,
compounded across the sample, would have produced the same final capital. It is
deliberately not the average of the period returns. Up 50% then down 50% leaves
75 of every 100 — a 25% loss — while the arithmetic mean of +0.5 and -0.5 is
zero. Averaging would report that strategy as having broken even.

ADR-011 rule 1 governs the shape of these signatures: nothing in
`Validation/Backtesting.md` says how many periods a year holds, so
`periods_per_year` is a required argument with no default. A silently assumed
252 is a decision no document made, and at a promotion gate it is
indistinguishable from one somebody chose.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from framework.artifacts.artifact import Artifact
from framework.metrics.reporting import Disclosure, metric_artifact

CAGR_METHODOLOGY = (
    "compound annual growth rate: the geometric product of simple period "
    "returns, raised to periods_per_year over the observation count"
)


def period_returns(prices: Sequence[float]) -> tuple[float, ...]:
    """Return the simple period returns of `prices`.

    ADR-011 rule 3: `r_t = P_t / P_(t-1) - 1`, never a log return.
    `Validation/Backtesting.md:15` asks for a *Compound* Annual Growth Rate, and
    the arithmetic mean of log returns is not a compound growth rate — carrying
    both conventions would let two Belay components disagree about what a return
    is while both looking correct.

    `n` prices yield `n - 1` returns: the first price has no predecessor. An
    off-by-one here would shift the entire series against its own sample period.

    Raises ValueError on fewer than two prices or on a non-positive price. Both
    are bad data rather than benign edge cases, and the second would otherwise
    divide by zero or invert the sign of a return.
    """
    if len(prices) < 2:
        raise ValueError(
            f"a return series needs at least two prices, got {len(prices)}; "
            "one price has no predecessor to be measured against"
        )
    if any(price <= 0 for price in prices):
        raise ValueError("price series contains a non-positive price")

    return tuple(
        prices[index] / prices[index - 1] - 1.0 for index in range(1, len(prices))
    )


def cagr(returns: Sequence[float], periods_per_year: float) -> float:
    """Return the compound annual growth rate implied by `returns`.

    `periods_per_year` states the observation frequency — 252 for trading days,
    12 for months, 1 for years. It has no default by ADR-011 rule 1: nothing in
    a sequence of floats says whether the numbers are daily or monthly, and the
    market data boundary that would carry real timestamps is Stage 2 and does
    not exist.

    A -100% period wipes the capital out and returns -1.0 however long the
    series runs, because the growth factor is zero and nothing after it can
    recover. That is an answer rather than an error.

    A return below -100% is refused. It denotes losing more than the capital
    committed, which makes the compound growth factor negative, and a fractional
    power of a negative number is not a real number — the alternative to
    refusing is a `nan` propagating into an artifact where it would read as a
    computed figure.
    """
    if not returns:
        raise ValueError("return series is empty")
    if periods_per_year <= 0:
        raise ValueError(
            f"periods_per_year must be positive, got {periods_per_year}"
        )
    for value in returns:
        if value < -1.0:
            raise ValueError(
                f"period return {value} is below -100%, which denotes losing more "
                "than the capital committed; the compound growth factor is then "
                "negative and no real annual rate exists"
            )

    growth = 1.0
    for value in returns:
        growth *= 1.0 + value

    return growth ** (periods_per_year / len(returns)) - 1.0


def cagr_artifact(
    identifier: str,
    title: str,
    returns: Sequence[float],
    periods_per_year: float,
    disclosure: Disclosure,
    timestamp: datetime | None = None,
) -> Artifact:
    """Compute CAGR over `returns` and return it as a signed Artifact.

    `periods_per_year` is recorded in the artifact's content, not just consumed:
    ADR-011 rule 2. The same series annualized at 252 and at 12 produces two
    different growth rates, and an artifact carrying only the result cannot say
    which question was asked.
    """
    return metric_artifact(
        identifier=identifier,
        title=title,
        metric="cagr",
        value=cagr(returns, periods_per_year=periods_per_year),
        observations=len(returns),
        methodology=CAGR_METHODOLOGY,
        disclosure=disclosure,
        parameters=(("periods_per_year", periods_per_year),),
        timestamp=timestamp,
    )
