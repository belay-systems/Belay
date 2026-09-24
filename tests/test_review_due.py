"""The cadence gate, run for real against a repository built for the purpose.

`tests/test_session_handoff.py` holds the gate's pure pieces — a branch name, two
regular expressions. Nothing there ever ran `git()`, `highest_finding()` or
`main()`, which is how `scripts/review_due.py` came to crash on the owner's
machine on 2026-09-19 with every test green: the first Markdown file containing
a byte cp1252 cannot decode (0x81, the second byte of "Ł") turned git's output
into `None`, and `None` went into a regex.

**Why two kinds of test, and what each is worth.** CI runs on Linux, where the
locale is UTF-8 and the original defect cannot occur. A test that only
reproduces it under a real cp1252 locale is red on Windows and green everywhere
else, including against the unfixed script — so it would have guarded nothing
where the suite is actually enforced. The in-process tests below therefore
*simulate* the Windows locale (any `subprocess.run(text=True)` with no
`encoding=` decodes as cp1252, which is precisely what Windows does) and are red
against the unfixed script on every platform. The one subprocess test is the
genuine article on Windows and an end-to-end smoke test elsewhere; its docstring
says so.

**What none of this checks.** That the cloud routine, on its own machine, gets
the same answer. That is believed and not observed.
"""

from __future__ import annotations

import importlib.util
import io
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "review_due.py"

#: Characters the fixture's prose carries. None of "κ̂ ≥ Ł" exists in cp1252, and
#: "Ł" is U+0141 = C5 81 in UTF-8 — 0x81 is one of the five bytes cp1252 leaves
#: undefined, so it is the byte that raises rather than merely garbling.
PROSE = "κ̂ ≥ — Ł\n\nF-123 is the highest finding anywhere in this fixture.\n"

#: A branch whose name cannot be encoded as cp1252 either, holding the newest
#: report, so that the verdict line itself has to print it.
BRANCH = "review/Łódź"

#: Hermetic git: no user or system config, a fixed identity, no signing.
GIT_ENV = {
    **os.environ,
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_AUTHOR_NAME": "fixture",
    "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
    "GIT_COMMITTER_NAME": "fixture",
    "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
}


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, env=GIT_ENV, check=True, capture_output=True)


def _commit(repo: Path, files: dict[str, bytes], message: str) -> None:
    for name, content in files.items():
        path = repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", message)


def _clone_with(tmp_path: Path, prose: bytes, files: dict[str, bytes] | None = None) -> Path:
    """Build an upstream and return a clone of it, which is what the gate reads.

    `main` carries an old report, the prose under test and any other `files`.
    `review/Łódź` carries a newer report that was never merged — the 2026-08-21
    situation — so a correct verdict must name that branch. Both reports are
    long past the twelve-day threshold, so the verdict is DUE and a number must
    be printed.
    """
    upstream = tmp_path / "upstream"
    upstream.mkdir()
    _git(upstream, "init", "-b", "main")
    _commit(
        upstream,
        {
            "docs/notes.md": prose,
            "reports/review/2026-01-02-review.md": b"# Review\n\n### F-007\n",
            **(files or {}),
        },
        "main",
    )
    _git(upstream, "switch", "-c", BRANCH)
    _commit(
        upstream,
        {"reports/review/2026-01-05-review.md": b"# Review\n\n### F-008\n"},
        "an unmerged review",
    )
    _git(upstream, "switch", "main")

    clone = tmp_path / "clone"
    _git(tmp_path, "clone", str(upstream), str(clone))
    return clone


@pytest.fixture
def clone(tmp_path: Path) -> Path:
    return _clone_with(tmp_path, PROSE.encode("utf-8"))


