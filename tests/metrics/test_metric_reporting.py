"""The metric artifact and its mandatory disclosures. ADR-011 rules 2, 9 and 12.

`Validation/Backtesting.md:35-43` states that backtests must document four
things: Assumptions, Data Source, Sample Period, Known Limitations. Until now
nothing in Belay recorded three of the four, and `docs/HANDOFF.md:1287` believed
`EvidenceRecord` had fields for them — it does not, and `docs/ROADMAP.md:107`
says so correctly.

This is the helper that makes the requirement executable. Its job is not to
compute anything; it is to refuse to emit a number that does not say where it
came from, what was assumed to get it, over what period, and what it cannot be
trusted to mean. `Validation/Backtesting.md:47`: "Outputs become evidence."
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from datetime import date, datetime, timezone

import pytest

from framework.artifacts.enums import ArtifactType, DeliverableType, EvidenceLevel
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.validator import ArtifactValidator
from framework.metrics.reporting import Disclosure, SamplePeriod, metric_artifact

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)

DISCLOSURE = Disclosure(
    assumptions="No transaction costs, no slippage, no financing charges.",
    data_source="unit test fixture, supplied by hand",
    # ADR-013 rule 7: two dates, not prose. Five consecutive trading days.
    sample_period=SamplePeriod(start=date(2024, 1, 2), end=date(2024, 1, 8)),
    known_limitations="The series carries no provenance and describes no real instrument.",
)

PARAMETERS = (("risk_free_rate", 0.04), ("periods_per_year", 252))


def _artifact(**overrides):
    fields = {
        "identifier": "RPT-0001",
        "title": "Sharpe ratio, sample series",
        "metric": "sharpe_ratio",
        "value": 6.6,
        "observations": 5,
        "methodology": "annualized mean excess return over annualized volatility",
        "disclosure": DISCLOSURE,
        "parameters": PARAMETERS,
        "timestamp": FIXED_TIME,
    }
    fields.update(overrides)
    return metric_artifact(**fields)


# ------------------------------------------------- the disclosures are required


@pytest.mark.parametrize(
    "field",
    ["assumptions", "data_source", "known_limitations"],
)
@pytest.mark.parametrize("blank", ["", "   ", "\n", "\t "])
def test_a_blank_disclosure_is_refused(field, blank):
    """ADR-011 rule 9, and whitespace does not count as an answer.

    Parametrised across both axes deliberately. A check written for one field
    would leave the others unguarded, and a check for `""` alone would let a
    single space through — which is the shape of compliance that satisfies a
    validator while telling a reviewer nothing.

    `sample_period` left this list when ADR-013 rule 7 made it two dates rather
    than a string: a blank is not one of the ways it can now be wrong, and the
    ways it *can* be are covered by `tests/metrics/test_sample_period.py`.
    """
    with pytest.raises(ValueError, match=field):
        replace(DISCLOSURE, **{field: blank})


def test_a_prose_sample_period_is_refused():
    """ADR-013 rule 7's other half, kept here beside the blank checks so the
    disclosure block's full set of refusals reads in one place."""
    with pytest.raises(TypeError, match="sample_period"):
        replace(DISCLOSURE, sample_period="five consecutive periods, undated")


def test_a_complete_disclosure_is_accepted():
    assert DISCLOSURE.assumptions
    assert DISCLOSURE.data_source
    assert DISCLOSURE.sample_period
    assert DISCLOSURE.known_limitations


def test_a_disclosure_cannot_be_edited_after_the_fact():
    """Frozen for the reason every record in `framework/` is frozen: the artifact
    is signed over these strings, and a mutable disclosure would let the
    assumptions behind a published number be rewritten underneath it."""
    with pytest.raises(FrozenInstanceError):
        DISCLOSURE.assumptions = "actually we did model costs"


# --------------------------------------------------- what the artifact carries


def test_the_artifact_carries_all_four_disclosures_in_content():
    """ADR-011 rule 9: recorded under fixed keys, so a reader knows where to look
    and a test can assert they are there at all."""
    content = dict(_artifact().content)

    assert content["assumptions"] == DISCLOSURE.assumptions
    assert content["data_source"] == DISCLOSURE.data_source
    assert content["sample_period_start"] == DISCLOSURE.sample_period.start.isoformat()
    assert content["sample_period_end"] == DISCLOSURE.sample_period.end.isoformat()
    assert content["known_limitations"] == DISCLOSURE.known_limitations


def test_the_artifact_carries_the_metric_and_its_value():
    content = dict(_artifact().content)

    assert content["metric"] == "sharpe_ratio"
    assert content["value"] == pytest.approx(6.6)
    assert content["observations"] == 5


