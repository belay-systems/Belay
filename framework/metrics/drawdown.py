"""Maximum drawdown — the worst peak-to-trough decline in a price series.

Drawdown answers a capital-preservation question directly: if capital had been
committed to this series at the worst possible moment, how far down would it
have gone before recovering? A value of 0.25 means the series fell 25% from its
running peak at the worst point.

This is the first Belay component to emit an Artifact carrying a computed
number rather than a synthetic one.

**Migrated onto `framework/metrics/reporting.py` on 2026-07-31 — ADR-011 rule
13.** This module predates both ADR-010 and ADR-011, so it emitted an untyped
`REPORT` carrying a bare `source` string and none of the four things
`Validation/Backtesting.md` requires a backtest to document. `docs/HANDOFF.md`
describes it as "the only worked example and the pattern to follow", and leaving
the one worked example as the one component that does not follow the rule would
have made the rule optional in practice on the day it was ratified.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from framework.artifacts.artifact import Artifact
from framework.metrics.reporting import Disclosure, metric_artifact

METHODOLOGY = "peak-to-trough maximum drawdown over the full observed series"


def max_drawdown(prices: Sequence[float]) -> float:
    """Return the worst peak-to-trough decline as a non-negative fraction.

    Walks the series once, tracking the highest price seen so far (the running
    peak) and the largest percentage fall below that peak. A series that never
    declines returns 0.0.

    Raises ValueError on an empty series or a non-positive price. Both indicate
    bad data rather than a benign edge case, and silently returning a number
    would let unusable input reach a promotion gate as if it were evidence.
    """
    if not prices:
        raise ValueError("price series is empty")
    if any(price <= 0 for price in prices):
        raise ValueError("price series contains a non-positive price")

    peak = prices[0]
    worst = 0.0

    for price in prices:
        if price > peak:
            peak = price
        decline = (peak - price) / peak
        if decline > worst:
            worst = decline

    return worst


def drawdown_artifact(
    identifier: str,
    title: str,
    prices: Sequence[float],
    disclosure: Disclosure,
    timestamp: datetime | None = None,
) -> Artifact:
    """Compute max drawdown over `prices` and return it as a signed Artifact.

    `disclosure` carries the four things `Validation/Backtesting.md` requires a
    backtest to document, and `Disclosure` refuses a blank one. It replaces the
    `source` string this function used to take — which covered `Data Source`
    alone and left the other three unrecorded.

    The old signature is **gone rather than deprecated.** A second accepted form
    would leave the pre-ADR-011 pattern legal, which is what `AGENTS.md` means
    by parallel implementations, and the callers are countable: this repository
    stores no artifacts, so nothing built by the old signature exists to break.

    Pass `timestamp` to make the result byte-for-byte reproducible; it defaults
    to now, which makes each call unique.

    Max drawdown takes no free parameters — there is no equivalent of Sharpe's
    risk-free rate to record — so `parameters` is left empty rather than filled
    with something invented to look symmetrical.
    """
    return metric_artifact(
        identifier=identifier,
        title=title,
        metric="max_drawdown",
        value=max_drawdown(prices),
        observations=len(prices),
        methodology=METHODOLOGY,
        disclosure=disclosure,
        timestamp=timestamp,
    )
