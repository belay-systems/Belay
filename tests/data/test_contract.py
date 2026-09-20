"""The market data boundary contract. ADR-013 rules 2, 6 and 9.

**Why there is a contract at all rather than one fetcher.** ADR-011's central
holding, extended: a single hard-coded fetcher does not avoid the ruling about
how many sources there can be, it *makes* that ruling silently — that there is
only ever one, and that its survivorship properties are whatever they happen to
be. `docs/ROADMAP.md` Stage 2's deliverable is "a defined boundary", and a
boundary is an adapter contract.

**Why it expresses options when only equities are implemented.**
`constitution/Operational_Constraints.md:25-27` — "No asset class, security, or
investment methodology possesses inherent preference." A contract that can only
express an equity price series does not merely omit options; it gives equities
inherent preference *by construction*, because a strategy needing option data
could not be expressed at all. Deferring the implementation is fine and is what
rule 6 does. Deferring the expressibility is not.

**Why an unsupported instrument raises rather than returns empty.** An empty
chain is indistinguishable from "this underlying had no options that day", and a
silent wrong answer in the survivorship direction is the whole failure mode this
rule set exists to prevent.

**Why there is no shared base class with execution.** Rule 2, on
`constitution/Immutable_Laws.md:45` (Law VI) — "Research and execution remain
independent." Retrying is *how* a data fetch recovers from a dropped connection;
a retried order submit doubles a position. A shared base must pick one default
and be wrong for the other.
"""

from __future__ import annotations

import inspect
from datetime import date
from decimal import Decimal

import pytest

from framework.data.contract import (
    DailyBar,
    DailyBarSeries,
    FetchedSeries,
    InstrumentClass,
    InstrumentNotSupported,
    MarketDataSource,
    OptionChain,
    OptionQuote,
    OptionRight,
)
from framework.data.survivorship import Retention, SurvivorshipDisclosure

DISCLOSURE = SurvivorshipDisclosure(
    delisted_prices=Retention.SURVIVORS_ONLY,
    delisted_universe_membership=Retention.PARTIAL,
    basis="Established by query against the source.",
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
    DailyBar(
        date=date(2024, 1, 3),
        open=Decimal("10.75"),
        high=Decimal("12.00"),
        low=Decimal("10.50"),
        close=Decimal("11.80"),
        volume=1_500,
    ),
)


class EquityOnlySource(MarketDataSource):
    """An adapter that supports equities and says so. Rule 6's normal case."""

    name = "test equity source"

    def supported_instruments(self) -> frozenset[InstrumentClass]:
        return frozenset({InstrumentClass.EQUITY})

    def _fetch_daily_bars(self, symbol, start, end) -> FetchedSeries:
        return FetchedSeries(
            series=DailyBarSeries(symbol=symbol, bars=BARS), payload=b"raw"
        )


class BothSource(EquityOnlySource):
    """An adapter that supports both, to prove the contract can express both."""

    name = "test dual source"

    def supported_instruments(self) -> frozenset[InstrumentClass]:
        return frozenset({InstrumentClass.EQUITY, InstrumentClass.OPTION})

    def _fetch_option_chain(self, underlying, as_of) -> OptionChain:
        return OptionChain(
            underlying=underlying,
            as_of=as_of,
            quotes=(
                OptionQuote(
                    expiration=date(2024, 3, 15),
                    strike=Decimal("70.00"),
                    right=OptionRight.CALL,
                    bid=Decimal("10.85"),
                    ask=Decimal("11.65"),
                ),
            ),
        )


# --------------------------------------------------------------- rule 9


def test_a_source_cannot_be_built_without_survivorship_answers():
    """Rule 9, and the reason it is enforced at construction rather than at
    fetch time: a source that has not answered cannot be handed to anything, so
    there is no path by which an unanswered source reaches a backtest."""
    with pytest.raises(TypeError):
        EquityOnlySource()  # type: ignore[call-arg]


def test_a_source_refuses_a_survivorship_answer_that_is_not_one():
    with pytest.raises((TypeError, ValueError)):
        EquityOnlySource(survivorship="probably fine")  # type: ignore[arg-type]


def test_the_survivorship_disclosure_is_reachable_from_the_source():
    """It has to travel onto every artifact derived from the source, so the
    source has to carry it rather than the caller remembering it."""
    source = EquityOnlySource(survivorship=DISCLOSURE)

    assert source.survivorship is DISCLOSURE


# --------------------------------------------------------------- rule 6


def test_the_contract_names_both_asset_classes():
    """`constitution/Operational_Constraints.md:25-27`. The vocabulary exists
    even where the implementation does not."""
    assert {member for member in InstrumentClass} == {
        InstrumentClass.EQUITY,
        InstrumentClass.OPTION,
    }


def test_the_contract_declares_an_option_operation():
    """Expressibility is the thing rule 6 refuses to defer. If this method did
    not exist, an options strategy could not be written against the boundary at
    all, which is inherent preference by construction."""
    assert hasattr(MarketDataSource, "fetch_option_chain")


