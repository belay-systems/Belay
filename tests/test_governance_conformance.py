"""The code must match the documents that govern it.

Every gap found on 2026-07-26 was found by a person reading a document and then
reading the code. Nothing was watching, so the gaps accumulated invisibly for
months. This file is what watches.

Two kinds of test live here.

**Passing tests** assert a conformance that currently holds. If someone edits the
enum, the constitution wins and the suite goes red.

**xfail(strict=True) tests** assert a conformance that does not hold yet. Each cites
the `docs/HANDOFF.md` section that explains it, by title rather than by number: the
findings are renumbered every time one closes, and markers left pointing at the old
numbering was itself a recorded finding. A title is a stable anchor. While the gap is
open the test fails as expected and the suite stays green — but the gap lives in the
test suite rather than buried in prose. When someone closes it, the test passes
unexpectedly and `strict` turns the suite red to say so: remove the marker, the work
is done. If it is ever broken again, the suite goes red the normal way.

The backlog maintains itself. No future session has to rediscover any of this.
"""

from __future__ import annotations

import dataclasses
import re
from pathlib import Path

import pytest

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import (
    ArtifactLifecycle,
    ArtifactType,
    EvidenceLevel,
    StrategyLifecycle,
)
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.primitives import version_key
from framework.artifacts.validator import ArtifactValidator
from framework.identifiers import VALID_PREFIXES

REPO = Path(__file__).resolve().parents[1]


def doc(relative: str) -> str:
    """Return a governing document's text, lowercased for tolerant matching."""
    return (REPO / relative).read_text(encoding="utf-8").lower()


def artifact_fields() -> set[str]:
    return {f.name for f in dataclasses.fields(Artifact)}


def schema_required_fields() -> set[str]:
    """The required field names between `Required Fields` and `Optional Fields`.

    Parsed, not transcribed. The count was carried as fourteen in prose for
    months and had reached a test docstring before anyone counted the lines;
    a list copied into this file would go stale the same way.
    """
    text = (REPO / "Knowledge" / "Schema.md").read_text(encoding="utf-8")
    body = text.split("Required Fields", 1)[1].split("Optional Fields", 1)[0]
    return {line.strip() for line in body.splitlines() if line.strip().strip("-")}


def relationship_types_in_document() -> set[str]:
    """The type names between the `Relationship Types` heading and the rule.

    Parsed rather than copied. A list transcribed into this file would drift
    from `Knowledge/Relationships.md` exactly as silently as the code did —
    the drift is the thing being tested, so the document has to be the input.
    """
    text = (REPO / "Knowledge" / "Relationships.md").read_text(encoding="utf-8")
    body = text.split("Relationship Types", 1)[1].split("---", 1)[0]
    return {line.strip() for line in body.splitlines() if line.strip()}


def outcomes_under(relative: str, heading: str) -> set[str]:
    """The review outcomes a document lists beneath `heading`.

    Each of the three documents writes its outcomes one per line between the
    heading and the next rule. Lines ending in `.` are prose, not outcomes —
    `workflows/Monthly/StrategyPromotion.md` closes its list with "Every decision
    requires written justification." and that is a rule about the outcomes rather
    than one of them.
    """
    text = (REPO / relative).read_text(encoding="utf-8")
    body = text.split(heading, 1)[1].split("---", 1)[0]
    return {
        line.strip()
        for line in body.splitlines()
        if line.strip() and not line.strip().endswith(".")
    }


def doctrine_lifecycle_stages() -> list[str]:
    """The doctrine's eight stages, in order, upper-cased as it writes them.

    A **list**, not a set: this is a sequence, and the thing most worth catching
    is a reordering. `test_strategy_stages_all_appear_in_the_doctrine` above
    checks only that each name appears somewhere in the file, which a shuffled
    doctrine would still satisfy.

    Parsed from `## Lifecycle` up to the next rule, discarding the `↓` arrows.
    ADR-007 follow-up.
    """
    text = (REPO / "constitution" / "Paper_First_Capital_Doctrine.md").read_text(
        encoding="utf-8"
    )
    body = text.split("## Lifecycle", 1)[1].split("---", 1)[0]
    return [
        line.strip()
        for line in body.splitlines()
        if line.strip() and line.strip() != "↓"
    ]


def workflow_requirements() -> list[str]:
    """The five things `workflows/README.md` says every workflow defines.

    Parsed rather than transcribed. The list used to be written out inside the
    test, which is the drift that put a wrong field count into a docstring for
    months — a copy cannot notice its source changing.
    """
    text = (REPO / "workflows" / "README.md").read_text(encoding="utf-8")
    body = text.split("Every workflow defines:", 1)[1]

    names = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("- "):
            break
        names.append(stripped[2:].strip())
    return names


# `workflows/` holds two markdown files that are not workflows. Named rather than
# subtracted: the test used to count `rglob("*.md")` and take away 2, so adding any
# markdown file under `workflows/` silently changed what the figure meant.
NOT_A_WORKFLOW = {"README.md", "WorkflowEngine.md"}


def documented_workflows() -> list[tuple[str, str]]:
    """Every workflow document under `workflows/`, as (category, name).

    Thirteen at the time of writing. The category is carried because two
    documents share a name — `Events/StrategyPromotion.md` and
    `Monthly/StrategyPromotion.md` — and the pair is not the same workflow.
    """
    return sorted(
        (path.parent.name, path.stem)
        for path in (REPO / "workflows").rglob("*.md")
        if path.name not in NOT_A_WORKFLOW
    )


def sections_defined_by(path: Path, required: list[str]) -> list[str]:
    """Which of `required` a workflow document actually has a section for.

    Matched as a heading or a bare line, case-insensitively, because these
    documents are inconsistent about both — some write `Trigger` as a plain line,
    `workflows/Events/NewResearch.md` writes `Departments Activated` as a heading.
    """
    text = path.read_text(encoding="utf-8")
    return [
        name
        for name in required
        if re.search(rf"^\s*#*\s*{re.escape(name)}\b", text, re.M | re.I)
    ]


# ADR-010 rule 5. These appear in Deliverables lists but are not artifacts:
# `workflows/WorkflowEngine.md` makes "Update Knowledge" a step in the execution
# model of every workflow, and `workflows/Events/StrategyPromotion.md` lists the
# other two as workflow steps. They are effects on stored state, not documents
# produced. Excluded by name and stated here rather than filtered silently.
DELIVERABLE_EFFECTS = {"Knowledge Update", "Repository Update", "Knowledge Graph Update"}

