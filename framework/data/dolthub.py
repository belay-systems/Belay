"""Daily equity bars from DoltHub `post-no-preference/stocks`. ADR-013.

**Which vendor was deliberately left open by ADR-013** — "a licence and coverage
question to settle against a current price list at implementation time, not a
doctrine question", made reversible by rule 2 ruling the contract first. This
module is that settlement. Every property recorded here was established by
querying the source on 2026-08-01, not read off its description.

**Licence: Creative Commons Attribution-ShareAlike 4.0 International.** From the
repository's own `LICENSE.md`, retrieved with `SELECT doc_name, doc_text FROM
dolt_docs`. Section 4 grants the right to "extract, reuse, reproduce, and Share
all or a substantial portion of the contents of the database", so rule 4's
storage ruling rests on unbounded repository growth alone rather than on a
licence bar. The attribution condition is why `name` carries the licence: it
lands in `Disclosure.data_source`, which is inside the integrity hash.
ShareAlike binds only on *sharing* adapted material, which a private research
repository does not do. **Belay is to be public — see ADR-013, OwnerDecisions 14h.**

**Survivorship: prices fail, universe partially passes.** This is the reverse of
the usual expectation and is the finding that settled the vendor question. See
`DOLTHUB_STOCKS_SURVIVORSHIP` below for the queries and their results.

**Coverage.** `ohlcv` begins 2011-01-03. The `symbol` table's `last_seen` column
begins 2017-10-26, which bounds how far back universe membership can be
reconstructed at all.

**The transport is injected** so the test suite never reaches the network. A
suite that does fails for reasons unrelated to the code, and `AGENTS.md` ranks
reproducibility fourth of eight engineering priorities.
"""

from __future__ import annotations

import calendar
import json
import re
import urllib.parse
import urllib.request
from collections.abc import Callable
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation

from framework.data.contract import (
    DailyBar,
    DailyBarSeries,
    FetchedSeries,
    InstrumentClass,
    MarketDataSource,
)
from framework.data.survivorship import Retention, SurvivorshipDisclosure

_API = "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks"

# `main` does not exist on this repository and returns "branch not found". The
# default branch name is a property of the source, not a convention Belay may
# assume.
_BRANCH = "master"

# Tickers are interpolated into SQL, so the accepted character set is stated
# rather than hoped for. The symbol table genuinely contains awkward entries —
# `DYN$A` is a real row for a preferred series — so the set cannot simply be
# letters, and a quote must never reach the statement.
#
# `\Z` rather than `$`: Python's `$` also matches immediately before a trailing
# newline, so `AAPL\n` satisfied the pattern. No injection was possible — a
# quote still could not pass — but the enforced set was not the stated set, and
# `AAPL\n` would also have forked the store into a second directory via `_slug`.
_SYMBOL = re.compile(r"\A[A-Za-z0-9.$^-]{1,32}\Z")

_TIMEOUT_SECONDS = 60

# Bounded. An unbounded retry against a genuinely dead source is a hang, which
# is worse than an error for something that runs unattended overnight. Three
# because the observed pattern is one failure followed by an immediate success,
# not a long degraded period.
_MAX_ATTEMPTS = 3


def _RETRYABLE(message: str) -> bool:
    """Whether a refusal is worth asking about again.

    Only the server-side deadline. A bad branch, a malformed query or an
    unreadable row will be refused identically however many times it is sent.
    """
    return "deadline exceeded" in message


class SourceUnavailable(Exception):
    """A transport could not answer. The base both transports' failures share.

    **Added for the chunk-naming wrapper below, and an independent verification
    pass is what showed it was needed.** `_fetch_daily_bars` wraps a failing
    chunk to say *which month* failed, because "a thirteen-year backfill is 156
    requests and a message that does not say which month failed turns a one-line
    fix into a search." That wrapper caught `DoltHubUnavailable` only, so
    `framework/data/dolt_clone.py`'s failures escaped it unnamed — and the clone
    is precisely what makes 156-chunk backfills routine rather than impossible.

    The two concrete types stay siblings rather than one inheriting the other:
    they fail for unrelated reasons — a server-side deadline against a missing
    binary or an absent clone — and `_RETRYABLE` must never treat the second as
    the first.
    """


