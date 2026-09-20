from enum import Enum


class EvidenceLevel(str, Enum):
    """The four classes of `constitution/Evidence_Standards.md`.

    A live validated, B paper validated, C historical simulation, D hypothesis.
    """

    RESEARCH = "D"
    HISTORICAL = "C"
    PAPER = "B"
    LIVE = "A"


# Strength, weakest first. Declared explicitly rather than read from the members'
# declaration order. `StrategyLifecycle` already demonstrated what position-as-rank
# costs: `RETIRED` sits above `PRODUCTION` positionally while being no rung at all,
# and every ordinal comparison over it reads a retirement as the deepest promotion
# in the system. An explicit table cannot be broken by reordering the members.
EVIDENCE_STRENGTH = {
    EvidenceLevel.RESEARCH: 0,
    EvidenceLevel.HISTORICAL: 1,
    EvidenceLevel.PAPER: 2,
    EvidenceLevel.LIVE: 3,
}


def strongest_evidence_level(records) -> "EvidenceLevel | None":
    """Return the strongest grade among `records`, or None if there are none.

    ADR-005 rule 5. The strongest and not the weakest, because
    `constitution/Evidence_Standards.md` states "Hypotheses do not invalidate
    production evidence" — taking the minimum would let one Level D record drag
    down an artifact carrying Level A, which is that sentence's exact prohibition.

    None for no records: an unevidenced artifact has no grade, and defaulting it
    to D would make "unevidenced" indistinguishable from "hypothesis".
    """
    levels = [record.level for record in records]
    if not levels:
        return None
    return max(levels, key=lambda level: EVIDENCE_STRENGTH[level])


class ArtifactLifecycle(str, Enum):
    """The lifecycle of a document or a unit of evidence.

    From `Knowledge/ArtifactLifecycle.md`. This is what every artifact carries:
    a report, a research memo, a critique, a backtest result. It describes
    editorial state — is this drafted, reviewed, approved, in use, retired to
    the archive — and it never touches capital.

    HISTORICAL is terminal. "No artifact is deleted. Artifacts become
    historical evidence."

    Do not confuse this with `StrategyLifecycle`, which governs a different
    subject. See ADR-003 in docs/DECISIONS.md.
    """

    DRAFT = "Draft"
    REVIEW = "Review"
    APPROVED = "Approved"
    ACTIVE = "Active"
    ARCHIVED = "Archived"
    HISTORICAL = "Historical"


class StrategyLifecycle(str, Enum):
    """The eight stages a strategy passes through to earn capital.

    From `constitution/Paper_First_Capital_Doctrine.md`, which `README.md`
    reproduces exactly. Only artifacts of type STRATEGY carry this.

    MICRO_CAPITAL is the first stage at which real money is committed, at
    minimal exposure, to prove the machinery works at all. LIMITED_CAPITAL then
    proves it survives a larger allocation. They are separate stages because
    they answer different questions, and skipping the smaller one would make a
    strategy's first contact with real capital also its largest.

    RETIRED is not a stage of maturity. The doctrine places retirement outside
    the sequence, reachable from anywhere.
    """

    IDEA = "Idea"
    RESEARCH = "Research"
    VALIDATION = "Validation"
    PAPER_TRADING = "Paper Trading"
    PROMOTION_REVIEW = "Promotion Review"
    MICRO_CAPITAL = "Micro Capital"
    LIMITED_CAPITAL = "Limited Capital"
    PRODUCTION = "Production"
    RETIRED = "Retired"


# The maturity ladder: the eight doctrine stages in order, RETIRED removed.
#
# RETIRED is declared last in StrategyLifecycle — index 8, above PRODUCTION at 7
# — but the doctrine places retirement outside the sequence, reachable from
# anywhere. Comparing positions over list(StrategyLifecycle) therefore reads
# every retirement as the deepest promotion in the system.
#
# ADR-004 warned that this trap "becomes live the moment this helper is
# written". It is now live: ADR-009 rule 5 compares ladder positions to check a
# review's declared outcome against its declared stage change. Anything
# comparing stage order must use this, and must classify RETIRED before it.
STRATEGY_LADDER = tuple(
    stage for stage in StrategyLifecycle if stage is not StrategyLifecycle.RETIRED
)