def _gate():
    """Import `scripts/review_due.py`, which is not an importable package."""
    spec = importlib.util.spec_from_file_location("review_due", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def cp1252_locale(monkeypatch):
    """Make text-mode subprocesses decode as cp1252 unless told otherwise.

    That is the whole of what a Windows locale does to `subprocess.run`: with
    `text=True` and no `encoding=`, output is decoded with the locale encoding.
    A caller that names its encoding, or reads bytes, is untouched — which is
    the property under test.
    """
    real_run = subprocess.run

    def run(*args, **kwargs):
        text = kwargs.get("text") or kwargs.get("universal_newlines")
        if text and not kwargs.get("encoding"):
            kwargs["encoding"] = "cp1252"
        return real_run(*args, **kwargs)

    monkeypatch.setattr(subprocess, "run", run)


def _run_main(clone: Path, monkeypatch) -> tuple[int, str, str]:
    """Run `main()` in `clone` with stdout a cp1252 pipe, as Windows gives it.

    Returns (exit code, stdout, stderr). Stdout is decoded as UTF-8 because
    that is what every reader of this script's output — the harness, the cloud
    routine — assumes; bytes that are not UTF-8 come back as U+FFFD, which is
    the "�" the owner saw in place of the em dash.
    """
    out, err = io.BytesIO(), io.BytesIO()
    monkeypatch.chdir(clone)
    monkeypatch.setattr(sys, "stdout", io.TextIOWrapper(out, encoding="cp1252"))
    monkeypatch.setattr(
        sys, "stderr", io.TextIOWrapper(err, encoding="cp1252", errors="backslashreplace")
    )
    code = _gate().main()
    sys.stdout.flush()
    sys.stderr.flush()
    return code, out.getvalue().decode("utf-8", "replace"), err.getvalue().decode("utf-8", "replace")


# ------------------------------------------------------------- the 2026-09-19 crash


def test_the_gate_answers_when_prose_holds_bytes_cp1252_cannot_decode(
    clone, cp1252_locale, monkeypatch
):
    """The defect itself: a verdict and a number, not a traceback.

    F-123 is in the one file a cp1252 decode chokes on, so this also proves the
    file was *read* — a fix that skipped undecodable files would print F-009
    here, which is a wrong number delivered with a straight face and strictly
    worse than the crash.
    """
    code, out, _ = _run_main(clone, monkeypatch)

    assert code == 0
    assert out.startswith("DUE")
    assert "first finding: F-124" in out


def test_the_verdict_prints_whatever_the_branch_is_called(clone, cp1252_locale, monkeypatch):
    """Printing must not be able to raise, and must arrive readable.

    The newest report sits on `review/Łódź`, so the verdict line carries a name
    a cp1252 stdout cannot encode: `UnicodeEncodeError`, the same crash
    `scripts/belay.py` has. And the em dash, which cp1252 *can* encode, arrives
    as byte 0x97 — not UTF-8 — and renders as "�" for every reader that assumes
    UTF-8. Both are one defect: the script's output encoding was left to the
    machine it happened to run on.
    """
    code, out, _ = _run_main(clone, monkeypatch)

    assert code == 0
    assert f"on {BRANCH})" in out
    assert "DUE — last review was" in out
    assert "�" not in out


# ------------------------------------------- unreadable output is not an empty file


@pytest.mark.parametrize(
    "prose",
    [
        pytest.param("x — F-200 was saved as cp1252.\n".encode("cp1252"), id="cp1252"),
        pytest.param("F-200 was written by PowerShell.\n".encode("utf-16"), id="utf-16-with-mark"),
    ],
)
def test_the_gate_stops_without_a_number_when_prose_is_not_utf8(prose, tmp_path, monkeypatch):
    """A file the gate cannot read must stop it, never be skipped.

    **The cp1252 case is the one that pins the strict decode**, and the second
    independent pass is why it exists. UTF-16 is the realistic accident on the
    owner's machine — Windows PowerShell's `>` writes it — but it is full of
    NULs, so once the gate refused NULs that fixture stopped for *that* reason
    and a lenient decode passed every test. A cp1252 file has no NUL: only
    strictness stops it, and decoded leniently its stray bytes can sit against
    an `F-NNN` and break the word boundary the regex needs.

    A failure is a stop: exit 2, nothing on stdout, and the ref and path named.
    """
    clone = _clone_with(tmp_path, prose)

    code, out, err = _run_main(clone, monkeypatch)

    assert code == 2, "0 is DUE and 1 is SKIP; this is neither"
    assert out == "", "stdout is where a verdict goes, so a stop leaves it empty"
    assert "docs/notes.md" in err and "not UTF-8" in err


def test_the_gate_stops_on_utf16_that_happens_to_be_valid_utf8(tmp_path, monkeypatch):
    """The hole in "strict": found by the independent pass, not by the author.

    UTF-16 *without* a byte-order mark, holding only ASCII, is valid UTF-8 — it
    is ASCII with a NUL after every character. A strict decode accepts it, the
    regex sees an F, a NUL, a hyphen, a NUL, and matches nothing, and the gate
    printed `first finding: F-009` over a repository holding F-200. No Markdown
    file has a reason to contain a NUL, so one is treated as what it is: a file
    the gate cannot read.
    """
    # A UTF-8 preamble first, so that a check of only the start of the file fails.
    prose = ("plain text\n" * 40).encode("utf-8") + "F-200 has no mark.\n".encode("utf-16-le")
    clone = _clone_with(tmp_path, prose)

    code, out, err = _run_main(clone, monkeypatch)

    assert code == 2
    assert out == ""
    assert "docs/notes.md" in err and "NUL" in err


def test_the_gate_stops_without_a_number_when_git_fails_on_a_listed_file(
    clone, monkeypatch
):
    """`git()` answered "" for a failed command, and "" reads as an empty file.

    Every `git show` here fails. Treated as empty, no finding exists anywhere
    and the gate prints `first finding: F-001` — over a repository whose prose
    says F-123.
    """
    real_run = subprocess.run

    def run(cmd, *args, **kwargs):
        if list(cmd[:2]) == ["git", "show"]:
            return real_run(["git", "show", "no-such-ref:no-such-path"], *args, **kwargs)
        return real_run(cmd, *args, **kwargs)

    monkeypatch.setattr(subprocess, "run", run)

    code, out, err = _run_main(clone, monkeypatch)

    assert code == 2
    assert out == ""
    assert "git show" in err


def test_a_directory_that_is_not_a_repository_is_still_told_so(tmp_path, monkeypatch):
    """The one git failure that is an answer rather than an accident.

    `.claude/skills/belay-review/SKILL.md` quotes this message, so making
    `git()` strict must not turn it into the generic stop above.
    """
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path.parent))

    code, out, _ = _run_main(tmp_path, monkeypatch)

    assert code == 1
    assert "not a git repository; cannot answer across refs" in out
    assert "first finding" not in out


