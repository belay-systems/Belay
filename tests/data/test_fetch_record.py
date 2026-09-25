"""What Belay keeps instead of the data. ADR-013 rules 1, 3, 8 and 10.

**The structural ruling, and it was forced rather than chosen.**
`Knowledge/Identifiers.md:27-57` defines eight prefixes — STRAT, EXP, RS, REV,
RPT, REGIME, WF, DOC — and none names market data. `ArtifactType` carries nine
members and none names it either. A price series has no honest identity under
the vocabulary Belay has, and manufacturing one means editing `Knowledge/`,
which widens the open finding that those two vocabularies already disagree.

The resolution is to notice that **the data is an input, not evidence.** What
Law VII requires Belay to retain is the knowledge of *what was obtained, from
where, when, covering what, and what it cannot be trusted to mean* — a record,
not a table of numbers.

**The hash is what makes the arrangement work.** Reproducibility becomes
checkable rather than asserted: re-fetch, hash, compare. And if the data store
is lost, the artifacts still record what was fetched and what it hashed to,
which is the institutional knowledge Law VII protects as distinct from the bytes.

**Rule 8: no evidence grade.** `constitution/Evidence_Standards.md` grades how
well a *strategy* has been tested — live, paper, simulation, hypothesis. A price
observation is on none of those axes, and grading it C would assert that
something was simulated when nothing was.

**Rule 10: not a `Market Snapshot`.** That `DeliverableType` exists and is
tempting. It is a daily *workflow* deliverable describing the state of the
market, and a ten-year historical backfill is not a snapshot of anything.
"""

from __future__ import annotations

import hashlib
import tempfile
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from framework.artifacts.enums import ArtifactType, DeliverableType, EvidenceLevel
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.validator import ArtifactValidator
from framework.data.contract import (
    DailyBar,
    DailyBarSeries,
    FetchedSeries,
    InstrumentClass,
    MarketDataSource,
)
from framework.data.fetch_record import disclosure_from, fetch_record
from framework.data.store import SeriesStore, StoredSeries
from framework.data.survivorship import Retention, SurvivorshipDisclosure
from framework.metrics.reporting import Disclosure, SamplePeriod

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

DISCLOSURE = SurvivorshipDisclosure(
    delisted_prices=Retention.SURVIVORS_ONLY,
    delisted_universe_membership=Retention.PARTIAL,
    basis="COH returns no bars; AAPL returns bars in the same window.",
)

PAYLOAD = b'[{"date":"2024-01-02","close":"10.75"}]'

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

SERIES = DailyBarSeries(symbol="AAPL", bars=BARS)


class Source(MarketDataSource):
    """A stand-in source. The provenance functions take the source rather than
    its name, so a fabricated disclosure cannot be paired with a real source's
    identity — see `test_survivorship_cannot_be_softened.py`."""

    name = "DoltHub post-no-preference/stocks"
    # Separate from the name, and both are recorded. ADR-014 rule 6.
    key = "test-source"

    def supported_instruments(self) -> frozenset[InstrumentClass]:
        return frozenset({InstrumentClass.EQUITY})

    def _fetch_daily_bars(self, symbol, start, end) -> FetchedSeries:
        return FetchedSeries(series=SERIES, payload=PAYLOAD)


SOURCE = Source(survivorship=DISCLOSURE)


# A real store, in a temporary directory. These tests are about what the record
# *says* rather than about where bytes land — `test_fetch_and_record.py` covers
# that — but `fetch_record` opens the file it is asked to name, so a fabricated
# path is no longer usable. It was until an independent pass signed a record
# naming a store path that held nothing.
_STORE = SeriesStore(root=Path(tempfile.mkdtemp(prefix="belay-fetch-record-tests-")))


def _stored(payload: bytes = PAYLOAD) -> StoredSeries:
    """Store `payload` for real and return the version it became."""
    return _STORE.store(source="test-source", symbol="AAPL", payload=payload)


