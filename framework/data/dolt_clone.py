"""The same database, queried locally instead of over HTTP. Finding 14.

**The problem this solves, measured rather than asserted.** The DoltHub hosted
SQL API cannot serve a backfill. Against the live database on 2026-08-01:

| request | over HTTP | from a local clone |
|---|---|---|
| AAPL daily bars, 2017-10-24..26 | **11.9s** | **0.078–0.135s** |
| AAPL daily bars, 2017-10-16..26 (novel window) | **37.4s** | — |
| `MIN/MAX` aggregate over one month | **52.8s** | — |
| AAPL daily bars, 2015-01-01..2017-12-31 (754 bars) | not attempted | **4.6s** |
| three months, as measured on 2026-08-01 | fails, 3/3 attempts | — |

**Only the first row is the same statement on both sides**, and it is the only
one that licenses a ratio: 11.9s against 0.078–0.135s. The rows below it are
different queries and are listed as evidence that the ceiling is real, not as
comparisons. An earlier version of this table presented all of them as one
comparison, which an independent verification pass correctly refused.

The server's own deadline is roughly 54 seconds, so a novel month-sized query
sits close enough to it to fail intermittently. `docs/HANDOFF.md`'s own table
records a 13-year backfill at about 6.6 hours per symbol over HTTP. The 754-bar
figure above is 36 monthly chunks in 4.6 seconds, so the same 13 years is roughly
20 seconds — bounded by process startup rather than by the network.

**What Dolt is, and why a clone is the intended path rather than a workaround.**
Dolt is a SQL database with Git's semantics — commits, branches, diffs. `dolt
clone` brings the whole database to local disk exactly as `git clone` brings a
repository, and a local query has no deadline, no rate limit and no network. The
shallow clone used here (`--depth 1`) is 730 MB against a full clone's history
back to 2017: Belay needs historical *prices*, which are rows, not historical
*commits*.

**This is a transport, not a second vendor.** It plugs into the
`Callable[[str], bytes]` seam `DoltHubStocksSource` already exposes, so
`MarketDataSource` does not change and neither does the parsing, the chunking or
the survivorship answer. `docs/HANDOFF.md` is explicit that widening the contract
to fit a second transport for the *same vendor* would mean the contract was wrong.

---

**What gets hashed, which is the decision `docs/HANDOFF.md` flagged as the one
that breaks silently.** ADR-013 rule 3 signs a hash of the bytes the source
returned, and "re-fetch, hash, compare" is how Belay detects a vendor restating
history. A local SQL result is not an HTTP response, so three things were ruled:

**1. The clone-backed source carries its own store key.** `fetch_and_record`
keys the store on `source.key`. Had both routes shared one, a symbol fetched over
HTTP and later from the clone would land as two versions of a single chain — and
`store.py` says a new version means the vendor's answer changed. It did not; the
route did. That is a false positive in the only mechanism Belay has for spotting
a real restatement, and it would arrive silently.

**Its cost, which an independent pass had to point out because the first version
of this docstring recorded only the benefit.** At the moment the clone becomes
the route, every series already fetched over HTTP becomes an orphaned chain:
two directories, two independent version-1s, and no cross-reference, because
`source.key` is read in exactly one place. `contract.py` names precisely this
hazard for `key` — "a re-fetch would start again at version 1 and nothing would
report that the history had been lost". So a genuine vendor restatement that
straddles the switch is invisible, and rule 3's re-fetch/hash/compare cannot be
run across the boundary at all.

**Both are true and the trade is deliberate:** a false restatement is a wrong
answer, while a split chain is a missing comparison that a reader can see in the
directory listing. Nothing stored is lost — `Versioning.md:27` keeps every
version searchable, under both keys. This is a ruling and it is the part of
finding 14 most worth revisiting if a second transport ever appears for a third
vendor.

**2. Byte-identity with the HTTP envelope is therefore not required, and is not
attempted.** This is the payoff of the first ruling and it is worth stating,
because forging that envelope is the obvious move. It would mean reproducing
DoltHub's exact key order, whitespace and `columnType` strings; one space off and
the hashes diverge anyway while the author believes they match. **A requirement
that fails silently when approximately met is worse than one that is not
attempted.** What is emitted below is a translation into the vocabulary
`DoltHubStocksSource._parse` already reads — it asserts nothing the local query
did not establish, and it fails loudly (a parse error) rather than quietly.

**3. The clone's commit hash is deliberately excluded from the payload.** It is
real provenance and it is the tempting thing to add. But `dolt pull` advances
that commit whenever upstream moves, and every stored series whose rows had not
changed would then hash differently — the phantom restatement again, arriving
through the provenance door instead of the transport door.

**4. The envelope emitted by `_translate` is a frozen constant, and changing it
is a migration rather than a refactor.** This is the door the first three rulings
did not name, and an independent verification pass found it: on this transport
the hashed bytes are *partly Belay's own serialisation*. Three cosmetically
different `_translate`s over identical vendor rows were shown to produce three
different hashes — `sort_keys=False` alone moves it. So `store.py`'s "a new
version means the vendor's answer changed" is false for any edit here, and
`fetch_record.py`'s "`payload` is the bytes the source returned" is, on this
path, true only of the `rows` inside it.

That is a real cost of translating rather than forging, and it is accepted rather
than hidden: forging fails silently when approximately met, whereas this fails
*loudly* the moment anyone edits the envelope, because
`test_the_translated_envelope_is_pinned_byte_for_byte` turns the suite red. The
mechanism this repository already relies on — make the drift impossible to make
quietly — is what carries the cost. **`_ENVELOPE_VERSION` is in the payload for
the same reason:** if a future change is genuinely needed, it announces itself in
the bytes instead of masquerading as a vendor restatement.

**A note on faithfulness, checked rather than assumed.** The clone and the hosted
API were queried for the identical window on 2026-08-01 and returned identical
values, including the awkward ones: `2017-10-26` high `157.8295` and volume
`17000469` from both. The clone is not an approximation of the source; it is the
source.

**Do not take the fixture in `tests/data/test_dolthub.py` as evidence against
that.** It carries `157.8300` and `17000500` for the same bar and is neither
transport's real output — an illustrative fixture written by hand, which tests
parsing and not accuracy. It is noted here because it is the only committed
record that appears to contradict the paragraph above, and finding it later
without this note would look like a discrepancy.

---

**`dolt sql` outside a clone directory exits 0 and answers anyway.** Established
by running `dolt sql -q "SELECT 1" -r json` in a directory that is not a
database: it returns `{"rows": [{"1":1}]}` and a zero exit code. So a mistyped
clone path does not announce itself — and if the working directory happened to
hold a *different* Dolt database, the wrong data would arrive with no error at
all. The pre-flight check in `_DoltSql` is load-bearing for that reason rather
than defensive.

**The genuinely silent failure is the reverse of the obvious one.** Plain-text
diagnostics are *not* a hazard: `_translate` refuses non-JSON loudly. What is
dangerous is `dolt` writing **valid JSON to stdout while exiting non-zero** —
`dolt sql -q "SELECT 1; SELECT * FROM nope" -r json` does exactly that. Read
without checking the exit code, a truncated result is stamped `Success` and
presented as complete. That is why `_DoltSql` checks `returncode` before anything
else, and why `test_a_partial_result_with_a_nonzero_exit_is_refused` exists.
"""

