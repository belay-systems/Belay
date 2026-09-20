from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime

from framework.artifacts.enums import EvidenceLevel
from framework.artifacts.primitives import canonical_digest, utc_now


@dataclass(frozen=True, slots=True)
class EvidenceRecord:
    source: str
    methodology: str
    level: EvidenceLevel
    confidence: float
    provenance: str
    timestamp: datetime
    hash: str

    @classmethod
    def create(
        cls,
        source: str,
        methodology: str,
        level: EvidenceLevel,
        confidence: float,
        provenance: str,
        timestamp: datetime | None = None,
    ) -> "EvidenceRecord":
        timestamp = timestamp or utc_now()

        # A naive timestamp carries no timezone, so nothing in it says which
        # clock produced it. It is rejected rather than assumed to be UTC:
        # this value goes straight into the evidence hash, and evidence whose
        # meaning depends on an assumption is not reproducible.
        if timestamp.tzinfo is None:
            raise ValueError(
                "evidence timestamp must be timezone-aware; "
                "pass datetime.now(timezone.utc) rather than a naive datetime"
            )

        # constitution/Operational_Constraints.md: "Belay shall communicate
        # uncertainty explicitly. Confidence is probabilistic. Never absolute."
        # A confidence of 42.0 or -3.0 was previously accepted and stored.
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                f"confidence must be a probability between 0 and 1, got {confidence}"
            )

        record = cls(
            source=source,
            methodology=methodology,
            level=level,
            confidence=confidence,
            provenance=provenance,
            timestamp=timestamp,
            hash="",
        )

        return replace(record, hash=canonical_digest(record.canonical_payload()))

    def canonical_payload(self) -> dict:
        """Return the fields this record's hash covers.

        `hash` is excluded: a fingerprint cannot cover itself. Mirrors
        `ArtifactIntegrity.canonical_payload` on the artifact side.
        """
        return {
            "source": self.source,
            "methodology": self.methodology,
            "level": self.level.value,
            "confidence": self.confidence,
            "provenance": self.provenance,
            "timestamp": self.timestamp.isoformat(),
        }

    def verify(self) -> bool:
        """Return True if this record's hash still matches its own contents.

        The counterpart to `ArtifactIntegrity.verify_hash`. Without it a forged
        evidence hash is undetectable — the validator only checks that the hash
        field is non-empty, not that it is correct.
        """
        return bool(self.hash) and canonical_digest(self.canonical_payload()) == self.hash
