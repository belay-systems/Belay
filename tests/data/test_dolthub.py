"""The one real implementation. ADR-013 rules 5, 6 and 9 applied to a vendor.

**Which vendor was deliberately left open by ADR-013** — "a licence and coverage
question to settle against a current price list at implementation time, not a
doctrine question." This is that settlement, and the properties below were
established by querying the source rather than read off its marketing.

**Licence: CC BY-SA 4.0**, from the repository's own `LICENSE.md`, retrieved
with `SELECT doc_name, doc_text FROM dolt_docs`. Section 4 grants the right to
"extract, reuse, reproduce, and Share all or a substantial portion of the
contents of the database", so rule 4's storage ruling rests on repository growth
alone rather than on a licence bar.

**Survivorship, established by query on 2026-08-01 and the finding of this
session.** Both halves were run against the live database:

- `SELECT act_symbol, security_name, last_seen FROM symbol ORDER BY last_seen
  ASC LIMIT 6` returns `COH  "Coach, Inc. Common Stock"  last_seen 2017-10-26`.
  Coach became Tapestry in October 2017 and the ticker died; the row survives,
  and the table holds 23,827 symbols against roughly 6,000 currently listed. The
  universe table therefore **accumulates** rather than snapshots.
- `SELECT date, act_symbol, close FROM ohlcv WHERE act_symbol='COH' AND date
  BETWEEN '2015-01-05' AND '2015-01-16'` returns **zero rows**, while the same
  query for `AAPL` over `2017-10-16` to `2017-10-26` returns three. COH has no
  price history at all, for any window, including years it actively traded.

So this source **fails the delisted-prices half and partially passes the
universe half** — the reverse of the usual expectation, and exactly the "a
source can pass one and fail the other" case ADR-013 rule 5 describes. Under
rule 9 that is a legitimate, *established* answer rather than an unknown one,
and rule 5 makes it a signed property of every artifact derived from it.

**No network here.** The transport is injected. A test suite that reaches the
internet fails for reasons that have nothing to do with the code, and
`AGENTS.md` ranks reproducibility fourth of eight engineering priorities.
"""

from __future__ import annotations

import json
from datetime import date
from decimal import Decimal

import pytest

from framework.data.contract import InstrumentClass, InstrumentNotSupported
from framework.data.dolthub import (
    DOLTHUB_STOCKS_SURVIVORSHIP,
    DoltHubStocksSource,
    DoltHubUnavailable,
)
from framework.data.survivorship import Retention

# Shaped exactly as the live API returns: every value a string, including the
# bigint volume, and the status carried in its own field rather than in the HTTP
# code.
SUCCESS = json.dumps(
    {
        "query_execution_status": "Success",
        "query_execution_message": "",
        "repository_owner": "post-no-preference",
        "repository_name": "stocks",
        "commit_ref": "master",
        "sql_query": "SELECT ...",
        "schema": [
            {"columnName": "date", "columnType": "date"},
            {"columnName": "open", "columnType": "decimal(14,4)"},
        ],
        "rows": [
            {
                "date": "2017-10-24",
                "open": "156.2900",
                "high": "157.4200",
                "low": "156.2000",
                "close": "157.1000",
                "volume": "17040200",
            },
            {
                "date": "2017-10-25",
                "open": "156.9100",
                "high": "157.5500",
                "low": "155.2700",
                "close": "156.4100",
                "volume": "21207300",
            },
            {
                "date": "2017-10-26",
                "open": "157.2300",
                "high": "157.8300",
                "low": "156.7800",
                "close": "157.4100",
                "volume": "17000500",
            },
        ],
    }
).encode("utf-8")

EMPTY = json.dumps(
    {
        "query_execution_status": "Success",
        "query_execution_message": "",
        "rows": [],
    }
).encode("utf-8")

ERROR = json.dumps(
    {
        "query_execution_status": "Error",
        "query_execution_message": "query error: branch not found",
        "rows": [],
    }
).encode("utf-8")

TIMEOUT = json.dumps(
    {
        "query_execution_status": "Error",
        "query_execution_message": "query error: context deadline exceeded",
        "rows": [],
    }
).encode("utf-8")


