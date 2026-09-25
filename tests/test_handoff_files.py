"""The shape of the handoff files, held by tests (`docs/OwnerDecisions.md` Part 29).

Until 2026-09-25 one file, `docs/HANDOFF.md`, did two jobs. It said what was
true now, and it kept every earlier session's account, with nothing ever
deleted. It reached 5,857 lines. An agent's file reader takes a few thousand
lines, or about 25,000 tokens, at a time, so no agent could read it in one
pass. The current next-task list sat at the bottom, under five superseded
ones, while `AGENTS.md` said the top-most block was current.

The two jobs are now split:

- `docs/NOW.md` is the current state. It is rewritten at every close, and
  capped so that it can always be read in one pass.
- `docs/sessions/` holds history, one file per session, and each file is
  never edited after it merges.
- `docs/HANDOFF.md` is the archive, frozen byte for byte, so none of the
  line citations into it can move.
- `docs/FINDINGS.md` is the findings register, one row per finding.

Every rule here is one that a convention alone failed to hold in this
repository (Issue #9 is the measured case). So each one fails the build.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOCS = REPO / "docs"
NOW = DOCS / "NOW.md"
FINDINGS = DOCS / "FINDINGS.md"
HANDOFF = DOCS / "HANDOFF.md"
SESSIONS = DOCS / "sessions"

#: SHA-256 of `docs/HANDOFF.md` with line endings normalised to LF, so a
#: Windows checkout that converts them still matches.
FROZEN_HANDOFF_SHA256 = "ab73c9d3ad1669b414eb37d3100dab3eb15926abc7708ca1e4d81cb4c1220e8a"

NOW_MAX_LINES = 200
NOW_MAX_BYTES = 16_000
SESSION_MAX_LINES = 300
SESSION_NAME = re.compile(r"\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md")


def _lf_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def test_the_archive_is_frozen():
    """`docs/HANDOFF.md` never changes again, so no citation into it moves.

    Two hundred and forty-one `path:line` citations point into this file and
    its three large neighbours, many of them from review reports that may not
    be edited. Freezing the archive is what keeps every one of them true.
    """
    digest = hashlib.sha256(_lf_bytes(HANDOFF)).hexdigest()
    assert digest == FROZEN_HANDOFF_SHA256, (
        "docs/HANDOFF.md is a frozen archive (docs/OwnerDecisions.md Part 29) "
        "and it has changed. A session's record goes in "
        "docs/sessions/YYYY-MM-DD-short-name.md; what is true now goes in "
        "docs/NOW.md; a finding opened or closed goes in docs/FINDINGS.md. If "
        "this branch appended to docs/HANDOFF.md before the freeze reached it, "
        "move that text to those files and restore docs/HANDOFF.md from main."
    )


def test_now_fits_in_one_read():
    """The start-up file has to be readable in one pass, by any agent."""
    lines = _lf_bytes(NOW).count(b"\n")
    size = len(_lf_bytes(NOW))
    assert lines <= NOW_MAX_LINES and size <= NOW_MAX_BYTES, (
        f"docs/NOW.md is {lines} lines and {size} bytes; the cap is "
        f"{NOW_MAX_LINES} lines and {NOW_MAX_BYTES} bytes. It holds what is true "
        "now, not how it came to be: move history into this session's record "
        "under docs/sessions/."
    )


def test_now_has_exactly_one_next_task_list():
    """One list, so there is never a question of which one is current.

    The archive ended with six next-task headings, and the rule for which one
    counted ("top-most") was the opposite of the practice ("bottom-most").
    """
    headings = re.findall(
        r"^#+\s*highest priority next task\b.*$", NOW.read_text(encoding="utf-8"), re.M | re.I
    )
    assert headings == ["## Highest Priority Next Task"], (
        f"docs/NOW.md must have exactly one '## Highest Priority Next Task'; found {headings}. "
        "Replace the list at session close; do not add another below it."
    )


def test_now_keeps_the_sections_a_session_starts_from():
    text = NOW.read_text(encoding="utf-8")
    for heading in ("## Where things stand", "## Highest Priority Next Task", "## Working Agreement"):
        assert re.search(rf"^{re.escape(heading)}\s*$", text, re.M), f"docs/NOW.md lost {heading!r}"


def test_session_records_are_named_by_date_and_capped():
    """One file per session, found by date, and too short to become a monolith."""
    bad_names, too_long = [], []
    for path in sorted(SESSIONS.glob("*")):
        if path.name == "README.md":
            continue
        if not SESSION_NAME.fullmatch(path.name):
            bad_names.append(path.name)
        elif _lf_bytes(path).count(b"\n") > SESSION_MAX_LINES:
            too_long.append(path.name)
    assert not bad_names, f"docs/sessions/ files must be named YYYY-MM-DD-short-name.md: {bad_names}"
    assert not too_long, (
        f"session records over {SESSION_MAX_LINES} lines: {too_long}. Split the "
        "work, or put the long part in docs/proposals/."
    )


def test_nothing_cites_a_rewritten_file_by_line_number():
    """`docs/NOW.md` and `docs/FINDINGS.md` are rewritten, so a line number rots.

    Cite them by heading or by a finding's title instead. The pattern is built
    from pieces so this file does not match itself.
    """
    pattern = re.compile(r"docs/(?:NOW|FINDINGS)\.md" + r":\d")
    offenders = []
    for path in REPO.rglob("*"):
        if ".git" in path.parts or not path.is_file() or path.suffix not in {".md", ".py", ".yml", ".yaml", ".toml"}:
            continue
        if pattern.search(path.read_text(encoding="utf-8", errors="replace")):
            offenders.append(str(path.relative_to(REPO)))
    assert not offenders, f"line citations into a rewritten file: {offenders}"
