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

**What this does not catch**, found by an independent pass and left open because
no shape test can close it: data small enough to sit under the size limit in a
file of an allowed kind, and data pasted into a markdown file. Those are caught
by review or not at all, which is why `AGENTS.md` states the rule in words too.
"""

from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath

REPO = Path(__file__).resolve().parents[1]

# Every kind of file tracked on the day the repository went public. Market data,
# databases, archives, notebooks and spreadsheets are absent on purpose.
ALLOWED_SUFFIXES = frozenset({".md", ".py", ".yml", ".yaml", ".toml", ".json", ".cmd"})

# Tracked files with no suffix, or whose whole name is the suffix. Whole paths,
# so that a `LICENSE` somewhere else in the tree is not waved through.
ALLOWED_PATHS = frozenset({"LICENSE", ".github/CODEOWNERS", ".gitignore"})

# Directories that hold fetched or cloned vendor data on a working machine.
FORBIDDEN_ROOTS = ("data/",)

# Bytes. Markdown gets more room because this project's records are never
# pruned, and the longest of them is already past the smaller limit. Everything
# else is code or configuration, and a quarter of a megabyte of either is
# usually data.
SIZE_LIMIT = 256 * 1024
MARKDOWN_SIZE_LIMIT = 1024 * 1024

# Only ordinary files. A symbolic link or a submodule entry can carry an allowed
# name and point at anything.
ORDINARY_MODES = frozenset({"100644", "100755"})

# The guards, which `.github/CODEOWNERS` must give to exactly the two owners.
# docs/OwnerDecisions.md Part 20c: the second contributor reviews them and does
# not rule on them. Both names are needed because the review ruleset has no
# bypass (Part 20b), so a path with one code owner is a path that person can
# never change. A third name would let someone else approve a guard's removal.
# An empty CODEOWNERS file fails nothing else in the suite.
OWNER = "@pewpewpressco-ux"
REVIEWER = "@eternalaether5"
OWNER_ONLY = (
    "/.github/",
    "/.gitignore",
    "/AGENTS.md",
    "/CLAUDE.md",
    "/.claude/",
    "/pyproject.toml",
    "/LICENSE",
    "/constitution/",
    "/docs/OwnerDecisions.md",
    "/docs/DECISIONS.md",
    "/scripts/public_settings.py",
    "/scripts/status.py",
    "/tests/test_publication_guard.py",
    "/tests/test_rulesets.py",
    "/tests/test_governance_conformance.py",
    "/tests/data/test_store.py",
    "/tests/data/test_dolt_clone.py",
    "/tests/artifacts/test_repository.py",
    "/docs/ENGINEERING_AGENT.md",
    "/CONTRIBUTING.md",
    "/SECURITY.md",
    "/departments/",
    "/workflows/",
    "/Knowledge/",
    "/strategies/",
)


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
        and p not in ALLOWED_PATHS
    ]
    assert not found, (
        f"tracked files of a kind not yet allowed: {found}. If this kind of "
        "file belongs in a public repository, the owner adds it to "
        "ALLOWED_SUFFIXES in this file. Do not add it on the owner's behalf."
    )


def test_every_tracked_entry_is_an_ordinary_file():
    out = subprocess.run(
        ["git", "ls-files", "-s", "-z"], cwd=REPO, capture_output=True, check=True
    ).stdout.decode("utf-8")
    found = [e for e in out.split("\0") if e and e.split(" ", 1)[0] not in ORDINARY_MODES]
    assert not found, f"tracked symbolic links or submodules: {found}"


def test_no_tracked_file_is_large_enough_to_be_a_dataset():
    def limit(path: str) -> int:
        return MARKDOWN_SIZE_LIMIT if path.lower().endswith(".md") else SIZE_LIMIT

    found = [
        (p, (REPO / p).stat().st_size)
        for p in _tracked()
        if (REPO / p).is_file() and (REPO / p).stat().st_size > limit(p)
    ]
    assert not found, (
        f"tracked files over their size limit: {found}. A file this large is "
        "usually data. If it is not, raising the limit is the owner's decision."
    )


def test_the_guards_need_both_owners_in_codeowners():
    """CODEOWNERS is last-match-wins, so what counts is the last line that
    matches each guard, not whether the guard has a line. The first version of
    this test looked each pattern up by name, and an independent pass voided
    every owner-only line by moving the catch-all to the end, suite green.

    Only the three pattern shapes this file uses are resolved: `*`, an exact
    path, and a directory ending in `/`."""
    lines = [
        line.split()
        for line in (REPO / ".github" / "CODEOWNERS").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    def owners_for(path: str) -> list[str] | None:
        winner = None
        for pattern, *owners in lines:
            if pattern == "*" or pattern == path or (
                pattern.endswith("/") and path.startswith(pattern)
            ):
                winner = owners
        return winner

    shapes = [p for p, *_ in lines if p != "*" and not p.startswith("/")]
    assert not shapes, f"patterns this test cannot resolve, so cannot vouch for: {shapes}"
    wrong = {p: owners_for(p) for p in OWNER_ONLY if owners_for(p) != [OWNER, REVIEWER]}
    assert not wrong, f"not owner-and-reviewer in .github/CODEOWNERS: {wrong}"