# ------------------------------------------- numbers the gate must not take on trust
#
# Each fixture below also holds F-123 in `docs/notes.md`, so the right answer is
# F-124 unless the case says otherwise. Found by independent passes on #27.


def _first_finding(tmp_path: Path, monkeypatch, prose: str, files=None) -> tuple[int, str, str]:
    clone = _clone_with(
        tmp_path,
        prose.encode("utf-8"),
        {name: text.encode("utf-8") for name, text in (files or {}).items()},
    )
    return _run_main(clone, monkeypatch)


#: A report shaped like the review skill's template, with the given body for its
#: `## Outside text` section and a real finding before it.
def _report(outside: str, after: str = "") -> str:
    return (
        "# Belay Review — 2026-01-03\n\n"
        "## Findings\n\n### F-130 — a real finding — **High**\n\nIt cites F-129 too.\n\n"
        "## Not found\n\nNothing.\n\n"
        f"## Outside text\n\n{outside}\n{after}"
    )


REPORT_PATH = "reports/review/2026-01-03-review.md"


@pytest.mark.parametrize(
    "digits", [pytest.param("９９９", id="fullwidth"), pytest.param("٩٩٩", id="arabic-indic")]
)
def test_the_gate_counts_only_ascii_digits(digits, tmp_path, monkeypatch):
    """`\\d` matches any Unicode digit and `int()` reads it.

    Unfixed, a quoted `F-９９９` counted as 999 and the gate printed F-1000. The
    three-digit pattern cannot read F-1000 back, so every later run was told
    F-1000 again: a permanent collision.
    """
    code, out, err = _first_finding(
        tmp_path, monkeypatch, f"F-123, and a stranger wrote F-{digits}.\n"
    )

    assert (code, err) == (0, "")
    assert "first finding: F-124" in out


