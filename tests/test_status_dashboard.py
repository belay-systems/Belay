"""The dashboard must read the findings register (docs/FINDINGS.md) correctly.

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
    text = (REPO / "docs" / "FINDINGS.md").read_text(encoding="utf-8")
    match = re.search(r"^## Open\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    assert match, "docs/FINDINGS.md has no '## Open' section; it moved or was renamed"
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


def test_every_archived_row_names_a_section_of_the_archive():
    """A row written up in the archive must name a section that is there.

    Until 2026-09-25 the register was a table *and* one prose section per
    finding in docs/HANDOFF.md, and this test caught their wording drifting
    apart (twice on 2026-07-30). The table is now the register and the
    sections are frozen, so the check becomes: every row marked "archive"
    names, word for word, a section under the archive's `# Open Findings`.
    A row that does not is a finding nobody can read up on.
    """
    headings = set(_archived_headings())
    missing = [row[0] for row in _table_rows() if row[3] == "archive" and row[0] not in headings]
    assert not missing, f"rows marked 'archive' with no section of that title: {missing}"


def test_every_other_row_names_a_file_that_exists():
    """A finding not in the archive is written up somewhere else; that file must exist."""
    missing = [
        (row[0], row[3])
        for row in _table_rows()
        if row[3] != "archive" and not (REPO / row[3].strip("`").split(":")[0]).exists()
    ]
    assert not missing, f"rows whose write-up does not exist: {missing}"


def test_every_row_has_four_cells_and_a_unique_title():
    rows = _table_rows()
    assert all(len(row) == 4 for row in rows), [row for row in rows if len(row) != 4]
    titles = [row[0] for row in rows]
    assert len(titles) == len(set(titles)), "two rows share a title"


def test_the_table_and_the_dashboard_count_the_same_findings():
    """Two figures derived two ways, which is the only reason to trust either."""
    assert len(_table_rows()) == len(status.open_findings())


# ------------------------------------------------ helpers for the tests above


def _archived_headings() -> list[str]:
    """The `## ` headings under `# Open Findings` in the frozen archive."""
    text = (REPO / "docs" / "HANDOFF.md").read_text(encoding="utf-8")
    match = re.search(r"\n# Open Findings\n(.*?)(?=\n# )", text, re.S)
    assert match, "docs/HANDOFF.md lost its Open Findings section, and it is frozen"
    return [block.splitlines()[0].strip() for block in match.group(1).split("\n## ")[1:]]


def _table_rows() -> list[list[str]]:
    """Every data row of the Open table, split into cells, by a second route.

    Deliberately not `status.FINDING_ROW`: a count checked against the parser's
    own pattern would agree with itself whatever the file said.
    """
    rows = []
    for line in _open_findings_section().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and cells[0] not in ("Finding",) and set(cells[0]) != {"-"}:
            rows.append(cells)
    return rows