# The headings under which a document declares what it produces. Four spellings
# because the documents use four — `Output` in the Research role documents,
# `Outputs` in the department READMEs, `Deliverable` in `Validation/Critic.md`,
# `Deliverables` everywhere else.
DELIVERABLE_HEADINGS = ("Deliverables", "Deliverable", "Outputs", "Output")


def declared_deliverables() -> set[str]:
    """Every deliverable the departmental and workflow documents declare.

    ADR-010 rule 4: the vocabulary is derived, never transcribed. A list copied
    into this file would drift from the documents exactly as silently as the code
    has drifted before, and the drift is the thing being guarded against — so the
    documents have to be the input.

    Singular and plural are one name: `departments/Research/README.md` writes
    `Universe Reports` and `Research/UniverseDiscovery.md` writes `Universe
    Report`, and they are the same deliverable. ADR-010 rule 6 — cadence and
    producer are not part of a deliverable's identity.

    Twenty-four as of 2026-07-31, from 34 entries across eleven documents.
    """
    found = set()
    for directory in ("departments", "Research", "Validation", "Operations", "workflows"):
        for path in sorted((REPO / directory).rglob("*.md")):
            # Annotation blocks are prior sessions' notes, not declarations.
            text = path.read_text(encoding="utf-8").split("\n> **")[0]
            for heading in DELIVERABLE_HEADINGS:
                match = re.search(
                    rf"^\s*#*\s*{heading}\s*?\n(.*?)(?=^---|\Z)", text, re.M | re.S
                )
                if match:
                    found.update(_entries_in(match.group(1)))
                    break  # `Deliverables` before `Deliverable`, `Outputs` before `Output`
    return {name for name in _singularise(found) if name not in DELIVERABLE_EFFECTS}


def _entries_in(body: str) -> list[str]:
    """The deliverable names in one declaration block, one per line.

    An `Output` section continues into a `Containing:` or `Fields:` block
    describing that deliverable's internals — `Motivation`, `Hypothesis`,
    `Expected Edge` and so on. Those are the deliverable's contents, not further
    deliverables, so the walk stops there.
    """
    entries = []
    for line in body.splitlines():
        name = line.strip()
        if name in ("Containing", "Fields:"):
            break
        if name and not name.startswith("#"):
            entries.append(name)
    return entries


def _singularise(names: set[str]) -> set[str]:
    """Collapse `Universe Reports` onto `Universe Report` where both are declared.

    `departments/Research/README.md` writes the plural and
    `Research/UniverseDiscovery.md` the singular. Only collapsed when both forms
    are actually present, so a deliverable that is only ever declared in the
    plural — `Paper Trade Logs` — keeps the name its document gives it.
    """
    return {name[:-1] if name.endswith("s") and name[:-1] in names else name for name in names}


def required_metadata_fields() -> set[str]:
    """The top-level keys of the example block in `docs/DocumentStandard.md`.

    The standard states its requirement by example rather than as a list, so the
    example *is* the specification and is parsed as one. The previous test read
    nothing from this document at all, which meant it could not notice the
    standard changing — it asserted only that a file began with `---`.
    """
    text = (REPO / "docs" / "DocumentStandard.md").read_text(encoding="utf-8")
    block = text.split("Example:", 1)[1].split("---", 2)[1]
    return set(re.findall(r"^([a-z_]+):", block, re.M))


def metadata_keys_in(text: str) -> set[str]:
    """The top-level keys of a document's own leading metadata block."""
    return set(re.findall(r"^([a-z_]+):", text.split("---", 2)[1], re.M))


def strategy_document_sequence() -> list[str]:
    """The arrow-joined entries `strategies/Lifecycle.md` presents as a sequence.

    Nine of them as of 2026-07-31, against the doctrine's eight. Parsed from the
    opening line down to the first rule that follows, discarding the `↓` arrows —
    the same shape as `doctrine_lifecycle_stages` above, because the two lists are
    meant to be compared.
    """
    text = (REPO / "strategies" / "Lifecycle.md").read_text(encoding="utf-8")
    body = text.split("Every strategy follows the same institutional lifecycle.", 1)[1]
    body = body.split("Strategies may move backward.", 1)[0]
    return [
        line.strip()
        for line in body.splitlines()
        if line.strip() and line.strip() != "↓"
    ]


def strategy_document_annotation() -> str:
    """Everything after the first rule in `strategies/Lifecycle.md`.

    The document carried no `---` before it was annotated on 2026-07-31, so this
    is the annotation and nothing else. Further notes appended below it are
    included, which is how `Validation/CapitalReview.md` already carries two.
    """
    text = (REPO / "strategies" / "Lifecycle.md").read_text(encoding="utf-8")
    return text.split("---", 1)[1]


def backtest_minimum_metrics() -> list[str]:
    """The nine names under `Minimum Metrics` in `Validation/Backtesting.md`.

    Parsed rather than transcribed, for the reason every parser in this file is:
    a copy cannot notice its source changing. The document writes them one per
    line with a blank line between, which is why blanks are dropped rather than
    used as a terminator.
    """
    text = (REPO / "Validation" / "Backtesting.md").read_text(encoding="utf-8")
    body = text.split("Minimum Metrics", 1)[1].split("---", 1)[0]
    return [line.strip() for line in body.splitlines() if line.strip()]


def backtest_required_documentation() -> list[str]:
    """The four things `Validation/Backtesting.md` says a backtest must document.

    Lines 35-43. This requirement had no implementation at all until ADR-011:
    `EvidenceRecord.source` covered `Data Source` and nothing covered the other
    three, while `docs/HANDOFF.md:1287` recorded that all four were covered.
    """
    text = (REPO / "Validation" / "Backtesting.md").read_text(encoding="utf-8")
    body = text.split("Backtests must document", 1)[1].split("---", 1)[0]
    return [line.strip() for line in body.splitlines() if line.strip()]


# ADR-011 rule 11. Four of the nine documented metrics are computable from a
# return series and are built; the other five are not, and the reasons differ.
#
# `Trade Count` and `Exposure` need an input a return series does not carry — it
# contains no trades, and a 0.0 return is indistinguishable between no position
# held and a position held at an unchanged price. `Win Rate` needs a ruling on
# whether a win is a period or a trade. `Benchmark Comparison` needs a second
# series. `Tail Events` needs a threshold no document states.
#
# `docs/HANDOFF.md:5321` claimed Win Rate, Exposure and Trade Count were
# computable from a return series alone. They are not, and `docs/ROADMAP.md:104`
# had it right.
ADR_011_IN_SCOPE = {"CAGR", "Sharpe", "Sortino", "Drawdown"}