class DoltHubUnavailable(SourceUnavailable):
    """The source could not answer.

    Distinct from "the source answered, and the answer was no rows". The API
    reports failure in a JSON field rather than in the HTTP status, so a parser
    that only reads `rows` treats every failure as an empty result — and an
    empty result for an equity is indistinguishable from a delisting. That is
    the survivorship failure mode arriving through the back door, which is why
    this exception exists rather than a returned empty series.
    """


# ADR-013 rules 5 and 9, established by query on 2026-08-01 rather than assumed.
#
# Fixed on the source rather than accepted from a caller, for the reason ADR-012
# rule 7 fixes its own constants: survivorship is a property of the data, not an
# opinion the caller holds, and a constructor argument would let the one thing
# that makes this free data honest be replaced with "clean" by whoever found it
# inconvenient.
DOLTHUB_STOCKS_SURVIVORSHIP = SurvivorshipDisclosure(
    # `SELECT date, act_symbol, close FROM ohlcv WHERE act_symbol='COH' AND date
    # BETWEEN '2015-01-05' AND '2015-01-16'` returns zero rows, as does the same
    # query over 2017-10-16..2017-10-26. The same query shape for AAPL over the
    # latter window returns three rows, so the empty result is a property of the
    # symbol rather than of the query. COH is Coach, Inc., which traded actively
    # until it became Tapestry in October 2017.
    #
    # **Two windows, not all windows.** An earlier version of this comment said
    # COH has no history "for any window", which is a universal drawn from two
    # samples — the `basis` string below said "in every window tried" and was
    # right where the comment was not. An ADR whose rules 5 and 9 forbid a vendor
    # from asserting coverage it has not established must not do it either.
    delisted_prices=Retention.SURVIVORS_ONLY,
    # `SELECT act_symbol, security_name, last_seen FROM symbol ORDER BY
    # last_seen ASC LIMIT 6` returns COH with last_seen 2017-10-26, and the
    # table holds 23,827 rows against roughly 6,000 currently-listed US stocks.
    # Dead tickers are retained, so "was this listed on date D?" is answerable
    # as `last_seen >= D`. Partial rather than retained because there is no
    # first-seen column — a symbol not yet listed on D cannot be excluded — and
    # because accumulation began on 2017-10-26, so anything that died before
    # that date is absent entirely.
    delisted_universe_membership=Retention.PARTIAL,
    # Facts and inferences are separated inside this string, because it is
    # signed into every artifact derived from the source and
    # `constitution/Operational_Constraints.md:9-17` — cited in
    # `survivorship.py` for exactly this — exists so the two cannot be filed
    # under one name. An earlier version opened "Established by query" and then
    # asserted a market-wide listing count and a start-of-accumulation date,
    # neither of which any query returned.
    basis=(
        "QUERIED 2026-08-01. Prices: ohlcv returned zero rows for COH (Coach, "
        "Inc., delisted October 2017) in both windows tried, 2015-01-05 to "
        "2015-01-16 and 2017-10-16 to 2017-10-26, while AAPL returned rows over "
        "the latter, so the empty result is a property of the symbol and not of "
        "the query. Universe: the symbol table returned COH with last_seen "
        "2017-10-26, and COUNT(*) returned 23,827 rows. INFERRED, not queried: "
        "that the price table therefore carries currently-listed symbols only "
        "(two delisted samples, not an exhaustive check); that 23,827 exceeds "
        "the number of currently-listed US stocks, which is external knowledge "
        "of roughly 6,000 rather than a query result; and that accumulation "
        "began on 2017-10-26, which the ORDER BY only shows to be the earliest "
        "last_seen retained. ESTABLISHED: membership is reconstructable as "
        "last_seen >= date, and there is no first-seen column, so a symbol not "
        "yet listed on a past date cannot be excluded."
    ),
)


