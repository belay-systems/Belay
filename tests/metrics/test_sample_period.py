"""`sample_period` is two dates, not prose. ADR-013 rule 7.

`Disclosure.sample_period` was a free-form `str` validated only as non-blank, so
"last five years" satisfied it. Three things depend on it being
machine-readable, and none of them can parse a sentence:

- **Tax years are calendar-bounded** and the taxable branch is live, so a tax
  year has to be derivable. `docs/DocumentStandard.md:42` exists to prevent
  exactly this defect — "index every document deterministically without parsing
  prose."
- **Rule 4's versioning must compare coverage** between two fetches of the same
  instrument. Two prose strings cannot be compared.
- **Reproducibility.** A backtest that cannot state its exact window cannot be
  re-run.

**The field name does not change, and that is forced rather than chosen.**
`tests/test_governance_conformance.py` parses `Validation/Backtesting.md` and
asserts `Disclosure`'s field *names* are the four the document requires.
Splitting into `sample_period_start` and `sample_period_end` would turn the
suite red against a governing document. So rule 7 changes the field's **type**.

**The cost of doing this now is zero and it was verified rather than assumed.**
`git ls-files "*.yaml"` returns nothing and no artifact exists on disk outside
`.git`, so no signature exists to break. After Stage 2 signs its first artifact
this becomes a migration of permanent append-only records.
"""

from __future__ import annotations

import dataclasses
from dataclasses import FrozenInstanceError
from datetime import date, datetime, timezone

import pytest

from framework.metrics.reporting import Disclosure, SamplePeriod, metric_artifact

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

PERIOD = SamplePeriod(start=date(2019, 1, 2), end=date(2024, 12, 31))


def _disclosure(**overrides) -> Disclosure:
    fields = {
        "assumptions": "No transaction costs, no slippage, no financing charges.",
        "data_source": "unit test fixture",
        "sample_period": PERIOD,
        "known_limitations": "Describes no real instrument.",
    }
    fields.update(overrides)
    return Disclosure(**fields)


def _artifact(**overrides):
    fields = {
        "identifier": "RPT-0001",
        "title": "Sharpe ratio, sample series",
        "metric": "sharpe_ratio",
        "value": 6.6,
        "observations": 5,
        "methodology": "annualized mean excess return over annualized volatility",
        "disclosure": _disclosure(),
        "timestamp": FIXED_TIME,
    }
    fields.update(overrides)
    return metric_artifact(**fields)


# ------------------------------------------------------------ the two dates


def test_a_sample_period_is_two_dates():
    assert PERIOD.start == date(2019, 1, 2)
    assert PERIOD.end == date(2024, 12, 31)


def test_a_sample_period_cannot_be_edited_after_the_fact():
    """Frozen for the reason every record under `framework/` is frozen: the
    artifact is signed over this, and a mutable window would let the period
    behind a published number be rewritten underneath it."""
    with pytest.raises(FrozenInstanceError):
        PERIOD.start = date(2020, 1, 1)


def test_a_period_that_ends_before_it_starts_is_refused():
    """Not a window at all. Accepting it would let a backtest claim a negative
    span, and every coverage comparison built on rule 4 would silently invert."""
    with pytest.raises(ValueError, match="end"):
        SamplePeriod(start=date(2024, 12, 31), end=date(2019, 1, 2))


def test_a_single_day_period_is_legal():
    """A one-day window is a real answer — a daily bar fetch for one date. The
    refusal above is about ordering, not about span."""
    same = SamplePeriod(start=date(2024, 3, 1), end=date(2024, 3, 1))

    assert same.start == same.end


@pytest.mark.parametrize(
    "value",
    ["2019-01-02", "last five years", 2019, None, datetime(2019, 1, 2)],
)
def test_anything_that_is_not_a_date_is_refused(value):
    """Prose is the specific thing rule 7 removes, and it is not the only wrong
    answer. A `datetime` is refused too: its isoformat carries a time component
    that would enter the integrity hash, asserting a precision daily bars do not
    have — and `date` cannot simply be widened, because `datetime` is a subclass
    of `date` and would pass an `isinstance` check unnoticed."""
    with pytest.raises((ValueError, TypeError)):
        SamplePeriod(start=value, end=date(2024, 12, 31))


# --------------------------------------------------- the disclosure block