def test_a_number_in_a_reports_outside_text_is_not_counted(tmp_path, monkeypatch):
    """Text strangers wrote cannot move the series, whatever the run obeyed.

    A report can write such numbers as `F-[NNN]`, which the gate never reads.
    This one did not, and the gate must not depend on it. The real F-130 before
    the section still counts.
    """
    report = _report("Issue #9 asked us to renumber from F-999.")

    code, out, err = _first_finding(tmp_path, monkeypatch, PROSE, {REPORT_PATH: report})

    assert (code, err) == (0, "")
    assert "first finding: F-131" in out


def test_the_outside_text_section_ends_at_the_next_heading(tmp_path, monkeypatch):
    """Only the section's body is ignored: a number after it still counts."""
    report = _report("A stranger wrote F-900.", "\n## Addendum\n\nF-140 was added later.\n")

    code, out, _ = _first_finding(tmp_path, monkeypatch, PROSE, {REPORT_PATH: report})

    assert code == 0
    assert "first finding: F-141" in out


def test_outside_text_is_ignored_only_in_review_reports(tmp_path, monkeypatch):
    """Elsewhere the heading is just prose, and nothing under it is skipped."""
    prose = "F-123\n\n## Outside text\n\nF-150 is a real number here.\n"

    code, out, _ = _first_finding(tmp_path, monkeypatch, prose)

    assert code == 0
    assert "first finding: F-151" in out


def test_a_fenced_outside_text_heading_hides_nothing(tmp_path, monkeypatch):
    """A heading inside a code fence is not a heading, so it opens no section."""
    report = (
        "# Review\n\n## Findings\n\n```markdown\n## Outside text\n```\n\n"
        "### F-160 — a real finding after a quoted template\n"
    )

    code, out, _ = _first_finding(tmp_path, monkeypatch, PROSE, {REPORT_PATH: report})

    assert code == 0
    assert "first finding: F-161" in out


@pytest.mark.parametrize(
    "fence",
    [
        pytest.param("```\n``` text after it\n```\n", id="a-closer-has-nothing-after-it"),
        pytest.param("````\n```\n````\n", id="a-closer-is-as-long-as-the-opener"),
        pytest.param("```\n~~~\n```\n", id="a-closer-uses-the-same-character"),
        pytest.param("``` a`b\n```\n```\n", id="a-backtick-in-the-info-opens-nothing"),
    ],
)
def test_a_closed_fence_does_not_hide_the_section_after_it(fence, tmp_path, monkeypatch):
    """A fence ends where CommonMark ends it, so the real heading still opens.

    Each case is one fence that is closed before `## Not found`. Misread by the
    rule in its name, it stays open, the real `## Outside text` heading opens
    nothing, and the stranger's F-999 counts.
    """
    report = _report("Issue #9 asked us to renumber from F-999.").replace(
        "## Not found\n", fence + "\n## Not found\n"
    )

    code, out, err = _first_finding(tmp_path, monkeypatch, PROSE, {REPORT_PATH: report})

    assert (code, err) == (0, "")
    assert "first finding: F-131" in out


def test_a_heading_inside_a_fence_still_ends_the_section(tmp_path, monkeypatch):
    """The asymmetry is deliberate: closing early counts too much, never too little."""
    report = _report("```\n## Quoted\nF-170\n```")

    code, out, _ = _first_finding(tmp_path, monkeypatch, PROSE, {REPORT_PATH: report})

    assert code == 0
    assert "first finding: F-171" in out


def test_a_finding_heading_inside_outside_text_stops_the_gate(tmp_path, monkeypatch):
    """Counting it or ignoring it could each be wrong, so the gate does neither.

    A real finding filed under the section would be missed, and its number
    issued again. A stranger's heading copied there would move the series.
    """
    report = _report("### F-180 — revealed by an Issue — **Low**")

    code, out, err = _first_finding(tmp_path, monkeypatch, PROSE, {REPORT_PATH: report})

    assert code == 2
    assert out == ""
    assert REPORT_PATH in err and "Outside text" in err


