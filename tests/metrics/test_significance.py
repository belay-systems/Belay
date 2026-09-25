"""Statistical significance and sample adequacy. ADR-012.

Seven documents demand statistical validity and none defines it.
`constitution/Promotion_Pipeline.md:27` defines maturity Level 2 **as** "Passed
statistical review", and `constitution/Capital_Authority.md:11-14` makes
`Statistical edge` one of six inputs that determine capital — so this number
sizes positions rather than merely informing a review.

The question it answers is "could luck have produced this?", never "is this
good". Immutable Law IV: "Past performance is evidence. It is never proof."
"""

from __future__ import annotations

import math
from datetime import date, datetime, timezone

import pytest

from framework.artifacts.enums import ArtifactType, DeliverableType, EvidenceLevel
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.validator import ArtifactValidator
from framework.metrics.distributions import t_critical_value
from framework.metrics.reporting import SamplePeriod
from framework.metrics.risk_adjusted import sharpe_ratio
from framework.metrics.statistics import (
    SignificanceResult,
    minimum_observations_for_significance,
    p_value,
    significance,
    significance_artifact,
    standard_error,
    t_statistic,
)
from framework.metrics.volatility import standard_deviation

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

# Mean 0.008, sample standard deviation sqrt(0.00037) ~ 0.019235. The same
# series ADR-011's tests use, so the two modules can be checked against each
# other rather than only against themselves.
WEAK = (0.01, -0.02, 0.03, 0.00, 0.02)

# Mean exactly 0.02, sample standard deviation exactly 0.002, n = 8.
# Deviations are 0, -0.002, 0.002, -0.001, 0.001, 0, 0.003, -0.003; the squares
# sum to 2.8e-05, over n-1 = 7 that is 4e-06, and the root is 0.002 exactly.
# So t = 0.02 / (0.002 / sqrt(8)) = 10 * sqrt(8), by hand.
STRONG = (0.020, 0.018, 0.022, 0.019, 0.021, 0.020, 0.023, 0.017)


# ------------------------------------------------------------- the arithmetic


def test_standard_error_is_the_dispersion_of_the_mean():
    """Not the dispersion of the returns. The standard error shrinks as the
    sample grows because an average of many observations is better pinned down
    than any one of them — which is the entire reason sample size matters."""
    assert standard_error(WEAK) == pytest.approx(
        standard_deviation(WEAK) / math.sqrt(len(WEAK))
    )


def test_the_t_statistic_is_hand_calculable():
    """STRONG has a mean of exactly 0.02 and a standard deviation of exactly
    0.002 over eight observations, so t = 0.02 / (0.002 / sqrt(8)) = 10*sqrt(8)."""
    assert t_statistic(STRONG, null_return=0.0) == pytest.approx(10.0 * math.sqrt(8))


def test_the_t_statistic_is_the_sharpe_ratio_annualized_at_the_sample_length():
    """An exact identity, and the most useful cross-check available.

    t = mean / (stdev / sqrt(n)) = (mean / stdev) * sqrt(n), and ADR-011's
    Sharpe at a zero risk-free rate is (mean * P) / (stdev * sqrt(P)) =
    (mean / stdev) * sqrt(P). Setting P = n makes them the same number.

    This is worth pinning because it ties two modules written under two
    different ADRs to one definition of dispersion. If someone changes
    `standard_deviation` from the sample to the population estimator, ADR-011's
    own tests catch it — and so does this one, from the other side.
    """
    for series in (WEAK, STRONG):
        assert t_statistic(series, null_return=0.0) == pytest.approx(
            sharpe_ratio(
                series, risk_free_rate=0.0, periods_per_year=len(series)
            )
        )


def test_raising_the_null_lowers_the_t_statistic():
    """A strategy tested against a 0% hurdle looks better than the same strategy
    tested against the risk-free rate. ADR-012 rule 2 exists so that which
    hurdle was used is never left implicit."""
    against_zero = t_statistic(WEAK, null_return=0.0)
    against_hurdle = t_statistic(WEAK, null_return=0.005)

    assert against_hurdle < against_zero