def _record(**overrides):
    fields = {
        "identifier": "RPT-0100",
        "source": SOURCE,
        "symbol": "AAPL",
        "requested": SamplePeriod(start=date(2024, 1, 1), end=date(2024, 1, 31)),
        "series": SERIES,
        "payload": PAYLOAD,
        "stored": _stored(),
        "timestamp": FIXED_TIME,
    }
    if "payload" in overrides and "stored" not in overrides:
        overrides["stored"] = _stored(overrides["payload"])
    fields.update(overrides)
    return fetch_record(**fields)


# ------------------------------------------------- rule 6: naming its own bytes


def test_a_record_refuses_a_stored_version_that_is_not_its_payload():
    """The failure the new parameter makes possible, refused rather than trusted.

    A record signed over one fetch's bytes while naming another fetch's file
    verifies perfectly — both halves are individually sound — and its provenance
    is wrong. `framework/data/store.py:101-104` states that bytes are written
    exactly as returned; this is the check that statement never had.
    """
    with pytest.raises(ValueError, match="must not name another fetch's file"):
        _record(payload=b"one set of bytes", stored=_stored(b"a different set"))


def test_the_record_carries_the_store_key_the_version_and_the_path():
    """Compared against the `StoredSeries` the record was built from rather than
    against the literal 1: the store here is shared across this module, so a
    hardcoded version would pass or fail on test ordering."""
    stored = _stored()
    content = dict(_record(stored=stored).content)

    assert content["source_key"] == SOURCE.key
    assert content["store_version"] == stored.version
    assert content["store_path"] == stored.relative_path
    assert content["store_path"].startswith("test-source/AAPL/")


# ------------------------------------------------------------------ rule 3


def test_the_fetch_record_is_a_report():
    """ADR-010's principle applies unchanged: the type describes what the
    artifact **is**, and this one reports what was obtained."""
    assert _record().type is ArtifactType.REPORT


def test_the_fetch_record_carries_no_deliverable():
    """`framework/artifacts/artifact.py:29-36` already states the needed
    meaning — "None means 'not a documented deliverable' — a real state, not an
    unset field." No governance document declares a data fetch among any
    department's deliverables, and ADR-010 rule 4 scopes that vocabulary to what
    the documents declare."""
    assert _record().deliverable is None


def test_the_fetch_record_is_not_a_market_snapshot():
    """Rule 10, recorded because the wrong mapping is easy, cheap to make, and
    permanent once signed. A `Market Snapshot` is a daily workflow deliverable
    describing the state of the market; a historical backfill is not a snapshot
    of anything.

    **Asserted so it can fail for the reason the rule exists.** The first
    version of this test was `assert deliverable is not MARKET_SNAPSHOT`, which
    `None` satisfies trivially and which would pass for any of the other
    twenty-three deliverables too — it could not distinguish the ruling from an
    accident. `fetch_record` takes no `deliverable` parameter at all, so the
    mapping cannot be made by a caller; that is the property worth pinning.
    """
    import inspect

    assert "deliverable" not in inspect.signature(fetch_record).parameters, (
        "rule 10's trap is a caller passing MARKET_SNAPSHOT; the safest form of "
        "the rule is that there is nothing to pass"
    )
    assert _record().deliverable is None
    assert DeliverableType.MARKET_SNAPSHOT.value == "Market Snapshot", (
        "the tempting member still exists — if it were removed this test would "
        "stop meaning anything and should be re-read rather than deleted"
    )


def test_the_identifier_prefix_is_one_that_exists():
    """`REPORT` holds the `RPT` prefix, so no new prefix is minted and open
    finding 4 is not widened."""
    assert _record().id.startswith("RPT-")

    with pytest.raises(ValueError, match="Invalid artifact identifier"):
        _record(identifier="DATA-0001")


def test_the_record_carries_the_content_hash_of_the_bytes_returned():
    """The hash is over the *bytes the source returned*, not over the parsed
    series. A parser change would alter the parsed form while the source's
    answer was identical, and the point of the hash is to detect the reverse."""
    content = dict(_record().content)

    assert content["content_hash"] == hashlib.sha256(PAYLOAD).hexdigest()


