"""A second adapter, to prove the contract is genuinely swappable. ADR-013 rule 2.

**Why this exists.** Rule 2 rules the contract first precisely so the vendor
choice stays reversible — "which vendor is implemented first" was deliberately
left unsettled as "a licence and coverage question to settle against a current
price list at implementation time, not a doctrine question". A contract with one
implementation has not been shown to be a contract at all; it may just be that
implementation's shape written twice. This adapter is the check.

**IMPORTANT: this has never been run against the live IBKR API**, and cannot be
from here — it needs a funded account and a paid market data subscription. Every
test below runs against a fixture shaped like IBKR's documented response. What
it proves is that the *contract* accommodates a second, structurally different
vendor: different transport, different response shape, different survivorship
answers, different failure modes. What it does not prove is that the wire format
is right. That is recorded rather than glossed, because asserting verified
behaviour Belay has not observed is the failure ADR-013's own Status block was
written about.

**Using the broker as the data source does not violate rule 2.** Rule 2 forbids
a shared *abstraction* — one interface for reads and writes, which must pick one
retry default and be wrong for the other. It says nothing about the vendor
behind each. `MarketDataSource` has no order vocabulary and never will; an
execution contract, when it exists, will be a separate type.

**Survivorship, from IBKR's own documentation rather than from a vendor claim:**
`interactivebrokers.github.io/tws-api/historical_data.html` states "if data is
not available for a specific instrument, data type, or period within a TWS chart
it will also not be available from the API". A delisted instrument has no TWS
chart, so it has no API history — the same survivor-only limitation the free
source has, at a price. The same page states "the API always requires Level 1
streaming real time data to return historical data", so historical data is not
included with an account.
"""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal

import pytest

from framework.data.contract import InstrumentClass, InstrumentNotSupported
from framework.data.ibkr import (
    IBKR_SURVIVORSHIP,
    IbkrHistoricalSource,
    IbkrUnavailable,
)
from framework.data.survivorship import Retention

# Shaped as IBKR's Client Portal `/iserver/marketdata/history` returns: an
# epoch-milliseconds `t`, and OHLCV under single-letter keys. Structurally
# unlike DoltHub's row-of-strings, which is the point of the exercise.
SUCCESS = json.dumps(
    {
        "symbol": "AAPL",
        "text": "APPLE INC",
        "barLength": 86400,
        "data": [
            {
                "t": 1704171600000,  # 2024-01-02
                "o": 187.15,
                "h": 188.44,
                "l": 183.89,
                "c": 185.64,
                "v": 82488.0,
            },
            {
                "t": 1704258000000,  # 2024-01-03
                "o": 184.22,
                "h": 185.88,
                "l": 183.43,
                "c": 184.25,
                "v": 58414.0,
            },
        ],
    }
).encode("utf-8")

NO_SUBSCRIPTION = json.dumps(
    {"error": "No market data permissions for ISLAND STK"}
).encode("utf-8")

EMPTY = json.dumps({"symbol": "COH", "data": []}).encode("utf-8")


class Recorder:
    def __init__(self, response: bytes = SUCCESS) -> None:
        self.response = response
        self.urls: list[str] = []

    def __call__(self, url: str) -> bytes:
        self.urls.append(url)
        return self.response


def _source(response: bytes = SUCCESS):
    transport = Recorder(response)
    return IbkrHistoricalSource(transport=transport), transport


# ------------------------------------------------ the contract accommodates it


def test_a_second_vendor_satisfies_the_same_contract():
    """The whole point. If this needed a change to `MarketDataSource`, the
    contract was really the DoltHub adapter's shape wearing a general name."""
    from framework.data.contract import MarketDataSource

    source, _ = _source()

    assert isinstance(source, MarketDataSource)


def test_it_returns_the_same_series_type_from_a_different_wire_format():
    """IBKR returns epoch milliseconds and floats under single-letter keys;
    DoltHub returns ISO dates and decimal strings. Both must arrive as the same
    `DailyBarSeries`, or downstream code would have to know which vendor it is
    talking to — which is the coupling the boundary exists to remove."""
    source, _ = _source()

    series = source.fetch_daily_bars(
        "AAPL", start=date(2024, 1, 1), end=date(2024, 1, 31)
    ).series

    assert series.symbol == "AAPL"
    assert [bar.date for bar in series.bars] == [date(2024, 1, 2), date(2024, 1, 3)]


def test_prices_are_decimal_even_though_the_vendor_sends_floats():
    """IBKR sends JSON numbers, which Python parses as float. Converting via
    `str` rather than `Decimal(float)` avoids inheriting the binary
    representation error — `Decimal(185.64)` is not 185.64."""
    source, _ = _source()

    close = source.fetch_daily_bars(
        "AAPL", start=date(2024, 1, 1), end=date(2024, 1, 31)
    ).series.bars[0].close

    assert isinstance(close, Decimal)
    assert close == Decimal("185.64")


def test_the_payload_is_the_bytes_the_vendor_returned():
    """Rule 3 is vendor-independent."""
    source, _ = _source()

    fetched = source.fetch_daily_bars(
        "AAPL", start=date(2024, 1, 1), end=date(2024, 1, 31)
    )

    assert fetched.payload == SUCCESS


def test_it_declares_equities_only():
    source, _ = _source()

    assert source.supported_instruments() == frozenset({InstrumentClass.EQUITY})

    with pytest.raises(InstrumentNotSupported):
        source.fetch_option_chain("AAPL", as_of=date(2024, 1, 2))


