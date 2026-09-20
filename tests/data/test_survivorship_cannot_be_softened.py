"""The survivorship disclosure cannot be substituted by a caller. ADR-013 rule 5.

**Written because an independent verification pass proved it could be.** The
first implementation of `fetch_record()` and `disclosure_from()` took
`survivorship` as a free parameter and `source_name` as a string, and never
consulted the source. Passing a fabricated `RETAINED / RETAINED` disclosure
together with the real source's name produced a signed artifact whose
`known_limitations` said nothing about survivorship at all.

**The module constant was un-overridable and that was not the guarantee.** Rule 5
says the answer is "a fixed constant on every artifact **derived from the
source**". Fixing the constant while letting the caller choose which disclosure
object carries it achieves the identical suppression one layer up — the
`known_limitations` string could be replaced with a clean one by whoever found
the real one inconvenient, which is precisely the artifact ADR-011 rule 9 and
ADR-012 rule 7 exist to make impossible.

**The test that was supposed to catch this asserted nothing.** It checked that
`DoltHubStocksSource(survivorship="clean")` raises `TypeError` — which it does,
because `__init__` accepts no such keyword, and which would pass identically for
any misspelled argument. The test carried the strongest statement of the
guarantee in the suite and defended none of it.

So: the provenance functions now take the **source object**, not its name, and
read the disclosure off it. There is no parameter to pass a different one.
"""

from __future__ import annotations

import inspect
import tempfile
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from framework.data.contract import DailyBar, DailyBarSeries, FetchedSeries, InstrumentClass, MarketDataSource
from framework.data.fetch_record import disclosure_from, fetch_record
from framework.data.store import SeriesStore
from framework.data.survivorship import Retention, SurvivorshipDisclosure
from framework.metrics.reporting import SamplePeriod

HONEST = SurvivorshipDisclosure(
    delisted_prices=Retention.SURVIVORS_ONLY,
    delisted_universe_membership=Retention.PARTIAL,
    basis="Established by query: COH returns no bars where AAPL returns bars.",
)

FLATTERING = SurvivorshipDisclosure(
    delisted_prices=Retention.RETAINED,
    delisted_universe_membership=Retention.RETAINED,
    basis="trust me",
)

BARS = (
    DailyBar(
        date=date(2024, 1, 2),
        open=Decimal("10.00"),
        high=Decimal("11.00"),
        low=Decimal("9.50"),
        close=Decimal("10.75"),
        volume=1_000,
    ),
)

SERIES = DailyBarSeries(symbol="AAPL", bars=BARS)
REQUESTED = SamplePeriod(start=date(2024, 1, 1), end=date(2024, 1, 31))


class BiasedSource(MarketDataSource):
    name = "a survivor-only source"
    key = "biased"

    def supported_instruments(self) -> frozenset[InstrumentClass]:
        return frozenset({InstrumentClass.EQUITY})

    def _fetch_daily_bars(self, symbol, start, end) -> FetchedSeries:
        return FetchedSeries(series=SERIES, payload=b"raw")


SOURCE = BiasedSource(survivorship=HONEST)

# The store entry every record below names. ADR-014 rule 6 made `stored`
# required, and it is supplied here as a *valid* pairing on purpose: these tests
# assert that a fabricated disclosure is refused, and a record that raised
# because its store argument was missing would pass them for the wrong reason.
STORED = SeriesStore(
    root=Path(tempfile.mkdtemp(prefix="belay-survivorship-tests-"))
).store(source="biased", symbol="AAPL", payload=b"raw")


# ------------------------------------------------- there is no parameter to pass


def test_the_fetch_record_takes_no_survivorship_parameter():
    """The structural guarantee. A parameter that does not exist cannot be
    supplied a kinder value, which is a stronger property than validating one."""
    parameters = inspect.signature(fetch_record).parameters

    assert "survivorship" not in parameters
    assert "source_name" not in parameters, (
        "taking the name rather than the source is what allowed a fabricated "
        "disclosure to be paired with a real source's name"
    )


def test_the_derived_disclosure_takes_no_survivorship_parameter():
    parameters = inspect.signature(disclosure_from).parameters

    assert "survivorship" not in parameters
    assert "source_name" not in parameters


# ------------------------------------------------ the source's own answer wins


def test_the_fetch_record_carries_the_sources_disclosure():
    record = fetch_record(
        identifier="RPT-0100",
        source=SOURCE,
        symbol="AAPL",
        requested=REQUESTED,
        series=SERIES,
        payload=b"raw",
        stored=STORED,
    )
    content = dict(record.content)

    assert content["survivorship_delisted_prices"] == Retention.SURVIVORS_ONLY.value
    assert "inflates" in content["known_limitations"].lower()


def test_a_second_source_with_a_kinder_answer_does_not_change_the_first():
    """The disclosure follows the source, so two sources produce two different
    records — which is the behaviour that makes the record worth reading."""
    clean = BiasedSource(survivorship=FLATTERING)

    biased_record = fetch_record(
        identifier="RPT-0100",
        source=SOURCE,
        symbol="AAPL",
        requested=REQUESTED,
        series=SERIES,
        payload=b"raw",
        stored=STORED,
    )
    clean_record = fetch_record(
        identifier="RPT-0101",
        source=clean,
        symbol="AAPL",
        requested=REQUESTED,
        series=SERIES,
        payload=b"raw",
        stored=STORED,
    )

    assert "inflates" in dict(biased_record.content)["known_limitations"].lower()
    assert "inflates" not in dict(clean_record.content)["known_limitations"].lower()


def test_the_metric_disclosure_carries_the_sources_answer():
    """`disclosure_from` is what puts survivorship onto every *metric*, which is
    what a promotion gate actually reads."""
    disclosure = disclosure_from(
        source=SOURCE, series=SERIES, assumptions="Daily closes."
    )

    assert disclosure.data_source == SOURCE.name
    assert "inflates" in disclosure.known_limitations.lower()


def test_additional_limitations_are_appended_never_substituted():
    """A caller may add what they know without removing what rule 5 requires."""
    disclosure = disclosure_from(
        source=SOURCE,
        series=SERIES,
        assumptions="Daily closes.",
        additional_limitations="Covers one regime only.",
    )

    assert "Covers one regime only." in disclosure.known_limitations
    assert "inflates" in disclosure.known_limitations.lower()


# ---------------------------------------------- the source cannot be hollowed out


def test_a_source_that_skipped_super_init_is_refused():
    """The previous claim — "there is no path by which an unanswered source
    reaches a backtest" — was not true of a subclass that overrides `__init__`
    without calling `super().__init__`. It fetched bars happily and carried no
    `survivorship` attribute at all, so the guard existed only for the ordinary
    path."""

    class Hollow(BiasedSource):
        def __init__(self):  # deliberately does not call super().__init__
            pass

    with pytest.raises((TypeError, AttributeError)):
        fetch_record(
            identifier="RPT-0100",
            source=Hollow(),
            symbol="AAPL",
            requested=REQUESTED,
            series=SERIES,
            payload=b"raw",
        )


def test_the_disclosure_cannot_be_reassigned_after_construction():
    """`self.survivorship` was a plain attribute on a non-frozen class, so
    `source.survivorship = clean` worked after construction — the same
    suppression by a different route."""
    source = BiasedSource(survivorship=HONEST)

    with pytest.raises(AttributeError):
        source.survivorship = FLATTERING