def test_a_convincing_series_has_a_small_p_value():
    assert p_value(STRONG, null_return=0.0) < 0.001


def test_an_unconvincing_series_does_not():
    """WEAK gained 0.8% a period on average while swinging 1.9%. Five
    observations of that are entirely ordinary luck, and the p-value says so."""
    assert p_value(WEAK, null_return=0.0) > 0.10


@pytest.mark.parametrize("series", [(), (0.01,)])
def test_fewer_than_two_observations_is_refused(series):
    """ADR-012 rule 9, extending ADR-011 rule 5. A t-statistic on one
    observation is undefined rather than zero."""
    with pytest.raises(ValueError, match="at least two"):
        t_statistic(series, null_return=0.0)


def test_a_series_with_no_variation_is_refused():
    """The standard error is zero, so the t-statistic divides by zero. Returning
    infinity would read at a promotion gate as perfect certainty, when what
    happened is that the test cannot be performed."""
    with pytest.raises(ValueError, match="no variation"):
        t_statistic((0.01, 0.01, 0.01), null_return=0.0)


# ------------------------------------------------------ no silent conventions


def test_the_null_return_has_no_default():
    """ADR-012 rule 2. Testing against zero is conventional and is still a
    choice: a strategy that beats zero but not the risk-free rate has no edge
    worth capital, and `Capital_Authority.md` makes that distinction load-bearing."""
    with pytest.raises(TypeError):
        t_statistic(WEAK)

    with pytest.raises(TypeError):
        p_value(WEAK)


def test_alpha_has_no_default():
    """ADR-012 rule 3. No Belay document states a significance level, and 0.05
    is exactly the threshold a selection process should be stricter than."""
    with pytest.raises(TypeError):
        significance(WEAK, null_return=0.0, periods_per_year=252)


def test_the_periods_per_year_convention_matches_adr_011():
    """`significance` takes an ANNUAL null return and converts it, exactly as
    `sharpe_ratio` does with its risk-free rate — ADR-011 rule 6.

    Two modules in one package disagreeing about whether a rate is annual or
    per-period is the silent factor-of-252 error ADR-011 rule 6 was written to
    prevent, so the convention is pinned rather than assumed.

    Driven to an exact equality: an annual null of 0.008 * 252 is precisely the
    mean per-period return of WEAK, so the t-statistic must be zero.
    """
    result = significance(
        WEAK, null_return=0.008 * 252, periods_per_year=252, alpha=0.05
    )

    assert result.t_statistic == pytest.approx(0.0)
    assert result.null_return_per_period == pytest.approx(0.008)
    assert result.p_value == pytest.approx(1.0)


# --------------------------------------------------- significance vs adequacy


def test_significant_means_exactly_p_below_alpha_and_nothing_more():
    """ADR-012 rule 11. The module reports whether the caller's threshold was
    met; it does not decide promotion.

    `Promotion_Pipeline.md:27` makes "Passed statistical review" a maturity
    level, which makes writing the gate here tempting. ADR-009 rule 5 drew the
    same line for review outcomes: comparing a computed number to a declared
    threshold is not deciding what follows from it.
    """
    for series in (WEAK, STRONG):
        result = significance(
            series, null_return=0.0, periods_per_year=252, alpha=0.05
        )
        assert result.significant is (result.p_value < result.alpha)


def test_the_module_does_not_expose_a_promotion_decision():
    """The other half of rule 11, asserted against the module's surface.

    A helper called `passes_statistical_review` would be read as authoritative
    by whoever found it, and the promotion decision belongs to a recorded review
    (`framework/artifacts/review.py`), not to arithmetic.
    """
    import framework.metrics.statistics as module

    forbidden = ["passes", "promote", "approve", "verdict", "gate", "decision"]
    exposed = [name for name in dir(module) if not name.startswith("_")]

    for name in exposed:
        assert not any(word in name.lower() for word in forbidden), (
            f"{name} reads as a promotion decision; ADR-012 rule 11 keeps that "
            "out of this module"
        )


