from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from framework.artifacts.enums import (
    ArtifactLifecycle,
    ArtifactType,
    DeliverableType,
    EvidenceLevel,
    StrategyLifecycle,
)
from framework.artifacts.evidence import EvidenceRecord
from framework.artifacts.primitives import utc_now


@dataclass(frozen=True, slots=True)
class Artifact:
    id: str
    title: str
    type: ArtifactType
    # Editorial state, carried by every artifact. See ADR-003.
    lifecycle: ArtifactLifecycle = ArtifactLifecycle.DRAFT
    # Capital promotion stage. Only artifacts of type STRATEGY carry one; for
    # everything else the question does not apply, and None says so rather than
    # forcing a report to claim a stage it can never occupy.
    strategy_stage: StrategyLifecycle | None = None
    # Which documented deliverable this is, where `type` says only what kind of
    # thing it is. ADR-010: sixteen of the twenty-five documented deliverables are
    # report-shaped and were all indistinguishable `REPORT`s before this existed.
    #
    # None means "not a documented deliverable" — a real state, not an unset
    # field. A strategy specification is not a workflow deliverable and neither is
    # a review record, so most artifacts carry None and never see this.
    deliverable: DeliverableType | None = None
    evidence: tuple[EvidenceRecord, ...] = field(default_factory=tuple)
    # Knowledge/Schema.md requires an artifact-level evidence grade alongside the
    # evidence records themselves. ADR-005 rule 5: the strongest grade present,
    # computed by ArtifactFactory and re-derived by ArtifactValidator, because a
    # hand-set grade is an opinion and the four-class hierarchy exists so that it
    # is not one. None when there is no evidence — an unevidenced artifact has no
    # grade, and inventing D for it would make "unevidenced" read as "hypothesis".
    evidence_level: EvidenceLevel | None = None
    # Required by Knowledge/Schema.md and filtered on by Knowledge/Search.md.
    # Search reads the summary before opening the artifact, so it is load-bearing
    # rather than decorative.
    tags: tuple[str, ...] = field(default_factory=tuple)
    summary: str = ""
    # ADR-005: revising this produces a NEW VERSION, never an in-place edit.
    # Knowledge/Versioning.md forbids overwriting, and the history of an estimate
    # is the evidence trail — a strategy whose confidence fell 0.6 -> 0.3 over
    # four reviews is a different object from one that was always 0.3.
    #
    # None rather than a default figure: 0.5 would be a fabricated estimate that
    # nothing distinguishes from a real one. None means "not yet assessed".
    confidence: float | None = None
    version: str = "1.0.0"
    schema_version: str = "1.0"
    created: datetime = field(default_factory=utc_now)
    updated: datetime = field(default_factory=utc_now)
    author: str = "Belay"
    relationships: tuple[tuple[str, tuple[str, ...]], ...] = field(default_factory=tuple)
    metadata: tuple[tuple[str, Any], ...] = field(default_factory=tuple)
    content: tuple[tuple[str, Any], ...] = field(default_factory=tuple)
    integrity_hash: str | None = None
    parent_hash: str | None = None
