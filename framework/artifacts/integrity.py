from __future__ import annotations

from dataclasses import replace

from framework.artifacts.artifact import Artifact
from framework.artifacts.primitives import canonical_digest


class ArtifactIntegrity:
    """Deterministic artifact integrity calculation and verification."""

    @staticmethod
    def canonical_payload(artifact: Artifact) -> dict:
        """Return the fields the integrity hash covers.

        Everything except `integrity_hash` itself, which cannot cover itself.

        `author`, `created`, `updated` and `parent_hash` were absent until
        2026-07-26. Their absence meant an artifact's authorship and timestamps
        could be rewritten while verification still passed — so the signature
        proved what an artifact said, but not who produced it or when, which is
        most of what an audit trail is for. `constitution/Governance.md` requires
        every artifact to possess identifier, version, author, date and status.

        `parent_hash` matters for the same reason: it binds an artifact to the
        version it superseded, and an unprotected link can be repointed.
        """
        return {
            "id": artifact.id,
            "title": artifact.title,
            "type": artifact.type.value,
            "lifecycle": artifact.lifecycle.value,
            "strategy_stage": (
                artifact.strategy_stage.value if artifact.strategy_stage else None
            ),
            # Added 2026-07-31 with ADR-010 rule 8, for the reason ADR-005 gave
            # for `confidence`: a governance gate reads this to decide whether an
            # artifact is the critique report it is looking for, and a claim a
            # gate reads must be covered by the signature.
            "deliverable": (
                artifact.deliverable.value if artifact.deliverable else None
            ),
            "evidence": [evidence.hash for evidence in artifact.evidence],
            # Added 2026-07-30 with ADR-005. An artifact's evidence grade and
            # confidence are exactly the kind of claim a signature exists to
            # protect: leaving them outside the hash would let a strategy's
            # confidence be raised from 0.3 to 0.9 while verification still
            # returned True. Same reasoning that brought author and dates in.
            "evidence_level": (
                artifact.evidence_level.value if artifact.evidence_level else None
            ),
            "tags": list(artifact.tags),
            "summary": artifact.summary,
            "confidence": artifact.confidence,
            "content": artifact.content,
            "metadata": artifact.metadata,
            "relationships": artifact.relationships,
            "version": artifact.version,
            "schema_version": artifact.schema_version,
            "author": artifact.author,
            "created": artifact.created.isoformat(),
            "updated": artifact.updated.isoformat(),
            "parent_hash": artifact.parent_hash,
        }

    @classmethod
    def calculate_hash(cls, artifact: Artifact) -> str:
        return canonical_digest(cls.canonical_payload(artifact))

    @classmethod
    def sign(cls, artifact: Artifact) -> Artifact:
        """Return a copy of `artifact` carrying its own integrity hash.

        Signing is a deliberate act, not something the Artifact does to itself.
        `Artifact` is a frozen record that keeps whatever hash it is handed —
        if construction signed automatically, `dataclasses.replace()` would
        hand every altered copy a fresh valid signature and tamper detection
        would stop working. `ArtifactFactory` is the sanctioned caller.
        """
        return replace(artifact, integrity_hash=cls.calculate_hash(artifact))

    @classmethod
    def verify_hash(cls, artifact: Artifact) -> bool:
        if artifact.integrity_hash is None:
            return False
        return cls.calculate_hash(artifact) == artifact.integrity_hash