class ReviewOutcome(str, Enum):
    """The four outcomes a strategy review may produce. ADR-009 rule 3.

    Three documents list these and no two listed them identically:
    `strategies/ReviewTemplate.md:47-55`, `Validation/CapitalReview.md:29-39`
    and `workflows/Monthly/StrategyPromotion.md:27-35`. ADR-008 rule 3 ruled
    `Remain Current Stage` canonical — two of the three use it, and it is
    unambiguous where bare `Remain` is not.

    **`Reject` is not a fifth member.** ADR-008 rule 4 rules it the
    decision-side name for the event whose state-side name is
    `REMAIN_CURRENT_STAGE`. `CapitalReview.md` is the only document listing
    both, and its own lines 7 and 9 explain why: it "does not allocate capital"
    but "recommends promotion", so it processes a *request* and names both the
    decision on the request and its effect on the strategy. Rejecting a
    promotion leaves the strategy where it is. One event with two names must not
    become two members.

    REMAIN_CURRENT_STAGE is the whole reason this enum exists. Until it could be
    recorded, a review that decided to hold a strategy was indistinguishable
    from no review having happened.
    """

    PROMOTE = "Promote"
    REMAIN_CURRENT_STAGE = "Remain Current Stage"
    DEMOTE = "Demote"
    RETIRE = "Retire"


class ConfidenceAdjustment(str, Enum):
    """`strategies/ReviewTemplate.md:37-43`. A decision the review makes.

    Recorded with no default, because a default would be a fabricated decision —
    the same objection ADR-005 rule 4 raised against defaulting confidence
    itself to 0.5, where the invented figure is indistinguishable from a real
    one.

    This records the *direction* only. ADR-005 rules that a confidence revision
    produces a new version of the subject artifact, and deciding to adjust is a
    separate act from producing that version.
    """

    INCREASE = "Increase"
    DECREASE = "Decrease"
    NO_CHANGE = "No Change"


class ArtifactType(str, Enum):
    """What kind of thing an artifact is. Coarse by ruling — ADR-010 rule 1.

    This does not name the specific documented deliverable; `DeliverableType`
    does. The two answer different questions and an artifact carries both.
    """

    REPORT = "Report"
    STRATEGY = "Strategy"
    EXPERIMENT = "Experiment"
    REVIEW = "Review"
    RESEARCH = "Research"
    REGIME = "Regime"
    PORTFOLIO = "Portfolio"
    WORKFLOW = "Workflow"
    FAILURE = "Failure"


class DeliverableType(str, Enum):
    """The documented outputs of the departments and workflows. ADR-010 rule 2.

    Twenty-four, counted rather than estimated. Eleven documents declare
    deliverables under an explicit `Output`, `Outputs`, `Deliverable` or
    `Deliverables` heading — 34 entries, 25 distinct, less `Knowledge Update`
    which rule 5 rules an effect rather than an artifact.

    **Spelled as the documents spell them, plurals included.** `Backtest Reports`
    keeps its plural because no document writes the singular, while `Universe
    Report` is singular because `Research/UniverseDiscovery.md` writes it that
    way. ADR-006 set this precedent when it reconciled the criteria lists:
    casing and house style were left alone because the ruling was about which
    word, not how to write it. `tests/test_governance_conformance.py` parses the
    eleven documents and holds this enum to them, so a deliverable added to a
    departmental document without a member here turns the suite red.

    **This is an enum and not a free string on purpose.** ADR-010 rule 3. A
    free-text subtype would re-open the exact hole the finding was raised about,
    where an orphaned draft passed `artifact_type="UniverseReport"` and nothing
    refused it.

    Four deliverables named only in prose are **not** here — `Portfolio
    Snapshot`, `Exception Report`, `Portfolio Summary` and `Historical Summary`.
    Rule 4 scopes the vocabulary to what the eleven documents *declare*, and
    promoting a phrase from a task list to a governed name is a ruling nobody has
    made. Recorded in `docs/HANDOFF.md` rather than quietly included.
    """

    # Research and knowledge production.
    UNIVERSE_REPORT = "Universe Report"
    REGIME_REPORT = "Regime Report"
    RESEARCH_MEMO = "Research Memo"
    RESEARCH_PROPOSAL = "Research Proposal"
    RESEARCH_DIGEST = "Research Digest"
    EXPERIMENT_PROPOSALS = "Experiment Proposals"
    EXPERIMENT_QUEUE = "Experiment Queue"
    LITERATURE_REVIEW = "Literature Review"
    CHIEF_SCIENTIST_REPORT = "Chief Scientist Report"

    # Validation.
    CRITIQUE_REPORT = "Critique Report"
    BACKTEST_REPORTS = "Backtest Reports"
    VALIDATION_REPORTS = "Validation Reports"
    PROMOTION_RECOMMENDATIONS = "Promotion Recommendations"
    FAILURE_INVESTIGATIONS = "Failure Investigations"

    # Operations.
    PAPER_TRADE_LOGS = "Paper Trade Logs"
    PERFORMANCE_REPORT = "Performance Report"
    PROMOTION_REVIEWS = "Promotion Reviews"
    OPERATIONAL_REPORTS = "Operational Reports"

    # Workflow outputs.
    MARKET_SNAPSHOT = "Market Snapshot"
    PORTFOLIO_HEALTH_REPORT = "Portfolio Health Report"
    DEVIATION_REPORT = "Deviation Report"
    DAILY_SUMMARY = "Daily Summary"
    INVESTMENT_COMMITTEE_MINUTES = "Investment Committee Minutes"
    RECOMMENDATIONS = "Recommendations"


