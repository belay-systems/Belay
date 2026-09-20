"""Survivorship, in two halves, refused when unstated. ADR-013 rules 5 and 9.

**The bias.** A dataset containing only the instruments that still exist has
already removed everything that failed. A strategy tested on it is being tested
on a sample selected, with hindsight, for having survived.

**Its direction is the part usually left out, and it runs both ways at once.**
The winners are all present and the failures are all missing, so returns rise
and the worst case never appears. `SURVIVORSHIP_DIRECTION` below is the fixed
statement of that, in the shape ADR-012 rule 7 established and
`framework/metrics/statistics.py` worked out: a module constant with no
parameter to override it. If it were caller-supplied it could be replaced with
"None." by whoever found it inconvenient, and the artifact would still satisfy
ADR-011 rule 9's non-blank check.

**Two questions, and a source can pass one and fail the other.** Delisted
*prices* and delisted *universe membership* are different capabilities.
`constitution/Operational_Constraints.md:29` — "Tradable universes must be
discovered through evidence" — makes the second constitutional rather than
departmental: a universe drawn from a survivor-only source was selected on the
outcome under prediction, so it was not discovered through evidence in the sense
that line means. `Research/UniverseDiscovery.md:25` requires Belay to "Evaluate
survivability", which cannot be done honestly from a dataset that has already
removed everything which failed to survive.

**Rule 9.** A source that cannot state these properties is refused rather than
assumed clean. `UNKNOWN` is a legitimate answer; silence is not, which is why
both halves are required arguments with no defaults.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Retention(str, Enum):
    """How a source answers one half of the survivorship question.

    An enum rather than a free string for the reason ADR-010 rule 3 gives for
    `DeliverableType`: free text re-opens the hole where a value nothing
    constrains passes silently. "probably fine" is not an answer.
    """

    # The source returns history for instruments that no longer trade, or knows
    # membership as at a past date. Established, not assumed.
    RETAINED = "Retained"

    # The source carries only what still exists. This is the biased case.
    SURVIVORS_ONLY = "Survivors only"

    # Reconstructable but incomplete — the answer exists for part of the range,
    # or can be approximated from something that was not designed to provide it.
    # ADR-013 rule 6 calls this survivorship-*reduced* rather than
    # survivorship-free, and treats it as a legitimate answer rather than a
    # failure.
    PARTIAL = "Partial"

    # Nobody has established it. Legal under rule 9, and must be stated as such
    # rather than left to read as clean.
    UNKNOWN = "Unknown"


# ADR-013 rule 5, in ADR-012 rule 7's shape. Fixed, with no parameter to
# override it.
#
# The direction is worse than the usual single-sided case and the wording says
# so: it does not merely make results noisier, it moves the return and the risk
# in opposite directions at the same time, so a reviewer checking only one of
# them sees nothing wrong.
SURVIVORSHIP_DIRECTION = (
    "Survivorship bias INFLATES every return measure and DEFLATES drawdown and "
    "tail measures SIMULTANEOUSLY, because the instruments that failed have "
    "already been removed from the sample. It flatters the return and "
    "understates the risk in one breath, so a result that looks acceptable on "
    "both axes may be unacceptable on both. It cannot be corrected from the "
    "data itself; ADR-012 rule 10 refuses to produce a number that looks "
    "adjusted and is not, so it is disclosed instead. ADR-013 rule 5."
)

_HALF_LABELS = {
    "delisted_prices": "delisted prices",
    "delisted_universe_membership": "delisted universe membership",
}


@dataclass(frozen=True, slots=True)
class SurvivorshipDisclosure:
    """What a source can and cannot say about instruments that no longer exist.

    Frozen, like every record under `framework/`. This travels into an
    artifact's `known_limitations` and the artifact is signed over it; a mutable
    disclosure would let the caveat behind a published number be rewritten
    underneath it.
    """

    # Can the source return a history for an instrument that no longer trades,
    # if you already know to ask for it?
    delisted_prices: Retention

    # Does the source know which instruments were in a universe *on a past
    # date*, as opposed to which are in it today? This is the half that causes
    # the damage, because Belay is universe-driven by design.
    delisted_universe_membership: Retention

    # How the two answers above were established. `Retained` with no basis is an
    # assertion, and `constitution/Operational_Constraints.md:9-17` distinguishes
    # Facts from Assumptions precisely so the two cannot be filed under one name.
    basis: str

    def __post_init__(self) -> None:
        for name in _HALF_LABELS:
            value = getattr(self, name)
            if not isinstance(value, Retention):
                raise TypeError(
                    f"{name} must be a Retention, got {type(value).__name__}. "
                    "ADR-013 rule 9: a source that cannot state its "
                    "survivorship properties is refused, not assumed clean, and "
                    "a free-text answer is not a statement of one."
                )

        if not isinstance(self.basis, str) or not self.basis.strip():
            raise ValueError(
                "basis must record how the survivorship answers were "
                "established and cannot be blank. An answer with no basis is an "
                "assumption filed as a fact."
            )

    @property
    def is_clean(self) -> bool:
        """Whether both halves are `RETAINED`.

        `UNKNOWN` is deliberately not clean. A source whose properties nobody
        established may be survivor-only, and treating unestablished as
        unbiased is the failure rule 9 exists to prevent — it fails in the
        direction that flatters.
        """
        return all(
            getattr(self, name) is Retention.RETAINED for name in _HALF_LABELS
        )

    def known_limitations(self) -> str:
        """Return the survivorship caveat this source forces onto every artifact.

        Takes no arguments, and that is the mechanism of ADR-012 rule 7 rather
        than an oversight: there is no override parameter because a caller who
        could pass one could suppress the caveat.

        A clean source does not receive the direction warning. A warning printed
        regardless of what was established would stop distinguishing the sources
        it is there to distinguish.
        """
        stated = ", ".join(
            f"{label}: {getattr(self, name).value}"
            for name, label in _HALF_LABELS.items()
        )
        established = f"Survivorship established as — {stated}. Basis: {self.basis}"

        if self.is_clean:
            return established

        return f"{established} {SURVIVORSHIP_DIRECTION}"
