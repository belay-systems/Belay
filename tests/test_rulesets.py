"""The tracked rulesets and the workflow they name must agree.

A ruleset requires status checks by name. If a job in
`.github/workflows/conformance.yml` is renamed and the ruleset is not, the
required check never reports, and nothing can merge into `main` — or, the other
way round, a job is added and never required. Neither shows up until somebody
is blocked, so it is held here.

No network. This reads two tracked files.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
RULESETS = sorted((REPO / ".github" / "rulesets").glob("*.json"))
WORKFLOW = REPO / ".github" / "workflows" / "conformance.yml"


def _job_names() -> set[str]:
    jobs = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))["jobs"]
    names: set[str] = set()
    for job in jobs.values():
        matrix = (job.get("strategy") or {}).get("matrix") or {}
        if not matrix:
            names.add(job["name"])
            continue
        (key, values), = matrix.items()
        names.update(job["name"].replace("${{ matrix." + key + " }}", str(v)) for v in values)
    return names


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rules(ruleset: dict) -> dict:
    return {rule["type"]: rule.get("parameters") or {} for rule in ruleset["rules"]}


def test_there_are_rulesets_to_check():
    assert [p.name for p in RULESETS] == [
        "carriers-review.json", "main-checks.json", "main-review.json"
    ]


def test_required_checks_are_exactly_the_workflow_jobs():
    required = {
        check["context"]
        for path in RULESETS
        for check in _rules(_load(path)).get("required_status_checks", {}).get("required_status_checks", [])
    }
    assert required == _job_names()


# Where each ruleset applies. `main` gets both. A carrier branch (one that other
# pull requests merge into, such as `adr/015-stage-is-carried`) gets the review
# requirement only: docs/OwnerDecisions.md Part 20a, "always second review".
# Working branches are not covered, because a review rule also blocks pushing
# to the branch it covers.
TARGETS = {
    "main-checks.json": ["~DEFAULT_BRANCH"],
    "main-review.json": ["~DEFAULT_BRANCH"],
    "carriers-review.json": ["refs/heads/adr/**"],
}


def test_every_ruleset_is_active_and_targets_what_it_should():
    for path in RULESETS:
        ruleset = _load(path)
        assert ruleset["enforcement"] == "active", path.name
        assert ruleset["target"] == "branch", path.name
        assert ruleset["conditions"] == {
            "ref_name": {"include": TARGETS[path.name], "exclude": []}
        }, path.name


def test_required_checks_must_come_from_github_actions():
    """15368 is the GitHub Actions app. Without it, any app able to post a
    status named `suite (py3.11)` satisfies the rule."""
    checks = _rules(_load(REPO / ".github" / "rulesets" / "main-checks.json"))[
        "required_status_checks"
    ]["required_status_checks"]
    assert {c.get("integration_id") for c in checks} == {15368}


def test_the_checks_ruleset_can_be_bypassed_by_nobody():
    """The one rule that binds both owners: red continuous integration, a
    force-push and a deletion never reach `main`, whoever asks."""
    ruleset = _load(REPO / ".github" / "rulesets" / "main-checks.json")
    assert ruleset["bypass_actors"] == []
    assert {"deletion", "non_fast_forward", "pull_request", "required_status_checks"} <= set(_rules(ruleset))


REVIEW_RULESETS = ("main-review.json", "carriers-review.json")


def test_the_review_rulesets_require_a_code_owner():
    for name in REVIEW_RULESETS:
        params = _rules(_load(REPO / ".github" / "rulesets" / name))["pull_request"]
        assert params["require_code_owner_review"] is True, name
        assert params["required_approving_review_count"] >= 1, name


def test_no_review_ruleset_can_be_bypassed():
    """docs/OwnerDecisions.md Part 20b. An organization Owner used to be able to
    merge into `main` with no review, and on 2026-09-22 a session did. The
    deadlock an empty list used to cause, every pull request the sole code
    owner wrote having no eligible reviewer, is closed in `.github/CODEOWNERS`
    instead (Part 20c), and `test_publication_guard.py` holds that side."""
    for name in REVIEW_RULESETS:
        assert _load(REPO / ".github" / "rulesets" / name)["bypass_actors"] == [], name


def test_the_review_rulesets_differ_only_in_name_and_target():
    """A carrier branch is reviewed exactly as `main` is. If one is tightened
    and the other is not, a change can land on the weaker one and be merged on
    from there."""
    main, carriers = (_load(REPO / ".github" / "rulesets" / n) for n in REVIEW_RULESETS)
    for ruleset in (main, carriers):
        ruleset.pop("name")
        ruleset.pop("conditions")
    assert main == carriers
