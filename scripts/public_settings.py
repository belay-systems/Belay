"""Check, or apply, the GitHub settings a public Belay depends on.

    python scripts/public_settings.py            read-only: PASS / FAIL per setting
    python scripts/public_settings.py --apply    set them, then run the check

Needs the GitHub CLI (`gh`), signed in as an owner of the organization. It never
changes the repository's visibility: that is the owner's own action, and
`--apply` refuses to run until the repository is already public, because GitHub
does not offer rulesets to a private repository on a free organization.

The rulesets themselves are `.github/rulesets/*.json`, so a change to what
`main` requires is a reviewed change to a tracked file. This script is operator
tooling. Nothing under `framework/` or `tests/` imports it, and no test runs it,
because it talks to the network.

Exit status: 0 when every check passes, 1 otherwise. UNKNOWN counts as not
passing — a setting that could not be read has not been verified.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RULESET_DIR = REPO_ROOT / ".github" / "rulesets"
DEFAULT_REPO = "belay-systems/Belay"

# `docs/OwnerDecisions.md` Part 13c: GitHub's default. Strangers' first pull
# request waits for a click before continuous integration runs it.
FORK_APPROVAL_POLICY = "first_time_contributors"

PASS, FAIL, UNKNOWN = "PASS", "FAIL", "UNKNOWN"


def _gh_path() -> str:
    found = shutil.which("gh")
    if found:
        return found
    fallback = Path("C:/Program Files/GitHub CLI/gh.exe")
    if fallback.exists():
        return str(fallback)
    sys.exit("The GitHub CLI (`gh`) was not found. Install it, run `gh auth login`, and retry.")


def api(path: str, method: str = "GET", body: dict | None = None) -> tuple[int, object]:
    """Returns (exit code, parsed JSON or raw text). Bytes are decoded here
    because a Windows console codepage turns undecodable output into None."""
    cmd = [_gh_path(), "api", "-X", method, path, "-H", "Accept: application/vnd.github+json"]
    data = None
    if body is not None:
        cmd += ["--input", "-"]
        data = json.dumps(body).encode("utf-8")
    done = subprocess.run(cmd, input=data, capture_output=True)
    text = (done.stdout or done.stderr or b"").decode("utf-8", errors="replace").strip()
    try:
        return done.returncode, json.loads(text) if text else {}
    except json.JSONDecodeError:
        return done.returncode, text


def wanted_rulesets() -> list[dict]:
    return [json.loads(p.read_text(encoding="utf-8")) for p in sorted(RULESET_DIR.glob("*.json"))]


def _shape(ruleset: dict) -> dict:
    """The parts of a ruleset that decide what it enforces, in a comparable form."""
    rules = {}
    for rule in ruleset.get("rules", []):
        params = dict(rule.get("parameters") or {})
        if "required_status_checks" in params:
            params["required_status_checks"] = sorted(
                c["context"] for c in params["required_status_checks"]
            )
        rules[rule["type"]] = {k: v for k, v in params.items() if k in _COMPARED}
    bypass = sorted(
        (a.get("actor_type"), a.get("bypass_mode")) for a in ruleset.get("bypass_actors") or []
    )
    return {"enforcement": ruleset.get("enforcement"), "rules": rules, "bypass": bypass}


_COMPARED = {
    "required_approving_review_count",
    "dismiss_stale_reviews_on_push",
    "require_code_owner_review",
    "required_status_checks",
}


# ---------------------------------------------------------------- the checks


def check_visibility(repo: str) -> tuple[str, str]:
    code, data = api(f"repos/{repo}")
    if code != 0 or not isinstance(data, dict):
        return UNKNOWN, f"could not read the repository: {data}"
    return (PASS if data.get("visibility") == "public" else FAIL), f"visibility is {data.get('visibility')}"


def check_rulesets(repo: str) -> list[tuple[str, str, str]]:
    code, listed = api(f"repos/{repo}/rulesets")
    if code != 0 or not isinstance(listed, list):
        return [("rulesets", UNKNOWN, f"could not list rulesets: {listed}")]
    by_name = {r["name"]: r["id"] for r in listed}
    rows = []
    for want in wanted_rulesets():
        label = f"ruleset '{want['name']}'"
        if want["name"] not in by_name:
            rows.append((label, FAIL, "missing"))
            continue
        code, live = api(f"repos/{repo}/rulesets/{by_name[want['name']]}")
        if code != 0 or not isinstance(live, dict):
            rows.append((label, UNKNOWN, f"could not read it: {live}"))
        elif _shape(live) != _shape(want):
            rows.append((label, FAIL, f"differs from the tracked file: live {_shape(live)}"))
        else:
            rows.append((label, PASS, "active and matches .github/rulesets/"))
    extra = sorted(set(by_name) - {w["name"] for w in wanted_rulesets()})
    if extra:
        rows.append(("no untracked rulesets", FAIL, f"found {extra}, which no tracked file describes"))
    return rows


def check_security(repo: str) -> list[tuple[str, str, str]]:
    code, data = api(f"repos/{repo}")
    if code != 0 or not isinstance(data, dict):
        return [("security settings", UNKNOWN, f"could not read the repository: {data}")]
    sa = data.get("security_and_analysis") or {}
    rows = []
    for key, label in (
        ("secret_scanning", "secret scanning"),
        ("secret_scanning_push_protection", "push protection"),
    ):
        status = (sa.get(key) or {}).get("status")
        rows.append((label, PASS if status == "enabled" else FAIL, f"status is {status}"))
    rows.append(("wiki is off (Part 14e)", PASS if data.get("has_wiki") is False else FAIL, f"has_wiki is {data.get('has_wiki')}"))
    rows.append(("Issues are on", PASS if data.get("has_issues") else FAIL, f"has_issues is {data.get('has_issues')}"))
    return rows


def check_vulnerability_reporting(repo: str) -> tuple[str, str]:
    code, data = api(f"repos/{repo}/private-vulnerability-reporting")
    if code != 0 or not isinstance(data, dict):
        return UNKNOWN, f"could not read it: {data}"
    return (PASS if data.get("enabled") else FAIL), f"enabled is {data.get('enabled')}"


def check_actions(repo: str) -> list[tuple[str, str, str]]:
    rows = []
    code, data = api(f"repos/{repo}/actions/permissions/workflow")
    if code != 0 or not isinstance(data, dict):
        rows.append(("workflow token is read-only", UNKNOWN, f"could not read it: {data}"))
    else:
        ok = data.get("default_workflow_permissions") == "read" and data.get("can_approve_pull_request_reviews") is False
        rows.append(("workflow token is read-only", PASS if ok else FAIL, json.dumps(data)))
    code, data = api(f"repos/{repo}/actions/permissions")
    if code != 0 or not isinstance(data, dict):
        rows.append(("only GitHub's own actions may run", UNKNOWN, f"could not read it: {data}"))
    else:
        rows.append(("only GitHub's own actions may run", PASS if data.get("allowed_actions") == "selected" else FAIL, f"allowed_actions is {data.get('allowed_actions')}"))
    code, data = api(f"repos/{repo}/actions/permissions/fork-pr-contributor-approval")
    if code != 0 or not isinstance(data, dict):
        rows.append(("fork pull requests wait for approval", UNKNOWN, "could not read it; check Settings, Actions, General by hand"))
    else:
        policy = data.get("approval_policy")
        ok = policy in {FORK_APPROVAL_POLICY, "all_external_contributors"}
        rows.append(("fork pull requests wait for approval", PASS if ok else FAIL, f"approval_policy is {policy}"))
    return rows


def run_checks(repo: str) -> list[tuple[str, str, str]]:
    rows = [("repository is public", *check_visibility(repo))]
    rows += check_rulesets(repo)
    rows += check_security(repo)
    rows.append(("private vulnerability reporting", *check_vulnerability_reporting(repo)))
    rows += check_actions(repo)
    return rows


# ----------------------------------------------------------------- the apply


def apply(repo: str) -> None:
    status, detail = check_visibility(repo)
    if status != PASS:
        sys.exit(f"Refusing to apply: {detail}. The owner makes the repository public first; this script never does.")

    code, listed = api(f"repos/{repo}/rulesets")
    existing = {r["name"]: r["id"] for r in listed} if code == 0 and isinstance(listed, list) else {}
    steps: list[tuple[str, str, str, dict | None]] = []
    for want in wanted_rulesets():
        if want["name"] in existing:
            steps.append((f"update ruleset '{want['name']}'", "PUT", f"repos/{repo}/rulesets/{existing[want['name']]}", want))
        else:
            steps.append((f"create ruleset '{want['name']}'", "POST", f"repos/{repo}/rulesets", want))
    steps += [
        ("secret scanning and push protection", "PATCH", f"repos/{repo}", {
            "security_and_analysis": {
                "secret_scanning": {"status": "enabled"},
                "secret_scanning_push_protection": {"status": "enabled"},
            }
        }),
        ("wiki off", "PATCH", f"repos/{repo}", {"has_wiki": False}),
        ("private vulnerability reporting", "PUT", f"repos/{repo}/private-vulnerability-reporting", None),
        ("dependency alerts", "PUT", f"repos/{repo}/vulnerability-alerts", None),
        ("workflow token read-only", "PUT", f"repos/{repo}/actions/permissions/workflow", {
            "default_workflow_permissions": "read", "can_approve_pull_request_reviews": False
        }),
        ("restrict which actions may run", "PUT", f"repos/{repo}/actions/permissions", {
            "enabled": True, "allowed_actions": "selected"
        }),
        ("allow only GitHub's own actions", "PUT", f"repos/{repo}/actions/permissions/selected-actions", {
            "github_owned_allowed": True, "verified_allowed": False, "patterns_allowed": []
        }),
        ("fork pull requests wait for approval", "PUT", f"repos/{repo}/actions/permissions/fork-pr-contributor-approval", {
            "approval_policy": FORK_APPROVAL_POLICY
        }),
    ]
    for label, method, path, body in steps:
        code, out = api(path, method, body)
        print(f"  {'ok    ' if code == 0 else 'FAILED'}  {label}" + ("" if code == 0 else f"  -> {out}"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apply", action="store_true", help="set the settings, then check them")
    parser.add_argument("--repo", default=DEFAULT_REPO)
    args = parser.parse_args()

    if args.apply:
        print(f"Applying to {args.repo}:")
        apply(args.repo)
        print()

    rows = run_checks(args.repo)
    width = max(len(label) for label, _, _ in rows)
    for label, status, detail in rows:
        print(f"  {status:<7}  {label:<{width}}  {detail}")
    failed = [r for r in rows if r[1] != PASS]
    print(f"\n{len(rows) - len(failed)} of {len(rows)} pass.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
