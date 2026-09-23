"""Fetching, storing and recording are one act. ADR-013 rules 3 and 4 together.

**Written because a verification pass found rule 4 was not wired to anything.**
`SeriesStore` existed, was tested, and had no caller outside its own test file.
`fetch_record()` received the payload, hashed it, and discarded it. So every
signed record carried a `content_hash` pointing at bytes nobody kept.

That is not a cosmetic gap. Rule 4's own argument for storing at all is that
"a backtest run against a series nobody kept is not reproducible, and its
irreproducibility is *silent*" — which described the state of the code exactly.
And rule 3's guarantee, "re-fetch, hash, compare", needs an original to compare
against; with nothing stored there is only ever the new answer.

**The two must happen together or the failure is silent by construction.** A
record written without a store is a promise about bytes that do not exist, and a
store written without a record is bytes with no signed statement of where they
came from.
"""

from __future__ import annotations

import hashlib
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path

import pytest

from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.repository import ArtifactRepository
from framework.data.contract import (
    DailyBar,
    DailyBarSeries,
    FetchedSeries,
    InstrumentClass,
    MarketDataSource,
)
from framework.data.fetch_record import fetch_and_record, orphan_versions
from framework.data.store import SeriesStore
from framework.data.survivorship import Retention, SurvivorshipDisclosure
from framework.metrics.reporting import SamplePeriod

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

