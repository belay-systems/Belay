"""The market data boundary. ADR-013 rules 2, 3, 6 and 9.

**What a boundary is, and why one hard-coded fetcher is not it.**
`docs/ROADMAP.md` Stage 2's whole deliverable is "a defined boundary for
obtaining a price series, with provenance recorded on the resulting evidence",
and a boundary is an adapter contract. Writing a single fetcher does not avoid
the ruling about how many sources there can be — under ADR-011's central holding
it *makes* that ruling silently: that there is only ever one source, and that
its survivorship properties are whatever they happen to be.

**Two shapes, not one shape with a flag.** A price series is one instrument over
time. An option chain is, for one date and underlying, many contracts each with
a strike, an expiry, a right and its own quotes. One is a sequence; the other is
a sequence of sets. ADR-013 rule 6 is explicit that collapsing them would be
wrong even though both are "market data".

**Nothing here is an Artifact.** ADR-013 rule 3: `Knowledge/Identifiers.md`
defines eight prefixes and `ArtifactType` nine members, and between them none
names market data. A fetched series has no honest identity under the vocabulary
Belay has, and manufacturing one widens the open finding that those two
vocabularies already disagree. The data is an *input*; what Law VII requires
Belay to retain is the record of what was obtained — see `fetch_record.py`.

**No shared base class with a broker.** Rule 2, on
`constitution/Immutable_Laws.md:45` (Law VI) — "Research and execution remain
independent." Market data is a read. An execution adapter writes to the world
and the write moves money irreversibly. Retrying is *how* a data fetch recovers
from a dropped connection; a retried order submit doubles a position. A shared
base class must pick one default and be wrong for the other.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum

from framework.data.survivorship import SurvivorshipDisclosure
from framework.metrics.reporting import SamplePeriod


class InstrumentClass(str, Enum):
    """The asset classes the contract can express. ADR-013 rule 6.

    Both are named even though only equities are implemented.
    `constitution/Operational_Constraints.md:25-27` forbids inherent preference
    between asset classes, and a contract that cannot express an option gives
    equities preference by construction — a strategy needing option data could
    not be written against it at all. Implementation order is not preference.
    """

    EQUITY = "Equity"
    OPTION = "Option"


class OptionRight(str, Enum):
    CALL = "Call"
    PUT = "Put"


class InstrumentNotSupported(Exception):
    """Raised when a source is asked for an instrument class it does not carry.

    Raised rather than returning an empty result. An empty chain is
    indistinguishable from "this underlying had no options that day", and a
    silent wrong answer is the failure mode the whole of ADR-013 is arranged
    against.
    """


@dataclass(frozen=True, slots=True)
class DailyBar:
    """One instrument on one day.

    Prices are `Decimal`, not `float`. Money in binary floating point
    accumulates error that stays invisible until it is material, and the source
    publishes `decimal(14,4)` — widening that to a float on the way in would
    discard precision Belay was given for free.
    """

    date: date
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


@dataclass(frozen=True, slots=True)
class DailyBarSeries:
    """One instrument over time. Not an Artifact — ADR-013 rule 3."""

    symbol: str
    bars: tuple[DailyBar, ...]

    def __post_init__(self) -> None:
        dates = [bar.date for bar in self.bars]
        # Strictly increasing, not merely sorted. The guard was
        # `dates != sorted(dates)`, and `[d1, d1, d2]` is sorted — so the same
        # trading day could appear any number of times in a series presenting
        # itself as validated. A repeated bar is read as a return of exactly
        # 0.0, which pulls the standard deviation down while barely moving the
        # mean: the standard error falls, the t-statistic rises, and
        # `significant` can flip true on observations that were never made.
        if any(later <= earlier for earlier, later in zip(dates, dates[1:])):
            raise ValueError(
                f"bars for {self.symbol} are not in strictly increasing date "
                "order; `period()` and every windowed computation built on this "
                "series would be silently wrong."
            )

    def period(self) -> SamplePeriod:
        """Return the window these bars actually cover. ADR-013 rule 7.

        Derived from the bars rather than supplied alongside them, so a series
        cannot claim coverage it does not have. This is the landing point that
        makes `Disclosure.sample_period` stop being written by hand at the call
        site.
        """
        if not self.bars:
            raise ValueError(
                f"the series for {self.symbol} is empty and covers no period; "
                "inventing a window for it would be a fabricated disclosure."
            )
        return SamplePeriod(start=self.bars[0].date, end=self.bars[-1].date)


@dataclass(frozen=True, slots=True)
class FetchedSeries:
    """A parsed series together with the bytes it arrived as. ADR-013 rule 3.

    Both, because the rule hashes *the bytes the source returned* rather than
    the parsed form. A parser change alters the parsed series while the source's
    answer is byte-identical, and the hash exists to detect the reverse — the
    source's answer changing underneath an unchanged parser, which is what a
    vendor restatement is. A fetch that discarded the payload could not produce
    the record rule 3 requires.
    """

    series: DailyBarSeries
    payload: bytes


@dataclass(frozen=True, slots=True)
class OptionQuote:
    """One contract on one day."""

    expiration: date
    strike: Decimal
    right: OptionRight
    bid: Decimal | None
    ask: Decimal | None


@dataclass(frozen=True, slots=True)
class OptionChain:
    """Many contracts, for one underlying, as at one date.

    The `as_of` date is the observation date and is distinct from each quote's
    `expiration`. Conflating them is the mistake that makes an option dataset
    look survivorship-clean when it is not: a source can hold today's chains for
    every expiry and still know nothing about what a chain looked like in 2019.
    """

    underlying: str
    as_of: date
    quotes: tuple[OptionQuote, ...]


class MarketDataSource(ABC):
    """A place market data comes from, and what it must be able to say for itself.

    Inherits from `ABC` and nothing else, deliberately. The moment a shared
    `Adapter` base appears above this, market data and execution are coupled
    across a boundary the constitution declares independent — ADR-013 rule 2.

    **Survivorship is required at construction.** Rule 9: a source that cannot
    state its properties is refused, not assumed clean. `Retention.UNKNOWN` is a
    legitimate answer; not answering is not.

    **The constructor is not the only guard, and saying it was is what a
    verification pass caught.** A subclass overriding `__init__` without calling
    `super().__init__` bypasses it entirely, and the attribute was plainly
    settable afterwards. So `survivorship` is now read-only here, and
    `framework/data/fetch_record.py` re-checks at the point the answer is
    written into a signed artifact. Two links, because the claim being defended
    — that a survivor-only source cannot present itself as clean — is the one
    thing making free biased data honest.
    """

    #: Human-readable source name. Becomes `Disclosure.data_source`, which
    #: `framework/metrics/reporting.py` requires non-blank and puts inside the
    #: integrity hash. Free to be long and descriptive — it carries the licence
    #: attribution CC BY-SA requires.
    name: str = ""

    #: Stable identifier, used to key the data store. **Deliberately separate
    #: from `name`**: the store path must not move when the display name is
    #: edited. Keying on `name` meant adding licence text to it silently
    #: orphaned every version already stored under the old wording — a re-fetch
    #: would start again at version 1 and nothing would report that the history
    #: had been lost, which is the silent irreproducibility ADR-013 rule 4
    #: exists to prevent. Short, lowercase, and never changed once data exists.
    key: str = ""

    def __init__(self, survivorship: SurvivorshipDisclosure) -> None:
        if not isinstance(survivorship, SurvivorshipDisclosure):
            raise TypeError(
                "a market data source must be constructed with a "
                "SurvivorshipDisclosure. ADR-013 rule 9: a source that cannot "
                "state its survivorship properties is refused, not assumed "
                "clean, and it fails in the direction that flatters."
            )
        # Written past the read-only property below. `object.__setattr__` is the
        # same device a frozen dataclass uses on its own `__init__`.
        object.__setattr__(self, "_survivorship", survivorship)

    @property
    def survivorship(self) -> SurvivorshipDisclosure:
        """The source's survivorship answer. Read-only after construction.

        Settable until 2026-08-01, which meant `source.survivorship = clean`
        suppressed the disclosure on every artifact derived afterwards — the
        same substitution ADR-012 rule 7 fixes its constants to prevent, by a
        different route.
        """
        return self._survivorship

    @abstractmethod
    def supported_instruments(self) -> frozenset[InstrumentClass]:
        """Return the instrument classes this source actually carries."""

    def fetch_daily_bars(
        self, symbol: str, start: date, end: date
    ) -> FetchedSeries:
        """Return daily bars for `symbol` over the inclusive window.

        Returns the payload alongside the parsed series because ADR-013 rule 3
        signs a hash of the bytes the source returned, not of the parse.
        """
        self._require(InstrumentClass.EQUITY)
        if end < start:
            raise ValueError(
                f"end {end.isoformat()} falls before start {start.isoformat()}"
            )
        return self._fetch_daily_bars(symbol, start, end)

    def fetch_option_chain(self, underlying: str, as_of: date) -> OptionChain:
        """Return the option chain for `underlying` as at `as_of`.

        Declared on the contract even where no adapter implements it. Rule 6:
        deferring the *implementation* is fine; deferring the *expressibility*
        gives equities inherent preference by construction.
        """
        self._require(InstrumentClass.OPTION)
        return self._fetch_option_chain(underlying, as_of)

    def _require(self, instrument: InstrumentClass) -> None:
        if instrument not in self.supported_instruments():
            raise InstrumentNotSupported(
                f"{self.name or type(self).__name__} does not carry "
                f"{instrument.value} data. Refused rather than answered with an "
                "empty result, which would be indistinguishable from the "
                "instrument genuinely having no data."
            )

    def _fetch_daily_bars(
        self, symbol: str, start: date, end: date
    ) -> FetchedSeries:
        raise NotImplementedError(
            f"{type(self).__name__} declares EQUITY support but does not "
            "implement _fetch_daily_bars."
        )

    def _fetch_option_chain(self, underlying: str, as_of: date) -> OptionChain:
        raise NotImplementedError(
            f"{type(self).__name__} declares OPTION support but does not "
            "implement _fetch_option_chain."
        )
