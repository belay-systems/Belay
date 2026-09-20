"""Run a real fetch through the local clone. Finding 14.

**Why this exists outside the test suite.** `pytest` touches no network and no
subprocess, deliberately — so a green suite says nothing about whether the data
works. Both real problems found on 2026-08-01 were found by running one live
fetch *after* the suite was green, and `docs/HANDOFF.md` makes it a standing
instruction: run a real fetch before believing any transport change.

Not a test. It needs a 730 MB clone and the `dolt` CLI, neither of which the
suite may depend on.

    python scripts/verify_clone.py

Exits non-zero if any check fails, so it can gate a session close.
"""

from __future__ import annotations

import hashlib
import shutil
import sys
import tempfile
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from framework.data.dolt_clone import (  # noqa: E402
    DOLT_CLONE_DEFAULT_PATH,
    DoltCloneStocksSource,
    DoltCloneUnavailable,
)
from framework.artifacts.repository import ARTIFACT_ROOT, ArtifactRepository  # noqa: E402
from framework.data.fetch_record import (  # noqa: E402
    fetch_and_record,
    orphan_versions,
)
from framework.data.store import SeriesStore  # noqa: E402
from framework.metrics.reporting import SamplePeriod  # noqa: E402

FAILURES: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    print(f"  {'PASS' if condition else 'FAIL'}  {label}{f' — {detail}' if detail else ''}")
    if not condition:
        FAILURES.append(label)