# The substring that identifies each documented metric among the function names
# under `framework/metrics/`. Substrings rather than exact names, so that
# `def benchmark(...)` is caught as readily as `def benchmark_comparison(...)` —
# the test exists to notice an unruled metric appearing, and an exact-match list
# would be evaded by any spelling its author preferred.
#
# **`Tail Events` was tokenised as `tail` and is now `tail_event`. ADR-012 rule
# 13.** The looser token had a false positive, found the day after this watcher
# was written and by the very next piece of work: a two-sided significance test
# is naturally implemented as a function with `two_tailed` in its name, which
# would have made this test report `Tail Events` as **built** while it was
# untouched. A watcher that reports a gap closed when it is open is the
# reassuring half-truth `scripts/status.py` exists to prevent, and it is worse
# than no watcher at all.
#
# The ADR-012 implementation avoids `tail` in its function names as well, so
# both halves hold independently. That is belt and braces on purpose: the
# naming was avoided by someone who happened to know about the collision, and
# that is not a property the next author inherits.
METRIC_TOKENS = {
    "CAGR": "cagr",
    "Sharpe": "sharpe",
    "Sortino": "sortino",
    "Drawdown": "drawdown",
    "Win Rate": "win_rate",
    "Exposure": "exposure",
    "Trade Count": "trade_count",
    "Benchmark Comparison": "benchmark",
    "Tail Events": "tail_event",
}


def metric_functions_defined() -> set[str]:
    """Every module-level function name under `framework/metrics/`."""
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((REPO / "framework" / "metrics").rglob("*.py"))
    )
    return set(re.findall(r"^def (\w+)", source, re.M))


def constitutional_promotion_criteria() -> list[str]:
    """The seven criteria of `constitution/Promotion_Pipeline.md:75-81`, in order.

    ADR-006 rule 1 ruled this list authoritative, and rule 3 ruled its wording
    canonical where the departmental documents disagree — `Regime robustness`
    not compatibility, `Operational consistency` not stability or readiness,
    `Risk-adjusted returns` not bare `Risk`. Parsed rather than transcribed, so
    the test cannot agree with a stale copy of the document.

    Bounded to the first bullet block. `startswith("-")` was too loose and this
    test caught it immediately: a `---` rule added lower down the same document
    parsed as an eighth, empty criterion. A markdown horizontal rule is not a
    list item, so the discriminator is `- ` with the space, and the walk stops at
    the first line that is neither blank nor a bullet.
    """
    text = (REPO / "constitution" / "Promotion_Pipeline.md").read_text(encoding="utf-8")
    body = text.split("Promotion shall consider:", 1)[1]

    criteria = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if not stripped.startswith("- "):
            break
        criteria.append(stripped[2:].strip())
    return criteria


# The maturity ladder: the eight doctrine stages in order, with RETIRED removed.
#
# RETIRED is declared last in StrategyLifecycle — index 8, above PRODUCTION at 7
# — but the doctrine places retirement outside the sequence, reachable from
# anywhere. Comparing positions over list(StrategyLifecycle) would therefore
# read every retirement as the deepest promotion in the system. RETIRED is
# removed before any position is compared and classified separately. ADR-004.
LADDER = [stage for stage in StrategyLifecycle if stage is not StrategyLifecycle.RETIRED]

# docs/DECISIONS.md ADR-004, "Resulting Transitions", reproduced as pairs. Ten
# moves, every one a demotion; no forward transition changed. PAPER_TRADING is
# the floor — a destination four times and never an origin, because below it
# there is no capital privilege left to withdraw.
ADR_004_DEMOTIONS = {
    (StrategyLifecycle.PRODUCTION, StrategyLifecycle.LIMITED_CAPITAL),
    (StrategyLifecycle.PRODUCTION, StrategyLifecycle.MICRO_CAPITAL),
    (StrategyLifecycle.PRODUCTION, StrategyLifecycle.PROMOTION_REVIEW),
    (StrategyLifecycle.PRODUCTION, StrategyLifecycle.PAPER_TRADING),
    (StrategyLifecycle.LIMITED_CAPITAL, StrategyLifecycle.MICRO_CAPITAL),
    (StrategyLifecycle.LIMITED_CAPITAL, StrategyLifecycle.PROMOTION_REVIEW),
    (StrategyLifecycle.LIMITED_CAPITAL, StrategyLifecycle.PAPER_TRADING),
    (StrategyLifecycle.MICRO_CAPITAL, StrategyLifecycle.PROMOTION_REVIEW),
    (StrategyLifecycle.MICRO_CAPITAL, StrategyLifecycle.PAPER_TRADING),
    (StrategyLifecycle.PROMOTION_REVIEW, StrategyLifecycle.PAPER_TRADING),
}


def demotions_in(table) -> set[tuple[StrategyLifecycle, StrategyLifecycle]]:
    """Every backward move a strategy transition table permits, as (from, to).

    RETIRED is discarded first rather than compared: it has no ladder position,
    and giving it one is the trap described above.
    """
    found = set()
    for stage in LADDER:
        for target in table[stage]:
            if target is StrategyLifecycle.RETIRED:
                continue
            if LADDER.index(target) < LADDER.index(stage):
                found.add((stage, target))
    return found


# --------------------------------------------------------------- holding today


def test_strategy_stages_all_appear_in_the_doctrine():
    """constitution/Paper_First_Capital_Doctrine.md defines the sequence."""
    text = doc("constitution/Paper_First_Capital_Doctrine.md")

    for stage in StrategyLifecycle:
        if stage is StrategyLifecycle.RETIRED:
            continue  # placed outside the sequence by the doctrine
        assert stage.value.lower() in text, f"{stage.value} is not in the doctrine"


def test_readme_agrees_with_the_doctrine():
    """Two documents state this sequence; the code follows both."""
    text = doc("README.md")

    for stage in StrategyLifecycle:
        if stage is StrategyLifecycle.RETIRED:
            continue
        assert stage.value.lower() in text


def test_strategy_lifecycle_is_the_doctrine_sequence_in_order():
    """ADR-007 rule 1: the doctrine's eight stages *are* the lifecycle.

    The test above checks membership, which a reordered doctrine would still
    pass. This one compares sequences, because the order is the whole content of
    a promotion ladder — a doctrine that swapped Micro and Limited Capital would
    make a strategy's first contact with real money its largest, and nothing
    would have gone red.

    RETIRED is excluded on both sides: the doctrine places retirement outside
    the sequence, reachable from anywhere, and it is the enum's highest ordinal.
    See the LADDER note above.
    """
    documented = doctrine_lifecycle_stages()

    assert len(documented) == 8, f"expected the doctrine's eight stages, parsed {documented}"
    assert [stage.value.upper() for stage in LADDER] == documented


