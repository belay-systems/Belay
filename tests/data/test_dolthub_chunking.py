"""Long windows are fetched in chunks, because the source cannot serve them.

**Measured against the live database on 2026-08-01, warm:**

| window   | result                          |
|----------|---------------------------------|
| 8 days   | 7 bars, 0.4s                    |
| 1 month  | 22 bars, 0.5s                   |
| 6 weeks  | 31 bars, 0.6s                   |
| 2 months | 42 bars, 28.8s                  |
| 3 months | `context deadline exceeded`, 3/3 attempts, ~54.5s each |
| 1 year   | `context deadline exceeded`     |

A sharp cliff between six weeks and three months, and a hard server-side
deadline near 54 seconds. Retrying does not help: three consecutive attempts at
the three-month window failed identically.

**Chunked on calendar months, not on a tunable number of days.** The boundaries
must depend only on the requested window, or the same fetch run with a different
chunk size would produce different bytes and therefore a different content hash
— which would break exactly the comparison ADR-013 rule 3 exists to enable
("re-fetch, hash, compare"). Calendar months are a property of the window alone.

**A failed chunk fails the whole fetch.** Returning the chunks that succeeded
would hand back a series with silent holes in it, and a hole in an equity's
history is indistinguishable from the instrument not having traded. That is the
survivorship failure mode reappearing as a transport bug, which is precisely
what rule 5 is arranged against.
"""

from __future__ import annotations

import json
from datetime import date

import pytest

from framework.data.dolthub import DoltHubStocksSource, DoltHubUnavailable


def _response(*days: tuple[str, str]) -> bytes:
    return json.dumps(
        {
            "query_execution_status": "Success",
            "query_execution_message": "",
            "rows": [
                {
                    "date": day,
                    "open": close,
                    "high": close,
                    "low": close,
                    "close": close,
                    "volume": "1000",
                }
                for day, close in days
            ],
        }
    ).encode("utf-8")


FAILURE = json.dumps(
    {
        "query_execution_status": "Error",
        "query_execution_message": "query error: context deadline exceeded",
        "rows": [],
    }
).encode("utf-8")


class Queue:
    """A transport returning a prepared response per call, recording each URL."""

    def __init__(self, *responses: bytes) -> None:
        self.responses = list(responses)
        self.urls: list[str] = []

    def __call__(self, url: str) -> bytes:
        self.urls.append(url)
        if not self.responses:
            raise AssertionError(f"unexpected extra request: {url}")
        return self.responses.pop(0)


def _windows(urls: list[str]) -> list[tuple[str, str]]:
    """Return the (start, end) pair each request asked for."""
    import re
    import urllib.parse

    found = []
    for url in urls:
        query = urllib.parse.unquote(urllib.parse.urlparse(url).query)
        dates = re.findall(r"'(\d{4}-\d{2}-\d{2})'", query)
        found.append((dates[0], dates[1]))
    return found


# ------------------------------------------------------------- the splitting


def test_a_window_inside_one_calendar_month_is_a_single_request():
    """No chunking overhead where none is needed."""
    transport = Queue(_response(("2024-01-03", "10.00")))
    source = DoltHubStocksSource(transport=transport)

    source.fetch_daily_bars("AAPL", start=date(2024, 1, 2), end=date(2024, 1, 31))

    assert len(transport.urls) == 1
    assert _windows(transport.urls) == [("2024-01-02", "2024-01-31")]


def test_a_window_spanning_three_months_becomes_three_requests():
    """Boundaries are the calendar month ends, and the first and last chunks
    keep the caller's actual start and end rather than widening to whole
    months — a widened window would fetch data nobody asked for and report
    coverage the caller did not request."""
    transport = Queue(
        _response(("2024-01-31", "10.00")),
        _response(("2024-02-15", "11.00")),
        _response(("2024-03-05", "12.00")),
    )
    source = DoltHubStocksSource(transport=transport)

    source.fetch_daily_bars("AAPL", start=date(2024, 1, 30), end=date(2024, 3, 10))

    assert _windows(transport.urls) == [
        ("2024-01-30", "2024-01-31"),
        ("2024-02-01", "2024-02-29"),
        ("2024-03-01", "2024-03-10"),
    ]


def test_the_leap_day_is_not_dropped():
    """February 2024 has 29 days. A month-end computed as "day 28" would skip a
    trading day every four years, and a missing bar is a silent wrong answer."""
    transport = Queue(
        _response(("2024-02-29", "11.00")),
        _response(("2024-03-01", "12.00")),
    )
    source = DoltHubStocksSource(transport=transport)

    source.fetch_daily_bars("AAPL", start=date(2024, 2, 1), end=date(2024, 3, 1))

    assert _windows(transport.urls)[0] == ("2024-02-01", "2024-02-29")


def test_a_year_boundary_is_crossed_correctly():
    """December to January is where an off-by-one in the month arithmetic shows
    up as either a crash or a silently skipped month."""
    transport = Queue(
        _response(("2023-12-29", "10.00")),
        _response(("2024-01-02", "11.00")),
    )
    source = DoltHubStocksSource(transport=transport)

    source.fetch_daily_bars("AAPL", start=date(2023, 12, 28), end=date(2024, 1, 5))

    assert _windows(transport.urls) == [
        ("2023-12-28", "2023-12-31"),
        ("2024-01-01", "2024-01-05"),
    ]


def test_a_single_day_window_is_one_request():
    transport = Queue(_response(("2024-01-03", "10.00")))
    source = DoltHubStocksSource(transport=transport)

    source.fetch_daily_bars("AAPL", start=date(2024, 1, 3), end=date(2024, 1, 3))

    assert _windows(transport.urls) == [("2024-01-03", "2024-01-03")]


