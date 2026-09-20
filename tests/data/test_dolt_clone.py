"""The local-clone transport. Finding 14, the transport ceiling.

**What this is for.** The DoltHub hosted SQL API cannot serve a backfill. Measured
against the live database on 2026-08-01, and re-measured on the same day from a
cold start: an eleven-day window returning nine bars took **37.4 seconds**, a
one-month aggregate took **52.8 seconds** against a server deadline of roughly 54,
and three months failed 3/3. Thirteen years is about 6.6 hours per symbol.

Dolt is "Git for data". `dolt clone` brings the database to local disk, where the
same query returns in milliseconds with no deadline and no rate limit.

**Nothing here runs `dolt`.** The subprocess is injected, exactly as the HTTP
transport is, for the reason `tests/data/test_dolthub.py` gives: a suite that
shells out to a multi-gigabyte database fails for reasons unrelated to the code.
The live verification is a separate, deliberate act — see `scripts/verify_clone.py`.

**The hashing decision these tests pin, because it is the one that fails
silently.** `docs/HANDOFF.md` warned that "a local SQL result is not an HTTP
response, so decide deliberately what gets hashed". The decision is:

1. The clone-backed source carries **its own store key**, so its version chain
   never interleaves with the HTTP source's. Two transports producing different
   bytes for the same data would otherwise register as a vendor restatement that
   never happened — silently, and in the one mechanism that exists to detect real
   restatements.
2. Because the keys differ, **byte-identity with the HTTP envelope is not
   required**, and is therefore not attempted. Forging that envelope would mean
   reproducing DoltHub's exact key order, whitespace and `columnType` strings; one
   space off and the hashes diverge anyway, while the author believes they match.
   A requirement that fails silently when approximately met is worse than one that
   is not attempted.
3. The clone's **commit hash is deliberately excluded from the payload**. It is
   real provenance and it is tempting, but `dolt pull` would then change the hash
   of every series whose rows had not moved — the phantom restatement again,
   arriving by the other door.
"""

from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path

import pytest

from framework.data.contract import InstrumentClass
from framework.data.dolt_clone import (
    _CLONE_MARKER,
    DOLT_CLONE_DEFAULT_PATH,
    DoltCloneStocksSource,
    DoltCloneTransport,
    DoltCloneUnavailable,
    _DoltSql,
)
from framework.data.dolthub import (
    DOLTHUB_STOCKS_SURVIVORSHIP,
    DoltHubStocksSource,
    DoltHubUnavailable,
    SourceUnavailable,
)
from framework.data.fetch_record import _survivorship_of

# **Copied verbatim from the live clone**, by running the adapter's own query
# against it on 2026-08-01. Two things about this shape are load-bearing and both
# were wrong when this fixture was first written from assumption:
#
# 1. **`volume` is a JSON number, not a string.** The hosted API returns it
#    quoted; `dolt sql -r json` does not. `_bar` calls `int()`, which reads both
#    — but that was an untested claim in a comment until
#    `test_a_numeric_volume_is_read_as_an_integer` below.
# 2. **The values are this transport's, not the other one's.** The first version
#    of this fixture carried `17040200` and `21207300`, copied out of
#    `tests/data/test_dolthub.py`. The real figures are below. A fixture wearing
#    a comment claiming it came from somewhere it did not is the exact defect
#    this repository keeps finding, reproduced inside the file meant to catch it.
#
# Keys are alphabetical because that is the order dolt emits them in.
DOLT_ROWS = (
    b'{"rows": ['
    b'{"close":"157.1000","date":"2017-10-24","high":"157.4200",'
    b'"low":"156.2000","open":"156.2900","volume":17757230},'
    b'{"close":"156.4100","date":"2017-10-25","high":"157.5500",'
    b'"low":"155.2700","open":"156.9100","volume":21207098}'
    b"]}"
)

# **`{}`, not `{"rows": []}`.** Established by running it, after this fixture was
# first written as the latter from assumption. `dolt sql -r json` omits the key
# entirely when nothing matches, which is precisely the shape most likely to be
# read as "no data" by a translation that assumed the key was always present.
DOLT_EMPTY = b"{} "


class FakeRunner:
    """Stands in for `dolt sql`. Records the SQL it was asked to run."""

    def __init__(self, response: bytes = DOLT_ROWS) -> None:
        self.response = response
        self.queries: list[str] = []

    def __call__(self, query: str) -> bytes:
        self.queries.append(query)
        return self.response