def test_the_strategy_document_annotates_every_entry_that_is_not_a_ladder_stage():
    """ADR-007 rule 3, and the last thing its Consequences flagged as unfixed.

    `strategies/Lifecycle.md` joins nine entries with `↓` arrows, and the arrow
    into `Retirement` is the defect: it presents retirement as the rung reached by
    surviving Production, when the doctrine places it outside the sequence and
    reachable from anywhere. Three of the nine — `Hypothesis`, `Paper` and
    `Retirement` — are not stages of `STRATEGY_LADDER` at all.

    ADR-007 required the document be annotated rather than rewritten, because
    lines 39 and 41 are quoted by ADR-004 and by `framework/artifacts/validator.py`.
    This holds the annotation to the sequence: whatever the document lists that is
    not a real ladder stage has to be explained in the note below it, so the two
    cannot drift apart the way the criteria lists did.

    Not vacuous by construction — an entry that parses to nothing would satisfy
    the loop trivially, so the parse is checked first. That is the failure mode
    that put a wrong figure on the dashboard for two sessions.
    """
    entries = strategy_document_sequence()
    assert len(entries) >= 8, f"the sequence did not parse: {entries}"

    ladder = {stage.value for stage in LADDER}
    annotation = strategy_document_annotation()

    for entry in entries:
        if entry in ladder:
            continue
        assert entry in annotation, (
            f"{entry!r} is listed as a lifecycle stage but is not one, and the "
            "annotation does not mention it"
        )


def test_the_strategy_document_keeps_the_lines_adr_004_and_the_validator_quote():
    """Two lines of this document are load-bearing outside it.

    `Strategies may move backward` is one of the five citations ADR-004 rests its
    demotion ruling on — `docs/DECISIONS.md:345`. `Strategies never skip stages`
    is quoted in the comment above `STRATEGY_TRANSITIONS` in
    `framework/artifacts/validator.py` and in three test docstrings.

    Deleting either would leave an Accepted ADR resting on a quotation that is no
    longer in the repository, and nothing else would notice. Immutable Law VII
    forbids discarding them; this is what enforces it.
    """
    text = (REPO / "strategies" / "Lifecycle.md").read_text(encoding="utf-8")

    for line in ("Strategies may move backward.", "Strategies never skip stages."):
        assert line in text, f"{line!r} was removed from strategies/Lifecycle.md"


def test_promotion_criteria_match_the_constitution():
    """ADR-006 rule 1: `constitution/Promotion_Pipeline.md:75-81` governs.

    `scripts/status.py` reports "N of 7 computable" against this list, and until
    ADR-006 that choice of seven was an explicitly recorded working assumption.
    It is now ruled, so the dashboard's list is checked against the document
    rather than trusted — including the wording, which ADR-006 rule 3 made
    canonical where the departmental documents disagree.
    """
    from scripts.status import PROMOTION_CRITERIA

    documented = constitutional_promotion_criteria()

    assert len(documented) == 7, f"expected seven criteria, parsed {documented}"
    assert [name for name, _expected_path in PROMOTION_CRITERIA] == documented


def test_review_outcomes_cover_every_documented_outcome():
    """ADR-009 rule 3, resting on ADR-008 rules 3 and 4.

    Three documents list the outcomes of a review and no two listed them
    identically. `ReviewOutcome` must cover all of them and add nothing of its
    own, so that a fourth spelling cannot appear in a document without the suite
    noticing.

    `Reject` is not a fifth member. ADR-008 rule 4 rules it the decision-side
    name for the event whose state-side name is `Remain Current Stage`:
    `Validation/CapitalReview.md` is the only document carrying both, and its
    lines 7 and 9 explain why — it processes a *request*, so it names the
    decision on the request as well as the effect on the strategy. One event with
    two names must not become two members.
    """
    from framework.artifacts.enums import ReviewOutcome

    aliases = {"Reject": ReviewOutcome.REMAIN_CURRENT_STAGE}
    sources = [
        ("strategies/ReviewTemplate.md", "Recommendation"),
        ("Validation/CapitalReview.md", "Possible Outcomes"),
        ("workflows/Monthly/StrategyPromotion.md", "Possible Decisions"),
    ]

    documented = set()
    for relative, heading in sources:
        listed = outcomes_under(relative, heading)
        assert listed, f"parsed no outcomes from {relative} under {heading}"
        documented |= listed

    resolved = {aliases.get(name) or ReviewOutcome(name) for name in documented}

    assert resolved == set(ReviewOutcome)
    assert {member.value for member in ReviewOutcome} | set(aliases) == documented


def test_artifact_stages_all_appear_in_the_knowledge_document():
    text = doc("Knowledge/ArtifactLifecycle.md")

    for stage in ArtifactLifecycle:
        assert stage.value.lower() in text, f"{stage.value} is not documented"


def test_evidence_levels_match_the_constitution():
    """constitution/Evidence_Standards.md recognises exactly four classes."""
    text = doc("constitution/Evidence_Standards.md")

    assert {level.value for level in EvidenceLevel} == {"A", "B", "C", "D"}
    for level in EvidenceLevel:
        assert f"level {level.value.lower()}" in text


def test_identifier_prefixes_match_the_knowledge_document():
    """Knowledge/Identifiers.md defines eight prefixes; the code must have all."""
    text = doc("Knowledge/Identifiers.md")

    assert len(VALID_PREFIXES) == 8
    for prefix in VALID_PREFIXES:
        assert prefix.lower() in text, f"{prefix} is not a documented prefix"


def test_integrity_covers_every_field_governance_requires():
    """constitution/Governance.md: every artifact shall possess identifier,
    version, author, date and status — so the signature must cover them."""
    covered = set(
        ArtifactIntegrity.canonical_payload(
            Artifact(id="RPT-0001", title="t", type=ArtifactType.REPORT)
        )
    )

    assert {"id", "version", "author", "created", "updated", "lifecycle"} <= covered


def test_retirement_is_reachable_from_every_strategy_stage():
    """Paper_First_Capital_Doctrine.md: retirement may occur at any stage."""
    table = ArtifactValidator.STRATEGY_TRANSITIONS

    for stage, onward in table.items():
        if stage is StrategyLifecycle.RETIRED:
            continue
        assert StrategyLifecycle.RETIRED in onward, f"cannot retire from {stage.value}"


