"""Belay status dashboard — generated from the repository, never hand-written.

    python scripts/status.py

Writes an HTML page and prints a short summary to the terminal.

Everything here is re-derived from the repository on every run. Nothing is typed
in by hand and left to go stale, because a status page that has drifted from
reality is worse than no status page at all: it reads as verified when it is not.
That is the same principle the Belay constitution applies to evidence, turned on
the project's own reporting.

Two things are deliberately hand-written, because they are judgements rather than
measurements: which module is expected to satisfy which promotion criterion, and
what counts as a real implementation versus a placeholder. Both are stated openly
below so a reader can disagree with them.

This script reports what is NOT covered as loudly as what passes. A green test
count next to an untested persistence layer is exactly the kind of reassuring
half-truth it exists to prevent.
"""

from __future__ import annotations

import contextlib
import html
import importlib
import io
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "reports" / "generated" / "status.html"

# A file this short cannot contain a working component. Used to tell a real
# implementation apart from one of the four-line placeholders in
# framework/services/, which exist as files but do nothing.
PLACEHOLDER_LINES = 20

# The seven things constitution/Promotion_Pipeline.md says promotion must
# consider. Each names evidence that some component has to be able to compute,
# which makes this list the engineering backlog. `expected` is where that
# component is expected to live. The dashboard reports whether it exists, not
# whether it is any good — no script can judge that.
PROMOTION_CRITERIA = [
    ("Statistical performance", "framework/metrics/statistics.py"),
    ("Risk-adjusted returns", "framework/metrics/risk_adjusted.py"),
    ("Drawdown behavior", "framework/metrics/drawdown.py"),
    ("Regime robustness", "framework/services/regime.py"),
    ("Execution quality", "framework/services/execution.py"),
    ("Liquidity", "framework/services/liquidity.py"),
    ("Operational consistency", "framework/services/performance.py"),
]


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


# ---------------------------------------------------------------- measurements