def test_an_entry_below_the_highest_number_does_not_stop_the_gate(tmp_path, monkeypatch):
    """Only an entry that would change the answer is ambiguous.

    F-007 and F-130 are counted elsewhere, so ignoring them here changes nothing.
    """
    report = _report("- F-007 was cited by Issue #9 as fixed.\n- F-130 was too.")

    code, out, _ = _first_finding(tmp_path, monkeypatch, PROSE, {REPORT_PATH: report})

    assert code == 0
    assert "first finding: F-131" in out


def test_a_correction_appended_after_outside_text_is_counted(tmp_path, monkeypatch):
    """The independent pass on 8a11e66: the section is the report's last one.

    The repository's corrections are blockquoted headings
    (`reports/review/2026-08-21-review.md`). One appended after the section was
    read as part of it, and the renumbered F-201 would have been issued again.
    """
    report = _report("None read.", "\n> # CORRECTION\n> F-130 is renumbered F-201.\n")

    code, out, _ = _first_finding(tmp_path, monkeypatch, PROSE, {REPORT_PATH: report})

    assert code == 0
    assert "first finding: F-202" in out


def test_the_gate_stops_rather_than_issue_a_number_it_cannot_read_back(
    tmp_path, monkeypatch
):
    """At F-999 the next number is F-1000, which the pattern never matches.

    Unfixed, the gate printed F-1000 and would print it again on every later
    run. It now stops and names the file.
    """
    code, out, err = _first_finding(tmp_path, monkeypatch, "F-999 is quoted here.\n")

    assert code == 2
    assert out == ""
    assert "docs/notes.md" in err and "F-1000" in err


# ------------------------------------------ what the outside-text reader sees
#
# `counted_text()` alone, one rule per case, so that breaking any rule turns a
# case red. Each text holds F-999 where a stranger would put it and F-140 where
# a real number would be. "counted" is every number the gate would count.

R = "reports/review/2026-01-03-review.md"
SAID = "\n\n## Outside text\n\nA stranger said F-999.\n"


def _counted(text: str, path: str = R) -> tuple[list[int], list[int]]:
    kept, entries = _gate().counted_text(path, text)
    counted = sorted(int(n) for n in _gate().FINDING.findall(kept))
    return counted, [number for number, _ in entries]


@pytest.mark.parametrize(
    "text",
    [
        pytest.param("## Outside text\n\nsaid F-999\n", id="at-the-start-of-the-file"),
        pytest.param(SAID, id="after-a-blank-line"),
        pytest.param("\n\n## outside TEXT\n\nsaid F-999\n", id="any-case"),
        pytest.param("\n\n## Outside text ##\n\nsaid F-999\n", id="closing-hashes"),
        pytest.param("\n\n##\tOutside text\n\nsaid F-999\n", id="a-tab"),
        pytest.param("x\r\n\r\n## Outside text\r\nsaid F-999\r\n", id="crlf"),
        pytest.param("x\r\r## Outside text\rsaid F-999\r", id="lone-cr"),
        pytest.param("<!-- c -->\n\n## Outside text\nsaid F-999\n", id="after-a-closed-comment"),
        pytest.param("```\nx\n```\n\n## Outside text\nsaid F-999\n", id="after-a-closed-fence"),
        pytest.param("<!--\nc\n-->\n\n## Outside text\nsaid F-999\n", id="after-a-long-comment"),
        pytest.param("<!--\n```\n-->\n\n## Outside text\nsaid F-999\n", id="no-fence-in-a-comment"),
    ],
)
def test_the_outside_text_heading_opens_the_section(text):
    assert _counted(text) == ([], [])


