"""What may be tracked in a public repository.

Belay is public. A commit is publication, and git history cannot be pruned
afterwards, so the question "should this file be in the repository" has to be
answered before the commit lands rather than after.

`.gitignore` answers it for two directories. These tests answer it for the whole
tree, and they ask git what is tracked rather than reading `.gitignore`, so
removing an ignore entry does not switch them off. `.github/CODEOWNERS` makes
this file the owner's alone to change: widening a list below is the owner
deciding that a new kind of file may be published.

Nothing here reads file contents for secrets. GitHub's push protection does
that, and a pattern list kept here would be a weaker copy of it.
"""

from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[1]

# Every kind of file tracked on the day the repository went public. Market data,
# databases, archives, notebooks and spreadsheets are absent on purpose.
ALLOWED_SUFFIXES = frozenset({".md", ".py", ".yml", ".yaml", ".toml", ".json", ".cmd"})

# Tracked files with no suffix, or whose whole name is the suffix.
ALLOWED_NAMES = frozenset({"LICENSE", "CODEOWNERS", ".gitignore"})

# Directories that hold fetched or cloned vendor data on a working machine.
FORBIDDEN_ROOTS = ("data/",)

# Bytes. The one exemption is the session record, which is long because nothing
# in it is ever deleted.
SIZE_LIMIT = 256 * 1024
SIZE_EXEMPT = frozenset({"docs/HANDOFF.md"})


def _tracked() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=REPO, capture_output=True, check=True
    ).stdout
    return [p for p in out.decode("utf-8").split("\0") if p]


def test_git_reports_tracked_files():
    """The guards below pass on an empty list, so an empty list is a failure."""
    assert len(_tracked()) > 100


def test_nothing_is_tracked_under_a_data_directory():
    found = [p for p in _tracked() if p.startswith(FORBIDDEN_ROOTS)]
    assert not found, (
        f"tracked under a data directory: {found}. Fetched and cloned vendor "
        "data is never committed (ADR-013 rule 4), and this repository is "
        "public, so committing it would also publish it."
    )


def test_every_tracked_file_is_of_a_kind_the_owner_has_allowed():
    found = [
        p
        for p in _tracked()
        if PurePosixPath(p).suffix.lower() not in ALLOWED_SUFFIXES
        and PurePosixPath(p).name not in ALLOWED_NAMES
    ]
    assert not found, (
        f"tracked files of a kind not yet allowed: {found}. If this kind of "
        "file belongs in a public repository, the owner adds it to "
        "ALLOWED_SUFFIXES in this file. Do not add it on the owner's behalf."
    )


def test_no_tracked_file_is_large_enough_to_be_a_dataset():
    found = [
        (p, (REPO / p).stat().st_size)
        for p in _tracked()
        if p not in SIZE_EXEMPT
        and (REPO / p).is_file()
        and (REPO / p).stat().st_size > SIZE_LIMIT
    ]
    assert not found, (
        f"tracked files over {SIZE_LIMIT} bytes: {found}. A file this large is "
        "usually data. If it is not, the owner adds it to SIZE_EXEMPT."
    )
