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
    assert len(RULESETS) == 2, [p.name for p in RULESETS]


def test_required_checks_are_exactly_the_workflow_jobs():
    required = {
        check["context"]
        for path in RULESETS
        for check in _rules(_load(path)).get("required_status_checks", {}).get("required_status_checks", [])
    }
    assert required == _job_names()


def test_every_ruleset_is_active_and_targets_the_default_branch():
    for path in RULESETS:
        ruleset = _load(path)
        assert ruleset["enforcement"] == "active", path.name
        assert ruleset["conditions"]["ref_name"]["include"] == ["~DEFAULT_BRANCH"], path.name


def test_the_checks_ruleset_can_be_bypassed_by_nobody():
    """The one rule that binds both owners: red continuous integration, a
    force-push and a deletion never reach `main`, whoever asks."""
    ruleset = _load(REPO / ".github" / "rulesets" / "main-checks.json")
    assert ruleset["bypass_actors"] == []
    assert {"deletion", "non_fast_forward", "pull_request", "required_status_checks"} <= set(_rules(ruleset))


def test_the_review_ruleset_requires_a_code_owner():
    params = _rules(_load(REPO / ".github" / "rulesets" / "main-review.json"))["pull_request"]
    assert params["require_code_owner_review"] is True
    assert params["required_approving_review_count"] >= 1
