"""The dashboard must read docs/HANDOFF.md correctly.

`scripts/status.py` re-derives the dashboard from the repository on every run,
which is why HANDOFF.md tells future sessions to trust it over any document
including itself. That only holds while it parses what it claims to parse.

It did not. The priority pattern required a blank line between "Priority:" and
the grade; every section in HANDOFF.md writes it inline. So every finding fell
through to "?" and rendered the same grey, and the failure was invisible —
a parser returning its fallback looks exactly like a parser that worked. It
survived at least two sessions and was found by reading the regex, not the page.

These tests exist so the next such drift is loud. They are cheap: the parse is a
regex over one file.
"""

from __future__ import annotations

import re
from pathlib import Path

from scripts import status

REPO = Path(__file__).resolve().parents[1]


def _open_findings_section() -> str:
    text = (REPO / "docs" / "HANDOFF.md").read_text(encoding="utf-8")
    match = re.search(r"\n# Open Findings\n(.*?)(?=\n# )", text, re.S)
    assert match, "the Open Findings section moved or was renamed"
    return match.group(1)


def _normalise(title: str) -> str:
    """Strip the markdown that differs between a table row and a heading."""
    return title.replace("`", "").replace("*", "").replace('"', "").lower().strip()


def test_every_open_finding_has_a_parsed_priority():
    """A "?" here means the parser failed, not that a finding lacks a grade.

    HANDOFF.md gives every open finding a priority in prose. If this goes red,
    either a new section omitted the line or its format drifted from what the
    pattern expects — check the document before touching the regex.
    """
    findings = status.open_findings()

    assert findings, "no findings parsed at all; the Open Findings section moved"

    unparsed = [title for title, priority in findings if priority == "?"]
    assert not unparsed, f"{len(unparsed)} findings have no parsed priority: {unparsed}"


def test_every_parsed_priority_can_be_rendered():
    """Parsing a grade and colouring it are two halves of one contract.

    Both were broken independently: the pattern never matched, and `PILLS` had
    no entry for P1/P2/P3, so a fixed parser would still have rendered the whole
    column the same grey. Passing the parser's own output through the renderer
    catches either half on its own.
    """
    for _, priority in status.open_findings():
        assert priority.lower() in status.PILLS, f"{priority} has no pill colour"


def test_findings_are_ordered_by_priority():
    """The table is a triage list, so P1 belongs above P3.

    While every grade was "?" this sort was inert and the table just followed
    document order. It only started to matter once the parse worked.

    Scoped to parsed grades on purpose. Unparsed ones sort last by a separate
    rule, and folding that in here would make this fail for a parsing reason
    with an ordering message — which the test above already reports properly.
    """
    grades = [priority for _, priority in status.open_findings() if priority != "?"]

    assert grades == sorted(grades), f"findings are not in priority order: {grades}"


def test_every_summary_row_matches_its_section_heading():
    """HANDOFF.md states that each row has a section of the same name.

    `scripts/status.py` counts the *sections*; the table is maintained by hand.
    So the count on the dashboard stays right even when a row's wording drifts
    from its heading — which makes the drift silent, and the table stops being
    checkable against the thing it summarises.

    It happened on 2026-07-30 twice in one session: three rows gained a
    "— ruled by ADR-00X" suffix their headings never got, and a heading kept
    saying 24 modules after the row said 23. Both were caught by hand. This is
    so the next one is caught by the suite.
    """
    section = _open_findings_section()

    headings = [block.splitlines()[0].strip() for block in section.split("\n## ")[1:]]
    rows = re.findall(r"^\| \d+ \| (.+?) \|", section, re.M)

    assert len(rows) == len(headings), (
        f"{len(rows)} table rows against {len(headings)} sections — "
        "every row must have a section and vice versa"
    )

    mismatched = [
        (row, heading)
        for row, heading in zip(rows, headings)
        if _normalise(row) != _normalise(heading)
    ]
    assert not mismatched, f"row/heading wording differs: {mismatched}"


def test_the_table_and_the_dashboard_count_the_same_findings():
    """Two figures derived two ways, which is the only reason to trust either."""
    rows = re.findall(r"^\| \d+ \| (.+?) \|", _open_findings_section(), re.M)

    assert len(rows) == len(status.open_findings())
