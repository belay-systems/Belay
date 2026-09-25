"""Turning a computed number into a signed, disclosed Artifact. ADR-011.

`Validation/Backtesting.md:35-43` states that backtests must document four
things — Assumptions, Data Source, Sample Period, Known Limitations — and closes
with "Outputs become evidence. Not guarantees." Until 2026-07-31 nothing in
Belay recorded three of the four. `docs/HANDOFF.md:1287` believed
`EvidenceRecord` had fields for them; it has `source`, `methodology`, `level`,
`confidence`, `provenance`, `timestamp` and `hash`, so `Data Source` was covered
under another name and the other three were not covered at all.
`docs/ROADMAP.md:107` recorded this correctly and was the document to believe.

This module is where the requirement becomes executable. It computes nothing.
Its whole job is to refuse to emit a number that does not say what was assumed
to produce it, where the data came from, over what period, and what it cannot be
trusted to mean.

**Why a shared helper rather than four copies.** ADR-011 rule 9 is enforced in
one place, so a metric added later cannot quietly skip it — and `AGENTS.md`
lists "parallel implementations" among the things to avoid. `drawdown.py` was
migrated onto this on the day the ADR was ratified rather than left as a second
pattern (rule 13).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, fields
from datetime import date, datetime
from typing import Any

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import (
    DELIVERABLE_ARTIFACT_TYPE,
    DeliverableType,
    EvidenceLevel,
)
from framework.artifacts.evidence import EvidenceRecord
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.primitives import utc_now


@dataclass(frozen=True, slots=True)
class SamplePeriod:
    """The window a result covers, as two dates. ADR-013 rule 7.

    `sample_period` was a free-form `str` validated only as non-blank, so "last
    five years" satisfied it. Three things depend on it being machine-readable:

    - **Tax years are calendar-bounded** and the taxable branch is live.
      Deriving a tax year by parsing prose is the defect
      `docs/DocumentStandard.md:42` exists to prevent — "index every document
      deterministically without parsing prose."
    - **Rule 4's versioning must compare coverage** between two fetches of the
      same instrument. Two prose strings cannot be compared.
    - **Reproducibility.** A backtest that cannot state its exact window cannot
      be re-run.

    A `datetime` is refused rather than accepted and truncated. Its isoformat
    carries a time component that would enter the integrity hash and assert a
    precision daily bars do not have. The check is on the exact type because
    `datetime` is a subclass of `date` and would pass `isinstance` unnoticed —
    the same class of silent widening `EvidenceRecord` refuses for naive
    timestamps.
    """

    start: date
    end: date

    def __post_init__(self) -> None:
        for name in ("start", "end"):
            value = getattr(self, name)
            if type(value) is not date:
                raise TypeError(
                    f"{name} must be a datetime.date, got {type(value).__name__}. "
                    "ADR-013 rule 7: a sample period is two dates, not prose — "
                    "'last five years' cannot be compared, re-run, or resolved "
                    "to a tax year."
                )

        if self.end < self.start:
            raise ValueError(
                f"sample period end {self.end.isoformat()} falls before start "
                f"{self.start.isoformat()}; that is not a window, and every "
                "coverage comparison built on it would silently invert."
            )


def _content_pairs(name: str, value: Any) -> tuple[tuple[str, Any], ...]:
    """Return the `content` entries `value` contributes, already encoded.

    `canonical_digest`'s docstring asks callers to pass already-encoded values —
    "a timestamp as `.isoformat()`, an enum as `.value`" — because `str()` of an
    arbitrary object is not a stable representation and `default=str` is only a
    backstop. A `SamplePeriod` placed in `content` unrendered would rely on
    exactly that backstop, so it is rendered here instead.

    Dispatching on the value rather than on a transcribed list of field names
    keeps `Disclosure.__post_init__`'s property: a field added to the disclosure
    is rendered without anyone remembering to extend this.
    """
    if isinstance(value, SamplePeriod):
        return (
            (f"{name}_start", value.start.isoformat()),
            (f"{name}_end", value.end.isoformat()),
        )
    return ((name, value),)


@dataclass(frozen=True, slots=True)
class Disclosure:
    """The four things `Validation/Backtesting.md` requires a backtest to record.

    Field names are the document's names, lower-cased and underscored.
    `tests/test_governance_conformance.py` parses the document and holds this
    class to it, so a fifth requirement added there turns the suite red rather
    than going unrecorded on every artifact Belay emits.

    Frozen, like every record under `framework/`. The artifact is signed over
    these strings, and a mutable disclosure would let the assumptions behind a
    published number be rewritten underneath it — the same reasoning that keeps
    `Artifact` frozen and that made `Relationship` frozen on 2026-07-30.
    """

    assumptions: str
    data_source: str
    # ADR-013 rule 7. Two dates, not prose — see `SamplePeriod`. The field
    # **name** is unchanged and that is forced rather than chosen:
    # `tests/test_governance_conformance.py` parses `Validation/Backtesting.md`
    # and holds these names to the document, so splitting this into
    # `sample_period_start` and `sample_period_end` would turn the suite red
    # against the constitution's validation layer. The rule changes the type.
    sample_period: SamplePeriod
    known_limitations: str

    def __post_init__(self) -> None:
        # Checked over `fields(self)` rather than a transcribed list of four
        # names, so a field added above is validated without anyone remembering
        # to add it here. Whitespace does not count as an answer: "   " would
        # satisfy a truthiness check while telling a reviewer nothing, and a
        # disclosure that technically exists is the failure mode this class was
        # written to prevent.
        for field in fields(self):
            value = getattr(self, field.name)

            # Named explicitly because it is the one field that is not a string,
            # and because the alternative — accepting whatever is not a string —
            # would let prose back in through the door rule 7 just closed.
            if field.name == "sample_period":
                if not isinstance(value, SamplePeriod):
                    raise TypeError(
                        "sample_period must be a SamplePeriod carrying two "
                        f"dates, got {type(value).__name__}. ADR-013 rule 7: "
                        "prose satisfied the old non-blank check while being "
                        "impossible to compare, re-run, or resolve to a tax year."
                    )
                continue

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"{field.name} must be recorded and cannot be blank. "
                    "Validation/Backtesting.md requires every backtest to "
                    "document its assumptions, data source, sample period and "
                    "known limitations; a metric that omits one is a number, "
                    "not evidence."
                )

    @property
    def evidence_level(self) -> EvidenceLevel:
        """The grade a metric computed over this disclosure's series may carry.

        **RESEARCH — Level D — unless the disclosure came from a recorded fetch.**
        Ruled by the owner 2026-09-25 (`docs/OwnerDecisions.md` Part 35, F-033).
        ADR-017 draft: `docs/proposals/ADR-017-grade-from-provenance-DRAFT.md`.

        Before that ruling `metric_artifact` stamped `HISTORICAL` — Level C,
        "historical simulation" — on every artifact it emitted, whatever produced
        the numbers. Eight figures typed at a keyboard with
        `data_source="I made these up"` validated as Level C and signed.
        `constitution/Evidence_Standards.md` defines Level C as historical
        simulation and Level D as "Hypothesis. Research only.", and the
        `references/red-team-checklist.md` B5 item names "C whose support is
        really D" as the thing to look for. That was it, in committed code.

        The grade now comes from provenance rather than from the emitter, and it
        fails in the unflattering direction: the hand-built case — the default,
        the easy path, the one every caller takes today — is Level D.
        `FetchedDisclosure` below is the only thing in Belay that answers Level C,
        and `disclosure_from` is the only thing that builds one.

        **What Level C now costs, since 2026-09-25 (Part 36).** A stored fetch
        record whose bytes are on disk and hash to what the record is signed over.
        `disclosure_from` takes a `Fetch` and checks all of that; it is the only
        thing in Belay that answers Level C.

        The first attempt at this took a source and a series and enforced only
        "came through `disclosure_from`" — and a series is a frozen dataclass any
        caller can build, so eight bars typed into a file with a real source
        yielded Level C carrying that vendor's name. An independent pass found it.
        The remaining limit is narrower and worth stating: a caller can still
        construct a `FetchedDisclosure` directly, which is an explicit, greppable
        claim rather than a by-product of the ordinary path.
        """
        return EvidenceLevel.RESEARCH


@dataclass(frozen=True, slots=True)
class FetchedDisclosure(Disclosure):
    """A `Disclosure` whose series came from a recorded fetch. Level C.

    **Adds no dataclass field, and that is forced rather than tidy.**
    `tests/test_governance_conformance.py` asserts set *equality* between
    `dataclasses.fields(Disclosure)` and the four things
    `Validation/Backtesting.md` requires a backtest to document — a document
    frozen by ADR-002. A fifth field here would turn the constitution's own
    validation conformance red. So the provenance is carried by the type and read
    through the property above, and the signed content of every artifact is
    byte-identical to what it was before this change.

    Built only by `framework.data.fetch_record.disclosure_from`, which takes a
    `Fetch` — the stored bytes and the signed record over them — and reads the
    vendor name, the covered window and the survivorship answer out of that
    record's signed content. There is no argument through which a caller can type
    any of the three.
    """

    @property
    def evidence_level(self) -> EvidenceLevel:
        return EvidenceLevel.HISTORICAL


def metric_artifact(
    identifier: str,
    title: str,
    metric: str,
    value: float,
    observations: int,
    methodology: str,
    disclosure: Disclosure,
    deliverable: DeliverableType = DeliverableType.BACKTEST_REPORTS,
    parameters: Sequence[tuple[str, Any]] = (),
    timestamp: datetime | None = None,
) -> Artifact:
    """Return `value` as a signed Artifact carrying its own evidence.

    `parameters` are the choices that entered the computation — a risk-free
    rate, a target return, a period count. ADR-011 rule 2 puts them in `content`
    because `content` is inside the integrity hash
    (`framework/artifacts/integrity.py:55`): a Sharpe of 1.4 at a 0% risk-free
    rate and a Sharpe of 1.4 at 4% are two different claims, and a signature
    that does not cover the difference lets one be rewritten into the other.

    Pass `timestamp` to make the result byte-for-byte reproducible; it defaults
    to now, which makes each call unique.

    **The evidence grade is read from `disclosure`, not chosen here.** A
    `FetchedDisclosure` yields HISTORICAL (Level C); a hand-built `Disclosure`
    yields RESEARCH (Level D). Until 2026-09-25 this function hardcoded
    HISTORICAL for every caller, and that line was F-033 — eight figures typed at
    a keyboard signed as historical simulation. See `Disclosure.evidence_level`
    and ADR-017's draft; the owner ruled it as `docs/OwnerDecisions.md` Part 35.

    The evidence confidence is 1.0 and expresses certainty in the *arithmetic*,
    not a forward-looking claim about the strategy the series came from.

    The artifact is signed because `ArtifactFactory` signs everything it emits,
    so that is a property of the creation path rather than something each metric
    has to remember.
    """
    timestamp = timestamp or utc_now()

    # `disclosure.data_source` becomes both the evidence source and a content
    # key. One argument, two renderings, so they cannot disagree — which is a
    # different thing from the duplication ADR-011 rule 10 refuses, where the
    # same run-level fact would be entered separately onto several records.
    # `EvidenceRecord.source` already means "where this came from", and rule 9
    # wants all four disclosures findable in one block.
    evidence = EvidenceRecord.create(
        source=disclosure.data_source,
        methodology=methodology,
        # F-033, owner ruling Part 35: the grade comes from the disclosure's
        # provenance, not from this function. Hardcoding it here graded every
        # metric Level C whatever produced the numbers.
        level=disclosure.evidence_level,
        confidence=1.0,
        provenance=f"{observations} observations",
        timestamp=timestamp,
    )

    content = (
        ("metric", metric),
        ("value", value),
        ("observations", observations),
        *(tuple(parameter) for parameter in parameters),
        # ADR-013 rule 7: `sample_period` renders as two encoded dates rather
        # than one object, so the window inside the signature is machine-readable
        # and does not depend on `canonical_digest`'s `default=str` backstop.
        *(
            pair
            for field in fields(disclosure)
            for pair in _content_pairs(field.name, getattr(disclosure, field.name))
        ),
    )

    return ArtifactFactory().create(
        identifier=identifier,
        title=title,
        # Derived from the deliverable rather than hardcoded, so the pair can
        # never contradict itself. `ArtifactValidator` refuses a mismatched pair
        # under ADR-010 rule 9, and computing one side from the other means that
        # refusal can only ever fire on a caller error, never on this function's.
        artifact_type=DELIVERABLE_ARTIFACT_TYPE[deliverable],
        # ADR-011 rule 12, resting on ADR-010. Without this a drawdown, a Sharpe
        # and a universe report are three indistinguishable REPORTs — the exact
        # finding ADR-010 was raised to close, and metric artifacts are the case
        # it was built for. `Backtest Reports` resolves to REPORT, which holds
        # the `RPT` identifier prefix, so the open PORTFOLIO/FAILURE prefix
        # finding does not reach this path.
        #
        # Parameterised on 2026-07-31 for ADR-012 rule 12: a statistical review
        # is a `Validation Report`, because `Validation/Workflow.md:15` makes
        # Statistical Review a step distinct from Backtesting. The default keeps
        # ADR-011 rule 12 as the behaviour every existing caller already had.
        deliverable=deliverable,
        evidence=(evidence,),
        content=content,
        created=timestamp,
        updated=timestamp,
    )