DISCLOSURE = SurvivorshipDisclosure(
    delisted_prices=Retention.SURVIVORS_ONLY,
    delisted_universe_membership=Retention.PARTIAL,
    basis="Established by query.",
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

REQUESTED = SamplePeriod(start=date(2024, 1, 1), end=date(2024, 1, 31))


class Source(MarketDataSource):
    name = "test source"
    key = "test-source"

    def __init__(self, payload: bytes = b'[{"close":"10.75"}]') -> None:
        super().__init__(survivorship=DISCLOSURE)
        self.payload = payload
        self.calls = 0

    def supported_instruments(self) -> frozenset[InstrumentClass]:
        return frozenset({InstrumentClass.EQUITY})

    def _fetch_daily_bars(self, symbol, start, end) -> FetchedSeries:
        self.calls += 1
        return FetchedSeries(
            series=DailyBarSeries(symbol=symbol, bars=BARS), payload=self.payload
        )


@pytest.fixture
def store(tmp_path: Path) -> SeriesStore:
    return SeriesStore(root=tmp_path / "market")


@pytest.fixture
def repository(tmp_path: Path) -> ArtifactRepository:
    """A repository per test, never the tracked default. ADR-014 rule 3: the
    root is the boundary between an experiment and a permanent record."""
    return ArtifactRepository(root=tmp_path / "artifacts")


def _fetch(store, source=None, repository=None, **overrides):
    fields = {
        "identifier": "RPT-0100",
        "source": source or Source(),
        "symbol": "AAPL",
        "requested": REQUESTED,
        "store": store,
        "repository": repository if repository is not None
        else ArtifactRepository(root=Path(store.root).parent / "artifacts"),
        "timestamp": FIXED_TIME,
    }
    fields.update(overrides)
    return fetch_and_record(**fields)


# ------------------------------------------------------- the bytes are kept


def test_the_fetched_bytes_reach_the_store(store):
    """Rule 4. The gap this test exists to close: nothing did this before."""
    result = _fetch(store)

    assert result.stored.path.read_bytes() == b'[{"close":"10.75"}]'


def test_the_record_and_the_store_agree_on_the_hash(store):
    """The whole arrangement rests on these being the same fingerprint. If the
    artifact's `content_hash` and the stored bytes could diverge, "re-fetch,
    hash, compare" would compare a record against bytes it does not describe."""
    result = _fetch(store)

    assert dict(result.record.content)["content_hash"] == result.stored.content_hash


def test_the_record_is_signed_and_validates(store):
    result = _fetch(store)

    assert ArtifactIntegrity.verify_hash(result.record) is True


def test_the_series_is_returned_for_use(store):
    """The caller wants the data as well as the record; making them fetch twice
    to get both would double the requests and could return two different
    answers."""
    result = _fetch(store)

    assert result.series.bars == BARS
    assert result.series.period().start == date(2024, 1, 2)


# ----------------------------------------------------------- rule 4 semantics


def test_an_identical_refetch_does_not_create_a_second_version(store):
    """Nothing was restated, so there is no new fact to record."""
    source = Source()
    first = _fetch(store, source=source)
    second = _fetch(store, source=source, identifier="RPT-0101")

    assert second.stored.version == first.stored.version == 1
    assert source.calls == 2, "the source was genuinely queried twice"


def test_a_restatement_becomes_a_new_version_and_both_survive(store):
    """Vendors restate history; which restatement a result was computed against
    is part of the result."""
    _fetch(store, source=Source(b'{"close":"10.75"}'))
    second = _fetch(
        store, source=Source(b'{"close":"10.80"}'), identifier="RPT-0101"
    )

    assert second.stored.version == 2
    assert len(store.versions(source="test-source", symbol="AAPL")) == 2


def test_two_records_of_a_restated_series_carry_different_hashes(store):
    """The point of keeping both: the artifacts are distinguishable, so a later
    reader can tell which bytes each number was computed from."""
    first = _fetch(store, source=Source(b'{"close":"10.75"}'))
    second = _fetch(
        store, source=Source(b'{"close":"10.80"}'), identifier="RPT-0101"
    )

    assert (
        dict(first.record.content)["content_hash"]
        != dict(second.record.content)["content_hash"]
    )


def test_the_store_is_keyed_by_source_so_two_vendors_do_not_collide(store):
    """Two vendors' answers for one ticker are different facts, and a shared
    version sequence would make one vendor's restatement look like the other's."""

    class Other(Source):
        name = "another source"
        key = "another-source"

    _fetch(store, source=Source())
    other = _fetch(store, source=Other(b"different"), identifier="RPT-0101")

    assert other.stored.version == 1


def test_renaming_a_source_does_not_orphan_its_stored_history():
    """The store is keyed on `key`, never on `name`. Keying on the display name
    meant that adding licence attribution to it silently started a fresh version
    chain and made the old history unreachable — a re-fetch would report version
    1 with nothing saying anything had been lost, which is exactly the silent
    irreproducibility rule 4 exists to prevent."""
    import tempfile

    with tempfile.TemporaryDirectory() as directory:
        shared = SeriesStore(root=Path(directory))
        first = _fetch(shared, source=Source())

        class Renamed(Source):
            name = "test source (now with a licence notice, CC BY-SA 4.0)"
            key = "test-source"

        second = _fetch(shared, source=Renamed(), identifier="RPT-0101")

        assert second.stored.path.parent == first.stored.path.parent
        assert second.stored.version == 1, "identical bytes, so still one version"


def test_a_source_declaring_no_key_is_refused():
    """A default derived from the class name would be silently unstable — a
    refactor renaming the class would move the store."""
    import tempfile

    class Keyless(Source):
        key = ""

    with tempfile.TemporaryDirectory() as directory:
        with pytest.raises(ValueError, match="key"):
            _fetch(SeriesStore(root=Path(directory)), source=Keyless())


# --------------------------------------------------------------- rule 9 holds


def test_a_source_with_no_survivorship_answer_is_refused_before_anything_is_stored(
    store,
):
    """Order matters. A source refused only after its bytes had landed would
    leave an unattributable file in an append-only store."""

    class Hollow(Source):
        def __init__(self):
            pass

    with pytest.raises((TypeError, AttributeError)):
        _fetch(store, source=Hollow())

    assert store.versions(source="test-source", symbol="AAPL") == ()


# ------------------------------------- rule 6: the record names its own bytes
#
# Opened as a finding while ADR-014 was drafted, and it is the reason rule 6
# had to land before rule 4 rather than after: the fields below are inside the
# integrity hash, and ADR-013 rule 7 established that changing signed content is
# free only while nothing is stored.


def test_the_record_names_the_store_key_and_not_only_the_display_name(store):
    """`framework/data/contract.py:195-196` says the display name "carries the
    licence attribution CC BY-SA requires" and is expected to be edited, while
    the key is "short, lowercase, and never changed once data exists".

    The record used to carry only the name — so the one source identifier it
    held was the one the store deliberately does not use, and an edit to the
    attribution text severed the record from its directory.
    """
    content = dict(_fetch(store).record.content)

    assert content["data_source"] == "test source"
    assert content["source_key"] == "test-source"


def test_the_record_names_the_store_version_and_relative_path(store):
    result = _fetch(store)
    content = dict(result.record.content)

    assert content["store_version"] == result.stored.version
    assert content["store_path"] == result.stored.relative_path


def test_the_recorded_path_is_relative_and_posix_on_every_platform(store):
    """The path is inside the integrity hash, so a backslash would make the same
    fetch sign differently on Windows and Linux — an artifact that fails to
    verify on the machine that did not create it.

    Relative to the store root for `framework/data/store.py:36-39`'s reason: an
    absolute path would carry this machine's home directory into a permanent
    signed record and mean nothing anywhere else.
    """
    content = dict(_fetch(store).record.content)

    assert "\\" not in content["store_path"]
    assert not Path(content["store_path"]).is_absolute()
    assert content["store_path"].startswith("test-source/AAPL/")


def test_the_record_resolves_to_its_bytes_without_searching_the_store(store):
    """The finding stated as a test. Before this, joining a record to its bytes
    meant hashing every file in the store until one matched."""
    content = dict(_fetch(store).record.content)

    landed = store.root / content["store_path"]

    assert landed.is_file()
    assert hashlib.sha256(landed.read_bytes()).hexdigest() == content["content_hash"]


# ----------------------------------- ADR-014 rules 4, 5 and 7: the record lands


def test_the_record_is_written_to_disk(store, repository):
    """F-002, stated as a test.

    `fetch_and_record` built this artifact and returned it, and nothing in Belay
    ever wrote one — so the claim `.gitignore` used to make, that "the record of
    what was obtained is signed and permanent whether or not the bytes are under
    version control", was false from the day it was written. That paragraph was
    replaced in the same commit that made this test pass; it is quoted here from
    the review rather than cited to a line that no longer holds it.
    """
    result = _fetch(store, repository=repository)

    assert result.record_path.is_file()
    assert result.record_is_new is True


def test_the_saved_record_reads_back_and_still_verifies(store, repository):
    """`ArtifactRepository.get()` vouches rather than parses — it refuses an
    artifact whose hash no longer matches — so a record that reads back at all
    is a record that survived the round trip intact."""
    result = _fetch(store, repository=repository)

    stored_record = repository.get("RPT-0100")

    assert stored_record.integrity_hash == result.record.integrity_hash
    assert dict(stored_record.content)["content_hash"] == result.stored.content_hash


def test_the_saved_record_resolves_to_its_own_bytes(store, repository):
    """The join rule 6 exists for, performed through the file rather than in
    memory: read the record back, follow its `store_path`, hash what is there."""
    _fetch(store, repository=repository)

    content = dict(repository.get("RPT-0100").content)
    landed = store.root / content["store_path"]

    assert hashlib.sha256(landed.read_bytes()).hexdigest() == content["content_hash"]


def test_a_fetch_that_stored_nothing_new_writes_no_second_record(store, repository):
    """ADR-014 rule 5. `SeriesStore.store` already declines to write a second
    copy of identical bytes because "nothing was restated, so there is no new
    fact to record"; before this the record half disagreed and minted one anyway.
    """
    source = Source()
    first = _fetch(store, source=source, repository=repository)
    second = _fetch(
        store, source=source, repository=repository, identifier="RPT-0101"
    )

    assert source.calls == 2, "the source was genuinely queried twice"
    assert second.record_is_new is False
    assert second.record.id == "RPT-0100", "the existing record, not a new one"
    assert repository.identifiers() == ["RPT-0100"]
    assert not (repository.root / "RPT-0101").exists()


def test_a_restatement_does_write_a_second_record(store, repository):
    """The other half of rule 5, so the rule cannot be satisfied by never
    recording anything. Different bytes are a new fact and get their own."""
    _fetch(store, source=Source(b'{"close":"10.75"}'), repository=repository)
    second = _fetch(
        store,
        source=Source(b'{"close":"10.80"}'),
        repository=repository,
        identifier="RPT-0101",
    )

    assert second.record_is_new is True
    assert repository.identifiers() == ["RPT-0100", "RPT-0101"]


def test_a_stored_version_with_no_record_is_reported_as_an_orphan(store, repository):
    """ADR-014 rule 7. This is the state F-002 left the whole store in, and it
    stays reachable: a fetch stores its bytes before discovering the series is
    empty, then raises.
    """
    store.store(source="test-source", symbol="MSFT", payload=b"unattributed")
    _fetch(store, repository=repository)

    orphans = orphan_versions(store, repository)

    assert [stored.relative_path for stored in orphans] == [
        stored.relative_path
        for stored in store.versions(source="test-source", symbol="MSFT")
    ]


def test_a_recorded_version_is_not_an_orphan(store, repository):
    """The converse, without which the check above would pass by reporting
    everything."""
    _fetch(store, repository=repository)

    assert orphan_versions(store, repository) == ()


# --------------------------- what an independent pass broke, one commit later


def test_two_symbols_with_identical_bytes_get_a_record_each(store, repository):
    """Dedup matched on the content hash alone, so two symbols whose payloads
    hashed identically collapsed into one record.

    The second fetch's bytes were written to disk, the record handed back named
    the *first* symbol and the first path, the caller's identifier was silently
    discarded, and `orphan_versions` then reported the store clean because it
    matched on the same hash. The pair (`store_path`, `content_hash`) is exact.
    """
    shared = b'{"close":"10.75"}'
    first = _fetch(store, source=Source(shared), repository=repository)
    second = _fetch(
        store,
        source=Source(shared),
        repository=repository,
        symbol="MSFT",
        identifier="RPT-0101",
    )

    assert first.stored.content_hash == second.stored.content_hash
    assert second.record_is_new is True
    assert second.record.id == "RPT-0101", "the caller's identifier, not the first's"
    assert dict(second.record.content)["symbol"] == "MSFT"
    assert orphan_versions(store, repository) == ()


def test_dedup_returns_the_version_that_describes_the_bytes(store, repository):
    """`get(identifier)` with no version returns `latest()`, so an identifier
    holding more than one handed back a record describing different bytes."""
    from dataclasses import replace

    from framework.artifacts.integrity import ArtifactIntegrity

    source = Source()
    first = _fetch(store, source=source, repository=repository)

    # A second version under the same identifier, describing something else.
    # `docs/HANDOFF.md`'s "An Identifier Reused At A New Version Is Silently
    # Mis-Filed" is what makes this reachable through sanctioned calls.
    other = _fetch(
        store,
        source=Source(b"unrelated bytes"),
        repository=repository,
        symbol="MSFT",
        identifier="RPT-0101",
    )
    repository.save(
        ArtifactIntegrity.sign(
            replace(other.record, id="RPT-0100", version="1.1.0", integrity_hash=None)
        )
    )

    again = _fetch(store, source=source, repository=repository, identifier="RPT-0102")

    assert again.record_is_new is False
    assert again.record.version == "1.0.0", "not latest()"
    assert dict(again.record.content)["content_hash"] == first.stored.content_hash


def test_an_unreadable_artifact_stops_the_walk_by_name(store, repository, tmp_path):
    """A silent skip would make a half-written record read as an absent one, and
    rule 5 treats an absent record as "these bytes are new" — so a corrupted
    artifact would mint a duplicate rather than raise an alarm."""
    _fetch(store, repository=repository)
    broken = repository.root / "RPT-0999"
    broken.mkdir(parents=True)
    (broken / "1.0.0.yaml").write_text("this: [is not: an artifact", encoding="utf8")

    with pytest.raises(ValueError, match="cannot read"):
        orphan_versions(store, repository)


def test_a_record_cannot_name_a_file_that_is_not_there(store, repository):
    """The hash guard compares two values the caller supplied and never opens the
    path, so it could not catch a record naming bytes that do not exist."""
    from dataclasses import replace

    from framework.data.fetch_record import fetch_record

    real = _fetch(store, repository=repository)
    missing = replace(
        real.stored, path=store.root / "nowhere" / "0007-deadbeefdeadbeef.bin"
    )

    with pytest.raises(ValueError, match="no file at"):
        fetch_record(
            identifier="RPT-0101",
            source=Source(),
            symbol="AAPL",
            requested=REQUESTED,
            series=real.series,
            payload=b'[{"close":"10.75"}]',
            stored=missing,
        )


# --------------------------------------------- F-019: two guards the suite never reached
#
# `reports/review/2026-09-04-review.md:89` (F-019). Disabling either guard below
# left the whole suite green. Owner ruling: `docs/OwnerDecisions.md` Part 21.


def test_an_unrecorded_version_is_an_orphan_even_when_its_bytes_match_a_recorded_one(
    store, repository
):
    """`orphan_versions` matches on the path *and* the hash. Matching on the hash
    alone is a regression `framework/data/fetch_record.py` records as having
    happened once already: a second symbol's identical bytes, stored with no
    record, look accounted for by the first symbol's record."""
    shared = b'{"close":"10.75"}'
    _fetch(store, source=Source(shared), repository=repository)
    unrecorded = store.store(source="test-source", symbol="MSFT", payload=shared)

    orphans = orphan_versions(store, repository)

    assert [stored.relative_path for stored in orphans] == [unrecorded.relative_path]


def test_a_source_with_no_survivorship_answer_is_refused_before_it_is_even_fetched(
    store,
):
    """ADR-013 rule 9 is checked **before** anything is written. The older test
    above passes without that check: its hollow source also lacks a payload, so
    the fetch itself fails first. This source fetches perfectly well. Only the
    pre-write check stops its bytes landing in an append-only store with no
    survivorship answer to attribute them to."""

    class Hollow(Source):
        def __init__(self):
            self.payload = b'[{"close":"10.75"}]'
            self.calls = 0

    source = Hollow()
    with pytest.raises(TypeError, match="SurvivorshipDisclosure"):
        _fetch(store, source=source)

    assert source.calls == 0, "the source was fetched before it was refused"
    assert store.versions(source="test-source", symbol="AAPL") == ()