def _calendar_months(start: date, end: date) -> list[tuple[date, date]]:
    """Split an inclusive window into per-calendar-month windows.

    **Calendar months rather than a configurable number of days, deliberately.**
    The boundaries must depend only on the requested window. If they could
    differ between two runs of the same fetch — because someone tuned a chunk
    size — the concatenated payload would differ and so would its content hash,
    and ADR-013 rule 3's "re-fetch, hash, compare" would report a vendor
    restatement that never happened.

    The first and last chunks keep the caller's own start and end rather than
    widening to whole months: a widened window would fetch data nobody asked for
    and report coverage the caller did not request.
    """
    windows: list[tuple[date, date]] = []
    cursor = start

    while cursor <= end:
        # `monthrange` returns the real length, so February 2024's 29th is not
        # dropped. A month end computed as "day 28" would skip a trading day
        # every four years, and a missing bar is a silent wrong answer.
        last_day = calendar.monthrange(cursor.year, cursor.month)[1]
        month_end = date(cursor.year, cursor.month, last_day)
        windows.append((cursor, min(month_end, end)))
        cursor = month_end + timedelta(days=1)

    return windows


def _urlopen(url: str) -> bytes:
    """Default transport. Separated so tests can replace it wholesale."""
    with urllib.request.urlopen(url, timeout=_TIMEOUT_SECONDS) as response:
        return response.read()


