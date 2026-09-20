"""Rendering an Artifact to YAML and reading one back.

`load()` did not exist until 2026-07-31. The repository could write an artifact
and never read it, so `latest()` could only ever return a version *string* — it
had no way to hand back the artifact itself. ADR-009 rule 9 ruled that this had
to close, because a decision record that cannot be read back cannot inform the
next review, which is most of why it exists.

**The contract is the round trip through integrity, not through equality.** An
artifact that comes back with every field looking right but hashing differently
has lost its signature silently, and silence is the failure mode this repository
has been bitten by three times. `tests/artifacts/test_serializer_round_trip.py`
asserts `verify_hash` after a round trip, not field equality.

Loading is not signing. An artifact read from disk keeps the hash it was stored
with. Re-signing on load would hand every tampered file a fresh valid signature
and switch tamper detection off — the same reasoning that keeps signing out of
`Artifact.__init__`.
"""

from dataclasses import asdict, fields
from datetime import datetime
from enum import Enum

import yaml

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import (
    ArtifactLifecycle,
    ArtifactType,
    DeliverableType,
    EvidenceLevel,
    StrategyLifecycle,
)
from framework.artifacts.evidence import EvidenceRecord

# Fields that hold an enum, and the enum each one holds. `load` reconstructs
# these rather than leaving the stored strings in place: `canonical_payload`
# reads `.value` off them, so a bare string breaks the signature check with an
# AttributeError rather than a mismatch, and a promotion gate comparing
# `artifact.strategy_stage is StrategyLifecycle.PRODUCTION` would silently be
# False for every loaded artifact.
_ENUM_FIELDS = {
    "type": ArtifactType,
    "lifecycle": ArtifactLifecycle,
    "strategy_stage": StrategyLifecycle,
    "evidence_level": EvidenceLevel,
    "deliverable": DeliverableType,
}

_DATETIME_FIELDS = ("created", "updated")

# Fields declared as a tuple of (key, value) pairs. YAML has no tuple, so these
# come back as lists of lists and have to be re-tupled — `Artifact` is frozen
# precisely so its contents cannot be edited after signing, and a list would
# make the payload mutable again.
_PAIR_FIELDS = ("metadata", "content")


class ArtifactSerializer:

    def _normalize(self, value):
        if isinstance(value, Enum):
            return value.value
        # Rendered explicitly rather than left to PyYAML's native timestamp type.
        #
        # Checked rather than assumed: on the installed PyYAML a `+05:00`
        # timestamp does round-trip to an identical isoformat, so this is not
        # fixing a live bug. It is removing a dependency. `canonical_payload`
        # hashes `created.isoformat()`, so the exact rendering of a timestamp is
        # signature-critical, and PyYAML's timestamp construction is a library
        # behaviour Belay does not control and has not pinned — older versions
        # returned naive UTC, which would change the isoformat and silently
        # invalidate every signature. `canonical_digest`'s own docstring already
        # asks callers to pass "a timestamp as `.isoformat()`"; this applies the
        # same convention on the way to disk.
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, tuple):
            return [self._normalize(item) for item in value]
        if isinstance(value, dict):
            return {key: self._normalize(val) for key, val in value.items()}
        if hasattr(value, "__dataclass_fields__"):
            return self._normalize(asdict(value))
        return value

    def dump(self, artifact):
        return yaml.safe_dump(
            self._normalize(artifact),
            sort_keys=False,
        )

    def load(self, text: str) -> Artifact:
        """Return the Artifact stored in `text`.

        Unknown keys are ignored and absent keys fall back to the dataclass
        default, so a file written by an older schema still loads. The reverse —
        a field this loader forgets — would silently drop data, which is why
        `test_the_loader_restores_every_field_the_artifact_declares` pins the
        result against `dataclasses.fields(Artifact)` rather than a list written
        out by hand.
        """
        raw = yaml.safe_load(text) or {}

        known = {field.name for field in fields(Artifact)}
        values = {key: value for key, value in raw.items() if key in known}

        for name, enum in _ENUM_FIELDS.items():
            if values.get(name) is not None:
                values[name] = enum(values[name])

        for name in _DATETIME_FIELDS:
            if values.get(name) is not None:
                values[name] = _to_datetime(values[name])

        for name in _PAIR_FIELDS:
            if values.get(name) is not None:
                values[name] = tuple(tuple(pair) for pair in values[name])

        if values.get("tags") is not None:
            values["tags"] = tuple(values["tags"])

        if values.get("relationships") is not None:
            values["relationships"] = tuple(
                (relationship, tuple(targets))
                for relationship, targets in values["relationships"]
            )

        if values.get("evidence") is not None:
            values["evidence"] = tuple(
                _to_evidence(record) for record in values["evidence"]
            )

        return Artifact(**values)


def _to_datetime(value) -> datetime:
    """Return `value` as a timezone-aware datetime.

    A naive timestamp is not reproducible evidence: nothing in it says which
    clock produced it, which is why `utc_now()` exists and why `EvidenceRecord`
    rejects naive timestamps outright. Anything stored without an offset is
    refused here rather than assumed to be UTC — assuming would produce a
    working-looking artifact whose signature silently no longer covers its own
    timestamp.
    """
    moment = value if isinstance(value, datetime) else datetime.fromisoformat(value)
    if moment.tzinfo is None:
        raise ValueError(
            f"stored timestamp {value!r} carries no timezone; nothing in it says "
            "which clock produced it, and the integrity hash covers its isoformat"
        )
    return moment


def _to_evidence(record: dict) -> EvidenceRecord:
    """Rebuild an EvidenceRecord from its stored mapping.

    Constructed directly rather than through `EvidenceRecord.create`, which
    would recompute the hash. The stored hash is the evidence, and recomputing
    it would make a tampered record verify — the same reason loading an artifact
    does not re-sign it. `record.verify()` is what says whether it survived.
    """
    return EvidenceRecord(
        source=record["source"],
        methodology=record["methodology"],
        level=EvidenceLevel(record["level"]),
        confidence=record["confidence"],
        provenance=record["provenance"],
        timestamp=_to_datetime(record["timestamp"]),
        hash=record["hash"],
    )