def main() -> int:
    print(f"Verifying the clone at {DOLT_CLONE_DEFAULT_PATH}\n")

    if not (DOLT_CLONE_DEFAULT_PATH / ".dolt").is_dir():
        print(f"No clone at {DOLT_CLONE_DEFAULT_PATH}. Create it with:")
        print(
            "  dolt clone --depth 1 post-no-preference/stocks "
            f"{DOLT_CLONE_DEFAULT_PATH}"
        )
        return 1

    source = DoltCloneStocksSource()

    # ---------------------------------------------------------- a real fetch
    print("A real fetch, end to end through fetch_and_record:")
    root = Path(tempfile.mkdtemp(prefix="belay-clone-verify-"))
    try:
        store = SeriesStore(root=root / "market")
        # ADR-014 rule 3. The root is the boundary between an experiment and a
        # permanent record, and nothing else enforces it — a diagnostic pointed
        # at the default would mint a permanent institutional record, under a
        # hardcoded identifier, every time somebody checked the clone still
        # worked.
        repository = ArtifactRepository(root=root / "artifacts")
        # Resolved on both sides, and `==` as well as `in parents`. The first
        # version compared an absolute path to `Path("artifacts")` — never equal
        # — and asked only about parents, so it reported PASS while pointed
        # directly at the tracked root.
        tracked, writing = ARTIFACT_ROOT.resolve(), repository.root.resolve()
        check("this script writes no artifact into the tracked root",
              writing != tracked and tracked not in writing.parents,
              f"writing to {writing}")
        requested = SamplePeriod(start=date(2017, 10, 24), end=date(2017, 10, 26))

        started = time.time()
        fetch = fetch_and_record(
            identifier="RPT-9001",
            source=source,
            symbol="AAPL",
            requested=requested,
            store=store,
            repository=repository,
        )
        elapsed = time.time() - started

        check("the fetch returned bars", len(fetch.series.bars) == 3,
              f"{len(fetch.series.bars)} bars in {elapsed:.3f}s")

        # **Labelled for what it actually does.** An earlier version called this
        # "the awkward values match the API exactly" while comparing against two
        # constants typed into this file — it never contacted the API, so it
        # could not have failed if they diverged. Pass --cross-check to make the
        # API half real; without it this pins the clone against its own recorded
        # observation, which is worth having and is a smaller claim.
        last = fetch.series.bars[-1]
        check("the clone returns the values recorded from it on 2026-08-01",
              str(last.high) == "157.8295" and last.volume == 17000469,
              f"high={last.high} volume={last.volume}")

        # 0.078-0.135s measured locally against 11.9s for the *same statement*
        # over HTTP. One second is comfortably an order of magnitude below that
        # and is a claim this threshold can actually support; the previous
        # `< 5.0` printed PASS for a 4.9s run under a label saying otherwise.
        check("it beat the HTTP path by an order of magnitude", elapsed < 1.0,
              f"{elapsed:.3f}s against 11.9s for the identical query over HTTP")

        check("the bytes landed in the store",
              fetch.stored.path.exists() and fetch.stored.version == 1)

        check("the store is keyed on the clone, not the API",
              "clone" in str(fetch.stored.path))

        check("the record carries the survivorship warning",
              "survivor" in dict(fetch.record.content)["known_limitations"].lower())

        check("the record names the clone route",
              "clone" in dict(fetch.record.content)["data_source"].lower())

        # ------------------------------------------------- ADR-014, F-002
        check("the record was written to disk, not just returned",
              fetch.record_path.is_file() and fetch.record_is_new,
              f"{fetch.record_path.name} under {repository.root.name}/")

        content = dict(fetch.record.content)
        landed = store.root / content["store_path"]
        check("the record names its own bytes and they are there",
              landed.is_file()
              and hashlib.sha256(landed.read_bytes()).hexdigest()
              == content["content_hash"],
              f"store_path={content['store_path']} key={content['source_key']}")

        # ------------------------------------------- rule 3: re-fetch, compare
        print("\nADR-013 rule 3 — re-fetch, hash, compare:")
        again = fetch_and_record(
            identifier="RPT-9002",
            source=source,
            symbol="AAPL",
            requested=requested,
            store=store,
            repository=repository,
        )
        check("an identical re-fetch is the same version, not a restatement",
              again.stored.version == 1,
              f"version {again.stored.version}")
        check("the content hashes agree",
              again.stored.content_hash == fetch.stored.content_hash)
        check("a fetch that stored nothing new wrote no second record",
              not again.record_is_new and again.record.id == "RPT-9001",
              "ADR-014 rule 5")

        # ----------------------------------------- the thing that was impossible
        print("\nThe backfill that could not be done over HTTP:")
        started = time.time()
        wide = source.fetch_daily_bars(
            "AAPL", start=date(2015, 1, 1), end=date(2017, 12, 31)
        )
        elapsed = time.time() - started
        check("three years of daily bars in one call",
              len(wide.series.bars) > 700,
              f"{len(wide.series.bars)} bars in {elapsed:.1f}s "
              f"(36 monthly chunks; over HTTP this is ~30+ minutes at best)")

        # ------------------------------------------------- the survivorship claim
        print("\nThe survivorship finding, re-established against the clone:")
        coh = source.fetch_daily_bars(
            "COH", start=date(2015, 1, 5), end=date(2015, 1, 16)
        )
        check("COH (delisted 2017) still returns no prices",
              coh.series.bars == (),
              "the survivor-only finding holds locally, as it must")

        # ------------------------------------------------------- a known trap
        #
        # Pre-existing in `fetch_record.py` and made routine by the clone, so it
        # is surfaced here rather than left to be discovered by a backfill.
        # `fetch_and_record` stores the bytes and *then* asks the series for its
        # period, which an empty series refuses. Every delisted symbol in a
        # backfill therefore leaves a file in an append-only store and raises —
        # and this source is survivor-only by its own disclosure, so delisted
        # symbols are not an edge case here, they are the expected case.
        print("\nA delisted symbol through the full record path:")
        before = len(store.versions(source.key, "COH"))
        try:
            fetch_and_record(
                identifier="RPT-9003",
                source=source,
                symbol="COH",
                requested=SamplePeriod(
                    start=date(2015, 1, 5), end=date(2015, 1, 16)
                ),
                store=store,
                repository=repository,
            )
            raised = ""
        except ValueError as error:
            raised = str(error)

        orphaned = len(store.versions(source.key, "COH")) > before
        check("KNOWN: an empty series raises after its bytes are already stored",
              bool(raised) and orphaned,
              "docs/HANDOFF.md — not fixed here, and not a regression "
              "introduced by the clone")

        # ADR-014 rule 7. The orphan above is exactly what the check is for, so
        # the check is exercised against a real one rather than a contrived one.
        orphans = orphan_versions(store, repository)
        check("rule 7's check reports that orphan and only that orphan",
              [o.relative_path for o in orphans]
              == [o.relative_path for o in store.versions(source.key, "COH")],
              f"{len(orphans)} unrecorded version(s): "
              f"{[o.relative_path for o in orphans]}")

    finally:
        shutil.rmtree(root, ignore_errors=True)

    # -------------------------------------------------------- the API cross-check
    if "--cross-check" in sys.argv:
        print("\nCross-checking the clone against the hosted API (slow, network):")
        import json
        import urllib.parse
        import urllib.request

        query = (
            "SELECT `date`, `open`, high, low, `close`, volume FROM ohlcv "
            "WHERE act_symbol='AAPL' AND `date` BETWEEN '2017-10-24' "
            "AND '2017-10-26' ORDER BY `date` ASC"
        )
        url = (
            "https://www.dolthub.com/api/v1alpha1/post-no-preference/stocks/"
            f"master?q={urllib.parse.quote(query)}"
        )
        with urllib.request.urlopen(url, timeout=120) as response:
            api_rows = json.loads(response.read())["rows"]

        local = DoltCloneStocksSource().fetch_daily_bars(
            "AAPL", start=date(2017, 10, 24), end=date(2017, 10, 26)
        ).series.bars

        # Compared field by field, with the API's strings coerced, because the
        # two transports genuinely differ in JSON type — dolt returns volume
        # unquoted — and a raw dict comparison would fail on that alone.
        agree = len(api_rows) == len(local) and all(
            row["date"] == bar.date.isoformat()
            and row["high"] == str(bar.high)
            and int(row["volume"]) == bar.volume
            for row, bar in zip(api_rows, local)
        )
        check("the clone and the hosted API return identical values", agree,
              f"{len(api_rows)} API rows against {len(local)} local bars")
    else:
        print("\n(Skipped the API cross-check. Pass --cross-check to run it.)")

    # ------------------------------------------------------- the missing clone
    print("\nA misconfigured clone fails loudly rather than answering:")
    try:
        DoltCloneStocksSource(
            transport=__import__(
                "framework.data.dolt_clone", fromlist=["DoltCloneTransport"]
            ).DoltCloneTransport(database="data/nope")
        ).fetch_daily_bars("AAPL", start=date(2017, 10, 24), end=date(2017, 10, 26))
        check("a missing clone is refused", False, "it answered instead")
    except DoltCloneUnavailable as error:
        check("a missing clone is refused", "not a dolt clone" in str(error))

    print()
    if FAILURES:
        print(f"{len(FAILURES)} check(s) FAILED: {', '.join(FAILURES)}")
        return 1
    print("All checks passed against the live clone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