def _transport(response: bytes = DOLT_ROWS) -> tuple[DoltCloneTransport, FakeRunner]:
    runner = FakeRunner(response)
    return DoltCloneTransport(database="data/upstream", runner=runner), runner


def _source(response: bytes = DOLT_ROWS):
    transport, runner = _transport(response)
    return DoltCloneStocksSource(transport=transport), runner


# --------------------------------------------------- the seam is the same one


def test_the_transport_satisfies_the_existing_seam():
    """Finding 14's instruction was a second implementation of the injected
    transport, not a wider contract. `DoltHubStocksSource` must accept it with no
    change to `MarketDataSource` at all."""
    transport, runner = _transport()

    source = DoltHubStocksSource(transport=transport)
    fetched = source.fetch_daily_bars(
        "AAPL", start=date(2017, 10, 24), end=date(2017, 10, 25)
    )

    assert len(fetched.series.bars) == 2
    assert runner.queries, "the injected runner was bypassed"


def test_the_query_is_taken_from_the_url_rather_than_rebuilt():
    """The transport receives the URL the adapter already built. Rebuilding the
    SQL here would put the query in two places, and the chunk boundaries that
    `_calendar_months` fixes so carefully would be fixed in only one of them."""
    transport, runner = _transport()

    transport(
        "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/master"
        "?q=SELECT%20%60date%60%20FROM%20ohlcv%20WHERE%20act_symbol%3D%27AAPL%27"
    )

    assert runner.queries == ["SELECT `date` FROM ohlcv WHERE act_symbol='AAPL'"]


def test_a_url_carrying_no_query_is_refused():
    """Rather than running an empty statement and reporting no rows, which is
    indistinguishable from a delisting."""
    transport, _ = _transport()

    with pytest.raises(DoltCloneUnavailable, match="no query"):
        transport("https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks")


# ------------------------------------------------------------- the payload


def test_the_payload_parses_through_the_unchanged_source_parser():
    """The translation exists to speak the vocabulary `_parse` already reads. If
    it did not, every clone fetch would raise `DoltHubUnavailable` on a source
    that was working perfectly."""
    source, _ = _source()

    fetched = source.fetch_daily_bars(
        "AAPL", start=date(2017, 10, 24), end=date(2017, 10, 25)
    )

    assert [bar.date for bar in fetched.series.bars] == [
        date(2017, 10, 24),
        date(2017, 10, 25),
    ]
    assert fetched.series.bars[0].volume == 17_757_230


def test_the_same_query_returns_identical_bytes():
    """ADR-013 rule 3 is "re-fetch, hash, compare". A payload carrying anything
    that varies between two runs of the same query — a timestamp, a uuid, a
    path — reports a vendor restatement that never happened.

    **This test is weaker than it looks and the docstring now says so.** A fake
    runner hands back one constant, and `_translate` is pure, so on its own this
    asserts little more than that a pure function is deterministic. It does catch
    an injected clock or uuid, which is worth having. It does **not** cover key
    order — see `test_the_translated_envelope_is_pinned_byte_for_byte` — and it
    does not cover row order, which `sort_keys` sorts nothing of: that is
    `test_row_order_is_preserved_rather_than_sorted` below.
    """
    transport, _ = _transport()
    url = (
        "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/master"
        "?q=SELECT%20%60date%60%20FROM%20ohlcv"
    )

    assert transport(url) == transport(url)


def test_the_translated_envelope_is_pinned_byte_for_byte():
    """Ruling 4: these bytes are hashed, so the envelope is a frozen constant.

    **The test an independent pass showed was missing.** Three cosmetically
    different `_translate` implementations over identical vendor rows produced
    three different content hashes — `sort_keys=False` alone moved it — and
    nothing in the suite went red. Downstream that is indistinguishable from the
    vendor restating history, which is the one thing `store.py`'s version count
    is supposed to mean.

    Pinning the exact bytes makes an envelope edit turn the suite red on purpose.
    If this test fails, the change under it is a **migration**, not a refactor:
    every series already stored under `dolthub-stocks-clone` will re-hash and
    register as a restatement that did not happen. Bump `_ENVELOPE_VERSION`
    deliberately, or put the change back.
    """
    transport, _ = _transport(b'{"rows": [{"date":"2017-10-24","volume":17757230}]}')

    payload = transport(
        "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/master"
        "?q=SELECT%201"
    )

    assert payload == (
        b'{"envelope":1,'
        b'"query_execution_message":"",'
        b'"query_execution_status":"Success",'
        b'"rows":[{"date":"2017-10-24","volume":17757230}],'
        b'"transport":"dolt clone (local)"}'
    )