def test_a_sample_can_be_inadequate_without_having_failed():
    """ADR-012 rule 8, and the distinction the whole rule exists for.

    WEAK is not significant. That does not mean the strategy has no edge — it
    means five observations cannot establish one either way. Reporting "not
    significant" and "not enough data to tell" as the same state is what rule 8
    refuses.

    The assertion is the *minimality* property rather than a magic number, so
    the test does not need updating if the arithmetic is refined: at n the
    effect clears the critical value, and at n-1 it does not.
    """
    needed = minimum_observations_for_significance(
        WEAK, null_return=0.0, alpha=0.05
    )
    effect = abs(sum(WEAK) / len(WEAK)) / standard_deviation(WEAK)

    assert needed > len(WEAK), "WEAK should need more data than it has"
    assert effect * math.sqrt(needed) >= t_critical_value(0.05, needed - 1)
    assert effect * math.sqrt(needed - 1) < t_critical_value(0.05, needed - 2)


def test_a_significant_result_is_always_an_adequate_sample():
    """These two are not independent, and saying so is more honest than
    implying a matrix of four outcomes.

    Significance at n *is* the condition that n meets the requirement, so
    `significant` implies `sample_adequate`. The informative case is the
    negative one: a sample that is inadequate tells you how many more
    observations the observed effect would need.
    """
    result = significance(STRONG, null_return=0.0, periods_per_year=252, alpha=0.05)

    assert result.significant is True
    assert result.sample_adequate is True
    assert result.minimum_observations <= result.observations


def test_a_stricter_alpha_demands_a_larger_sample():
    at_five = minimum_observations_for_significance(WEAK, null_return=0.0, alpha=0.05)
    at_one = minimum_observations_for_significance(WEAK, null_return=0.0, alpha=0.01)

    assert at_one > at_five


def test_an_effect_of_exactly_zero_can_never_become_significant():
    """No sample size rescues a mean sitting exactly on the null. Refused rather
    than looping to the cap and reporting an enormous number, which would read
    as "collect more data" when the honest answer is "there is nothing here"."""
    flat = (0.01, -0.01, 0.01, -0.01)

    assert sum(flat) == pytest.approx(0.0)
    with pytest.raises(ValueError, match="indistinguishable from the null"):
        minimum_observations_for_significance(flat, null_return=0.0, alpha=0.05)


def test_the_result_record_is_frozen():
    result = significance(WEAK, null_return=0.0, periods_per_year=252, alpha=0.05)

    assert isinstance(result, SignificanceResult)
    with pytest.raises(Exception):
        result.p_value = 0.0001


# ------------------------------------------------------------- as an artifact


def _artifact(**overrides):
    fields = {
        "identifier": "RPT-0011",
        "title": "Statistical review, sample series",
        "returns": STRONG,
        "null_return": 0.0,
        "periods_per_year": 252,
        "alpha": 0.05,
        "data_source": "unit test fixture, supplied by hand",
        # ADR-013 rule 7: two dates, not prose. Eight consecutive trading days.
        "sample_period": SamplePeriod(start=date(2024, 1, 2), end=date(2024, 1, 11)),
        "timestamp": FIXED_TIME,
    }
    fields.update(overrides)
    return significance_artifact(**fields)


def test_the_artifact_is_a_validation_report_not_a_backtest_report():
    """ADR-012 rule 12. `Validation/README.md:37` declares `Validation Reports`
    among the department's outputs, and `Validation/Workflow.md:15` places
    Statistical Review as a step distinct from Backtesting. No enum member is
    added — `VALIDATION_REPORTS` already exists."""
    artifact = _artifact()

    assert artifact.deliverable is DeliverableType.VALIDATION_REPORTS
    assert artifact.deliverable is not DeliverableType.BACKTEST_REPORTS
    assert artifact.type is ArtifactType.REPORT
    assert ArtifactValidator().validate(artifact) is True