class Recorder:
    """A transport that returns a canned response and remembers the URL."""

    def __init__(self, response: bytes = SUCCESS) -> None:
        self.response = response
        self.urls: list[str] = []

    def __call__(self, url: str) -> bytes:
        self.urls.append(url)
        return self.response


def _source(response: bytes = SUCCESS) -> tuple[DoltHubStocksSource, Recorder]:
    transport = Recorder(response)
    return DoltHubStocksSource(transport=transport), transport


# ------------------------------------------------------------------ parsing


def test_a_successful_response_becomes_a_series():
    source, _ = _source()

    fetched = source.fetch_daily_bars(
        "AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26)
    )

    assert fetched.series.symbol == "AAPL"
    assert len(fetched.series.bars) == 3


def test_prices_arrive_as_decimal_not_float():
    """The source publishes `decimal(14,4)`. Widening that to a float on the way
    in would discard precision Belay was handed for free, and money in binary
    floating point accumulates error that stays invisible until it is material.
    """
    source, _ = _source()

    close = source.fetch_daily_bars(
        "AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26)
    ).series.bars[-1].close

    assert isinstance(close, Decimal)
    assert close == Decimal("157.4100")


def test_volume_arrives_as_an_integer():
    """The API returns bigint as a JSON string, so a naive parse leaves the
    volume as text and every liquidity filter silently compares strings."""
    source, _ = _source()

    volume = source.fetch_daily_bars(
        "AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26)
    ).series.bars[0].volume

    assert volume == 17_040_200
    assert isinstance(volume, int)


def test_the_payload_is_the_bytes_the_source_returned():
    """ADR-013 rule 3 hashes these, not the parse."""
    source, _ = _source()

    fetched = source.fetch_daily_bars(
        "AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26)
    )

    assert fetched.payload == SUCCESS


def test_bars_come_back_in_date_order():
    source, _ = _source()

    bars = source.fetch_daily_bars(
        "AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26)
    ).series.bars

    assert [bar.date for bar in bars] == sorted(bar.date for bar in bars)


# ------------------------------------------------------------ the query sent