def test_row_order_is_preserved_rather_than_sorted():
    """`sort_keys=True` sorts the keys of each row object and reorders no array.

    Pinned because the determinism test above once claimed to defend row order
    and could not: the vendor's `ORDER BY` decides it, and re-sorting here would
    be Belay editing the source's answer inside the bytes it then signs.
    `DailyBarSeries` enforces date order on the *parsed* series separately, which
    is the right place for that invariant.
    """
    forward = _transport(
        b'{"rows": [{"date":"2017-10-24"},{"date":"2017-10-25"}]}'
    )[0]
    backward = _transport(
        b'{"rows": [{"date":"2017-10-25"},{"date":"2017-10-24"}]}'
    )[0]
    url = (
        "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/master"
        "?q=SELECT%201"
    )

    assert forward(url) != backward(url)
    assert forward(url).index(b"2017-10-24") < forward(url).index(b"2017-10-25")


def test_a_numeric_volume_is_read_as_an_integer():
    """`dolt` returns volume unquoted where the API quotes it. `dolt_clone.py`
    claims "`_bar` reads both, which was checked rather than hoped" — this is
    that check. Without it the claim was a comment, and the suite only ever saw
    the quoted form because the fixture had been copied from the HTTP tests."""
    source, _ = _source()

    volume = source.fetch_daily_bars(
        "AAPL", start=date(2017, 10, 24), end=date(2017, 10, 25)
    ).series.bars[0].volume

    assert volume == 17_757_230
    assert isinstance(volume, int)


def test_the_clone_commit_is_not_in_the_payload():
    """Deliberately excluded, and this is the subtle half of the hashing ruling.

    The commit the clone sits on is genuine provenance and it is tempting to
    record it in the bytes. But `dolt pull` advances that commit daily, and every
    stored series whose rows had not changed would then hash differently — a
    phantom restatement arriving through the provenance door rather than the
    transport door.
    """
    transport, _ = _transport()

    payload = transport(
        "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/master"
        "?q=SELECT%20%60date%60%20FROM%20ohlcv"
    )
    body = json.loads(payload)

    assert "commit" not in json.dumps(body).lower()


def test_an_empty_result_is_an_empty_series_rather_than_an_error():
    """A genuine "this symbol has no bars in this window" is a real answer and
    the one COH returns. It must survive the translation as an answer."""
    source, _ = _source(DOLT_EMPTY)

    fetched = source.fetch_daily_bars(
        "COH", start=date(2015, 1, 5), end=date(2015, 1, 16)
    )

    assert fetched.series.bars == ()


# ------------------------------------------------------------------ failure


def test_a_dolt_failure_is_raised_rather_than_read_as_no_data():
    """The failure mode the whole of ADR-013 is arranged against. An error that
    becomes an empty result is indistinguishable from a delisting, which is
    survivorship bias arriving through the back door."""

    def broken(query: str) -> bytes:
        raise DoltCloneUnavailable("table not found: ohlcv")

    transport = DoltCloneTransport(database="data/upstream", runner=broken)
    source = DoltCloneStocksSource(transport=transport)

    with pytest.raises(DoltCloneUnavailable, match="table not found"):
        source.fetch_daily_bars(
            "AAPL", start=date(2017, 10, 24), end=date(2017, 10, 25)
        )


def test_output_that_is_not_json_is_refused():
    """`dolt` writes diagnostics to stdout in some failure modes. Parsed as an
    empty result they would read as a delisting."""
    transport, _ = _transport(b"error: not a dolt directory")

    with pytest.raises(DoltCloneUnavailable):
        transport(
            "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/master"
            "?q=SELECT%201"
        )


def test_a_missing_clone_is_refused_before_anything_is_run():
    """A clone that is not there must fail loudly. The alternative is a backtest
    that quietly has no data, which `store.py` already names as the failure it
    most wants to avoid."""
    transport = DoltCloneTransport(database="data/upstream-that-does-not-exist")

    with pytest.raises(DoltCloneUnavailable, match="clone"):
        transport(
            "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/master"
            "?q=SELECT%201"
        )


