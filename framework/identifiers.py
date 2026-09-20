"""Artifact identifiers.

`Knowledge/Identifiers.md` defines eight prefixes and states the rule plainly:
"Identifiers are permanent. They are never reused. Titles may change. Versions may
change. Identifiers never change."

This module had six of the eight prefixes and no way to check one. REGIME and DOC
were missing, and nothing validated the format, so `DD-0001` — a prefix that has
never existed — was in use in the drawdown tests.

Uniqueness is not enforced here, and cannot be: this module sees one identifier at
a time. `ArtifactRepository` is where reuse becomes destructive, and it refuses to
overwrite a stored version.
"""

from __future__ import annotations

import re

PREFIXES = {
    "strategy": "STRAT",
    "experiment": "EXP",
    "research": "RS",
    "review": "REV",
    "report": "RPT",
    "regime": "REGIME",
    "workflow": "WF",
    "documentation": "DOC",
}

VALID_PREFIXES = frozenset(PREFIXES.values())

# STRAT-0001, RPT-0217, REGIME-0010 — and RPT-10000 once four digits run out.
#
# **Four is the minimum width, not the width.** This read `\d{4}` until
# 2026-08-02, which capped every prefix at 10,000 identifiers for all time
# against `Knowledge/Identifiers.md:3-5` making them permanent and never reused.
# ADR-014 rule 4 mints one per stored series version, so a 6,000-symbol backfill
# would have spent 60% of the RPT space in a single run — and RPT is shared with
# every other REPORT artifact Belay will ever produce.
#
# **The document never stated a count.** It gives seven examples and every one
# of them happens to use four digits; this module turned the examples into a
# rule, which is why widening it amends no governance document. All seven
# examples remain valid, and so does every identifier ever issued.
#
# **The alternation refuses a padded alias rather than accepting `\d{4,}`.**
# `RPT-00217` and `RPT-0217` would otherwise both be valid, denote the same
# number, and become two different directories under
# `ArtifactRepository.path_for` — permanently, since identifiers are never
# corrected.
#
# **`[0-9]` rather than `\d`, and `\Z` rather than `$`.** Both were wrong in the
# first version of this widening and an independent pass found them: `\d` is
# Unicode-aware, so `RPT-٠١٢٣` (Arabic-Indic) and
# `RPT-०१२३` (Devanagari) validated and mapped to the same
# `identifier_key` as `RPT-0123` — three directories for one number, reached
# through `save()`. `$` matches before a trailing newline, so an identifier with
# one on the end was a fourth. The `[1-9]` branch was already ASCII-only, which
# made the four-digit branch the looser of the two and nothing said so.
PATTERN = re.compile(r"^([A-Z]+)-([0-9]{4}|[1-9][0-9]{4,})\Z")


def build(prefix: str, number: int) -> str:
    """Return an identifier for a kind of artifact, e.g. build("report", 217).

    Pads to a minimum of four digits rather than to a width of four, so numbers
    below 10,000 render exactly as they always have and larger ones render
    without a padded alias. Before the pattern was widened this function already
    emitted `RPT-10000` for 10,000 while `validate()` refused it — the two halves
    of this module disagreed about what it had produced.
    """
    if prefix not in PREFIXES:
        raise ValueError(f"Unknown artifact kind {prefix!r}. Known: {sorted(PREFIXES)}")
    return f"{PREFIXES[prefix]}-{number:04d}"


def identifier_key(identifier: str) -> tuple[int, str, int, str]:
    """Return a sort key ordering identifiers by prefix, then by number.

    Sorting the strings themselves compares them character by character, which
    puts `RPT-10000` before `RPT-9999`. **A fixed width hid this and the width is
    no longer fixed**, so the ordering has to be stated rather than inherited
    from the filesystem. It is the third time this repository has met the same
    defect: `framework/artifacts/primitives.py:58-78` exists because `0.10.0`
    sorted before `0.9.0`, and `framework/data/store.py:41-49` zero-pads version
    filenames for the same reason.

    A string that is not a valid identifier sorts below every valid one rather
    than being dropped, and orders lexicographically among its own kind —
    `version_key`'s convention, for `version_key`'s reason: history stays
    searchable, and nothing unorderable may present itself as the newest.

    The leading `0`/`1` rank keeps the two classes from ever being compared
    field by field, so no pair of keys can raise `TypeError`.
    """
    match = PATTERN.match(identifier or "")
    if match is None or match.group(1) not in VALID_PREFIXES:
        return (0, "", 0, identifier or "")
    return (1, match.group(1), int(match.group(2)), "")


def is_valid(identifier: str) -> bool:
    match = PATTERN.match(identifier or "")
    return bool(match) and match.group(1) in VALID_PREFIXES


def validate(identifier: str) -> str:
    """Return the identifier unchanged, or raise explaining why it is not one."""
    if not is_valid(identifier):
        raise ValueError(
            f"Invalid artifact identifier {identifier!r}. Expected PREFIX-NNNN "
            f"with a prefix from {sorted(VALID_PREFIXES)}, for example RPT-0217."
        )
    return identifier
