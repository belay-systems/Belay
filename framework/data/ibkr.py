"""Daily equity bars from Interactive Brokers. A second adapter. ADR-013.

**Why a second adapter exists at all.** Rule 2 rules the contract first
precisely so the vendor choice stays reversible. A contract with exactly one
implementation has not been shown to be a contract — it may just be that
implementation's shape wearing a general name. This is the check, and it is
deliberately a *structurally different* vendor: epoch-millisecond timestamps and
JSON floats against DoltHub's ISO dates and decimal strings, a duration-based
request against a date-range one, and a different failure mode.

**Using the broker as the data source does not violate rule 2.** Rule 2 forbids
a shared *abstraction* — one interface covering reads and writes, which must
pick one retry default and be wrong for the other, across a boundary Law VI
declares independent. It says nothing about which company is behind each
contract. `MarketDataSource` has no order vocabulary and never will.

**⚠ NEVER RUN AGAINST THE LIVE API.** This has been unit-tested against fixtures
shaped like IBKR's documented responses and nothing more. Verifying it needs a
funded account and a paid market data subscription, neither of which Belay has.
That limitation is recorded in `IBKR_SURVIVORSHIP.basis` so it travels onto
every artifact rather than living in a comment nobody reads at the point a
number is used. Asserting verified behaviour Belay has not observed is the exact
failure ADR-013's own Status block was written about.

**Cost and entitlement.** `interactivebrokers.github.io/tws-api/historical_data.html`
states "the API always requires Level 1 streaming real time data to return
historical data", so historical data is not included with an account. IBKR
waives the subscription fee above a monthly commission threshold — which a
paper-first system generating no commissions cannot reach, and which does not
change the survivorship position either way.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from collections.abc import Callable
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation

from framework.data.contract import (
    DailyBar,
    DailyBarSeries,
    FetchedSeries,
    InstrumentClass,
    MarketDataSource,
)
from framework.data.survivorship import Retention, SurvivorshipDisclosure

# The Client Portal API is served by a gateway the user runs locally and
# authenticates through a browser. Belay never handles the credentials, which is
# a property worth keeping: nothing here can be given a password.
_GATEWAY = "https://localhost:5000/v1/api"

_TIMEOUT_SECONDS = 30


class IbkrUnavailable(Exception):
    """IBKR could not or would not answer.

    Distinct from "answered, with no bars". The most likely real failure is a
    missing data entitlement, and an entitlement error read as an empty series
    would look exactly like a delisting — the survivorship failure mode arriving
    as an authentication bug.
    """


# ADR-013 rules 5 and 9, from IBKR's own documentation rather than from a vendor
# claim or from general knowledge.
IBKR_SURVIVORSHIP = SurvivorshipDisclosure(
    # `interactivebrokers.github.io/tws-api/historical_data.html`: "if data is
    # not available for a specific instrument, data type, or period within a TWS
    # chart it will also not be available from the API". A delisted instrument
    # has no TWS chart, so it has no API history. Paying for data does not
    # remove this limitation — which is the finding that settled the vendor
    # question, because it means IBKR buys the same bias the free source has.
    delisted_prices=Retention.SURVIVORS_ONLY,
    # Nothing located states whether IBKR can report index membership as at a
    # past date. Rule 9 makes "unknown" a legitimate answer that must be
    # *stated*; inferring a favourable answer from silence is the failure that
    # flatters, and it is the one this rule set exists to prevent.
    delisted_universe_membership=Retention.UNKNOWN,
    basis=(
        "Prices: IBKR's own TWS API documentation states that data unavailable "
        "in a TWS chart is unavailable from the API, and a delisted instrument "
        "has no chart. Universe: not established; no IBKR documentation "
        "locating historical index membership was found, so it is recorded as "
        "unknown rather than inferred. This adapter has NOT BEEN VERIFIED "
        "against the live IBKR API — it is unit-tested against fixtures only, "
        "because verification requires a funded account and a paid Level 1 "
        "market data subscription."
    ),
)


def _urlopen(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=_TIMEOUT_SECONDS) as response:
        return response.read()


class IbkrHistoricalSource(MarketDataSource):
    """Daily equity bars from IBKR's Client Portal history endpoint."""

    name = (
        "Interactive Brokers Client Portal history "
        "(requires a paid Level 1 market data subscription)"
    )
    key = "ibkr-cportal"

    def __init__(self, transport: Callable[[str], bytes] | None = None) -> None:
        # No `survivorship` parameter, for the reason ADR-012 rule 7 fixes its
        # own constants: survivorship is a property of the data, not an opinion
        # the caller holds.
        super().__init__(survivorship=IBKR_SURVIVORSHIP)
        self._transport = transport or _urlopen

    def supported_instruments(self) -> frozenset[InstrumentClass]:
        return frozenset({InstrumentClass.EQUITY})

    def _fetch_daily_bars(
        self, symbol: str, start: date, end: date
    ) -> FetchedSeries:
        # IBKR takes a *duration* ending at a point in time, not a date range,
        # so the window is expressed as a span plus the instant it ends at. That
        # structural difference from DoltHub is what makes this adapter worth
        # having as a check on the contract.
        #
        # **Both parts come from the arguments and neither from the clock.** An
        # earlier version computed the span as `(date.today() - start).days`,
        # which made the request a function of the day it ran on: re-fetching
        # the identical window tomorrow sent a different `period`, returned
        # different bytes, and produced a different `content_hash` — silently
        # breaking ADR-013 rule 3's "re-fetch, hash, compare" by reporting a
        # vendor restatement that never happened. `dolthub.py`'s
        # `_calendar_months` reasons at length about avoiding exactly this and
        # this module did the opposite. Found by an independent verification
        # pass; the test that should have caught it passed against the defect,
        # because both of its calls ran on the same calendar day.
        span_days = max((end - start).days + 1, 1)
        query = urllib.parse.urlencode(
            {
                "conid": symbol,
                "period": f"{span_days}d",
                "bar": "1d",
                # IBKR's documented format is YYYYMMDD-HH:mm:ss. UNVERIFIED
                # against the live API, like everything else here.
                "startTime": f"{end.strftime('%Y%m%d')}-23:59:59",
            }
        )
        payload = self._transport(f"{_GATEWAY}/iserver/marketdata/history?{query}")

        return FetchedSeries(
            series=DailyBarSeries(
                symbol=symbol, bars=self._parse(payload, symbol, start, end)
            ),
            payload=payload,
        )

    def _parse(
        self, payload: bytes, symbol: str, start: date, end: date
    ) -> tuple[DailyBar, ...]:
        try:
            body = json.loads(payload)
        except json.JSONDecodeError as error:
            raise IbkrUnavailable(
                f"the response for {symbol} was not JSON: {error}"
            ) from error

        if not isinstance(body, dict):
            raise IbkrUnavailable(f"unexpected response shape for {symbol}")

        # An entitlement failure arrives as a normal 200 with an `error` key,
        # so this must be checked before the absence of `data` is read as "no
        # bars".
        if "error" in body:
            raise IbkrUnavailable(
                f"IBKR refused the request for {symbol}: {body['error']}"
            )

        bars = [self._bar(point, symbol) for point in body.get("data", ())]

        # Trimmed, because a duration-based request routinely overshoots the
        # window asked for. Keeping the extra bars would make the series claim
        # coverage the caller never requested, and `Disclosure.sample_period` is
        # derived from the series — so the overshoot would land inside a signed
        # artifact as a false statement about what was examined.
        within = [bar for bar in bars if start <= bar.date <= end]

        return tuple(sorted(within, key=lambda bar: bar.date))

    def _bar(self, point: dict, symbol: str) -> DailyBar:
        """Return one IBKR data point as a `DailyBar`.

        Prices arrive as JSON numbers, which Python parses as `float`.
        Converting via `str` rather than `Decimal(value)` matters: `Decimal(185.64)`
        is 185.6400000000000005684341886080801486968994140625, because that is
        what the float actually holds. `Decimal(str(185.64))` is 185.64.
        """
        try:
            moment = datetime.fromtimestamp(point["t"] / 1000, tz=timezone.utc)
            return DailyBar(
                # Interpreted as UTC. IBKR timestamps a daily bar at the
                # exchange session, and for US equities that lands in the
                # morning UTC of the same calendar day. UNVERIFIED against the
                # live API, and the failure mode if it is wrong is a whole
                # series shifted by one day — which is why it is named here
                # rather than assumed correct.
                date=moment.date(),
                open=Decimal(str(point["o"])),
                high=Decimal(str(point["h"])),
                low=Decimal(str(point["l"])),
                close=Decimal(str(point["c"])),
                volume=int(point["v"]),
            )
        except (KeyError, ValueError, TypeError, InvalidOperation) as error:
            raise IbkrUnavailable(
                f"a data point for {symbol} could not be read as a daily bar: "
                f"{error} in {point!r}"
            ) from error
