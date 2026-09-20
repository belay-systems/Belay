from __future__ import annotations

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import (
    DELIVERABLE_ARTIFACT_TYPE,
    ArtifactLifecycle,
    ArtifactType,
    DeliverableType,
    StrategyLifecycle,
    strongest_evidence_level,
)
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.relationships import RELATIONSHIP_TYPES


class ArtifactValidator:

    REQUIRED = [
        "id",
        "title",
        "type",
    ]

    # Knowledge/ArtifactLifecycle.md. Editorial progression, terminal at
    # HISTORICAL: "No artifact is deleted. Artifacts become historical evidence."
    ARTIFACT_TRANSITIONS = {
        ArtifactLifecycle.DRAFT: (ArtifactLifecycle.REVIEW,),
        ArtifactLifecycle.REVIEW: (ArtifactLifecycle.APPROVED,),
        ArtifactLifecycle.APPROVED: (ArtifactLifecycle.ACTIVE,),
        ArtifactLifecycle.ACTIVE: (ArtifactLifecycle.ARCHIVED,),
        ArtifactLifecycle.ARCHIVED: (ArtifactLifecycle.HISTORICAL,),
        ArtifactLifecycle.HISTORICAL: (),
    }

    # constitution/Paper_First_Capital_Doctrine.md, with demotion ruled by
    # ADR-004. Each row reads: the forward move, then any demotions, then
    # RETIRED.
    #
    # Forward, one stage at a time — strategies/Lifecycle.md states "Strategies
    # never skip stages", because each stage proves something and a skipped
    # proof cannot be claimed.
    #
    # Backward, any distance in a single move, down to a floor of
    # PAPER_TRADING. Falling proves nothing, so the one-stage constraint does
    # not bind downward: a rung is hard to climb and easy to lose. Below the
    # floor there is no capital privilege left to withdraw, and a strategy whose
    # statistical proof is falsified has not been demoted but refuted — which is
    # retirement with history preserved.
    #
    # RETIRED is reachable from anywhere, because the doctrine places retirement
    # outside the sequence rather than at the end of it.
    #
    # Legality only. This table can rule that a move is possible; it cannot know
    # whether the written justification ADR-004 rule 4 requires was produced, nor
    # trigger the fresh allocation determination rule 4 sequences after it. Both
    # belong wherever review decisions are recorded, which does not exist yet.
    STRATEGY_TRANSITIONS = {
        StrategyLifecycle.IDEA: (StrategyLifecycle.RESEARCH, StrategyLifecycle.RETIRED),
        StrategyLifecycle.RESEARCH: (StrategyLifecycle.VALIDATION, StrategyLifecycle.RETIRED),
        StrategyLifecycle.VALIDATION: (StrategyLifecycle.PAPER_TRADING, StrategyLifecycle.RETIRED),
        StrategyLifecycle.PAPER_TRADING: (StrategyLifecycle.PROMOTION_REVIEW, StrategyLifecycle.RETIRED),
        # Promotion review releases capital into MICRO_CAPITAL, never straight
        # into LIMITED_CAPITAL. The jump would make a strategy's first exposure
        # to real money its largest.
        #
        # Demoting to PAPER_TRADING is not the same as remaining here. This
        # stage means the strategy is a candidate awaiting decision; falling out
        # of it means it is no longer a candidate and must build a fresh record
        # before it is one again.
        StrategyLifecycle.PROMOTION_REVIEW: (
            StrategyLifecycle.MICRO_CAPITAL,
            StrategyLifecycle.PAPER_TRADING,
            StrategyLifecycle.RETIRED,
        ),
        StrategyLifecycle.MICRO_CAPITAL: (
            StrategyLifecycle.LIMITED_CAPITAL,
            StrategyLifecycle.PROMOTION_REVIEW,
            StrategyLifecycle.PAPER_TRADING,
            StrategyLifecycle.RETIRED,
        ),
        StrategyLifecycle.LIMITED_CAPITAL: (
            StrategyLifecycle.PRODUCTION,
            StrategyLifecycle.MICRO_CAPITAL,
            StrategyLifecycle.PROMOTION_REVIEW,
            StrategyLifecycle.PAPER_TRADING,
            StrategyLifecycle.RETIRED,
        ),
        # The two zero-capital destinations are not interchangeable.
        # PROMOTION_REVIEW withdraws the capital but keeps the strategy a
        # candidate, to be re-decided at the next review. PAPER_TRADING does
        # not. A demoted strategy re-earns every stage through the normal gates
        # either way; no fast lane exists, which follows from the forward moves
        # above being left untouched.
        StrategyLifecycle.PRODUCTION: (
            StrategyLifecycle.LIMITED_CAPITAL,
            StrategyLifecycle.MICRO_CAPITAL,
            StrategyLifecycle.PROMOTION_REVIEW,
            StrategyLifecycle.PAPER_TRADING,
            StrategyLifecycle.RETIRED,
        ),
        StrategyLifecycle.RETIRED: (),
    }

    def validate(self, artifact: Artifact) -> bool:
        self._validate_required_fields(artifact)
        self._validate_lifecycle(artifact)
        self._validate_relationships(artifact)
        self._validate_deliverable(artifact)
        self._validate_evidence(artifact)
        self._validate_confidence(artifact)
        self._validate_integrity(artifact)
        return True

    def validate_transition(self, current, target) -> bool:
        """Validate a move within one lifecycle.

        Both arguments must belong to the same lifecycle. Mixing them is
        rejected rather than coerced: an artifact cannot be moved into a capital
        stage, and asking to is a bug rather than an unusual request.
        """
        if type(current) is not type(target):
            raise ValueError(
                f"Cannot transition between different lifecycles: "
                f"{type(current).__name__} -> {type(target).__name__}"
            )

        table = self._table_for(current)
        if target not in table.get(current, ()):
            raise ValueError(f"Invalid lifecycle transition: {current} -> {target}")

        return True

    def _table_for(self, stage) -> dict:
        if isinstance(stage, ArtifactLifecycle):
            return self.ARTIFACT_TRANSITIONS
        if isinstance(stage, StrategyLifecycle):
            return self.STRATEGY_TRANSITIONS
        raise ValueError(f"Not a lifecycle stage: {stage!r}")

    def _validate_required_fields(self, artifact: Artifact) -> None:
        for field in self.REQUIRED:
            if getattr(artifact, field) is None:
                raise ValueError(f"{field} missing.")

    def _validate_lifecycle(self, artifact: Artifact) -> None:
        if not isinstance(artifact.lifecycle, ArtifactLifecycle):
            raise ValueError("Invalid artifact lifecycle.")

        if artifact.strategy_stage is not None and not isinstance(
            artifact.strategy_stage, StrategyLifecycle
        ):
            raise ValueError("Invalid strategy stage.")

        # strategies/Registry.md: "Every strategy exists in exactly one
        # lifecycle stage." A strategy without one is not merely incomplete —
        # it cannot be placed in the promotion pipeline at all.
        if artifact.type is ArtifactType.STRATEGY and artifact.strategy_stage is None:
            raise ValueError(
                "Artifacts of type STRATEGY must carry a strategy_stage; "
                "every strategy exists in exactly one lifecycle stage."
            )

        # The converse: a report has no capital stage, and claiming one would
        # assert something untrue of it.
        if artifact.type is not ArtifactType.STRATEGY and artifact.strategy_stage is not None:
            raise ValueError(
                f"Only STRATEGY artifacts carry a strategy_stage; "
                f"{artifact.type.value} artifacts do not."
            )

    def _validate_relationships(self, artifact: Artifact) -> None:
        # Knowledge/Relationships.md defines eleven types. The field accepted
        # any string, so a typo did not fail — it silently created a twelfth
        # kind of edge that nothing else would ever match. The document's claim
        # that "relationships create intelligence" holds only if both ends of
        # an edge agree on the word.
        for entry in artifact.relationships:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise ValueError(
                    f"Malformed relationship entry {entry!r}: expected "
                    "(relationship_type, (target_id, ...))."
                )

            relationship, _targets = entry
            if relationship not in RELATIONSHIP_TYPES:
                raise ValueError(
                    f"Unknown relationship type {relationship!r}. "
                    "Knowledge/Relationships.md defines: "
                    f"{', '.join(sorted(RELATIONSHIP_TYPES))}."
                )

    def _validate_deliverable(self, artifact: Artifact) -> None:
        # ADR-010 rule 3. This is the check that makes the subtype constrained
        # rather than free text, and it is the whole reason the coarse-plus-
        # subtype shape is safe to adopt: a free string would have made
        # `artifact_type="UniverseReport"` legal rather than fixing it, and that
        # orphaned draft is the defect the finding was raised about.
        #
        # None is legal and means "not a documented deliverable" — most artifacts.
        if artifact.deliverable is None:
            return

        if not isinstance(artifact.deliverable, DeliverableType):
            raise ValueError(
                f"Unknown deliverable {artifact.deliverable!r}. It must be a "
                "DeliverableType, whose members are held to the departmental and "
                "workflow documents by tests/test_governance_conformance.py."
            )

        # ADR-010 rule 9 makes the (type, deliverable) pair meaningful, so a pair
        # that contradicts itself is a defect rather than a harmless extra field.
        # `type` is the coarser of the two and is what a promotion gate reads
        # first, so a universe report declared as a STRATEGY must not stand.
        expected = DELIVERABLE_ARTIFACT_TYPE[artifact.deliverable]
        if artifact.type is not expected:
            raise ValueError(
                f"{artifact.deliverable.value} is an artifact of type "
                f"{expected.value}, not {artifact.type.value}. ADR-010 rule 9."
            )

    def _validate_evidence(self, artifact: Artifact) -> None:
        for evidence in artifact.evidence:
            if not evidence.hash:
                raise ValueError("Evidence hash missing.")

        # ADR-005 rule 5. The grade is derived, so the validator re-derives it
        # and refuses a mismatch — the same factory-computes/validator-verifies
        # split already used for the integrity hash. Without this an artifact
        # built by calling Artifact() directly could claim Level A while
        # carrying nothing but hypotheses, and that claim is what a promotion
        # gate reads.
        expected = strongest_evidence_level(artifact.evidence)
        if artifact.evidence_level != expected:
            raise ValueError(
                f"Evidence level {artifact.evidence_level} does not match the "
                f"artifact's evidence, which supports {expected}. "
                "The grade is the strongest record present and is not settable."
            )

    def _validate_confidence(self, artifact: Artifact) -> None:
        # constitution/Operational_Constraints.md: "Belay shall communicate
        # uncertainty explicitly. Confidence is probabilistic. Never absolute."
        # None is legal and means not yet assessed; a number outside 0-1 is not
        # a probability and says nothing.
        if artifact.confidence is None:
            return

        if not 0.0 <= artifact.confidence <= 1.0:
            raise ValueError(
                f"confidence must be a probability between 0 and 1, "
                f"got {artifact.confidence}"
            )

    def _validate_integrity(self, artifact: Artifact) -> None:
        # An unsigned artifact used to pass here. That made "unsigned" a valid
        # state all the way to a promotion gate: unverifiable content could be
        # consumed as evidence. Absence of a signature is now a failure, not an
        # exemption from checking one.
        if artifact.integrity_hash is None:
            raise ValueError(
                "Artifact is unsigned. Build artifacts through ArtifactFactory, "
                "which signs them, or sign explicitly with ArtifactIntegrity.sign."
            )

        if not ArtifactIntegrity.verify_hash(artifact):
            raise ValueError("Artifact integrity hash mismatch.")