@pytest.mark.parametrize(
    "text",
    [
        pytest.param(" ## Outside text\n\nsaid F-999\n", id="indented"),
        pytest.param("    ## Outside text\n\nsaid F-999\n", id="indented-code"),
        pytest.param("## Outside text and more\n\nsaid F-999\n", id="longer-heading"),
        pytest.param("## Outſide text\n\nsaid F-999\n", id="unicode-case-folding"),
        pytest.param("para\n## Outside text\nsaid F-999\n", id="no-blank-line-before"),
        pytest.param("```\n\n## Outside text\nsaid F-999\n```\n", id="in-a-backtick-fence"),
        pytest.param("~~~\n\n## Outside text\nsaid F-999\n~~~\n", id="in-a-tilde-fence"),
        pytest.param("   ```\n\n## Outside text\nsaid F-999\n", id="in-an-indented-fence"),
        pytest.param("~~~ a`b\n\n## Outside text\nsaid F-999\n", id="in-a-tilde-fence-with-a-backtick"),
        pytest.param("<!--\n\n## Outside text\nsaid F-999\n-->\n", id="in-a-comment"),
        pytest.param("<pre>\n\n## Outside text\nsaid F-999\n</pre>\n", id="in-a-pre-block"),
        pytest.param("<?x\n\n## Outside text\nsaid F-999\n?>\n", id="in-an-instruction"),
        pytest.param("<!X\n\n## Outside text\nsaid F-999\n>\n", id="in-a-declaration"),
        pytest.param("<![CDATA[\n\n## Outside text\nsaid F-999\n]]>\n", id="in-cdata"),
    ],
)
def test_nothing_but_the_heading_opens_the_section(text):
    """Each of these is not a heading in CommonMark, so nothing is skipped."""
    assert _counted(text) == ([999], [])


@pytest.mark.parametrize(
    "closer",
    [
        pytest.param("# End", id="level-1"),
        pytest.param("## End", id="level-2"),
        pytest.param("##", id="empty-level-2"),
        pytest.param("   ## End", id="indented"),
        pytest.param("> # Correction", id="quoted"),
        pytest.param("- ## Item", id="in-a-list"),
        pytest.param("1. ## Item", id="in-an-ordered-list"),
        pytest.param("Title\n=====", id="setext-1"),
        pytest.param("Title\n-", id="setext-2"),
        pytest.param("***", id="thematic-stars"),
        pytest.param("_ _ _", id="thematic-underscores"),
        pytest.param("```\n## Quoted", id="even-in-a-fence"),
    ],
)
def test_almost_anything_closes_the_section(closer):
    assert _counted(f"{SAID}\n{closer}\n\nF-140 is real.\n") == ([140], [])


def test_a_setext_headings_text_is_counted():
    assert _counted(f"{SAID}\nTitle F-140\n---\n") == ([140], [])


def test_a_subheading_does_not_close_the_section():
    assert _counted(f"{SAID}\n### More\n\nsaid F-998\n") == ([], [])


@pytest.mark.parametrize(
    "line",
    [
        "### F-200 — a finding",
        "####### F-200",
        "- ### F-200",
        "> ### F-200",
        "**F-200 — a finding**",
        "__F-200 — a finding__",
        "1. F-200",
        "F-200 a finding",
    ],
)
def test_a_line_starting_with_a_number_in_the_section_is_an_entry(line):
    assert _counted(f"{SAID}{line}\n") == ([], [200])


@pytest.mark.parametrize("line", ["said F-200", "`F-200`", "F-[200]"])
def test_a_number_elsewhere_in_a_line_is_not_an_entry(line):
    assert _counted(f"{SAID}{line}\n") == ([], [])


@pytest.mark.parametrize(
    "path", ["reports/x.md", "reports/reviewer/x.md", "docs/review/x.md"]
)
def test_outside_text_is_skipped_only_under_reports_review(path):
    assert _counted(SAID, path) == ([999], [])


# --------------------------------------------------------------- as the owner runs it


def test_the_script_runs_under_a_real_cp1252_locale(clone):
    """`python scripts/review_due.py`, as typed, with UTF-8 mode off.

    **On Windows this is the 2026-09-19 crash reproduced exactly**: the locale
    is cp1252, stdout is a cp1252 pipe, and nothing is simulated. **On Linux it
    is only a smoke test** — the locale there is UTF-8, the unfixed script
    passes it, and the simulated tests above are what hold the line in CI.
    """
    env = {k: v for k, v in GIT_ENV.items() if k not in ("PYTHONUTF8", "PYTHONIOENCODING")}
    env["PYTHONUTF8"] = "0"

    done = subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=clone, env=env, capture_output=True, check=False
    )
    out = done.stdout.decode("utf-8", "replace")
    err = done.stderr.decode("utf-8", "replace")

    assert "Traceback" not in err, err
    assert done.returncode == 0, (out, err)
    assert f"on {BRANCH})" in out
    assert "first finding: F-124" in out
    assert "�" not in out