def test_no_strategy_stage_may_be_skipped():
    """strategies/Lifecycle.md: "Strategies never skip stages."

    Each stage has exactly one forward move. Micro capital cannot be bypassed.

    Forward is now the operative word. This test used to filter RETIRED out of
    each row and treat the remainder as the promotion, which was true only while
    every other move was one. ADR-004 admits backward moves of any depth, so the
    proxy is replaced by a ladder-position comparison.

    It also examines PRODUCTION, which the old bound of ordered[:-2] excluded:
    the stage that gained the most new transitions was precisely the one stage
    this test was not looking at.
    """
    table = ArtifactValidator.STRATEGY_TRANSITIONS

    for index, stage in enumerate(LADDER):
        forward = [
            target
            for target in table[stage]
            if target is not StrategyLifecycle.RETIRED and LADDER.index(target) > index
        ]
        # Empty at PRODUCTION, the top of the ladder — there is nowhere further
        # to be promoted to, and the slice yields [] to say so.
        assert forward == LADDER[index + 1 : index + 2], (
            f"{stage.value} does not step forward by exactly one"
        )


def test_a_strategy_can_be_demoted():
    """Five documents require backward movement; three treat Demote as a formal
    decision outcome — ReviewTemplate.md, CapitalReview.md, and the monthly
    StrategyPromotion workflow all list it beside Promote, Remain and Retire.

    ADR-004 rule 1: a demotion names one destination and moves there in a single
    act. Promotion steps one stage at a time because each stage proves something
    and a skipped proof cannot be claimed. Falling proves nothing, so the
    constraint does not bind downward — a rung is hard to climb and easy to
    lose.

    Legality only. The table can rule that a move is possible; it cannot know
    whether the written justification rule 4 requires was ever produced.
    """
    validator = ArtifactValidator()

    for current, target in sorted(ADR_004_DEMOTIONS, key=lambda p: (p[0].value, p[1].value)):
        assert validator.validate_transition(current, target)


def test_demotion_goes_no_lower_than_paper_trading():
    """ADR-004 rule 2: the floor is PAPER_TRADING.

    A demoted strategy may lose every unit of capital and be sent back to
    rebuild its live-behaviour record. It may not be sent below that.
    VALIDATION, RESEARCH and IDEA are stages of construction rather than
    operation, and a strategy whose statistical proof is falsified has not been
    demoted, it has been refuted — which is retirement with history preserved.
    """
    floor = LADDER.index(StrategyLifecycle.PAPER_TRADING)

    for current, target in demotions_in(ArtifactValidator.STRATEGY_TRANSITIONS):
        assert LADDER.index(target) >= floor, (
            f"{current.value} may be demoted to {target.value}, below the floor"
        )
        assert LADDER.index(current) > floor, (
            f"{current.value} is at or below the floor and still has a demotion target"
        )

    # Stated directly as well as by the rule above, because a rule quantified
    # over an empty set would pass: the floor itself has nowhere down to go.
    assert ArtifactValidator.STRATEGY_TRANSITIONS[StrategyLifecycle.PAPER_TRADING] == (
        StrategyLifecycle.PROMOTION_REVIEW,
        StrategyLifecycle.RETIRED,
    )


def test_the_demotion_table_is_exactly_what_adr_004_tabulates():
    """Ten moves become legal, and no more.

    Pinned as a whole set rather than checked one at a time, so that a later
    extra or missing demotion is caught rather than assumed. An eleventh would
    be a capital rule nobody decided.
    """
    assert len(ADR_004_DEMOTIONS) == 10
    assert demotions_in(ArtifactValidator.STRATEGY_TRANSITIONS) == ADR_004_DEMOTIONS


def test_the_disclosure_block_names_everything_a_backtest_must_document():
    """`Validation/Backtesting.md:35-43` — ADR-011 rule 9.

    "Backtests must document: Assumptions, Data Source, Sample Period, Known
    Limitations." That is a requirement of the constitution's validation layer,
    and until 2026-07-31 nothing enforced it — `EvidenceRecord` covered `Data
    Source` under the name `source` and had no field for the other three.

    Held to the document rather than to a list written here, so that a fifth
    requirement added to `Validation/Backtesting.md` turns the suite red instead
    of being silently unrecorded on every metric artifact Belay emits.
    """
    from framework.metrics.reporting import Disclosure

    documented = backtest_required_documentation()
    assert len(documented) == 4, f"expected four, parsed {documented}"

    fields = {field.name for field in dataclasses.fields(Disclosure)}

    assert {name.lower().replace(" ", "_") for name in documented} == fields


def test_only_the_backtest_metrics_adr_011_scopes_in_are_built():
    """`Validation/Backtesting.md` names nine minimum metrics. Four are built.

    This is a watcher in both directions and that is the point of it.

    Downward: if `framework/metrics/` loses one of the four, the suite goes red
    rather than the dashboard quietly reporting one fewer computable criterion.

    Upward — the direction that matters — **if someone implements `Win Rate`,
    `Exposure`, `Trade Count`, `Benchmark Comparison` or `Tail Events`, this
    goes red until the ruling each of them needs has been made.** Every one of
    those five is missing something a return series cannot supply, and building
    one means inventing the missing input. `Win Rate` is the likeliest: it looks
    like an afternoon's work and it requires deciding whether a win is a period
    or a trade, which is a question `Validation/Backtesting.md:23` does not
    answer. Choosing quietly between two readings of one word is how the
    five-way promotion-criteria divergence started.

    The nine names are parsed from the document, so the test cannot agree with a
    stale copy of the list — and if the document ever names a tenth metric, the
    count assertion fails before the scope assertion gets a chance to mislead.
    """
    documented = backtest_minimum_metrics()

    assert len(documented) == 9, f"expected nine metrics, parsed {documented}"
    assert set(documented) == set(METRIC_TOKENS), (
        f"the document names {sorted(set(documented) - set(METRIC_TOKENS))} "
        f"which this test has no token for"
    )

    defined = metric_functions_defined()
    built = {
        name
        for name in documented
        if any(METRIC_TOKENS[name] in function for function in defined)
    }

    assert built == ADR_011_IN_SCOPE, (
        f"built but not scoped in by ADR-011 rule 11: {sorted(built - ADR_011_IN_SCOPE)}; "
        f"scoped in but not built: {sorted(ADR_011_IN_SCOPE - built)}"
    )


# ------------------------------------------------- open findings, see HANDOFF


def test_artifact_has_every_field_the_schema_requires():
    """Knowledge/Schema.md lists thirteen required fields, lines 7-31.

    The count was recorded as fourteen until 2026-07-30, when it was counted
    line by line. Thirteen is the verified figure, and it is now parsed from the
    document rather than written here, so editing the schema moves this test.
    """
    required = schema_required_fields()

    assert len(required) == 13
    assert {"Tags", "Summary", "Current Confidence", "Evidence Level"} <= required
    assert {"tags", "summary", "confidence", "evidence_level"} <= artifact_fields()


