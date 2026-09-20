"""Statistical significance and sample adequacy. ADR-012.

**The question this module answers is "could luck have produced this?" — never
"is this good".** Every other number under `framework/metrics/` describes a
track record. This one draws a conclusion from one, and
`constitution/Capital_Authority.md:11-14` makes `Statistical edge` one of six
inputs that determine capital, so the conclusion sizes positions.

Seven documents demand statistical validity and none defines it.
`constitution/Promotion_Pipeline.md:27` defines maturity Level 2, `Validated`,
**as** "Passed statistical review" — the only one of the seven levels defined by
the passing of a test — and `Validation/README.md:23` makes "Evaluate
statistical significance" a departmental responsibility. What none of them
states is a test, a threshold, a null hypothesis or a minimum sample. ADR-012
rules those, and rules that Belay supplies none of them silently.

**Immutable Law IV is the constraint that shapes the whole module: "Past
performance is evidence. It is never proof."** A p-value is that law written as
arithmetic — it can make luck an unconvincing explanation, and it can never make
an edge a fact. Rule 7 therefore fixes what every artifact from here must admit
about itself, and rule 11 keeps the promotion decision out.

Note the module name shadows the standard library's `statistics` for a reader
but not for the interpreter: absolute imports mean `import statistics` anywhere
else in Belay still resolves to the standard library. Nothing here imports it.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import DeliverableType
from framework.metrics.distributions import student_t_two_sided_p, t_critical_value
from framework.metrics.reporting import Disclosure, SamplePeriod, metric_artifact
from framework.metrics.volatility import standard_deviation

METHODOLOGY = (
    "two-sided one-sample Student's t-test on the mean period return, with n-1 "
    "degrees of freedom; null return supplied as an annual rate and converted "
    "to the observation frequency"
)

# ADR-012 rule 7. These strings are fixed rather than caller-supplied, and that
# is the whole mechanism of the rule: if `known_limitations` were a parameter,
# the caveat could be replaced with "None." by whoever found it inconvenient,
# and the artifact would still satisfy ADR-011 rule 9's non-blank check.
ASSUMPTIONS = (
    "Two-sided one-sample Student's t-test on the mean period return. Assumes "
    "returns are independent and identically distributed. The null hypothesis "
    "is that the mean period return equals the stated null return."
)

KNOWN_LIMITATIONS = (
    "The independence assumption is violated by real return series, which are "
    "autocorrelated and heteroskedastic, and their tails are fatter than the t "
    "distribution allows. The resulting p-value is therefore OPTIMISTIC: it "
    "understates the probability that this record is luck. No multiple-testing "
    "or data-snooping correction is applied, because Belay does not record how "
    "many strategies were tried; a record that survived many variations before "
    "passing has demonstrated less than this p-value suggests. ADR-012 rules 7 "
    "and 10."
)

# ADR-012 rule 8's search bound. An effect this small is not worth a sample size
# nobody could ever collect: a million daily observations is roughly four
# thousand years of trading.
_MAX_OBSERVATIONS = 1_000_000


@dataclass(frozen=True, slots=True)
class SignificanceResult:
    """One statistical review, with every input that produced it.

    Carries both the annual `null_return` as supplied and the
    `null_return_per_period` actually used, because the conversion is exactly
    where a silent factor-of-252 error would live and reporting only one of them
    would hide it.
    """

    observations: int
    null_return: float
    null_return_per_period: float
    periods_per_year: float
    alpha: float
    mean_return: float
    standard_error: float
    t_statistic: float
    p_value: float
    significant: bool
    minimum_observations: int
    sample_adequate: bool


def _mean(returns: Sequence[float]) -> float:
    return sum(returns) / len(returns)


def _require_series(returns: Sequence[float]) -> None:
    if len(returns) < 2:
        raise ValueError(
            f"a significance test needs at least two observations, got "
            f"{len(returns)}; a t-statistic on one observation is undefined"
        )


def standard_error(returns: Sequence[float]) -> float:
    """Return the standard error of the mean: the dispersion of the *average*.

    Not the dispersion of the returns themselves. An average of many
    observations is better pinned down than any single one of them, which is
    why it shrinks as the square root of the sample size — and why sample size
    is a question in its own right rather than a detail.
    """
    _require_series(returns)
    return standard_deviation(returns) / math.sqrt(len(returns))


def t_statistic(returns: Sequence[float], null_return: float) -> float:
    """Return how many standard errors the mean sits from `null_return`.

    `null_return` is a **per-period** figure, matching the series. The
    annual-to-period conversion belongs to the caller that also knows
    `periods_per_year`, which is `significance` — one conversion in one place,
    the same split ADR-011 made between `downside_deviation` and
    `sortino_ratio`.

    It has no default. ADR-012 rule 2: testing against zero is conventional and
    is still a choice, because a strategy that beats zero but not the risk-free
    rate has no edge worth capital.

    A series with no variation is refused. The standard error is zero there, and
    returning infinity would read at a promotion gate as perfect certainty when
    what actually happened is that the test cannot be performed.
    """
    _require_series(returns)

    error = standard_error(returns)
    if error == 0.0:
        raise ValueError(
            "the series has no variation, so the standard error is zero and no "
            "t-statistic exists; every period returned the same figure"
        )

    return (_mean(returns) - null_return) / error


def p_value(returns: Sequence[float], null_return: float) -> float:
    """Return the two-sided p-value for `returns` against `null_return`.

    The probability of observing a mean at least this far from the null, in
    either direction, if the null were true. **It is not the probability that
    the strategy has no edge**, and nothing in Belay may present it as one —
    Immutable Law IV.
    """
    return student_t_two_sided_p(
        t_statistic(returns, null_return=null_return), len(returns) - 1
    )


def confidence_interval(
    returns: Sequence[float], confidence: float
) -> tuple[float, float]:
    """Return the interval around the mean period return at `confidence`.

    `confidence` of 0.95 gives the conventional 95% interval. It has no default
    for the reason alpha has none — ADR-012 rule 3.

    An interval that straddles the null is the same statement as a p-value above
    alpha, said in the units of the thing being measured, which is often the
    more useful form for a review to read.
    """
    if not 0.0 < confidence < 1.0:
        raise ValueError(
            f"confidence must be a probability between 0 and 1, got {confidence}"
        )
    _require_series(returns)

    margin = t_critical_value(1.0 - confidence, len(returns) - 1) * standard_error(
        returns
    )
    centre = _mean(returns)
    return (centre - margin, centre + margin)


def minimum_observations_for_significance(
    returns: Sequence[float], null_return: float, alpha: float
) -> int:
    """Return how many observations this effect size would need to be significant.

    **ADR-012 rule 8, and the distinction the rule exists for.** "Not
    significant" and "not enough data to tell" are different states, and
    reporting them identically is the failure this answers. A sample below this
    number has not failed the test — it has not taken it.

    Found by binary search. The condition `effect * sqrt(n) >= t_crit(alpha,
    n-1)` is monotone in n: the left side grows and the right side shrinks, so
    there is exactly one crossing and bisection finds it without stepping
    through a million candidates.

    An effect of exactly zero is refused rather than searched for. No sample
    size rescues a mean sitting on the null, and returning `_MAX_OBSERVATIONS`
    would read as "collect more data" when the honest answer is that there is
    nothing here to establish.
    """
    _require_series(returns)
    if not 0.0 < alpha < 1.0:
        raise ValueError(f"alpha must be a probability between 0 and 1, got {alpha}")

    dispersion = standard_deviation(returns)
    if dispersion == 0.0:
        raise ValueError(
            "the series has no variation, so no significance test applies"
        )

    # Absolute, because the test is two-sided: an effect below the null becomes
    # significant in the other direction and needs the same sample to show it.
    effect = abs(_mean(returns) - null_return) / dispersion
    if effect == 0.0:
        raise ValueError(
            "the observed mean is indistinguishable from the null, so no sample "
            "size makes it significant; this is not a shortage of data"
        )

    def clears(n: int) -> bool:
        return effect * math.sqrt(n) >= t_critical_value(alpha, n - 1)

    if not clears(_MAX_OBSERVATIONS):
        raise ValueError(
            f"an effect of {effect:.6g} standard deviations would need more than "
            f"{_MAX_OBSERVATIONS} observations at alpha {alpha}, which is not a "
            "sample anyone can collect"
        )

    low, high = 2, _MAX_OBSERVATIONS
    while low < high:
        middle = (low + high) // 2
        if clears(middle):
            high = middle
        else:
            low = middle + 1

    return low


def significance(
    returns: Sequence[float],
    null_return: float,
    periods_per_year: float,
    alpha: float,
) -> SignificanceResult:
    """Run one statistical review and return every number that went into it.

    `null_return` is an **annual** rate and is divided by `periods_per_year`
    here — ADR-011 rule 6's convention, applied so that two modules in one
    package cannot disagree about whether a rate is annual or per-period.

    `alpha` has no default. ADR-012 rule 3: no Belay document states a
    significance level, and 0.05 is precisely the threshold a selection process
    should be stricter than rather than equal to.

    **`significant` is `p < alpha` and nothing more.** ADR-012 rule 11: this
    reports whether the caller's own threshold was met, and does not decide
    promotion. `Promotion_Pipeline.md:27` makes "Passed statistical review" a
    maturity level, but a maturity level is a governance decision recorded
    through `framework/artifacts/review.py`.
    """
    _require_series(returns)
    if periods_per_year <= 0:
        raise ValueError(f"periods_per_year must be positive, got {periods_per_year}")
    if not 0.0 < alpha < 1.0:
        raise ValueError(f"alpha must be a probability between 0 and 1, got {alpha}")

    per_period_null = null_return / periods_per_year
    observed_p = p_value(returns, null_return=per_period_null)

    # Only meaningful when an effect exists. A mean sitting exactly on the null
    # has no sample size that would establish it, and the result records that as
    # "the sample is not adequate" rather than propagating the refusal — the
    # review still wants the p-value it came for.
    try:
        needed = minimum_observations_for_significance(
            returns, null_return=per_period_null, alpha=alpha
        )
    except ValueError:
        needed = _MAX_OBSERVATIONS

    return SignificanceResult(
        observations=len(returns),
        null_return=null_return,
        null_return_per_period=per_period_null,
        periods_per_year=periods_per_year,
        alpha=alpha,
        mean_return=_mean(returns),
        standard_error=standard_error(returns),
        t_statistic=t_statistic(returns, null_return=per_period_null),
        p_value=observed_p,
        significant=observed_p < alpha,
        minimum_observations=needed,
        sample_adequate=len(returns) >= needed,
    )


def significance_artifact(
    identifier: str,
    title: str,
    returns: Sequence[float],
    null_return: float,
    periods_per_year: float,
    alpha: float,
    data_source: str,
    sample_period: SamplePeriod,
    additional_limitations: str = "",
    timestamp: datetime | None = None,
) -> Artifact:
    """Run a statistical review and return it as a signed `Validation Report`.

    **ADR-012 rule 12: a `Validation Report`, not a `Backtest Report`.**
    `Validation/README.md:37` declares `Validation Reports` among the
    department's outputs and `Validation/Workflow.md:15` places Statistical
    Review as a step distinct from Backtesting. `VALIDATION_REPORTS` already
    exists, so no enum member is added and ADR-010's vocabulary is untouched.

    `sample_period` is a `SamplePeriod` — two dates, ADR-013 rule 7. It was a
    free-form string until 2026-08-01, which meant a statistical review could
    state a window nothing could compare against the series it was run on.

    **There is no `assumptions` or `known_limitations` parameter, deliberately.**
    ADR-012 rule 7 fixes both. `data_source` and `sample_period` are the caller's
    to state because only the caller knows them; the caveat about what a t-test
    on financial returns is worth is not negotiable, and a signature that
    accepted a replacement would let it be softened to "None." by whoever found
    it inconvenient.

    `additional_limitations` is appended, never substituted, so a caller can add
    what they know without removing what the ruling requires.
    """
    result = significance(
        returns,
        null_return=null_return,
        periods_per_year=periods_per_year,
        alpha=alpha,
    )

    limitations = KNOWN_LIMITATIONS
    if additional_limitations.strip():
        limitations = f"{limitations} {additional_limitations.strip()}"

    return metric_artifact(
        identifier=identifier,
        title=title,
        metric="statistical_significance",
        value=result.p_value,
        observations=result.observations,
        methodology=METHODOLOGY,
        disclosure=Disclosure(
            assumptions=ASSUMPTIONS,
            data_source=data_source,
            sample_period=sample_period,
            known_limitations=limitations,
        ),
        deliverable=DeliverableType.VALIDATION_REPORTS,
        parameters=(
            ("null_return", result.null_return),
            ("null_return_per_period", result.null_return_per_period),
            ("periods_per_year", result.periods_per_year),
            ("alpha", result.alpha),
            ("mean_return", result.mean_return),
            ("standard_error", result.standard_error),
            ("t_statistic", result.t_statistic),
            ("significant", result.significant),
            ("minimum_observations_for_significance", result.minimum_observations),
            ("sample_adequate", result.sample_adequate),
        ),
        timestamp=timestamp,
    )