def test_a_different_payload_produces_a_different_content_hash():
    """Reproducibility becomes checkable rather than asserted: re-fetch, hash,
    compare. A vendor restatement changes the bytes and therefore the hash."""
    restated = _record(payload=b'[{"date":"2024-01-02","close":"10.80"}]')

    assert dict(restated.content)["content_hash"] != dict(_record().content)[
        "content_hash"
    ]


def test_the_content_hash_is_inside_the_signature():
    """A hash the signature does not cover could be rewritten to match whatever
    was re-fetched later, which is the opposite of the guarantee."""
    record = _record()
    content = dict(record.content)
    content["content_hash"] = hashlib.sha256(b"something else").hexdigest()

    from dataclasses import replace

    forged = replace(record, content=tuple(content.items()))

    assert ArtifactIntegrity.verify_hash(forged) is False


def test_the_record_survives_the_validator():
    """The `(REPORT, None)` pair has to be storable, not merely declared.
    `ArtifactValidator._validate_deliverable` returns early on None, so this
    asserts the combination is legal rather than assuming it."""
    assert ArtifactValidator().validate(_record()) is True


def test_the_series_itself_is_not_in_the_artifact():
    """Rule 3's whole point: the record carries the series' fingerprint rather
    than its contents. Putting the numbers in would place a large,
    restatement-prone dataset inside a contract designed for immutable signed
    records."""
    content = dict(_record().content)
    rendered = str(content)

    assert "10.75" not in rendered.replace(str(content["observations"]), "")
    assert "bars" not in content


# ------------------------------------------------------------------ rule 8


def test_the_record_carries_no_evidence_and_therefore_no_grade():
    """`ArtifactFactory.create` derives `evidence_level` via
    `strongest_evidence_level`, which returns None for an artifact carrying no
    evidence records. `framework/artifacts/artifact.py:38-44` states the
    reasoning: "an unevidenced artifact has no grade, and inventing D for it
    would make 'unevidenced' read as 'hypothesis'."

    A fetch record is an observation, not a test of a strategy, so none of
    `Evidence_Standards.md`'s four classes applies to it.
    """
    record = _record()

    assert record.evidence == ()
    assert record.evidence_level is None


# ------------------------------------------------------- what was asked for


def test_the_record_distinguishes_what_was_asked_for_from_what_arrived():
    """These differ constantly and the difference is the finding. A request for
    January that returns two days means the source does not have January, and a
    record storing only one of the two windows cannot say so."""
    content = dict(_record().content)

    assert content["requested_start"] == "2024-01-01"
    assert content["requested_end"] == "2024-01-31"
    assert content["covered_start"] == "2024-01-02"
    assert content["covered_end"] == "2024-01-03"


def test_the_record_states_how_many_observations_arrived():
    assert dict(_record().content)["observations"] == 2


def test_the_record_names_its_source():
    """Rule 1: every fact Belay did not compute itself arrives with a recorded
    source, and that record sits inside the consuming artifact's signature."""
    assert dict(_record().content)["data_source"] == (
        "DoltHub post-no-preference/stocks"
    )


# ------------------------------------------------------ survivorship travels


def test_the_record_carries_the_survivorship_answers_and_the_direction():
    """Rule 5. The bias is a signed, undeletable property of the record, and it
    names the direction rather than merely flagging that a limitation exists."""
    limitations = dict(_record().content)["known_limitations"].lower()

    assert "inflates" in limitations
    assert "deflates" in limitations
    assert "delisted prices" in limitations


def test_a_fetch_record_cannot_be_built_from_a_source_with_no_answers():
    """Rule 9 again, at the record rather than at the source, because a record
    is what a later reader actually sees — and because a subclass that skips
    `super().__init__` bypasses the constructor guard entirely."""

    class Hollow(Source):
        def __init__(self):
            pass

    with pytest.raises((TypeError, AttributeError)):
        _record(source=Hollow())


# ------------------------------------------- the loop back into the metrics