class DoltHubStocksSource(MarketDataSource):
    """Daily US equity bars, free, survivor-only in the prices.

    Rule 6: this adapter carries equities and says so. The *contract* expresses
    options — implementation order is not preference.
    """

    name = "DoltHub post-no-preference/stocks (CC BY-SA 4.0)"
    key = "dolthub-stocks"

    def __init__(self, transport: Callable[[str], bytes] | None = None) -> None:
        # No `survivorship` parameter, deliberately. See
        # `DOLTHUB_STOCKS_SURVIVORSHIP` above.
        super().__init__(survivorship=DOLTHUB_STOCKS_SURVIVORSHIP)
        self._transport = transport or _urlopen

    def supported_instruments(self) -> frozenset[InstrumentClass]:
        return frozenset({InstrumentClass.EQUITY})

    def _fetch_daily_bars(
        self, symbol: str, start: date, end: date
    ) -> FetchedSeries:
        if not _SYMBOL.match(symbol):
            raise ValueError(
                f"symbol {symbol!r} contains characters that are not accepted "
                "here. It is interpolated into a SQL statement, and a ticker "
                "carrying a quote would change the statement rather than the "
                "filter."
            )

        # Fetched a calendar month at a time, and **a month is not reliably
        # small enough**. Measured against the live database on 2026-08-01:
        # three months exceeded the server's ~54s deadline on 3/3 attempts, and
        # a *novel* month — April 2024, which the server had not served before —
        # failed 2/2 at 54.5s. The same month in weekly chunks succeeded at
        # 0.6s / 33.4s / 33.8s / 43.3s: 111 seconds for one month, so thirteen
        # years is roughly 6.6 hours per symbol.
        #
        # The tempting figure of ~0.5s per month is a *warm* reading and does
        # not hold for a window the server has not served before. It was taken
        # as representative once and the chunk size was chosen against it; that
        # error is recorded here rather than corrected away, because the
        # superseded reading is what makes the correct one legible.
        #
        # Chunking therefore reduces the failure rate without eliminating it,
        # and a failing chunk fails the whole fetch. The real fix is a
        # `dolt clone` transport behind the injected seam below —
        # `docs/HANDOFF.md` finding 14.
        payloads: list[bytes] = []
        bars: list[DailyBar] = []

        for chunk_start, chunk_end in _calendar_months(start, end):
            query = (
                "SELECT `date`, `open`, high, low, `close`, volume FROM ohlcv "
                f"WHERE act_symbol='{symbol}' "
                f"AND `date` BETWEEN '{chunk_start.isoformat()}' "
                f"AND '{chunk_end.isoformat()}' "
                "ORDER BY `date` ASC"
            )
            url = f"{_API}/{_BRANCH}?q={urllib.parse.quote(query)}"

            try:
                payload = self._attempt(url, symbol)
                bars.extend(self._parse(payload, symbol))
            # `SourceUnavailable`, not `DoltHubUnavailable`. The narrower catch
            # let every local-clone failure past this wrapper unnamed, which is
            # the one place a 156-chunk backfill says which chunk went wrong.
            except SourceUnavailable as error:
                # Named, because a thirteen-year backfill is 156 requests and a
                # message that does not say which month failed turns a one-line
                # fix into a search.
                #
                # Re-raised as the *original* type rather than as
                # `DoltHubUnavailable`. Adding the chunk's identity must not
                # relabel a missing local clone as a hosted-API failure — a
                # caller distinguishing the two would be reading a lie.
                raise type(error)(
                    f"{symbol}: the chunk covering {chunk_start.isoformat()} to "
                    f"{chunk_end.isoformat()} failed, so the whole fetch fails "
                    f"rather than returning a series with a hole in it. {error}"
                ) from error

            payloads.append(payload)

        return FetchedSeries(
            series=DailyBarSeries(
                symbol=symbol, bars=tuple(sorted(bars, key=lambda bar: bar.date))
            ),
            # Every chunk, because rule 3 hashes the bytes the source returned
            # and with more than one request that is all of them. Joined rather
            # than merged: re-parsing is not this hash's job, and a merge would
            # be a transformation the signature then covered instead of the
            # source's actual answer.
            payload=b"\n".join(payloads),
        )

    def _attempt(self, url: str, symbol: str) -> bytes:
        """Request `url`, retrying a deadline failure. ADR-013 rule 2.

        **Rule 2 blesses this explicitly**, and it is half of that rule's
        argument for two contracts: "Retrying is *how* a data fetch recovers
        from a dropped connection. A retried order submit doubles a position."
        Market data is the side where retrying is the correct default, and an
        adapter that gives up on the first timeout declines the recovery its own
        contract is shaped around.

        **Measured 2026-08-01, correcting an earlier note in this repository.**
        The same window failed at 54.6s and then succeeded in 1.0s on the next
        attempt. "Retrying does not help" was true of the three-month window
        (3/3 failures) and false in general — this source is *intermittent* as
        well as slow, and the two call for different responses.

        Only the deadline is retried. A bad branch does not become a good branch
        by asking again, and retrying it turns a fast clear error into a slow
        one.
        """
        last: DoltHubUnavailable | None = None

        for attempt in range(1, _MAX_ATTEMPTS + 1):
            payload = self._transport(url)
            try:
                self._check(payload, symbol)
                return payload
            except DoltHubUnavailable as error:
                if not _RETRYABLE(str(error)):
                    raise
                last = error

        raise DoltHubUnavailable(
            f"{symbol}: gave up after {_MAX_ATTEMPTS} attempts. {last}"
        )

    def _check(self, payload: bytes, symbol: str) -> None:
        """Raise if `payload` is a refusal rather than an answer."""
        self._parse(payload, symbol)

    def _parse(self, payload: bytes, symbol: str) -> tuple[DailyBar, ...]:
        try:
            body = json.loads(payload)
        except json.JSONDecodeError as error:
            raise DoltHubUnavailable(
                f"the response for {symbol} was not JSON: {error}"
            ) from error

        status = body.get("query_execution_status")
        if status != "Success":
            raise DoltHubUnavailable(
                f"the source refused the query for {symbol}: "
                f"{body.get('query_execution_message') or status!r}"
            )

        bars = [self._bar(row, symbol) for row in body.get("rows", ())]

        # Sorted here as well as in the query. `DailyBarSeries` refuses an
        # unordered series, and a source is not trusted to have honoured
        # ORDER BY — the invariant belongs to Belay, not to the vendor.
        return tuple(sorted(bars, key=lambda bar: bar.date))

    def _bar(self, row: dict, symbol: str) -> DailyBar:
        """Return one row as a `DailyBar`.

        Every value arrives as a JSON string, including the bigint volume — a
        naive parse leaves volume as text and every liquidity filter silently
        compares strings.
        """
        try:
            return DailyBar(
                date=date.fromisoformat(row["date"]),
                open=Decimal(row["open"]),
                high=Decimal(row["high"]),
                low=Decimal(row["low"]),
                close=Decimal(row["close"]),
                volume=int(row["volume"]),
            )
        except (KeyError, ValueError, TypeError, InvalidOperation) as error:
            raise DoltHubUnavailable(
                f"a row for {symbol} could not be read as a daily bar: "
                f"{error} in {row!r}"
            ) from error
