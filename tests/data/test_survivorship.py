"""Survivorship, in two halves, refused when unstated. ADR-013 rules 5 and 9.

**What survivorship bias is.** A dataset that contains only the instruments
which still exist has already removed everything that failed. A strategy tested
on it is being tested on companies that were selected, with hindsight, for
having survived — so the test is answering a question nobody asked.

**Its direction is the part that matters, and it is the part usually left out.**
The bias does not merely add noise. It **inflates every return measure and
deflates drawdown and tail measures simultaneously**: the winners are all
present and the failures are all missing, so the average return rises and the
worst case never appears. It flatters the return and understates the risk in one
breath. ADR-012 rule 10 already settled the response to a bias that cannot be
corrected — refuse to produce a number that "looks adjusted and is not", and
disclose instead.

**Two questions, not one, and a source can pass one and fail the other.**

- **Delisted prices** — can the source return a history for an instrument that
  no longer trades, if you already know to ask for it?
- **Delisted universe membership** — does the source know which instruments were
  in a universe *on a past date*, as opposed to which are in it today?

The second is the one that causes the damage, and
`Research/UniverseDiscovery.md` makes Belay universe-driven by design.
`constitution/Operational_Constraints.md:29` — "Tradable universes must be
discovered through evidence" — makes this constitutional rather than
departmental: a universe drawn from a survivor-only source was selected on the
outcome under prediction.

**Rule 9: a source that cannot state its properties is refused, not assumed
clean.** "Unknown" is a legitimate answer and must be *stated* as unknown.
Silence is not an answer. A source silently assumed survivor-free is the failure
this rule set exists to prevent, and it fails in the direction that flatters.
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from framework.data.survivorship import (
    SURVIVORSHIP_DIRECTION,
    Retention,
    SurvivorshipDisclosure,
)

CLEAN = SurvivorshipDisclosure(
    delisted_prices=Retention.RETAINED,
    delisted_universe_membership=Retention.RETAINED,
    basis="Established by querying a delisted ticker and finding its history.",
)

SURVIVOR_ONLY = SurvivorshipDisclosure(
    delisted_prices=Retention.SURVIVORS_ONLY,
    delisted_universe_membership=Retention.PARTIAL,
    basis="COH returns no bars in any window; AAPL returns bars in the same window.",
)


# ------------------------------------------------------ the two halves are two


def test_the_disclosure_answers_both_halves_separately():
    """Not one flag. A source can retain delisted prices and still know nothing
    about historical universe membership, and collapsing the two into one
    boolean loses exactly the half that does the damage."""
    assert SURVIVOR_ONLY.delisted_prices is Retention.SURVIVORS_ONLY
    assert SURVIVOR_ONLY.delisted_universe_membership is Retention.PARTIAL


@pytest.mark.parametrize(
    "half", ["delisted_prices", "delisted_universe_membership"]
)
def test_neither_half_may_be_omitted(half):
    """Rule 9. Silence is not an answer, so both are required arguments and
    neither has a default that could stand in for one."""
    answers = {
        "delisted_prices": Retention.RETAINED,
        "delisted_universe_membership": Retention.RETAINED,
        "basis": "irrelevant",
    }
    del answers[half]

    with pytest.raises(TypeError):
        SurvivorshipDisclosure(**answers)


def test_unknown_is_a_legal_answer():
    """Rule 9 states it explicitly: "Unknown" is legitimate and must be stated
    as unknown. A source whose properties nobody has established is usable, so
    long as the artifact says that is the situation."""
    unknown = SurvivorshipDisclosure(
        delisted_prices=Retention.UNKNOWN,
        delisted_universe_membership=Retention.UNKNOWN,
        basis="Not established; no query was run against this source.",
    )

    assert unknown.delisted_prices is Retention.UNKNOWN


def test_an_answer_outside_the_vocabulary_is_refused():
    """A free string would re-open the hole ADR-010 rule 3 closed for
    deliverables, where `artifact_type="UniverseReport"` was legal because
    nothing constrained it."""
    with pytest.raises((ValueError, TypeError)):
        SurvivorshipDisclosure(
            delisted_prices="probably fine",
            delisted_universe_membership=Retention.RETAINED,
            basis="hand-waved",
        )


def test_the_basis_cannot_be_blank():
    """How the answer was established is part of the answer. `Retained` with no
    basis is an assertion, and `constitution/Operational_Constraints.md:9-17`
    distinguishes Facts from Assumptions precisely so the two cannot be filed
    under one name."""
    with pytest.raises(ValueError, match="basis"):
        SurvivorshipDisclosure(
            delisted_prices=Retention.RETAINED,
            delisted_universe_membership=Retention.RETAINED,
            basis="   ",
        )


def test_a_disclosure_cannot_be_edited_after_the_fact():
    with pytest.raises(FrozenInstanceError):
        SURVIVOR_ONLY.delisted_prices = Retention.RETAINED


# ------------------------------------------- the direction, which is the point


def test_the_direction_constant_names_the_bias_and_which_way_it_runs():
    """ADR-012 rule 7's shape, which `framework/metrics/statistics.py` is the
    worked example of: a fixed module constant, not a caller-supplied string.

    ADR-013 rule 5 is explicit that the direction is worse than the usual
    single-sided case, because it runs both ways at once."""
    direction = SURVIVORSHIP_DIRECTION.lower()

    assert "survivorship" in direction
    assert "inflates" in direction
    assert "deflates" in direction
    assert "simultaneous" in direction


def test_a_biased_source_states_the_direction_in_its_limitations():
    """The disclosure is only worth having if it reaches the artifact carrying
    the direction, rather than a neutral note that a limitation exists."""
    limitations = SURVIVOR_ONLY.known_limitations().lower()

    assert "inflates" in limitations
    assert "deflates" in limitations


def test_the_limitations_say_which_half_failed_and_how_it_was_established():
    """Two halves means the artifact must record which one is the problem. A
    reader who cannot tell whether prices or universe membership is missing
    cannot judge whether a given strategy is affected."""
    limitations = SURVIVOR_ONLY.known_limitations()

    assert "delisted prices" in limitations.lower()
    assert "universe membership" in limitations.lower()
    assert SURVIVOR_ONLY.basis in limitations


def test_an_unknown_source_still_carries_the_direction():
    """Unknown is not clean. A source whose properties were never established
    may be survivor-only, and the artifact must not read as though the question
    was asked and answered favourably."""
    unknown = SurvivorshipDisclosure(
        delisted_prices=Retention.UNKNOWN,
        delisted_universe_membership=Retention.UNKNOWN,
        basis="Not established.",
    )

    assert "inflates" in unknown.known_limitations().lower()


def test_a_clean_source_does_not_claim_a_bias_it_does_not_have():
    """The converse, and the reason this is not just a constant string pasted
    everywhere. A source that genuinely retains both must not carry a warning
    about a bias it does not exhibit, or the warning stops meaning anything."""
    limitations = CLEAN.known_limitations().lower()

    assert "inflates" not in limitations
    assert "retained" in limitations


def test_the_limitations_take_no_arguments_at_all():
    """ADR-012 rule 7's mechanism, not an inconvenience to route around.

    **This asserts the signature, and that is all it asserts.** An earlier
    version was named "cannot be replaced by a caller" and checked only that
    `known_limitations(override=...)` raises `TypeError` — true of every
    zero-argument method, including one returning `""`. The guarantee the name
    claimed lives one layer up and is tested in
    `tests/data/test_survivorship_cannot_be_softened.py`, because fixing the
    constant while letting the caller choose which disclosure object carries it
    achieves the identical suppression.
    """
    import inspect

    assert inspect.signature(
        SurvivorshipDisclosure.known_limitations
    ).parameters.keys() == {"self"}


def test_biased_and_clean_sources_do_not_produce_the_same_limitations():
    """A disclosure that reads identically regardless of what was established is
    not a disclosure."""
    assert CLEAN.known_limitations() != SURVIVOR_ONLY.known_limitations()