def test_the_artifact_carries_the_test_and_its_thresholds():
    content = dict(_artifact().content)

    assert content["metric"] == "statistical_significance"
    assert content["value"] == pytest.approx(p_value(STRONG, null_return=0.0))
    assert content["alpha"] == pytest.approx(0.05)
    assert content["null_return"] == pytest.approx(0.0)
    assert content["periods_per_year"] == 252
    assert content["observations"] == len(STRONG)
    assert content["t_statistic"] == pytest.approx(10.0 * math.sqrt(8))
    assert content["significant"] is True
    assert ArtifactIntegrity.verify_hash(_artifact()) is True


def test_the_artifact_admits_that_its_p_value_is_optimistic():
    """ADR-012 rule 7, and the most important thing this module says about itself.

    The t-test assumes returns are independent and identically distributed.
    Real returns are autocorrelated, heteroskedastic and fatter-tailed than the
    t distribution allows, and the consequence has a **direction**: the p-value
    understates the probability that a track record is luck.

    Asserted on the artifact rather than on a docstring, because the artifact is
    what a promotion gate reads.
    """
    content = dict(_artifact().content)
    limitations = content["known_limitations"].lower()
    assumptions = content["assumptions"].lower()

    assert "independent" in assumptions
    assert "optimistic" in limitations
    assert "multiple" in limitations, "rule 10's exclusion must be disclosed"


def test_the_caller_cannot_suppress_the_limitations():
    """Rule 7 fixes these strings. If `known_limitations` were a parameter, the
    caveat could be replaced with "None." by whoever found it inconvenient —
    which is exactly the artifact ADR-011 rule 9 was written to make impossible."""
    with pytest.raises(TypeError):
        _artifact(known_limitations="None.")

    with pytest.raises(TypeError):
        _artifact(assumptions="Returns are well behaved.")


def test_the_caller_may_add_limitations_but_only_add():
    """Appending is allowed; the fixed text survives underneath it."""
    artifact = _artifact(additional_limitations="Series covers one regime only.")
    limitations = dict(artifact.content)["known_limitations"]

    assert "Series covers one regime only." in limitations
    assert "optimistic" in limitations.lower()


def test_two_reviews_at_different_thresholds_do_not_share_a_hash():
    """Alpha is inside the signature, so a review run at 0.05 and one run at
    0.01 are distinguishable records rather than the same record twice."""
    loose = _artifact(alpha=0.05)
    strict = _artifact(alpha=0.01)

    assert loose.integrity_hash != strict.integrity_hash


def test_the_significance_artifact_is_graded_research_not_historical():
    """F-033 / Part 35a: Level C needs provenance, and this path cannot have it.

    `significance_artifact` takes `data_source` as a bare string and builds its own
    `Disclosure`, so nothing about it can come from a stored fetch. It therefore
    answers Level D — which is correct, and is **F-003 made visible in the grade**
    rather than a new defect.

    **This test exists because nothing asserted it.** ADR-017's draft stated the
    Level D consequence as fact while
    `grep -n "EvidenceLevel\\|\\.level" tests/metrics/test_significance.py` returned
    nothing — a claim in a governing document resting on no test, which is F-019's
    and F-032's shape. Found by the third independent pass on that work.

    It goes red the day this path learns real provenance, which is the right moment
    to revisit both this test and ADR-017's consequence list.
    """
    artifact = _artifact()

    assert artifact.evidence_level is EvidenceLevel.RESEARCH
    assert [record.level for record in artifact.evidence] == [EvidenceLevel.RESEARCH]
    assert ArtifactValidator().validate(artifact) is True