from __future__ import annotations

import json
import subprocess
import urllib.parse
from collections.abc import Callable
from pathlib import Path

from framework.data.dolthub import _BRANCH, DoltHubStocksSource, SourceUnavailable

# Beside the series store, never inside it. `data/market/` holds fetched series
# versioned on restatement; this holds a copy of the vendor's whole database. One
# is a record and the other is a cache, and sharing a directory would make rule
# 4's version count include clone refreshes. Both have their own `.gitignore`
# entry.
DOLT_CLONE_DEFAULT_PATH = Path("data") / "upstream"

# A Dolt database is marked by this directory, the same way a Git repository is
# marked by `.git`.
_CLONE_MARKER = ".dolt"

# Ruling 4 in the module docstring. These bytes are hashed, so the envelope is a
# frozen constant: bumping this is a deliberate migration that announces itself
# inside the payload, rather than a cosmetic edit that reads downstream as the
# vendor having restated history.
_ENVELOPE_VERSION = 1

# Measured against `dolt version 2.2.3`. Recorded because `_translate` depends on
# the shape of `-r json` output, and a future release changing it would otherwise
# be found by a wrong number rather than by an error.
_VERIFIED_DOLT_VERSION = "2.2.3"

# Generous, because the failure this guards against is a hung subprocess rather
# than a slow query: the measured local query is 0.135s and the slowest plausible
# one is orders of magnitude inside this.
_TIMEOUT_SECONDS = 300