# ADR-010 rule 9: every documented deliverable resolves to a
# (ArtifactType, DeliverableType) pair. This is that resolution, and the ADR
# deferred it to implementation deliberately — "where each choice can be tested
# rather than asserted in prose".
#
# What can be tested is that the mapping is total and closed, which
# `tests/artifacts/test_deliverables.py` asserts. What cannot be tested is
# whether each individual choice is *right*, so the principle is stated here and
# the arguable ones are named rather than buried.
#
# The principle: the type describes what the artifact IS, not who produced it.
# REPORT is the honest answer for a document reporting findings about something
# else, and it covers thirteen of the twenty-four. A specific member is used only
# where the deliverable is that thing rather than a report about it — a Regime
# Report *is* the regime assessment, a Research Memo *is* research.
#
# Four are genuinely arguable and are recorded as such:
#   Universe Report        REPORT vs RESEARCH — Research produces it, but it
#                          reports on the tradable universe rather than being
#                          research in itself.
#   Chief Scientist Report REPORT vs RESEARCH — same tension, resolved the same
#                          way; its head noun is Report.
#   Market Snapshot        REPORT vs PORTFOLIO — it snapshots the market, not the
#                          portfolio, so PORTFOLIO would be wrong for the reason
#                          it is right for Portfolio Health Report.
#   Paper Trade Logs       PORTFOLIO vs REPORT — a trade log is portfolio
#                          activity rather than a document reporting on it.
#
# STRATEGY and WORKFLOW receive nothing, which is correct: a strategy
# specification is not a workflow deliverable, and neither is a workflow.
DELIVERABLE_ARTIFACT_TYPE = {
    DeliverableType.UNIVERSE_REPORT: ArtifactType.REPORT,
    DeliverableType.REGIME_REPORT: ArtifactType.REGIME,
    DeliverableType.RESEARCH_MEMO: ArtifactType.RESEARCH,
    DeliverableType.RESEARCH_PROPOSAL: ArtifactType.RESEARCH,
    DeliverableType.RESEARCH_DIGEST: ArtifactType.RESEARCH,
    DeliverableType.EXPERIMENT_PROPOSALS: ArtifactType.EXPERIMENT,
    DeliverableType.EXPERIMENT_QUEUE: ArtifactType.EXPERIMENT,
    DeliverableType.LITERATURE_REVIEW: ArtifactType.RESEARCH,
    DeliverableType.CHIEF_SCIENTIST_REPORT: ArtifactType.REPORT,
    DeliverableType.CRITIQUE_REPORT: ArtifactType.REPORT,
    DeliverableType.BACKTEST_REPORTS: ArtifactType.REPORT,
    DeliverableType.VALIDATION_REPORTS: ArtifactType.REPORT,
    DeliverableType.PROMOTION_RECOMMENDATIONS: ArtifactType.REPORT,
    DeliverableType.FAILURE_INVESTIGATIONS: ArtifactType.FAILURE,
    DeliverableType.PAPER_TRADE_LOGS: ArtifactType.PORTFOLIO,
    DeliverableType.PERFORMANCE_REPORT: ArtifactType.REPORT,
    DeliverableType.PROMOTION_REVIEWS: ArtifactType.REVIEW,
    DeliverableType.OPERATIONAL_REPORTS: ArtifactType.REPORT,
    DeliverableType.MARKET_SNAPSHOT: ArtifactType.REPORT,
    DeliverableType.PORTFOLIO_HEALTH_REPORT: ArtifactType.PORTFOLIO,
    DeliverableType.DEVIATION_REPORT: ArtifactType.REPORT,
    DeliverableType.DAILY_SUMMARY: ArtifactType.REPORT,
    DeliverableType.INVESTMENT_COMMITTEE_MINUTES: ArtifactType.REPORT,
    DeliverableType.RECOMMENDATIONS: ArtifactType.REPORT,
}