def test_the_artifact_carries_every_parameter_that_entered_the_computation():
    """ADR-011 rule 2. A Sharpe of 1.4 at a risk-free rate of 0.00 and a Sharpe
    of 1.4 at 0.04 are two different claims about two different strategies, and
    an artifact carrying only the number cannot tell them apart."""
    content = dict(_artifact().content)

    assert content["risk_free_rate"] == pytest.approx(0.04)
    assert content["periods_per_year"] == 252


def test_the_data_source_is_also_the_evidence_source():
    """One input, two renderings, so they cannot disagree.

    `EvidenceRecord.source` already means "where this came from", and rule 9
    requires `Data Source` in the disclosure block. Recording them from a single
    argument keeps rule 9 literal without creating two facts that can drift —
    which is the objection rule 10 raises against putting run-level facts onto
    each evidence record separately.
    """
    artifact = _artifact()

    assert artifact.evidence[0].source == DISCLOSURE.data_source
    assert dict(artifact.content)["data_source"] == DISCLOSURE.data_source


def test_the_artifact_is_a_backtest_report():
    """ADR-011 rule 12, resting on ADR-010.

    Without `deliverable`, a drawdown, a Sharpe and a universe report are three
    indistinguishable `REPORT`s — which is the finding ADR-010 was raised to
    close, and metric artifacts are the case it was built for.
    """
    artifact = _artifact()

    assert artifact.type is ArtifactType.REPORT
    assert artifact.deliverable is DeliverableType.BACKTEST_REPORTS


def test_the_pair_is_storable_rather_than_merely_declared():
    """The `(REPORT, BACKTEST_REPORTS)` pair has to survive the validator, which
    refuses a subtype contradicting its type — ADR-010 rule 9. Asserting the two
    fields separately would not prove the combination is legal."""
    assert ArtifactValidator().validate(_artifact()) is True


def test_the_identifier_prefix_is_one_that_exists():
    """ADR-011 rule 12's other half, and the reason the open `PORTFOLIO`/`FAILURE`
    identifier finding does not bite here: `REPORT` has the `RPT` prefix, so a
    metric artifact can receive an identifier that names what it is."""
    assert _artifact().id.startswith("RPT-")

    with pytest.raises(ValueError, match="Invalid artifact identifier"):
        _artifact(identifier="PORTFOLIO-0001")


def test_a_hand_built_disclosure_is_graded_research():
    """F-033, owner ruling Part 35. **This test asserted Level C until 2026-09-25.**

    Its fixture's own `data_source` reads "unit test fixture, supplied by hand", so
    the test encoded the defect: a number computed over a series nobody fetched was
    graded "historical simulation". The grade now comes from the disclosure's
    provenance, and a hand-built `Disclosure` answers Level D — hypothesis,
    research only — which is what this fixture actually is.
    """
    evidence = _artifact().evidence

    assert len(evidence) == 1
    assert evidence[0].level is EvidenceLevel.RESEARCH
    assert evidence[0].verify() is True


# -------------------------------------------------- the signature covers it all


def test_the_artifact_is_signed_and_verifies():
    artifact = _artifact()

    assert artifact.integrity_hash is not None
    assert ArtifactIntegrity.verify_hash(artifact) is True


def test_rewriting_a_disclosure_breaks_verification():
    """ADR-011 rule 2 is only worth stating if the signature actually enforces it.

    An artifact whose `known_limitations` can be softened after signing is worse
    than one carrying none: it reads as a disclosed, reviewed number while
    saying whatever was most convenient last.
    """
    artifact = _artifact()
    content = dict(artifact.content)
    content["known_limitations"] = "None."

    forged = replace(artifact, content=tuple(content.items()))

    assert ArtifactIntegrity.verify_hash(forged) is False


def test_rewriting_a_parameter_breaks_verification():
    """The same protection for the numbers behind the number. Moving the
    risk-free rate from 0.04 to 0.00 raises a Sharpe without touching it."""
    artifact = _artifact()
    content = dict(artifact.content)
    content["risk_free_rate"] = 0.0

    forged = replace(artifact, content=tuple(content.items()))

    assert ArtifactIntegrity.verify_hash(forged) is False


def test_identical_inputs_produce_an_identical_hash():
    """Reproducibility, with the timestamp pinned. `AGENTS.md` ranks it fourth
    of eight engineering priorities."""
    assert _artifact().integrity_hash == _artifact().integrity_hash


def test_a_different_disclosure_produces_a_different_hash():
    other = _artifact(
        disclosure=replace(DISCLOSURE, assumptions="Costs modelled at 5 basis points.")
    )

    assert other.integrity_hash != _artifact().integrity_hash