class DoltCloneUnavailable(SourceUnavailable):
    """The local clone could not answer.

    **A sibling of `DoltHubUnavailable`, not a subclass of it, and not
    unrelated.** The two fail for reasons that call for opposite responses — a
    server-side deadline is worth another attempt, a missing binary is not — so
    neither may be caught where the other is meant. But both are a *transport
    failing to answer*, and `dolthub.py`'s chunk wrapper needs to name the
    failing month for either.

    **An earlier version of this docstring justified the separation with a
    hazard that cannot occur**, and the correction is worth keeping because the
    claim was plausible: it said a shared type "would invite retrying a missing
    clone three times". It would not. `dolthub.py`'s `_attempt` calls the
    transport *outside* its `try`, so a transport that raises is never retried —
    measured at one call, not three. Only a deadline reported inside a
    successfully returned payload is retried. The real cost of the separation
    was the unnamed chunk, which is now fixed rather than argued about.

    Distinct from "the query ran and matched no rows", which is a real answer and
    the one a delisted symbol gives.
    """


class _DoltSql:
    """Runs a statement with the `dolt` CLI inside the clone directory.

    Separated from the transport so the test suite never shells out. A suite that
    depends on a 730 MB clone fails for reasons unrelated to the code, which is
    the same argument `dolthub.py` makes for injecting its HTTP transport.
    """

    def __init__(self, database: Path) -> None:
        self._database = database

    def __call__(self, query: str) -> bytes:
        # Checked before running, because `dolt` does not check for us. See the
        # module docstring: outside a database it answers `SELECT 1` happily and
        # exits 0.
        if not (self._database / _CLONE_MARKER).is_dir():
            raise DoltCloneUnavailable(
                f"{self._database} is not a dolt clone — no {_CLONE_MARKER}/ "
                "directory. Refused here rather than left to the CLI, which "
                "would run the query against whatever database it found instead "
                "and return an answer that looks correct. Create it with: "
                "dolt clone --depth 1 post-no-preference/stocks "
                f"{self._database}"
            )

        try:
            completed = subprocess.run(
                # A list, never a shell string. The query reaches the process as
                # one argv element, so no shell ever parses it — the symbol is
                # already constrained by `dolthub.py`'s `_SYMBOL`, and this is
                # the second reason a ticker cannot become a command.
                ["dolt", "sql", "-q", query, "-r", "json"],
                cwd=self._database,
                capture_output=True,
                timeout=_TIMEOUT_SECONDS,
                check=False,
            )
        except FileNotFoundError as error:
            raise DoltCloneUnavailable(
                "the `dolt` command was not found. It is a CLI dependency of "
                "this transport only; the HTTP transport needs nothing "
                "installed. Install it from https://github.com/dolthub/dolt "
                f"or with: winget install DoltHub.Dolt. {error}"
            ) from error
        except subprocess.TimeoutExpired as error:
            raise DoltCloneUnavailable(
                f"the local query exceeded {_TIMEOUT_SECONDS}s, which a clone "
                "should never do — the measured local query is 0.135s. Suspect "
                "a held lock or an interrupted clone rather than a slow query. "
                f"{error}"
            ) from error

        if completed.returncode != 0:
            # **This check is the one that matters, and its real justification is
            # not the obvious one.** A bad table or a syntax error is reported as
            # plain text on *stderr* with an empty stdout, and that case is
            # already safe: `_translate` refuses non-JSON loudly.
            #
            # The dangerous case is `dolt` writing **valid JSON to stdout while
            # exiting non-zero**, which a multi-statement query does —
            # `SELECT 1; SELECT * FROM nope` emits the first result and fails on
            # the second. Without this check that truncated payload is stamped
            # `Success` and stored as complete: fewer bars than the window holds,
            # signed, with nothing to distinguish it from a symbol that genuinely
            # stopped trading. That is the back-door survivorship failure, and an
            # earlier version of this comment defended the wrong door while this
            # one stood open in every mutation test.
            detail = (completed.stderr or completed.stdout).decode(
                "utf-8", errors="replace"
            )
            raise DoltCloneUnavailable(
                f"dolt exited {completed.returncode}: {detail.strip()}"
            )

        return completed.stdout