def test_the_disclosure_still_declares_exactly_the_four_documented_names():
    """The conformance test parses `Validation/Backtesting.md` and holds this
    class to it. Rule 7 changes the type of a field, never the set of names, so
    that check must be unaffected by this migration."""
    names = {field.name for field in dataclasses.fields(Disclosure)}

    assert names == {
        "assumptions",
        "data_source",
        "sample_period",
        "known_limitations",
    }


def test_a_prose_sample_period_no_longer_satisfies_the_disclosure():
    """The whole of rule 7. "last five years" satisfied the old non-blank check
    and is exactly what the rule exists to stop being recordable."""
    with pytest.raises((ValueError, TypeError)):
        _disclosure(sample_period="last five years")


@pytest.mark.parametrize("field", ["assumptions", "data_source", "known_limitations"])
@pytest.mark.parametrize("blank", ["", "   ", "\n"])
def test_the_other_three_disclosures_are_still_refused_when_blank(field, blank):
    """ADR-011 rule 9 is untouched by rule 7. The three string fields keep their
    non-blank check; only `sample_period` stops being a string at all."""
    with pytest.raises(ValueError, match=field):
        _disclosure(**{field: blank})


# ------------------------------------------------------ what reaches the hash


def test_the_artifact_carries_the_window_as_two_encoded_dates():
    """`canonical_digest`'s own docstring asks callers to pass already-encoded
    values — "an enum as `.value`", a timestamp as `.isoformat()` — because
    `str()` of an arbitrary object is not a stable representation. A
    `SamplePeriod` dropped into `content` unrendered would be hashed through
    `default=str`, which is the backstop that docstring warns against relying on.
    """
    content = dict(_artifact().content)

    assert content["sample_period_start"] == "2019-01-02"
    assert content["sample_period_end"] == "2024-12-31"


def test_the_window_is_inside_the_signature():
    """Rule 7's reproducibility reason is only worth stating if the signature
    enforces it. A period that can be widened after signing lets a result that
    covered one year present itself as covering five."""
    original = _artifact()
    wider = _artifact(
        disclosure=_disclosure(
            sample_period=SamplePeriod(start=date(2011, 1, 3), end=date(2024, 12, 31))
        )
    )

    assert original.integrity_hash != wider.integrity_hash


def test_two_identical_windows_hash_identically():
    """Reproducibility, with the timestamp pinned."""
    assert _artifact().integrity_hash == _artifact().integrity_hash


# ------------------------------------------- the reasons the rule gives for itself


def test_the_tax_year_is_derivable_without_parsing_prose():
    """`docs/DocumentStandard.md:42` — "index every document deterministically
    without parsing prose." This is the defect the rule names first.

    **Asserted against the prose form, not over the fixture's own literals.**
    The first version of this test was `assert period.start.year ==
    period.end.year == 2023`, a tautology that would pass unchanged if
    `SamplePeriod.__post_init__` were deleted — one of two tests named after the
    rule's justifications that asserted nothing about the implementation.
    """
    spanning = SamplePeriod(start=date(2023, 11, 1), end=date(2024, 2, 28))

    # The point: a tax-year question has an answer here and does not in prose.
    assert {spanning.start.year, spanning.end.year} == {2023, 2024}

    with pytest.raises((ValueError, TypeError)):
        SamplePeriod(start="the 2023 tax year", end="the 2023 tax year")


def test_coverage_between_two_fetches_is_comparable():
    """Rule 4's versioning reason. Two prose strings cannot be compared; two
    windows can, which is what makes a re-fetch checkable against the original.

    **The comparison that matters is "did the second fetch cover the first",**
    not `date.__gt__`. The earlier version asserted only `extended.end >
    first.end`, which tests the standard library.
    """
    first = SamplePeriod(start=date(2019, 1, 2), end=date(2024, 12, 31))
    extended = SamplePeriod(start=date(2019, 1, 2), end=date(2025, 12, 31))
    shifted = SamplePeriod(start=date(2020, 1, 2), end=date(2025, 12, 31))

    def covers(outer: SamplePeriod, inner: SamplePeriod) -> bool:
        return outer.start <= inner.start and outer.end >= inner.end

    assert covers(extended, first)
    assert not covers(shifted, first), (
        "a later window that starts after the original does not cover it, and a "
        "re-fetch that quietly lost the early years must not read as a superset"
    )
    assert not covers(first, extended)
