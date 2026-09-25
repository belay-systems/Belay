"""Student's t distribution. ADR-012 rule 5.

**Why this exists rather than a dependency.** Belay needs one function — the
probability that a t-statistic this large arises by chance — and `scipy` is
neither installed nor declared in `pyproject.toml`. Adding it would be a large
dependency for a small need, and a less explainable one: Immutable Law II
prohibits black-box reasoning, and "the library said so" is the answer it
forbids. Thirty-five lines a reviewer can check against a printed t-table are
explainable in the sense Law II means.

`numpy` is not used either, and **since 2026-09-25 it is not installed at all.**
It used to arrive as a transitive dependency of `pandas` while appearing nowhere
in `pyproject.toml`; the owner ruled `pandas` removed and `numpy` not declared in
its place (F-036, `docs/OwnerDecisions.md` Part 35c and 35d). Building on a
package nobody declared is the 2026-07-26 defect from the other side — there
`pyyaml` was declared but not installed, and `ArtifactRepository.save()` had
never once executed while the suite reported 46 passing. Either direction is the
same error, so if numerical work later wants `numpy`, declare it first.

**This module is a leaf. It imports nothing from Belay**, the same shape as
`framework/artifacts/primitives.py` and for the same reason: it is arithmetic
with no opinion about strategies, artifacts or capital, and nothing here should
ever acquire one.

The correctness argument is entirely in `tests/metrics/test_distributions.py`,
which pins fifteen values against a **published** t-table rather than against
another implementation. Testing one implementation against another proves the
two agree; testing against a printed table proves this one is right.
"""

from __future__ import annotations

import math

# Continued-fraction controls. 300 iterations is far more than the expansion
# needs anywhere it is used here — convergence is typically inside 30 — and the
# cap exists so a pathological input terminates rather than spins.
_MAX_ITERATIONS = 300
_EPSILON = 3.0e-16
_TINY = 1.0e-300


def _beta_continued_fraction(a: float, b: float, x: float) -> float:
    """Evaluate the continued fraction for the incomplete beta function.

    Lentz's algorithm with the modification that guards against a zero
    denominator by clamping to `_TINY` rather than dividing by it. Standard
    numerical-recipes material; the variable names are kept terse because the
    recurrence is only readable as a recurrence.
    """
    qab = a + b
    qap = a + 1.0
    qam = a - 1.0

    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < _TINY:
        d = _TINY
    d = 1.0 / d
    result = d

    for m in range(1, _MAX_ITERATIONS + 1):
        m2 = 2 * m

        # Even step.
        numerator = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + numerator * d
        if abs(d) < _TINY:
            d = _TINY
        c = 1.0 + numerator / c
        if abs(c) < _TINY:
            c = _TINY
        d = 1.0 / d
        result *= d * c

        # Odd step.
        numerator = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + numerator * d
        if abs(d) < _TINY:
            d = _TINY
        c = 1.0 + numerator / c
        if abs(c) < _TINY:
            c = _TINY
        d = 1.0 / d
        delta = d * c
        result *= delta

        if abs(delta - 1.0) < _EPSILON:
            break

    return result


def _regularized_incomplete_beta(a: float, b: float, x: float) -> float:
    """Return I_x(a, b), the regularized incomplete beta function.

    The continued fraction converges quickly only for x below the distribution's
    centre, so the symmetry I_x(a,b) = 1 - I_(1-x)(b,a) is used above it. Both
    branches are exercised by the published-table tests, at high and low
    degrees of freedom.
    """
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0

    # Computed in log space. The direct form overflows for the degrees of
    # freedom this is called with — df/2 reaches 500,000 in the normal-limit
    # test — and `math.lgamma` is exact where `math.gamma` is not finite.
    front = math.exp(
        math.lgamma(a + b)
        - math.lgamma(a)
        - math.lgamma(b)
        + a * math.log(x)
        + b * math.log(1.0 - x)
    )

    if x < (a + 1.0) / (a + b + 2.0):
        return front * _beta_continued_fraction(a, b, x) / a
    return 1.0 - front * _beta_continued_fraction(b, a, 1.0 - x) / b


def student_t_two_sided_p(t: float, degrees_of_freedom: int) -> float:
    """Return P(|T| > |t|) for Student's t with `degrees_of_freedom`.

    The two-sided p-value: the probability of observing a t-statistic at least
    this far from zero **in either direction** when the null hypothesis is true.

    Two-sided by ADR-012 rule 4. A one-sided test halves this number and does so
    by assuming the sign of the effect — which is the thing under examination.
    `Validation/README.md:11`: "Validation seeks flaws."

    Zero degrees of freedom means a single observation, which cannot support a
    test at all, so it is refused rather than answered — ADR-012 rule 9.

    The result is clamped to [0, 1]. A continued-fraction expansion can drift a
    few ulps outside the interval at the extremes, and a negative p-value would
    compare against alpha as overwhelming significance rather than as a bug.
    """
    if degrees_of_freedom < 1:
        raise ValueError(
            f"degrees of freedom must be at least 1, got {degrees_of_freedom}; "
            "a single observation supports no test"
        )

    df = float(degrees_of_freedom)
    p = _regularized_incomplete_beta(df / 2.0, 0.5, df / (df + t * t))
    return min(1.0, max(0.0, p))


def t_critical_value(alpha: float, degrees_of_freedom: int) -> float:
    """Return the t at which the two-sided p-value equals `alpha`.

    The inverse of `student_t_two_sided_p`, found by bisection rather than by a
    closed form. Bisection is slower and is chosen deliberately: it is obviously
    correct by inspection, it cannot diverge, and it inherits its accuracy from
    the function it inverts, which is the function pinned against the published
    table. Nothing here is on a hot path.

    Used by the confidence interval and by ADR-012 rule 8's sample-adequacy
    calculation, both of which need to go from a chosen alpha to a threshold.
    """
    if not 0.0 < alpha < 1.0:
        raise ValueError(f"alpha must be a probability between 0 and 1, got {alpha}")

    # p is 1 at t = 0 and decreases monotonically towards 0, so the root is
    # bracketed by [0, high] for any high with p(high) < alpha. 1e6 is beyond
    # any t a return series produces; the loop that grows it is a guard rather
    # than an expected path.
    low, high = 0.0, 1.0e6
    while student_t_two_sided_p(high, degrees_of_freedom) > alpha:
        high *= 10.0

    for _ in range(200):
        middle = (low + high) / 2.0
        if student_t_two_sided_p(middle, degrees_of_freedom) > alpha:
            low = middle
        else:
            high = middle

    return (low + high) / 2.0
