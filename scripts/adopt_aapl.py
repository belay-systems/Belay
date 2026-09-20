"""Re-fetch the one series Belay holds, so that it stops being unprovenanced.

ADR-014 rule 8. `data/market/dolthub-stocks/AAPL/0001-a7dbcaf3fb6aba2d.bin` was
stored before any record was ever written — F-002 — and its fetch timestamp is
not recoverable, so **no retroactive record is written for it**. A record is
signed over `created`, and inventing one would file an Assumption under Facts,
which `constitution/Operational_Constraints.md:9-17` separates precisely so that
it cannot happen.

Instead the window is fetched again, now, through the same transport that
produced those bytes:

- **identical bytes** — `SeriesStore.store` returns the existing version 1, and
  the new record's `content_hash` proves it describes the file already on disk.
  The orphan is adopted without anything being asserted that was not observed.
- **different bytes** — the vendor restated. The new bytes land as version 2
  with a record of their own, and version 1 stays on disk permanently
  unprovenanced, which is a true statement about it rather than a loss.

The window is `2024-01-02` to `2024-02-09`, read out of the stored payload's own
`sql_query` fields rather than guessed: the two chunks it contains cover
`2024-01-02..2024-01-31` and `2024-02-01..2024-02-09`.

Kept as a script rather than a test because it needs the network. Run once.

    python scripts/adopt_aapl.py
"""

from __future__ import annotations

import hashlib
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from framework.artifacts.repository import ArtifactRepository  # noqa: E402
from framework.data.dolthub import DoltHubStocksSource  # noqa: E402
from framework.data.fetch_record import (  # noqa: E402
    fetch_and_record,
    orphan_versions,
)
from framework.data.store import SeriesStore  # noqa: E402
from framework.metrics.reporting import SamplePeriod  # noqa: E402

EXISTING = Path("data/market/dolthub-stocks/AAPL/0001-a7dbcaf3fb6aba2d.bin")
REQUESTED = SamplePeriod(start=date(2024, 1, 2), end=date(2024, 2, 9))
IDENTIFIER = "RPT-0001"


def main() -> int:
    store, repository = SeriesStore(), ArtifactRepository()

    before = EXISTING.read_bytes() if EXISTING.is_file() else None
    if before is None:
        print(f"No such file: {EXISTING}. Nothing to adopt.")
        return 1

    print(f"The unprovenanced file: {EXISTING}")
    print(f"  {len(before)} bytes, sha256 {hashlib.sha256(before).hexdigest()}")
    print(f"  orphans before: {len(orphan_versions(store, repository))}")
    print(f"\nRe-fetching {REQUESTED.start} to {REQUESTED.end} over HTTP...")

    fetch = fetch_and_record(
        identifier=IDENTIFIER,
        source=DoltHubStocksSource(),
        symbol="AAPL",
        requested=REQUESTED,
        store=store,
        repository=repository,
    )

    content = dict(fetch.record.content)
    adopted = fetch.stored.version == 1 and fetch.stored.path == EXISTING

    print(f"\n  bars:          {len(fetch.series.bars)}")
    print(f"  store version: {fetch.stored.version}")
    print(f"  store path:    {content['store_path']}")
    print(f"  content hash:  {content['content_hash']}")
    print(f"  record:        {fetch.record_path} (new={fetch.record_is_new})")
    print(f"  orphans after: {len(orphan_versions(store, repository))}")

    if adopted:
        print(
            "\nADOPTED. The bytes were byte-identical, so the store returned "
            "version 1 and the record describes the file that was already there."
        )
    else:
        print(
            "\nRESTATED. The vendor's answer changed: the new bytes are version "
            f"{fetch.stored.version} with a record, and version 1 remains on "
            "disk permanently unprovenanced. That is a vendor restatement "
            "observed in the wild and it deserves its own note."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
