"""The series is stored, versioned, never overwritten — and kept out of git.

ADR-013 rule 4, resting on `Knowledge/Versioning.md:23-27`: "Knowledge records
every version. No version is overwritten. Historical versions remain
searchable." That passage has never been cited for this before.

**Why store at all.** Data vendors restate history. Splits, dividend
adjustments and corrected prints mean the same ticker over the same dates can
return different numbers next month. That is normal vendor behaviour rather than
a fault, and it has two consequences: a backtest run against a series nobody
kept is not reproducible, and *its irreproducibility is silent*.

**Why a differing re-fetch is a new version and not a correction.** Which
restatement a result was computed against is part of the result. Correcting in
place would destroy the answer to "what did the data say when we decided this?",
which is the question Law VII exists to keep answerable.

**Why out of git, and why that is a ruling rather than an omission.** Git
retains every version of every file permanently by design, so a daily-refreshed
series makes repository growth unbounded with no prunable path. A vendor licence
may restrict retention independently of visibility. And rule 3 already covers
the integrity requirement — the fetch record carries the content hash, so
committing the bytes adds no guarantee rule 3 does not already provide. The
`.gitignore` entry is the enforcement; `tests/data/test_store.py` asks git
itself whether it holds.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

# Relative, so the store travels with a clone while its contents do not. An
# absolute path would make the store machine-specific and silently empty
# everywhere else, which is the kind of failure that only shows up as a backtest
# quietly having no data.
STORE_ROOT = Path("data") / "market"

# 0001-<16 hex>.bin — the version zero-padded so filename order is version
# order, and the content hash in the name so a duplicate can be recognised
# without opening every file.
#
# Zero padding is not cosmetic. `framework/artifacts/primitives.py:58-78` exists
# because sorting version strings character by character puts `0.10.0` before
# `0.9.0`; the same defect here would make the tenth fetch sort before the
# second and the "latest" version stop being the newest.
_VERSION_FILE = re.compile(r"^(\d{4})-([0-9a-f]{16})\.bin$")
_HASH_PREFIX = 16


@dataclass(frozen=True, slots=True)
class StoredSeries:
    """One version of one symbol's bytes, as stored.

    `relative_path` is where the file sits **inside the store**, as a POSIX
    string, and it exists because ADR-014 rule 6 puts it inside a fetch record's
    integrity hash. Both properties are load-bearing there: `path` is absolute
    on most callers, so signing it would carry one machine's home directory into
    a permanent record, and a Windows separator would make the identical fetch
    sign differently on two machines.
    """

    version: int
    path: Path
    content_hash: str
    relative_path: str


def _slug(value: str) -> str:
    """Return `value` reduced to characters that are safe in a path.

    A ticker can contain characters a filesystem treats specially — the DoltHub
    symbol table carries entries such as `DYN$A` for preferred series — and a
    symbol that silently became a directory separator would write outside the
    store.

    **The replacement alone is not injective**, and that was a real defect until
    2026-08-01: `DYN$A`, `DYN/A` and `DYN A` all reduced to `DYN_A`, so two
    distinct symbols shared one version chain and `latest()` for one could
    return the other's bytes. Nothing was ever overwritten — the hashes differ —
    but the version count stopped meaning what `store()` says it means. A short
    digest of the original value is appended so distinct inputs stay distinct,
    while the readable stem survives for anyone looking at the directory.
    """
    cleaned = re.sub(r"[^A-Za-z0-9._-]", "_", value)
    if not cleaned or cleaned.strip(".") == "":
        raise ValueError(f"{value!r} does not reduce to a usable path segment")

    if cleaned == value:
        return cleaned

    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:8]
    return f"{cleaned}-{digest}"


class SeriesStore:
    """A versioned, append-only home for fetched bytes.

    Stores bytes exactly as returned. No normalisation and no re-encoding: the
    hash in the fetch record is taken over what the source returned, so anything
    done to the bytes on the way in would make the artifact and the disk
    disagree about what was fetched.
    """

    def __init__(self, root: Path | str = STORE_ROOT) -> None:
        self.root = Path(root)

    def _directory(self, source: str, symbol: str) -> Path:
        return self.root / _slug(source) / _slug(symbol)

    def versions(self, source: str, symbol: str) -> tuple[StoredSeries, ...]:
        """Return every stored version, oldest first.

        `Versioning.md:27` — historical versions remain searchable. A store that
        could only answer "what is current" could not answer "what did we decide
        against", which is the question an audit asks.
        """
        directory = self._directory(source, symbol)
        if not directory.is_dir():
            return ()

        found = []
        for path in directory.iterdir():
            match = _VERSION_FILE.match(path.name)
            if match:
                found.append(
                    StoredSeries(
                        version=int(match.group(1)),
                        path=path,
                        content_hash=self._full_hash(path),
                        relative_path=self._relative(path),
                    )
                )

        # Sorted on the parsed integer rather than the filename, so the ordering
        # does not depend on the padding width being sufficient.
        return tuple(sorted(found, key=lambda stored: stored.version))

    def latest(self, source: str, symbol: str) -> StoredSeries | None:
        versions = self.versions(source, symbol)
        return versions[-1] if versions else None

    def store(self, source: str, symbol: str, payload: bytes) -> StoredSeries:
        """Store `payload` and return the version it became.

        A re-fetch whose bytes are identical returns the existing version rather
        than writing a second copy: nothing was restated, so there is no new
        fact to record, and the version count keeps meaning "number of times the
        vendor's answer changed".
        """
        digest = hashlib.sha256(payload).hexdigest()

        existing = self.versions(source, symbol)
        for stored in existing:
            if stored.content_hash == digest:
                return stored

        version = existing[-1].version + 1 if existing else 1
        directory = self._directory(source, symbol)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / f"{version:04d}-{digest[:_HASH_PREFIX]}.bin"

        self._write(path, payload)
        return StoredSeries(
            version=version,
            path=path,
            content_hash=digest,
            relative_path=self._relative(path),
        )

    def _relative(self, path: Path) -> str:
        """Return `path` relative to the store root, as POSIX.

        `as_posix()` rather than `str()`, because this string goes inside a fetch
        record's integrity hash under ADR-014 rule 6 — and a backslash would make
        the same fetch, from the same source, produce a different signature on
        Windows than on Linux.
        """
        return path.relative_to(self.root).as_posix()

    def _write(self, path: Path, payload: bytes) -> None:
        """Write `payload` to `path`, refusing to replace anything.

        `Versioning.md:25`: "No version is overwritten." Enforced with an
        exclusive create rather than a prior existence check, because the check
        and the write would be two steps with a gap between them.
        """
        with open(path, "xb") as handle:
            handle.write(payload)

    def _full_hash(self, path: Path) -> str:
        """Return the SHA256 of the stored bytes.

        Read from the file rather than taken from the filename. The name carries
        a truncated digest for cheap duplicate detection; the full hash is what
        the fetch record is signed over, and a truncation must never be able to
        pass as one.
        """
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def all_versions(self) -> tuple[StoredSeries, ...]:
        """Return every stored version of every symbol, across every source.

        ADR-014 rule 7 needs the whole store rather than one series: the check it
        names is "does every stored version have a record", and a per-symbol
        method can only answer it for symbols somebody already thought to ask
        about — which is exactly the shape of the gap that let F-002 run for the
        life of the module.

        Ordered by path so the same disk contents always produce the same list.
        """
        if not self.root.is_dir():
            return ()

        # **Every depth, not `glob("*/*")`.** The first version of this walked
        # exactly two levels, so a version file directly under a source, or one
        # nested a level deeper, was invisible — and `orphan_versions` then
        # returned `()`, which is indistinguishable from "clean" rather than from
        # "I did not look". That is the same shape as the per-symbol gap this
        # docstring argues against, one level up.
        #
        # Never re-slugged back to a source and symbol: `_slug` appends a digest
        # for an unsafe ticker and is not reversible, so a walk that recovered
        # names and then asked `versions()` for them would silently return
        # nothing for exactly the symbols `_slug` exists to protect.
        found = [
            StoredSeries(
                version=int(_VERSION_FILE.match(path.name).group(1)),
                path=path,
                content_hash=self._full_hash(path),
                relative_path=self._relative(path),
            )
            for path in sorted(self.root.rglob("*"))
            if path.is_file() and _VERSION_FILE.match(path.name)
        ]
        return tuple(found)