def test_the_window_is_passed_to_the_source_rather_than_filtered_afterwards():
    """The `date` column leads the primary key. A query without a date range is
    a full table scan, which is what made the exploratory aggregates time out —
    so this is a correctness *and* a feasibility requirement."""
    source, transport = _source()

    source.fetch_daily_bars("AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26))

    sent = transport.urls[0]

    assert "2017-10-16" in sent
    assert "2017-10-26" in sent
    assert "AAPL" in sent


def test_the_query_targets_the_master_branch():
    """`main` does not exist on this repository and returns "branch not found".
    Pinned because the default branch name is a property of the source, not a
    convention Belay may assume."""
    source, transport = _source()

    source.fetch_daily_bars("AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26))

    assert "master" in transport.urls[0]


@pytest.mark.parametrize("hostile", ["AA'PL", "AAPL; DROP", "AAPL' OR '1'='1"])
def test_a_symbol_that_could_alter_the_query_is_refused(hostile):
    """The symbol is interpolated into SQL. A ticker carrying a quote would
    change the statement rather than the filter, and the DoltHub symbol table
    genuinely contains awkward characters — `DYN$A` is a real row."""
    source, _ = _source()

    with pytest.raises(ValueError, match="symbol"):
        source.fetch_daily_bars(
            hostile, start=date(2017, 10, 16), end=date(2017, 10, 26)
        )


# ------------------------------------------------------------------ failure


def test_a_query_error_is_raised_rather_than_read_as_no_data():
    """The API reports failure in a JSON field, not in the HTTP status, so a
    parser that only looks at `rows` reads every failure as an empty result —
    and an empty result for an equity is indistinguishable from a delisting.
    This is the survivorship failure mode arriving through the back door."""
    source, _ = _source(ERROR)

    with pytest.raises(DoltHubUnavailable, match="branch not found"):
        source.fetch_daily_bars(
            "AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26)
        )


def test_a_timeout_is_raised_and_says_so():
    """Observed repeatedly against the live database: full-table aggregates
    return `context deadline exceeded` with `Success`-shaped structure and no
    rows."""
    source, _ = _source(TIMEOUT)

    with pytest.raises(DoltHubUnavailable, match="deadline"):
        source.fetch_daily_bars(
            "AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26)
        )


def test_an_empty_result_is_an_empty_series_rather_than_an_error():
    """A genuine "this symbol has no bars in this window" is a real answer and
    the one COH returns. It is not an error — but it also cannot produce a
    sample period, so nothing downstream can quietly treat it as coverage."""
    source, _ = _source(EMPTY)

    fetched = source.fetch_daily_bars(
        "COH", start=date(2015, 1, 5), end=date(2015, 1, 16)
    )

    assert fetched.series.bars == ()

    with pytest.raises(ValueError, match="empty"):
        fetched.series.period()


# ------------------------------------------------------- rules 5, 6 and 9


def test_the_source_declares_equities_only():
    """Rule 6: implementation order is not preference. The *contract* expresses
    options; this adapter does not carry them and says so."""
    source, _ = _source()

    assert source.supported_instruments() == frozenset({InstrumentClass.EQUITY})


def test_asking_this_source_for_options_is_refused():
    source, _ = _source()

    with pytest.raises(InstrumentNotSupported):
        source.fetch_option_chain("AAPL", as_of=date(2024, 1, 2))


def test_the_survivorship_answers_are_the_ones_established_by_query():
    """Not hopeful defaults. Prices are survivor-only because COH returns
    nothing in any window while AAPL returns bars in the same window; universe
    membership is partial because the symbol table retains dead tickers with a
    `last_seen` date but records no first-seen and begins on 2017-10-26."""
    assert (
        DOLTHUB_STOCKS_SURVIVORSHIP.delisted_prices is Retention.SURVIVORS_ONLY
    )
    assert (
        DOLTHUB_STOCKS_SURVIVORSHIP.delisted_universe_membership
        is Retention.PARTIAL
    )


def test_the_constructor_takes_no_survivorship_argument():
    """Survivorship is a property of the *source*, established by query — not an
    opinion the caller holds.

    **This checks the constructor and nothing beyond it.** Under its previous
    name — "a caller cannot substitute a kinder survivorship disclosure" — it
    was the strongest statement of the guarantee in the suite and defended none
    of it: the assertion passes for any misspelled keyword. The substitution it
    named was genuinely possible one layer up, at `fetch_record()`, until an
    independent verification pass demonstrated it. See
    `tests/data/test_survivorship_cannot_be_softened.py`.
    """
    import inspect

    assert "survivorship" not in inspect.signature(DoltHubStocksSource).parameters
    assert _source()[0].survivorship is DOLTHUB_STOCKS_SURVIVORSHIP


def test_the_source_carries_the_direction_of_the_bias():
    """Rule 5. Every artifact derived from this source inherits it."""
    limitations = DOLTHUB_STOCKS_SURVIVORSHIP.known_limitations().lower()

    assert "inflates" in limitations
    assert "deflates" in limitations


def test_the_source_names_itself_and_its_licence():
    """`Disclosure.data_source` is enforced non-blank and sits inside the
    integrity hash. CC BY-SA 4.0 carries an attribution condition, so the
    attribution belongs in the signed record rather than in a comment."""
    source, _ = _source()

    assert "post-no-preference" in source.name
    assert "CC BY-SA" in source.name


def test_the_survivorship_basis_records_how_it_was_established():
    """`Retained` with no basis is an assertion.
    `constitution/Operational_Constraints.md:9-17` distinguishes Facts from
    Assumptions precisely so the two cannot be filed under one name."""
    basis = DOLTHUB_STOCKS_SURVIVORSHIP.basis

    assert "COH" in basis
    assert "AAPL" in basis


# ------------------------------------------------------------- no network


def test_nothing_here_reaches_the_network():
    """The transport is injected, and this asserts the seam exists rather than
    trusting that it was used. A suite that reaches the internet fails for
    reasons unrelated to the code."""
    source, transport = _source()

    source.fetch_daily_bars("AAPL", start=date(2017, 10, 16), end=date(2017, 10, 26))

    assert transport.urls, "the injected transport was bypassed"
