from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import (
    ArtifactType,
    StrategyLifecycle,
    strongest_evidence_level,
)
from framework.artifacts.integrity import ArtifactIntegrity
from framework.identifiers import validate as validate_identifier


class ArtifactFactory:
    """The sanctioned creation path for Artifacts. Everything it emits is signed.

    Producers in the mechanics layer should build artifacts here rather than
    calling `Artifact(...)` directly, so that signing cannot be forgotten.
    """

    def create(
        self,
        identifier,
        title,
        artifact_type: ArtifactType,
        **kwargs,
    ) -> Artifact:
        if "integrity_hash" in kwargs:
            raise ValueError(
                "integrity_hash is computed by the factory and cannot be supplied; "
                "a caller-provided hash would be a signature nobody checked"
            )

        # Knowledge/Identifiers.md defines the format and the prefixes. Checked
        # here rather than at validation because an identifier is permanent —
        # it is the one field that can never be corrected later.
        validate_identifier(identifier)

        # ADR-005 rule 5: the artifact's evidence grade is derived, never
        # supplied. A caller-provided grade is an assertion nobody checked, in
        # the one place the constitution is most explicit that assertions do not
        # count. Same shape as the integrity_hash refusal above.
        if "evidence_level" in kwargs:
            raise ValueError(
                "evidence_level is derived from the artifact's evidence and "
                "cannot be supplied; it is the strongest grade present."
            )

        # constitution/Paper_First_Capital_Doctrine.md: "Every strategy begins
        # with zero capital. No exceptions." The lifecycle guard was on movement
        # and not on birth — `validate_transition` refuses IDEA -> Micro Capital,
        # but `strategy_stage` arrived here through **kwargs untouched and the
        # validator checked only that it *was* a StrategyLifecycle, never
        # *which*. A strategy signed into existence at PRODUCTION validated True
        # with no VALIDATION artifact and no PAPER_TRADING history behind it,
        # because it never occupied those stages. Same shape as the two refusals
        # above: a caller-provided stage is an assertion nobody checked.
        #
        # Unconditional, because nothing in Belay creates a STRATEGY artifact
        # today. Reconstruction at a later stage is not this path's job —
        # `ArtifactSerializer.load()` builds `Artifact(...)` directly, and the
        # repository verifies the integrity hash on read, so a stage that was
        # earned survives the round trip while a hand-edited one does not.
        stage = kwargs.get("strategy_stage")
        if (
            artifact_type is ArtifactType.STRATEGY
            and stage is not None
            and stage is not StrategyLifecycle.IDEA
        ):
            raise ValueError(
                f"a strategy cannot be created at stage {stage!r}; every "
                "strategy begins at IDEA with zero capital and reaches every "
                "later stage only by climbing it through validate_transition."
            )

        # constitution/Operational_Constraints.md: "Confidence is probabilistic.
        # Never absolute." Bounded here for the same reason EvidenceRecord bounds
        # it — 42.0 was previously accepted and stored on the evidence side.
        confidence = kwargs.get("confidence")
        if confidence is not None and not 0.0 <= confidence <= 1.0:
            raise ValueError(
                f"confidence must be a probability between 0 and 1, got {confidence}"
            )

        artifact = Artifact(
            id=identifier,
            title=title,
            type=artifact_type,
            evidence_level=strongest_evidence_level(kwargs.get("evidence", ())),
            **kwargs,
        )

        # Signed last, so the hash covers the finished artifact.
        return ArtifactIntegrity.sign(artifact)