def test_an_object_that_is_neither_empty_nor_carrying_rows_is_refused():
    """`body.get("rows", [])` turned *any* unrecognised exit-0 object into a
    clean empty success — so a hypothetical `{"error": "..."}` would arrive as
    zero bars, indistinguishable from a delisted symbol. That is the back-door
    survivorship failure through the one path nobody had checked."""
    transport, _ = _transport(b'{"error":"syntax error near ohlcv"}')

    with pytest.raises(DoltCloneUnavailable, match="neither empty nor"):
        transport(
            "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/master"
            "?q=SELECT%201"
        )


def test_a_url_naming_another_branch_is_refused():
    """`dolthub.py` pins `master` because `main` does not exist on this
    repository. The branch was being dropped from the URL while the query was
    honoured, so a request for another branch ran against whatever the clone had
    checked out and returned confident wrong data."""
    transport, _ = _transport()

    with pytest.raises(DoltCloneUnavailable, match="branch"):
        transport(
            "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/"
            "some-other-branch?q=SELECT%201"
        )


# ------------------------------------------------- the runner that shells out
#
# None of these spawn `dolt`. They pin the four properties of `_DoltSql` that a
# mutation pass showed were entirely undefended: deleting the returncode check,
# or switching the argv list to `shell=True`, left the whole suite green.


def _clone(tmp_path):
    (tmp_path / _CLONE_MARKER).mkdir()
    return tmp_path


def test_a_partial_result_with_a_nonzero_exit_is_refused(tmp_path, monkeypatch):
    """**The mutation that survived, and the one that matters.**

    `dolt sql -q "SELECT 1; SELECT * FROM nope" -r json` writes valid JSON to
    stdout, the error to stderr, and exits 1. Without the returncode check that
    truncated payload is stamped `Success` and stored as complete — fewer bars
    than the window holds, signed, and indistinguishable from a symbol that
    stopped trading. Plain-text output was never the hazard; `_translate` refuses
    that loudly. This is.
    """
    monkeypatch.setattr(
        subprocess,
        "run",
        lambda *a, **k: subprocess.CompletedProcess(
            a, 1, stdout=b'{"rows": [{"date":"2017-10-24"}]}', stderr=b"error on line 1"
        ),
    )

    with pytest.raises(DoltCloneUnavailable, match="exited 1"):
        _DoltSql(_clone(tmp_path))("SELECT 1; SELECT * FROM nope")


def test_the_query_reaches_the_process_as_one_argv_element(tmp_path, monkeypatch):
    """No shell ever parses the query. Undefended until now: replacing the argv
    list with an f-string and `shell=True` kept every test green, which made the
    "a list, never a shell string" claim in the source a comment rather than a
    property."""
    seen: dict = {}

    def record(args, **kwargs):
        seen["args"] = args
        seen["kwargs"] = kwargs
        return subprocess.CompletedProcess(args, 0, stdout=b"{}", stderr=b"")

    monkeypatch.setattr(subprocess, "run", record)
    _DoltSql(_clone(tmp_path))("SELECT * FROM ohlcv WHERE act_symbol='DYN$A'")

    assert isinstance(seen["args"], list)
    assert seen["kwargs"].get("shell") is not True
    assert seen["args"].count("SELECT * FROM ohlcv WHERE act_symbol='DYN$A'") == 1


def test_the_clone_is_checked_before_any_process_is_spawned(tmp_path, monkeypatch):
    """`dolt` answers `SELECT 1` happily outside a database and exits 0, so a
    mistyped path does not announce itself. The check must therefore come first
    rather than rely on the CLI complaining."""
    spawned: list = []
    monkeypatch.setattr(subprocess, "run", lambda *a, **k: spawned.append(a))

    with pytest.raises(DoltCloneUnavailable, match="not a dolt clone"):
        _DoltSql(tmp_path)("SELECT 1")

    assert not spawned, "the clone check ran after spawning a process"


def test_a_missing_dolt_binary_says_how_to_install_it(tmp_path, monkeypatch):
    """The CLI is a dependency of this transport only — the HTTP transport needs
    nothing installed — so the error has to say that rather than read as a
    broken repository."""

    def missing(*a, **k):
        raise FileNotFoundError("dolt")

    monkeypatch.setattr(subprocess, "run", missing)

    with pytest.raises(DoltCloneUnavailable, match="winget|not found"):
        _DoltSql(_clone(tmp_path))("SELECT 1")