def test_confidence_can_be_adjusted():
    """ReviewTemplate.md:37-43 has a Confidence Adjustment field: Increase,
    Decrease, No Change.

    ADR-005 rules that an adjustment produces a NEW VERSION rather than mutating
    in place, because `Knowledge/Versioning.md:25` states "No version is
    overwritten" — the history of an estimate is itself the evidence trail.

    Until 2026-07-30 this test asserted only `"confidence" in artifact_fields()`,
    which an immutable field would have satisfied. It would have gone green
    without confidence becoming adjustable at all, and closing the *other*
    finding would have flipped it. It now checks both halves of the ruling: the
    figure is revisable across versions, and it is not mutable in place.
    """
    factory = ArtifactFactory()
    common = dict(
        identifier="RPT-0001",
        title="Max drawdown",
        artifact_type=ArtifactType.REPORT,
    )

    original = factory.create(**common, version="1.0.0", confidence=0.4)
    revised = factory.create(**common, version="1.0.1", confidence=0.7)

    # Revisable: the same artifact carries a different figure at a later version.
    assert original.confidence == 0.4
    assert revised.confidence == 0.7
    assert version_key(revised.version) > version_key(original.version)

    # Not mutable in place: the prior figure cannot be destroyed.
    with pytest.raises(dataclasses.FrozenInstanceError):
        original.confidence = 0.7


@pytest.mark.xfail(strict=True, reason="HANDOFF: Workflow Base Class Incomplete; Registry Empty")
def test_workflow_defines_everything_the_documentation_requires():
    """`workflows/README.md`: every workflow *defines* five things.

    **Strengthened 2026-07-31. It asserted `hasattr` for five transcribed
    names.** `framework/workflows/base.py` already carries `trigger = ""` and
    `departments = []`, so two of the five passed against empty placeholders, and
    adding `required_inputs = []`, `deliverables = []` and
    `completion_criteria = []` would have turned it green with the base class
    defining nothing at all. A watcher that can be satisfied without closing its
    finding is worse than no watcher: the backlog then reports itself cleaner
    than it is.

    The document says every workflow *defines* these, so the property to assert
    is that a subclass cannot omit them — which `abc` already expresses in this
    very class, where `execute` is an `@abstractmethod`. This applies the
    mechanism the base class already chose rather than inventing a second one,
    and an empty default is then not enough by construction.

    Two spellings are accepted per requirement because the document writes
    `Departments Activated` and the code writes `departments`. Nothing has ruled
    that naming, so this test rules on substance instead.
    """
    from framework.workflows.base import Workflow

    required = workflow_requirements()
    assert len(required) == 5, f"expected five requirements, parsed {required}"

    for name in required:
        candidates = {name.lower().replace(" ", "_"), name.split()[0].lower()}
        assert candidates & Workflow.__abstractmethods__, (
            f"{name!r} is not required of a Workflow subclass — none of "
            f"{sorted(candidates)} is abstract, so a subclass may omit it"
        )


@pytest.mark.xfail(strict=True, reason="HANDOFF: Workflow Base Class Incomplete; Registry Empty")
def test_every_documented_workflow_is_registered():
    """Thirteen workflows are documented under `workflows/`. None exist in code.

    **Strengthened 2026-07-31. It asserted `len(WORKFLOWS) >= documented`**, which
    thirteen unrelated entries would have satisfied — it never checked that the
    registered workflows were the documented ones. And `documented` came from
    `len(rglob("*.md")) - 2`, so adding any markdown file under `workflows/`
    silently changed what the figure meant.

    Both are fixed: the two non-workflow documents are named rather than
    subtracted, the count is exact rather than a floor, and every documented
    workflow has to be findable among the registry keys.

    **One limit, recorded rather than guessed.** The match normalises away case
    and punctuation because the registry key convention is undecided —
    `register()` uses `workflow.name` and nothing rules what that string looks
    like.

    Two documents share the stem `StrategyPromotion`, under `Events/` and
    `Monthly/`. **Both were opened on 2026-07-31 and they are two workflows, not
    one** — the claim was asserted here before it was checked, and the evidence
    turns out to be sharper than the claim. `Events/StrategyPromotion.md` is an
    event: its trigger is "Promotion threshold satisfied", and it runs one
    candidate through Validation → Operations → Knowledge → Investment Committee.
    `Monthly/StrategyPromotion.md` is a calendared review whose objective is to
    "Evaluate every promotion candidate" and which ends in a decision from
    `ReviewOutcome`. Different trigger, different scope, different cadence.

    So name matching cannot tell that pair apart, and the exact count is what
    forces thirteen distinct keys. Pinning a stricter rule would mean ruling the
    key convention first, which is the mistake ADR-004 named.
    """
    from framework.workflows.registry import WORKFLOWS

    documented = documented_workflows()
    assert documented, "no workflow documents parsed at all"

    assert len(WORKFLOWS) == len(documented), (
        f"{len(WORKFLOWS)} registered against {len(documented)} documented"
    )

    registered = {re.sub(r"[^a-z0-9]", "", key.lower()) for key in WORKFLOWS}
    for _category, name in documented:
        token = re.sub(r"[^a-z0-9]", "", name.lower())
        assert any(token in key for key in registered), f"{name} is not registered"


@pytest.mark.xfail(strict=True, reason="HANDOFF: Workflow Base Class Incomplete; Registry Empty")
def test_every_workflow_document_defines_what_the_readme_requires():
    """`workflows/README.md`: "Every workflow defines" five things.

    **The documents are in the same state as the base class, which was not known
    until 2026-07-31.** The finding this watches has always been stated as a code
    defect — `framework/workflows/base.py` provides two of the five. All thirteen
    documents were then checked rather than the two that happened to be open:
    **not one of them defines all five.** The best is two (`Trigger` and
    `Deliverables`); `Monthly/StrategyPromotion.md` and
    `Weekly/WeeklyPortfolioReview.md` define none of the five.

    That matters for sequencing, which is why it is a test rather than a
    paragraph. `Workflow` cannot be filled in by transcribing these documents,
    because the documents do not carry the five things either — so whoever
    implements it is writing doctrine and should expect to need a ruling, not
    just an afternoon.
    """
    required = workflow_requirements()
    assert len(required) == 5, f"expected five requirements, parsed {required}"

    incomplete = []
    for path in sorted((REPO / "workflows").rglob("*.md")):
        if path.name in NOT_A_WORKFLOW:
            continue
        defined = sections_defined_by(path, required)
        if len(defined) < len(required):
            missing = [name for name in required if name not in defined]
            incomplete.append(f"{path.parent.name}/{path.stem} lacks {', '.join(missing)}")

    assert not incomplete, (
        f"{len(incomplete)} workflow documents define fewer than five: "
        + "; ".join(incomplete[:3])
        + (" ..." if len(incomplete) > 3 else "")
    )


