"""The series is stored, versioned, never overwritten — and kept out of git.

ADR-013 rule 4, resting on `Knowledge/Versioning.md:23-27`: "Knowledge records
every version. No version is overwritten. Historical versions remain
searchable."

**Why store at all.** Data vendors restate history. Splits, dividend
adjustments and corrected prints mean the same ticker over the same dates can
return different numbers next month. That is normal vendor behaviour, not a
fault. A backtest run against a series nobody kept is not reproducible, and its
irreproducibility is *silent* — which is the failure mode this repository has
been bitten by repeatedly.

**Why a differing re-fetch is a new version rather than a correction.**
`Versioning.md:27` requires historical versions to remain searchable, and
*which* restatement a result was computed against is part of the result. A
correction would destroy the answer to "what did the data say when we decided
this?"

**Why an identical re-fetch is not a new version.** Nothing was restated, so
there is no new fact to record. Writing one anyway would fill the store with
duplicates and make the version count stop meaning "number of times the vendor's
answer changed".

**Out of git.** Asserted here as well as in `.gitignore`, because the entry is
the enforcement and an enforcement nobody checks is a convention.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from framework.artifacts.repository import ARTIFACT_ROOT, ArtifactRepository
from framework.data.fetch_record import orphan_versions
from framework.data.store import STORE_ROOT, SeriesStore

FIRST = b'[{"date":"2024-01-02","close":"10.75"}]'
RESTATED = b'[{"date":"2024-01-02","close":"10.80"}]'


@pytest.fixture
def store(tmp_path: Path) -> SeriesStore:
    return SeriesStore(root=tmp_path)


# ------------------------------------------------------------ storing at all


def test_a_stored_series_can_be_read_back(store):
    stored = store.store(source="testsource", symbol="AAPL", payload=FIRST)

    assert stored.path.read_bytes() == FIRST


def test_the_stored_version_records_the_content_hash(store):
    """The same fingerprint the fetch record carries, so the artifact and the
    bytes on disk can be checked against each other."""
    import hashlib

    stored = store.store(source="testsource", symbol="AAPL", payload=FIRST)

    assert stored.content_hash == hashlib.sha256(FIRST).hexdigest()


def test_the_first_version_is_version_one(store):
    stored = store.store(source="testsource", symbol="AAPL", payload=FIRST)

    assert stored.version == 1


# --------------------------------------------------------------- versioning


def test_a_restatement_becomes_a_new_version_and_both_survive(store):
    """The rule's central case. Splits and corrected prints change the numbers
    for a window already fetched, and both answers must remain because a past
    result was computed against the earlier one."""
    first = store.store(source="testsource", symbol="AAPL", payload=FIRST)
    second = store.store(source="testsource", symbol="AAPL", payload=RESTATED)

    assert second.version == 2
    assert first.path.read_bytes() == FIRST
    assert second.path.read_bytes() == RESTATED


def test_an_identical_refetch_does_not_create_a_second_version(store):
    """Nothing was restated, so there is no new fact to record. The version
    count means "number of times the vendor's answer changed", and duplicating
    would destroy that meaning."""
    first = store.store(source="testsource", symbol="AAPL", payload=FIRST)
    again = store.store(source="testsource", symbol="AAPL", payload=FIRST)

    assert again.version == first.version
    assert again.path == first.path
    assert len(store.versions(source="testsource", symbol="AAPL")) == 1


def test_every_version_remains_searchable(store):
    """`Versioning.md:27`. A store that can only answer "what is current" cannot
    answer "what did we decide against", which is the question an audit asks."""
    store.store(source="testsource", symbol="AAPL", payload=FIRST)
    store.store(source="testsource", symbol="AAPL", payload=RESTATED)

    versions = store.versions(source="testsource", symbol="AAPL")

    assert [version.version for version in versions] == [1, 2]


def test_versions_are_ordered_oldest_first_beyond_nine(store):
    """Ordering by filename breaks at ten if the number is not zero-padded, and
    the last element silently stops being the newest — the same defect
    `version_key` exists to prevent for semantic versions."""
    for index in range(11):
        store.store(
            source="testsource", symbol="AAPL", payload=b"payload-%d" % index
        )

    versions = store.versions(source="testsource", symbol="AAPL")

    assert [version.version for version in versions] == list(range(1, 12))


def test_the_latest_version_is_the_newest_not_the_alphabetically_last(store):
    for index in range(11):
        store.store(
            source="testsource", symbol="AAPL", payload=b"payload-%d" % index
        )

    assert store.latest(source="testsource", symbol="AAPL").version == 11


def test_a_symbol_never_fetched_has_no_versions(store):
    assert store.versions(source="testsource", symbol="MSFT") == ()
    assert store.latest(source="testsource", symbol="MSFT") is None


def test_two_sources_do_not_share_a_version_sequence(store):
    """Two vendors' answers for the same ticker are different facts. Sharing a
    sequence would make one vendor's restatement look like the other's."""
    store.store(source="alpha", symbol="AAPL", payload=FIRST)
    beta = store.store(source="beta", symbol="AAPL", payload=RESTATED)

    assert beta.version == 1


# ------------------------------------------------------------ never overwrite


def test_an_existing_version_is_never_overwritten(store):
    """`Versioning.md:25`: "No version is overwritten." Enforced rather than
    relied upon — the store refuses even when handed a path that already
    exists."""
    stored = store.store(source="testsource", symbol="AAPL", payload=FIRST)

    with pytest.raises(FileExistsError):
        store._write(stored.path, b"different bytes")


def test_two_symbols_that_sanitise_alike_do_not_share_a_version_chain(store):
    """Found by an independent verification pass. `DYN$A`, `DYN/A` and `DYN A`
    all reduced to `DYN_A`, so distinct instruments shared one chain and
    `latest()` for one could hand back the other's bytes. Nothing was
    overwritten, because the hashes differ — but the version count stopped
    meaning "times this symbol's data was restated"."""
    first = store.store(source="testsource", symbol="DYN$A", payload=FIRST)
    second = store.store(source="testsource", symbol="DYN A", payload=RESTATED)

    assert first.path.parent != second.path.parent
    assert second.version == 1
    assert store.latest(source="testsource", symbol="DYN$A").content_hash == (
        first.content_hash
    )


def test_a_sanitised_symbol_keeps_a_readable_stem(store):
    """The directory is something a person looks at. A pure hash would be safe
    and unreadable; the stem plus a short digest is both."""
    stored = store.store(source="testsource", symbol="DYN$A", payload=FIRST)

    assert stored.path.parent.name.startswith("DYN_A-")


def test_an_ordinary_symbol_is_not_given_a_suffix(store):
    """The common case stays clean: no digest where none is needed."""
    stored = store.store(source="testsource", symbol="AAPL", payload=FIRST)

    assert stored.path.parent.name == "AAPL"


def test_the_stored_bytes_are_exactly_what_was_returned(store):
    """No normalisation, no re-encoding. The hash in the fetch record is over
    the bytes the source returned, so anything the store does to them on the way
    in would make the two disagree."""
    awkward = b"\xef\xbb\xbf{\r\n  \"close\": 10.75\r\n}\x00"
    stored = store.store(source="testsource", symbol="AAPL", payload=awkward)

    assert stored.path.read_bytes() == awkward


# ------------------------------------------------------------------ out of git


def test_the_default_store_root_is_ignored_by_git():
    """ADR-013 rule 4's enforcement. Asked of git itself rather than by reading
    `.gitignore` for a string, because what matters is whether git would
    actually track the file — a rule written in the wrong section, or shadowed
    by a later negation, would still read correctly and behave wrongly.

    Git history cannot be pruned afterwards, which is why this is a test rather
    than a note.
    """
    probe = STORE_ROOT / "testsource" / "AAPL" / "0001-probe.bin"

    result = subprocess.run(
        ["git", "check-ignore", "-q", str(probe)],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
    )

    assert result.returncode == 0, (
        f"{probe} is not ignored by git. ADR-013 rule 4 keeps the fetched "
        "series out of version control, and a repository that starts tracking "
        "it cannot be cleaned afterwards."
    )


def test_the_store_root_is_inside_the_repository_but_not_of_it():
    """The path is relative to the repository so the store travels with a clone,
    while the contents do not. Both halves matter: an absolute path would make
    the store machine-specific and silently empty on another machine."""
    assert not STORE_ROOT.is_absolute()
    assert STORE_ROOT.parts[0] == "data"


def test_no_stored_version_in_this_repository_is_unrecorded():
    """ADR-014 rule 7, run against this repository's own store and artifact root.

    **This is the check that makes `.gitignore`'s claim checkable rather than
    asserted**, which is the property it lacked from the day it was written until
    F-002 was closed: it said the record of what was obtained is "signed and
    permanent", and no record had ever been written to disk.

    On a fresh clone the store is empty and this passes with nothing to check —
    the store is gitignored, so it must, and pretending otherwise would mean
    committing the bytes. It earns its place on the machine that did the
    fetching, which is the only place the question can be asked at all.

    A failure here does not mean the bytes are wrong. It means a stored version
    has no signed statement of where it came from, which is the state F-002 left
    the whole store in and which `docs/HANDOFF.md`'s "A Fetch Stores Its Bytes
    Before Discovering The Series Is Empty" still reaches.
    """
    repo_root = Path(__file__).resolve().parents[2]

    orphans = orphan_versions(
        SeriesStore(root=repo_root / STORE_ROOT),
        ArtifactRepository(root=repo_root / ARTIFACT_ROOT),
    )

    assert orphans == (), (
        f"{len(orphans)} stored version(s) have no fetch record: "
        f"{[stored.relative_path for stored in orphans]}. ADR-014 rule 4 writes "
        "one on every fetch; a version without one cannot say where it came from."
    )


def test_all_versions_finds_files_at_every_depth(tmp_path):
    """`glob("*/*")` walked exactly two levels, so a version file directly under
    a source, or one nested a level deeper, was invisible — and `orphan_versions`
    then returned `()`, which reads as "clean" rather than as "I did not look".

    That is the same shape as the per-symbol gap `all_versions` exists to close,
    one level up.
    """
    store = SeriesStore(root=tmp_path)
    name = "0001-ca978112ca1bbdca.bin"
    for relative in ("src/AAPL", "src", "src/AAPL/deeper", ""):
        directory = tmp_path / relative
        directory.mkdir(parents=True, exist_ok=True)
        (directory / name).write_bytes(b"c")

    found = {stored.relative_path for stored in store.all_versions()}

    assert found == {
        "src/AAPL/" + name,
        "src/" + name,
        "src/AAPL/deeper/" + name,
        name,
    }
