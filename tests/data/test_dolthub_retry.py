"""A timed-out chunk is retried. ADR-013 rule 2, applied rather than quoted.

**Rule 2 blesses this explicitly and it is half of that rule's argument for two
contracts:** "Retrying is *how* a data fetch recovers from a dropped connection.
A retried order submit doubles a position. A shared base class must pick one
default and be wrong for the other." Market data is the side where retrying is
correct, so an adapter that gives up on the first timeout is not being careful —
it is declining the recovery its own contract is shaped around.

**Measured 2026-08-01, and it corrects an earlier claim in this repository.**
The same window — AAPL, 2024-01-02 to 2024-02-09 — failed at 54.6s and then
succeeded in **1.0s** on the immediately following attempt. An earlier note said
"retrying does not help", which was true of the three-month window (3/3 failures)
and false in general. The source is *intermittent*, not merely slow, and the two
call for different responses.

**Bounded, and it does not retry everything.** A refusal the source will repeat —
a bad branch, a malformed query — is not made true by asking again, so only the
deadline failure is retried. An unbounded retry against a genuinely dead source
is a hang, which is worse than an error for something that runs unattended.
"""

from __future__ import annotations

import json
from datetime import date

import pytest

from framework.data.dolthub import DoltHubStocksSource, DoltHubUnavailable

OK = json.dumps(
    {
        "query_execution_status": "Success",
        "rows": [
            {
                "date": "2024-01-03",
                "open": "1",
                "high": "1",
                "low": "1",
                "close": "1",
                "volume": "1",
            }
        ],
    }
).encode()

DEADLINE = json.dumps(
    {
        "query_execution_status": "Error",
        "query_execution_message": "query error: context deadline exceeded",
        "rows": [],
    }
).encode()

NOT_RETRYABLE = json.dumps(
    {
        "query_execution_status": "Error",
        "query_execution_message": "query error: branch not found",
        "rows": [],
    }
).encode()


class Sequence:
    def __init__(self, *responses: bytes) -> None:
        self.responses = list(responses)
        self.calls = 0

    def __call__(self, url: str) -> bytes:
        self.calls += 1
        return self.responses.pop(0) if self.responses else OK


def _fetch(transport):
    return DoltHubStocksSource(transport=transport).fetch_daily_bars(
        "AAPL", start=date(2024, 1, 2), end=date(2024, 1, 31)
    )


def test_a_deadline_failure_is_retried_and_succeeds():
    """The observed case: one timeout, then the identical query returns in a
    second."""
    transport = Sequence(DEADLINE, OK)

    fetched = _fetch(transport)

    assert transport.calls == 2
    assert len(fetched.series.bars) == 1


def test_the_payload_is_the_response_that_succeeded():
    """ADR-013 rule 3 hashes the bytes the source returned, and a failed attempt
    returned an error document rather than data. Including it would put a
    timeout message inside the content hash and make an identical successful
    re-fetch look like a vendor restatement."""
    fetched = _fetch(Sequence(DEADLINE, OK))

    assert fetched.payload == OK
    assert b"deadline" not in fetched.payload


def test_retries_are_bounded():
    """An unbounded retry against a genuinely dead source is a hang, which is
    worse than an error for something that runs unattended overnight."""
    transport = Sequence(*[DEADLINE] * 20)

    with pytest.raises(DoltHubUnavailable, match="deadline"):
        _fetch(transport)

    assert transport.calls < 20, "the retry did not stop"


def test_the_error_says_how_many_attempts_were_made():
    """"It timed out" and "it timed out four times" are different facts, and the
    second is what decides whether the source is slow or down."""
    with pytest.raises(DoltHubUnavailable, match="attempt"):
        _fetch(Sequence(*[DEADLINE] * 20))


def test_a_failure_the_source_will_repeat_is_not_retried():
    """A bad branch does not become a good branch by asking again. Retrying it
    turns a fast, clear error into a slow one."""
    transport = Sequence(NOT_RETRYABLE)

    with pytest.raises(DoltHubUnavailable, match="branch not found"):
        _fetch(transport)

    assert transport.calls == 1


def test_a_successful_first_attempt_is_not_retried():
    transport = Sequence(OK)

    _fetch(transport)

    assert transport.calls == 1