def test_the_chunking_depends_only_on_the_window():
    """Determinism, and the reason chunking is by calendar month rather than by
    a configurable number of days. If the boundaries could differ between two
    runs of the same fetch, the content hash would differ too, and "re-fetch,
    hash, compare" would report a vendor restatement that had not happened."""
    first = Queue(_response(("2024-01-31", "1")), _response(("2024-02-01", "2")))
    second = Queue(_response(("2024-01-31", "1")), _response(("2024-02-01", "2")))

    for transport in (first, second):
        DoltHubStocksSource(transport=transport).fetch_daily_bars(
            "AAPL", start=date(2024, 1, 15), end=date(2024, 2, 20)
        )

    assert _windows(first.urls) == _windows(second.urls)


# ------------------------------------------------------------- the stitching


def test_bars_from_every_chunk_are_present_and_ordered():
    transport = Queue(
        _response(("2024-01-31", "10.00")),
        _response(("2024-02-15", "11.00"), ("2024-02-16", "11.50")),
        _response(("2024-03-05", "12.00")),
    )
    source = DoltHubStocksSource(transport=transport)

    series = source.fetch_daily_bars(
        "AAPL", start=date(2024, 1, 30), end=date(2024, 3, 10)
    ).series

    assert [bar.date for bar in series.bars] == [
        date(2024, 1, 31),
        date(2024, 2, 15),
        date(2024, 2, 16),
        date(2024, 3, 5),
    ]


def test_the_covered_period_spans_the_whole_stitched_series():
    transport = Queue(
        _response(("2024-01-31", "10.00")),
        _response(("2024-02-15", "11.00")),
        _response(("2024-03-05", "12.00")),
    )
    source = DoltHubStocksSource(transport=transport)

    period = (
        source.fetch_daily_bars(
            "AAPL", start=date(2024, 1, 30), end=date(2024, 3, 10)
        )
        .series.period()
    )

    assert period.start == date(2024, 1, 31)
    assert period.end == date(2024, 3, 5)


def test_the_payload_carries_every_chunk_the_source_returned():
    """ADR-013 rule 3 hashes the bytes the source returned. With more than one
    request, that is all of them — a payload holding only the last chunk would
    sign a fraction of what was actually fetched."""
    chunks = (
        _response(("2024-01-31", "10.00")),
        _response(("2024-02-15", "11.00")),
    )
    transport = Queue(*chunks)
    source = DoltHubStocksSource(transport=transport)

    payload = source.fetch_daily_bars(
        "AAPL", start=date(2024, 1, 30), end=date(2024, 2, 20)
    ).payload

    for chunk in chunks:
        assert chunk in payload


def test_a_month_with_no_data_is_not_an_error():
    """A gap is a real answer — a suspended instrument, or a month before the
    series began. It is only a problem if it is confused with a failure."""
    transport = Queue(
        _response(("2024-01-31", "10.00")),
        _response(),
        _response(("2024-03-05", "12.00")),
    )
    source = DoltHubStocksSource(transport=transport)

    series = source.fetch_daily_bars(
        "AAPL", start=date(2024, 1, 30), end=date(2024, 3, 10)
    ).series

    assert len(series.bars) == 2


# --------------------------------------------------------------- failure


def test_a_failing_chunk_fails_the_whole_fetch():
    """Not a partial series. A hole in an equity's history is indistinguishable
    from the instrument not having traded, so returning the chunks that
    succeeded would reintroduce the survivorship failure as a transport bug."""
    transport = Queue(
        _response(("2024-01-31", "10.00")),
        # A deadline failure is retried up to `_MAX_ATTEMPTS` (ADR-013 rule 2 —
        # retrying is how a *read* recovers), so the February chunk must fail
        # every attempt before the fetch as a whole gives up.
        FAILURE,
        FAILURE,
        FAILURE,
        _response(("2024-03-05", "12.00")),
    )
    source = DoltHubStocksSource(transport=transport)

    with pytest.raises(DoltHubUnavailable, match="deadline"):
        source.fetch_daily_bars(
            "AAPL", start=date(2024, 1, 30), end=date(2024, 3, 10)
        )


def test_a_failing_chunk_names_the_window_that_failed():
    """A backfill spanning years fails on one month, and a message that does not
    say which one turns a one-line fix into a search."""
    transport = Queue(
        _response(("2024-01-31", "10.00")), FAILURE, FAILURE, FAILURE
    )
    source = DoltHubStocksSource(transport=transport)

    with pytest.raises(DoltHubUnavailable, match="2024-02"):
        source.fetch_daily_bars(
            "AAPL", start=date(2024, 1, 30), end=date(2024, 2, 20)
        )


def test_a_long_backfill_issues_one_request_per_calendar_month():
    """Thirteen years is 156 requests.

    **Not eighty seconds.** This docstring read "roughly half a second each —
    about eighty seconds per symbol" until an independent verification pass
    caught it: a backfill is composed entirely of *novel* queries, and the ~0.5s
    figure is a warm reading. The repository's own measurement for this workload
    is **roughly 6.6 hours per symbol**, so the claim was wrong by about 300×.

    It is the same shape as the `Knowledge/Schema.md` miscount ADR-013 cites as
    precedent — a corrected number left standing in a test docstring, where the
    correction had already reached `CHANGELOG.md`, `docs/ROADMAP.md` and
    `docs/HANDOFF.md`. Chunking is not what makes a backfill viable; it is what
    keeps small fetches working. Finding 14 is the viable path.
    """
    months = 156
    transport = Queue(*[_response() for _ in range(months)])
    source = DoltHubStocksSource(transport=transport)

    source.fetch_daily_bars("AAPL", start=date(2011, 1, 1), end=date(2023, 12, 31))

    assert len(transport.urls) == months
