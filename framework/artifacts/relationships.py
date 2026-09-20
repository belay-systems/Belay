"""The eleven relationship types, and the edge that carries one.

`Knowledge/Relationships.md` names eleven types and states no rule about
direction, inverses, or which artifact types may participate — so none is
invented here. The document is implemented, not extended.

Until 2026-07-30 the vocabulary existed only in that document. `relationship`
was a bare `str`, so `"Superseded By"`, `"superseded_by"` and `"banana"` were
equally legal. The document closes with "Relationships create intelligence",
and an unconstrained string cannot: two artifacts joined by `"supports"` and
`"Supports"` do not connect to each other.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RelationshipType(Enum):
    """The eleven types in `Knowledge/Relationships.md`, lines 9-29.

    Values carry the document's own spelling and capitalisation, so a stored
    relationship reads as the governing document writes it. The conformance
    suite parses that document and asserts this enum matches it exactly, which
    is what stops the two drifting apart again.
    """

    CREATED_FROM = "Created From"
    SUPPORTS = "Supports"
    CONTRADICTS = "Contradicts"
    REPLACES = "Replaces"
    DEPENDS_ON = "Depends On"
    DERIVED_FROM = "Derived From"
    VALIDATED_BY = "Validated By"
    REJECTED_BY = "Rejected By"
    ARCHIVED_WITH = "Archived With"
    REFERENCED_BY = "Referenced By"
    SUPERSEDED_BY = "Superseded By"


# The legal vocabulary as stored on `Artifact.relationships`, whose keys are
# strings. Built from the enum so there is one source of truth rather than a
# list that has to be kept in step with it.
RELATIONSHIP_TYPES = frozenset(member.value for member in RelationshipType)


@dataclass(frozen=True, slots=True)
class Relationship:
    """One directed edge between two artifacts.

    Frozen, like every other model in the framework. It was the only unfrozen
    dataclass in `framework/`, which meant an edge could be repointed after
    construction while the artifact describing it kept the integrity hash
    computed before the change.
    """

    source: str
    target: str
    relationship: RelationshipType
