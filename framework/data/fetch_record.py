"""What Belay keeps instead of the data. ADR-013 rules 1, 3, 8 and 10.

**A fetched series is not an Artifact. The fetch record is, and it carries the
series' fingerprint rather than its contents.**

This is the structural ruling and it is forced by the existing vocabulary rather
than chosen. `Knowledge/Identifiers.md:27-57` defines eight prefixes — STRAT,
EXP, RS, REV, RPT, REGIME, WF, DOC — and none names market data. `ArtifactType`
carries nine members and none names it either. A price series has no honest
identity under the vocabulary Belay has, and manufacturing one means editing
`Knowledge/`, which widens the open finding that those two vocabularies already
disagree (`docs/HANDOFF.md` finding 4).

The resolution is to notice that **the data is an input, not evidence.** What
Law VII requires Belay to retain is the knowledge of *what was obtained, from
where, when, covering what, and what it cannot be trusted to mean*.

**The hash is what makes the arrangement work.** Reproducibility becomes
checkable rather than asserted — re-fetch, hash, compare. And if the data store
is lost, the artifacts still record what was fetched and what it hashed to,
which is the institutional knowledge Law VII protects as distinct from the bytes.

**Not built through `metric_artifact`.** That helper derives the artifact type
from a `DeliverableType`, and rule 3 requires `deliverable=None` — which would
be a `KeyError` against `DELIVERABLE_ARTIFACT_TYPE` rather than a ruling. A
fetch record is not a metric; it reports an observation, and it goes through
`ArtifactFactory` directly.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import ArtifactType
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.primitives import utc_now
from framework.artifacts.repository import ArtifactRepository
from framework.artifacts.validator import ArtifactValidator
from framework.data.contract import DailyBarSeries, MarketDataSource
from framework.data.store import SeriesStore, StoredSeries
from framework.data.survivorship import SurvivorshipDisclosure
from framework.metrics.reporting import Disclosure, FetchedDisclosure, SamplePeriod


def fetch_record(
    identifier: str,
    source: MarketDataSource,
    symbol: str,
    requested: SamplePeriod,
    series: DailyBarSeries,
    payload: bytes,
    stored: StoredSeries,
    timestamp: datetime | None = None,
) -> Artifact:
    """Return the signed record of one fetch.

    **Takes the source, not its name, and there is no `survivorship`
    parameter.** ADR-013 rule 5 requires the survivorship answer to be "a fixed
    constant on every artifact **derived from the source**", and an earlier
    version of this function satisfied only half of that: the constant inside
    `SurvivorshipDisclosure` could not be overridden, but the *disclosure object
    itself* was a caller-supplied argument sitting beside a caller-supplied
    `source_name` string. An independent verification pass showed the
    consequence — a fabricated `RETAINED / RETAINED` disclosure paired with the
    real source's name produced a signed artifact whose `known_limitations`
    mentioned no survivorship bias at all. Reading it off the source removes the
    parameter rather than validating it.

    `payload` is the **bytes the source returned**, and the hash is taken over
    those rather than over the parsed series. A parser change would alter the
    parsed form while the source's answer was byte-identical, and the point of
    the hash is to detect the reverse — the source's answer changing underneath
    an unchanged parser, which is what a vendor restatement is.

    `requested` and the series' own coverage are both recorded because they
    differ constantly and the difference is the finding: a request for January
    that returns two days means the source does not have January, and a record
    storing only one of the two windows cannot say so.

    **`stored` is required, and it is what makes the record able to name its own
    bytes.** ADR-014 rule 6. Until 2026-08-02 the only source identifier in the
    signed content was `source.name` — the display name, which
    `framework/data/contract.py:195-196` says carries the licence attribution and
    is *expected* to be edited, while the store is keyed on `source.key`, which
    never changes. So the record held the one identifier the store does not use,
    and joining a record to its bytes meant hashing every file in the store until
    one matched. The version and the store-relative path go in for the same
    reason: they are what the store can be asked with.

    Pass `timestamp` to make the result byte-for-byte reproducible; it defaults
    to now, which makes each call unique.
    """
    survivorship = _survivorship_of(source)

    # Re-checked here rather than only in `fetch_and_record`, for the reason
    # `_survivorship_of` is: this is the point at which the answer enters a
    # signed artifact, and a permanent record whose stable source identifier is
    # the empty string cannot name its own bytes — which is the whole of rule 6.
    if not source.key:
        raise ValueError(
            f"{type(source).__name__} declares no `key`. ADR-014 rule 6 puts it "
            "inside the record's signature, because the display name carries the "
            "licence attribution and is expected to be edited while the store is "
            "keyed on something that never changes."
        )

    # `store.py:101-104` states that bytes are written exactly as returned, "so
    # anything done to the bytes on the way in would make the artifact and the
    # disk disagree about what was fetched". That was a docstring; this is the
    # check. It also catches the caller error the new parameter makes possible —
    # a record signed over one fetch's payload while pointing at another fetch's
    # file, which would verify perfectly and be wrong.
    digest = hashlib.sha256(payload).hexdigest()
    if stored.content_hash != digest:
        raise ValueError(
            f"the stored version at {stored.relative_path} hashes to "
            f"{stored.content_hash} and the payload hashes to {digest}. A record "
            "signed over one fetch's bytes must not name another fetch's file: "
            "both halves would verify and the provenance would be wrong."
        )

    # **And the file itself, which the hash check alone does not reach.** An
    # independent pass signed a record naming a store path that held nothing:
    # `stored.content_hash` agreed with the payload because both were supplied by
    # the caller, and rule 6's headline — the record must be able to name the
    # bytes it is a record of — was enforced for the hash and unenforced for the
    # three fields the rule actually added.
    if not stored.path.is_file():
        raise ValueError(
            f"no file at {stored.path}. ADR-014 rule 6 signs the store path into "
            "the record, so a record naming bytes that are not there would be a "
            "permanent, verifiable statement about a file that does not exist."
        )
    on_disk = hashlib.sha256(stored.path.read_bytes()).hexdigest()
    if on_disk != digest:
        raise ValueError(
            f"the file at {stored.path} hashes to {on_disk}, and this record is "
            f"signed over bytes hashing to {digest}. The record would name a real "
            "file holding different data, which verifies and is wrong."
        )

    timestamp = timestamp or utc_now()
    covered = series.period()

    content = (
        ("data_source", source.name),
        # The stable key, beside the editable display name rather than instead
        # of it — the name carries the attribution CC BY-SA requires.
        ("source_key", source.key),
        ("symbol", symbol),
        # What was asked for, and what actually arrived. Both, for the reason
        # above.
        ("requested_start", requested.start.isoformat()),
        ("requested_end", requested.end.isoformat()),
        ("covered_start", covered.start.isoformat()),
        ("covered_end", covered.end.isoformat()),
        ("observations", len(series.bars)),
        # The fingerprint, not the contents. Inside the integrity hash, so it
        # cannot be repointed at whatever was re-fetched later.
        ("content_hash", digest),
        ("content_bytes", len(payload)),
        # Where the bytes landed. ADR-014 rule 6, and the pair a later reader
        # actually asks the store with: `store.root / store_path` resolves, and
        # `store_version` says which restatement this record describes.
        ("store_version", stored.version),
        ("store_path", stored.relative_path),
        ("survivorship_delisted_prices", survivorship.delisted_prices.value),
        (
            "survivorship_delisted_universe_membership",
            survivorship.delisted_universe_membership.value,
        ),
        ("known_limitations", survivorship.known_limitations()),
    )

    return ArtifactFactory().create(
        identifier=identifier,
        title=f"Fetch record: {symbol} from {source.name}",
        # ADR-010's principle unchanged: the type describes what the artifact
        # **is**, and this one reports what was obtained. `REPORT` holds the
        # `RPT` prefix, so no new identifier prefix is minted.
        artifact_type=ArtifactType.REPORT,
        # Rule 3, and rule 10's refusal of `MARKET_SNAPSHOT`. None is a real
        # state here rather than an unset field: no governance document declares
        # a data fetch among any department's deliverables, and ADR-010 rule 4
        # scopes that vocabulary to what the documents declare.
        deliverable=None,
        # Rule 8: no evidence records, therefore no grade.
        # `constitution/Evidence_Standards.md` grades how well a *strategy* has
        # been tested; a price observation is on none of those axes, and grading
        # it C would assert that something was simulated when nothing was.
        evidence=(),
        content=content,
        summary=(
            f"{len(series.bars)} daily bars for {symbol} covering "
            f"{covered.start.isoformat()} to {covered.end.isoformat()}"
        ),
        created=timestamp,
        updated=timestamp,
    )


@dataclass(frozen=True, slots=True)
class Fetch:
    """One completed fetch: the data, the bytes on disk, and the signed record.

    All three, because they are only useful together. The series is what a
    backtest consumes, the stored version is what makes a later re-fetch
    comparable, and the record is what Law VII requires Belay to keep.

    `record_path` is where the record landed. `record_is_new` is false when this
    fetch changed nothing and an existing record already covered these bytes —
    ADR-014 rule 5, and the only way a caller can tell the difference, since the
    record it gets back is the same either way.
    """

    series: DailyBarSeries
    stored: StoredSeries
    record: Artifact
    record_path: Path
    record_is_new: bool


def records_by_stored_version(
    repository: ArtifactRepository,
) -> dict[tuple[str, str], tuple[str, str]]:
    """Return `{(store_path, content_hash): (identifier, version)}` for every
    stored fetch record.

    **Keyed on the path as well as the hash, and it returns the version, because
    an earlier form of this function did neither and an independent pass broke it
    twice.** Keyed on the hash alone, two symbols whose payloads happened to hash
    identically collapsed into one record: the second fetch's bytes were written
    to disk, the record handed back named the *first* symbol and the first path,
    the caller's identifier was silently discarded, and `orphan_versions` then
    reported the store clean because it matched on the same hash. Returning the
    identifier alone was the second: `get(identifier)` with no version returns
    `latest()`, so an identifier holding more than one version — which
    `docs/HANDOFF.md`'s "An Identifier Reused At A New Version Is Silently
    Mis-Filed" makes reachable — handed back a record describing different bytes
    entirely.

    The pair is exact. The same bytes at the same path are the same stored
    version; anything else is a different one.

    **The lookup ADR-014 assumes and does not name**, which is a finding against
    that ADR rather than a design choice here — see `docs/HANDOFF.md`, "ADR-014
    Rules 5 And 8 Cannot Both Be Executed As Written". Rule 5 says a fetch that
    stored nothing new writes no record, and rule 8 says re-fetching the
    unprovenanced AAPL bytes *adopts* them by writing one; both describe the same
    dedup path and only a record-exists check tells them apart.

    Built by reading every record, with no index kept on disk. That is O(stored
    records) per call and it is a stated cost rather than a hidden one: an index
    is a second copy of the truth, and this repository has been bitten three
    times by a derived thing disagreeing with the thing it derived from. The
    trigger to revisit is the same one ADR-014 names for its growth — the first
    time Belay selects instruments rather than being handed them.

    Records that are not fetch records carry no `store_path` and are skipped
    rather than refused; ADR-014 rule 1 makes this the root for *every* artifact
    type, so most of what is here will eventually not be a fetch record.

    **An artifact that cannot be read stops the walk, loudly and by name.** It is
    tempting to skip it — this function runs inside every fetch — but a silent
    skip would make a hand-edited or half-written record read as an absent one,
    and an absent record is exactly what rule 5 treats as "these bytes are new".
    A corrupted record would therefore cause a duplicate to be minted rather than
    an alarm to be raised.
    """
    index: dict[tuple[str, str], tuple[str, str]] = {}
    for identifier in repository.identifiers():
        for version in repository.versions(identifier):
            try:
                artifact = repository.get(identifier, version)
            except Exception as error:
                raise ValueError(
                    f"cannot read {repository.path_for(identifier, version)} while "
                    "indexing the artifact root. Every fetch consults this index, "
                    "so an unreadable artifact is a stop rather than a skip: "
                    "treating it as absent would let rule 5 mint a duplicate "
                    f"record for bytes that already have one. {error}"
                ) from error
            if artifact is None:
                continue
            content = dict(artifact.content)
            path, digest = content.get("store_path"), content.get("content_hash")
            if path and digest:
                index.setdefault((path, digest), (identifier, version))
    return index


def orphan_versions(
    store: SeriesStore, repository: ArtifactRepository
) -> tuple[StoredSeries, ...]:
    """Return every stored version that no record accounts for. ADR-014 rule 7.

    A stored version with no record is the state F-002 left the repository in,
    and rule 4 makes it the abnormal case rather than the only case. It stays
    reachable — `docs/HANDOFF.md`'s "A Fetch Stores Its Bytes Before Discovering
    The Series Is Empty" writes bytes and then raises — so it is detected rather
    than assumed away.

    **Matched on the path *and* the hash computed from the file.** Matching on
    the hash alone reported a store clean while one of its two versions had no
    record naming it: two symbols with identical payload bytes shared a single
    record, and the one that was not named looked accounted for. Both halves have
    to agree — the path says which stored version this is, the hash says the
    bytes have not changed under it.
    """
    known = set(records_by_stored_version(repository))
    return tuple(
        stored
        for stored in store.all_versions()
        if (stored.relative_path, stored.content_hash) not in known
    )


def fetch_and_record(
    identifier: str,
    source: MarketDataSource,
    symbol: str,
    requested: SamplePeriod,
    store: SeriesStore,
    repository: ArtifactRepository,
    timestamp: datetime | None = None,
) -> Fetch:
    """Fetch, store the bytes, and save the signed record. ADR-013 rules 3 and 4,
    ADR-014 rules 4 and 5.

    **These are one act, and separating them is how the failure goes silent.**
    Until 2026-08-01 `SeriesStore` had no caller outside its own tests:
    `fetch_record()` received the payload, hashed it, and discarded it, so every
    signed record carried a `content_hash` pointing at bytes nobody kept. Rule
    4's own argument for storing is that "a backtest run against a series nobody
    kept is not reproducible, and its irreproducibility is silent" — which
    described the code exactly. Found by an independent verification pass, not
    by the suite, because each half was tested and the join was not.

    **`repository` is required for the same reason `store` is, and F-002 is the
    proof.** The paragraph above was written about the bytes and was true of the
    record all along: `fetch_and_record` built a signed record, returned it, and
    nothing in Belay ever wrote one to disk — so `.gitignore:46-49`'s claim that
    "the record of what was obtained is signed and permanent" was false from the
    day it was written. ADR-014 rule 4 puts the save here rather than in a script
    somebody has to remember to call, because remembering is what failed.

    **A fetch that stored nothing new saves nothing new.** ADR-014 rule 5.
    `SeriesStore.store` returns the existing version when the bytes are identical
    because "nothing was restated, so there is no new fact to record"; this
    function used to build a record regardless, so the two halves disagreed about
    what a new fact is. The test is whether a record already covers *these
    bytes*, not whether the store wrote a file — which is what lets rule 8's
    re-fetch adopt bytes that were stored before any record existed.

    Order is forced and is not a preference: the record hashes the payload, so it
    cannot precede it, and the bytes must be on disk before a record can name
    where they are. Rule 9 is checked **before** anything is written. A source
    refused after its bytes had landed would leave an unattributable file in an
    append-only store.
    """
    # Called for its refusal, before anything is fetched or written. Not an
    # `assert`, which `python -O` strips — and a guard that disappears under an
    # optimisation flag is not a guard.
    _survivorship_of(source)

    fetched = source.fetch_daily_bars(symbol, start=requested.start, end=requested.end)

    # Keyed on `source.key`, never on `source.name`. The display name carries
    # licence attribution and is expected to be edited; the store path must not
    # move when it is, or a re-fetch silently starts a new version chain and the
    # old history becomes unreachable without anything reporting it.
    if not source.key:
        raise ValueError(
            f"{type(source).__name__} declares no `key`. The data store is "
            "keyed on it rather than on the display name, so that renaming a "
            "source cannot orphan the versions already stored under it."
        )

    stored = store.store(source=source.key, symbol=symbol, payload=fetched.payload)

    existing = records_by_stored_version(repository).get(
        (stored.relative_path, stored.content_hash)
    )
    if existing is not None:
        known_identifier, known_version = existing
        # Rule 5. The bytes already have a record, so this fetch established
        # nothing that is not already written down. The existing record is
        # returned rather than a freshly built one: they would differ in their
        # timestamp and therefore in their signature, and handing back an
        # unsaved artifact that looks saved is the silent wrong answer this
        # repository keeps meeting.
        # The exact version, never `latest()`. An identifier can hold more than
        # one, and the newest is not necessarily the one describing these bytes.
        return Fetch(
            series=fetched.series,
            stored=stored,
            record=repository.get(known_identifier, known_version),
            record_path=repository.path_for(known_identifier, known_version),
            record_is_new=False,
        )

    record = fetch_record(
        identifier=identifier,
        source=source,
        symbol=symbol,
        requested=requested,
        series=fetched.series,
        payload=fetched.payload,
        stored=stored,
        timestamp=timestamp,
    )

    return Fetch(
        series=fetched.series,
        stored=stored,
        record=record,
        record_path=repository.save(record),
        record_is_new=True,
    )


def _survivorship_of(source: MarketDataSource) -> SurvivorshipDisclosure:
    """Return `source`'s survivorship answer, refusing a source that has none.

    A subclass that overrides `__init__` without calling `super().__init__` has
    no `survivorship` attribute and previously fetched bars perfectly happily —
    so the constructor guard was real for the ordinary path and the claim that
    "there is no path by which an unanswered source reaches a backtest" was not
    true. This is the second link in that chain, at the point the answer is
    actually written into a signed artifact.
    """
    survivorship = getattr(source, "survivorship", None)
    if not isinstance(survivorship, SurvivorshipDisclosure):
        raise TypeError(
            f"{type(source).__name__} carries no SurvivorshipDisclosure. "
            "ADR-013 rule 9: a source that cannot state its survivorship "
            "properties is refused, not assumed clean, and it fails in the "
            "direction that flatters."
        )
    return survivorship


#: The signed-content keys only `fetch_record` writes. `disclosure_from` refuses a
#: record missing any of them, which is how it tells a fetch record from any other
#: REPORT without adding a marker field that would change what records are signed
#: over. Kept beside `disclosure_from` rather than beside `fetch_record` because it
#: is a *reader's* requirement: a key added to the record is not automatically one
#: a disclosure may rely on.
_PROVENANCE_KEYS = frozenset(
    {
        "data_source",
        "source_key",
        "covered_start",
        "covered_end",
        "content_hash",
        "store_path",
        "known_limitations",
    }
)


def disclosure_from(
    fetch: Fetch,
    assumptions: str,
    store: SeriesStore,
    repository: ArtifactRepository,
    additional_limitations: str = "",
) -> FetchedDisclosure:
    """Build a metric `Disclosure` from a stored fetch, and refuse otherwise.

    **This is ROADMAP Stage 2's purpose stated as a function.** Every metric
    artifact carries a `data_source` and a `sample_period`, and until Stage 2 both
    were typed at the call site — which is why every number Belay had ever computed
    said, inside its own signature, that the series was supplied by hand.

    **Nothing the caller hands in is trusted except the identifier.** Owner ruling
    Part 36. `fetch` is used to learn *which* record to look for; the record itself
    is re-read from `repository`, the bytes are resolved from `store.root` and the
    record's own signed `store_path`, and the disclosure is built from what came
    off disk. The caller's `fetch.record` and `fetch.stored.path` are deliberately
    ignored.

    **Why it has to work that way, and it took three attempts to get here.**

    - Attempt one took a `MarketDataSource` and a `DailyBarSeries`. A
      `DailyBarSeries` is a frozen dataclass anyone can build, so eight typed bars
      with a real source produced Level C carrying that vendor's name.
    - Attempt two took a `Fetch` and checked its record's signature. `Fetch` and
      `StoredSeries` are also plain dataclasses, and **the signature is an unkeyed
      hash whose `sign` is a public classmethod** — so a caller supplied the seven
      provenance keys, signed the result, and got Level C claiming a licensed
      vendor, a 25-year window and no survivorship bias. `MarketDataSource` was
      never instantiated, so the survivorship guard never ran.

    Both were found by independent passes, not by the author. The lesson is that
    `ArtifactValidator` proves a record is *internally consistent*, never that
    `fetch_record` wrote it. No key set and no marker field can close that, because
    the adversary is the caller in this process and it can reach anything the code
    can reach.

    **The guarantee this does give, stated exactly.** *This record is in the
    repository on disk, these are the bytes it names, and the series is the one it
    describes.* It is **not** "these bytes came from the vendor". Nothing available
    here can prove that: it would need a signature from the source. A caller
    determined to fake provenance must now write a permanent, discoverable record
    into the repository rather than construct an object in memory — a real cost
    that leaves evidence, which is the honest ceiling absent keyed signing.

    Five checks, each refusing rather than downgrading. A caller reaching this
    function is claiming a fetch; an unverifiable claim is an error, not a Level D
    result, and quietly returning Level D would flatter the caller while hiding a
    broken store. **Refusal is this session's reading, not the owner's** — the
    ruling settled what Level C requires, not what happens on failure.
    """
    identifier, version = fetch.record.id, fetch.record.version
    stored_record = repository.get(identifier, version)
    if stored_record is None:
        raise ValueError(
            f"no record {identifier} version {version} in the repository at "
            f"{repository.root}. Owner ruling Part 36: Level C requires the stored "
            "fetch record, so a record that exists only in the caller's hands "
            "cannot earn it."
        )

    content = dict(stored_record.content)
    # Read off the stored record, never off `fetch.record`. Checked by shape rather
    # than a marker key because a marker is exactly as forgeable as these are — the
    # discriminator is that the record came out of the repository, not its fields.
    missing = sorted(_PROVENANCE_KEYS - content.keys())
    if missing:
        raise ValueError(
            f"{identifier} is not a fetch record: its signed content is missing "
            f"{', '.join(missing)}. Only a record written by `fetch_record` carries "
            "the provenance this disclosure claims."
        )

    # The record's OWN signed path, resolved against the store root. Taking the
    # path from `fetch.stored` let a caller point at any file whose bytes happened
    # to hash to the record's digest, which made ADR-014 rule 6's `store_path`
    # inert at read time — the rule exists so a record can name its own bytes.
    path = store.root / content["store_path"]
    digest = content["content_hash"]
    if not path.is_file():
        raise ValueError(
            f"no file at {path}, which is where {identifier} says its bytes are. "
            "A record naming bytes that are not there cannot support a Level C "
            "grade."
        )
    on_disk = hashlib.sha256(path.read_bytes()).hexdigest()
    if on_disk != digest:
        raise ValueError(
            f"the file at {path} hashes to {on_disk}, and {identifier} is signed "
            f"over bytes hashing to {digest}. The stored series is not the one the "
            "record describes."
        )

    # The series the metric will be computed over must be the one the record
    # describes. Without this, a genuine fetch could have its series swapped and the
    # disclosed window and the actual bars would be disjoint, at Level C.
    covered = SamplePeriod(
        start=date.fromisoformat(content["covered_start"]),
        end=date.fromisoformat(content["covered_end"]),
    )
    if len(fetch.series.bars) != content["observations"]:
        raise ValueError(
            f"the series carries {len(fetch.series.bars)} bars and {identifier} "
            f"records {content['observations']}. The disclosure would describe a "
            "different series from the one the metric is computed over."
        )
    if fetch.series.period() != covered:
        raise ValueError(
            f"the series covers {fetch.series.period().start} to "
            f"{fetch.series.period().end} and {identifier} records {covered.start} "
            f"to {covered.end}. Same refusal, by window rather than by count."
        )

    limitations = content["known_limitations"]
    if additional_limitations.strip():
        limitations = f"{limitations} {additional_limitations.strip()}"

    return FetchedDisclosure(
        assumptions=assumptions,
        data_source=content["data_source"],
        sample_period=covered,
        known_limitations=limitations,
    )