def test_artifact_type_can_name_the_documented_deliverables():
    """ADR-010 rule 9. **The `xfail` marker came off on 2026-07-31.**

    This test was the last of the six weak watchers, and the only one that could
    not honestly be strengthened when the others were. Its name claimed the enum
    could name the documented deliverables — roughly twenty — while it asserted a
    four-name subset, so adding exactly `UNIVERSE_REPORT`, `BACKTEST`, `CRITIQUE`
    and `RESEARCH_MEMO` would have turned it green with sixteen deliverables
    still unnameable and the decision its finding asked for left unmade.

    It could not be fixed because **what it should assert was the open question.**
    A closed enum meant "every deliverable has an `ArtifactType` member"; a coarse
    enum plus a subtype means "every deliverable resolves to a pair". ADR-010
    ruled the second, so this is now that test.

    The vocabulary is parsed from the eleven declaring documents rather than
    transcribed, so a deliverable added to a departmental document without a
    corresponding member turns the suite red — which is the property the old
    version never had.
    """
    from framework.artifacts.enums import DELIVERABLE_ARTIFACT_TYPE, DeliverableType

    declared = declared_deliverables()
    assert len(declared) == 24, f"expected twenty-four deliverables, parsed {sorted(declared)}"

    assert {member.value for member in DeliverableType} == declared

    for deliverable in DeliverableType:
        assert deliverable in DELIVERABLE_ARTIFACT_TYPE, (
            f"{deliverable.value} resolves to no ArtifactType"
        )


def test_every_expected_component_is_either_built_or_planned():
    """Every component the dashboard expects must exist or be in the roadmap.

    **This was written as an `xfail(strict=True)` watcher and the marker came
    off within the same commit, because the commit that opened its finding also
    closed the thing it watched.** Recorded rather than tidied away: it is the
    clearest demonstration in this repository of the mechanism working, and it
    caught its own author.

    The sequence. `framework/services/execution.py` and
    `framework/services/liquidity.py` existed in no file and in no plan, which
    is the narrow checkable edge of `docs/HANDOFF.md`'s "The Roadmap Does Not
    Reach The Mission". The watcher was written, run under `--runxfail`, and
    confirmed to fail naming both. Then `docs/ROADMAP.md` gained Stages 6 to 9
    and named both components — and the suite went **red with `XPASS(strict)`**
    on the next run, exactly as the mechanism is designed to: the gap closed, so
    the marker had to go.

    `PROMOTION_CRITERIA` names the component expected to make each
    constitutional promotion criterion computable. That list is the engineering
    backlog — `docs/ROADMAP.md` says so itself. So every path in it should
    either exist, or be named somewhere in the roadmap as work that is coming.

    **`framework/services/execution.py` and `framework/services/liquidity.py`
    are neither.** They do not exist as files, they are not among the ten
    placeholders under `framework/services/` that ROADMAP Stage 5 promises to
    fill in, and neither filename appears anywhere in `docs/ROADMAP.md`.

    That is the narrow, checkable edge of a wider gap. `constitution/Mission.md:5`
    states Belay exists for "evidence-driven capital allocation" and line 38 that
    it "optimizes for decades—not days", but the roadmap's six stages end at a
    services layer and never deliver execution, live position state, a halt
    mechanism, or tax lot accounting. The plan does not reach the mission. See
    the HANDOFF section this marker cites.

    **The finding is not closed. This test never watched all of it.** It watches
    whether the work is *planned*; whether it is *done* is what the dashboard's
    "N of 7 computable" and "N of 10 stages" already report, and duplicating that
    here would give one gap two watchers that could disagree.

    So its job now is a regression guard rather than a countdown: **if a future
    session deletes Stages 6 to 9, or drops a criterion's component from the
    plan, this goes red.** That is precisely the regression that created the
    finding — a roadmap that stopped short and looked complete because every
    stage it did list was real.
    """
    from scripts.status import PROMOTION_CRITERIA

    unaccounted = []
    for criterion, relative in PROMOTION_CRITERIA:
        if (REPO / relative).exists():
            continue
        if Path(relative).name in (REPO / "docs" / "ROADMAP.md").read_text(
            encoding="utf-8"
        ):
            continue
        unaccounted.append(f"{criterion} expects {relative}")

    assert not unaccounted, (
        f"{len(unaccounted)} of {len(PROMOTION_CRITERIA)} promotion criteria "
        f"expect a component that neither exists nor appears in the roadmap: "
        + "; ".join(unaccounted)
    )


@pytest.mark.xfail(strict=True, reason="HANDOFF: ArtifactType And The Identifier Prefixes Are Two Vocabularies That Disagree")
def test_artifact_types_and_identifier_prefixes_name_the_same_kinds():
    """Two vocabularies for "what kind of artifact is this" that do not agree.

    Found on 2026-07-31 while implementing ADR-010 rule 9, which needed to map
    each deliverable to an `ArtifactType`. `PORTFOLIO` and `FAILURE` are enum
    members with no prefix in `Knowledge/Identifiers.md`, and `DOC` is a prefix
    with no member.

    **The consequence is demonstrable rather than theoretical.** ADR-010 maps
    `Paper Trade Logs` and `Portfolio Health Report` to `PORTFOLIO` and
    `Failure Investigations` to `FAILURE`, and `ArtifactFactory` refuses
    `PORTFOLIO-0001` — "Expected PREFIX-NNNN with a prefix from ['DOC', 'EXP',
    'REGIME', 'REV', 'RPT', 'RS', 'STRAT', 'WF']". So three documented
    deliverables cannot receive an identifier that names what they are, and the
    only way to store one today is to label it `RPT-`, which is untrue.

    Closing this is a ruling, not an edit: either `Knowledge/Identifiers.md`
    gains two prefixes, or `ArtifactType` loses two members, and both directions
    touch a governing document. Not guessed here.
    """
    from framework.identifiers import PREFIXES

    types = {member.value.lower() for member in ArtifactType}
    kinds = set(PREFIXES)

    assert types == kinds, (
        f"types without a prefix: {sorted(types - kinds)}; "
        f"prefixes without a type: {sorted(kinds - types)}"
    )


