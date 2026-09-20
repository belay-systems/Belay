"""Dependency-free primitives shared by every part of the Artifact contract.

This module imports nothing from Belay, and nothing in Belay may make it do so.
That is the point: `evidence.py` and `integrity.py` both need the same hashing
function, but `integrity.py` imports `artifact.py`, which imports `evidence.py`.
Putting the function in either of them would close an import cycle. Putting it at
the bottom, where it depends on nobody, gives both sides one implementation.

One hashing function means one integrity guarantee. Two would eventually disagree.
"""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone

# MAJOR.MINOR.PATCH, per `Knowledge/Versioning.md` and
# `strategies/NamingConvention.md`. Neither document defines pre-release or
# build-metadata syntax, so neither is accepted.
#
# Digits are `[0-9]` rather than `\d`, which in Python also matches other
# Unicode decimal digits. Those parse as integers too, so `\d` would admit a
# filename that orders identically to one written in ASCII while looking
# nothing like it.
#
# Leading zeros are refused because `01.0.0` denotes the same version as
# `1.0.0` but is a different filename. Storage is append-only, so both could
# exist forever and nothing could say which one is current.
_SEMANTIC_VERSION = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def canonical_digest(payload: dict) -> str:
    """Return the SHA256 of `payload` in a form that is stable across runs.

    Keys are sorted so that two dictionaries holding the same facts hash
    identically regardless of the order they were built in. `default=str`
    is a backstop for values JSON cannot encode on its own; callers should
    still pass already-encoded values (a timestamp as `.isoformat()`, an
    enum as `.value`) rather than relying on it, because `str()` of an
    arbitrary object is not a stable representation.
    """
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()


def is_semantic_version(version: str) -> bool:
    """Return whether `version` is a semantic version: three integers, nothing else.

    `Knowledge/Versioning.md` states that Belay follows semantic versioning and
    gives `1.2.4` as the example; `strategies/NamingConvention.md` repeats it.
    """
    return _SEMANTIC_VERSION.match(version) is not None


def version_key(version: str) -> tuple[int, tuple[int, ...], str]:
    """Return a sort key ordering versions by precedence, oldest first.

    Sorting the strings themselves compares them character by character, which
    puts `0.10.0` before `0.9.0` — so the last element stops being the newest
    version as soon as any component reaches double digits.

    A string that is not a semantic version has no precedence relative to one.
    It sorts below every valid version rather than being dropped: history is
    append-only and must stay searchable, but an unorderable stem must never be
    able to present itself as the newest. Among themselves such strings order
    lexicographically, which is arbitrary but stable — the point is only that
    the same disk contents always produce the same list.

    The leading `0`/`1` rank keeps the two classes from ever being compared
    component-wise, so no pair of keys can raise `TypeError`.
    """
    match = _SEMANTIC_VERSION.match(version)
    if match is None:
        return (0, (), version)
    return (1, tuple(int(part) for part in match.groups()), "")


def utc_now() -> datetime:
    """Return the current time as a timezone-aware UTC datetime.

    Replaces `datetime.utcnow()`, which is deprecated and returns a datetime
    carrying no timezone. A timestamp with no timezone is not reproducible
    evidence: nothing in it says which clock produced it.
    """
    return datetime.now(timezone.utc)