# --------------------------------------------------------------- rule 9


def test_the_survivorship_answers_come_from_ibkrs_own_documentation():
    """Prices survivor-only: "if data is not available ... within a TWS chart it
    will also not be available from the API", and a delisted instrument has no
    chart.

    Universe membership UNKNOWN rather than assumed: nothing located states
    whether IBKR can report historical index membership, and rule 9 makes
    "unknown" a legitimate answer that must be *stated* — inferring a favourable
    answer is the failure that flatters."""
    assert IBKR_SURVIVORSHIP.delisted_prices is Retention.SURVIVORS_ONLY
    assert IBKR_SURVIVORSHIP.delisted_universe_membership is Retention.UNKNOWN


def test_paying_for_data_does_not_remove_the_disclosure():
    """The finding that decided the vendor question: IBKR costs money and buys
    the same survivorship limitation. An artifact derived from it must say so
    just as loudly as one derived from the free source."""
    limitations = IBKR_SURVIVORSHIP.known_limitations().lower()

    assert "inflates" in limitations
    assert "deflates" in limitations


def test_the_constructor_takes_no_survivorship_argument():
    """See the note on the DoltHub equivalent: this checks the constructor only.
    The substitution guarantee is tested in
    `tests/data/test_survivorship_cannot_be_softened.py`."""
    import inspect

    assert "survivorship" not in inspect.signature(IbkrHistoricalSource).parameters
    assert _source()[0].survivorship is IBKR_SURVIVORSHIP


def test_the_basis_records_that_this_is_unverified_against_the_live_api():
    """Belay has never run this against IBKR. Recording that inside the basis
    means it travels onto every artifact rather than living in a comment nobody
    reads at the point the number is used."""
    assert "not been verified" in IBKR_SURVIVORSHIP.basis.lower()


def test_the_source_name_records_that_a_paid_subscription_is_required():
    """`Disclosure.data_source` is inside the integrity hash, and "which data
    entitlement produced this" is exactly the kind of fact a later reviewer
    cannot reconstruct."""
    source, _ = _source()

    assert "Level 1" in source.name


# --------------------------------------------------------------- failure


def test_a_missing_subscription_is_raised_rather_than_read_as_no_data():
    """The most likely real failure, and the most dangerous: an entitlement
    error that reads as an empty series would look exactly like a delisting."""
    source, _ = _source(NO_SUBSCRIPTION)

    with pytest.raises(IbkrUnavailable, match="permissions"):
        source.fetch_daily_bars("AAPL", start=date(2024, 1, 1), end=date(2024, 1, 31))


def test_an_empty_result_is_an_empty_series_rather_than_an_error():
    source, _ = _source(EMPTY)

    fetched = source.fetch_daily_bars(
        "COH", start=date(2015, 1, 5), end=date(2015, 1, 16)
    )

    assert fetched.series.bars == ()


def test_the_request_depends_only_on_the_window_not_on_todays_date():
    """ADR-013 rule 3, and the defect an independent verification pass found.

    The first version computed `span_days = (date.today() - start).days + 1`, so
    the request was a function of the calendar day it ran on: re-fetching the
    identical `(symbol, start, end)` tomorrow sent a different `period`, returned
    different bytes, and produced a different `content_hash`. That silently
    breaks "re-fetch, hash, compare" — it would report a vendor restatement that
    never happened, which is exactly the failure `dolthub.py`'s calendar-month
    chunking reasons at length about avoiding.

    **Asserted on the span the request actually carries, not by comparing two
    calls.** The first version of this test compared two sources fetching the
    same window and passed against the defective code, because both ran on the
    same calendar day — a test that only fails if left overnight is not a test.
    A 31-day window must ask for 31 days whatever the date is; the old code sent
    `period=944d` here.
    """
    source, transport = _source()

    source.fetch_daily_bars("AAPL", start=date(2024, 1, 1), end=date(2024, 1, 31))

    assert "period=31d" in transport.urls[0], (
        "the requested span must come from (end - start), never from today"
    )


def test_the_requested_end_reaches_the_request():
    """The window's end was never sent to the API at all — only used to trim
    afterwards — which is why the request could depend on today's date instead."""
    source, transport = _source()

    source.fetch_daily_bars("AAPL", start=date(2024, 1, 1), end=date(2024, 1, 31))

    assert "20240131" in transport.urls[0]


def test_two_different_windows_send_two_different_requests():
    """The converse of determinism, and the check that the URL is not simply
    constant — which would satisfy the equality above while fetching the wrong
    thing."""
    source, transport = _source()

    source.fetch_daily_bars("AAPL", start=date(2024, 1, 1), end=date(2024, 1, 31))
    source.fetch_daily_bars("AAPL", start=date(2023, 1, 1), end=date(2023, 6, 30))

    assert transport.urls[0] != transport.urls[1]


def test_bars_outside_the_requested_window_are_discarded():
    """IBKR takes a duration and a bar size rather than two dates, so it returns
    whatever the duration covers — which routinely overshoots the window asked
    for. Keeping the extra bars would make the series claim coverage the caller
    did not request, and `Disclosure.sample_period` is derived from the series."""
    source, _ = _source()

    series = source.fetch_daily_bars(
        "AAPL", start=date(2024, 1, 3), end=date(2024, 1, 31)
    ).series

    assert [bar.date for bar in series.bars] == [date(2024, 1, 3)]