def test_relationship_types_are_constrained():
    """Knowledge/Relationships.md defines eleven types, lines 9-29.

    This test used to assert only `hasattr(relationships, "RelationshipType")`,
    which an empty enum would have satisfied — it checked that a name existed,
    not that the vocabulary matched. It now compares the enum against the
    document itself, so adding a twelfth type to either side turns the suite
    red until both agree.
    """
    from framework.artifacts.relationships import RelationshipType

    documented = relationship_types_in_document()

    assert len(documented) == 11
    assert {member.value for member in RelationshipType} == documented


@pytest.mark.xfail(strict=True, reason="HANDOFF: Document Metadata Standard Declared, Never Applied")
def test_every_document_carries_the_metadata_block():
    """`docs/DocumentStandard.md` requires a metadata block on every document,
    and states the reason: so tooling can index them without parsing prose.

    `scripts/status.py` parses prose with regular expressions because this is open.

    **Strengthened 2026-07-31. It asserted `text.startswith("---")` and nothing
    about the contents.** Prepending `---` to all hundred documents would have
    turned it green with the standard still unimplemented. Worse, the standard's
    own note says the single document carrying a block "uses `owner:` where this
    standard says `author:` and omits five required fields" — so that document
    already satisfied the old test while failing the standard, which is the exact
    shape of a watcher that lies.

    It also parsed nothing from `DocumentStandard.md`, so it could not notice the
    standard changing. The standard states its requirement by example rather than
    as a list, so the example is parsed as the specification: twelve top-level
    keys.

    Verified against the one document that has a block —
    `strategies/StrategyTemplate.md` is reported missing `author`, `evidence`,
    `regime`, `relationships`, `tags` and `type`, which is `owner:` for `author:`
    plus the five omissions the standard describes. The document's own claim was
    checked by opening it, not taken on trust.
    """
    required = required_metadata_fields()
    assert len(required) == 12, f"expected twelve keys, parsed {sorted(required)}"

    skip = {".pytest_cache", "reports", ".git"}
    documents = [
        p
        for p in REPO.rglob("*.md")
        if not skip & set(p.relative_to(REPO).parts)
    ]
    assert documents, "no documents found at all"

    nonconformant = []
    for path in documents:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(REPO).as_posix()
        if not text.startswith("---"):
            nonconformant.append(f"{relative}: no metadata block")
            continue
        missing = required - metadata_keys_in(text)
        if missing:
            nonconformant.append(f"{relative}: missing {', '.join(sorted(missing))}")

    assert not nonconformant, (
        f"{len(nonconformant)} of {len(documents)} documents do not conform: "
        + "; ".join(nonconformant[:3])
        + (" ..." if len(nonconformant) > 3 else "")
    )


# --------------------------------------------------- F-034: a complete stage's ADR claims
#
# `reports/review/2026-09-25-review.md` (F-034), proposing the durable fix that
# `reports/review/2026-08-21-review.md` had already proposed a month earlier and
# that was never built: "a conformance test that fails when a `Stage N — …
# (complete)` heading disagrees with the ADR status it cites".
#
# The defect it is written against: `docs/ROADMAP.md`'s Stage 2 section said
# "**ADR-014 was accepted 2026-08-02 and is implemented in no part**" while
# `docs/DECISIONS.md`'s ADR-014 Status block read "Accepted and implemented,
# 2026-08-02, in all nine rules." The two sat 35 days apart in the repository,
# and `AGENTS.md` sends every session to read the roadmap.

#: Phrases by which the roadmap asserts that an ADR is NOT implemented. Matched
#: within one sentence of the ADR reference, not document-wide, so a stage may
#: still discuss unimplemented work generally.
_NOT_IMPLEMENTED = re.compile(
    r"implemented in no part|implemented in none|not implemented in any part"
    r"|is not (?:yet )?implemented|unimplemented",
)

_STAGE_HEADING = re.compile(r"^## Stage \d+ .*$", re.MULTILINE)
_ADR_REFERENCE = re.compile(r"ADR-(\d{3})")


def _complete_stage_sections() -> list[tuple[str, str]]:
    """Return (heading, body) for each `## Stage N — … (complete)` section."""
    text = (REPO / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
    headings = list(_STAGE_HEADING.finditer(text))
    sections = []
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        heading = match.group(0)
        if "(complete)" in heading.lower():
            sections.append((heading.strip(), text[match.end() : end]))
    return sections


def _adr_status_blocks() -> dict[str, str]:
    """Return {ADR number: its Status block text} from `docs/DECISIONS.md`."""
    text = (REPO / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
    headings = list(re.finditer(r"^## ADR-(\d{3}).*$", text, re.MULTILINE))
    blocks = {}
    for index, match in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        body = text[match.end() : end]
        if status := re.search(r"^Status:\s*\n(.*?)(?:\n\n|\Z)", body, re.DOTALL | re.MULTILINE):
            blocks[match.group(1)] = status.group(1).lower()
    return blocks


def test_a_complete_stage_does_not_call_an_implemented_adr_unimplemented():
    """A `(complete)` stage may not contradict the ADR status it cites.

    Sentence-scoped on purpose: a complete stage is entitled to say that some
    *other* work is unimplemented. What it may not do is name an ADR and, in the
    same sentence, deny an implementation `docs/DECISIONS.md` records.

    **Known limit: this cannot tell a quotation from a claim.** A correction note
    that quotes the wording it is correcting will fail this test. The convention is
    to describe the old wording instead — the same move `scripts/review_due.py`
    asks for with the bracketed `F-[NNN]` form. Tightening this to parse quoting
    was judged not worth the fragility; the workaround is one sentence.
    """
    statuses = _adr_status_blocks()
    assert statuses, "no ADR Status blocks parsed out of docs/DECISIONS.md"

    contradictions = []
    for heading, body in _complete_stage_sections():
        for sentence in re.split(r"(?<=[.!?])\s+", body):
            flat = " ".join(sentence.split())
            if not _NOT_IMPLEMENTED.search(flat.lower()):
                continue
            for number in _ADR_REFERENCE.findall(flat):
                status = statuses.get(number, "")
                if "implemented" in status and "not implemented" not in status:
                    contradictions.append(
                        f"{heading}: says ADR-{number} is unimplemented "
                        f"({flat[:110]!r}), but its Status block reads "
                        f"{status.strip()[:110]!r}"
                    )

    assert not contradictions, "docs/ROADMAP.md contradicts an ADR status:\n" + "\n".join(
        contradictions
    )