def run_tests() -> dict:
    """Run the suite and report what actually happened.

    Runs pytest as a separate process rather than importing it, so a test that
    crashes cannot take this script down with it.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=300,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "passed": 0, "failed": 0, "note": f"could not run: {exc}"}

    output = result.stdout + result.stderr

    def count(pattern: str) -> int:
        return int(m.group(1)) if (m := re.search(pattern, output)) else 0

    return {
        "ok": result.returncode == 0,
        "passed": count(r"(\d+) passed"),
        "failed": count(r"(\d+) failed") + count(r"(\d+) error"),
        # Each xfail is an open finding held as an executable check rather than
        # as prose. See tests/test_governance_conformance.py.
        "watched": count(r"(\d+) xfailed"),
        "note": "" if result.returncode == 0 else "suite is not green",
    }


def module_health() -> list[tuple[str, str]]:
    """Import every module under framework/ and record which ones fail.

    A module that cannot be imported is invisible to the test suite — no test can
    exercise what will not load — so these never show up as failures. Output is
    suppressed because importing a module runs its top-level code.
    """
    broken: list[tuple[str, str]] = []
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))

    for path in sorted((ROOT / "framework").rglob("*.py")):
        if path.name == "__init__.py":
            continue
        name = path.relative_to(ROOT).with_suffix("").as_posix().replace("/", ".")
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                with contextlib.redirect_stderr(io.StringIO()):
                    importlib.import_module(name)
        except BaseException as exc:  # noqa: BLE001 - reporting, not handling
            broken.append((name, f"{type(exc).__name__}: {exc}"))

    return broken


def untested_modules() -> list[str]:
    """Framework modules that no test file so much as mentions.

    A crude measure — a mention is not a test — but it reliably finds the code
    nobody has ever exercised, which is the thing a passing suite hides.
    """
    referenced: set[str] = set()
    for path in (ROOT / "tests").rglob("*.py"):
        for match in re.finditer(r"framework\.([\w.]+)", read(path)):
            referenced.add(match.group(1))

    untested = []
    for path in sorted((ROOT / "framework").rglob("*.py")):
        if path.name == "__init__.py":
            continue
        dotted = path.relative_to(ROOT / "framework").with_suffix("").as_posix()
        dotted = dotted.replace("/", ".")
        if not any(r == dotted or r.startswith(dotted + ".") for r in referenced):
            untested.append(f"framework/{path.relative_to(ROOT / 'framework').as_posix()}")

    return untested


def implementation_state(relative: str) -> str:
    """Classify a path as built, stub, or missing."""
    path = ROOT / relative
    if not path.exists():
        return "missing"
    lines = [ln for ln in read(path).splitlines() if ln.strip()]
    return "built" if len(lines) >= PLACEHOLDER_LINES else "stub"


def repo_stats() -> dict:
    def count_lines(folder: str) -> int:
        return sum(len(read(p).splitlines()) for p in (ROOT / folder).rglob("*.py"))

    return {
        "python_files": sum(1 for _ in ROOT.rglob("*.py") if ".git" not in _.parts),
        "framework_lines": count_lines("framework"),
        "test_lines": count_lines("tests"),
        "markdown": sum(1 for _ in ROOT.rglob("*.md") if ".git" not in _.parts),
    }


# ------------------------------------------------------------- document parsing


def roadmap_stages() -> list[tuple[str, str]]:
    """Read the stage list out of docs/ROADMAP.md.

    The roadmap is hand-maintained by design — it is a plan, not a measurement —
    so editing it is what moves this section.
    """
    stages = []
    for line in read(ROOT / "docs" / "ROADMAP.md").splitlines():
        if match := re.match(r"^## (Stage \d+ — .+?)(?:\s*\((.+)\))?$", line):
            stages.append((match.group(1), match.group(2) or "not started"))
    return stages


#: One row of docs/FINDINGS.md's "Open" table. A priority cell that is not
#: P1-P3 parses as "?", so a malformed grade shows rather than vanishing.
FINDING_ROW = re.compile(r"^\| (.+?) \| (\S*) \| (?:yes|no) \| .+? \|$", re.M)


def open_findings() -> list[tuple[str, str]]:
    """Pull the open findings and their priorities out of docs/FINDINGS.md.

    Until 2026-09-25 the register was prose sections in docs/HANDOFF.md, now a
    frozen archive (docs/OwnerDecisions.md Part 29). It is one table row per
    finding, so the priority is a cell rather than a phrase to hunt for, and a
    title is the finding's name, word for word as the archive heads it.
    """
    text = read(ROOT / "docs" / "FINDINGS.md")
    section = re.search(r"^## Open\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not section:
        return []

    findings = []
    for title, cell in FINDING_ROW.findall(section.group(1)):
        findings.append((title.strip(), cell if re.fullmatch(r"P[1-3]", cell) else "?"))

    # Unparsed findings sort last, not first. While every grade was "?" this
    # sort was inert and the table simply followed document order; now that it
    # bites, an untriaged finding at the top would read as the most urgent one.
    # Ties break by title so the order does not depend on document position.
    return sorted(findings, key=lambda f: (f[1] == "?", f[1], f[0].lower()))


def decisions() -> list[tuple[str, str]]:
    """List the architectural decisions and their status from docs/DECISIONS.md."""
    text = read(ROOT / "docs" / "DECISIONS.md")
    found = []
    for match in re.finditer(r"^## (ADR-\d+:.*?)$(.*?)(?=^## ADR-|\Z)", text, re.S | re.M):
        status = m.group(1).strip() if (m := re.search(r"Status:\s*\n(.+)", match.group(2))) else "?"
        found.append((match.group(1).strip(), status))
    return found


# ------------------------------------------------------------------- rendering

CSS = """
:root { color-scheme: light dark;
  --bg:#faf9f7; --card:#fff; --text:#1a1a19; --muted:#5f5e5a; --line:#e2e0da;
  --ok:#3b6d11; --okbg:#eaf3de; --warn:#854f0b; --warnbg:#faeeda;
  --bad:#993c1d; --badbg:#faece7; --none:#5f5e5a; --nonebg:#f1efe8; }
@media (prefers-color-scheme: dark) { :root {
  --bg:#191917; --card:#222220; --text:#f0efe9; --muted:#b4b2a9; --line:#3a3a37;
  --ok:#c0dd97; --okbg:#27500a; --warn:#fac775; --warnbg:#854f0b;
  --bad:#f5c4b3; --badbg:#712b13; --none:#d3d1c7; --nonebg:#444441; } }
* { box-sizing:border-box; }
body { margin:0; padding:2.5rem 1.5rem; background:var(--bg); color:var(--text);
  font:16px/1.65 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif; }
main { max-width:900px; margin:0 auto; }
h1 { font-size:22px; font-weight:500; margin:0 0 .25rem; }
h2 { font-size:18px; font-weight:500; margin:2.5rem 0 .75rem; }
.sub { color:var(--muted); font-size:14px; margin:0 0 2rem; }
.cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:.75rem; }
.card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:1rem; }
.num { font-size:26px; font-weight:500; }
.lbl { color:var(--muted); font-size:13px; margin-top:.15rem; }
table { width:100%; border-collapse:collapse; font-size:14px; }
th { text-align:left; font-weight:500; color:var(--muted); padding:.5rem .6rem;
  border-bottom:1px solid var(--line); font-size:13px; }
td { padding:.55rem .6rem; border-bottom:1px solid var(--line); vertical-align:top; }
.wrap { background:var(--card); border:1px solid var(--line); border-radius:12px;
  padding:.4rem .6rem; overflow-x:auto; }
.pill { display:inline-block; padding:.1rem .5rem; border-radius:999px; font-size:12px; }
.p-ok{background:var(--okbg);color:var(--ok);} .p-warn{background:var(--warnbg);color:var(--warn);}
.p-bad{background:var(--badbg);color:var(--bad);} .p-none{background:var(--nonebg);color:var(--none);}
code { font-family:ui-monospace,Menlo,Consolas,monospace; font-size:13px; color:var(--muted); }
.note { background:var(--warnbg); color:var(--warn); border-radius:12px;
  padding:.85rem 1rem; font-size:14px; margin-top:.75rem; }
.bar { display:flex; gap:.4rem; margin:.75rem 0 0; }
.seg { flex:1; height:8px; border-radius:4px; background:var(--nonebg); }
.seg.on { background:var(--ok); }
"""

PILLS = {
    "built": "p-ok", "complete": "p-ok", "in progress": "p-warn",
    "stub": "p-warn", "missing": "p-bad", "not started": "p-none",
    # Finding priorities. Without these every grade fell through to the default
    # and the whole column rendered the same grey, which is no more use than the
    # "?" it replaced.
    "p1": "p-bad", "p2": "p-warn", "p3": "p-none",
}


def pill(label: str) -> str:
    return f'<span class="pill {PILLS.get(label.lower(), "p-none")}">{html.escape(label)}</span>'


def table(headers: list[str], rows: list[list[str]]) -> str:
    if not rows:
        return '<p class="sub">Nothing to report.</p>'
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def render(data: dict) -> str:
    tests = data["tests"]
    criteria = data["criteria"]
    stages = data["stages"]

    covered = sum(1 for _, _, s in criteria if s == "built")
    done = sum(1 for _, s in stages if s.lower() == "complete")
    test_pill = "p-ok" if tests["ok"] else "p-bad"
    test_txt = f"{tests['passed']} passing" if tests["ok"] else f"{tests['failed']} failing"

    cards = f"""
    <div class="card"><div class="num"><span class="pill {test_pill}">{html.escape(test_txt)}</span></div>
      <div class="lbl">test suite</div></div>
    <div class="card"><div class="num">{done} / {len(stages)}</div>
      <div class="lbl">roadmap stages complete</div></div>
    <div class="card"><div class="num">{covered} / {len(criteria)}</div>
      <div class="lbl">promotion criteria computable</div></div>
    <div class="card"><div class="num">{len(data["findings"])}</div>
      <div class="lbl">open findings</div></div>
    <div class="card"><div class="num">{tests["watched"]}</div>
      <div class="lbl">gaps watched by a test</div></div>"""

    segments = "".join(
        f'<div class="seg{" on" if s.lower() == "complete" else ""}"></div>' for _, s in stages
    )

    warning = ""
    if tests["ok"] and data["untested"]:
        warning = (
            f'<div class="note">The suite is green, but {len(data["untested"])} module(s) '
            "under framework/ are not referenced by any test. A passing suite is not "
            "coverage — see untested code below.</div>"
        )

    stats = data["stats"]
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Belay status</title><style>{CSS}</style></head><body><main>
<h1>Belay status</h1>
<p class="sub">Generated {data["generated"]} from the repository. Re-run
<code>python scripts/status.py</code> to refresh.</p>

<div class="cards">{cards}</div>
<div class="bar">{segments}</div>
{warning}

<h2>Roadmap stages</h2>
{table(["Stage", "Status"], [[html.escape(n), pill(s)] for n, s in stages])}

<h2>Promotion criteria</h2>
<p class="sub">The seven things constitution/Promotion_Pipeline.md says promotion
must consider. A criterion nothing computes is not a gate.</p>
{table(["Criterion", "Expected component", "State"],
       [[html.escape(n), f"<code>{html.escape(p)}</code>", pill(s)] for n, p, s in criteria])}

<h2>Untested code</h2>
<p class="sub">Framework modules no test file references. These cannot fail the
suite, which is what makes them worth listing.</p>
{table(["Module"], [[f"<code>{html.escape(m)}</code>"] for m in data["untested"]])}

<h2>Modules that will not import</h2>
<p class="sub">Broken on load, so no test can reach them.</p>
{table(["Module", "Error"],
       [[f"<code>{html.escape(n)}</code>", html.escape(e)] for n, e in data["broken"]])}

<h2>Open findings</h2>
{table(["Finding", "Priority"],
       [[html.escape(t), pill(p)] for t, p in data["findings"]])}

<h2>Architectural decisions</h2>
{table(["Decision", "Status"],
       [[html.escape(t), html.escape(s)] for t, s in data["decisions"]])}

<h2>Composition</h2>
{table(["Measure", "Count"],
       [["Python files", str(stats["python_files"])],
        ["Lines under framework/", str(stats["framework_lines"])],
        ["Lines under tests/", str(stats["test_lines"])],
        ["Markdown documents", str(stats["markdown"])]])}
</main></body></html>"""


def main() -> int:
    criteria = [(name, path, implementation_state(path)) for name, path in PROMOTION_CRITERIA]
    data = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "tests": run_tests(),
        "stages": roadmap_stages(),
        "criteria": criteria,
        "untested": untested_modules(),
        "broken": module_health(),
        "findings": open_findings(),
        "decisions": decisions(),
        "stats": repo_stats(),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(data), encoding="utf-8")

    tests = data["tests"]
    done = sum(1 for _, s in data["stages"] if s.lower() == "complete")
    covered = sum(1 for _, _, s in criteria if s == "built")

    # ASCII only in terminal output: the default Windows console codepage cannot
    # encode an em dash and raises UnicodeEncodeError rather than degrading.
    print(f"Belay status - {data['generated']}")
    print(f"  tests               {tests['passed']} passing, {tests['failed']} failing")
    print(f"  gaps watched        {tests['watched']} (xfail conformance checks)")
    print(f"  roadmap stages      {done} of {len(data['stages'])} complete")
    print(f"  promotion criteria  {covered} of {len(criteria)} computable")
    print(f"  untested modules    {len(data['untested'])}")
    print(f"  will not import     {len(data['broken'])}")
    print(f"  open findings       {len(data['findings'])}")
    print(f"\n  {OUTPUT}")

    return 0 if tests["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