def test_a_hung_query_is_refused_rather_than_waited_on_forever(tmp_path, monkeypatch):
    """A local query measured at 0.078s cannot legitimately take five minutes. A
    held lock or an interrupted clone can, and an unattended overnight backfill
    must not hang on one."""

    def hang(*a, **k):
        raise subprocess.TimeoutExpired(cmd="dolt", timeout=300)

    monkeypatch.setattr(subprocess, "run", hang)

    with pytest.raises(DoltCloneUnavailable, match="exceeded"):
        _DoltSql(_clone(tmp_path))("SELECT 1")


# ------------------------------------------- the store key, and why it differs


def test_the_clone_source_has_its_own_store_key():
    """The ruling this file's docstring sets out.

    `fetch_and_record` keys the store on `source.key`. If the clone and the API
    shared one, a symbol fetched over HTTP and then from the clone would land as
    two versions of one chain — and `store.py` says a new version means "the
    vendor's answer changed". It did not; the route did.
    """
    assert DoltCloneStocksSource.key != DoltHubStocksSource.key
    assert DoltCloneStocksSource.key


def test_the_clone_source_names_the_route_in_its_own_name():
    """`source.name` becomes `Disclosure.data_source` and sits inside the
    integrity hash. A reader of a signed artifact should be able to tell which
    route produced the bytes without consulting anything else."""
    assert "clone" in DoltCloneStocksSource.name.lower()
    assert "CC BY-SA" in DoltCloneStocksSource.name


def test_the_clone_source_carries_the_identical_survivorship_answers():
    """A local clone is the same data. Finding 14 is explicit that the
    survivorship answers do not change, and this pins the constant itself rather
    than its values — a copy would drift."""
    source, _ = _source()

    assert source.survivorship is DOLTHUB_STOCKS_SURVIVORSHIP


def test_a_subclass_that_skips_the_constructor_is_still_refused():
    """**The guarantee this module briefly removed while claiming to preserve
    it**, and the reason this test exists rather than a comment.

    `contract.py` describes two links defending the claim that a survivor-only
    source cannot present itself as clean: the constructor, and
    `fetch_record._survivorship_of` at the point the answer enters a signed
    artifact. The second works by asking whether the validated constructor ever
    ran.

    An earlier `DoltCloneStocksSource` defined `survivorship` as a class-level
    property "to make the inheritance explicit". That answers `getattr(source,
    "survivorship", None)` whether the constructor ran or not — so this exact
    subclass **passed** the guard on the clone branch while **failing** it on the
    parent's. Inert-looking code, and it removed the one thing that makes free
    biased data honest. Found by an independent pass, not by the suite, because
    nothing asked this question.
    """
    class SkipsTheConstructor(DoltCloneStocksSource):
        def __init__(self) -> None:  # noqa: D107 - deliberately calls no super()
            pass

    with pytest.raises(TypeError, match="SurvivorshipDisclosure"):
        _survivorship_of(SkipsTheConstructor())


def test_the_clone_source_defines_no_survivorship_of_its_own():
    """Belt and braces on the test above, and it fails for a different reason.

    The guard test would still pass if someone reintroduced the override *and*
    made it validating. This one says the attribute is inherited rather than
    restated at all — which is the property the docstring actually claims, and
    the one that keeps `DOLTHUB_STOCKS_SURVIVORSHIP` a single object rather than
    something a subclass is free to redefine.
    """
    assert "survivorship" not in vars(DoltCloneStocksSource)


def test_the_clone_source_declares_equities_only():
    source, _ = _source()

    assert source.supported_instruments() == frozenset({InstrumentClass.EQUITY})


# ------------------------------------------------------------- no network


def test_nothing_here_reaches_the_network():
    """The point of the exercise. The clone transport must never fall back to
    HTTP: a silent fallback would restore the 37-second ceiling while appearing
    to have fixed it.

    **Asserted against the imports rather than against the source text**, and
    that correction is the point. This test was first written as `"urllib" not
    in source`, which banned `urllib.parse` — string manipulation, and the right
    tool for reading the query out of the URL. Rewritten to `"urlopen" not in
    source`, it then failed on the phrase "a drop-in for `_urlopen`" inside a
    docstring. **A substring search over source text cannot tell a call from a
    comment**, so it was replaced with a question about what the module can
    actually reach.
    """
    import ast
    import inspect

    import framework.data.dolt_clone as module

    imported: set[str] = set()
    for node in ast.walk(ast.parse(inspect.getsource(module))):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)

    assert not {"urllib.request", "http.client", "socket", "requests"} & imported
    assert "urllib.parse" in imported, "the URL is parsed rather than hand-split"


