"""Student's t distribution, pinned against published critical values. ADR-012 rule 5.

**These tests are the whole justification for implementing a distribution rather
than importing one.** `scipy` is neither installed nor declared in
`pyproject.toml`, and Immutable Law II prohibits black-box reasoning — "the
library said so" is the answer it forbids. Thirty-five lines of standard
numerical code are only more explainable than a dependency if someone can check
them, so the reference values below are taken from a **published t-table**
rather than from another implementation.

That distinction matters. Testing one implementation against another proves the
two agree; testing against a printed table proves the implementation is right.

The table values are quoted to three decimal places, so the observed deviation
is bounded by the table's own rounding rather than by the algorithm — the worst
across all fifteen is 7.5e-05, which is why the tolerance is 2e-04 rather than
something looser.
"""

from __future__ import annotations

import statistics as stdlib_statistics

import pytest

from framework.metrics.distributions import student_t_two_sided_p, t_critical_value

# (degrees of freedom, two-sided alpha, critical t) from a published Student's t
# table. Read as: with this many degrees of freedom, |t| exceeds this value with
# probability alpha when the null is true.
PUBLISHED_CRITICAL_VALUES = [
    (1, 0.05, 12.706),
    (2, 0.05, 4.303),
    (5, 0.05, 2.571),
    (10, 0.05, 2.228),
    (20, 0.05, 2.086),
    (30, 0.05, 2.042),
    (60, 0.05, 2.000),
    (1, 0.01, 63.657),
    (5, 0.01, 4.032),
    (10, 0.01, 3.169),
    (20, 0.01, 2.845),
    (30, 0.01, 2.750),
    (5, 0.10, 2.015),
    (10, 0.10, 1.812),
    (30, 0.10, 1.697),
]

TABLE_TOLERANCE = 2e-4


@pytest.mark.parametrize(
    "degrees_of_freedom,alpha,critical_t", PUBLISHED_CRITICAL_VALUES
)
def test_the_p_value_reproduces_the_published_table(
    degrees_of_freedom, alpha, critical_t
):
    """Feed the table's critical value in; the table's alpha must come out."""
    assert student_t_two_sided_p(critical_t, degrees_of_freedom) == pytest.approx(
        alpha, abs=TABLE_TOLERANCE
    )


@pytest.mark.parametrize(
    "degrees_of_freedom,alpha,critical_t", PUBLISHED_CRITICAL_VALUES
)
def test_the_critical_value_reproduces_the_published_table(
    degrees_of_freedom, alpha, critical_t
):
    """And the inverse direction, which is what confidence intervals need."""
    assert t_critical_value(alpha, degrees_of_freedom) == pytest.approx(
        critical_t, abs=1e-3
    )


def test_a_t_of_zero_is_certain_to_be_exceeded():
    """P(|T| > 0) = 1. The observed mean sitting exactly on the null is the least
    surprising result available, and a p-value of 1 says so."""
    assert student_t_two_sided_p(0.0, 10) == pytest.approx(1.0)


def test_the_distribution_is_symmetric():
    """Two-sided, so the sign of t cannot matter. A one-sided implementation
    would fail here, and rule 4 rejected one-sided deliberately."""
    assert student_t_two_sided_p(-2.228, 10) == pytest.approx(
        student_t_two_sided_p(2.228, 10)
    )


def test_a_larger_t_is_less_probable():
    values = [student_t_two_sided_p(t, 10) for t in (0.5, 1.0, 2.0, 4.0, 8.0)]

    assert values == sorted(values, reverse=True)


def test_fewer_degrees_of_freedom_make_the_same_t_less_impressive():
    """The reason rule 5 rejected the normal distribution.

    Student's t has fatter tails at low degrees of freedom, so the same observed
    t is more easily produced by chance on a short sample. At df = 5 a t of 2.0
    is unremarkable; at df = 500 it is close to conventional significance. A
    normal approximation cannot express that difference, and the entire
    sample-adequacy half of ADR-012 is about short samples.
    """
    short = student_t_two_sided_p(2.0, 5)
    long = student_t_two_sided_p(2.0, 500)

    assert short > long
    assert short > 0.05  # not significant at conventional alpha
    assert long < 0.05  # significant


def test_it_converges_on_the_normal_distribution():
    """As degrees of freedom grow the t distribution becomes the normal one.

    Checked against `statistics.NormalDist` from the standard library, which is
    an independent implementation of the limit rather than of the t itself. A
    two-sided normal p at t = 1.96 is the textbook 0.05.
    """
    normal_two_sided = 2.0 * (1.0 - stdlib_statistics.NormalDist().cdf(1.96))

    assert student_t_two_sided_p(1.96, 1_000_000) == pytest.approx(
        normal_two_sided, abs=1e-5
    )
    assert normal_two_sided == pytest.approx(0.05, abs=1e-3)


def test_an_extreme_t_does_not_underflow_to_a_negative_probability():
    """A p-value is a probability. Continued-fraction expansions can drift
    outside [0, 1] near the extremes, and a negative p-value would compare
    against alpha as "overwhelmingly significant" rather than as broken."""
    for t in (30.0, 100.0, 1000.0):
        p = student_t_two_sided_p(t, 3)
        assert 0.0 <= p <= 1.0


@pytest.mark.parametrize("degrees_of_freedom", [0, -1, -10])
def test_degrees_of_freedom_must_be_positive(degrees_of_freedom):
    """Zero degrees of freedom means a single observation, which cannot support
    a test at all. ADR-012 rule 9 refuses it rather than answering."""
    with pytest.raises(ValueError, match="degrees of freedom"):
        student_t_two_sided_p(2.0, degrees_of_freedom)


@pytest.mark.parametrize("alpha", [0.0, 1.0, -0.1, 1.5])
def test_a_critical_value_needs_a_probability(alpha):
    with pytest.raises(ValueError, match="between 0 and 1"):
        t_critical_value(alpha, 10)


def test_the_critical_value_inverts_the_p_value():
    """The two functions are each other's inverse, which is the property the
    confidence interval and the sample-adequacy calculation both rely on."""
    for alpha in (0.001, 0.01, 0.05, 0.10, 0.5):
        for degrees_of_freedom in (1, 4, 12, 75):
            critical = t_critical_value(alpha, degrees_of_freedom)
            assert student_t_two_sided_p(
                critical, degrees_of_freedom
            ) == pytest.approx(alpha, rel=1e-6)
