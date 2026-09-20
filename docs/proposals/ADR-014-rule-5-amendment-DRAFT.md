# DRAFT — Amendment to ADR-014 rule 5

**Not ratified. Amending a ratified ADR is the owner's call.** No code changes
with this; the code already obeys the amended reading and is the reason the
defect is visible at all.

---

## What is wrong

Rule 5's **heading** is correct and survives the amendment untouched:

> **5. One record per stored series version, not one per fetch.**

Its **operative sentence** is the defect:

> Under this rule a fetch that produced no new store version produces no new
> record, and a fetch that differs produces both.

That sentence states a *test* — "did the store write a new version?" — which is
a **proxy** for the invariant in the heading, and the proxy is wrong in exactly
one case. That case is rule 8, in the same ADR:

> re-fetching the same window either returns identical bytes — in which case
> `framework/data/store.py:145-148` returns the *existing* version 1 and the new
> record's `content_hash` proves it describes the file already on disk, so the
> orphan is adopted

The adoption fetch **produces no new store version**. Rule 5's test therefore
forbids the record rule 8 requires, and the one file this ADR was written to
provenance is the one file its own rules cannot provenance.

**The heading was never in conflict with rule 8.** A stored version with no
record has zero; writing one takes it to one, which is what "one record per
stored series version" asks for. Only the proxy conflicts.

## What the code does

`fetch_and_record` (`framework/data/fetch_record.py:387-405`) asks a third
question neither rule states: **does a record already cover these bytes?**

```python
existing = records_by_stored_version(repository).get(
    (stored.relative_path, stored.content_hash)
)
if existing is not None:
    ...  # return the existing record, record_is_new=False
```

That reading satisfies both rules. The adoption writes a record because nothing
covered those bytes; an ordinary unchanged re-fetch writes none because
something does.

## Proposed replacement text

Replace the operative sentence with:

> **Under this rule a fetch whose bytes already have a record produces no new
> record, and a fetch whose bytes have none produces one — whether or not the
> store wrote a file.**
>
> **The test is the record, not the write, and the difference is rule 8.** "Did
> the store write a new version" reads as the same question and is not: the one
> case where the two diverge is bytes that were already on disk without a
> record, which is precisely the AAPL file rule 8 adopts. Its adoption fetch
> stores nothing new and must still write a record, so a rule keyed on the write
> would forbid the only act this ADR exists to make possible.
>
> **This requires a lookup from stored bytes to their record, and the ADR as
> ratified did not name one.** `records_by_stored_version` in
> `framework/data/fetch_record.py` is it, keyed on the pair
> `(store_path, content_hash)` — the path as well as the hash, because two
> symbols whose payloads collide on a hash alone are not the same stored
> version, and returning the exact version rather than `latest()`, because an
> identifier can hold more than one. It follows that an artifact the walk cannot
> read is a **stop, not a skip**: an unreadable record is indistinguishable from
> an absent one, and an absent one is what this rule reads as "these bytes are
> new".

The cost paragraph that follows ("What this rule costs, stated rather than
buried…", the ~723 KB per symbol per year arithmetic) is **unaffected** and
should stand as written. What it prices is confirmations that a re-fetch found
nothing changed, and the amendment does not change whether those are recorded —
under both readings they are not.

## Amendment note, for the ADR's Status block

> **Rule 5 amended <date>.** Its operative sentence tested whether the store
> wrote a version, which contradicted rule 8 in the same document: rule 8's
> adoption fetch stores nothing and must still produce a record. The heading and
> the intent were correct; the test stated under them was a proxy that fails on
> exactly the case the ADR was written for. The code was already correct and is
> unchanged by this amendment — it was implemented against the intent, and the
> gap between the two is what surfaced the contradiction. Recorded as
> `docs/HANDOFF.md`, "ADR-014 Rules 5 And 8 Cannot Both Be Executed As Written".

## One correction the amendment should carry with it

**Rule 5's own citation is now stale, and it was correct when ratified.** The
rule opens `framework/data/store.py:137-141` already rules the parallel case and
gives the reason` and then quotes "nothing was restated, so there is no new fact
to record". That quote lives at `store.py:148-151` today; lines 137-141 are the
sort comment inside `versions()` and the `def latest` line.

Verified, rather than asserted:

```
$ git show 48511a8:framework/data/store.py | awk 'NR>=137 && NR<=141'
        A re-fetch whose bytes are identical returns the existing version rather
        than writing a second copy: nothing was restated, so there is no new
        fact to record, and the version count keeps meaning "number of times the
        vendor's answer changed".

$ awk 'NR>=137 && NR<=141' framework/data/store.py
        # Sorted on the parsed integer rather than the filename, so the ordering
        # does not depend on the padding width being sufficient.
        return tuple(sorted(found, key=lambda stored: stored.version))

    def latest(self, source: str, symbol: str) -> StoredSeries | None:
```

`48511a8` is the commit that ratified ADR-014. The citation was exact then and
was broken by `a19c24e`, the commit that implemented it — the same failure mode
F-003's own repointing note records, one level up, inside a ratified document.
It is not the only one; see the finding recorded separately.

## Two things the amendment deliberately does not settle

1. **The invariant is enforced on one path only.** `fetch_and_record` dedups;
   `fetch_record()` does not, and it can be called directly and saved by the
   caller. Two records covering one stored version is therefore reachable, and
   nothing detects it — rule 7's orphan check reports versions with *no* record,
   never versions with two. Recorded separately as a new finding rather than
   folded in here, because closing it is a code change and this is a wording
   correction.

2. **Whether `record_is_new=False` should be observable in the artifact root.**
   Today the fact that Belay asked again and got the same answer lives only in
   the return value of one call. That is the cost the rule already prices and
   leaves open; the amendment does not reopen it.