def test_a_disclosure_can_be_built_from_the_fetch_without_hand_written_strings():
    """This is the point of Stage 2 stated as a test.

    Every metric artifact carries `data_source` and `sample_period`, and until
    now both were typed at the call site — which is why every number Belay has
    ever computed says the series was supplied by hand. A series that arrives
    knowing where it came from and what it covers makes those two fields say
    something else.
    """
    disclosure = disclosure_from(
        source=SOURCE,
        series=SERIES,
        assumptions="Daily closes, unadjusted for dividends.",
    )

    assert disclosure.data_source == "DoltHub post-no-preference/stocks"
    assert disclosure.sample_period == SamplePeriod(
        start=date(2024, 1, 2), end=date(2024, 1, 3)
    )
    assert "inflates" in disclosure.known_limitations.lower()


def test_a_derived_disclosure_grades_the_metric_historical_and_a_hand_built_one_does_not():
    """F-033, owner ruling Part 35 (ADR-017 draft): the grade comes from provenance.

    The pair is the point, and it is the whole of what makes the guard assertable.
    Before this, `metric_artifact` hardcoded `HISTORICAL` on every artifact it
    emitted, so eight numbers typed at a keyboard signed as historical simulation.

    Built so that only the return type of `disclosure_from` can satisfy it: if that
    function returns a plain `Disclosure`, the first assertion fails. That is the
    mutation the ADR says must turn the suite red, since a guard nothing asserts is
    F-019's and F-032's shape.
    """
    derived = disclosure_from(
        source=SOURCE,
        series=SERIES,
        assumptions="Daily closes, unadjusted for dividends.",
    )
    hand_built = Disclosure(
        assumptions="Daily closes, unadjusted for dividends.",
        data_source=SOURCE.name,
        sample_period=SamplePeriod(start=date(2024, 1, 2), end=date(2024, 1, 3)),
        known_limitations="Typed at the call site.",
    )

    assert derived.evidence_level is EvidenceLevel.HISTORICAL
    assert hand_built.evidence_level is EvidenceLevel.RESEARCH

    # Identical in every documented field, and graded differently. The four things
    # `Validation/Backtesting.md` requires cannot tell these apart, which is why
    # the provenance is carried by the type rather than by a fifth field.
    assert derived.data_source == hand_built.data_source
    assert derived.sample_period == hand_built.sample_period


def test_the_derived_disclosure_reports_the_covered_window_not_a_claimed_one():
    """The window comes from the bars that arrived. A disclosure stating the
    window that was *requested* would claim coverage the data does not have."""
    short = DailyBarSeries(symbol="AAPL", bars=BARS[:1])

    disclosure = disclosure_from(
        source=SOURCE,
        series=short,
        assumptions="Daily closes.",
    )

    assert disclosure.sample_period.end == date(2024, 1, 2)


# ------------------------------------------------------------ reproducibility


def test_identical_fetches_produce_identical_records():
    """With the timestamp pinned. `AGENTS.md` ranks reproducibility fourth of
    eight engineering priorities."""
    assert _record().integrity_hash == _record().integrity_hash


def test_the_record_is_signed():
    record = _record()

    assert record.integrity_hash is not None
    assert ArtifactIntegrity.verify_hash(record) is True


# ------------------------------- F-019: the file on disk, not only the hash it claims
#
# `reports/review/2026-09-04-review.md:89` (F-019). The check that the stored
# version's claimed hash matches the payload was tested; the check that the file
# on disk still holds those bytes was not, and disabling it left the suite green.
# Owner ruling: `docs/OwnerDecisions.md` Part 21.


def test_a_record_refuses_a_stored_file_whose_bytes_have_changed(tmp_path):
    """The stored version agrees with the payload on paper, and the file under it
    holds different data. Signed, that record would verify and be wrong."""
    store = SeriesStore(root=tmp_path / "market")
    stored = store.store(source="test-source", symbol="AAPL", payload=PAYLOAD)
    stored.path.write_bytes(b"not the bytes this record is signed over")

    with pytest.raises(ValueError, match="holding different data"):
        _record(stored=stored)