def test_an_equity_only_source_refuses_options_explicitly():
    """Not an empty chain. An empty result is indistinguishable from "no options
    traded", and would be a silent wrong answer."""
    source = EquityOnlySource(survivorship=DISCLOSURE)

    with pytest.raises(InstrumentNotSupported, match="Option"):
        source.fetch_option_chain("AAPL", as_of=date(2024, 1, 2))


def test_a_source_supporting_both_returns_a_chain():
    """The contract is genuinely capable of expressing options; the equity-only
    refusal above is a property of that adapter, not of the boundary."""
    chain = BothSource(survivorship=DISCLOSURE).fetch_option_chain(
        "AAPL", as_of=date(2024, 1, 2)
    )

    assert chain.underlying == "AAPL"
    assert chain.quotes[0].right is OptionRight.CALL


def test_a_fetch_returns_the_bytes_alongside_the_parsed_series():
    """ADR-013 rule 3 signs a hash of the bytes the source returned, so a fetch
    that discarded them could not produce the record the rule requires."""
    fetched = EquityOnlySource(survivorship=DISCLOSURE).fetch_daily_bars(
        "AAPL", start=date(2024, 1, 1), end=date(2024, 1, 31)
    )

    assert fetched.payload == b"raw"
    assert fetched.series.symbol == "AAPL"


def test_a_series_and_a_chain_are_different_shapes():
    """Rule 6: "They are two shapes, not one shape with a flag." A price series
    is one instrument over time. A chain is, for one date, many contracts each
    with a strike, an expiry and a right. One is a sequence; the other is a
    sequence of sets."""
    series = DailyBarSeries(symbol="AAPL", bars=BARS)
    chain = BothSource(survivorship=DISCLOSURE).fetch_option_chain(
        "AAPL", as_of=date(2024, 1, 2)
    )

    assert not hasattr(series, "as_of")
    assert not hasattr(chain, "bars")


# --------------------------------------------------------------- rule 2


def test_the_contract_shares_no_base_class_with_anything_else():
    """Rule 2. `MarketDataSource` inherits from `ABC` and nothing else — the
    moment a shared `Adapter` base appears above it, market data and execution
    are coupled across a boundary Law VI declares independent."""
    bases = [base.__name__ for base in MarketDataSource.__mro__]

    assert bases == ["MarketDataSource", "ABC", "object"]


def test_the_contract_has_no_execution_vocabulary():
    """An interface designed for reads has no vocabulary for idempotency,
    partial fills, cancel-in-flight or a halt path — and it must not acquire
    one, because that is how the dangerous contract gets designed in the
    language of the safe one."""
    methods = {
        name for name, _ in inspect.getmembers(MarketDataSource, inspect.isfunction)
    }
    forbidden = {"submit", "cancel", "place_order", "halt", "fill", "amend"}

    assert methods & forbidden == set()


# ------------------------------------------------------- the series itself


def test_a_series_reports_the_window_it_actually_covers():
    """Rule 7's landing point. The window is derived from the bars rather than
    stated alongside them, so a series cannot claim coverage it does not have."""
    period = DailyBarSeries(symbol="AAPL", bars=BARS).period()

    assert period.start == date(2024, 1, 2)
    assert period.end == date(2024, 1, 3)


def test_an_empty_series_has_no_window_to_report():
    """Nothing was covered, and inventing a window for it would be a fabricated
    disclosure — the objection ADR-005 rule 4 raised against defaulting
    confidence to 0.5."""
    with pytest.raises(ValueError, match="empty"):
        DailyBarSeries(symbol="AAPL", bars=()).period()


def test_a_series_is_not_an_artifact():
    """Rule 3, asserted rather than assumed. The eight identifier prefixes and
    the nine `ArtifactType` members between them have no name for market data,
    so a series carrying an artifact's shape would be manufacturing an identity
    the vocabulary does not have."""
    series = DailyBarSeries(symbol="AAPL", bars=BARS)

    assert not hasattr(series, "integrity_hash")
    assert not hasattr(series, "evidence_level")


def test_bars_must_be_ordered():
    """An out-of-order series makes `period()` wrong and every windowed
    computation silently wrong with it."""
    with pytest.raises(ValueError, match="ord"):
        DailyBarSeries(symbol="AAPL", bars=tuple(reversed(BARS)))


def test_bars_must_not_repeat_a_trading_day():
    """The ordering guard was `dates != sorted(dates)`, which passes duplicates:
    `[d1, d1, d2]` is sorted. Four bars over two trading days were accepted as a
    validated series.

    Not a cosmetic miscount. `period_returns` reads a repeated bar as a return
    of exactly 0.0, and fabricated zeros pull the standard deviation down while
    barely moving the mean — the standard error falls, the t-statistic rises,
    and `significant` flips true on a record that did not earn it. The
    `observations` count on the fetch record and every artifact's `provenance`
    string inherit the inflated count, and nothing anywhere reports it.
    """
    with pytest.raises(ValueError, match="ord"):
        DailyBarSeries(symbol="AAPL", bars=(BARS[0], BARS[0], BARS[1]))


def test_prices_are_decimal_rather_than_float():
    """Money in binary floating point accumulates error that is invisible until
    it is material. The source returns `decimal(14,4)`; nothing in Belay should
    widen that to a float on the way in."""
    assert isinstance(BARS[0].close, Decimal)