def test_the_clone_source_never_falls_back_to_the_http_transport():
    """The parent's constructor reads `transport or _urlopen`, so a clone source
    constructed with `None` would silently reach the network — restoring the
    37-second ceiling while appearing to have fixed it, which is the worst
    available outcome because it looks like success."""
    source = DoltCloneStocksSource()

    assert isinstance(source._transport, DoltCloneTransport)


def test_the_default_clone_path_is_outside_the_series_store():
    """`data/market/` holds fetched series, versioned on restatement. The clone
    is an upstream cache. Sharing a directory would make rule 4's version count
    include clone refreshes."""
    assert "market" not in str(DOLT_CLONE_DEFAULT_PATH)
    assert str(DOLT_CLONE_DEFAULT_PATH).startswith("data")


def test_git_itself_ignores_the_clone_directory():
    """**Asked of git rather than of `.gitignore`**, which is the precedent
    `tests/data/test_store.py` already set for the store beside this one: a rule
    written in the wrong section, or shadowed by a later negation, reads
    correctly and behaves wrongly.

    Not followed here until an independent pass pointed at the neighbouring test.
    The stake is higher, not lower — this directory is 730 MB and git history
    cannot be pruned after the fact.
    """
    probe = DOLT_CLONE_DEFAULT_PATH / ".dolt" / "noms" / "probe"

    result = subprocess.run(
        ["git", "check-ignore", "-q", str(probe)],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
    )

    assert result.returncode == 0, (
        f"{probe} is not ignored by git. The clone is a multi-gigabyte upstream "
        "cache; a repository that starts tracking it cannot be cleaned "
        "afterwards."
    )


def test_the_transport_is_not_coupled_to_the_http_error_type():
    """`DoltCloneUnavailable` is a sibling of `DoltHubUnavailable`, not a
    subclass. They call for opposite responses — a server deadline is worth
    another attempt, a missing binary is not — so neither may be caught where the
    other is meant."""
    assert not issubclass(DoltCloneUnavailable, DoltHubUnavailable)
    assert not issubclass(DoltHubUnavailable, DoltCloneUnavailable)
    assert issubclass(DoltCloneUnavailable, SourceUnavailable)


def test_a_failing_chunk_says_which_month_failed():
    """**The regression an independent pass found**, and the reason the shared
    base class exists.

    `dolthub.py` wraps a failing chunk to name the month, because "a thirteen-year
    backfill is 156 requests and a message that does not say which month failed
    turns a one-line fix into a search." That wrapper caught `DoltHubUnavailable`
    only, so every clone failure escaped it bare — and the clone is precisely
    what makes 156-chunk backfills routine rather than impossible. The diagnostic
    was lost by the change that made the thing needing it possible.
    """

    def broken(query: str) -> bytes:
        raise DoltCloneUnavailable("table not found: ohlcv")

    source = DoltCloneStocksSource(
        transport=DoltCloneTransport(database="data/upstream", runner=broken)
    )

    with pytest.raises(DoltCloneUnavailable) as caught:
        source.fetch_daily_bars(
            "AAPL", start=date(2015, 1, 1), end=date(2015, 3, 31)
        )

    message = str(caught.value)

    assert "2015-01-01" in message, "the failing chunk is not named"
    assert "table not found" in message, "the underlying cause was discarded"


def test_naming_the_chunk_does_not_relabel_the_failure():
    """The wrapper re-raises the *original* type. Relabelling a missing local
    clone as a hosted-API failure would hand a caller distinguishing the two a
    lie, which is worse than the bare message it replaced."""

    def broken(query: str) -> bytes:
        raise DoltCloneUnavailable("no clone")

    source = DoltCloneStocksSource(
        transport=DoltCloneTransport(database="data/upstream", runner=broken)
    )

    with pytest.raises(DoltCloneUnavailable):
        source.fetch_daily_bars(
            "AAPL", start=date(2015, 1, 1), end=date(2015, 1, 31)
        )