class DoltCloneTransport:
    """Answers a DoltHub API URL from a local clone instead of the network.

    Satisfies the `Callable[[str], bytes]` seam `DoltHubStocksSource` already
    injects, so it is a drop-in for `_urlopen`.
    """

    def __init__(
        self,
        database: Path | str = DOLT_CLONE_DEFAULT_PATH,
        runner: Callable[[str], bytes] | None = None,
    ) -> None:
        self._database = Path(database)
        self._runner = runner or _DoltSql(self._database)

    def __call__(self, url: str) -> bytes:
        parsed = urllib.parse.urlparse(url)
        query = self._query_of(parsed, url)
        self._check_branch(parsed, url)
        return self._translate(self._runner(query))

    def _query_of(self, parsed: urllib.parse.ParseResult, url: str) -> str:
        """Return the SQL the adapter encoded into `url`.

        Read out of the URL rather than rebuilt. The chunk boundaries
        `_calendar_months` fixes so that a re-fetch hashes identically are
        decided in `dolthub.py`, and a transport that composed its own statement
        would be a second place those boundaries had to agree.
        """
        query = urllib.parse.parse_qs(parsed.query).get("q", [""])[0]

        if not query.strip():
            raise DoltCloneUnavailable(
                f"the URL carries no query to run: {url!r}. Refused rather than "
                "run as an empty statement, whose no-rows result would be "
                "indistinguishable from a symbol that has no data."
            )

        return query

    def _check_branch(self, parsed: urllib.parse.ParseResult, url: str) -> None:
        """Refuse a URL naming a branch this clone is not checked out at.

        **Added because an independent pass noticed half the URL was
        authoritative and half was ignored.** `dolthub.py` puts the branch in the
        path — `_BRANCH`, `master`, pinned there because `main` does not exist on
        this repository — and the query was being honoured while the branch was
        silently dropped. A URL naming a different branch ran anyway, against
        whatever the clone had checked out, and returned confident wrong data.

        A string comparison rather than `dolt branch --show-current`: the check
        runs once per chunk and a 156-chunk backfill cannot afford a subprocess
        per request for it. **What that leaves unverified is stated rather than
        implied** — this confirms the caller asked for the branch the clone was
        cloned from, not that the working copy still sits on it. `dolt clone`
        checks out the remote's default branch, and nothing in Belay ever runs
        `dolt checkout`.
        """
        requested = parsed.path.rstrip("/").rpartition("/")[2]

        if requested and requested != _BRANCH:
            raise DoltCloneUnavailable(
                f"the URL asks for branch {requested!r} but this clone tracks "
                f"{_BRANCH!r}: {url!r}. Refused rather than answered from the "
                "checked-out branch, which would return data the caller did not "
                "ask for and could not tell apart from data it did."
            )

    def _translate(self, output: bytes) -> bytes:
        """Render dolt's answer in the vocabulary `_parse` already reads.

        **A translation, not a forgery of the HTTP envelope.** See the module
        docstring: the store key differs, so byte-identity across transports is
        not required and attempting it would fail silently when approximately
        met.

        `sort_keys` and fixed separators because ADR-013 rule 3 is "re-fetch,
        hash, compare" — a payload whose key order could vary between two runs of
        the same query would report a restatement that never happened.

        Row values pass through **untouched**, and the row *array* is never
        reordered. `dolt` returns volume as a JSON number where the API returns a
        string, and normalising either way would be Belay editing the vendor's
        answer inside the bytes it then signs. `_bar` reads both, and
        `test_a_numeric_volume_is_read_as_an_integer` is what checks that rather
        than the claim being hoped.

        **Editing anything below is a migration.** See ruling 4 in the module
        docstring: these bytes are hashed, so a cosmetic change here is
        indistinguishable downstream from the vendor restating history.
        """
        try:
            body = json.loads(output)
        except json.JSONDecodeError as error:
            raise DoltCloneUnavailable(
                f"dolt returned output that is not JSON: "
                f"{output[:200]!r}. {error}"
            ) from error

        if not isinstance(body, dict):
            raise DoltCloneUnavailable(
                f"dolt returned JSON that is not an object: {output[:200]!r}"
            )

        rows = self._rows_of(body, output)

        return json.dumps(
            {
                # The two fields `_parse` reads. Success is asserted only because
                # the runner already refused a non-zero exit; nothing here claims
                # a status the local query did not earn.
                "query_execution_status": "Success",
                "query_execution_message": "",
                "rows": rows,
                # Named so that anyone reading raw stored bytes can tell which
                # route produced them without consulting the artifact. Constant,
                # therefore hash-safe.
                "transport": "dolt clone (local)",
                # Ruling 4. A future envelope change announces itself here rather
                # than arriving disguised as a vendor restatement.
                "envelope": _ENVELOPE_VERSION,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")

    def _rows_of(self, body: dict, output: bytes) -> list:
        """Return `body`'s rows, refusing a shape that only looks like no data.

        **`{}` means no matches and `{"rows": [...]}` means matches. Anything
        else is refused**, and the distinction is the whole point: an independent
        verification pass observed that a bare `body.get("rows", [])` turns *any*
        unrecognised exit-0 object into a clean empty success. A hypothetical
        `{"error": "syntax error near ohlcv"}` would have become
        `{"query_execution_status":"Success","rows":[]}` — indistinguishable from
        a delisted symbol, which is the back-door survivorship failure this
        module is written against, arriving through the one path nobody checked.

        `dolt` 2.2.3 emits `{}` for no matches, established by running it against
        COH rather than assumed. Pinning the accepted shapes means a future
        `dolt` whose envelope differs fails loudly on the first fetch instead of
        reporting an empty market.
        """
        if not body:
            return []

        rows = body.get("rows")
        if not isinstance(rows, list):
            raise DoltCloneUnavailable(
                "dolt returned an object that is neither empty nor carrying a "
                f"`rows` array: {output[:200]!r}. Refused rather than read as "
                "no data — an empty result for an equity is indistinguishable "
                "from a delisting, and guessing here would put that "
                "indistinguishability inside a signed artifact."
            )

        return rows


class DoltCloneStocksSource(DoltHubStocksSource):
    """`post-no-preference/stocks`, read from a local clone.

    Everything that makes the data what it is comes from the parent unchanged:
    the parsing, the calendar-month chunking, the symbol constraint, and above
    all `DOLTHUB_STOCKS_SURVIVORSHIP` — **a clone is the same data, so the
    survivorship answer is the same object rather than a copy of it.** It is
    inherited rather than restated, and that is load-bearing rather than tidy.

    **Exactly two things differ, and both are identity rather than behaviour.**

    An earlier version of this class also overrode the `survivorship` property
    "to make the inheritance explicit". An independent verification pass showed
    that it was inert — the parent already returns that object — and that it
    **silently removed a guarantee**. `fetch_record._survivorship_of` is the
    second of two links defending the claim that a survivor-only source cannot
    present itself as clean, and it works by asking whether the validated
    constructor ever ran. A *class-level* property answers `getattr(source,
    "survivorship", None)` whether it ran or not, so a subclass skipping
    `super().__init__()` passed the guard on this branch of the hierarchy while
    failing it on the parent's. Demonstrated, not theorised. The override is
    gone; the inheritance was already doing the job it claimed to document.
    """

    #: Says which route produced the bytes. This becomes `Disclosure.data_source`
    #: and sits inside the integrity hash, so a reader of a signed artifact can
    #: tell a clone-derived number from an API-derived one without consulting
    #: anything else. The CC BY-SA attribution is carried over because the
    #: licence condition travels with the data, not with the transport.
    name = "DoltHub post-no-preference/stocks via local clone (CC BY-SA 4.0)"

    #: **Distinct from the parent's, and this is the hashing ruling in one
    #: line.** `fetch_and_record` keys the store on it. Sharing the parent's key
    #: would interleave two version chains whose bytes differ for reasons that
    #: have nothing to do with the vendor restating anything.
    key = "dolthub-stocks-clone"

    def __init__(self, transport: DoltCloneTransport | None = None) -> None:
        # `transport or ...` never resolves to the parent's `_urlopen` default,
        # which is the point: a clone source that silently fell back to HTTP
        # would restore the 37-second ceiling while appearing to have fixed it.
        super().__init__(transport=transport or DoltCloneTransport())
