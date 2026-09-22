"""Is an Belay review due, and what number does its first finding take?

    python scripts/review_due.py

Prints a verdict and exits 0 when a review should run, 1 when it should not.
The scheduled task's cadence gate calls this rather than reimplementing it,
because the gate has been wrong once and prose in a task config is not
something any test in this repository can reach.

**Both questions are answered across every remote ref, not the working tree.**
That distinction is the whole reason this file exists. On 2026-08-21 the gate
listed `reports/review/` on the default branch, saw a twenty-day-old report and
authorised a run — while a seven-day-old review sat unmerged on
`review/2026-08-14`. The run went ahead, could not see it, and reused seven
finding numbers that were already claimed and already ruled on. Four of its nine
findings were rediscovery.

**Finding numbers are read from all prose, not from report headings.** A report's
headings are what one pass called its findings; they are not the durable series.
`reports/review/2026-08-21-review.md` heads its findings F-007..F-015 while its
own correction block renumbers them F-014..F-018 — so scanning headings returns
015 and would collide, and so would scanning `docs/HANDOFF.md`, which carries
only what has been registered so far.

**When git's output cannot be obtained or read, the gate stops: exit 2, a reason
on stderr, nothing on stdout.** It does not skip the file and answer anyway. A
skipped file is a lower number, and a lower number is the collision above.
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import date, datetime, timezone

#: A review is due when the newest report is at least this old. The routine
#: fires weekly and is meant to run fortnightly, so the threshold sits below
#: fourteen days to absorb jitter without letting two runs land in one period.
MINIMUM_AGE_DAYS = 12

REPORT = re.compile(r"(\d{4}-\d{2}-\d{2})-review\.md")
FINDING = re.compile(r"\bF-(\d{3})\b")


class GateCannotAnswer(RuntimeError):
    """Git's output could not be obtained or read, so no number is safe to print."""


def git(*args: str, may_fail: bool = False) -> str:
    """Return git's stdout decoded as UTF-8, or raise. Never a guess.

    **Bytes are captured and decoded here, not by `subprocess`.** With
    `text=True` the locale picks the codec — cp1252 on Windows — and there the
    decode runs in a reader thread, so an undecodable byte does not raise:
    `stdout` silently comes back `None`. That was the 2026-09-19 crash, and
    `encoding="utf-8"` alone keeps the `None` for any file that is not UTF-8.

    **Strict, and a NUL is refused too.** A lenient decode turns UTF-16 (what
    PowerShell's `>` writes) into `F`, NUL, `-`…, matching nothing; without a
    byte-order mark that is even *valid* UTF-8. The gate would print a number
    already taken, and a wrong number is worse than none — so it stops instead.

    **A failed command raises for the same reason**: "" is what an empty file
    looks like. `may_fail` is for `rev-parse` alone, whose every failure is
    reported as "not a git repository" — a stop, whatever the real cause.
    """
    command = "git " + " ".join(args)
    done = subprocess.run(["git", *args], capture_output=True, check=False)
    if done.returncode != 0:
        if may_fail:
            return ""
        detail = done.stderr.decode("utf-8", "replace").strip()
        raise GateCannotAnswer(f"`{command}` exited {done.returncode}: {detail}")
    try:
        text = done.stdout.decode("utf-8")
    except UnicodeDecodeError as error:
        problem = f"bytes that are not UTF-8 ({error})"
    else:
        problem = "a NUL byte, so UTF-16 or not text at all" if "\0" in text else ""
    if problem:
        raise GateCannotAnswer(f"`{command}` printed {problem}. Re-save it as UTF-8.")
    return text


def remote_refs() -> list[str]:
    refs = git("for-each-ref", "--format=%(refname)", "refs/remotes/origin").split()
    # HEAD is a symbolic alias for another ref already in the list; including it
    # would double every file it names.
    return [ref for ref in refs if not ref.endswith("/HEAD")]


def branch_of(ref: str) -> str:
    """Return the branch name for a remote ref.

    `refs/remotes/origin/review/2026-08-21` is the branch `review/2026-08-21`,
    not `2026-08-21` — the name contains slashes of its own, so only the fixed
    prefix may be removed.
    """
    prefix = "refs/remotes/origin/"
    return ref[len(prefix):] if ref.startswith(prefix) else ref


def newest_report() -> tuple[date, str, str] | None:
    """Return (date, filename, branch) for the newest review report on any ref.

    A report that has been merged exists on several refs at once. `main` is named
    in preference to the branch it came from, because "still only on a branch" is
    a materially different thing for a reader to be told.
    """
    found: dict[tuple[date, str], set[str]] = {}
    for ref in remote_refs():
        for path in git("ls-tree", "-r", "--name-only", ref, "reports/review/").split():
            if match := REPORT.search(path):
                key = (date.fromisoformat(match.group(1)), path.rsplit("/", 1)[-1])
                found.setdefault(key, set()).add(branch_of(ref))
    if not found:
        return None

    (when, name), branches = max(found.items())
    where = "main" if "main" in branches else sorted(branches)[0]
    return when, name, where


def highest_finding() -> int:
    """Return the highest F-NNN mentioned in any tracked prose, on any ref.

    Zero when none exists. Read from `reports/` and `docs/` together rather than
    from either alone — see the module docstring for why each is insufficient.
    """
    highest = 0
    for ref in remote_refs():
        listing = git("ls-tree", "-r", "--name-only", ref, "reports/", "docs/")
        for path in listing.split():
            if not path.endswith(".md"):
                continue
            for number in FINDING.findall(git("show", f"{ref}:{path}")):
                highest = max(highest, int(number))
    return highest


def main() -> int:
    # The verdict carries an em dash and whatever a branch happens to be called.
    # Left to the machine, a piped stdout on Windows is cp1252: the dash arrives
    # as a byte no UTF-8 reader can decode, and a name outside cp1252 raises.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")

    try:
        return verdict()
    except GateCannotAnswer as error:
        # Neither DUE nor SKIP, so neither 0 nor 1 — and nothing on stdout, where
        # a verdict would be. Every number is computed before any line is
        # printed, so no `first finding:` can have escaped ahead of this.
        print(f"the gate cannot answer: {error}", file=sys.stderr)
        return 2


def verdict() -> int:
    if not git("rev-parse", "--git-dir", may_fail=True).strip():
        print("not a git repository; cannot answer across refs")
        return 1

    # Refs are only as current as the last fetch, and a stale ref is exactly the
    # blindness this script exists to remove.
    subprocess.run(["git", "fetch", "--quiet", "--all"], check=False)

    newest = newest_report()
    today = datetime.now(timezone.utc).date()
    next_finding = highest_finding() + 1

    if newest is None:
        print("DUE — no review report on any ref.")
        print(f"  first finding: F-{next_finding:03d}")
        return 0

    when, name, branch = newest
    age = (today - when).days

    if age < MINIMUM_AGE_DAYS:
        due = when.toordinal() + MINIMUM_AGE_DAYS
        print(
            f"SKIP — last review was {age} days ago "
            f"({name}, on {branch}). Next due {date.fromordinal(due).isoformat()}."
        )
        return 1

    print(f"DUE — last review was {age} days ago ({name}, on {branch}).")
    print(f"  first finding: F-{next_finding:03d}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
