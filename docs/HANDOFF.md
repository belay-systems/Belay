# Belay Session Handoff

## Provenance — read this first

**Belay's recorded history begins with this repository's first commit.** These
documents were written while the platform was called Atlas, in a separate
repository of that name which stays private, and are reproduced in full here.

Four things follow, for anything you read below or in `docs/`, `reports/`,
`framework/` and `CHANGELOG.md`:

- **Ids, pull request numbers and Issue numbers dated before Belay's first
  commit refer to that private archive and will not resolve here.** They are
  kept as written: they are the evidence trail this repository rests on.
- **The platform was renamed Atlas -> Belay on 2026-09-20** by the owner's
  ruling (`docs/OwnerDecisions.md` Part 14). It was applied to these records as
  well as to the code, so a document dated before that day may read "Belay"
  where it said "Atlas" at the time. The originals are in the private archive.
- **Where a sentence names the archive repository it still says Atlas**, because
  that repository is genuinely named Atlas. Most URLs were left pointing at it;
  three an operator must follow were repointed, and five file paths renamed.
- **"This repository" in a dated record means the Atlas archive, not Belay.**
  Records written before publication say the repository is private. That was
  true of the archive, which stays private. **It will not be true of Belay once
  it is public**, and ADR-013 rests on that premise — see Part 14g.

---

## Current Repository State

**Corrected 2026-09-19 at session close-out — F-022**
(`reports/review/2026-09-04-review.md:267`; `docs/OwnerDecisions.md:1207`, Part
9d, rules that the correction happens here, at close-out, rather than in a
register commit). Everything from "State As Last Written, 2026-08-02" onward
below is kept exactly as written — Immutable Law VII — because it was true the
day it was written and has since gone seven merged pull requests stale rather
than wrong. This paragraph and the block immediately following it are what is
current as of 2026-09-19; trust `python scripts/status.py` over either.

Repository (the private Atlas archive, where this session ran — not this one):
`pewpewpressco-ux/Atlas`

Last session:
2026-09-19

Session focus:
**Session close-out only — this commit closes it.** No framework code changed
this session; the work was governance — registering the 2026-09-04 and
2026-09-11 review findings, closing three of them, drafting (not ratifying)
ADR-015, and correcting this section. See `# Completed This Session
(2026-09-19)` below for the full account and `# Highest Priority Next Task`
for what is next.

**On `main`, at `cc80866`.** Three pull requests merged 2026-09-19 — #6
(`a4e7a2a`, the review cadence gate), #7 (`b5e17d9`, the 2026-09-04 review
report) and #8 (`3af14a6`, the 2026-09-11 review report). `git log --merges
--oneline main` lists all three and nothing else since `fb5b919`. CI (the
`conformance` workflow) is green on `cc80866`: run `35447797882`.

**Not on `main`, open as draft pull requests.** #9
(`register/2026-08-21-corrected` @ `387254e`) registers F-014..F-018 and puts
`docs/OwnerDecisions.md` Part 9 (9a-9e) on file. #11
(`register/2026-09-reviews`, this branch) registers F-019..F-030 and closes
F-021, F-026 and F-022. #10 (`adr/015-stage-is-carried` @ `9196a0b`) carries
ADR-015, **PROPOSED, not ratified**. #4 (`register/2026-08-21-findings`) is
superseded by #9 and remains open — closing it is an owner action, recorded in
`docs/OperatorChecklist.md`.

**Suite: 635 passed, 1 skipped, 5 xfailed** (`python -m pytest -q`; this
branch and `main` agree, because the register commits touch no code).
**`python scripts/status.py` reports open findings 42** on this commit (43
immediately before it — F-022 closes here). **14 ADRs** are on file
(`grep -c "^## ADR-" docs/DECISIONS.md`); ADR-015 is not among them — it
exists only on PR #10's branch, and it is unratified there too.

**This is a snapshot, not a mechanism, and it goes stale the moment anything
merges — the exact condition this paragraph corrects.** Re-derive it with:
`git log --oneline -12 main`; `git log --merges --oneline main`;
`python -m pytest -q`; `python scripts/status.py`;
`grep -c "^## ADR-" docs/DECISIONS.md`; `gh pr list --state all --limit 15`;
`gh run list --branch main --limit 3`. Nothing forces that re-derivation to
happen — F-022's underlying cause, that this section is corrected by
convention rather than by anything that checks it, is **not** fixed by this
commit. See F-022's entry in `# Closed Findings` for exactly what was and was
not done.

**Corrected again 2026-09-19 (evening), by the same convention rather than a
rewrite.** Kept above exactly as written; superseded by this paragraph.

**On `main`, at `3080848`.** Two further pull requests merged since the
paragraph above was written: #9 (`2f44c19`) and #11 (`3080848`, retargeted from
`register/2026-08-21-corrected` to `main` before merging) — both owner-approved,
`docs/OwnerDecisions.md:1300` (Part 10a). PR #4 is `CLOSED`, superseded by #9,
per `docs/OwnerDecisions.md:1361` (Part 10c).

**Open pull requests: #10 and #12, both draft, and this one.** #10
(`adr/015-stage-is-carried`) carries ADR-015, still PROPOSED and unratified.
#12 (`fix/review-skill-numbering` @ `01c1e24`) fixes the review skill's
numbering instruction and closes F-025; CI green on all five checks; **not
merged** — `docs/OwnerDecisions.md:1589` (Part 10j) records that an unattended
merge of it was refused by Claude Code's own permission control. This pull
request is stacked on `fix/review-skill-numbering` for that reason, and
retargets to `main` once #12 merges.

**Suite on this branch: 638 passed, 1 skipped, 5 xfailed** (`python -m
pytest -q`). **`python scripts/status.py` reports open findings 41** on this
branch before this pull request's own changes (42 on `main` before #12's F-025
closure; 41 after it, on `fix/review-skill-numbering`). **14 ADRs** are on
file; ADR-015 still exists only on PR #10's branch and is unratified there.

Re-derive with the same commands as the paragraph above.

---

### State As Last Written, 2026-08-02 (superseded 2026-09-19 — F-022; kept as the record of that session, Law VII)

Repository (the private Atlas archive, where this session ran — not this one):
`pewpewpressco-ux/Atlas`

Last session:
2026-08-02

Session focus:
**F-002 is closed and ADR-014 is implemented in all nine rules.** The first
artifact this repository has ever kept is `artifacts/RPT-0001/1.0.0.yaml`, a
signed fetch record for the one AAPL series Belay holds — adopted rather than
back-dated, because a re-fetch returned byte-identical data and the store handed
back the version that was already there. No retroactive record was written; the
original fetch timestamp was never recoverable. Suite 594 → 626.

**The number that matters more than the feature: an independent pass over this
work found 19 defect-grade errors across 93 claims, and the author's own review
found none of them.** Eight were in committed code, including a dedup that
collapsed two symbols with identical bytes into a single record and an orphan
check that then reported the store clean. All eight are fixed with regression
tests confirmed red against the pre-fix code. **And the pass ran after
implementation when ADR-014 requires it before** — two documents written in one
session gave opposite orderings for that step.

Earlier the same day:
**ADR-014 was drafted and ratified.** F-002 said no fetch record has
ever been written to disk and that `.gitignore:46-49` rests on the belief that
they are. That is a ruling rather than a repair — no document in `Knowledge/` or
`docs/` names a directory for artifacts, and `ArtifactRepository(root)` has always
made every caller pick one — so ADR-014 rules where artifacts live (`artifacts/`,
tracked, named by a module constant), that `fetch_and_record` persists, that the
AAPL bytes get **no retroactive record** because their fetch timestamp is
unrecoverable, and what a `.gitignore` comment may assert. **Nothing was
implemented, deliberately.** See `★ START HERE` for the order the work has to run
in and why it is not free to reorder.

**The measurement that changed a rule: at Belay's chosen daily cadence, the
tracked record is 3.7× the size of the ignored payload** — 2,732 bytes against
~747 — and 1,535 of those record bytes are the survivorship constant, which rule 5
forbids deduplicating. `.gitignore`'s "nothing is lost by this" compares the wrong
two quantities and does not come back in any wording.

**Three findings opened by drafting it, three for three across ADR-010, ADR-013
and ADR-014.** The record carries `source.name` while the store is keyed on
`source.key`; four digits means 10,000 `RPT` identifiers ever, permanent, against
a 6,000-symbol backfill; and an identifier reused at a *new version* is accepted
and silently mis-filed as that artifact's history. The third was found by running
it. **The second blocks ADR-014 rule 4.**

Earlier the same day:
**F-001 and F-005 are closed.** A strategy can no longer be born past `IDEA`, and
`DailyBarSeries` no longer accepts the same trading day twice. Suite 584 → 594.

2026-08-01:
**Finding 14 is closed. Belay can complete a multi-year backfill for the first
time** — three years of AAPL, 754 daily bars, in **4.4 seconds** against roughly
25 minutes and frequent failures over the hosted API. `framework/data/dolt_clone.py`
is a second implementation of the `Callable[[str], bytes]` seam that already
existed, so `MarketDataSource` did not change and neither did the parsing, the
chunking or the survivorship answer. Suite 551 → 584.

**The number that has not improved in three sessions: an independent pass found
6 defect-grade errors across 65 claims, and the author's own pass found none of
them.** The worst was a `survivorship` property override added "to make the
inheritance explicit" — inert, and it defeated the guard that catches a subclass
skipping `super().__init__()`. The guard held on the HTTP branch and was defeated
on the clone branch, demonstrated by running it. **Self-certification is still
not verification**, on code whose tests were written first and were all green.

**The transport ceiling produced a fifth wrong reading on the way out.** An
11-day novel window measured 37.4s where the recorded table says 8 days took
0.4s. The fast figures were warm-cache readings all along.

Earlier the same day:
**ROADMAP Stage 2 is built. ADR-013 is implemented in all ten rules, and Belay
can obtain a price series from a named source with provenance on the resulting
evidence.** Suite 388 → 520. `framework/data/` exists where nothing did.

**The sentence that was true of every number Belay had ever computed — that the
series was supplied by hand and describes no real instrument — is now false by
construction.** `disclosure_from()` builds a metric's `data_source` and
`sample_period` from the fetch itself, so neither is typed at a call site.

**The finding worth carrying out of this session is not in any document Belay
had: the free equity source is survivor-only in its prices.** `SELECT date,
act_symbol, close FROM ohlcv WHERE act_symbol='COH'` returns zero rows in every
window tried, while AAPL returns rows in the same window — Coach traded actively
until October 2017 and has no history at all. Meanwhile the `symbol` table
*retains* dead tickers with a `last_seen` date, 23,827 rows against roughly
6,000 listed. **It fails the delisted-prices half and partly passes the universe
half**, which is the reverse of the expected shape and exactly the "a source can
pass one and fail the other" case rule 5 describes. Under rule 9 that is a
legitimate *established* answer, and rule 5 now bolts it to every artifact.

**Two of ADR-013's Required Follow-Ups are closed against the source rather than
against a document.** The options database is CC BY-SA 4.0 (its own `LICENSE.md`,
via `SELECT doc_name, doc_text FROM dolt_docs`), and it **does** retain expired
contracts — a chain expiring 2019-03-15, observed 2019-03-02, is still queryable
in a database whose newest row is 2026-07-31.

**One thing failed and is recorded rather than worked around: the DoltHub SQL
API cannot serve a backfill.** See `The transport ceiling` below.

Earlier the same day — the previous session:
**ADR-013 is Accepted and Stage 2 is unblocked. No code was written and none was
meant to be.** The owner answered the questions no document could, the repository
went private, and the data-boundary ruling was drafted, independently verified,
corrected and ratified in one sitting.

**The number worth carrying out of that session: an independent verification pass
found 3 defect-grade errors that the author's own pass missed, out of 4 total.**
One of them was a ratified-ADR rule resting on a fact no file in the repository
contained. Self-certification is not verification, and that lesson cost nothing
this time only because the pass ran before implementation.

Earlier the same day:
**A scoping session, not a build session. No code was written and no ruling was
made.** Finding 10's four open questions were each tested against the documents
that already exist, and the answers are in the new `docs/EndState.md`. **Two of
the four turn out to be rulable from documents alone; one cannot be ruled by any
amount of reading; and the question that actually blocks ROADMAP Stage 2 is not
the one anybody expected.** See `The Four Questions Were Not Four` below.

Earlier the same day:
**ROADMAP Stage 1, then the first of the seven constitutional criteria. Two
ADRs ratified and implemented, and the dashboard moved from 1 of 7 promotion
criteria computable to 3 of 7** — it had never moved before today.

**ADR-012 is the second, and it is the one with teeth.** Belay can now ask
whether a track record is distinguishable from luck.
`constitution/Promotion_Pipeline.md:27` defines maturity Level 2 **as** "Passed
statistical review" — the only one of the seven levels defined by passing a test
— and `constitution/Capital_Authority.md:11-14` makes `Statistical edge` one of
six inputs that determine capital. Seven documents demand statistical validity
and not one of them defines it. See `ADR-012` below.

Suite 231 → 387 across the session.

**ADR-011 first: Belay can compute a risk-adjusted return.**

Four of the nine metrics `Validation/Backtesting.md` requires are now built
where one was: CAGR, volatility, Sharpe and Sortino, plus the shared reporting
helper that makes the document's disclosure requirement executable. Suite 231 →
318.

**The ruling was necessary rather than ceremonial.** The document names nine
metrics and defines none of them, and four cannot be computed at all without a
convention no Belay document states. ADR-011 rules that none of them is
defaulted: the risk-free rate, the target return and the period count are
required arguments, and every one of them is recorded inside the artifact's
signature beside the number it produced.

**Two claims in this document's own brief for the session were wrong, and are
corrected below rather than quietly dropped.** Both were caught by opening the
files. One of them changed the scope of the work.

**A third error was caught in the ADR itself, by a second reader, before any
code was written.** Twenty citations checked, four wrong — including one that
was self-refuting. See `The Verification Pass Earned Its Place` below.

---

Earlier still, the same day:
**Two small things, both finished. `ArtifactRepository.get()` exists, so the
repository can hand back an artifact rather than a version number; and
`strategies/Lifecycle.md` is annotated, which closes `Four Different Promotion
Sequences`.** Open findings 10 → 9. No ADR was needed for either, as expected.

The one real decision was whether `get()` verifies integrity on read. It does,
and the reasoning is written into the method rather than here — the short version
is that `save()` can only vouch for a file at the moment it lands, and a YAML
edited on disk afterwards is invisible to every write-time check.

**Then, with the window left over: three of the four weak `xfail` watchers were
strengthened.** Each now parses its governing document instead of a list copied
out of it. All three still `xfail`, checked with `--runxfail` to be failing for
the intended reason rather than on a parser bug.

**Then the two deferred questions were taken up, and only one of them was a
ruling.** The workflow-registry one turned out to be factual — opening both
`StrategyPromotion.md` documents settled it, and widened its finding: not one of
the thirteen workflow documents defines all five things `workflows/README.md`
requires.

**The `ArtifactType` one was a real ruling. ADR-010 is Accepted and implemented.**
All 31 departmental and workflow documents were read to draft it: the deliverables
were counted rather than estimated, and the count changed the answer.
`DeliverableType` now carries twenty-four members parsed from the eleven
documents that declare them, and `Artifact` carries a `deliverable` alongside its
`type`. **The longest-open P2 finding is closed, and so is the weak-watcher
finding** — all six watchers are honest for the first time.

**One new finding, found by implementing rather than by reading.** ADR-010 rule 9
had to map deliverables onto `ArtifactType`, which meant comparing it against
`Knowledge/Identifiers.md` for the first time. They disagree, and three
deliverables now map to types that cannot receive a truthful identifier.
Demonstrated against the running code, not inferred.

Open findings 10 → 8 across the session.

Previous session:
**ADR-009 ratified and implemented: Belay can record that a review happened.**
Three ratified obligations had been waiting on this one component, and all three
are now discharged — ADR-004 rule 4 (written justification for a demotion, not
enforced anywhere since the day it was ratified), ADR-004's re-sizing step, and
ADR-008's `Remain Current Stage`.

**Artifacts can also be read back for the first time.**
`ArtifactSerializer.load()` exists, so an artifact is no longer write-only. The
acceptance test is the round trip through the signature, not through field
equality.

The ADR-006 and ADR-007 follow-ups were applied, and the two ADR-008 document
corrections that ADR-009 unblocked: `ReviewTemplate.md` says `Remain Current
Stage`, and `CapitalReview.md` now defines `Reject`.

One new finding, about this document's own machinery: **all four remaining
`xfail(strict=True)` tests are weaker than their names.** Six audited, six
defective.

Test suite:
584 passing, 5 xfail, 1 skipped. Run `pytest` from the repository root, or
double-click `refresh-status.cmd` for the dashboard.

**This number is not to be trusted and the dashboard is.** It read `388` until
2026-08-01 — stale by 196 across three sessions that each wrote code and each
left it alone, in the very paragraph that exists to warn about the drift. It had
already been caught once at a size of one, described then as "the '46 passing'
drift the roadmap already records, at a smaller size", and it then drifted by
four hundred times that. **A number maintained by hand in a document nobody reads
top-to-bottom will go stale**, which is the argument for `refresh-status.cmd`
re-deriving it and for this document deferring to it.

---

# The Structural Change

Every defect found this session was found the same way: a person read a governing
document, then read the code, and noticed they disagreed. Nothing was watching, so
the disagreements accumulated invisibly for months.

`tests/test_governance_conformance.py` is what watches now.

Most of its tests assert conformances that hold today — the strategy lifecycle
against `Paper_First_Capital_Doctrine.md`, the artifact lifecycle against
`Knowledge/ArtifactLifecycle.md`, evidence levels against `Evidence_Standards.md`,
identifier prefixes against `Knowledge/Identifiers.md`, the integrity payload
against `Governance.md`, the demotion table against ADR-004, and the deliverable
vocabulary against the eleven documents that declare it. If code drifts from the
constitution, the suite goes red.

The counts are deliberately not written here. They were carried as "eleven" and
"seven" long after both had changed; `refresh-status.cmd` re-derives them, and
the dashboard is what this document tells you to trust over itself.

The rest use `xfail(strict=True)`, each citing the section below that explains it.
While a gap is open the test fails as expected and the suite stays green — but the
gap lives in the test suite rather than in prose. When someone closes it, the test
passes unexpectedly and `strict` turns the suite red to say so. Verified:
`XPASS(strict)` does fail the run.

Markers cite section **titles**, not finding numbers. Numbers renumber whenever a
finding closes, and markers left pointing at an old numbering was itself a finding
— closed this session by removing the thing that goes stale rather than by
refreshing it.

The backlog maintains itself. No future session needs to rediscover any of it.

---

# Completed This Session (2026-09-19)

**Session close-out, per `AGENTS.md` steps 13 and 14.** One commit on
`register/2026-09-reviews` (PR #11), stacked on draft PR #9. No framework code
changed this session — the work is governance and registration.

**Preconditions of the session brief verified.**
`docs/proposals/register-rebuild-session-brief.md`'s Phase 1 ran: `python -m
pytest -q` returned 635 passed, 1 skipped, 5 xfailed, and `python
scripts/status.py` reported open findings 28 — the baseline before this
session's own registration work added to it.

**The cloud review routine fired once, as a verification rather than as a
review.** Cloud run `cse_<id>` made one tool call —
`python scripts/review_due.py` — which printed `SKIP - last review was 8 days
ago (2026-09-11-review.md, on main). Next due 2026-09-23.`, exited 1, and
wrote nothing. `/belay-review` was **not** run. Next due 2026-09-23; next
**scheduled** firing 2026-09-25.

**Phase 2 — the register was rebuilt, not rebased.** PR #9
(`register/2026-08-21-corrected`; commits `f6fb971`, `9ff5a58`, `387254e`):
F-014 to F-018 registered, the four withdrawn duplicates absent, and
`docs/OwnerDecisions.md` Part 9 (9a-9e) put on file. PR #11
(`register/2026-09-reviews`; commits `4a96cac`, `9dc6ff9`, `eddf57e`, `86bfeac`,
`e6cb8de`, `eb7120b`, and the citation-fix commit that follows): F-019 to F-030 registered, and F-021, F-026 and F-022 closed.

**Phase 3 — F-007 reproduced on `main`'s code.** Open paths: a bare
`Artifact(...)` plus `ArtifactIntegrity.sign()`, `ArtifactSerializer.load()`,
a hand-edit re-signed, and `dataclasses.replace()` plus `sign()`. Closed
paths: `ArtifactFactory.create()` (`framework/artifacts/factory.py:61-71`) and
an unsigned hand-edit through `ArtifactRepository.get()`
(`framework/artifacts/repository.py:185-190`). The "birth is version 1.0.0
with no `parent_hash`" candidate definition was rejected on executed
evidence.

**Phase 4 — ADR-015 drafted, PROPOSED, on PR #10.** Commits `2717e76` →
`13d188d` → `d734bcb` → `9196a0b` on `adr/015-stage-is-carried`. It covers
F-007 and F-014 together (`docs/OwnerDecisions.md:1231`, Part 9e-ii).
**Not ratified.** Ratification is blocked on the owner's ruling on the
evidence-bar proposal, which exists only **on PR #10's branch** as
`docs/proposals/evidence-bar-per-rung.md` — named here rather than cited as a
`path:line`, because it is not a resolvable path on this branch.

**Phases 5 to 8 not started, deliberately.** Tests are written from a ratified
shape, and nothing about F-007 or F-014 is ratified yet.

**Independent verification record for the session — this repository's running
evidence that self-review does not work.** PR #9, first pass: the author
reported 0 problems; an independent pass found 10, 2 of them blockers.
ADR-015 v1: an independent pass found 11, 3 blockers. ADR-015 v2: 9, 2
blockers, including a one-file forgery that returned `PRODUCTION` from
`get()`. PR #9's fix plus PR #11: 11 found, 0 blockers. A Haiku inventory
agent fabricated `docs/HANDOFF.md` contents during the session; discarded
after a `grep` check against the real file, and nothing was built on what it
returned.

**Owed and not done.** A third independent pass on ADR-015, after the
evidence bar is filled in. An independent pass on the evidence-bar proposal
itself, before the owner rules on it. And an independent pass on this
close-out commit, scheduled after it lands.

---

## Evening addendum (2026-09-19) — eleven owner selections, two research proposals, one merge that stayed manual

**What this covers.** After the close-out above, the session continued on
standing authorisation and put eleven further questions to the owner, recorded
verbatim-selection style as `docs/OwnerDecisions.md` Part 10 (10a-10k). This
addendum states what happened; Part 10 is the authority.

**The register landed.** PR #9 merged as `2f44c19`, then PR #11 (retargeted to
`main`) merged as `3080848` — both owner-approved (10a), the first attempt
blocked by an automated permission check and then explicitly approved. PR #4
was closed as superseded by #9, not deleted (10c).

**The review skill's numbering fix shipped as PR #12** (`fix/review-skill-numbering`,
commits `40adc86`, `b0864f2`, `01c1e24`), owner-authorised (10d) and
independently attacked twice before this pull request opened — **7 defects**,
then **4 more**. CI is green on all five checks. **It is not merged**: see
below.

**Two research proposals were run, each independently attacked once.** The
evidence-bar proposal on PR #10's branch (evidence-bar-per-rung.md under
docs/proposals/ there — not a resolvable path on this branch, so named
without backticks; owner-authorised in 10b): **17 defects, 4 blockers**, all applied at `8e3edb2`;
seven owner questions remain, and ADR-015 stays PROPOSED and unratified. The
sample-adequacy proposal for F-004 (`docs/proposals/sample-adequacy-definition.md`,
this pull request, owner-ruled shape in 10e): **15 defects, 5 blockers**, all
applied; seven owner questions remain and it has not had a second pass.

**F-004 and F-006 moved from flatly unruled to partially ruled.** F-004 is
ruled as to shape (10e) with its numbers still open; F-006's narrow fix is
authorised (10f) and its wide question is ruled as calendar-proposal-first with
gaps failing closed once a calendar exists (10g). Corrected in place at every
location that previously stated F-004 or F-006 as unruled without
qualification — see Part 10e-g and this document's own F-004/F-006 entries
above.

**The publication scan ran and came back clean.** 291 commits, 37 refs, 12
PRs, 20 Actions runs at scan time; no secrets, no MUST-FIX; six owner's-call
items now in `docs/OperatorChecklist.md`. **The repository is still private**
— re-verified this session. A local pre-push guard refusing direct pushes to
`main` was installed in this clone only (10k).

**A usage limit interrupted two agents mid-task during the evening, and both
were resumed or re-run** rather than left half-done; nothing here rests on an
interrupted pass that was not either completed or redone.

**The one thing that did not go as asked: unattended merging.** The owner
authorised merging this session's own records/docs pull requests to `main`
unattended, after a fresh independent pass and green CI (10j). **Claude Code's
own "Merge Without Review" permission classifier refused it anyway**, and nothing
in the session worked around that refusal. So PR #12 and this pull request both
wait on the owner's own merge, in that order.

---

# Completed In The Previous Session (2026-08-01)

## ROADMAP Stage 2: the market data boundary is built

**All ten ADR-013 rules are implemented.** `framework/data/` is new and is the
home ADR-002 requires; `framework/services/` was left as the ten four-line
placeholders it was rather than gaining an eleventh.

| Rule | Where it lives |
|---|---|
| 1 provenance on the consuming artifact | `fetch_record.py`, `disclosure_from()` |
| 2 two contracts, no shared base | `contract.py` — `MarketDataSource.__mro__` is asserted to be exactly `(MarketDataSource, ABC, object)` |
| 3 the fetch record, not the series | `fetch_record.py` — `REPORT`, `deliverable=None`, SHA256 of the payload inside the signature |
| 4 stored, versioned, never overwritten, out of git | `store.py` and `.gitignore` |
| 5 survivorship as a fixed constant naming the direction | `survivorship.py` — `SURVIVORSHIP_DIRECTION` |
| 6 the contract expresses equities *and* options | `contract.py` — `InstrumentClass`, `OptionChain`, `fetch_option_chain` |
| 7 `sample_period` is two dates | `reporting.py` — `SamplePeriod` |
| 8 no evidence grade on a fetch record | `fetch_record.py` — `evidence=()`, so `strongest_evidence_level` returns `None` |
| 9 an unstating source is refused | `contract.py` — `MarketDataSource.__init__` |
| 10 not a `Market Snapshot` | `fetch_record.py`, asserted in `test_fetch_record.py` |

**Rule 7 could not be implemented the obvious way, and the reason is worth
keeping.** Splitting `sample_period` into `sample_period_start` and
`sample_period_end` turns the suite red:
`tests/test_governance_conformance.py` parses `Validation/Backtesting.md` and
holds `Disclosure`'s field **names** to the document. So the rule changes the
field's **type** — `sample_period: SamplePeriod` — and the two dates are rendered
into `content` as encoded ISO strings, because `canonical_digest`'s own docstring
asks callers not to rely on its `default=str` backstop. Cost was zero exactly as
the ADR predicted: `git ls-files "*.yaml"` still returns nothing.

### The independent verification pass, and the third consecutive time it earned its place

**44 claims checked, 15 wrong or questionable, 6 defect-grade. The author's own
pass found none of the six.** That is a worse ratio than ADR-013's own drafting
scorecard (4 defect-grade, author caught 1), and it happened on code whose tests
were written first and were all green.

**The worst one undid the point of the session.** Rule 5 requires the
survivorship answer to be a fixed constant "on every artifact **derived from the
source**". The implementation fixed the constant *inside*
`SurvivorshipDisclosure` and then let the caller choose which disclosure object
to pass, alongside a caller-supplied `source_name` **string**. The pass
demonstrated the consequence: a fabricated `RETAINED / RETAINED, basis="trust
me"` disclosure paired with the real source's name produced a signed artifact
whose `known_limitations` mentioned no survivorship bias at all. **The test named
"a caller cannot substitute a kinder survivorship disclosure" asserted only that
an unknown keyword raises `TypeError`** — it would have passed for any
misspelling and defended nothing.

Fixed by removing the parameter rather than validating it: `fetch_record()` and
`disclosure_from()` now take the **source object** and read the disclosure off
it, `survivorship` is a read-only property, and `_survivorship_of()` re-checks at
the point the answer enters a signed artifact — because a subclass skipping
`super().__init__()` bypassed the constructor guard entirely.
`tests/data/test_survivorship_cannot_be_softened.py` is new and tests the
guarantee the old test only named.

**The second: rule 4 was not wired to anything.** `SeriesStore` existed, was
tested, and had no caller outside its own test file. `fetch_record()` took the
payload, hashed it and discarded it — so every signed record carried a
`content_hash` pointing at bytes nobody kept, which is rule 4's own argument for
storing, describing the code. `fetch_and_record()` now does the three acts
together, because separating them is how the failure stays silent.

**The third: the IBKR adapter was non-deterministic.** `span_days = (date.today()
- start).days` made the request a function of the day it ran, so an identical
re-fetch tomorrow returned different bytes and a different content hash — rule
3's guarantee broken in the exact direction `dolthub.py` reasons at length about
avoiding. **The test written to catch this passed against the defect**, because
both its calls ran on the same calendar day; it now asserts the span the request
actually carries.

Three more were documentation defects: a stale measurement left in a code
comment as the stated basis for the chunk size, a test docstring claiming
"eighty seconds per symbol" where the repository's own figure is 6.6 hours
(wrong by ~300×, the same shape as the `Knowledge/Schema.md` miscount), and
**ADR-013's Status block still reading "Not implemented" one commit after
`0a6d5f7`, whose whole subject was closing stale ADR-013 statuses.**

**And a failure mode this repository had not previously named: implementing a
document invalidated its citations.** ADR-013 rule 1 cited
`framework/metrics/reporting.py:58` and rule 7 cited `:59`; both were correct
when written and were broken by inserting `SamplePeriod` above `Disclosure` — in
obedience to rule 7. Repointed to `:125` and `:132`, and marked.

Also fixed from the same pass: the store's `_slug` was not injective, so `DYN$A`,
`DYN/A` and `DYN A` shared one version chain and `latest()` for one could return
another's bytes; the symbol regex used `$`, which admits a trailing newline; and
three more tests asserted tautologies over their own fixtures.

### The transport ceiling — a failure, recorded rather than worked around

The boundary works. **The DoltHub hosted SQL API does not scale to a backfill**,
measured on 2026-08-01 against the live database:

| window | result |
|---|---|
| 8 days | 7 bars, 0.4s |
| 1 month | 22 bars, 0.5s |
| 6 weeks | 31 bars, 0.6s |
| 2 months | 42 bars, 28.8s |
| 3 months | `context deadline exceeded`, **3/3 attempts**, ~54.5s each |
| 1 year, 13 years | `context deadline exceeded` |

The adapter now chunks on **calendar months** — boundaries that depend only on
the requested window, so the concatenated payload and therefore the content hash
stay comparable across re-fetches, which a tunable chunk size would have broken.
**But a novel month-sized query still times out**: April 2024 failed twice at
54.5s, and the same month in weekly chunks succeeded at 0.6s / 33.4s / 33.8s /
43.3s — **111 seconds for one month**, so thirteen years is roughly 6.6 hours per
symbol.

**The first measurement was wrong and the correction is the point.** A one-month
window returned in 0.5s once, and that number is what the chunk size was chosen
against; it does not hold for windows the server has not served before. An
initial diagnosis blaming the primary key ordering was also wrong — the same
query returned in 0.4s moments later.

**Dolt's intended path is `dolt clone`** — pull the database locally and query at
full speed. Not built, because swapping the transport was not the sanctioned
scope. Open finding 14.

### A second adapter, to prove the contract is one

`framework/data/ibkr.py`. **It has never run against the live IBKR API and says
so inside its own survivorship basis**, so the admission travels onto every
artifact rather than sitting in a comment. Verification needs a funded account
and a paid subscription. What it does prove is that the contract accommodates a
structurally different vendor — epoch-millisecond timestamps and JSON floats
against ISO dates and decimal strings, a duration-based request against a
date-range one — without `MarketDataSource` changing.

**IBKR does not solve the problem, and this is the finding that settled the
vendor question.** Its own documentation states "the API always requires Level 1
streaming real time data to return historical data", so historical data is not
included with an account; and "if data is not available for a specific
instrument, data type, or period within a TWS chart it will also not be available
from the API" — a delisted instrument has no chart. **IBKR costs money and buys
the same survivorship limitation.** The fee is waivable above a monthly
commission threshold, which a paper-first system generating no commissions cannot
reach.

**Using the broker as the data source would not violate rule 2.** Rule 2 forbids
a shared *abstraction*, not a shared vendor. `MarketDataSource` has no order
vocabulary and a test asserts it never acquires one.

### The distinction that decides when to buy data

**Survivorship bias is not "this data is wrong" — it is "selecting from this data
is wrong".** A backtest of AAPL from 2011 is unbiased for AAPL, which survived.
The bias enters when instruments are *chosen* by screening a survivor-only
universe, because everything that failed was removed before anyone looked. So the
free source is adequate for named-instrument work and inadequate the moment Belay
screens — which ADR-013 already forbids until Stage 3. **The trigger to buy data
is precise: the first time Belay selects instruments rather than being handed
them.** Norgate carries 25,222 delisted securities back to 1950 at its Platinum
or Diamond tier; 2026 pricing was not established and is not claimed.

---

# Completed Previously (2026-07-31)

## ADR-013 Drafted: The Data Boundary

**Status Proposed. Not ratified, not implemented.** `docs/DECISIONS.md`. It is
what ROADMAP Stage 2 is blocked on, and it is **ten rules rather than the five
`docs/EndState.md` predicted.**

**Every citation was read in this session rather than carried from
`docs/EndState.md` or `docs/HANDOFF.md`**, which is how the three unpredicted
rules were found — none was visible without opening `Knowledge/Identifiers.md`,
`framework/artifacts/enums.py` and `constitution/Evidence_Standards.md` together.

### Three constitutional lines nobody had cited

- **`Operational_Constraints.md:29`** — "Tradable universes must be discovered
  through evidence." `docs/EndState.md` rested the survivorship argument on
  `Research/UniverseDiscovery.md:7`, a *departmental* document. The identical
  sentence is in the constitution, which `Governance.md:7` gives authority over
  everything. **The argument was stronger than the document making it knew.**
- **`Operational_Constraints.md:25-27`** — "No asset class, security, or
  investment methodology possesses inherent preference." This decides the
  equities-versus-options question against an equities-only boundary: a contract
  that can only express an equity price series does not merely omit options, it
  gives equities preference *by construction*.
- **`Operational_Constraints.md:9-17`** — "Belay shall distinguish: Facts /
  Assumptions / Predictions / Opinions." The vocabulary the evidence hierarchy
  lacks, sitting in a different document. Finding 12.

### The structural ruling, and why it was forced rather than chosen

**Rule 3: a fetched series is not an Artifact. The fetch record is, and it
carries the series' content hash rather than its contents.**

`Knowledge/Identifiers.md` defines eight prefixes and `ArtifactType` nine
members, and **between them there is no name for market data**. Manufacturing one
means editing `Knowledge/` and widening finding 4. The way out is to notice the
data is an *input*: what Law VII requires Belay to keep is the record of what was
obtained, from where, over what period, and what it cannot be trusted to mean.

**Checked against the code rather than assumed** — `framework/artifacts/artifact.py:29-36`
already types `deliverable` as `DeliverableType | None` and its comment already
says *"None means 'not a documented deliverable' — a real state, not an unset
field."* So no enum member is added, ADR-010's vocabulary is untouched, and
finding 4 is not widened. The hash makes reproducibility checkable rather than
asserted: re-fetch, hash, compare.

### `Knowledge/Versioning.md` is load-bearing for the storage question

Never cited for it before. **Data vendors restate history** — splits, dividend
adjustments and corrected prints mean the same ticker over the same dates returns
different numbers later. So a backtest run against a series nobody kept is not
reproducible, *and its irreproducibility is silent*. `Versioning.md:25` — "No
version is overwritten" — makes a differing re-fetch a **new version rather than
a correction**, with both retained.

**Rule 4 keeps the store out of git**, and the deciding argument is not size: rule
3's hash already covers integrity, so committing the bytes adds no guarantee while
making repository growth unbounded and — under append-only history —
irreversible.

### Two verification passes, and the second is why the first cannot be trusted

**The author's pass found one defect.** Rule 2 cited `Immutable_Laws.md:45` as
**Law VII**; the line number is right and the law is **Law VI** — `:43` is the
heading — so the draft named two different laws identically and **contradicted
its own Rejected Alternatives section**, which had it right.

**The independent pass then found three more defects and six imprecisions across
71 distinct claims.** All corrected and marked inline rather than quietly
rewritten. The three:

1. **Rule 6 rested on a premise no file in this repository contained.** The owner
   answered that Belay trades equities and options; **nobody wrote it down**; and
   the ADR cited `docs/OwnerDecisions.md` for it. The fact existed in three files
   written in one commit, each pointing at the others. **This is what an
   unsourced claim propagating looks like from the inside**, and it is the one
   that should have blocked ratification. Fixed at the root rather than in the
   citation — `docs/OwnerDecisions.md` Part 4 question 5 now records the answer.
2. **"Eight rules" was a miscount; there are ten.** It had already reached
   `docs/ROADMAP.md`, `CHANGELOG.md` and a commit subject — the same shape as the
   `Knowledge/Schema.md` miscount that reached a test docstring on 2026-07-30.
3. **Rule 7's supporting bullet was carried near-verbatim from `docs/EndState.md`
   and re-attributed to `docs/OwnerDecisions.md` row 6**, which contains neither
   half of it. That is precisely what the ADR's own Status block claimed it had
   not done.

**And the boast was itself unaudited.** The Status block claimed "twenty-two
citations checked, one wrong" — a denominator that cannot be reproduced under any
counting rule, quoted here and in `CHANGELOG.md` before anyone tested it.
**Reporting a good error rate against a made-up denominator is the shape ADR-012
rule 10 refuses**, and doing it in a document whose subject is provenance is worse
than not reporting one. The real figures are the independent pass's: **71 claims
checked, 11 wrong or questionable, 4 defect-grade, of which the author's pass
caught 1.**

It also corrected this document's claim that ADR-011's and ADR-012's citation
errors were "both self-refuting". ADR-011 had four wrong citations of which **one**
was self-refuting; ADR-012's single correction was a query-versus-text drift.

**The practice is what this vindicates, not the draft.** A careful author who had
opened every file still shipped four defect-grade errors and caught one of them.

### What it deliberately does not settle

**Where the halt lives.** It was added to this ADR's scope earlier the same day
and removed on reflection: rule 2 holds that market data and execution are two
contracts because designing the dangerous one in the language of the safe one is
how the vocabulary for danger goes missing, and ruling an execution-safety
property inside a data-boundary ADR would commit that error inside the document
ruling against it. Finding 11 stays open.

---

## The Owner Answered

`docs/OwnerDecisions.md` is the deliverable. It is a fourth category beside
DECIDED, IMPLIED and OPEN — **ANSWERED**, meaning *a fact now exists that no
document contained*, not *a rule now binds*. Every answer is written in three
parts: what it settles, what it does not settle, and what it opens. **None of
them is doctrine until an ADR makes it so**, which is the distinction ADR-004
already paid for once.

### The repository is public, and it is public on a false premise

`docs/EndState.md` row 13 recorded that this could not be determined from inside
the repository because `gh` was unavailable. It still is. The check was made
against the API instead, and the query is pasted rather than paraphrased:

```
curl -s -o /dev/null -w "%{http_code}\n" https://api.github.com/repos/pewpewpressco-ux/Atlas
```

**`200`, with no credentials presented.** A private repository returns `404` to
an anonymous caller.

**The owner made it public believing Claude Code required it for access. It does
not** — this repository is read from local disk and the remote is never fetched
for content. Making it private removes no access, no history and no ability to
push.

**Nothing of substance has been exposed.** 185 tracked files, and a search across
them for `.env`, `secret`, `credential`, `.key`, `.pem`, `token`, `password` and
`api_key` returns nothing. No credentials, no market data, no account
identifiers. What was at risk was every *future* commit, which is what makes this
cheap to fix now and not later. The owner has directed that it be made private;
it is an account setting and was not changed from here.

**Note the asymmetry, because it is the whole argument:** private → public is a
click, and public → private does not recall what has already been read.

### What the three narrowing questions settled

`docs/EndState.md` argued that row 1 — single-operator, family or product — does
not need answering as posed, because three narrower yes/no questions do the same
work. All three were put and all three answered.

- **Belay will never place orders in an account that is not its operator's.**
  This closes the largest regulatory question in the document and voids the
  entire multi-user column of its cost table: no per-user credential isolation,
  no managed secrets service, and exchange "professional" status is not triggered
  by Belay's design.
- **Belay will never run on hardware its operator does not control.** Secrets
  handling stays at the keychain-or-encrypted-file tier permanently, and there is
  no hosting bill. **This one contradicted the roadmap — see finding 11, opened
  and then narrowed within the session.**
- **The repository is now private.** Changed and verified the same day — the
  query above returns `404` where it returned `200` an hour earlier. **Row 13
  stays OPEN but stops being blocked:** while the repository was public,
  committing a fetched price series *was* redistribution and no free or retail
  licence tolerates that. Private storage is not, so ADR-013 can weigh Law VII's
  retention obligation against `Knowledge/Versioning.md` on the merits, with a
  per-vendor licence check rather than a categorical bar. The two commits
  recording this session were held unpushed until the check passed.

### And four operating questions were answered, which is the shape of Belay

**None of this existed in any document before today**, and between them the four
decide what Stage 2 is built against:

> **Belay runs on a small always-on machine in the owner's house. It trades a US
> account — taxable, tax-advantaged, or both. It holds positions for days to
> months, deciding once a day on daily bars. And it starts on free market data,
> carrying the survivorship bias as a disclosure inside every artifact's
> signature rather than pretending to have corrected it.**

What each one settles is in `docs/OwnerDecisions.md` Part 4. Three things worth
lifting out because they change work rather than only context:

- **The always-on machine resolves finding 11 as first written and leaves a
  sharper residual.** Stage 8 is satisfied — a missed hour costs a days-to-months
  strategy nothing. Stage 7 is not: a home machine loses power and reboots, and
  an emergency brake's reliability bar cannot be lowered by choosing a longer
  holding period.
- **"Taxable, tax-advantaged, or both" undoes a condition written earlier the
  same day**, and it is amended openly rather than quietly. Row 6's scope
  reduction was recorded as conditional on **one broker and one account**; two
  account types is now the expected case. The tax treatment therefore becomes
  **per-account**, so an artifact must record which account it describes or two
  different numbers for the same strategy are indistinguishable — the same defect
  ADR-011 refused when it declined to let a Sharpe ratio omit its risk-free rate.
- **A zero data budget makes the survivorship disclosure mandatory rather than
  conditional, and it makes the row 8 ruling concrete.** A free source will
  answer "no" to one or both survivorship questions, and **a contract that cannot
  express "this source does not know past universe membership" cannot record the
  answer on the day a better source does.** That is the argument for ruling the
  boundary before writing the fetcher, stated in something other than principle.

### And row 1's answer opened a row nobody had

**"Once proven, Belay becomes an exclusive application — possibly sold, possibly
given away in free copies."** So there will be *N* installations, each
single-operator, which is a materially different object from one machine in one
house and is described nowhere in this repository.

**Distributing software that produces investment recommendations is a different
question from managing money, and answering the first does not answer the
second.** It is recorded as row 16 in `docs/OwnerDecisions.md`, it is a
professional's question in the owner's jurisdiction rather than an engineering
one, and **it blocks nothing today** — no copy is being distributed and none can
be until Belay has something worth distributing. Two habits start now because
they are free now and expensive later: no credential is ever committed (already
true), and **no vendor's data is ever committed**, because a personal-use licence
that tolerates a copy on your disk will not tolerate that copy shipping inside an
application.

### Tax collapsed to its small branch, with a condition

**The broker issues the documents; Belay reconciles against them and is aware of
tax implications rather than being the system of record.** Stage 9 loses per-lot
cost basis, lot-selection policy, cross-account wash-sale tracking and any filing
output. `docs/ROADMAP.md` Stage 9 is corrected accordingly, with the superseded
wording preserved.

**The condition must survive into the ADR rather than being assumed:** this holds
while Belay trades **one account at one broker**. A second broker or a second
account reopens it at the large size, because the rules that matter most are in
some jurisdictions computed *across* accounts precisely because no single venue
sees everything.

**And it needs no new mechanism.** A tax rate is a convention no Belay document
states, so ADR-011's central holding already governs it: a required argument,
recorded inside the artifact's integrity hash, never defaulted — the same
treatment the risk-free rate has.

### "Bullet-proof and scalable", with one correction

Standing owner guidance for the remaining open rows. **Recorded with a correction,
because the obvious reading of "scalable" is a trap this repository has already
fallen into once.** For a single-operator application it should mean *swappable*,
*re-runnable* and *portable* — and **not** multi-tenant, horizontally scaled or
service-oriented. The distributed future is *N* independent single-operator
copies, not one system with *N* users, and those require opposite architectures.
Building infrastructure for operators who do not exist is finding 10 from the
other direction.

### A live order path exists in the room

Recorded in `docs/OwnerDecisions.md` Part 5. Broker tooling including
order placement is connected to the Claude session Belay is built in. Nothing
was called. It is not a defect in Belay — `framework/` has no broker connection of
any kind — and that is exactly the point: **it sits outside every control Belay
has.** The rule belongs in `AGENTS.md`, pending `docs/EndState.md` row 12 —
whether `AGENTS.md` carries authority at all: *no session working on Belay places
a live order
through a connected broker tool. Belay trades through Belay, after Belay has
earned it, or it does not trade.*

---

## The Four Questions Were Not Four

`docs/EndState.md` is the deliverable. It rules nothing — every claim in it is
marked DECIDED with a `file:line`, IMPLIED with its reasoning and an explicit note
that nothing rules it, or OPEN. Fifteen decisions, against the four that finding 10
recorded.

**Confirmed before writing it: `docs/` is outside ADR-002's freeze.** ADR-002's
Decision section enumerates the governance layer as `constitution/`,
`departments/`, `workflows/`, `Knowledge/` and the markdown under `strategies/`,
and freezes the *addition of new governance documents* to that layer. `docs/` is
not in the enumeration, and ADR-002's Required Follow-Up mandates an edit to
`docs/Architecture.md`, which would be incoherent if it were.

### What each of the four turned out to be

- **Single-operator, family, or product — OPEN, and no reading will close it.**
  The one near-signal is `docs/ENGINEERING_AGENT.md:27`, the repository's only
  organisation chart, which puts a singular "Human Owner" at the top. It does not
  rule this: it is in `docs/`, it governs who approves *code* rather than whose
  capital is at risk, and `constitution/Governance.md:3` — "Belay is governed by
  process rather than hierarchy" — is the constitution deliberately declining to
  name a person. **But the question does not need answering as posed.** Three
  narrower questions do the same work and each has a yes/no answer: will Belay
  ever place orders in an account that is not the owner's; will it ever run on
  hardware the owner does not control; will this repository ever be public.
- **Runtime AI model — IMPLIED at four independent constitutional points, and one
  of them has never been cited.** `constitution/README.md:5` reads "No department,
  workflow, script, report, strategy, or **AI process** may violate the
  Constitution" — the Constitution already contemplates an AI process inside Belay
  and pre-commits it to every Immutable Law. And
  `constitution/Evidence_Standards.md:31-35` already defines the class a generated
  idea belongs to: Level D, "Hypothesis. Research only."
  **The argument that settles the other half is one Belay has already made.**
  ADR-012 rule 11 forbids `framework/metrics/statistics.py` from deciding a
  promotion, enforced by a test refusing any name containing `passes`, `promote`,
  `approve`, `verdict`, `gate` or `decision` — and that module is the most
  explainable component in the repository. If hand-verifiable arithmetic may not
  decide, a model whose reasoning cannot be reproduced certainly may not. **What
  is genuinely open is how strict Law II is**, and ADR-012 rule 5 already took the
  strict reading once when it refused `scipy` on the ground that "the library said
  so" is the answer Law II forbids. Under that reading a model is barred from the
  explanation path entirely, not merely from the decision.
- **Tax — IMPLIED, and this is the strongest implication of the four.**
  `constitution/Mission.md:7` says Belay "seeks to maximize long-term compounded
  **purchasing power**". Not return. Not pre-tax return. **Purchasing power is an
  after-tax quantity**, and `Mission.md:38` — "optimizes for decades—not days" —
  makes the gap material rather than a rounding error. So tax-*aware evaluation*
  is implied by one adjective in the Mission. **Tax accounting and filing is a
  different question and it is OPEN**, because its size depends on whether Belay
  is the system of record — which depends on the first question above.
- **Broker as swappable adapter — IMPLIED, but not on the citation everyone
  reaches for.** `AGENTS.md:201` and `:240-246` prefer "explicit interfaces" and
  "dependency inversion" — but `AGENTS.md` sits in neither of ADR-002's two layers
  and ADR-002's follow-up to assign every top-level directory to a layer is still
  open, so its authority is itself unassigned. **That is a new open question and it
  is recorded in `EndState.md` rather than here, because it changes nothing today.**
  What does imply the pattern is `Immutable_Laws.md:51` (Law VII): if fills,
  positions and cost basis live only inside a broker's systems, changing broker
  *discards institutional knowledge*. So the ruling should be that Belay keeps its
  own signed record of every fact a venue tells it, with swappability falling out
  as a consequence rather than being asserted as a preference.

### The finding that changes the next session

**Ruling the adapter pattern once, to cover both the broker and market data, is a
false economy.** What generalises is the *provenance obligation* — every fact from
outside Belay arrives with a recorded source — and that is one ruling covering
both, already half-built in `Disclosure` at `framework/metrics/reporting.py:58`.
What does not generalise is the *contract*. Market data is a read and can be
retried freely; a broker adapter writes to the world and a retried submit doubles
a position, so their correct failure defaults are opposites. And
`constitution/Immutable_Laws.md:45` — "Research and execution remain independent"
— puts the two on opposite sides of a boundary the constitution declares
independent. `docs/ROADMAP.md:219-221` is itself evidence: it constrains the
ordering of the broker work and imposes no such constraint on market data.

**So: rule the provenance obligation once; rule the two adapter contracts
separately.**

### Which of the four blocks Stage 2 — not the one expected

The session brief expected only the first question to block Stage 2, via data
licensing. **The shape of that expectation is right — there is one blocker, and
saying so beats a list — but the identity is wrong.**

**Stage 2's deliverable is "a defined boundary for obtaining a price series"
(`docs/ROADMAP.md:157-158`). A boundary *is* an adapter contract.** So the fourth
question is not a Stage 6 question that happens to touch Stage 2; it is asked
directly by Stage 2's own definition. Writing one hard-coded fetcher instead is
not avoiding the ruling — by ADR-011's central holding that no convention Belay
was not told is ever defaulted, it *is* the ruling, made silently.

The first question blocks only the choice of first vendor, and only while the
fourth is unruled: with multiple implementations behind one contract, picking a
personal-use source first is reversible.

**And a fifth thing blocks Stage 2 that was on nobody's list: whether a fetched
price series is stored inside the repository.** Law VII argues for keeping
everything, `Knowledge/Versioning.md` will have opinions, and a vendor licence may
forbid redistribution. The remote is `https://github.com/pewpewpressco-ux/Atlas.git`;
whether it is public could not be determined from inside the repository this
session, and **if it is, committing a fetched series is redistribution at
single-operator scale** and the first question never enters into it.

### Survivorship bias is a Stage 2 acceptance criterion, in two halves

Query run over the whole repository including code —
`grep -rniE "survivorship|delisted"` — returns **zero hits.** `look-ahead` appears
exactly once, at `docs/ROADMAP.md:169`.

It is a property of the *source*, not of the backtester, so Stage 2 is the only
place it can be caught: by Stage 3 the choice is made, and nothing recovers
returns for a company whose data the vendor deleted.
`Research/UniverseDiscovery.md:7` — "Tradable universes must be discovered through
evidence" — makes it constitutional: a universe drawn from a survivor-only source
has been selected on the outcome under prediction.

**The bias has a direction, which is the pattern ADR-012 rule 7 already ruled on.**
It inflates every return measure *and* deflates drawdown and tail measures — it
flatters the return and understates the risk at the same time. ADR-012 rule 10
already settled the correct response to a bias that cannot be corrected: refuse to
produce a number that "looks adjusted and is not", and disclose instead. So the
machinery exists — `Disclosure.known_limitations` is non-blank-enforced and inside
the integrity hash, and the rule is a fixed module constant rather than a
caller-supplied string.

**The part most people get wrong: "includes delisted names" is two properties.**
A source may return prices for a dead ticker if you know to ask, while its
universe membership is as-of-today. The second is what causes the damage in a
universe-driven strategy, and `Research/UniverseDiscovery.md` makes Belay
universe-driven. The acceptance criterion is therefore not "does the source have
delisted data" but **"can the adapter answer both questions, and is the answer
recorded rather than assumed?"**

### No ADR was drafted, deliberately

The session constraint was to give a token estimate before drafting one and to
leave any ruling Proposed rather than implemented. **A proposed ADR-013 on the
boundary is the recommended next ruling** — it is what Stage 2 is blocked on — and
`docs/EndState.md` Part 5 lists the five things it has to settle. The runtime-model
ADR is more interesting and less urgent: nothing is blocked on it, and `framework/`
contains no model call to govern.

## ADR-012 ratified and implemented: Belay can ask whether a record is luck

**Accepted as drafted; no rule was amended on ratification.** Implemented the
same day. `Statistical performance` is the **first** of the seven criteria
`constitution/Promotion_Pipeline.md:75-81` requires promotion to consider, and it
now has a component behind it. Dashboard **2 of 7 → 3 of 7**.

### Why this criterion is not like the others

Every number ADR-011 built *describes* a record: it grew 11.4% a year, it swung
6.5%, its Sharpe was 1.08. **None of them asks whether a coin could have done
that.** ADR-012 is the machinery for that question — it computes the probability
of observing a record at least this strong if the strategy had no edge at all.

Two documents make it structural rather than advisory, and both were opened:

- **`constitution/Promotion_Pipeline.md:27`** — maturity Level 2, `Validated`, is
  *defined as* "Passed statistical review". Checked against all seven levels: it
  is the only one whose description is the passing of a test. Levels 4 and 5 name
  validation as an *objective*, but their descriptions are exposure statements.
- **`constitution/Capital_Authority.md:11-14`** — "Capital shall be determined
  using: ... `Statistical edge`", one of six inputs. **So this number sizes
  positions**, it does not merely inform a review.

Five more demand it — `Validation/README.md:23`, `Validation/Workflow.md:15`,
`strategies/PromotionCriteria.md:7`, `constitution/Mission.md:16`,
`Promotion_Pipeline.md:75`. **None of the seven defines a test, a threshold, a
null hypothesis or a minimum sample.**

### What was built

`framework/metrics/statistics.py` and `framework/metrics/distributions.py`.

- **`distributions.py`** — Student's t, implemented rather than imported. A leaf
  module importing nothing from Belay, the same shape as
  `framework/artifacts/primitives.py`.
- **`statistics.py`** — standard error, t-statistic, two-sided p-value,
  confidence interval, and the sample-adequacy calculation. `significance()`
  returns one record carrying every input that produced it;
  `significance_artifact()` emits it as a signed `Validation Report`.

69 new tests. Written first and run against unchanged code: both modules failed
to import. Suite 318 → 387, same five `xfail` watchers, none flipped.

### The two rulings worth re-reading before touching this

**Rule 7 — the p-value is optimistic, and every artifact must say so.** The
t-test assumes returns are independent and identically distributed. Real returns
are neither: they are autocorrelated, heteroskedastic and fatter-tailed than the
t distribution allows. **The consequence has a direction** — the p-value
understates the probability that a record is luck. `ASSUMPTIONS` and
`KNOWN_LIMITATIONS` are fixed module constants and `significance_artifact` takes
no parameter for either, so the caveat cannot be softened to "None." by whoever
finds it inconvenient. A test asserts the artifact contains the word
"optimistic".

**Rule 8 — "not significant" and "not enough data" are different states.**
`minimum_observations_for_significance` answers the second. Demonstrated on the
weak fixture: p = 0.405, not significant, **and it reports that this effect size
would need 25 observations against the 5 it has.** A sample below that has not
failed the test, it has not taken it. Reporting those two identically is what
the rule refuses.

The two are not independent, and the code says so rather than implying a
four-outcome matrix: significance at n *is* the condition that n suffices, so
`significant` implies `sample_adequate`. The informative case is the negative one.

### Rule 5: no scipy, and the reason is constitutional

`scipy` is neither installed nor declared in `pyproject.toml`. **Immutable Law
II — "Black-box reasoning is prohibited"** — constrains the implementation and
not only the output: "the library said so" is the answer it forbids. So the
regularized incomplete beta is thirty-five readable lines, and
`tests/metrics/test_distributions.py` pins fifteen values against a **published
t-table** rather than against another implementation. Testing one implementation
against another proves they agree; testing against a printed table proves this
one is right. Worst deviation across all fifteen: 7.5e-05, inside the table's own
rounding.

`numpy` was rejected too, and for an extra reason: it is present only as a
transitive dependency of `pandas` and appears nowhere in `pyproject.toml`.
Building on an undeclared package is the 2026-07-26 defect from the other side.

### Rule 11: the gate was not written, deliberately

`Promotion_Pipeline.md:27` makes "Passed statistical review" a maturity level,
which makes `passes_statistical_review()` tempting. `significant` is `p < alpha`
and nothing more — the caller's own threshold, compared. ADR-009 rule 5 drew this
line already. A test asserts the module exposes no name containing `passes`,
`promote`, `approve`, `verdict`, `gate` or `decision`.

### Rule 13: ADR-011's watcher had a false positive, found one day later

`test_only_the_backtest_metrics_adr_011_scopes_in_are_built` tokenised `Tail
Events` as the substring `tail`, and matches tokens against function names as
substrings. **A two-sided significance test is naturally written as
`two_tailed_p_value`** — which would have made that watcher report `Tail Events`
as *built* while it was untouched, one day after the watcher was written and by
the very next piece of work. Tightened to `tail_event`. The ADR-012 functions
also avoid `tail` in their names, so both halves hold independently — belt and
braces, because the collision was avoided by someone who happened to know about
it, and the next author does not inherit that.

### A second self-refuting citation, in as many ADRs

The verification pass ran again before implementation. Nineteen of twenty claims
held with correct line numbers. **The twentieth failed the same way ADR-011's
did.** ADR-012's context claimed the statistical vocabulary returned "three hits,
two of them the version string `v1.0.0-alpha`" — but `v1.0.0-alpha` contains none
of the ten terms the sentence enumerates, so that count was unreachable from that
list. The true figure is **one hit** outside the ADR's own text.

The substantive claim survived: no Belay document defines any of this vocabulary.
Only the count was wrong, and it is corrected in place.

**Two ADRs in one day, the same defect, and the lesson is narrower than "check
citations".** In both cases a search was run, its terms were then written down
from memory, and the two drifted. **Paste the query. Do not paraphrase it.**

---

## ADR-011 ratified and implemented: Belay can compute a risk-adjusted return

**Accepted as drafted; no rule was amended on ratification.** Implemented the
same day. `Risk-adjusted returns` is one of the seven criteria
`constitution/Promotion_Pipeline.md` requires promotion to consider, and it now
has a component behind it. This took the dashboard from **1 of 7 computable to
2 of 7** — the first movement in that figure since it was written. ADR-012 took
it to 3 later the same day.

### What was built, and what each thing is

Four of the nine metrics `Validation/Backtesting.md` names now exist where one
did. In plain terms, because the arithmetic is less interesting than what each
number is *for*:

- **`framework/metrics/returns.py`** — turns a price series into a return
  series ("the position gained 1.2% this period" rather than "the price was
  104.7"), and computes **CAGR**, the single yearly growth rate that would have
  produced the same final capital. Deliberately geometric: up 50% then down 50%
  leaves 75 of every 100, a 25% loss, while the *average* of +0.5 and -0.5 is
  zero. An averaging implementation reports that strategy as having broken even.
- **`framework/metrics/volatility.py`** — how far a return series swings around
  its own average. Not one of the nine, which is why it has its own module: it
  is the denominator of both ratios below, so the conventions chosen here decide
  both of their values.
- **`framework/metrics/risk_adjusted.py`** — **Sharpe** asks how much return
  above cash a strategy handed back for every unit of swing it put you through.
  **Sortino** asks the same question counting only the *downward* swing, because
  upside volatility is not a risk anyone needs compensating for and Sharpe
  penalises it identically to a loss. The filename is not a preference:
  `scripts/status.py:50` names exactly that path as the component expected to
  make `Risk-adjusted returns` computable.
- **`framework/metrics/reporting.py`** — the shared helper that turns a computed
  number into a signed Artifact and **refuses to emit one that is not
  disclosed.** See below.

87 new tests, written first and run against the unchanged code to prove they
fail rather than pass vacuously: all five metric test modules failed to import,
because none of the modules existed. Suite 231 → 318, with the same five `xfail`
watchers still failing as expected — none was flipped.

### The ruling itself, in one sentence

**No convention Belay was not told is defaulted.** `Validation/Backtesting.md`
names nine metrics in nine words and defines none of them. Sharpe needs a
risk-free rate, Sortino a target return, CAGR a periods-per-year, and the
volatility both divide by needs a sample-versus-population choice — and no
document Belay governs itself by states any of the four.

So they are required arguments with no defaults, and rule 2 records every one of
them inside the artifact's integrity hash beside the number it produced. A
Sharpe of 1.4 computed against a 0% risk-free rate and a Sharpe of 1.4 computed
against 4% are two different claims about two different strategies; an artifact
carrying only the figure cannot tell them apart, and a promotion gate reading it
would be reading a number rather than a claim.

Zero would have been a perfectly defensible convention. Applied silently it is
indistinguishable, at the gate, from a rate somebody chose — which is the shape
ADR-005 rule 4 already refused when it declined to default `confidence` to 0.5.

### The disclosure requirement is executable for the first time

`Validation/Backtesting.md:35-43` states that backtests must document
Assumptions, Data Source, Sample Period and Known Limitations. **Nothing in
Belay recorded three of those four.** `Disclosure` now carries them, refuses a
blank or whitespace-only entry, and `metric_artifact` cannot emit a number
without one. All four sit inside the signature, so a `known_limitations` field
cannot be softened to "None." after the fact.

The field names are held to the document by a conformance test that parses it,
so a fifth requirement added there turns the suite red rather than going
silently unrecorded on every artifact Belay emits.

**`drawdown.py` was migrated onto the same helper rather than left beside it**
(rule 13). It predates both ADR-010 and ADR-011 and took a bare `source` string.
That signature is gone rather than deprecated — this repository stores no
artifacts, so nothing built the old way exists to break, and a second accepted
form would have left the pre-ADR-011 pattern legal. This document calls
`drawdown.py` "the only worked example and the pattern to follow"; leaving the
one worked example as the one component not following the rule would have made
the rule optional on the day it was ratified.

### Two claims in this document were wrong

Both were found by opening the files that this document's own closing line says
to open. Recorded here rather than silently corrected, because the second one
changed what the session could honestly contain.

**1. `EvidenceRecord` did not have fields for the four disclosures.** This
document said it did. It has `source`, `methodology`, `level`, `confidence`,
`provenance`, `timestamp` and `hash` — `Data Source` was covered under the name
`source`, and the other three were not covered at all. `docs/ROADMAP.md:107`
stated this correctly, so two documents disagreed and the roadmap was right.

**2. Trade Count and Exposure are not computable from a return series.** This
document listed them, with CAGR and Win Rate, as computable from one.

- A return series **contains no trades.** Nothing in a sequence of period
  returns says how many positions were opened; a series produced by one position
  held for a year is identical to one produced by weekly turnover.
- A period return of `0.0` is **indistinguishable** between "no position was
  held" and "a position was held and the price did not move". Exposure is
  precisely the difference between those.
- **Win Rate is undetermined rather than wrong.** The fraction of winning
  *periods* and the fraction of winning *trades* are different numbers, and
  `Validation/Backtesting.md:23` says only `Win Rate`.

`docs/ROADMAP.md:104-105` had it right again. **The honest Stage 1 slice was
therefore four metrics rather than the wider set the brief implied — smaller
because the brief was wrong, not because scope was cut.** ADR-011 rule 11
records the five that are excluded and why each one is.

### The verification pass earned its place

Before any code was written, a second reader re-opened every file ADR-011 cites
and checked each claim against the actual lines — the check that caught the
`Knowledge/Schema.md` miscount on 2026-07-30.

**Twenty claims. Four wrong.**

- the document is forty-nine lines, not fifty
- its nine metric names sit on lines 15-31 on alternating lines, not 13-31 one
  per line; line 13 is the heading
- **the claim that `risk-free`, `target return` and `standard deviation` appear
  in no document was false, and self-refuting** — the ADR asserting it contains
  `risk-free` seventeen times. Narrowed to "no document outside `docs/`", which
  is the claim the ruling actually rests on and which does hold
- the `Risk-adjusted returns` entry is `scripts/status.py:50`, not `:52`

None of the four touched a rule, and all four are marked in the ADR rather than
quietly rewritten. **The number worth carrying forward is the rate: one citation
in five was wrong in a first draft written carefully by someone who had opened
every file.** Size your trust in a first draft accordingly — including this one.

### `framework/metrics/statistics.py` was deliberately not created

Recorded because it looks like an omission and is a ruling.

`scripts/status.py` expects that path for `Statistical performance`, and
`implementation_state()` grades a file `built` on twenty non-blank lines with no
view of what is inside them. Putting CAGR there would have moved the dashboard to
3 of 7 by turning green a criterion that nothing satisfies — statistical
performance is significance and sample adequacy, not a growth rate.

`scripts/status.py`'s own docstring says it exists to prevent "a reassuring
half-truth". Two of seven is the honest figure and is what it reports.

---

## The repository can return an artifact

`ArtifactRepository.get()`. `latest()` returns a version *string* because until
`ArtifactSerializer.load()` landed there was nothing else it honestly could;
`get()` is the method the question "what is this strategy's current stage"
actually wanted.

With no version named it asks `latest()` which one is current, so it inherits
both of that method's conventions rather than deciding again — None when nothing
is stored, a raise when nothing stored is *orderable*. Two things that could
diverge silently are tested separately: an unknown identifier, and a directory
that exists and holds nothing. `versions()` takes a different branch for each.

**It verifies integrity on read. That was the one open design question and the
argument is in the method, not here.** In brief: `save()` refuses unsigned and
tampered artifacts, but that only promises a file was intact when it landed. A
YAML edited by hand afterwards is invisible to every write-time check, and the
read is the only place left that can notice. `load()` still returns such a file
unchanged — correct for a parser, since the tampering should be *visible* — but
`get()` is the repository vouching for a record, and its likeliest caller is a
promotion gate reading a stage. It is one call to `ArtifactIntegrity.verify_hash`,
the same one `save()` makes, and it covers integrity only.

Nine tests, written first and run against the unchanged code to prove they fail
rather than pass vacuously: 9 failed, 22 passed.

## `strategies/Lifecycle.md` annotated — finding closed

The last thing `Four Different Promotion Sequences` was open on. ADR-007's own
Consequences flagged it as a negative rather than a follow-up.

The document joins nine entries with `↓` arrows, and the arrow from `Production`
to `Retirement` is the defect: it presents retirement as the rung reached by
surviving Production, which ADR-007 rule 3 and ADR-004 both deny. It diverges
three further ways — it omits `Idea` and opens at `Research`, inserts
`Hypothesis`, and writes `Paper` for `Paper Trading` — so it is not the doctrine
plus a ninth entry; the first two rungs differ too.

Annotated, not rewritten. Lines 39 and 41 are quoted by ADR-004 and by the
comment above `STRATEGY_TRANSITIONS`, and every original line survives.

Two tests rather than a paragraph. One holds the annotation to the sequence:
anything the document lists that is not a `STRATEGY_LADDER` stage must be named
in the note, so the two cannot drift apart. Its parser was run and printed rather
than assumed — nine entries, the real ones — and the assertion loop was confirmed
to run against three genuine divergences rather than zero. The other pins the two
quoted lines, because deleting either would leave an Accepted ADR resting on a
quotation no longer in the repository.

## ADR-010 ratified and implemented: the `ArtifactType` question

**Accepted as drafted; no rule amended on ratification. Implemented the same
day.** Two findings close with it — `ArtifactType Cannot Name Most Documented
Deliverables`, open since 2026-07-26 and routed around three times, and the
weak-watcher finding, because the last of the six could finally be written.

What landed: `DeliverableType` with twenty-four members, `DELIVERABLE_ARTIFACT_TYPE`
resolving each to an `ArtifactType`, `Artifact.deliverable` inside the integrity
hash, validator refusal of an unknown subtype *and* of a pair that contradicts
itself, and enum reconstruction on load. Nine tests plus the rewritten watcher,
run against the unchanged source first — the module would not even import.

**The mapping was the part ADR-010 deferred to implementation, and it needed a
stated principle rather than taste.** The type describes what the artifact *is*,
not who produced it: `REPORT` is the honest answer for a document reporting on
something else and covers thirteen of the twenty-four, while a specific member is
used only where the deliverable *is* that thing — a `Regime Report` is the regime
assessment, a `Research Memo` is research. Four are genuinely arguable and are
named as such in the code rather than buried: `Universe Report`, `Chief Scientist
Report`, `Market Snapshot` and `Paper Trade Logs`.

Four deliverables named only in prose — `Portfolio Snapshot`, `Exception Report`,
`Portfolio Summary`, `Historical Summary` — are deliberately **not** members. Rule
4 scopes the vocabulary to what the eleven documents *declare*, and promoting a
phrase from a task list to a governed name is a ruling nobody made.

### The evidence, since it is what made the ruling possible

The finding has been open since 2026-07-26 and routed around three times, most
recently by ADR-009 which said so explicitly. It rested on an estimate — "roughly
twenty deliverables" — that nobody had counted.

Counted: all 31 documents under `departments/`, `Research/`, `Validation/`,
`Operations/` and `workflows/`. Eleven declare deliverables under an explicit
heading — 34 entries, **25 distinct**, plus four named only in prose. **29 against
nine enum members.** The estimate was low.

The count mattered less than three things it exposed, none of which was visible
before the pass:

- **The enum can already type almost all of them; it cannot distinguish them.**
  Sixteen of the 25 are report-shaped and are honestly `REPORT` today. The
  finding's title turns out to be exact.
- **Seven are declared by more than one document** — `Universe Report` three
  times, as a department deliverable, a function's output, and a daily workflow
  deliverable. A closed enum would have to rule whether those are one member.
- **Three entries are not artifacts at all.** `Knowledge Update` sits in three
  Deliverables lists while `WorkflowEngine.md` makes it a step in every workflow.

ADR-010 rules the coarse-type-plus-constrained-subtype shape. It is not invented:
**ADR-009 already chose it for review records** and its Rejected Alternatives
refused to add an enum member for exactly the reason this finding gives. The
subtype is an enum parsed against the eleven documents rather than transcribed, so
no new governance document is created and ADR-002's freeze is untouched.

Rule 9 is the part that unblocked the last weak watcher: the test now asserts
every declared deliverable resolves to a `(ArtifactType, DeliverableType)` pair,
and its marker is gone. That sentence could not be written before the ruling,
which is why the test stayed weak on purpose rather than out of neglect.

One thing it deliberately does not settle, recorded rather than merged quietly:
whether `Research Memo`, `Research Proposal` and `Experiment Proposal` are one
concept. Rule 10 refuses to decide it, because that is a ruling about what the
Research department produces and making it as a side effect of a typing decision
is the failure ADR-004 named. All three have their own member for now.

### And a new finding, found by implementing rather than by reading

Rule 9's mapping meant comparing `ArtifactType` against `Knowledge/Identifiers.md`
for the first time. **They are two vocabularies for the same question and they
disagree** — `PORTFOLIO` and `FAILURE` have no prefix, `DOC` has no member.

That is not cosmetic. Three deliverables map to `PORTFOLIO` or `FAILURE`, and
`ArtifactFactory` refuses `PORTFOLIO-0001` outright, so those artifacts cannot
receive an identifier that names what they are. Checked by running it, not by
reading the code. See the finding.

## Three weak `xfail` watchers strengthened

The mechanism this repository leans on: a `strict` xfail fails while its gap is
open and turns the suite **red** the moment the gap closes, so the backlog
maintains itself. That only works if the test asserts what its name claims. Six
were audited and six did not. Two were fixed on 2026-07-30, three now.

Each was rewritten to parse its governing document rather than a list
transcribed from it, because a copy cannot notice its source changing — the drift
that put a wrong field count into a docstring for months. Details are in the
finding and in each docstring.

**The verification that matters here is unusual, so it is worth naming.** A
strengthened watcher must still fail, and must fail *for the right reason* — an
`xfail` hides the assertion, so a parser bug would look identical to the gap
being open. All three were re-run under `--runxfail` and their real messages
read: `'Trigger' is not required of a Workflow subclass`, `0 registered against
13 documented`, `100 of 100 documents do not conform`. Each parser was also run
directly and printed: five requirements, thirteen workflows, twelve metadata
keys.

One claim in `docs/DocumentStandard.md` was checked rather than inherited. It
says the single document carrying a block "uses `owner:` where this standard says
`author:` and omits five required fields". Opened and parsed:
`strategies/StrategyTemplate.md` carries `owner`, and is missing `author`,
`evidence`, `regime`, `relationships`, `tags` and `type` — six, which is
`author` plus exactly the five it describes. The document is right.

## ADR-009 ratified and implemented: the review decision record

Ruled first, implemented after ratification — ADR-004 recorded that guessing a
contract is how the classifier went wrong. Ratified as drafted; no rule was
amended on ratification, which is the first time that has happened here.

`framework/artifacts/review.py` holds it. Tests were written first and run
against the unchanged code to prove they fail rather than pass vacuously.
Suite 168 → 211.

**The three obligations are discharged.** ADR-004 rule 4 is enforced for the
first time since it was ratified: a review record with an empty justification is
refused at construction. ADR-004's re-sizing step has a home in `resizing_note`.
ADR-008's `Remain Current Stage` is recordable, so a strategy held at a stage is
no longer indistinguishable from one nobody looked at.

What it rules, briefly. The record is an **Artifact of type `REVIEW`**, not a new
kind of object: `ArtifactType.REVIEW` and the `REV` identifier prefix both already
exist, and an artifact is the only thing in Belay that arrives signed, versioned
and append-only — a decision record that can be altered afterwards documents
nothing. It carries its **subject** in typed fields (`subject_id`,
`subject_version`) separate from its own identity, because it has both and
`ReviewTemplate.md` only has room to name one. **Justification is mandatory for
every outcome**, which is where ADR-004 rule 4 finally lands. The **outcome must
agree with the recorded stage change**, which is what makes a held strategy
distinguishable from an unreviewed one. And **`ArtifactSerializer` gains
`load()`** — see below.

Four things worth carrying forward even if the ADR is rejected:

**`PromotionCriteria.md:33` was never cited.** ADR-008 quoted line 35, "Every
rejection requires written justification". Line 33 says "Every promotion requires
written justification" and appears in no ADR. With `Governance.md:15`
(retirements), `StrategyPromotion.md:37` (every decision) and ADR-004 rule 4
(demotion), **four documents between them require justification for all four
outcomes.** Found by opening the file rather than by trusting the ADR that quoted
it.

**The `ArtifactType` finding is routed around, not settled.** `REVIEW` already
exists, so no member is added and
`test_artifact_type_can_name_the_documented_deliverables` stays `xfail`. This was
checked rather than assumed: the test asserts four names, none of which this
touches.

**ADR-004's `RETIRED` trap goes live here.** ADR-004 warned it "becomes live the
moment this helper is written". Rule 5 compares ladder positions, which makes
ADR-009 the first code outside the two guarded test modules to do so. `RETIRED`
is index 8, above `PRODUCTION` at 7, so it is removed from the ladder before any
comparison — the same handling both test modules already use.

**Rule 5 is not the classifier ADR-004 defers.** The deferred classifier derives
a *name* from a transition and must cope with `Draft → Review → Approved`, which
is not a promotion, a demotion or a retirement. Rule 5 is the inverse: given an
outcome the reviewer *declared*, is it consistent with the stage pair they
declared? It only ever sees `StrategyLifecycle` values. No general
`classify(current, target)` is added and ADR-004's follow-up stays open.

## ADR-006 and ADR-007 follow-ups applied

Three departmental documents reconciled to the constitutional wording (ADR-006
rule 3): `Risk` → `Risk-adjusted returns`, `Operational Stability` /
`Operational readiness` → `Operational consistency`, `Regime Compatibility` →
`Regime robustness`. `workflows/Monthly/StrategyPromotion.md` gained the three
criteria ADR-006 rule 5 names as omissions — `Statistical performance`,
`Execution quality`, `Liquidity`.

`Drawdown` was deliberately left alone in all three. ADR-006 rule 2 treats it as
the one criterion already named identically across the constitutional and metric
lists, so "correcting" it to `Drawdown behavior` would have manufactured a
divergence the ADR says does not exist.

**Two divergences were flagged rather than fixed**, and each is recorded in the
document itself:

- `strategies/PromotionCriteria.md` says `Execution Consistency` where the
  Constitution says `Execution quality`. ADR-006 read all five lists and
  enumerated exactly three naming collisions; this is not among them. It either
  judged them different concepts — consistency is a track record, quality is a
  standard, which is the same distinction ADR-006 drew for readiness versus
  consistency — or missed it. Renaming on the general principle would extend a
  ruling rather than apply one.
- `Validation/CapitalReview.md` omits four constitutional criteria, and now reads
  `Consistency` beside `Operational consistency`. ADR-006 rule 5 rules omissions
  to be defects but enumerates only `StrategyPromotion.md`'s three. Adding four
  criteria to a review whose own lines 7 and 9 say it "does not allocate capital"
  and only "recommends promotion" expands a department's remit, which is a ruling
  to make deliberately.

`constitution/Promotion_Pipeline.md` now records that its seven levels are a
maturity model rather than the lifecycle. Its first line already said "maturity
level"; what was missing was the distinction from the doctrine's eight stages —
and that confusion is what put a false "eight promotion gates" citation inside
Accepted ADR-002 until ADR-007 amended it.

`strategies/PromotionCriteria.md` now records that its 0-100 Promotion Score is
suspended (ADR-006 rule 4). The document previously read as though it were live.

## Two conformance tests, one of which immediately earned its place

`test_strategy_lifecycle_is_the_doctrine_sequence_in_order` compares the
doctrine's eight stages to `StrategyLifecycle` **as a sequence**. The existing
`test_strategy_stages_all_appear_in_the_doctrine` checks only that each name
appears somewhere in the file, which a reordered doctrine would still pass — and
order is the whole content of a promotion ladder. A doctrine that swapped Micro
and Limited Capital would make a strategy's first contact with real money its
largest, and nothing would have gone red.

`test_promotion_criteria_match_the_constitution` parses
`Promotion_Pipeline.md:75-81` and holds `scripts/status.py`'s
`PROMOTION_CRITERIA` to it, wording included.

**It caught a real drift within the hour — one this session introduced.** The
ADR-007 note added to `Promotion_Pipeline.md` begins with a `---` rule, and the
parser's `startswith("-")` read it as an eighth, empty criterion. The parser was
tightened to `"- "` and bounded to the first bullet block; the test was not
loosened. Both parsers were then run directly and printed their output rather
than being assumed non-vacuous: seven criteria and eight stages, correct content.

## Artifacts can be read back

`ArtifactSerializer.load()` exists. Until 2026-07-31 the serializer implemented
`dump` and nothing else, so an artifact could be written and never read — which
is why `latest()` can only return a version *string*.

**The acceptance test is the round trip through the signature, not through field
equality.** A loader that rebuilds every field but produces a different canonical
payload has silently broken every signature it touched, and equality would not
catch a value that renders to the same text and hashes differently. `load()`
reconstructs enums, timestamps and nested `EvidenceRecord`s, and it does not
sign: an artifact read from disk keeps the hash it was stored with, so a tampered
file loads and then fails the gate rather than being handed a fresh signature.

The loader is pinned against `dataclasses.fields(Artifact)` rather than a
transcribed list, because it is a second place that has to know the schema and a
field added to one and not the other would be dropped in silence.

**One correction worth carrying, because the reasoning was wrong before it was
right.** `dump` now renders timestamps as `isoformat` strings, and the comment
first justifying that said PyYAML converts an offset timestamp to UTC and returns
it naive. Checked directly: **the installed PyYAML round-trips `+05:00` to an
identical isoformat**, so that was false and no live bug was being fixed. The
change was kept on the honest ground — `canonical_payload` hashes
`created.isoformat()`, which makes the exact rendering signature-critical, while
PyYAML's timestamp handling is library behaviour Belay neither controls nor pins,
and older releases *did* return naive UTC. A stored timestamp with no offset is
refused rather than assumed to be UTC.

## Completed Previously (2026-07-30)

## The repository can be asked what the current version is

`versions()` sorted filenames, so `0.10.0` came before `0.9.0` and the last
element stopped being the newest version once any component reached double
digits. Confirmed rather than assumed: run against the unchanged code, saving
`0.9.0`, `0.10.0` and `0.2.0` returns `['0.10.0', '0.2.0', '0.9.0']` — the
newest version sorts *first*, and `versions()[-1]` hands back `0.9.0`.

Nothing called it. Both references in the repository were tests, so no wrong
number was in circulation; the exposure was the first caller to need a current
stage. That is also why the fix was worth making now rather than after
something depended on it.

Three parts, because the ordering alone would not have been honest:

**`versions()` orders by semantic precedence.** `version_key` lives in
`framework/artifacts/primitives.py`, the leaf module that imports nothing from
Belay — the same reasoning that put `canonical_digest` there.

**`latest()` exists.** A correct sort still leaves "what is current?" as an
idiom every caller re-derives, and an idiom cannot be tested in one place.
ADR-004 is what made that question load-bearing: a strategy can move backward,
so its current stage is no longer the highest stage it ever held and can only
be read from its most recent version.

**`save()` refuses a version that is not `MAJOR.MINOR.PATCH`.** Nothing
validated version strings anywhere — `Artifact.version` is a plain `str`
defaulting to `1.0.0`, and `ArtifactValidator` never mentions it. Storage is
append-only, so an unorderable filename can never be corrected or removed, and
one of them would break that artifact's ordering permanently with no remedy
available. Before it lands is the only place to catch it, which is why the
check sits beside the existing unsigned and tampered refusals rather than in
the validator. Leading zeros are refused too: `01.0.0` denotes the same version
as `1.0.0` but is a different filename, and both could exist forever with
nothing able to say which is current.

A file can still be placed by hand, bypassing `save()`. `versions()` lists it
— `Knowledge/Versioning.md` requires that historical versions remain
searchable, so hiding it would trade one defect for a worse one — but it sorts
below every valid version and so can never read as the newest. `latest()`
raises rather than guessing when nothing stored is orderable, which is the
lesson from the dashboard: a silent fallback is indistinguishable from a
working answer.

Fourteen regression tests, written first and run against the unchanged code to
prove they fail rather than pass vacuously: 14 failed, 8 passed in 0.39s.

Both governing documents were opened, not recalled. `Knowledge/Versioning.md`
gives Major/Minor/Patch with the example `1.2.4`;
`strategies/NamingConvention.md` repeats it under "Version numbers". Neither
defines pre-release or build-metadata syntax, so neither is accepted.

## Relationship types are enforced against the document

`Knowledge/Relationships.md` defines eleven types. `Artifact.relationships`
accepted any string, so `"supports"` and `"Supports"` were two unconnected edges
and a typo created a twelfth kind of relationship rather than failing. The
document's closing claim — "Relationships create intelligence" — only holds if
both ends of an edge agree on the word.

`RelationshipType` now carries the eleven, spelled as the document spells them.
`ArtifactValidator._validate_relationships` refuses anything else. `Relationship`
is frozen; it was the only unfrozen dataclass in `framework/`, so an edge could be
repointed after the artifact describing it had been signed.

**The watching test was weaker than its name and was strengthened, not merely
satisfied.** It asserted `hasattr(relationships, "RelationshipType")` — an empty
enum would have passed it. It now parses `Knowledge/Relationships.md` and asserts
the enum equals the document exactly. A list transcribed into the test would have
drifted from the document as silently as the code did, so the document is the
input. Verified non-vacuous: the parser returns the eleven real names.

Three incompatible representations of a relationship still exist and only one is
now constrained: `Artifact.relationships` (validated), the `Relationship`
dataclass (typed, imported by nothing), and `KnowledgeGraph.relate` in
`framework/knowledge.py`, which puts an arbitrary object on a networkx edge.
Consolidating them was not attempted here.

## docs/Architecture.md records ADR-002

The file said "Belay consists of four permanent departments" — *consists of*
asserting totality, which is the precise claim ADR-002 overturned. It made no
mention of the mechanics layer, `framework/`, or the Artifact contract, and
`AGENTS.md` step 5 directs every session to read it two steps before it reaches
the ADR that superseded it.

HANDOFF called the fix "arguably already permitted". It is not merely arguable:
ADR-002's **Required Follow-Up** section mandates it as the fourth item, and the
governance freeze in ADR-002's **Decision** section covers only the *addition of
new governance documents*. `docs/` is not in the enumerated governance layer at
all. Every original line was kept; the two-layer architecture was added around
them, so this records an accepted decision rather than writing new doctrine.

**Both citations here were line numbers and both had gone stale; corrected to
section names on 2026-07-31.** They read `docs/DECISIONS.md:181` and
`DECISIONS.md:120-122`. Opened: line 181 is a horizontal rule and the follow-up
bullet is at `DECISIONS.md:190-191`; lines 120-122 are the end of ADR-002's
Context and the `## Decision` heading, and the freeze sentence is at
`DECISIONS.md:129-131`. Both drifted downward when ADR-007's amendment note was
inserted into ADR-002 at `DECISIONS.md:105-112`. **The fix is the one this
document already applied to the `xfail` markers: cite a heading, not a number.**
A section title does not move when text is inserted above it. Checked across the
whole repository — `grep -rnoE "DECISIONS\.md:[0-9]+(-[0-9]+)?"` returns six
citations and only these two are stale; the three `DECISIONS.md:102` references
in ADR-007 and the `DECISIONS.md:345` reference in
`tests/test_governance_conformance.py` all still resolve to the lines they name.

## ADR-005 implemented: the artifact schema is complete

`tags`, `summary`, `confidence` and `evidence_level` are on `Artifact`, closing
two P2 findings. All four are inside the integrity hash — a confidence figure a
promotion gate reads must be covered by the signature, or it could be raised from
0.3 to 0.9 with verification still returning `True`. Pinned by tests.

**Confidence is revised by producing a new version, never in place.** `Artifact`
stays frozen. `Knowledge/Versioning.md:25` forbids overwriting, and the history of
an estimate *is* the evidence trail. It defaults to `None`, not 0.5: a default
would be a fabricated figure indistinguishable from a real one. Bounded to 0-1 at
both the factory and the validator, matching `EvidenceRecord`.

**`evidence_level` is derived, never supplied.** ADR-005 rule 5 was amended on
ratification to settle it: the **strongest** grade present, because
`Evidence_Standards.md:41` states "Hypotheses do not invalidate production
evidence" — taking the minimum would let one Level D record drag down an artifact
carrying Level A, which that sentence forbids. The factory computes it and refuses
a caller-supplied value; the validator re-derives it and refuses a mismatch, the
same split already used for the integrity hash. Without the validator half, an
artifact built by calling `Artifact()` directly could claim Level A while carrying
only hypotheses — and that claim is what a promotion gate reads.

`EVIDENCE_STRENGTH` is an explicit table rather than the enum's declaration order.
`StrategyLifecycle` already showed what position-as-rank costs: `RETIRED` sits
above `PRODUCTION` positionally while being no rung at all.

**Both watching tests were strengthened before implementation, not after.**
`test_confidence_can_be_adjusted` asserted only that a `confidence` field existed —
an immutable field would have satisfied it, so closing the *other* finding would
have flipped it green without this one being closed. It now checks both halves of
the ruling: revisable across versions, and not mutable in place.
`test_artifact_has_every_field_the_schema_requires` now parses `Schema.md` rather
than hard-coding the list that had already gone stale once. Run against unchanged
code first: 2 failed, 12 passed.

## Four rulings ratified

ADR-005 through ADR-008 are in `docs/DECISIONS.md`, all **Accepted** 2026-07-30.
ADR-005 is implemented. ADR-007's amendment to ADR-002 is applied. ADR-006 and
ADR-008 are ruled but their follow-ups are unapplied.

Two rules were sharpened on ratification rather than accepted as drafted:
ADR-005 rule 5 (`Evidence Level`, previously undecided) and ADR-008 rule 4
(`Reject`, previously called a synonym without saying why only one document
carries both — it is the decision-side name for the event whose state-side name
is `Remain Current Stage`, which is why only the document framed as handling a
*request* lists both).

- **ADR-005** — *implemented*. Artifact-level confidence and the absent schema
  fields.
- **ADR-006** — the constitutional seven govern promotion. The five lists are not
  five rivals; they sit at three altitudes (criteria, instruments, departmental
  checklists). The 0-100 Promotion Score is suspended, not adopted. **Follow-ups
  unapplied:** three departmental documents to reconcile, one conformance test to
  add.
- **ADR-007** — the doctrine's eight stages are the lifecycle. **The amendment to
  ADR-002 is applied**; its false "eight promotion gates" citation now reads
  `Paper_First_Capital_Doctrine.md`, with the original sentence preserved in the
  amendment note rather than discarded. **Follow-up unapplied:** a conformance
  test parsing the doctrine's eight stages against `StrategyLifecycle`.
- **ADR-008** — `Remain` is an outcome, not a transition. No self-transition is
  added to the lifecycle table. **Unimplementable** until review decisions are
  recorded somewhere.

The evidence behind all four was gathered by opening every governing document and
then having a second agent re-open each file to confirm every quote appeared
verbatim at the stated line. One claim of roughly two hundred failed: a line
number off by four in `ROADMAP.md`, text correct. That check is why the Schema.md
miscount below was caught rather than inherited.

## A miscount that had propagated into a test

`Knowledge/Schema.md` lists **thirteen** required fields, not fourteen. Counted
line by line: lines 7-31, with `Optional Fields` beginning at line 35. The wrong
figure was in this document and had been copied into the docstring of
`test_artifact_has_every_field_the_schema_requires`. The conclusion it supported —
three fields missing — is unaffected.

Worth recording how it surfaced: a subagent sent to read the document reported
fourteen, because it anchored on HANDOFF rather than counting. The document was
opened and counted by hand afterwards. A second reader repeating a number is not
evidence for it.

Not built at the time: there was no `load()`. `ArtifactSerializer` had `dump` and
nothing else, so the repository could write artifacts but not read one back.
**Closed 2026-07-31 by ADR-009 rule 9.** `latest()` still returns a version
string, but `get()` now returns the artifact — closed 2026-07-31, below.

---

# Completed Previously (2026-07-28)

## ADR-004 implemented: a strategy can be demoted

Ten backward transitions are now legal, and nothing else changed direction. A
strategy degrading at limited capital no longer has to be left alone or retired
outright — the choice demotion exists to avoid. Depth is unbounded downward, the
floor is `PAPER_TRADING`, and the forward gates are untouched, so a demoted
strategy re-earns every stage the normal way.

**The order was the whole risk.** Both affected tests used "everything except
`RETIRED`" as a proxy for "forward", which stopped being true the moment backward
moves shared the table. `test_promotion_path_walks_every_stage_in_order` — now
`test_forward_path_walks_every_stage_in_order` — walked the table in a `while True`
loop whose only exit was a stage with no non-`RETIRED` successor; once
`PRODUCTION` gained four demotion targets that exit disappears,
and `RETIRED` — the one row that would end it — is filtered out before the walk
can reach it. With no `conftest.py` and no `pytest-timeout`, changing the table
first produces a silent hang, not a red suite.

Confirmed rather than assumed. Run against the new table, the old logic settles
into a two-stage cycle: `Production → Limited Capital → Production → …`, still
going at 200 iterations. It takes `onward[0]`, which at `PRODUCTION` is now the
first demotion, and the first move back out of `LIMITED_CAPITAL` is the promotion
to `PRODUCTION`. So it is not a walk that runs long — it is one that never ends,
and `pytest` prints nothing while it does.

Both tests were rewritten first and run against the unchanged table to prove they
fail rather than hang: two failures in 0.18s. Only then was the table changed.

`RETIRED` sits at enum index 8, above `PRODUCTION` at 7, so "compare stage
ordering" cannot be a bare position comparison — under one, every retirement
reads as the deepest promotion in the system. Both test modules derive a `LADDER`
with `RETIRED` removed and carry the warning at the definition. No ordinal
comparison anywhere sees it.

The ten transitions are pinned as a set, so an eleventh — a capital rule nobody
decided — fails the suite rather than passing unnoticed.

Rule 4 (written justification) is **not** enforced and cannot be: a transition
table rules that a move is legal, not that a reason was written. Nor is the
re-sizing step ADR-004 sequences after a demotion. Both need a layer that records
review decisions, which does not exist. The promotion/demotion/retirement
classifier is still deferred on purpose — ADR-004 says to specify it before
writing it, and "Remain" is still an open question.

## The dashboard was showing no priorities at all

Every open finding rendered as a grey `?` instead of P1/P2/P3. Two independent
breaks in one path. `open_findings()` matched `Priority:\s*\n\s*\n\s*(P\d)`,
requiring a blank line before the grade — no section in this document has ever
been written that way, they all put it inline as `Priority: P2. Watched by ...`,
so the match failed for all fifteen. And `PILLS` had no entry for P1/P2/P3, so
even a working parser would have rendered the whole column the same grey.

Both fixed; the sort now puts unparsed findings last rather than first, where
ASCII was quietly placing them above P1.

**This is the failure mode the conformance suite exists for, and it got past it.**
A parser returning its fallback looks exactly like a parser that worked. Nothing
was red, the page rendered, and the figure it printed was wrong for at least two
sessions — found by reading the regex, not by looking at the dashboard.
`tests/test_status_dashboard.py` now watches it: three tests asserting every
finding parses a grade, every grade has a colour, and the order is by priority.
Verified against the old regex, which fails all fifteen.

Worth generalising: the dashboard is the thing this document tells you to trust
over itself, and it had no tests. Treat a silent fallback as a defect, not a
default.

## `xfail` markers no longer cite a numbering that goes stale

Closed while editing that file, as the finding asked. Every marker cited a finding
number from the original 23-defect audit, so following one from a failing test
landed on the wrong section. They now cite section titles. Titles do not renumber
when a finding closes, which is what kept breaking them — this session closed two
findings and would have broken them again.

---

# Completed Previously (2026-07-26)

## Both P1 integrity defects closed

`ArtifactFactory` signs everything it creates; `ArtifactValidator` rejects unsigned
artifacts, so an artifact built by any route cannot pass the gate governance uses.

`ArtifactIntegrity.canonical_payload` now covers `author`, `created`, `updated`,
`parent_hash` and `strategy_stage`. Their absence meant an artifact's author could
be changed and its creation date moved by years while verification still returned
`True` — the signature proved what an artifact said, not who produced it or when.
`constitution/Governance.md` requires artifacts to possess identifier, version,
author, date and status.

Evidence and artifact hashing were consolidated into `canonical_digest` in
`framework/artifacts/primitives.py`, a leaf module importing nothing from Belay —
necessary because `evidence.py` cannot import `integrity.py` without closing an
import cycle. No existing evidence hash changed; pinned in
`tests/artifacts/test_evidence_hashing.py`.

## ADR-003 accepted: one lifecycle per governed subject

`ArtifactLifecycle` now carries what `Knowledge/ArtifactLifecycle.md` defines —
Draft, Review, Approved, Active, Archived, Historical — and every artifact holds
one. `StrategyLifecycle` carries the eight stages of
`Paper_First_Capital_Doctrine.md`, and only STRATEGY artifacts carry a
`strategy_stage`.

Before the split, a drawdown report's legal future states included Micro Capital and
Production. The validator now refuses to transition between lifecycles rather than
coercing, so that is unrepresentable.

`MICRO_CAPITAL` was missing entirely, so promotion stepped from review straight to
limited capital — a strategy's first exposure to real money would have been its
largest. `strategies/Lifecycle.md` states "Strategies never skip stages" outright.
`RETIRED` is now reachable from every stage, not only `PRODUCTION`.

## Persistence works and is tested for the first time

`ArtifactRepository.save()` wrote to `{id}.yaml`, so saving a second version
silently destroyed the first — forbidden by ten documents. Artifacts now live at
`{root}/{id}/{version}.yaml`. Writing different content to an existing version
raises; re-saving identical content is a no-op. Unsigned and tampered artifacts are
refused at the persistence boundary.

This code had never executed. The suite reported 46 passing while `save()` had never
run once, because no test referenced it and `pyyaml` was declared but not installed.

## Validation hardened

Identifiers are checked against `Knowledge/Identifiers.md` at creation — the one
field that can never be corrected later. `framework/identifiers.py` gained the two
missing prefixes (REGIME, DOC) and a validator; it was extended rather than replaced,
per AGENTS.md change discipline. Twenty tests failed on invalid identifiers,
including `DD-0001`, a prefix that never existed.

Confidence is bounded to 0–1. `42.0` and `-3.0` were previously accepted and stored.

## Every module imports; every file is visible

Runtime dependencies installed. Eight `framework/services/` placeholders subclassed
`Service` without importing it. Modules that will not import: **15 → 0**.

Nineteen files were tracked without extensions — invisible to `*.md` searches, to
GitHub rendering, and to every prior session. One contained a repository-wide
specification nobody had read; it is now `docs/DocumentStandard.md`. The rest are in
`docs/notes/` with a README, moved with `git mv` so history follows. Kept rather
than deleted, per Immutable Law VII.

## Status dashboard

`scripts/status.py` writes `reports/generated/status.html`; `refresh-status.cmd`
regenerates and opens it. Everything is re-derived from the repository each run —
tests, watched gaps, untested modules, unimportable modules, findings, ADR statuses,
stage progress. Nothing is hand-maintained.

Note for future sessions: a browser cannot run the test suite, so an HTML page can
never self-refresh against working-tree state. The launcher has to live outside the
browser.

---

# Closed Findings

| Finding | Closed by |
|---|---|
| Unsigned artifacts passed validation | Factory signs; validator rejects |
| Two divergent hashing implementations | Both use `primitives.canonical_digest` |
| Author, dates, parent hash outside the hash | Added to `canonical_payload` |
| `save()` overwrote prior versions | Version-aware paths; refuses to overwrite |
| Lifecycles conflated in one enum | ADR-003 accepted and implemented |
| `MICRO_CAPITAL` missing | Added; skipping it is now illegal |
| Retirement only from `PRODUCTION` | Reachable from every stage |
| Timezone-naive timestamps | `utc_now()`; naive evidence timestamps rejected |
| Runtime dependencies not installed | `pip install -e .`; 15 broken modules → 0 |
| `framework/services/` would not import | Missing `Service` import added to eight |
| Identifier format unenforced | Validated at creation; REGIME and DOC added |
| `confidence` accepted any float | Bounded to 0–1 |
| Nineteen invisible extensionless files | Renamed; `NEW STANDARD` promoted to `docs/` |
| Missing/misnamed governance references | `docs/ROADMAP.md` created; `AGENTS.md` fixed |
| Demotion is not representable | ADR-004 ruled and implemented; ten transitions added |
| `xfail` reasons cite a retired numbering | Markers cite section titles, which do not renumber |
| `versions()` sorted as strings, not semver | Semantic ordering; `latest()` added; non-semver refused at `save()` |
| Relationship types unenforced | `RelationshipType` enum; validator refuses anything else |
| ADR-002 follow-up on `docs/Architecture.md` | Two-layer architecture recorded; ADR-002 mandated it |
| Three required schema fields absent | ADR-005: `tags`, `summary`, `confidence`, `evidence_level` added |
| Artifact-level confidence does not exist | ADR-005: revisable across versions, never in place |
| ADR-002 cited eight gates that do not exist | ADR-007: amended, original text preserved in the note |
| "Remain" is a review outcome with no representation | ADR-008 ruled it; ADR-009 records it. `ReviewOutcome.REMAIN_CURRENT_STAGE` |
| Artifacts could be written but never read back | `ArtifactSerializer.load()`, ADR-009 rule 9 |
| Four different promotion sequences | ADR-007 ruled the doctrine's eight; both documents that read as rival sequences are annotated |
| `ArtifactType` cannot name most documented deliverables | ADR-010: coarse type plus `DeliverableType`, 24 members parsed from the eleven declaring documents |
| Six xfail tests were weaker than their names | Five strengthened; the sixth rewritten to ADR-010 rule 9 and its marker removed |

---

# Closed Findings

Kept in full rather than deleted. `scripts/status.py` counts `## ` sections
inside `# Open Findings` only, so a closed finding has to leave that section or
the dashboard keeps reporting it — which is why this heading exists rather than
the section being trimmed away. The sequence of wrong readings inside this one
is the most reusable thing in it.

## No Fetch Record Is Ever Written To Disk (F-002) — CLOSED 2026-08-02

**F-002, High.** `reports/review/2026-08-01-review.md`.

`git ls-files` returns zero artifacts of any type. `ArtifactRepository` is
instantiated nowhere outside its own module and tests. The only production caller
of `fetch_and_record` is `scripts/verify_clone.py`, which writes its store to
`tempfile.mkdtemp` (`:61`), `rmtree`s it (`:177`), and drops the returned record.
The one series Belay holds has no record anywhere.

This falsifies `.gitignore:46-49`, which is the stated reason the bytes are not
committed: "the record of what was obtained is signed and permanent whether or
not the bytes are under version control." Neither half is true. Breach:
`constitution/Governance.md:27` — "Institutional memory is mandatory."

**Graded High but carried at P1, on urgency rather than severity.** Every fetch
run before this is fixed produces bytes with no record, and that damage is
retroactively unfixable — a vendor restatement cannot be reconstructed after the
fact. Today it is one AAPL series and cheap to redo. **This finding gates any
bulk backfill**, and the clone transport has just made backfills fast, which is
exactly what makes the sequencing matter.

Structural — where artifacts live, what is tracked, what `.gitignore` may assert
— so it wants an ADR-014 rather than a patch.

Priority: P1. Not watched by a test.

---
## The Fetch Record Cannot Name The Bytes It Records — CLOSED 2026-08-02

**Found 2026-08-02 by drafting ADR-014.** A fact about the repository as
committed, not a consequence of that ruling.

`framework/data/fetch_record.py:88-108` writes `("data_source", source.name)` into
the signed content and nothing else that identifies the file — no source key, no
store version, no path. `framework/data/fetch_record.py:191` files the bytes under
`source.key`. **The one source identifier the record carries is the one the store
deliberately does not use**, and `framework/data/contract.py:199-206` says why the
two are separate in terms: the display name "carries the licence attribution CC
BY-SA requires" and is expected to be edited, where the key is "short, lowercase,
and never changed once data exists".

Concretely, for the only series Belay holds: the bytes are at
`data/market/dolthub-stocks/AAPL/0001-a7dbcaf3fb6aba2d.bin`, keyed
`dolthub-stocks`, and a record for them would say
`DoltHub post-no-preference/stocks (CC BY-SA 4.0)`.

**What survives is the content hash, and only by brute force.** Given a record you
can find its bytes by hashing every file in the store until one matches; given a
file you can find its record the same way. ADR-013 rule 3's "re-fetch, hash,
compare" still works — comparison was never the broken half. Locating the prior
bytes is.

Breach: `constitution/Operational_Constraints.md:5` — "Belay shall maintain
accurate records." A record that cannot identify its own subject is not one.

**P1 on timing rather than on damage.** The content tuple is inside the integrity
hash, and ADR-013 rule 7 established that changing signed content is free only
while nothing is stored — after that it is a migration of append-only records,
which `Knowledge/Versioning.md:25` forbids. ADR-014 rule 6 proposes the fix and
rule 4 closes the window; the two have to land in that order.

Priority: P1. Not watched by a test.

---
## The Identifier Space Cannot Fund One Record Per Fetch — CLOSED 2026-08-02

**Found 2026-08-02 by drafting ADR-014**, by reading `Knowledge/Identifiers.md`
against the arithmetic of persisting one record per fetch. Nobody had.

`framework/identifiers.py:33-35` compiles `^([A-Z]+)-(\d{4})$` — four digits, so
**10,000 identifiers per prefix, ever**. `Knowledge/Identifiers.md:3-5` makes them
permanent and never reused. `RPT` is shared with every other REPORT artifact
Belay will ever produce.

Against that: one fetch record per fetch means a 6,000-symbol backfill consumes
**60% of the entire RPT space in a single run**, and one symbol refreshed daily
consumes 252 a year. There is no allocator — `framework/identifiers.py:11-13`
states that uniqueness "is not enforced here, and cannot be", every call site
picks its own, and `scripts/verify_clone.py:68` hardcodes `RPT-9001`.

**The four-digit limit is the code's, not the document's, and that decides how
expensive this is.** `Knowledge/Identifiers.md` never states a digit count; it
gives seven examples (`:9-21`) and every one of them happens to use four.
`framework/identifiers.py:33-35` turned the examples into a rule and its comment
says so — "four digits, as every example in Knowledge/Identifiers.md uses". So
this may be a code change rather than an amendment to governance, and nobody has
established which.

**P1 because it cannot be corrected afterwards.** Identifiers are permanent, so
the first record persisted under a wrong answer fixes it forever. It blocks
ADR-014 rule 4 and nothing else in that draft.

Priority: P1. Not watched by a test.

---
## A Strategy Can Be Created Already Standing At Production (F-001) — CLOSED 2026-08-02

**F-001, Critical.** `reports/review/2026-08-01-review.md`. Closed by
`framework/artifacts/factory.py:42-68` — `create()` now refuses a `strategy_stage`
that is anything other than `IDEA` on a STRATEGY artifact.

**What was wrong.** The lifecycle guard was on movement and not on birth.
`ArtifactFactory.create()` passed `strategy_stage` through `**kwargs` untouched
and `ArtifactValidator._validate_lifecycle` checked only that it *was* a
`StrategyLifecycle`, never *which* one. A signed STRATEGY artifact at
`PRODUCTION` validated `True`, carrying no VALIDATION artifact and no
PAPER_TRADING history because it had never occupied those stages. Breach:
`constitution/Paper_First_Capital_Doctrine.md:5` — "Every strategy begins with
zero capital. No exceptions."

**Why the factory rather than the validator.** The movement path was already
sound — `validate_transition` refuses `IDEA -> Micro Capital`, verified by
running it — and the factory is the only unguarded way in. `serializer.load()`
builds `Artifact(**values)` directly (`serializer.py:134`) and `repository.get()`
verifies the integrity hash on read (`repository.py:99`), so a hand-edited YAML
at PRODUCTION already failed while a factory-minted one passed everything. The
refusal is shaped like the `integrity_hash` and `evidence_level` refusals above
it and rests on the same sentence: a caller-provided stage is an assertion nobody
checked.

**Unconditional, because there was nothing to migrate.** `grep -rn
"ArtifactType.STRATEGY" framework scripts departments` returned only
`validator.py:157` and `:165` — no production code creates a STRATEGY artifact.

**Watched by `test_a_strategy_cannot_be_born_past_idea`**
(`tests/artifacts/test_factory.py`), parametrized over all eight non-`IDEA`
stages including RETIRED, plus `test_a_strategy_may_be_born_at_idea` for the
other half. Run against the unchanged code first: nine of them, all
`DID NOT RAISE ValueError`.

**Two existing tests were creating strategies past IDEA and both were fixed
rather than exempted.** `test_deliverables.py` used PAPER_TRADING where the stage
was incidental — now IDEA. `test_serializer_round_trip.py` needed a strategy
genuinely at LIMITED_CAPITAL, and now builds one the way one actually comes to
exist: born at IDEA, then `dataclasses.replace` and re-signed. That the earlier
version asked the factory for LIMITED_CAPITAL directly is the finding in
miniature.

---

## DailyBarSeries Accepts Duplicate Dates (F-005) — CLOSED 2026-08-02

**F-005, Medium.** `reports/review/2026-08-01-review.md`. Closed by
`framework/data/contract.py:98-111` — the guard is now
`any(later <= earlier for earlier, later in zip(dates, dates[1:]))`, which
subsumes the ordering check it replaces.

**What was wrong.** The guard was `dates != sorted(dates)`, and `[d1, d1, d1, d2]`
is sorted, so the same trading day could appear any number of times in a series
presenting itself as validated. Breach:
`constitution/Operational_Constraints.md:5` — "Belay shall maintain accurate
records."

**It ran in the flattering direction.** A duplicated bar yields a fabricated `0.0`
return in `period_returns`, which pulls the standard deviation down while barely
moving the mean — the standard error falls, the t-statistic rises, and
`significant` flips true on a record that did not earn it. The fetch record's
`observations` count and every artifact's `provenance` string inherit the
inflated count, and nothing anywhere reported it.

**Closed as a prediction, not an observation.** The landed AAPL series has no
duplicates and the current chunker does not overlap, so this never produced a
wrong number. The route in was a vendor emitting a repeated row, or any future
adapter concatenating overlapping windows — `dolthub.py:365` and `:295` both sort
without de-duplicating, and now raise instead of accepting.

**Watched by `test_bars_must_not_repeat_a_trading_day`**
(`tests/data/test_contract.py`). Run against the unchanged code first:
`DID NOT RAISE ValueError`.

---

## The Hosted SQL API Cannot Serve A Backfill — CLOSED 2026-08-01

**Closed the same day it was opened, by building the `dolt clone` transport it
names as the fix.** `framework/data/dolt_clone.py`. The closing condition written
below was "a transport exists that can complete a multi-year backfill, verified
by running one" — three years of AAPL, 754 bars, returns in **4.4 seconds**
against an estimated 25+ minutes over HTTP, and `scripts/verify_clone.py` is the
run.

**The measurements that closed it, all taken 2026-08-01:**

| request | over HTTP | from the clone |
|---|---|---|
| AAPL 2017-10-24..26 — *the same statement both sides* | **11.9s** | **0.078–0.135s** |
| AAPL 2017-10-16..26, novel window | **37.4s** | — |
| `MIN/MAX` over one month | **52.8s** | — |
| AAPL 2015-01-01..2017-12-31, 754 bars | not attempted | **4.4s** |

**Only the first row licenses a ratio.** The others are different statements and
are evidence the ceiling is real, not comparisons — a distinction an independent
verification pass had to insist on, because the first version of that table
presented all four as one comparison.

**A fifth wrong reading, and it is the same shape as the first four.** The
recorded table below says "8 days → 0.4s". The equivalent novel window measured
**37.4s** — roughly 90× worse. The fast figures in that table are warm cache
readings, which is what the entry already suspected and what a cold-start run
confirmed.

**Cost:** the `dolt` CLI (installed via `winget install DoltHub.Dolt`, version
2.2.3) and a **730 MB** shallow clone at `data/upstream/`, gitignored before the
first byte landed. `--depth 1` is what makes it 730 MB rather than multi-GB:
Belay needs historical *prices*, which are rows, not historical *commits*. The
consequence is that Dolt's `diff` features cannot be used to inspect how the
vendor restated a price — nothing needs that today, and a full clone would be
required if anything ever does.

Original entry, kept because the sequence of wrong readings is the useful part:

---

Found 2026-08-01 by running a real fetch after the suite was green.

**The boundary works. Getting bulk data through it does not.** ADR-013 is
implemented in all ten rules and 520 tests pass, and not one of them touches the
network — deliberately, because a suite that reaches the internet fails for
reasons unrelated to the code. **That is exactly why the suite did not catch
this.**

Measured against the live database, warm:

| window | result |
|---|---|
| 8 days | 7 bars, 0.4s |
| 1 month | 22 bars, 0.5s |
| 6 weeks | 31 bars, 0.6s |
| 2 months | 42 bars, 28.8s |
| 3 months | `context deadline exceeded`, **3/3 attempts**, ~54.5s |
| 1 year, 13 years | `context deadline exceeded` |

**A window the server has not served before behaves worse than the table
suggests.** April 2024 — a novel month — failed **2/2** at 54.5s, and the same
month split into weeks succeeded at 0.6s / 33.4s / 33.8s / 43.3s: **111 seconds
for one month**, so thirteen years is roughly 6.6 hours per symbol.

**And then the sharper finding, from re-running a window that had already
worked.** AAPL 2024-01-02..2024-02-09 succeeded in seconds, and an hour later
the identical fetch **failed at 54.6s and then succeeded in 1.0s on the very
next attempt.** So the source is *intermittent* as well as slow, and an earlier
note here saying "retrying does not help" was true only of the three-month
window (3/3 failures) and false in general.

**That correction is what put a retry in.** ADR-013 rule 2 blesses it explicitly
and it is half of that rule's argument for two contracts: "Retrying is *how* a
data fetch recovers from a dropped connection. A retried order submit doubles a
position." Market data is the side where retrying is the correct default, so
`_attempt()` retries a deadline failure up to three times and retries nothing
else — a bad branch does not become a good branch by asking again. **This does
not close finding 14**; it makes the current transport usable for the fetch sizes
it can already serve.

**Three readings of this behaviour were wrong before the fourth was right, and
all are recorded rather than tidied away.** The 0.5s one-month measurement was
taken as representative and the chunk size chosen against it; it only holds for
windows already served. The first diagnosis — that the primary key leads with
`date`, making a per-symbol range scan expensive — collapsed when the identical
query returned in 0.4s moments later. And "retrying does not help" generalised a
result that held only for the three-month window. **The sequence is the useful
part**, which is why it is kept: every one of the three was a confident reading
of a real measurement, and the source's behaviour is variable enough to support
several.

**What was done.** A bounded retry on the deadline failure, per rule 2 — see
above — and `framework/data/dolthub.py` chunks on calendar months.
Boundaries derive from the requested window alone, never from a tunable, because
a configurable chunk size would change the concatenated payload and therefore the
content hash — breaking the "re-fetch, hash, compare" that ADR-013 rule 3 exists
to enable. A failing chunk fails the whole fetch and names the window: a partial
series has a silent hole in it, and a hole in an equity's history is
indistinguishable from the instrument not having traded, which is the
survivorship failure mode reappearing as a transport bug.

**What was not done, and why.** Dolt's intended access path is `dolt clone` —
pull the database locally and query it at full speed with no deadline and no rate
limit. The adapter's transport is already an injected `Callable[[str], bytes]`,
so this is a second implementation of an existing seam rather than a change to
the contract. It was not built because swapping the transport was outside the
sanctioned scope, and because `dolt` is a CLI dependency plus a multi-GB
download — a real cost the owner should choose.

**No rule of ADR-013 is affected.** This is a property of one vendor's HTTP API,
which rule 2 made replaceable by ruling the contract first.

**Sharper than first written: the source is intermittent, not merely slow.**
Re-running a window that had already succeeded produced a failure at 54.6s
followed by success in **1.0s on the very next attempt**. A bounded retry on the
deadline failure is now in place — ADR-013 rule 2 blesses it explicitly, as half
of that rule's own argument for two contracts — and it makes the current
transport usable at the sizes it can already serve. **It does not close this
finding.** A retry cannot rescue a three-month window that fails 3/3.

Priority: P2. Not watched by a test, and cannot easily be — the failure is only
visible against the live API, and the suite touches no network by design. It
closes when a transport exists that can complete a multi-year backfill, verified
by running one.

**That condition is now met. See the CLOSED note at the head of this section.**

---

## Five 2026-08-21 Findings Are In No Register The Dashboard Counts (F-021) — CLOSED 2026-09-19

**F-021, High.** `reports/review/2026-09-04-review.md:213`. **Registered and
closed in the same commit**, under `docs/OwnerDecisions.md:1120` (Part 9b).
Registration is not a claim that a finding is open; it is a claim that the
repository has read it.

**A note on how this entry is written.** It does not spell out the five durable
numbers, because `tests/test_session_handoff.py:58-82` refuses any number that
appears both here and in `# Highest Priority Next Task`, and several of them are
legitimately named there as current work. They are rows 29 to 33 of the table in
`# Open Findings`, and `reports/review/2026-08-21-review.md:38-47` carries the
authoritative mapping.

**What was wrong.** The five findings of `reports/review/2026-08-21-review.md`
that survive its correction block — one of them Critical — were merged to `main`
on 2026-08-29 as a report and appeared in no register the dashboard counts.
`scripts/status.py` reads only `docs/HANDOFF.md`'s `# Open Findings` section and
reported 28, none of which was any of the five. The register that would have
carried them was PR #4, a draft still targeting a review branch rather than
`main`, whose stated blocker had cleared six days earlier. A second half: two of
the report's *withdrawn* heading numbers were already in use on `main` for other
findings, in a `CHANGELOG.md` bullet written 2026-08-27.

Breach: `constitution/Governance.md:27` — "Institutional memory is mandatory" —
and `constitution/Governance.md:11`, because the only document on `main` that
listed the five was a session brief asserting an owner approval that no register
recorded.

**Closed by, and the evidence.** `f6fb971` added the five as five `## ` sections
with matching summary rows. `9ff5a58` put the authority on file as
`docs/OwnerDecisions.md:1157` (Part 9c) — which is the half the report said was
missing, that `docs/OwnerDecisions.md` mentioned none of the five — and corrected
the `CHANGELOG.md` bullet in place, which is now `CHANGELOG.md:85` and carries a
dated correction rather than the wrong numbers.

The five `## ` headings the report said were absent are in this document, each
carrying its durable identifier in both the heading and its summary row, where
`grep` for them returned nothing. `python scripts/status.py` printed
`open findings       33` on `9ff5a58` — the commit that closed this — and printed
43 on this one, 42 after F-022's closure, which registers ten more. Neither figure is 28, which is what the
report measured and what the finding is about.

**Closed against this branch, and it reaches `main` when PR #9 merges.** This
branch is stacked on `register/2026-08-21-corrected`. The commits named above are
on that branch and not yet on `main`, so a reader on `main` today would still
find the finding true. That is a property of the stack, not a qualification of
the closure — the two pull requests land in order.

**Not closed by the route the report proposed, and the difference is the point.**
It proposed landing PR #4 rebased onto `main`. PR #4 registers nine findings
under the 2026-08-21 report's own heading numbers, which `main` now assigns to
other findings; rebasing it would reinstate four withdrawn rediscoveries under
numbers that denote something else. It was rebuilt to five rows instead. **PR #4
remains open and `CONFLICTING` on `origin`.** Closing it is an owner action, it
is not part of this finding's claim, and nothing in this commit touches it.

---

## The Cadence Gate Fired At Seven Days And Produced A Duplicate Review (F-026) — CLOSED 2026-09-19

**F-026, High.** `reports/review/2026-09-11-review.md:114`. **Registered and
closed in the same commit**, under `docs/OwnerDecisions.md:1120` (Part 9b).

**What was wrong.** The scheduled review gate read the working tree, so a report
sitting on an unmerged branch was invisible to it. It fired early twice, and the
second firing produced the very report that raised this. The repository
simultaneously carried a written, tested fix on a branch **and** a sentence in
`docs/OperatorChecklist.md` telling every reader that no session could fix it —
which is why the pass a week earlier had identified the problem, called it the
most consequential open item in the repository, and declined to raise it as a
finding.

Breach: `constitution/Governance.md:27` — a review process that cannot see the
previous review has no institutional memory of itself — and
`constitution/Evidence_Standards.md:45`, because the checklist's conclusion was
contradicted by a branch in the same repository.

**Closed by, and the evidence.** Both halves, which were always two problems
wearing one entry. The repository half: PR #6 merged as `a4e7a2a`, and
`scripts/review_due.py` now enumerates `reports/review/` across every `origin/*`
ref rather than the working tree. The account half: `cc80866` recorded that the
cloud routine's Step 1 runs the script and obeys its exit code instead of listing
a directory, and corrected the "no session can fix it" sentence — the correction,
and why the evidence for the original claim was bad, is at
`docs/OperatorChecklist.md:474-488`. Executed on this commit:

```
$ python scripts/review_due.py
SKIP - last review was 8 days ago (2026-09-11-review.md, on main). Next due 2026-09-23.
$ echo $?
1
```

`git ls-tree main --name-only scripts/` lists `scripts/review_due.py`, so the
gate is on the default branch rather than on a branch nobody merged.

**Already verified by a real firing; what remains untested is that the firing
be scheduled.** Cloud run `cse_<id>` fired the account half
on 2026-09-19 — one tool call, `python scripts/review_due.py`, printed SKIP,
exited 1, wrote nothing (`docs/OwnerDecisions.md:1197-1201`, Part 9d). That is
a real firing of the account half in the environment that uses it, and it is
recorded rather than smoothed over that it was invoked directly rather than by
the cron. The next **scheduled** run is 2026-09-25, and the gate returns SKIP
until 2026-09-23, so a scheduled (cron) firing is the one thing still
unverified.

**The instruction that caused the original collision is still in the review
skill, and it is not closed by this.** It carries no finding number and is
recorded as a note for the next review in the preamble to `# Open Findings`
below. Only `scripts/review_due.py` assigns finding numbers.

---

## HANDOFF's "Current Repository State" Describes The Repository Four Merged Pull Requests Ago (F-022) — CLOSED 2026-09-19

**F-022, Medium.** `reports/review/2026-09-04-review.md:267`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only,
no fix ruled — and closed the same day at session close-out**, under
`docs/OwnerDecisions.md:1207` (Part 9d), which rules that this section is
corrected at close-out rather than in a register commit.

**What was wrong.** `## Current Repository State` stated the last session was
2026-08-02 and the suite stood at 626, both unchanged since that date while
seven pull requests merged and the suite moved to 635. The register beneath it
was current, so the document was internally inconsistent about its own date
rather than uniformly stale. Breach: `constitution/Operational_Constraints.md:5`
— "Belay shall maintain accurate records."

**Closed by, and the evidence.** This commit. `docs/HANDOFF.md:29-111` now states
the repository as of 2026-09-19 — `main` at `cc80866`, PRs #6/#7/#8 merged,
suite 635/1/5, dashboard 42 open findings, 14 ADRs, and which pull requests are
still open and why — re-derived from `git log`, `python -m pytest -q`,
`python scripts/status.py`, `grep -c "^## ADR-" docs/DECISIONS.md` and
`gh pr list` run against this commit rather than carried over from a prior
one. The 2026-08-02 text is not deleted: it is kept, dated, under
`docs/HANDOFF.md:115` ("State As Last Written, 2026-08-02"), Law VII.

**What this does not fix, said plainly rather than left to be discovered
again.** The report's proposed mechanism — a staleness check comparing the
suite count this section states against the count the suite reports — was
**not built**. Nothing in the repository forces this section to be re-derived
at the next close-out; it depends on whoever closes the next session doing it
by hand, exactly as this commit did. That is a fix of the symptom this
session, not of the cause, and it is left to the owner or the next review
rather than claimed as more than it is.

Breach graded Medium by the report rather than High, with the argument for
High recorded in it rather than acted on.

Priority: P3. Not watched by a test.

---

## The Review Skill's Hardcoded Counts Have Rotted (F-025) — CLOSED 2026-09-19

**F-025, Low.** `reports/review/2026-09-04-review.md:404`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only —
and closed the same day on a separate owner selection made in chat.** That
selection is two choices and nothing wider: correct the review skill's
finding-numbering instruction, and take this finding's hardcoded counts in the
same file. It is recorded as a selection rather than quoted, and it authorises
no other finding.

**What was wrong.** `.claude/skills/belay-review/SKILL.md` told every reviewer to
read "`docs/DECISIONS.md` — the 13 ADRs" and to read the ones a review touches
"rather than all 158 KB". Measured on this commit,
`grep -c "^## ADR-" docs/DECISIONS.md` returns **14** and the file is **190,559
bytes** — so the size figure had rotted twice, the report having measured
186,945. ADR-015 is drafted on PR #10's branch, so any restated count was due to
rot again the day that merges. Breach: `docs/DocumentStandard.md:5-7`, which
records the same precedent — a count written as 81 that was 100 by the time
anyone checked, fixed by deriving it rather than by restating it.

**Closed by, and the evidence.** The report's own proposal, which was to delete
both figures rather than correct them. `.claude/skills/belay-review/SKILL.md:90-96`
now tells the reviewer that `grep -c "^## ADR-" docs/DECISIONS.md` is how many
there are and `grep -n "^## ADR-" docs/DECISIONS.md` is the index, to read every
ADR the review touches rather than the whole file, and not to state a count there
or carry one — naming the "13 ADRs" rot as the reason. **No number replaces the
deleted ones. That is the fix**; a restated count rots again on the same
schedule.

**Two more rotted numbers were found by reading the rest of the skill, and are
fixed here rather than left for the next pass.** Neither is part of the finding
as written. `.claude/skills/belay-review/references/red-team-checklist.md:43-53`
cited `.gitignore:39-42` for the claim that the bytes are uncommitted *because*
the signed record suffices; that claim is at `.gitignore:46-49` and `:39-42` is
the unbounded-growth argument. **This was wrong when written rather than
rotted, and the first draft of this entry said the opposite — an independent
pass caught it.** `git show 079f43a:.gitignore`, the commit that created the
checklist, already has the growth argument at `:39-42` and the record claim at
`:46-49`; ADR-014 (`a19c24e`) then rewrote `:46-49` in place. Nothing moved.
(A miscount repeated, which is the "Searched all 101 documents" finding's shape
without its cause — named by title rather than by number on purpose, because
`tests/test_session_handoff.py:58-82` refuses any finding number that appears
both here and in `# Highest Priority Next Task`, and that one is legitimately
named there as current work.) And its B1 entry opened "Ten rules
exist", which has never been true of this repository: `strategies/` holds twelve
documents and no rule, and Belay has held zero strategies for its whole life.
Both now tell the reviewer to count rather than to trust the sentence. Checked
and left alone: "all 11 documents" in
`constitution/` is correct — `ls constitution/*.md | wc -l` returns 11.

**Closed against this branch, and it reaches `main` only when this pull request
merges.** The fix is on `fix/review-skill-numbering`; a reader on `main` today
still finds "the 13 ADRs" in the skill. That is a property of the branch, not a
qualification of the closure.

Priority: P3. Not watched by a test, and deliberately not: the fix is the
*absence* of a figure, and a test asserting that no count appears would pass on
any prose that happens to omit one. The numbering instruction corrected in the
same commit **is** watched —
`tests/test_session_handoff.py:287-445`, both checks confirmed red against the
unfixed skill before the fix landed.

---

# Open Findings

Twenty-one. Three are watched by `xfail(strict=True)` tests and will announce
themselves when closed; ten are housekeeping, blocked, ruled but
not yet applied, or — in finding 10's case — guarded by a test that passes. Three
came from the 2026-08-01 review, one from drafting ADR-014, and the last four
from implementing it and having that implementation independently verified.

**Corrected on this commit: the count is thirty-three, not twenty-one.** The
paragraph above describes the register as it stood before the 2026-08-14 review
was entered. It is kept as written rather than rewritten — Immutable Law VII —
and this sentence supersedes its count. Seven findings were added on 2026-08-14,
and they are six plus one rather than seven from one source: **F-007 to F-012
came from `reports/review/2026-08-14-review.md`, and F-013 came from writing that
review's ruling** — it corrects the review's own "Not found" section and is
recorded at `docs/OwnerDecisions.md:1046`, under the Part 8 that begins at
`docs/OwnerDecisions.md:935`. That took the count 21 -> 28. Five more are added on
this commit (F-014..F-018, 28 -> 33). `scripts/status.py` counts the `## `
sections below, so its figure is the one to trust over any number written in
prose, including this one.

**Corrected again on this commit: the count is forty-three, not thirty-three.**
The two paragraphs above are kept as written — Immutable Law VII — and this one
supersedes both counts. The twelve findings of
`reports/review/2026-09-04-review.md` (F-019 to F-025) and
`reports/review/2026-09-11-review.md` (F-026 to F-030) are registered on this
commit. **Ten of the twelve are open and are rows and sections below; two —
F-021 and F-026 — were verified fixed before they were written down and went
straight to `# Closed Findings`.** That is why the rows below run 34 to 43 while
the numbers in them skip 021 and 026: a finding closed before registration is
still registered, just not in this table, because `scripts/status.py` counts only
the `## ` sections under this heading. The arithmetic is 33 + 10 = 43, and
`scripts/status.py` derives that figure by counting rather than by reading this
sentence, which is again why its number is the one to trust over this one.

**Corrected again on this commit: the count is forty-two, not forty-three.**
The three paragraphs above are kept as written — Immutable Law VII — and this
one supersedes all three. F-022 — HANDOFF's "Current Repository State"
describing the repository four merged pull requests ago — closes on this
commit, at the same session close-out that corrects the section it was about;
see its entry in `# Closed Findings`. It leaves the table, which is why the
rows below run 34 to 42 rather than 34 to 43. The arithmetic is 43 - 1 = 42,
and `scripts/status.py` derives that figure by counting rather than by reading
this sentence, which is again why its number is the one to trust over this
one.

**Corrected again on this commit: the count is forty-one, not forty-two.** The
four paragraphs above are kept as written — Immutable Law VII — and this one
supersedes all four. F-025 — the review skill's hardcoded counts — closes on
this commit, on the owner's chat selection of 2026-09-19, in the same change
that corrects the skill's finding-numbering instruction; see its entry in
`# Closed Findings`. It leaves the table, which is why the rows below run 34 to
41 rather than 34 to 42. The arithmetic is 42 - 1 = 41, and `scripts/status.py`
derives that figure by counting rather than by reading this sentence, which is
again why its number is the one to trust over this one.

**The authority is `docs/OwnerDecisions.md:1120` (Part 9b), owner-selected
2026-09-19, and it approves registration and nothing else.** No fix for any of
F-019 to F-030 is authorised by it, none of them has a ruled fix, and none may be
worked on the strength of having a row here. That is the opposite of Part 8,
which approved six findings *for fix*; a reader who carries the Part 8 reading
across to these twelve will be wrong. Part 9b also declines to ratify the
severities and priorities — they are recorded, not endorsed.

**Neither report states a priority for any finding — grep them and there is no
`Priority: P` anywhere in either.** Severity is the report's grade; priority is
this registration's own mapping onto it, derived by this commit
(`4a96cac`) rather than restated from a document that never named one. The
mapping used is **Critical → P1, High → P2, Medium → P3, Low → P3** — wider
than the two-case rule stated further below in this preamble ("Critical maps
to P1 and Medium to P3"), which names only the two cases this table's older
rows needed and which this registration's twelve extend rather than replace.
**Recorded here as this registration's derivation, not as a ruling: the owner
may re-grade any of the twelve.**

**Both reports number their findings durably, neither carries a correction block,
and there is no overlap to withdraw.** `reports/review/2026-09-04-review.md:17-20`
reads the series forward from 018 and claims F-019 to F-025.
`reports/review/2026-09-11-review.md:48-51` reads it forward from 025 and claims
F-026 to F-030 — and that report opens by saying the pass **should not have run**,
because the cadence gate fired at seven days rather than fourteen. It narrows its
own obligations accordingly: nothing the 2026-09-04 pass found is re-raised in
its findings list, only in its meta-review
(`reports/review/2026-09-11-review.md:52-53`). That instruction is honoured here.
All twelve are registered once each, at the number its own report gives it, and
nothing is withdrawn as a duplicate — which is what makes this registration
unlike the 2026-08-21 one above.

**Every `path:line` carried across from those reports was re-verified against
this branch before it was written down, and several had moved.** The reports were
written against `fb5b919`; four pull requests and two register commits have
landed since. Where a citation moved, the section below carries today's line and
says what the report cited. Where a claim had stopped being true, the finding is
registered as closed rather than as a live defect. The reports themselves are not
edited — one file per review, forever.

**A live hazard for the next review, deliberately carrying no finding number.**
`.claude/skills/belay-review/SKILL.md:250-252` still instructs a reviewer to
"number them continuously across reviews — if the last report ended at F-014,
this one starts at F-015", which is numbering from the previous report's
*headings*. `CHANGELOG.md:64` names that exact instruction as the collision
mechanism; `CHANGELOG.md:62` is where it cost seven already-claimed numbers on
2026-08-21. The skill now contradicts itself rather than being simply wrong:
`.claude/skills/belay-review/SKILL.md:44-45` and `:51-53` were corrected when the
cadence gate landed and require calling `scripts/review_due.py`, from which
"finding numbers likewise come from all prose, not report headings". **Only
`scripts/review_due.py` assigns numbers, and only at the next due review** — so
this is recorded as a note for whoever runs that review rather than as a finding,
and no file under `.claude/` is edited by this commit.

**Corrected in place 2026-09-19: the hazard above is fixed, and the paragraph
is kept because a reader who has only ever seen `main` will still find the old
instruction there.** The skill is edited by *this* commit, on the owner's chat
selection of the same date — two choices, the numbering instruction and F-025's
hardcoded counts, and nothing wider. What that paragraph describes is now
`.claude/skills/belay-review/SKILL.md:279-299`, and it says the opposite: the
first finding takes the number `python scripts/review_due.py` printed on its
`first finding: F-NNN` line, the gate is the only authority on the next number,
and the number is never derived from where a previous report's headings ended.
The cadence section it used to contradict is now
`.claude/skills/belay-review/SKILL.md:42-79`, which states both verdicts the
gate prints and what to do on each. `tests/test_session_handoff.py:287-445`
holds both halves — that the numbering instruction names the gate, and that no
numbering paragraph counts on from the report before it — and both were
confirmed red against the unfixed skill. **It is fixed on this branch only, and
reaches `main` when this pull request merges**; until then the caution in
`docs/OperatorChecklist.md` stands for anyone working from `main`.

**A second unnumbered note for the next review, from the same pass and
deliberately not fixed here.** `scripts/review_due.py:90` describes
`highest_finding()` as returning "the highest F-NNN mentioned in any tracked
prose, on any ref". It does not: `scripts/review_due.py:97` lists only
`reports/` and `docs/`, and `:99` keeps only `.md` files — so an `F-NNN` in
`CHANGELOG.md`, under `.claude/`, or in a test is invisible to the gate. The
skill now states the real scope
(`.claude/skills/belay-review/SKILL.md:283-288`), and the docstring is left
alone because **editing the gate is outside what the owner selected for this
change**, and because whether the scope should be widened or the sentence
narrowed is a question for whoever runs the next review. Recorded here rather
than minted as a finding: only `scripts/review_due.py` assigns numbers.

**Five came from `/belay-review` on 2026-08-21, and the owner approved them on
2026-08-26 — recorded, with the provenance of that date, at
`docs/OwnerDecisions.md:1157` (Part 9c).** That Part also says what the approval
is not: the five are approved **as findings**, and no fix shape is ruled for any
of them. They are registered here as **F-014 to F-018**, which is *not* how
`reports/review/2026-08-21-review.md` heads them. That pass could not see the
2026-08-14 review — it was open on a branch and invisible to whoever looked next
— so it reused F-007..F-015, numbers that had already been claimed and already
ruled on. The correction block at the head of that report carries the
authoritative mapping, and the report's body is deliberately left as written so
it remains the record of what one pass found and believed.

**Four of that report's nine findings are withdrawn as duplicates, carry no
durable number, and must never be registered here.** Its F-008, F-009, F-010 and
F-012 restate the 2026-08-14 review's **F-007**, **F-012**, **F-008** and
**F-011** respectively — all four of which already have rows and sections below.
Registering them would count the same defect twice and inflate this table in the
flattering direction.

**Six came from `/belay-review` on 2026-08-01 and they carry durable
identifiers, which the rest of this table does not.** They are F-001 to F-006 in
`reports/review/2026-08-01-review.md`, numbered once and never renumbered, and
that report is the evidence — every one of them carries a `path:line` and was
produced by constructing the failure and running it rather than by reading.
**F-001, F-002 and F-005 closed on 2026-08-02 and have moved to
`# Closed Findings`; three remain below.** They
are listed here as well because `scripts/status.py:187-213` counts the `## `
sections in *this* file and knows nothing about `reports/review/`, so a finding
that lived only in the report would be invisible to the dashboard. That gap was
itself found by checking, after the review was already committed: the dashboard
would have reported thirteen open findings while nineteen were open, and it would
have under-reported in the flattering direction.

**Two registers, one ledger.** The review report is immutable — one file per
review, forever — so it is the permanent record of what was found and when. This
table is the live state. When one of F-001 to F-006 closes, it moves to
`# Closed Findings` here and the report is left untouched.

**Priority is not severity, and the two are mapped rather than equated.** The
report grades by which document is breached; a priority says what to do next.
Critical maps to P1 and Medium to P3, but F-002 is graded High and carried at P1
anyway — see its section for why.

**The count did not move on 2026-08-01, twice, and both times it was a
coincidence rather than a quiet period.** First `Option Data Is Unreachable At
The Stated Budget` **closed** on its own stated condition — both undocumented
properties established against the source: CC BY-SA 4.0 from its own
`LICENSE.md`, and expired contracts *are* retained, shown by a chain expiring
2019-03-15 still queryable in a database whose newest row is 2026-07-31 — while
`The Hosted SQL API Cannot Serve A Backfill` **opened** in its place.

Then later the same day that one **closed too**, on its own stated condition: a
`dolt clone` transport completes a three-year backfill in 4.4 seconds, verified
by running it. `A Fetch Stores Its Bytes Before Discovering The Series Is Empty`
**opened** in its place — found by an independent verification pass, in code that
predates the session, and made routine rather than theoretical by the very
transport that closed the finding above it.

**All three were found the same way and it is worth naming: by going and looking
rather than by reading.** Finding 13's original premise was falsified by querying
the source. Finding 14 was found by running one real fetch after the suite was
already green — and its own closing measurement produced a **fifth** wrong
reading of the same behaviour, an 11-day window at 37.4s where the recorded table
says 8 days took 0.4s. Finding 15 was found by a fresh reader attacking work its
author had just declared finished. **The suite touches no network and spawns no
subprocess by design, so it cannot find this class of thing** — which is the
standing lesson, not a one-off.

**Two of the three findings ADR-014's drafting opened closed the same day, by
implementing it.** The fetch record now carries the source key, the store version
and the store-relative path, and the identifier pattern was widened without any
governance amendment — `Knowledge/Identifiers.md` never stated a digit count.
What remains open from that batch is finding 17, which nothing in ADR-014
required fixing.

**Findings 18 to 21 came from implementing ADR-014 and from the independent pass
over that implementation, and the second of those is the one worth reading.** The
pass found **19 defect-grade errors across 93 claims; the author's own review of
the same work found none of them.** Eight were in committed code — a dedup that
collapsed two symbols with identical bytes into one record, an orphan check that
then reported the store clean, three Unicode digit forms reaching `save()` through
a pattern widened one commit earlier to prevent exactly that, a store walk that
covered two directory levels and reported `()` for everything else. All eight are
fixed, each with a regression test confirmed red against the pre-fix code. Four
were structural enough to stay open and are below.

**The pass ran after implementation, and ADR-014's own Required Follow-Up says
before.** `★ START HERE`, written by the same author in the same session, placed
it after step 6 — so two governance documents gave opposite orderings for one
mandatory step and the implementer followed the weaker one. Rule 6's one-way door
had already closed by the time the pass ran. Recorded in ADR-014's Status block.

**The original note, kept:** findings opened by *drafting* ADR-014 made the
pattern three for three. Ruling where artifacts live forces the fetch
record, the data store and the identifier standard to be read against each other,
which nothing had done: the record turns out to carry the one source identifier
the store deliberately does not use, the identifier space turns out to be too
small to fund one record per fetch, and an identifier reused at a new version
turns out to be filed as a version of the artifact it has nothing to do with. The
third was found by running it rather than by reading. **All three are facts about
the repository as committed and are true whether or not ADR-014 is ratified** —
but 19 has to be settled *before* it is, because identifiers are permanent and
`ArtifactRepository.save()` would start minting them.

**Finding 12 was found by drafting ADR-013 rather than by reading for defects**,
the pattern ADR-010 established: implementing or ruling a thing forces two
documents to be compared that nobody had compared before. It is true whether or
not ADR-013 is ratified — a fact about what the documents say, not a consequence
of the ruling.

**Finding 11 opened on 2026-07-31 and is the first one this repository has
recorded that is a contradiction between two *requirements* rather than a gap
between a document and its code.** It exists because the owner answered a
question, and the answer turned out to be incompatible with something the
roadmap already required. That is the scoping work doing exactly what it was for.

**Finding 10 is the largest thing on this list and it is a gap in the plan
rather than in the code.** It was found on 2026-07-31 by the repository owner
asking how funds, execution and taxes would eventually work — a question this
document had no answer to, because the roadmap never reaches them. Findings 2
and 8 turn out to be symptoms of it.

**Its watcher fired inside the commit that created it, which is worth reading
before writing the next one.** `test_every_expected_component_is_either_built_or_planned`
was written as a strict `xfail`, confirmed failing, and then the same commit
amended `docs/ROADMAP.md` — which closed the exact condition it watched, and the
suite went red with `XPASS(strict)` on the next run. The marker came off and the
test is now a passing regression guard. Nothing was wrong with the watcher; it
was aimed at "is this planned", and the answer became yes. The finding stays
open because the work is not *done*, and that half is what the dashboard counts.

Finding 9 opened on 2026-07-31 while implementing ADR-011 and is the only one
here watched in *reverse*: no `xfail` will announce its closure, but a test goes
red if anyone closes it the wrong way. See its section.

**The watchers can be trusted again.** All six were audited on 2026-07-30 and
2026-07-31 and all six asserted less than their names claimed. Five were
strengthened; the sixth could not be, because what it should assert *was* the
open question — ADR-010 answered it, and that test is now rewritten with its
marker removed. Every remaining watcher parses its governing document rather than
a list transcribed from it, so none can be satisfied without closing the gap it
stands for.

The dashboard reports five watched gaps against three watched findings, and both
figures are correct: finding 2 carries three tests — the `Workflow` base class,
the empty registry, and the workflow documents. `scripts/status.py` counts
`xfail` tests; the table counts findings. **Finding 10 is marked watched and is
in neither figure**, because its guard passes rather than xfails — see above.

Finding 5 has been **ruled** by ADR-006 and stays open only because part of its
follow-up is unapplied. The question it asked is settled; the editing is not
finished. What remains is recorded in its section.

Its counterpart closed on 2026-07-31. `Four Different Promotion Sequences` was
ruled by ADR-007 and stayed open on one unedited document; `strategies/Lifecycle.md`
is now annotated and the finding is in the closed table above.

Each row below has a section of the same name. `scripts/status.py` counts those
sections, so the dashboard's figure and this table agree by construction.

The numbers below are positions in this table, not durable identifiers — they
shift every time a finding closes, which is what made the old `xfail` markers
stale. Markers now cite section titles instead. Cite the title.

| # | Finding | Priority | Watched |
|---|---|---|---|
| 1 | Document metadata standard declared, never applied | P2 | yes |
| 2 | `Workflow` base class incomplete; registry empty | P2 | yes |
| 3 | `framework/registry.py` implements none of the Registry Specification | P2 | no |
| 4 | `ArtifactType` and the identifier prefixes are two vocabularies that disagree | P2 | yes |
| 5 | Five different promotion criteria lists | P3 | no |
| 6 | 22 framework modules have no test reference | P3 | no |
| 7 | Broken imports in `departments/` | P3 | no |
| 8 | No halt mechanism; demotion runs at review speed | P2 | no |
| 9 | Five backtest metrics cannot be built without a ruling | P3 | no |
| 10 | The roadmap does not reach the mission | P2 | yes |
| 11 | A home machine cannot guarantee a halt within seconds | P2 | no |
| 12 | The evidence classes have no class for observed fact | P3 | no |
| 13 | A fetch stores its bytes before discovering the series is empty | P2 | no |
| 14 | A statistical review cannot carry the survivorship disclosure (F-003) | P2 | no |
| 15 | `sample_adequate` is arithmetically identical to `significant` (F-004) | P3 | no |
| 16 | A series with a hole discloses full coverage (F-006) | P3 | no |
| 17 | An identifier reused at a new version is silently mis-filed | P2 | no |
| 18 | ADR-014 rules 5 and 8 cannot both be executed as written | P2 | no |
| 19 | Rule 7's orphan check is vacuous on every machine but the one that fetched | P2 | no |
| 20 | The store's version filenames carry the four-digit cap the identifiers shed | P3 | no |
| 21 | Every fetch reads every stored record | P3 | no |
| 22 | A strategy can still be signed into existence at Production (F-007) | P1 | no |
| 23 | The survivorship guard is defeated three ways in committed code (F-008) | P2 | no |
| 24 | A suite that could not run is reported as zero failing (F-009) | P3 | no |
| 25 | The dashboard's import health scans only `framework/` (F-010) | P3 | no |
| 26 | The roadmap denies the market data layer it declares complete (F-011) | P3 | no |
| 27 | HANDOFF describes a working tree that exists on no machine (F-012) | P3 | no |
| 28 | `test_findings_are_ordered_by_priority` cannot fail (F-013) | P3 | no |
| 29 | A promotion can be recorded with no evidence whatsoever (F-014) | P1 | no |
| 30 | `belay doctor` cannot fail (F-015) | P2 | no |
| 31 | `is_clean` decides whether the survivorship warning prints, and has no test (F-016) | P2 | no |
| 32 | The significance test's two-sidedness is asserted by nothing (F-017) | P3 | no |
| 33 | "Searched all 101 documents" has rotted to 107 (F-018) | P3 | no |
| 34 | Eight guards on the capital and provenance path are asserted by nothing (F-019) | P2 | no |
| 35 | The citation for "every decision requires written justification" points at the wrong line in nine places (F-020) | P2 | no |
| 36 | The dashboard's "could not run" branch destroys the page instead of reporting (F-023) | P3 | no |
| 37 | Nothing checks an artifact's identifier prefix against its type (F-024) | P3 | no |
| 38 | A significance result reports 1,000,000 observations where its own function refuses to name any number (F-027) | P3 | no |
| 39 | CI states the dashboard job fails when the regexes stop matching; it does not (F-028) | P3 | no |
| 40 | ADR-002 places `departments/` in a layer that remains prose; it holds Python, and `pyproject.toml` ships it (F-029) | P3 | no |
| 41 | `test_no_session_brief_is_orphaned` counts `docs/proposals/` as its own pointer set (F-030) | P3 | no |

Rows 14-16 and 22-41 carry their durable `F-NNN` identifier because, unlike the
rest of this table, they have one. It is in the row **and in the section heading**, which
is not decoration: `test_every_summary_row_matches_its_section_heading` compares
the two after normalising, so an identifier in only one of them turns the suite
red. It did, on the first attempt at this table.

Rows are worded to match their section headings exactly, because the two are kept
in step by hand and `scripts/status.py` counts the sections. Ruling status is
recorded above rather than in the row for the same reason — a row that drifts from
its heading is how this table stops being checkable.

---

## Document Metadata Standard Declared, Never Applied

`docs/DocumentStandard.md` specifies a metadata block on every document and states
the reason: so tooling can "index every document deterministically without parsing
prose." Exactly one document carries one — `strategies/StrategyTemplate.md` — and it
uses `owner:` where the standard says `author:` and omits five required fields.

The total was recorded here as 82 and in the standard as 81; it was 100 on
2026-07-31. Both figures are now derived by the watcher rather than written down,
which is the same fix applied to the Schema.md field count.

`scripts/status.py` parses prose with regular expressions because this is open.

Priority: P2. Watched by `test_every_document_carries_the_metadata_block`.

---

## Workflow Base Class Incomplete; Registry Empty

`workflows/README.md` states every workflow defines five things: trigger, required
inputs, departments activated, deliverables, completion criteria.
`framework/workflows/base.py` provides two.

`WORKFLOWS` is an empty dict; nothing calls `register()`. Thirteen workflows are
documented, none exist in code. `framework/workflows/events.py` defines eight event
constants against those thirteen — absent are weekly portfolio review, new regime,
strategy retirement and new experiment, while `MONTHLY_REVIEW` conflates the
Investment Committee with the monthly Strategy Promotion Review.

**The documents are in the same state as the base class. Found 2026-07-31 by
checking all thirteen rather than the two that were open.** Not one of them
defines all five things the README requires: the best is two (`Trigger` and
`Deliverables`), and `Monthly/StrategyPromotion.md` and
`Weekly/WeeklyPortfolioReview.md` define none of the five. `Workflow` therefore
cannot be filled in by transcribing these documents — whoever implements it is
writing doctrine and should expect to need a ruling.

**A second event-constant conflation, distinct from `MONTHLY_REVIEW`.** Both
`StrategyPromotion.md` documents were opened, and they are two workflows rather
than one file duplicated. `Events/StrategyPromotion.md` is triggered by "Promotion
threshold satisfied" and runs a single candidate through Validation → Operations →
Knowledge → Investment Committee. `Monthly/StrategyPromotion.md` is calendared,
evaluates *every* candidate, and ends in a `ReviewOutcome`. Different trigger,
scope and cadence — but `Event.PROMOTION = "promotion-review"` is a single
constant whose value matches the monthly document's title while living in the
event vocabulary, so it names neither unambiguously.

Priority: P2. Watched by three tests — the `Workflow` base class, the empty
registry, and the documents.

---

## framework/registry.py Implements None Of The Registry Specification

`strategies/Registry.md` describes the authoritative strategy inventory with nine
per-strategy fields and two rules: "Every strategy exists in exactly one lifecycle
stage" and "No duplicate identifiers are permitted."

`framework/registry.py` is a generic JSON key-value store enforcing neither. Its
`save()` replaces the entire file — the same history-destroying pattern fixed in
`ArtifactRepository`.

Not repaired in isolation: this needs replacing rather than patching, and the
validator now enforces the first rule for STRATEGY artifacts.

Priority: P2.

---

## ArtifactType And The Identifier Prefixes Are Two Vocabularies That Disagree

Both answer "what kind of artifact is this" and they do not carry the same kinds.
`ArtifactType` has **`PORTFOLIO` and `FAILURE`, which have no prefix** in
`Knowledge/Identifiers.md`. That document has **`DOC` / Documentation, which has
no enum member.** Seven of nine line up; the vocabularies are close enough that
the gap went unnoticed through five ADRs.

Found on 2026-07-31 while implementing ADR-010 rule 9, which had to map each
deliverable to an `ArtifactType` and so compared the two lists for the first time.

**The consequence is demonstrated, not theoretical.** ADR-010 maps `Paper Trade
Logs` and `Portfolio Health Report` to `PORTFOLIO`, and `Failure Investigations`
to `FAILURE`. Run against the implementation, `ArtifactFactory` refuses
`PORTFOLIO-0001`:

    Invalid artifact identifier 'PORTFOLIO-0001'. Expected PREFIX-NNNN with a
    prefix from ['DOC', 'EXP', 'REGIME', 'REV', 'RPT', 'RS', 'STRAT', 'WF']

So three documented deliverables cannot receive an identifier that says what they
are. The only way to store one today is to label it `RPT-`, which is untrue — and
identifiers are the one field `Knowledge/Identifiers.md` states can never be
corrected: "Identifiers are permanent. They are never reused."

**Closing this is a ruling, not an edit.** Either `Knowledge/Identifiers.md` gains
two prefixes or `ArtifactType` loses two members, and both directions touch a
governing document. Nothing here guesses which. The `DOC` direction is the same
question from the other side: `Documentation` may be a kind of artifact the enum
should carry, or a prefix for things that are not artifacts at all.

Priority: P2. Watched by
`test_artifact_types_and_identifier_prefixes_name_the_same_kinds`, which prints
both differences when it turns green.

---

## Five Different Promotion Criteria Lists

| Source | Count |
|---|---|
| `constitution/Promotion_Pipeline.md` | 7 |
| `strategies/PromotionCriteria.md` | 8, plus a 0–100 score nothing computes |
| `Validation/CapitalReview.md` | 6 |
| `workflows/Monthly/StrategyPromotion.md` | 7 |
| `Validation/Backtesting.md` | 9 minimum metrics |

`docs/ROADMAP.md` and `scripts/status.py` are built on the seven in
`Promotion_Pipeline.md`. That is a working assumption, recorded so it is not
mistaken for a reading of the whole repository. The roadmap's Stage 1 is keyed to
the backtest metric list instead, which is the only one specific enough to build
against.

Read in full on 2026-07-30: **no criterion appears in all five lists.** `Drawdown`
comes closest at four of five and is absent from `PromotionCriteria.md`, the one
document defining a 0-100 Promotion Score — a score with no weights, no mapping
and a threshold deferred to the Investment Committee. Three shared concepts are
named inconsistently in ways that change their meaning: regime robustness versus
compatibility, operational consistency versus stability versus readiness, and
risk-adjusted returns versus bare risk.

Governance question. Priority: P3. **ADR-006 is Accepted and every one of its
required follow-ups is applied** as of 2026-07-31 — the three departmental
documents are reconciled and the conformance test parses the constitutional list.

**It stays open on two divergences ADR-006 did not enumerate**, both flagged in
the documents themselves rather than fixed on a guessed reading:

- `PromotionCriteria.md` says `Execution Consistency` where the Constitution says
  `Execution quality`. ADR-006 read all five lists and named exactly three naming
  collisions; this is not among them. It either judged them different concepts —
  consistency is a track record, quality is a standard, the same distinction
  ADR-006 itself drew for readiness versus consistency — or missed it.
- `CapitalReview.md` omits four constitutional criteria and now reads
  `Consistency` beside `Operational consistency`. ADR-006 rule 5 rules omissions
  to be defects but enumerates only `StrategyPromotion.md`'s three, and adding
  four criteria to a review that "does not allocate capital" expands a
  department's remit.

Closing this needs a ruling on those two, not more editing.

---

## 22 Framework Modules Have No Test Reference

Down from 28, and from 23 on 2026-07-31 when `serializer.py` gained a test module
of its own. No module now fails to import, so the count is honest rather than
masked. Most of these should be rewritten rather than tested as they stand; the
number is a target to drive down as each roadmap stage lands.

The figure is re-derived by `scripts/status.py` on every run, so it is the one
number in this document that cannot go stale silently — but the **heading** can,
and did: it read 24 after `relationships.py` gained tests. If you close one of
these, change the heading too, because the table above is matched to section
titles by hand.

Priority: P3.

---

## Broken Imports In departments/

`departments/validation.py` imports `framework.services.backtesting`, which does not
exist. `departments/Research/research.py` imports `framework.departments.base`, which
is not a package. Both reach for structure described in `docs/notes/` and never
built. Latent — nothing imports either module.

Priority: P3.

---

## No Halt Mechanism; Demotion Runs At Review Speed

Surfaced by ADR-004, which rules that a demotion is always a review outcome and
never automatic. That is the right call — what a strategy has *earned* is not the
same question as whether it should be trading right now — but it leaves the second
question with no answer at all.

A strategy breaching a hard risk limit needs to stop within seconds.
`strategies/RiskFramework.md` defines eight mandatory per-strategy limits and none
are implemented; `constitution/Capital_Authority.md` is the document those limits
answer to. The only mechanisms Belay has for reducing exposure today are demotion
and retirement, and both run at the speed of a monthly review.

This is not a demotion bug. It is a missing axis: lifecycle stage records earned
capital, and a halt flag records whether the strategy is live. Conflating them
would make the emergency brake deliberative, which is exactly what ADR-004 rejects.

Depends on the risk engine, which does not exist. See `docs/ROADMAP.md`.

Priority: P2. Not watched — there is no specification concrete enough to test yet.

---

## Five Backtest Metrics Cannot Be Built Without A Ruling

`Validation/Backtesting.md` names nine minimum metrics. Four are built as of
2026-07-31. **The other five are each missing an input or a definition, and
building one means inventing what is missing.**

| Metric | What is missing |
|---|---|
| Win Rate | whether a win is a *period* or a *trade*. Different numbers. |
| Trade Count | trades. A return series contains none. |
| Exposure | position records. A `0.0` return could be flat or held-and-unchanged. |
| Benchmark Comparison | a second return series. |
| Tail Events | a threshold — worst *k*, beyond *n* sigma, or a quantile. |

Two of these were recorded in this document as computable from a return series
alone until 2026-07-31, which is how the finding surfaced: the correction is
what exposed that the remaining work is rulings rather than arithmetic.

**Win Rate is the dangerous one.** It looks like an afternoon, and the period
reading is the one most people would implement without noticing there was a
choice. A backtest reporting "62% win rate" means something different depending
on which was meant, and the number would be quoted in reviews either way.
Choosing quietly between two readings of one word is how the five-way
promotion-criteria divergence began.

**Watched in reverse, which is unusual enough to state.** No `xfail` will turn
green when this closes. Instead `test_only_the_backtest_metrics_adr_011_scopes_in_are_built`
parses the nine names from the document and asserts that exactly the four
ADR-011 rule 11 scopes in are implemented — so **the suite goes red the moment
a fifth appears**, and stays red until whoever added it updates the scope set,
which is the point at which they have to say which ruling they made.

Priority: P3. It blocks no gate today: `Risk-adjusted returns` and `Drawdown
behavior` are the constitutional criteria this family feeds, and both are
computable. See ADR-011 rule 11 and its "Still open, deliberately" section.

---

## The Roadmap Does Not Reach The Mission

`constitution/Mission.md:5` states that Belay exists for "evidence-driven
**capital allocation**", and line 38 that it "optimizes for decades—not days".
`docs/ROADMAP.md` sequences six stages — artifact contract, metrics, market
data, backtester, risk engine, services layer — and **none of them deploys
capital, places an order, holds a position, or reports a tax lot.**

The plan builds the machinery that decides whether a strategy deserves money,
and stops there. It never builds the part that then does anything about it.

### The checkable edge

`scripts/status.py`'s `PROMOTION_CRITERIA` names the component expected to make
each constitutional criterion computable, and `docs/ROADMAP.md` calls that list
"the engineering backlog". **Two of the seven expect a file that does not exist
and is named nowhere in the roadmap**: `framework/services/execution.py`
(`Execution quality`) and `framework/services/liquidity.py` (`Liquidity`).

They are not among the ten placeholders under `framework/services/` that Stage 5
promises to fill in — that directory holds `archive`, `base`, `critic`,
`librarian`, `performance`, `portfolio`, `promotion`, `regime`, `scientist` and
`universe`. So two promotion criteria the Constitution requires are expected from
components no stage of the plan ever produces.

### What is missing, and how much of it is already specified

Four things, and the second and third are not new findings so much as this one
seen from underneath:

- **Execution and broker integration.** No document names a broker. There is no
  `execution.py`, no `broker.py`, no order model. Nothing in Belay has ever
  placed, cancelled or tracked an order.
- **Live position state and a halt mechanism.** **This is finding 8.** ADR-004
  flagged it: a strategy breaching a hard limit "needs to stop within seconds",
  and Belay's only ways to reduce exposure run at monthly-review speed.
- **The daily operating loop. This is finding 2, and the specification already
  exists.** `workflows/` documents **thirteen** workflows including
  `Daily/MarketOpen`, `Daily/MiddayReview` and `Daily/MarketClose` — literally
  the thing that runs every morning — and `WORKFLOWS` is an empty dict. The
  operating layer is not unspecified. It is unbuilt, and unsequenced.
- **Tax lots and reporting.** Searched all 101 documents: `tax`, `wash sale`,
  `cost basis` and `1099` return **zero hits**. This one is genuinely absent
  rather than merely unbuilt, and whether it is in scope is a ruling nobody has
  made. The repository owner has stated it is intended; no document records that.

### Why this is a P2 and not a P1

Nothing is unsafe today, and the reason is worth stating plainly: **no capital
is at risk because nothing trades.** The absence is the mitigation. It becomes
urgent the moment execution work begins, and finding 8 is the specific thing
that must land before or alongside it — an execution layer without a halt
mechanism is the one ordering of this work that would be dangerous.

It is also a plan defect rather than a code defect, and no code contradicts the
mission. The roadmap simply stops early, and stopping early looked like
completeness because every stage it *does* list is real, well-sequenced and
being delivered.

### What needs a ruling before any of it is built

Recorded rather than guessed, because deciding these quietly is the failure this
repository keeps finding:

- **Is Belay single-operator, family, or a product for others?** Everything
  about broker credentials, cost and deployment follows from this and nothing
  states it.
- **Does Belay call an AI model at runtime?** `framework/` contains **no LLM
  call of any kind** — today Claude is the builder, not a component. The vision
  describes runtime agents. **Immutable Law II — "Black-box reasoning is
  prohibited" — bears on this directly**, and the shape that appears to satisfy
  it is: a model may generate hypotheses, and may never decide a promotion.
  Nothing has ruled it.
- **Is tax accounting in scope?** See above.
- **Broker as a swappable adapter.** Consistent with everything, implied by
  nothing. It is the owner's stated preference and is not written down.

### All four were tested against the documents on 2026-07-31. See `docs/EndState.md`

**Two of the four are rulable from documents alone and need nothing from the
owner** — the runtime-model question and the adapter question. **One cannot be
ruled by any amount of reading** — who Belay is for — though three narrower
yes/no questions in `EndState.md` do the same work. **One splits in half**: tax-aware
*evaluation* is implied by `constitution/Mission.md:7`'s "purchasing power", which
is an after-tax quantity; tax *accounting* is open and its size depends on the
first question.

**And the fourth question blocks ROADMAP Stage 2, which nobody expected.** Stage 2's
deliverable is "a defined boundary for obtaining a price series"
(`docs/ROADMAP.md:157-158`), and a boundary *is* an adapter contract. A fifth
blocker that was on no list is whether a fetched price series is stored inside the
repository. See `The Four Questions Were Not Four` above for the reasoning, and
`docs/EndState.md` for the fifteen-row decision table, the survivorship acceptance
criterion, and the external-service costs.

**Then the owner answered, the same day. See `docs/OwnerDecisions.md`.** Of the
four questions above: **who Belay is for is answered** — single-operator per copy,
never trading an account that is not its operator's, possibly distributed later as
an application each operator runs on their own hardware; **tax accounting is
answered at its small size** — the broker issues the documents and Belay
reconciles — **conditional on one broker and one account**; and the owner concurs
with the recommended reading on the runtime-model and adapter questions, which
authorises the ADRs to be drafted that way and does not rule them.

**Two things opened that were on no list.** Distribution of the application to
other operators is a different question from managing money and closing the first
does not close the second — it is a professional's question in the owner's
jurisdiction and it blocks nothing today. And finding 11 below, which is a direct
contradiction between the owner's hardware answer and this roadmap's own halt
requirement.

**Nothing here is ruled.** The finding stays open and stays P2 — an owner's answer
is a fact the documents lacked, not a rule they now contain.

`docs/ROADMAP.md` was amended on 2026-07-31 to name the missing stages so the
gap is visible rather than absent, but naming them is not scoping them. Each
carries an explicit note that it is unscoped. **Stage 9's description is now known
to be wrong** — it reads "Cost basis, lot selection, wash sales, and the records a
filing needs", which is the large branch the owner has ruled out. It is corrected
in `docs/ROADMAP.md` and the superseded wording is preserved there.

Priority: P2. Watched by
`test_every_expected_component_is_either_built_or_planned` — **as a passing
guard, not an `xfail`.** It was written as a strict `xfail`, confirmed failing
against both components, and then the roadmap amendment in the same commit
closed the condition it watched; the suite went red with `XPASS(strict)` and the
marker came off, which is the mechanism behaving exactly as designed.

It now guards the regression that produced this finding: **if a future session
deletes Stages 6 to 9, or drops a criterion's expected component from the plan,
the suite goes red.** It does not track whether any of it is *built* — that is
the dashboard's "3 of 7 computable" and "1 of 10 stages complete", and giving
one gap two counters that could disagree is a defect this repository has already
recorded twice.

---

## A Home Machine Cannot Guarantee A Halt Within Seconds

Opened, and then narrowed, on 2026-07-31 by `docs/OwnerDecisions.md`. **This is a
conflict between two stated requirements, not a defect in code — there is no code
on either side of it yet, which is the only reason it is cheap to fix.**

**Recorded as opened and narrowed within the session rather than tidied into its
final form**, because the sequence is the useful part: a fact was missing, the
finding was as wide as the missing fact, the owner supplied it, and the finding
shrank to what actually remains. That is the scoping work behaving correctly, and
a finding that appeared already-narrow would teach the next session nothing.

**As first written this said own-hardware-only and halt-within-seconds "cannot
both hold".** That was true while "your devices" could mean "my laptop, when I am
using it". The owner has since answered that **Belay gets a small dedicated
always-on machine at home**, which resolves the contradiction as stated: there is
something for the daily workflows and the halt to run on.

**What remains is narrower and sharper: a home machine is not a datacenter.** A
power cut, an ISP outage, or an operating system rebooting at three in the
morning each leave a position unattended, without warning and without Belay
knowing. So "within seconds" is met in the normal case and **not met in exactly
the cases that make anyone want it.**

The owner has also answered that Belay runs **only on hardware its operator
controls**, which removes an entire column of cost and engineering — see
`docs/OwnerDecisions.md` Q2 — and rules out the obvious mitigation of moving the
halt to a hosted machine.

`docs/ROADMAP.md:225-240` (Stage 7) requires that a strategy breaching a hard
risk limit "needs to stop within seconds", and `docs/ROADMAP.md:219-221` makes
that an ordering constraint on Stage 6: execution "must not land before Stage 7's
halt mechanism, or alongside it", because "an execution layer that can open
positions faster than Belay can close them is the one ordering of this work that
would be dangerous."

Stage 8 is now satisfied by the answer: `docs/ROADMAP.md:241-254` describes "the
thing that runs every day", and `workflows/` holds `Daily/MarketOpen`,
`Daily/MiddayReview` and `Daily/MarketClose` — three fixed times a day, every
trading day. An always-on machine runs them. **A missed hour costs a
days-to-months strategy nothing**, which the owner has also now answered is the
holding period, so the reliability bar for the daily loop is low.

**Stage 7 is the half that survives**, because the reliability bar for an
emergency brake is not low and cannot be made low by choosing a longer holding
period. A halt is needed precisely when something has gone wrong, and the states
in which a home machine is down are correlated with nothing that makes them
rarer at the moment they matter.

**Nothing here is ruled.** `docs/OwnerDecisions.md` Part 3 sets out three ways
out — a dedicated always-on machine, a protective order resting at the broker, or
holding nothing while Belay is not running — and **recommends the second as the
primary halt with the first as its supervisor.** The reasoning is not convenience:
**any halt that depends on Belay being awake, connected and correct fails exactly
when things are worst.** A resting stop survives Belay being off, the internet
being down, and Belay being wrong; it is the strategy's own risk limit made
external to Belay, which is a stronger guarantee than an internal flag can be.

**With the caveat that belongs in a `Disclosure` rather than a footnote**, in the
shape ADR-012 rule 7 established: a resting stop is not filled at the stop price
in a gap, and not every instrument and venue supports one. It **reduces**
exposure to the failure and does not eliminate it, and the residue has a known
direction — it fails worst in the conditions that make you want it. That is a
fixed constant on the artifact, not a caller-supplied string.

The third option — Belay holds nothing it is not watching — is a strategy
decision wearing an infrastructure costume and should be made as one.

It is recorded now rather than at Stage 7 because the answer changes what Stage 6
is allowed to be, and `docs/ROADMAP.md:219-221` already forbids discovering that
late.

Priority: P2. Not watched — there is no code to assert against, and a test that
parses two prose requirements to check they do not contradict each other would be
asserting the finding rather than watching it. It closes when a Stage 6/7 ruling
settles where the halt lives. **ADR-013 explicitly declines to settle it**, on
the ground that ruling an execution-safety property inside a data-boundary ADR
would commit the error that ADR's rule 2 rules against.

---

## The Evidence Classes Have No Class For Observed Fact

Found 2026-07-31 while drafting ADR-013, by opening
`constitution/Evidence_Standards.md` and `framework/artifacts/enums.py` together.

**`Evidence_Standards.md` recognises four classes and every one of them grades
how well a *strategy* has been tested** — Level A live validated, B paper
validated, C historical *simulation*, D hypothesis.

**A fetched price is none of them.** It is not a simulation; nothing was
simulated. It is an observation of what actually happened, and the ladder has no
rung for that. Grading it C because C is nearest would assert a simulation that
did not occur — the unstated convention ADR-011 exists to refuse.

**The constitution has the right vocabulary in a different document.**
`constitution/Operational_Constraints.md:9-17` requires Belay to distinguish
**Facts / Assumptions / Predictions / Opinions**, and a price observation is a
Fact in that sense. So the concept is constitutional; it is the *evidence
hierarchy* that has no slot for it.

**ADR-013 rule 8 routes around this rather than closing it**, and the route is
sound: a fetch record carries no `EvidenceRecord`s, so `strongest_evidence_level`
returns `None`, and `framework/artifacts/artifact.py:38-44` already rules that
"an unevidenced artifact has no grade". Nothing needs inventing for Stage 2.

It stays open because the routing works only while nothing needs to *grade* an
observation. The moment a promotion gate wants to weigh "this was measured"
against "this was simulated", the hierarchy has no way to express the
comparison — and `Evidence_Standards.md:39` says the hierarchy "may never be
reversed", which presumes every piece of evidence sits somewhere on it.

Priority: P3. Not watched — a test asserting a document lacks a concept would
pass for the wrong reasons forever. Closing it means amending
`Evidence_Standards.md`, which is inside ADR-002's frozen governance layer, so it
needs its own ruling rather than an edit.

---

## A Fetch Stores Its Bytes Before Discovering The Series Is Empty

Found 2026-08-01 by an independent verification pass, in code that predates this
session. **Pre-existing, and the clone transport is what makes it routine.**

`fetch_and_record()` stores the payload and *then* builds the record, and
building the record calls `series.period()`, which an empty series refuses:

```
ValueError: the series for COH is empty and covers no period
```

By then the bytes are already on disk. The store is append-only, so what is left
behind is a version nothing points at — and `fetch_record.py` names exactly this
outcome as the thing its rule-9 ordering exists to prevent: "A source refused
after its bytes had landed would leave an unattributable file in an append-only
store." That guard covers the survivorship refusal. It does not cover this.

**Why it is not an edge case on this source.** `DOLTHUB_STOCKS_SURVIVORSHIP`
records `delisted_prices=SURVIVORS_ONLY`, established by query. Every delisted
symbol therefore returns zero rows, so any backfill that walks a symbol list hits
this on every dead ticker — and a backfill over a symbol list is exactly what the
clone transport just made possible.

### RULED by the owner 2026-08-01 — validate before writing

**The owner's words: "empty result is unacceptable. fetch, validate and fill is
acceptable here."** Put to them as four readings, because `fill` carries three
incompatible meanings in a market-data context and one of them fabricates prices.
**The ruling is the first: reorder the work so nothing is written until the
answer has been checked.** Not gap-filling, not a second source, and explicitly
not synthesising the missing bars.

**Why the question was asked rather than guessed.** For COH there is no series to
patch — the source has zero rows, not a hole. So "fill" could only have meant
inventing a price history for a company that stopped trading, which
`docs/DECISIONS.md` already forbids twice over: ADR-005 rule 4 refuses a default
that "would be a fabricated estimate that nothing distinguishes from a real one",
and ADR-012 rule 10 refuses "a number that looks adjusted and is not". A backtest
over filled COH prices would look clean and be fiction. The owner confirmed the
safe reading; the dangerous one is recorded here so nobody re-derives it as an
obvious optimisation later.

**What to build, in order — this is the next session's first task:**

1. **Tests first, run against unchanged code to prove they fail.** The precedent
   to copy is `tests/data/test_fetch_and_record.py:226` —
   `test_a_source_with_no_survivorship_answer_is_refused_before_anything_is_stored`
   — which asserts `store.versions(...) == ()` after the raise. That is the exact
   shape this needs.
2. **A distinct exception type** (`EmptyFetch` or similar) in
   `framework/data/fetch_record.py`. **Not a bare `ValueError`, and the reason is
   operational rather than stylistic:** a backfill over a symbol list meets two
   failures constantly and they need opposite responses — "this symbol has no
   data" should skip and continue, "the transport broke" should stop. Today both
   surface identically and a loop cannot tell them apart. Since this source is
   `SURVIVORS_ONLY`, the first case is the common one.
3. **The check in two places, not one.** `fetch_and_record()` is the ordinary
   path, but `fetch_record()` can be called directly and it is the one that signs
   the artifact. Same two-link pattern as `_survivorship_of`, and for the same
   reason: **the guard that only covered the ordinary path is precisely the one
   that turned out not to hold** when an independent pass attacked it this
   session.
4. **Then re-run `python scripts/verify_clone.py`.** Its `KNOWN` check asserts the
   *current* broken behaviour — bytes orphaned, then a raise — so **that check
   must be inverted when this is fixed**, not deleted. If it still passes
   afterwards, the fix did not work.

Two things the ruling deliberately does **not** settle, so neither gets decided by
accident:

- **Whether an empty fetch deserves a signed record at all.** Refusing to write
  bytes is not the same as refusing to record that the source was asked and said
  nothing, and Law VII arguably wants the second kept. Left open.
- **Gap detection inside an otherwise-good series** — AAPL returning 250 of 252
  expected trading days. A real problem and a different one. Not in scope *here*,
  meaning not in this finding's fix — **but no longer out of scope for Belay.**
  This originally read "it needs a trading calendar Belay does not have", which
  the owner overruled on 2026-08-01: not having one is a reason to build or
  connect one, not a reason to stop asking the question. See
  `docs/OwnerDecisions.md` Part 7. The work now sits with F-006's ruling.

---

Surfaced by `scripts/verify_clone.py` on every run, labelled `KNOWN`, so it
cannot be rediscovered as a surprise.

Priority: P2. Not watched by an `xfail` — the behaviour is a raise rather than a
gap in a document, and a strict-xfail watcher would assert that a defect persists.

---

## A Statistical Review Cannot Carry The Survivorship Disclosure (F-003)

**F-003, High.** `reports/review/2026-08-01-review.md`.

`significance_artifact` takes `data_source: str`
(`framework/metrics/statistics.py:307-318`) and builds its `Disclosure` inline
(`:359-364`), so it never consults the source. A Validation Report computed on
survivor-only data carries no survivorship caveat at all. Verified by running it
against `DoltHubStocksSource` (`survivorship.is_clean` is `False`):
`known_limitations` contains no mention of survivorship.

`disclosure_from()` at `framework/data/fetch_record.py:446` exists to prevent
exactly this, has zero non-test callers, and cannot be used here because
`significance_artifact` accepts no `Disclosure`. Its own docstring at `:469-472`
describes the current signature as the defect.

> **Repointed 2026-08-02 from `:227` and `:250-253`.** Implementing ADR-014 added
> about 220 lines above this function and moved it, which is the failure mode
> ADR-013 rule 1 already has a note about — a citation that was accurate when
> written and was broken by work done elsewhere in the same file. Nothing about
> the finding changed.

**Gates ROADMAP Stage 3.** Stage 3's output is the return series this function
consumes; building it first means retrofitting the disclosure onto artifacts
already signed.

Fix: take a `MarketDataSource`, derive `data_source` and the survivorship half of
`known_limitations` from it, appending to ADR-012 rule 7's fixed strings rather
than replacing them.

Priority: P2.

---

## sample_adequate Is Arithmetically Identical To significant (F-004)

**F-004, Medium.** `reports/review/2026-08-01-review.md`.

`clears(n)` *is* the significance test and is monotone in n, so
`n >= needed <=> significant`. 60 random trials produced 0 mismatches — only
`(True, True)` and `(False, False)`. ADR-012 rule 8 exists to separate "not
significant" from "not enough data to tell"; the boolean does not implement that
distinction, though the number `minimum_observations` does.
`tests/metrics/test_significance.py:226-239` asserts only the one-way implication
and concedes the mechanism in its own docstring.

**Needs a ruling before code.** Either drop the boolean, or define adequacy
against something independent of the observed effect — a minimum count, a minimum
span, or regime coverage.

**Corrected in place 2026-09-19 (evening) — F-004 is now ruled as to shape.**
`docs/OwnerDecisions.md:1411` (Part 10e): adequacy is a minimum observation
count AND a minimum time span, both required, neither depending on the
observed effect; regime coverage is deferred as an open gap, because Belay
cannot measure a regime today. **The numbers are not ruled.** A research
proposal carrying candidate numbers,
`docs/proposals/sample-adequacy-definition.md`, has had one independent
adversarial pass (15 defects, 5 blockers, all applied) and awaits a second
pass and the owner's ruling on its seven questions. No code opens for this
finding until then. Original wording left standing under Law VII.

Priority: P3.

---

## A Series With A Hole Discloses Full Coverage (F-006)

**F-006, Medium.** `reports/review/2026-08-01-review.md`.

`period()` is first-bar-to-last-bar (`framework/data/contract.py:107-120`), so two
bars three years apart disclose a three-year sample period. Verified by
constructing one. The live route: an empty month is a *successful* chunk
(`framework/data/dolthub.py:360`), and the comment at `:286-288` promising "the
whole fetch fails rather than returning a series with a hole in it" sits inside an
`except SourceUnavailable` block, so it covers transport failures only.

**Partially overlaps something already recorded, and the review did not cite it.**
The finding above — `A Fetch Stores Its Bytes Before Discovering The Series Is
Empty` — already names gap detection as out of scope, on the grounds that it
"needs a trading calendar Belay does not have". That is true of detecting *which*
bars are missing. It is not true of the narrower claim here: noticing that two
observations cannot support a three-year coverage assertion needs only the count
beside the span, not a calendar. The review missed the existing note because it
grepped `docs/HANDOFF.md` rather than reading it, which is a real limitation of
how that pass was run.

**The calendar clause has since been overruled by the owner** — 2026-08-01,
`docs/OwnerDecisions.md` Part 7 — on the grounds that Belay not having a trading
calendar is a reason to build or connect one, not a reason to stop asking. So the
option set here is wider than the review described.

**Needs a ruling before code.** Two questions, and they should not be collapsed:
the narrow one — record observation count beside span, which needs no calendar and
is not blocked on anything — and the wider one, whether Belay acquires a trading
calendar and what a detected gap then does. Rule the narrow one first; it stops a
two-bar series claiming three years today.

**Corrected in place 2026-09-19 (evening) — both questions are now ruled.**
`docs/OwnerDecisions.md:1464` (Part 10f): the narrow fix — observation count
recorded beside span — is **authorised**, to be built at step 4 of the Part 9a
order, alongside F-004. `docs/OwnerDecisions.md:1487` (Part 10g): the wide
question is ruled as a trading-calendar **proposal** first, comparing options
with no code and no library chosen; once a calendar exists, an unexplained gap
**fails closed** — the fetch is refused rather than stored with a warning —
while a gap explained by the calendar or by a recorded reason such as a halt is
allowed and disclosed. Original wording left standing under Law VII.

Priority: P3.

---

## An Identifier Reused At A New Version Is Silently Mis-Filed

**Found 2026-08-02 by running it**, against the repository as committed, while
drafting ADR-014. Two independently produced fetch records were handed the same
identifier:

```
save(record A, RPT-0001 v1.0.0)                     -> written
save(record B, RPT-0001 v1.0.0), differing content  -> FileExistsError, correct
save(record B, RPT-0001 v1.0.1), differing content  -> ACCEPTED
  versions('RPT-0001') -> ['1.0.0', '1.0.1']
  latest('RPT-0001')   -> '1.0.1'
```

So the destructive case is caught (`framework/artifacts/repository.py:202-208`)
and the *silent* case is not. Two unrelated fetches become two versions of one
artifact, `latest()` names one of them current, and `get()` verifies its integrity
and vouches for it — every check passes, because each record is individually
sound. What is wrong is the claim the directory makes about them.

`framework/identifiers.py:11-13` is the file that says where this is supposed to
be caught: uniqueness "is not enforced here, and cannot be: this module sees one
identifier at a time. `ArtifactRepository` is where reuse becomes destructive, and
it refuses to overwrite a stored version." That sentence is true of one of the two
cases above.

Breach: `Knowledge/Identifiers.md:5` — "They are never reused." And
`Knowledge/Versioning.md:23-27`, since a version list that mixes unrelated
subjects is not the searchable history that document requires.

**Not exercised today, because nothing persists any artifact — which is F-002.**
It becomes live the moment anything does, and it is the failure mode that looks
exactly like success.

Priority: P2. Not watched by a test.

---

## ADR-014 Rules 5 And 8 Cannot Both Be Executed As Written

**Found 2026-08-02 by implementing ADR-014.** The two rules describe the same
code path and require opposite things of it.

**Rule 5**: "One record per stored series version, not one per fetch" — a fetch
that produced no new store version produces no new record. **Rule 8**: the
unprovenanced AAPL bytes are adopted by re-fetching them, and "if the bytes come
back identical, `store()` returns the *existing* version 1 and the new record's
`content_hash` proves it describes the file already on disk". **The adoption
fetch produces no new store version**, so rule 5 forbids the record rule 8
requires.

**Resolved in code by a test the ADR never names.** `fetch_and_record` asks
whether a record already covers *these bytes* rather than whether the store wrote
a file — so the adoption writes one (nothing covered them) and a genuine
unchanged re-fetch does not (something does). That reading satisfies both rules
and neither rule states it. `records_by_stored_version` in
`framework/data/fetch_record.py` is the lookup it requires, and ADR-014 does not
mention that such a lookup has to exist.

**Left open because the ADR text is what is wrong, not the code.** Rule 5's
wording should be amended to the test that was actually implemented, which is an
amendment to a ratified ADR and therefore the owner's.

Priority: P2. Not watched by a test.

---

## Rule 7's Orphan Check Is Vacuous On Every Machine But The One That Fetched

**Found 2026-08-02 by the independent verification pass**, in the rewrite ADR-014
rule 9 authorised.

Rule 9 permits a `.gitignore` comment to assert a fact about another subsystem
"only where something checkable holds that fact true — and the check must
interrogate the system, not the prose". The rewritten `.gitignore` names
`test_no_stored_version_in_this_repository_is_unrecorded`. That test walks
`data/market/`, which `.gitignore` itself keeps out of every clone — so on any
machine that has not fetched, it asserts `() == ()` and passes with nothing
examined.

```
fresh-clone simulation: orphans = ()  -> assertion PASSES vacuously
```

**This is the shape rule 9 exists to close, reappearing inside rule 9's own
implementation.** The test's docstring admits the vacuity; `.gitignore` does not,
and `.gitignore` is where the claim is made.

**Not obviously fixable by trying harder.** The check cannot be made non-vacuous
without either committing the bytes — which ADR-013 rule 4 refuses — or shipping
a manifest of expected store contents, which is a second copy of the truth. The
honest options are to weaken what `.gitignore` claims, or to accept that this
class of check is machine-local and say so in the comment.

Priority: P2. Not watched by a test.

---

## The Store's Version Filenames Carry The Four-Digit Cap The Identifiers Shed

**Found 2026-08-02 by the independent verification pass.** Pre-existing in
`framework/data/store.py:49`, and made load-bearing by ADR-014 rule 7.

`_VERSION_FILE` requires exactly four digits while `store()` writes
`f"{version:04d}"`, which is five at 10,000. So the ten-thousandth restatement of
one symbol writes a file the store cannot see:

```
filename written by store()'s own f-string: 10000-2a21fe6d592a19b7.bin
  _VERSION_FILE matches it?  False
  versions() sees it?        ()
  store() after v10000:      wrote 0001-c6c1c9a9c8543f1e.bin
```

Version numbering **restarts at 0001**, `latest()` stops being the newest, and the
invisible file drops out of `all_versions()` and therefore out of
`orphan_versions()` — it is unrecorded and reports as clean.

**The same defect, in the same repository, as the identifier cap closed the same
day**, and the commit that closed that one did not touch this line. Reachability
is low: 10,000 vendor restatements of a single symbol. It is recorded rather than
fixed because ADR-014's step list did not reach it and because a fix changes
filenames in an append-only store, which is a migration.

Priority: P3. Not watched by a test.

---

## Every Fetch Reads Every Stored Record

**Found 2026-08-02 by implementing ADR-014 rule 5.**

`fetch_and_record` consults `records_by_stored_version`, which reads and
integrity-verifies every artifact under the root on every call. So a backfill of
*n* symbols performs O(n²) record reads, and F-002's own entry says it "gates any
bulk backfill" — this is the cost that arrives once that gate opens. At 6,000
symbols the last fetch of the run reads 6,000 records, about 17 MB, before it
fetches anything.

**No index was built, deliberately**, and the reasoning is in the function's
docstring: an index is a second copy of the truth, and this repository has been
bitten three times by a derived thing disagreeing with what it derived from. That
is a defensible trade at today's scale and not at a universe backfill's.

**The trigger to revisit is the one ADR-014 already names for its growth** — the
first time Belay selects instruments rather than being handed them. Recorded so
that it is a decision then rather than a surprise.

Priority: P3. Not watched by a test.

---

## A Strategy Can Still Be Signed Into Existence At Production (F-007)

**F-007, Critical.** `reports/review/2026-08-14-review.md`. **Ruled for fix by the
owner 2026-08-14** — `docs/OwnerDecisions.md` Part 8.

**F-001 is not closed.** Its guard is on `ArtifactFactory.create()`
(`framework/artifacts/factory.py:61-71`) and nowhere else. `Artifact(...)` and
`ArtifactIntegrity.sign()` (`framework/artifacts/integrity.py:71`) are both public
and unguarded, so the same artifact is constructible in two lines. Executed
against the repository as committed: a STRATEGY artifact built directly at
`PRODUCTION` and signed reports `integrity verify -> True`,
`ArtifactValidator().validate -> True`, saves, and reloads from the repository
with its stage and its integrity intact.

**The stated defence covers the wrong attack.** `framework/artifacts/factory.py:55-60`
argues the round trip is safe because "the repository verifies the integrity hash
on read, so a stage that was earned survives the round trip while a hand-edited
one does not". Hand-editing is indeed refused — verified both on a saved strategy
and on `artifacts/RPT-0001/1.0.0.yaml`. But nobody has to hand-edit: the
constructor's output is signed by the same public function the repository then
verifies against.

**The missing pattern is already in the file next door.**
`framework/artifacts/validator.py:227-232` re-derives `evidence_level` and refuses
a mismatch, for the reason its own comment gives: "an artifact built by calling
`Artifact()` directly could claim Level A while carrying nothing but hypotheses,
and that claim is what a promotion gate reads". `strategy_stage` is the same kind
of claim and gets no such check (`framework/artifacts/validator.py:145-168`).

**One part is deliberately unruled.** The proposal's test for "birth" — version
`1.0.0` with no `parent_hash` — is the reviewer's construction and no
constitutional document states it. Attack it before implementing; the finding
survives either way.

Breach: `constitution/Paper_First_Capital_Doctrine.md:5-7`,
`constitution/Immutable_Laws.md:23-25` (Law III) and `:39` (Law V).

Priority: P1.

---

## The Survivorship Guard Is Defeated Three Ways In Committed Code (F-008)

**F-008, High.** `reports/review/2026-08-14-review.md`. **Ruled for fix by the
owner 2026-08-14** — `docs/OwnerDecisions.md` Part 8.

Three bypasses, all executed against `main`, all live on the path that produced
`artifacts/RPT-0001/1.0.0.yaml`:

1. A `SurvivorshipDisclosure` subclass overriding `known_limitations()` to
   `"None."` passes both links, because both test `isinstance`
   (`framework/data/contract.py:209`, `framework/data/fetch_record.py:436`) and
   the method is ordinary and overridable (`framework/data/survivorship.py:142-152`).
2. `source._survivorship = clean` succeeds past the read-only property
   (`framework/data/contract.py:218-227`).
   `tests/data/test_survivorship_cannot_be_softened.py:211-218` asserts only the
   public half — one underscore narrower than its own name.
3. `_survivorship_of` never checks that `source` is a `MarketDataSource`
   (`framework/data/fetch_record.py:435`), so a `SimpleNamespace` carrying the
   real source's name and a clean disclosure is accepted.

**These were first raised on 2026-08-02** with executed evidence
(`reports/review/2026-08-02-f003-partial-pass.md:43-121`) and have never been in
this table. Their only prior record was that report and one narrative paragraph
below. Registering them is sub-part 4 of the fix and is worth landing first on its
own.

Breach: `constitution/Evidence_Standards.md:45` for the mechanism,
`constitution/Governance.md:27` for the register.

Priority: P2.

---

## A Suite That Could Not Run Is Reported As Zero Failing (F-009)

**F-009, Medium.** `reports/review/2026-08-14-review.md`. **Ruled for fix by the
owner 2026-08-14** — `docs/OwnerDecisions.md` Part 8.

`run_tests()` builds a `note` distinguishing "could not run" from "not green"
(`scripts/status.py:84`, `:98`) and nothing renders it. The terminal line prints
only counts (`scripts/status.py:394`) and the card renders `"{failed} failing"`
whenever `ok` is false (`scripts/status.py:295`); both are zero when nothing ran.
**Observed, not predicted:** the first `python scripts/status.py` of the
2026-08-14 review, in a fresh checkout without the `dev` extra installed, printed
`tests  0 passing, 0 failing`.

Second mechanism, same function: `scripts/status.py:84` omits the `watched` key
that `scripts/status.py:306` reads, so the branch written to handle a suite that
cannot run raises `KeyError: 'watched'` and produces no dashboard at all.
`refresh-status.cmd:20-31` then reports the wrong cause.

Mitigated but not fixed by the red pill (`scripts/status.py:294`) and the
`refresh-status.cmd:35-43` pause, which say "the test suite is NOT passing" when
the truth is that nothing was measured.

Breach: `constitution/Evidence_Standards.md:45`,
`constitution/Operational_Constraints.md:19`.

Priority: P3.

---

## The Dashboard's Import Health Scans Only `framework/` (F-010)

**F-010, Medium.** `reports/review/2026-08-14-review.md`. **Ruled for fix by the
owner 2026-08-14** — `docs/OwnerDecisions.md` Part 8.

`module_health()` walks `framework/` alone (`scripts/status.py:113`) while the
section it feeds is headed "Modules that will not import"
(`scripts/status.py:348-349`) with no scope stated. `pyproject.toml:39-40` ships
`departments`, and four of its modules will not import — executed:
`departments.Research.research` and `departments.validation` reach for structure
that does not exist, and `departments/knowledge.py:6` and
`departments/operations.py:6` reference `Department` with no import for it at all.
The dashboard on the same tree reports `will not import  0`.

**The existing finding is narrower than the fact.** `Broken Imports In departments/`
above names two of the four and one of the two causes. `untested_modules()`
(`scripts/status.py:139`) has the same scope and should move with the fix.

Breach: `constitution/Operational_Constraints.md:5`.

Priority: P3.

---

## The Roadmap Denies The Market Data Layer It Declares Complete (F-011)

**F-011, Medium.** `reports/review/2026-08-14-review.md`. **Ruled for fix by the
owner 2026-08-14** — `docs/OwnerDecisions.md` Part 8.

`docs/ROADMAP.md:43` lists "No market data layer" under "What does not exist", in
a section introduced at `:13` as "confirmed by running or reading the repository".
`docs/ROADMAP.md:156` heads "Stage 2 — Market data (complete)" and `:165-167`
states ADR-013 is implemented in all ten rules. `framework/data/` holds eight
modules and 2,264 lines.

**The stale test count in the same block is not the finding** — `docs/ROADMAP.md:8`
dates the section and `:16-18` discloses that its numbers are a snapshot. The
structural list carries no such caveat, and this is the same failure the document
records against itself at `:15-18` recurring on the prose after being fixed on the
number.

Breach: `constitution/Operational_Constraints.md:5`, `:9-17`.

Priority: P3.

---

## HANDOFF Describes A Working Tree That Exists On No Machine (F-012)

**F-012, Medium.** `reports/review/2026-08-14-review.md`. **Ruled for fix by the
owner 2026-08-14** — `docs/OwnerDecisions.md` Part 8.

`docs/HANDOFF.md`'s `★★ READ FIRST` section states "The working tree holds seven
modified files and they are the F-003 fix." Every clone's working tree is clean.
The work is on `origin/f003-awaiting-verification` at `8db018f`, one commit ahead
of `main` with no divergence, seven files, +257/−44 — verified by `git ls-remote`
and `git diff --stat`. The section names no branch.

Its resume pointer compounds it: run `wf_<id>` under
`.claude/projects/C--Users-<user>-Atlas/.../workflows/scripts/`, a path `.gitignore:26`
keeps out of every clone. `git ls-files .claude` returns two files, both under
`skills/`.

**The work is not lost; the account of where it is, is wrong.** The 2026-08-14
review was one command from reporting it lost.

Breach: `constitution/Operational_Constraints.md:5`; `AGENTS.md:7` and `:9`.

Priority: P3.

---

## `test_findings_are_ordered_by_priority` Cannot Fail (F-013)

**F-013, Medium.** Found 2026-08-14 while recording the rulings for the six
findings above, and it corrects that review's own "Not found" section — see
`docs/OwnerDecisions.md` Part 8, final subsection. **Ruled for fix by the owner
2026-08-14** under the same Part.

`tests/test_status_dashboard.py:66-79` asserts that the priorities returned by
`status.open_findings()` are sorted. `scripts/status.py:213` returns
`sorted(findings, key=...)`. The assertion restates the implementation, so it
passes for every possible state of `docs/HANDOFF.md` — including the one it is
named to catch.

Constructed and run: with this table deliberately reordered to read
`P3, P2, P2, P2, P1, P3` — a triage list with a P1 fifth and a P3 first — all five
tests in `tests/test_status_dashboard.py` pass.

**The requirement and the implementation are different claims.** The document says
this table is a triage list; the dashboard sorts it on read regardless. Either the
test should assert the *document's* order, or the document should stop claiming an
order it does not keep. The first is the useful one, because the table is what a
human reads.

**Why it is worth more than P3.** It is the first confirmed instance in this
repository of the failure section C of
`.claude/skills/belay-review/references/red-team-checklist.md` exists for, and it
was missed by a mechanical sweep across all 35 test files that reported itself
clean — because the sweep excluded builtins and the tautology runs through
`sorted`. A green sweep is not a green surface.

**Demonstrated live on 2026-09-19, and deliberately left standing.** Registering
F-014..F-018 put a **P1** row at position 29 of the summary table above, below
fourteen P3 rows. The table is now knowingly in **registration order, not
priority order** — and `tests/test_status_dashboard.py:66-79` stayed green
through the entire change, because `scripts/status.py:213` sorts the list before
the assertion compares it. That is this finding, happening, in f6fb971, the
commit that registered the rows. Row 22 (F-007, P1) had already done the same
thing since 2026-08-14; F-014 makes it two.

**The table was not reordered to hide it.** Rows are kept in registration order
so that a row's position never has to move, which is what keeps the table
checkable against the `## ` sections beneath it. What is wrong is the document's
claim, at the head of this section, that the table is a triage list. Either the
test asserts the *document's* order, or the document stops claiming an order it
does not keep — and `scripts/status.py` already sorts for the rendered dashboard,
so a reader who wants triage order has one there. This note stands until the
finding is fixed.

Breach: `constitution/Operational_Constraints.md:5`.

Priority: P3.

---

## A Promotion Can Be Recorded With No Evidence Whatsoever (F-014)

**F-014, Critical.** `reports/review/2026-08-21-review.md`, which heads this
finding F-007 — a number the 2026-08-14 review had already claimed. That report's
correction block is authoritative and gives it the durable number F-014.
**Approved by the owner as a finding, 2026-08-26, reconfirmed 2026-09-19 —
`docs/OwnerDecisions.md:1157` (Part 9c). THE FIX IS UNRULED.** Nothing in this
repository decides what a `PROMOTE` must carry, or whether the change takes an
ADR. An owner ruling is owed before any code is written for this finding.

`review_artifact` — the only code in Belay that records a promotion — has no
`evidence` and no `relationships` parameter
(`framework/artifacts/review.py:70-84`), its only substance check is a non-blank
justification string (`framework/artifacts/review.py:131-136`), and it passes no
evidence to the factory (`framework/artifacts/review.py:167-174`). Executed by
the review: a signed, validating, storable REVIEW artifact moving
PROMOTION_REVIEW -> MICRO_CAPITAL on "Looks good.", with `evidence: ()`,
`relationships: ()`, `evidence_level: None`.
`tests/artifacts/test_review_decision.py` contains the string "evidence" zero
times — re-confirmed on this commit by `grep -c evidence`, which returns 0.

Breach: `constitution/Paper_First_Capital_Doctrine.md:45-47` — "Promotion
requires evidence. Never confidence alone." That sentence appears in exactly one
**authority** document, `constitution/Paper_First_Capital_Doctrine.md:45`, and
nowhere else except in reports and briefs that quote it. A recursive grep for
"requires evidence" across the tracked Markdown returns five files on this
commit: the constitution, this register,
`docs/proposals/register-rebuild-session-brief.md`,
`reports/review/2026-08-21-review.md` and `reports/review/2026-09-04-review.md`.
One authority, four quotations. No ADR has ever cited it; ADR-009 rules the
review record and never mentions evidence.

**Do this before the first REVIEW artifact is signed.**
`artifacts/RPT-0001/1.0.0.yaml` is still the only artifact in the entire git
history — re-confirmed on this commit with `git log --all --diff-filter=A` over
`artifacts/` — so no REVIEW artifact has ever been signed anywhere, and the shape
of a REVIEW's `content` is still free to change. It stops being free the first
time a REV is signed, because an artifact is signed over its content and
`Knowledge/Versioning.md:25` forbids rewriting an append-only record.

**Corrected 2026-09-19: that one-way door is ADR-014 rule 6's *reasoning*, not
its ruling, and the first version of this section said otherwise.** Rule 6
(`docs/DECISIONS.md:3375-3393`) is about the **fetch record's** signed content
gaining the source key, the store version and the store-relative path. It rules
nothing about REVIEW artifacts. What carries across is the argument it makes at
`docs/DECISIONS.md:3387-3393` — changing signed content is free only while
nothing is stored, and the first saved record turns every later change into a
migration of permanent records. The door is real, it is open, and **no rule names
it**, which is itself part of why this finding wants a ruling.

**This is not F-007, and the two sit on the same path.** F-007 is a STRATEGY
artifact being *born* at a capital stage through `Artifact(...)` plus
`ArtifactIntegrity.sign()`. This one is the promotion *record* carrying no
evidence. Closing either leaves the other open, which is why both are Critical
and both are named at the top of "Highest Priority Next Task".

**Proposed** fix, and it is a proposal rather than a specification because the
fix is unruled: per the review's Proposal section — require evidence on
`PROMOTE`, refused at construction beside the `justification` refusal, plus a
conformance test that parses the doctrine sentence rather than transcribing it.
Structural, so it wants an ADR rather than a patch; which number that ADR takes
depends on whether F-007's ruling lands first, ADR-014 being the highest ratified
today. **Contrast Part 8** (`docs/OwnerDecisions.md:949`), which made each
2026-08-14 finding's Proposal *the specification*. Nothing has done that for this
finding, so the paragraph above is a reviewer's suggestion and no more.

Priority: P1. Not watched by a test.

---

## `belay doctor` Cannot Fail (F-015)

**F-015, High.** `reports/review/2026-08-21-review.md`, which heads this finding
F-011; the durable number is F-015 per that report's correction block.
**Approved by the owner as a finding, 2026-08-26, reconfirmed 2026-09-19 —
`docs/OwnerDecisions.md:1157` (Part 9c). No fix shape is ruled.**

**The defect is that it inspects nothing.** `scripts/belay.py:19-31` is four
`print` calls and no check: the command has no way to reach a conclusion about
`constitution/`, `Knowledge/`, `strategies/` or `workflows/`, because it never
reads them. Executed by the review against a copy with all four deleted:
identical output, exit 0.

**The title needs one qualification, found on 2026-09-19 by re-running it.** On
Windows the command *does* fail — `python scripts/belay.py doctor` on this
machine (Windows 11, Python 3.12, console encoding cp1252) prints
`Belay Repository Health` and then raises a `UnicodeEncodeError` — the charmap
codec cannot encode `✓` — at `scripts/belay.py:25`, exiting 1. **That is not
the command failing a check.** It is a console that cannot encode the
checkmark, and it would crash identically on a repository in perfect health. The
finding stands as written: `belay doctor` can crash, and it cannot fail *for a
reason it checked*, because it checks nothing.

Breach: `constitution/Evidence_Standards.md:45` — "Every conclusion must
reference supporting evidence." Four conclusions, no evidence, and one of them is
that the document set holding Belay's authority is intact at a moment when it has
been removed.

**Why it survived four sessions**: it was recorded only in the review skill's own
checklist — `.claude/skills/belay-review/references/red-team-checklist.md:151`,
which names `scripts/belay.py:21` by line — and in **no register the dashboard
counts**, so nothing ever put it in front of a session reading `docs/HANDOFF.md`.
That checklist is tracked; the earlier wording here said it was in no document
Belay maintains, which was false and is corrected on 2026-09-19. The 2026-08-01
review declined to number the finding and the 2026-08-21 review overturned that.
This entry is the fix for the invisibility; the code is still open.

Mitigant, stated so it can be weighed down rather than argued away: nothing
consumes the output, and `scripts/status.py` genuinely re-derives everything it
prints.

Fix: delete the command, or make each line check the thing it names and return
non-zero when the check fails.

Priority: P2. Not watched by a test.

---

## `is_clean` Decides Whether The Survivorship Warning Prints, And Has No Test (F-016)

**F-016, Medium.** `reports/review/2026-08-21-review.md`, which heads this
finding F-013 — a number the 2026-08-14 review had already claimed. The durable
number is F-016 per that report's correction block. **Approved by the owner as a
finding, 2026-08-26, reconfirmed 2026-09-19 — `docs/OwnerDecisions.md:1157`
(Part 9c). No fix shape is ruled.**

`framework/data/survivorship.py:129-140` defines `is_clean`;
`framework/data/survivorship.py:159-162` uses it to decide whether the direction
warning — "Survivorship bias INFLATES every return measure and DEFLATES drawdown
and tail measures SIMULTANEOUSLY" (`framework/data/survivorship.py:71-77`) —
appears on every artifact derived from a source. A recursive grep for `is_clean`
across `tests/` and `framework/` returns two hits, both inside the module itself
(`framework/data/survivorship.py:130` and `:159`). Mutating `all()` to `any()` at
`framework/data/survivorship.py:138` passes the entire suite — **re-executed on
this commit: 635 passed, 1 skipped, 5 xfailed**, the same result the review
recorded when the suite stood at 626.

Not yet wrong: both existing sources answer in a shape where `all()` and `any()`
agree. The shape that breaks is `RETAINED` prices with `UNKNOWN` membership,
which `docs/ROADMAP.md:214-219` anticipates — the contract must carry both
questions "even though the first implementation answers 'no' to both", so that
the answer can be recorded "on the day a better source does".

**Related to F-008, and not the same finding.** F-008 is three ways a caller
*defeats* the survivorship guard. This is the single branch deciding whether the
caveat prints at all, asserted by nothing.

Fix: four parametrised assertions on the truth table in
`tests/data/test_survivorship.py`, each also asserting the direction warning is
present or absent as the row requires. Roughly eight lines.

Priority: P2. Not watched by a test.

---

## The Significance Test's Two-Sidedness Is Asserted By Nothing (F-017)

**F-017, Low.** `reports/review/2026-08-21-review.md`, which heads this finding
F-014; the durable number is F-017 per that report's correction block.
**Approved by the owner as a finding, 2026-08-26, reconfirmed 2026-09-19 —
`docs/OwnerDecisions.md:1157` (Part 9c). No fix shape is ruled.**

Every series in `tests/metrics/test_significance.py` has a positive mean against
a zero null (`tests/metrics/test_significance.py:42` and
`tests/metrics/test_significance.py:48`), so the property claimed at
`framework/metrics/statistics.py:219-221` — that an effect below the null is
significant in the other direction and needs the same sample to show it — is
untested. Removing the `abs()` at `framework/metrics/statistics.py:221` passes
the entire suite — **re-executed on this commit: 635 passed, 1 skipped, 5
xfailed**, the same result the review recorded when the suite stood at 626 — and
turns every below-null series into the "would need more than 1000000
observations" refusal at `framework/metrics/statistics.py:231-236`, which is the
direction that flatters.

Fix: one test, a below-null series through `significance()`, asserting
`t_statistic < 0`, `significant is True`, and `minimum_observations` equal to
that of its mirror-image positive series.

Priority: P3. Not watched by a test.

---

## "Searched All 101 Documents" Has Rotted To 107 (F-018)

**F-018, Low.** `reports/review/2026-08-21-review.md`, which heads this finding
F-015; the durable number is F-018 per that report's correction block.
**Approved by the owner as a finding, 2026-08-26, reconfirmed 2026-09-19 —
`docs/OwnerDecisions.md:1157` (Part 9c). No fix shape is ruled.**

`docs/ROADMAP.md:367` and `docs/HANDOFF.md:3218` both state the count as a fact.
`git ls-files '*.md' | wc -l` returned 107 when the review ran on 2026-08-21;
**re-run on this commit it returns 114**, so the figure has rotted twice and the
"107" in this finding's own title is now historical too. The title is not
corrected because finding titles are durable identifiers here; the number to
trust is the one in this paragraph.

`docs/DocumentStandard.md:5-7` records the precedent exactly — the count "was
written as 81, and was 100 by 2026-07-31" — and says
`tests/test_governance_conformance.py` derives both figures instead of stating
them.

The underlying search claim still holds. This is number rot, not a false
conclusion.

**One citation was repointed on this commit.** The review cites
`docs/HANDOFF.md:2599` for the second occurrence; registering the 2026-08-14 and
2026-08-21 findings moved that line down, and it is `docs/HANDOFF.md:3218` as of
this commit.

Fix: drop the number and date the claim, or derive it the way
`docs/DocumentStandard.md` already does.

Priority: P3. Not watched by a test.

---

## Eight Guards On The Capital And Provenance Path Are Asserted By Nothing (F-019)

**F-019, High.** `reports/review/2026-09-04-review.md:89`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only. No
fix is ruled.**

Forty-nine one-token bugs were applied to load-bearing logic and the suite run
against each, and eight survivors are both undetected and consequential. (The
report's own tally of survivors does not close: it says thirteen survived and
then accounts for eight plus two boundary cases plus four masked by a second
guard, which is fourteen. The eight are enumerated individually there and here,
and the enumeration is what was re-executed; the summary figure is not relied
on.) Four of the eight mint a signed, valid, storable artifact stating
something untrue about a strategy's capital — among them a review whose declared
outcome is `Retire` while the strategy moves from Promotion Review into
`MICRO_CAPITAL`, and one reading `Promote` while the strategy descends from
Production to Paper Trading.

**Re-executed on this commit rather than carried over.** The eight mutations were
re-applied one at a time to a `git archive` copy of this branch under a scratch
directory, `__pycache__` cleared before each run, baseline confirmed
`3 failed, 632 passed, 1 skipped, 5 xfailed` before the first and after the
last — a `git archive` tree has no `.git`, so the three `git check-ignore`
tests fail there regardless (`CHANGELOG.md:83`); that is not the branch's own
suite result, which is `635 passed, 1 skipped, 5 xfailed`. **All eight still
survive at that archive baseline.** The working tree was not modified. The
eight, at their lines on this branch — all eight unmoved since the report:
`framework/artifacts/validator.py:157` (a STRATEGY with no stage validates),
`framework/artifacts/validator.py:165` (a REPORT carrying `PRODUCTION` validates),
`framework/artifacts/review.py:228` (`RETIRE` not landing at `RETIRED`),
`framework/artifacts/review.py:265` (`PROMOTE` on a descent),
`framework/data/fetch_record.py:138` (a record naming bytes it was not signed
over), `framework/data/fetch_record.py:317` (matching on the hash alone — the
exact regression `framework/data/fetch_record.py:306-311` records as having
already happened once), `framework/data/fetch_record.py:367` (rule 9's
"checked **before** anything is written" unheld), and
`framework/data/survivorship.py:138` — which is F-016 above, already open, and is
counted there rather than twice.

Breach: `constitution/Evidence_Standards.md:45` — "Every conclusion must
reference supporting evidence." The conclusion "these eight guards hold" is
supported by reading the code, which is the standard Belay refuses from a
strategy. `.github/workflows/conformance.yml:17-19` states the entitled claim
correctly — a green badge means the suite ran — and this finding is the size of
the gap between that and health. **Citation repointed on this commit:** the
report cites `:15-17`; correcting the numbering note in that file on `9ff5a58`
moved the sentence down two lines.

Proposed fix, and it is the report's proposal rather than a ruling: eight
regression tests, one per row, each confirmed red against its mutation first. Six
need no fixture. No production code changes. Step 2 of the owner-approved Stage 3
ordering (`docs/OwnerDecisions.md:1076`, Part 9a) — which sequences it and rules
nothing about it.

Priority: P2. Not watched by a test.

---

## The Citation For "Every Decision Requires Written Justification" Points At The Wrong Line In Nine Places (F-020)

**F-020, High.** `reports/review/2026-09-04-review.md:155`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only. No
fix is ruled.**

Nine tracked locations cite `workflows/Monthly/StrategyPromotion.md:37` for the
sentence "Every decision requires written justification." The sentence is at
`workflows/Monthly/StrategyPromotion.md:43`; line 37 of that file reads "Remain
Current Stage". Both re-read on this commit and both unchanged. The nine, all at
the lines the report gives and all still wrong today:
`framework/artifacts/review.py:129` (the comment), `:134` (inside the `ValueError`
a human reads when their review is refused), `docs/DECISIONS.md:982`, `:1099`,
`:1182`, `:1344` — four of them inside ADR-008 and ADR-009, **both Accepted** —
`strategies/ReviewTemplate.md:75`, `docs/HANDOFF.md:1536`, and
`tests/artifacts/test_review_decision.py:127`.

**This is not a prediction.** The citation is already wrong in a runtime error
message, and anyone who follows it lands on a line that says something else. The
four neighbouring citations cover promotion, rejection and retirement
individually; `:43` is the only source for the general rule the code implements,
so the one load-bearing citation of the set is the broken one. It is the same
shape as ADR-002's "eight promotion gates", which also stood inside an Accepted
decision until ADR-007 amended it.

**Neither existing enforcement can see it.**
`tests/test_session_handoff.py:178` checks only that a cited line number is
inside the file, and 37 is. The report (`reports/review/2026-09-04-review.md:183`)
says five of the nine write the bare basename `StrategyPromotion.md:37`;
re-counted on this commit it is **six** —
`framework/artifacts/review.py:129`, `docs/DECISIONS.md:982`, `:1182`, `:1344`,
`docs/HANDOFF.md:1536` and `tests/artifacts/test_review_decision.py:127` write
the bare form, while `framework/artifacts/review.py:134`,
`docs/DECISIONS.md:1099` and `strategies/ReviewTemplate.md:75` already qualify
it with `workflows/Monthly/`. The bare basename resolves to two files —
`workflows/Monthly/` (59 lines) and `workflows/Events/` (37 lines) — and
`tests/test_session_handoff.py:223` passes if any candidate is long enough. Both
line counts re-measured on this commit.

Breach: `constitution/Evidence_Standards.md:45`.

Proposed fix, unruled: change `37` to `43` in all nine and qualify the six bare
ones. Then extend the citation test so that a `` `path:line` `` followed by a
quoted string checks the quote against the cited line, and so that an ambiguous
basename is reported rather than passed on the longest candidate. The
renumbering alone leaves the mechanism intact.

Priority: P2. Not watched by a test.

---

## The Dashboard's "Could Not Run" Branch Destroys The Page Instead Of Reporting (F-023)

**F-023, Medium.** `reports/review/2026-09-04-review.md:304`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only. No
fix is ruled.**

`run_tests()` has a branch for the case where pytest cannot be launched. It
returns a dict with no `watched` key (`scripts/status.py:84`), which `render()`
reads unconditionally (`scripts/status.py:306`), so the script raises `KeyError`
and writes no page at all. `scripts/status.py:70-74` states the intent this
contradicts: pytest is run as a separate process "so a test that crashes cannot
take this script down with it."

**Re-executed on this commit**, with `subprocess.run` raising `OSError`:

```
run_tests() -> {'ok': False, 'passed': 0, 'failed': 0, 'note': 'could not run: ...'}
status.main() raised: KeyError 'watched'
    OUTPUT.write_text(render(data), encoding="utf-8")
  File "scripts/status.py", line 306, in render
    <div class="card"><div class="num">{tests["watched"]}</div>
```

Both cited lines are unmoved. The defect is that the branch written to keep the
dashboard reporting under exactly this condition is the branch that stops it.

Breach: `constitution/Operational_Constraints.md:5`. Medium rather than higher
because the failure is loud — the `dashboard builds` job would go red. The
adjacent false-note and `0 passing, 0 failing` behaviour at
`scripts/status.py:394` belongs to F-009 above and is counted there.

Proposed fix, unruled: `"watched": 0` in the dict at `scripts/status.py:84`,
render `note` when it is non-empty, and set the note on the pytest-absent path
too. Three lines, which the report says the already-ruled F-009 fix should absorb
rather than land separately.

Priority: P3. Not watched by a test.

---

## Nothing Checks An Artifact's Identifier Prefix Against Its Type (F-024)

**F-024, Medium.** `reports/review/2026-09-04-review.md:354`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only. No
fix is ruled.**

`Knowledge/Identifiers.md:25-57` maps each prefix to a kind of artifact. No code
compares the two. `framework/artifacts/factory.py:34` calls
`validate_identifier`, and `framework/identifiers.py:108-115` takes only the
string — shape and prefix against a whitelist, never against the artifact's type.
Both citations unmoved.

**Re-executed on this commit**, against the repository as committed:

```
ArtifactFactory().create("REV-0001", ..., ArtifactType.STRATEGY, strategy_stage=IDEA)
  type / id : Strategy / REV-0001   validates: True
```

`Knowledge/Identifiers.md:61` — "Identifiers never change" — is what makes it
permanent once written.

**This is not the open finding it resembles.** Row 4 above, "ArtifactType And The
Identifier Prefixes Are Two Vocabularies That Disagree", is about the two lists
not containing the same kinds. Reconciling them would still leave nothing
comparing an individual artifact's prefix to its own type.

Breach: `Knowledge/Identifiers.md:25-57` and `:61`. Medium: drift between a
governing document and the code that has not yet produced a false claim, because
`artifacts/RPT-0001/1.0.0.yaml` is the only artifact that exists and its prefix
is right.

Proposed fix, unruled: a type-to-prefix mapping beside `DELIVERABLE_ARTIFACT_TYPE`
in `framework/artifacts/enums.py`, checked in `ArtifactFactory.create` after
`validate_identifier`, covering the seven types that have a prefix and skipping
the two the vocabulary finding leaves unruled. Step 5 of the Stage 3 ordering
(`docs/OwnerDecisions.md:1076`, Part 9a), which sequences it and rules nothing.

Priority: P3. Not watched by a test.

---

## A Significance Result Reports 1,000,000 Observations Where Its Own Function Refuses To Name Any Number (F-027)

**F-027, Medium.** `reports/review/2026-09-11-review.md:180`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only. No
fix is ruled.**

`minimum_observations_for_significance` refuses, by design and with a docstring
explaining why (`framework/metrics/statistics.py:204-207`), to return
`_MAX_OBSERVATIONS` when no sample size would establish the effect;
`framework/metrics/statistics.py:222-226` is that refusal. `significance()`
catches it sixty lines later and substitutes exactly the value the refusal exists
to avoid (`framework/metrics/statistics.py:284-289`, with
`_MAX_OBSERVATIONS = 1_000_000` at `:71`), writes it to `minimum_observations`
(`:302`), derives `sample_adequate` from it (`:303`), and
`significance_artifact` puts it in the artifact's `parameters` (`:375`) — which
`framework/metrics/reporting.py:219-232` places inside the integrity hash. Every
citation unmoved.

**Re-executed on this commit**, on a series whose mean sits exactly on a zero
null (`[0.01, -0.01, 0.02, -0.02]`):

```
minimum_observations_for_significance(...) -> ValueError: the observed mean is
  indistinguishable from the null, so no sample size makes it significant;
  this is not a shortage of data
significance(...) -> minimum_observations = 1000000
                     sample_adequate      = False
                     significant          = False , p = 1.0
```

One number stands for three different states — "no effect exists", "no sample
could ever show it", and "a million would do it" — and no test constructs any of
them.

Breach: ADR-012 rule 8, `docs/DECISIONS.md:2231-2238` — "**A sample below that
number has not failed the test — it has not taken it**, and reporting those two
states identically is the failure this rule exists to prevent." The substitution
runs that prohibition in the opposite direction. The constitutional line is
`constitution/Operational_Constraints.md:5`. Medium deliberately:
`significance_artifact` has no non-test caller today and no Validation Report has
ever been signed, so no false claim has been produced yet — and
`Knowledge/Versioning.md:25` means the first one cannot be corrected.

Proposed fix, unruled: make the two states distinguishable rather than collapsing
them — `minimum_observations` becomes `int | None`, with the reason carried
alongside. Step 5 of the Stage 3 ordering (`docs/OwnerDecisions.md:1076`,
Part 9a), which sequences it and rules nothing.

Priority: P3. Not watched by a test.

---

## CI States The Dashboard Job Fails When The Regexes Stop Matching; It Does Not (F-028)

**F-028, Medium.** `reports/review/2026-09-11-review.md:261`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only. No
fix is ruled.**

`.github/workflows/conformance.yml` tells the reader its `dashboard builds` job
"fails outright if the regular expressions in `scripts/status.py` stop matching
the prose they parse". The first half of that sentence holds —
`scripts/status.py:403` returns 1 when the suite is not green. The second does
not: no parse function raises, each returns an empty list, and the page renders
"Nothing to report."

**Citation repointed on this commit.** The report cites
`.github/workflows/conformance.yml:110-115`; the numbering correction applied on
`9ff5a58` moved the comment down two lines and it is `:112-117` today.

**Re-executed on this commit.** `scripts/status.py:182` matches a roadmap heading
on a literal em dash. Against a scratch copy of `docs/ROADMAP.md` with one
heading's em dash replaced by a colon and nothing else changed,
`roadmap_stages()` returned **9 stages, 2 complete** against the unmutated **10
stages, 2 complete**, raised nothing, and did not report Stage 3 as missing. The
stage leaves the denominator, so the completion ratio *improves* from 20% to 22%
— the failure runs in the flattering direction — and `dashboard builds` stays
green.

Which of the parse functions are covered, re-checked by grep over `tests/` on
this commit: only `status.open_findings` and `status.PILLS` are named by any
test. `roadmap_stages`, `decisions`, `untested_modules`, `module_health`,
`run_tests`, `repo_stats` and `implementation_state` are named by none. **This
contradicts the report's own claim at
`reports/review/2026-09-11-review.md:265-266`** — "Three of the six regexes
it refers to are guarded by tests" — without resolving which count is right;
the report's re-derivation two paragraphs later (`:299-303`) finds the same two
this entry finds, so the report disagrees with itself and this entry inherits
the two-count side of that disagreement.

**Narrower than it looks.** `reports/review/2026-09-04-review.md:678-684` already
lists the six regexes as unchecked and is right. The finding here is the one that
pass did not make: a tracked document **states that they are checked**, which is
why nobody has written the tests. An unchecked surface documented as unchecked
costs nothing; one documented as covered is why it stays uncovered.

Breach: `constitution/Evidence_Standards.md:45`. Medium rather than High: the
false claim is about a CI job, not about a strategy, and nothing computes on it.

Proposed fix, unruled: delete the second clause, or make it true — assert
`roadmap_stages()` matches every `^## Stage` line in `docs/ROADMAP.md`, the same
shape `test_every_open_finding_has_a_parsed_priority` already uses. The report is
explicit that loosening the regex is the wrong fix.

Priority: P3. Not watched by a test.

---

## ADR-002 Places `departments/` In A Layer That Remains Prose; It Holds Python, And `pyproject.toml` Ships It (F-029)

**F-029, Medium.** `reports/review/2026-09-11-review.md:338`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only. No
fix is ruled.**

`docs/DECISIONS.md:127-131` (ADR-002, **Accepted**) puts `departments/` in the
Governance Layer and says "It remains prose"; `docs/DECISIONS.md:133-134` puts
all new code in `framework/`. `docs/Architecture.md:25-28` and `:36-38` reproduce
both. The directory is not prose: re-measured on this commit,
`find departments -name "*.py" | xargs wc -l` returns **80 total** — 78 across
the five named modules (`base.py` 12, `knowledge.py` 14, `operations.py` 14,
`validation.py` 18, `Research/research.py` 20) plus two 1-line `__init__.py`
files (`departments/__init__.py`, `departments/Research/__init__.py`) that make
up the remaining 2. `pyproject.toml:31` — "Per ADR-002 only the mechanics
layer is packaged" — sits directly above `pyproject.toml:39-40`, which list
`"departments"` and `"departments.Research"` in `packages`. Every citation
unmoved.

**This is not the open finding it resembles.** Row 25 above (F-010) is that the
dashboard's import health walks `framework/` alone. Widening that scan would make
the dashboard report four broken modules and would leave the contradiction
between an Accepted ADR and the build untouched.

Breach: `docs/DECISIONS.md:129` — an Accepted ADR asserting something the
repository contradicts, graded Medium as doc-vs-code drift, the same grade as
F-011 above, which is the identical shape.

**The fix is a ruling, not an edit, and the report says so.** Either drop the two
entries from `pyproject.toml:39-40`, which costs nothing today because the four
modules do not import, or amend ADR-002 to move `departments/` into the mechanics
layer inline with the original text preserved, as ADR-007 amended the "eight
promotion gates" sentence. Part 9b authorises neither.

Priority: P3. Not watched by a test.

---

## `test_no_session_brief_is_orphaned` Counts `docs/proposals/` As Its Own Pointer Set (F-030)

**F-030, Low.** `reports/review/2026-09-11-review.md:411`. **Registered
2026-09-19 under `docs/OwnerDecisions.md:1120` (Part 9b) — registration only. No
fix is ruled.**

The test that exists to prove a session brief is reachable from a document a
session actually reads includes the brief directory in the set it searches.
`tests/test_session_handoff.py:123-127` builds `pointers` from `docs/HANDOFF.md`,
`docs/OperatorChecklist.md` and `docs/OwnerDecisions.md` — and then appends
`"".join(read(p) for p in (REPO / "docs" / "proposals").glob("*.md"))`. Both
citations unmoved, and the second `"".join(...)` term is still there on this
commit. Its docstring at `tests/test_session_handoff.py:110-117` states the
property it means to hold: a brief nobody links to "is in the same position as
work on an unmerged branch, which is the failure that has cost this repository
twice."

So two briefs naming each other and named by nothing else satisfy it. The report
constructed exactly that and the file passed — at six tests then; the cadence
gate has since added three, and `python -m pytest -q tests/test_session_handoff.py`
returns **9 passed** on this commit. The construction was not re-run here,
because it requires writing files into `docs/proposals/`; the line that causes
it was re-read instead.

**The briefs on this branch are not orphaned in fact.**
`docs/OperatorChecklist.md:24` and `:26` name both of them. The test passes for
the right reason today; it would also pass for the wrong one, and its own
docstring records that it caught a real orphan on its first run. (Verified current on this branch; both line numbers will shift by roughly 21 lines when PR #10 merges.)

Breach: none in the constitution, so Low by the severity rule rather than by
judgement. The nearest governing sentence is `AGENTS.md:19`, which puts
`docs/HANDOFF.md` and not `docs/proposals/` in every session's mandatory reading
— the distinction the pointer set erases.

Proposed fix, unruled: delete the second `"".join(...)` term, confirmed red
against two mutually-referencing briefs first. Whether `reports/review/*.md`
should then count as a pointer is a judgement the change forces and nothing has
made.

Priority: P3. Not watched by a test.

---

# Repository Composition

Modules that will not import: 0, down from 15.
Framework modules with no test reference: 22, down from 28.

Real implementation remains confined to `framework/artifacts/`,
`framework/metrics/` and `framework/identifiers.py`. There is no risk engine, no
market data layer, no backtester, and no strategy implementation. See
`docs/ROADMAP.md` for the inventory of what the documents specify and what exists.

`framework/metrics/` grew from one module to seven on 2026-07-31 — `returns.py`,
`volatility.py`, `risk_adjusted.py` and `reporting.py` under ADR-011, then
`distributions.py` and `statistics.py` under ADR-012, all joining `drawdown.py`.
Every one is referenced by tests, so the untested-module count is unchanged at
22, which is the intended shape: new code arrives with its tests rather than
adding to that number.

`distributions.py` is a **leaf module importing nothing from Belay**, the same
role `framework/artifacts/primitives.py` plays on the artifact side. Keep it
that way — it is arithmetic with no opinion about strategies, artifacts or
capital, and it is the only place in the repository where a numerical-methods
bug could hide.

---

# Architectural Decisions

The existing Artifact Framework remains the canonical artifact boundary. No
replacement Artifact system should be created.

Artifacts are signed at creation. Unsigned artifacts do not pass validation and are
refused by the repository.

`Artifact` is a record that keeps whatever hash it is given. It does not sign
itself: `dataclasses.replace()` re-runs the constructor, so constructor-time signing
would hand every tampered copy a fresh valid signature and silently disable tamper
detection. Guarded by `test_replace_does_not_resign_an_artifact`.

Artifacts are never overwritten. Versions are append-only.

An artifact's confidence is revised by producing a new version, never by editing
one. Its evidence grade is the strongest record it carries, derived rather than
asserted — the factory computes it, the validator re-derives it, and a mismatch is
refused. Both are inside the integrity hash. ADR-005.

Versions are semantic and are ordered as such, never as filenames. A version
that cannot be ordered does not enter storage: append-only means it could never
be corrected afterwards. `latest()` is the one way to ask which version is
current, and it raises rather than guessing.

Reading an artifact back is not vouching for it. `load()` returns what is stored,
hash included, and never re-signs — so a tampered file loads successfully and then
fails the gate. The same reasoning that keeps signing out of the constructor.

**`ArtifactRepository.get()` is where the vouching happens.** `load()` is a
parser and hands back exactly what is on disk; `get()` is the repository
presenting a record, and it verifies integrity before doing so. `save()` can only
promise a file was intact when it landed — a YAML edited by hand afterwards is
invisible to every write-time check, and the read is the only place left that can
notice. The two rules are complementary rather than in tension: because `load()`
keeps the stored hash, there is something for `get()` to check. `ArtifactValidator`
still owns everything beyond integrity, and callers needing that still run it.

A review decision is an Artifact of type `REVIEW`, carrying its subject in typed
content rather than in its own identity. Written justification is mandatory for
every outcome, and the declared outcome must agree with the declared stage change.
`Remain Current Stage` is an outcome, never a self-transition — ADR-008, ADR-009.

`RETIRED` is not on the maturity ladder. Any code comparing stage order must use
`STRATEGY_LADDER`, which excludes it, and must classify retirement before taking
a position — `RETIRED` is the highest ordinal in `StrategyLifecycle`, so a bare
comparison reads every retirement as the deepest promotion in the system.

One lifecycle per governed subject — ADR-003.

Governance is asymmetric: a stage is climbed one rung at a time and can be lost in
a single move, down to a floor of `PAPER_TRADING`. Capital is a privilege, never
an entitlement — ADR-004.

A strategy's stage is the *ceiling* it has earned; its allocation is the sum it
actually holds, at or below that ceiling. Demotion lowers the ceiling and then
triggers a fresh allocation determination underneath it. The two are separate
decisions, in that order, and the six inputs in `constitution/Capital_Authority.md`
size the second — they may never gate the first. See ADR-004 rule 4.

**A statistical result states what it cannot establish.** Immutable Law IV —
"Past performance is evidence. It is never proof." — is implemented rather than
quoted: every significance artifact carries, inside its signature, the fact that
its p-value is *optimistic* because real returns are not independent, and that no
multiple-testing correction is applied because Belay does not record how many
strategies were tried. Neither string is a parameter. **Belay computes the
number and reports it against the caller's threshold; it never decides
promotion** — that remains a recorded review. ADR-012.

**A metric convention the documents do not state is never defaulted.** The
risk-free rate, the target return and the observation frequency are required
arguments, and every one of them is recorded inside the artifact's signature
beside the number it produced — a figure whose assumptions can be edited after
signing is not evidence. A metric artifact carries the four things
`Validation/Backtesting.md` requires a backtest to document, and refuses to be
built without them. ADR-011.

Dispersion is the sample estimator, `n - 1`, and downside deviation divides by
the full sample rather than by the count of periods that fell short. Both
choices are the ones that cannot flatter a strategy, and both are invisible in
the result — which is why they are ruled rather than left in a function body.

Belay is two layers joined by one contract. Mechanics emit Artifacts; governance
consumes them. See ADR-002.

---


# Highest Priority Next Task

**Updated 2026-09-20 — this is Belay's first commit.** This stands in front of
the night list below without rewriting it, per this file's convention. **The
task that list names as next — building this repository — is what produced it.**

`docs/OwnerDecisions.md` Part 14 records the rulings made that day, each put to
the owner one at a time with a recommendation. **Read 14b before making sense
of anything dated earlier**: the platform was renamed from Atlas to Belay, and
the rename was applied to the records as well as the code.

**What is owed, and by whom.** `docs/OperatorChecklist.md` carries the
owner-only items: making this repository public, and applying the ruleset on
`main` the same day. Two findings from the independent passes are open and
to be opened as Issues — ADR-013 rests on a premise that inverts once this
repository is public (Part 14h), and `scripts/review_due.py` mis-numbers
findings in a clone with no remote (Part 14g).

**Before running a review here, run `python scripts/review_due.py` and check the
finding number it prints against the register.** In the snapshot it restarted
the numbering from the beginning, over findings that already existed, because
the gate reads `refs/remotes/origin`. A fetched clone should be correct;
Part 14g has the detail. Confirm it rather than assume it.

**The work queued before publication continues from the night list below**,
starting at its item 2: the evidence-bar questions, then
`docs/proposals/sample-adequacy-definition.md`, then ADR-015.

Run `refresh-status.cmd` first. The dashboard reports current state more reliably
than this document.

**Updated 2026-09-19 (night) — this stands in front of the evening list below
without rewriting it, per this file's own convention. Belay now has a second
contributor, and the repository is the only thing the contributors share**
(`docs/OwnerDecisions.md` Part 11). Every agent, from any AI provider, starts at
`AGENTS.md`; every person starts at `CONTRIBUTING.md`. If you are reading this
after time away, synchronize first: `main` may have moved without you.

What the night session did, all in one pull request
(`hardening/co-contributor-readiness`), no framework code touched:
`AGENTS.md` gained "Any Agent, Any Provider" and "Determinism and Provider
Independence" and lost a stale hard-coded priority; `CONTRIBUTING.md`,
`.github/pull_request_template.md`, `.github/CODEOWNERS` and
`.github/ISSUE_TEMPLATE/task.md` are new; `README.md` was rewritten for an
outside reader; `LICENSE` changed from MIT to a proprietary notice (owner
selected, Part 11c); `docs/research/known-data-sources.md` records what the
owner's other project learned about data collection, as leads only.

The order now:

0. **Owner-only: merge the pull request above**, after reading the independent
   passes pasted into it.
1. **Publication, in this order.** (i) Put the remaining publication decisions
   in `docs/OperatorChecklist.md` to the owner, one at a time, each with a
   recommendation and the reasons. **Ask the new seventh one first** (publish
   this history, or a fresh repository from a cleaned snapshot): if the owner
   chooses a fresh repository, items 1, 2 and 3 of the six are answered by it.
   Item 4 is answered; 5 and 6 remain either way. **RULED the same night: a fresh repository (`docs/OwnerDecisions.md` Part 12b), and PR #15 is merged; the next publication step is to put Part 12b's four open points to the owner, one at a time, then build and independently scan the snapshot.** **ANSWERED at close of night (`docs/OwnerDecisions.md` Part 13): the new repository is named Belay, is the day-to-day source, and includes the full findings if two independent passes on the snapshot come back clean. THE NEXT SESSION'S TASK IS `docs/proposals/fresh-public-repository-brief.md`, start to finish.**
   (ii) The owner flips visibility personally. (iii) The ruleset on `main` goes
   on the same day, now including "require review from Code Owners".
   (iv) Only then does the second contributor fork and claim an Issue.
2. **Then the evening list below continues from its item 2**, starting at its
   second sub-item (the evidence-bar questions); its item 1 is done and its
   first sub-item is step 1 above.

A good first task for the second contributor's agent, because it is owed and is
worth most coming from a different model: the second independent pass on the
evidence-bar proposal on PR #10's branch, and on
`docs/proposals/sample-adequacy-definition.md`.

**Updated 2026-09-19 (evening) — this order supersedes the "Updated 2026-09-19
at session close-out" list below by standing in front of it, not by rewriting
it; that list is kept exactly as written beneath this one, per this file's own
convention.**

1. **Owner-only: merge PR #12, then this pull request.** PR #12
   (`fix/review-skill-numbering`) fixes the review skill's numbering
   instruction; merge it to `main` first. This pull request is stacked on top
   of it — once #12 merges, retarget this pull request's base to `main` and
   merge it. PR #10 (ADR-015) stays a draft throughout.
2. **Then the next session opens by asking the owner, one question at a time,
   each with a recommendation and the reasons — the format the owner asked
   for.** In this order:
   1. The six publication items in `docs/OperatorChecklist.md` (item D),
      before the repository goes public.
   2. The seven questions in the evidence-bar proposal, on **PR #10's
      branch** — named without backticks because
      evidence-bar-per-rung.md is not a resolvable path on this branch.
   3. The seven questions in `docs/proposals/sample-adequacy-definition.md`
      (section 10, this branch).
   4. Whether an explicit owner instruction may override the review gate's
      SKIP verdict — `docs/OperatorChecklist.md`'s "Owner glance items",
      item (d).
3. **Fill ADR-015's per-rung table from the evidence-bar ruling**, run a fresh
   independent pass over the whole ADR, and the owner ratifies it.
4. **Only then, brief Phases 5 to 8** — tests red, implement, independent
   verification *before* landing, then land — **for F-007 and F-014
   together.** `docs/proposals/F-007-session-brief.md` starts F-007 from
   executed evidence.
5. **Then the Part 9a order continues** (`docs/OwnerDecisions.md:1076`):
   F-019; then F-003, F-008 and F-016 together; then **F-004 (shape ruled,
   numbers pending — `docs/OwnerDecisions.md:1411`, Part 10e) and F-006
   (narrow fix authorised; the calendar proposal is still owed —
   `docs/OwnerDecisions.md:1487`, Part 10g)**; then F-024 and F-027 — **F-027
   must land in the same change as F-004's numbers, not after**, per
   `docs/proposals/sample-adequacy-definition.md` section 9.

`docs/proposals/register-rebuild-session-brief.md`,
`docs/proposals/F-007-session-brief.md` and
`docs/proposals/sample-adequacy-definition.md` are the briefs to read before
touching code on any of the above.

---

**Kept below exactly as written 2026-09-19 at session close-out, and
superseded by the list above rather than rewritten, per this file's own
convention.**

1. **Owner-only: land the register.** Mark PR #9 ready and merge it; retarget
   PR #11's base to `main` and mark it ready and merge it. Owner action
   only — see `docs/OperatorChecklist.md`. PR #10 (ADR-015) stays a draft
   throughout this step.
2. **Independent verification pass on the evidence-bar proposal, then the
   owner rules the bar.** The proposal exists only on PR #10's branch, as
   evidence-bar-per-rung.md under docs/proposals/ there — not a resolvable
   path on this branch, so named without backticks rather than cited — and
   has had no independent pass.
3. **Fill ADR-015's per-rung table from that ruling**, run a fresh
   independent pass over the whole ADR, and the owner ratifies it.
4. **Only then, brief Phases 5 to 8** — tests red, implement, independent
   verification *before* landing, then land — **for F-007 and F-014
   together.** `docs/proposals/F-007-session-brief.md` starts F-007 from
   executed evidence.
5. **Then the Part 9a order continues** (`docs/OwnerDecisions.md:1076`):
   F-019; then F-003, F-008 and F-016 together; then F-004 and F-006 —
   **still UNRULED — ask the owner, do not assume a fix shape**; then F-024
   and F-027. [**Corrected in place 2026-09-19 (evening)** — F-004 and F-006
   are no longer flatly unruled; see the list above. Original wording left
   standing under Law VII.]

`docs/proposals/register-rebuild-session-brief.md` and
`docs/proposals/F-007-session-brief.md` remain the two briefs to read before
touching code on any of the above.

---

**Kept below as the record of how the order above was reached, and
superseded by it rather than rewritten.**

**Start here: `docs/proposals/register-rebuild-session-brief.md`, Phase 3
onward.** Phase 2 of that brief is what this commit did — F-014 to F-018 are now
rows and sections in Open Findings above, and `scripts/status.py` counts 33. The
brief carries the phases that follow, in order, and a session continuing this
work needs no prompt beyond its name. Phases 3 to 8 are about F-007 and are not
started. [**Count corrected 2026-09-19: `scripts/status.py` counts 43.** The
paragraph is kept as written because it describes what the commit that wrote it
did; the figure moved when the ten open findings of the 2026-09-04 and 2026-09-11
reviews were registered on the commit after it. Phases 3 to 8 are still not
started.]

**The order the Stage 3 (Backtester) blockers are to be worked in —
owner-approved 2026-09-19, recorded at `docs/OwnerDecisions.md:1076`
(Part 9a).** This supersedes the ordering in the 2026-07-31 list below, which is
kept as a record. **Part 9a approves the order and nothing else**: no fix shape
is ruled by it, and step 4 below is explicitly blocked.

1. **F-007 and F-014 together.** Both are Critical and both sit on the same
   promotion-and-capital gate: F-007 is a STRATEGY artifact born at a capital
   stage without climbing there, F-014 is a promotion recorded with no evidence
   at all. Neither closes the other. `docs/proposals/F-007-session-brief.md`
   starts F-007 from executed evidence.
2. **F-019 — eight guards on the capital and provenance path are asserted by
   nothing.** A one-token change to each passed the suite when it was found.
3. **F-003, F-008 and F-016 — the survivorship surface**, taken as one piece of
   work rather than three. F-003 is a statistical review that cannot carry the
   disclosure, F-008 is three ways a caller defeats the guard, F-016 is the one
   branch deciding whether the caveat prints at all being untested.
4. **F-004 and F-006 — both still UNRULED. An owner ruling is required before
   any work starts on either.** They are in Open Findings above as rows 15 and
   16, and `docs/OwnerDecisions.md:988` is where Part 8 left them unruled;
   Part 9a did not change that. Do not open code for these until they are ruled.
5. **F-024 and F-027.**

**Corrected in place on 2026-09-19: they are rows now, and the paragraph this
replaces said they were not.** It read: "Said plainly, because it would otherwise
mislead: F-019 and every number above it are not rows in this register as of this
commit ... Registering them is deliberately not part of this commit; it lands in
a following pull request so the two changes can be verified separately." **That
following pull request is the commit you are reading.** All twelve findings of
`reports/review/2026-09-04-review.md` and `reports/review/2026-09-11-review.md`
are registered in `# Open Findings` above — **ten of them as open rows, and two
verified fixed and written straight into `# Closed Findings`.**
`scripts/status.py` counts **43**, from 33. It is corrected rather than kept
because the original said the exact opposite of what is now true, and a reader
acting on it would skip the ten.

**The two closed ones are not named by number in this section**, and that is a
mechanical constraint rather than coyness: `tests/test_session_handoff.py:58-82`
goes red when a number in `# Closed Findings` is also named here, which is the
staleness check that stops this list pointing at finished work. Their entries are
in `# Closed Findings` with the closing evidence.

**All twelve were approved for registration** — `docs/OwnerDecisions.md:1120`
(Part 9b), owner-selected 2026-09-19 — **and that approves registration only. No
fix for any of F-019 to F-030 is authorised by it.** The ordering above sequences
some of them; sequencing is not authorisation. Part 9b is the record that a row
in the register is a statement that the repository has read a finding, and
nothing more.

**The 2026-07-31 list below is finished and is kept only as a record.** What was
next, in order, as that list had it:

1. **Finding 18 — amend ADR-014 rule 5, or rule it correct as written. Owner's
   call.** Rules 5 and 8 of a ratified ADR contradict each other; the code obeys
   a reading neither rule states. Small, blocks nothing, and leaves a ratified
   document self-contradictory until it is settled.
2. **F-003 — a statistical review cannot carry the survivorship disclosure.**
   `significance_artifact` takes a source *name* and builds its `Disclosure`
   inline, so a Validation Report computed on survivor-only data carries no
   survivorship caveat. The 2026-08-01 review's own verdict is that this
   **becomes load-bearing the moment Stage 3 produces a number a promotion review
   reads** — so it wants closing before Stage 3, not after.
3. **ROADMAP Stage 3 — the Backtester.** Stage 2 is complete and the data path is
   real: the boundary, the store, the record, and now a signed record on disk for
   the one series Belay holds. Nothing in the open findings blocks starting it.

**And one standing rule, earned the hard way on 2026-08-02:** when an ADR says a
verification pass runs *before* implementation, it runs before implementation.
This document said "after step 6", the ADR said "before", the implementer
followed this document, and the pass then found eight defects in code that had
already been committed — after a one-way door had closed. **Where two documents
disagree about when a check happens, the stricter one governs.**

---

# ★★ READ FIRST — F-003 is written, green, and deliberately NOT committed

**Session of 2026-08-02, interrupted. The working tree holds seven modified files
and they are the F-003 fix. Do not commit them yet.** Suite 633 (from 626, +7
tests), `python scripts/verify_clone.py` passes end to end against the live
clone. The reason it is uncommitted is the rule this repository learned the hard
way: the independent verification pass runs **before** the change lands, and that
pass is only one sixth finished.

**What is done:**

- **F-003 implemented.** `significance_artifact` now takes `source:
  MarketDataSource` instead of `data_source: str`, derives `data_source` from
  `source.name`, and **appends** the survivorship caveat to ADR-012 rule 7's
  fixed `KNOWN_LIMITATIONS` rather than replacing it. Tests were written first
  and run red against unchanged code.
- **The guard moved.** `fetch_record._survivorship_of` is now
  `contract.survivorship_of`, public, so the metrics layer can reach it without
  importing the artifact repository and the series store. Behaviour unchanged;
  callers, the `dolt_clone.py` docstring and `test_dolt_clone.py` repointed.
- **Finding 18's amendment drafted**, at
  `docs/proposals/ADR-014-rule-5-amendment-DRAFT.md`. **Not ratified — the
  owner's call.** No code changes with it; the code already obeys the amended
  reading. The draft also records that rule 5's own citation into
  `framework/data/store.py` was exact at ratification (`48511a8`) and was broken
  by the commit that implemented the ADR (`a19c24e`).

**What is NOT done, and gates the commit:**

**The independent pass is one lens of six.** See
`reports/review/2026-08-02-f003-partial-pass.md`. The adversarial lens finished
and returned **six defect-grade findings with executed evidence**; the other five
lenses and the entire three-skeptic refutation stage were killed when the session
ended, so **nothing in it has been refuted or confirmed**. Three of the six
predate F-003 — a `SurvivorshipDisclosure` subclass can override
`known_limitations()` to `"None."`, `survivorship_of` accepts a duck-typed
non-source, and `_survivorship` is rebindable past the read-only property — but
F-003's new docstrings assert guarantees those holes break, which makes them this
change's problem to answer.

**Resume the pass, do not re-launch it from scratch:** run ID
`wf_<id>`, script under `.claude/projects/.../workflows/scripts/`.
Completed agents return cached results.

**One correction to the section below, and it is a document bug rather than a
wrong fact.** The `dolt` path recorded there contained a literal backspace
character, so `Dolt\bin\` rendered as `Doltin\` and read as a directory that does
not exist. The path was always right; the escaping was not. Repaired. It is
`C:\Program Files\Dolt\bin\dolt.exe`, and it is still not on this shell's PATH —
prefix it before running `scripts/verify_clone.py` or the script fails with
"the `dolt` command was not found".

---

# ★ START HERE — ADR-014 is implemented, and the pass that checked it ran late

**F-002 is closed. `artifacts/RPT-0001/1.0.0.yaml` is the first artifact of any
type this repository has ever committed**, and it is a signed fetch record for
`data/market/dolthub-stocks/AAPL/0001-a7dbcaf3fb6aba2d.bin`. `git ls-files` no
longer returns nothing. Suite 626.

**Read ADR-014's Status block before anything else, and read it as a warning
about process rather than about the ruling.** The independent verification pass
that ADR requires *before* implementation ran *after* it, because the START HERE
section this replaces put it after step 6 while the ADR put it before. Two
documents, one mandatory step, opposite orderings, and the implementer followed
the weaker one. **The pass then found 19 defect-grade errors across 93 claims and
the author's own review of the same work found none of them** — eight in code
already committed, after rule 6's one-way door had closed.

**If you take one operating lesson from this session, take that one.** It is the
fourth consecutive session with the same shape and the first where the ordering
of the check was itself the defect.

### What is now true, and where the seams are

- `artifacts/` is the artifact root, tracked, defaulted in
  `framework/artifacts/repository.py`. Nothing else may be assumed about where
  artifacts live — the constant is the answer.
- `fetch_and_record` takes a repository and saves. **A caller that passes the
  default root writes a permanent institutional record**; that is rule 3 and
  nothing but the choice of root enforces it. `scripts/verify_clone.py` checks
  its own root on every run and that check was broken when written.
- **One record per stored version, not per fetch** — the test is whether a record
  already covers *these bytes*, not whether the store wrote a file. Finding 18
  records why the ADR's own wording cannot be followed literally.
- `orphan_versions(store, repository)` answers "which stored bytes have no
  record". It is the only thing holding `.gitignore`'s claim true, and finding 19
  records that it is vacuous on any machine that has not fetched.

### Before touching any of it

**Run `python scripts/verify_clone.py`.** The suite touches no network and no
subprocess, so 626 green tests say nothing about whether the data path works.
Both real problems on 2026-08-01 were found by one live fetch after the suite was
already green.

**The HTTP transport is intermittent and that is not a bug to fix.**
`scripts/adopt_aapl.py` failed on its first run with three `context deadline
exceeded`s and succeeded on the second, which is finding 14's recorded behaviour
unchanged. If a fetch fails, run it again before diagnosing it.

**`dolt` is installed at `C:\Program Files\Dolt\bin\dolt.exe` and is not on
this shell's PATH.** The clone at `data/upstream/` is 730 MB and present.

### The three things that are still one-way

1. **Signed content.** Rule 6's fields are inside the integrity hash and a record
   now exists, so changing the shape of `content` is a migration of append-only
   records rather than an edit. That window closed on 2026-08-02.
2. **Identifiers.** `RPT-0001` is issued and permanent. `framework/identifiers.py`
   now accepts four digits or more, ASCII only, `\Z`-anchored.
3. **Anything written under `artifacts/`.** Tracked, append-only, and git history
   cannot be pruned.

## Still current — Stage 2, the clone transport, and the verification record

**ROADMAP Stage 2 is complete, ADR-013 is implemented in all ten rules, and
finding 14 is closed.** The boundary exists, a fetch record is signed with a
content hash, the store is versioned and out of git, a metric's disclosure is
derived from the fetch rather than typed — and bulk data now gets through.
Suite 584.

**Belay can complete a multi-year backfill for the first time.** Three years of
AAPL — 754 daily bars — returns in **4.4 seconds** from
`framework/data/dolt_clone.py`, against roughly 25 minutes and frequent failures
over the hosted API. Thirteen years drops from an estimated 6.6 hours per symbol
to about 20 seconds.

**What it cost:** the `dolt` CLI (2.2.3, via `winget install DoltHub.Dolt`) and a
730 MB shallow clone at `data/upstream/`, gitignored. Recreate it with:

```bash
dolt clone --depth 1 post-no-preference/stocks data/upstream
```

### Read this before touching the clone transport

**The suite proves nothing about whether the data works.** 584 tests pass and not
one touches the network or spawns a subprocess, both deliberately. Run
`python scripts/verify_clone.py` — it does a real fetch end to end, and
`--cross-check` additionally queries the hosted API and compares values.

**Three rulings are frozen into `framework/data/dolt_clone.py` and the reasoning
is in its module docstring rather than here.** In brief: the clone-backed source
has **its own store key**, so the two transports' version chains never
interleave; **byte-identity with the HTTP envelope is deliberately not
attempted**, because forging it fails silently when approximately met; and the
clone's **commit hash is excluded from the payload**, because `dolt pull` would
otherwise re-hash every series whose rows had not moved.

**The fourth ruling is the one to be careful about.** The hashed bytes on this
path are partly Belay's own serialisation, so editing `_translate` is a
**migration, not a refactor** — every stored clone series re-hashes and registers
as a vendor restatement that did not happen.
`test_the_translated_envelope_is_pinned_byte_for_byte` turns the suite red to say
so. If you need to change it, bump `_ENVELOPE_VERSION` deliberately.

### What the independent pass found, because the number has not improved

**65 claims checked, 17 wrong or questionable, 6 defect-grade. The author's own
pass found none of the six.** Third consecutive session with that shape, on code
whose tests were written first and were all green.

**The worst one removed a guarantee while its docstring claimed to preserve it.**
`DoltCloneStocksSource` defined `survivorship` as a class-level property "to make
the inheritance explicit". It was inert — the parent already returned that object
— and it defeated the second of the two links defending ADR-013 rules 5 and 9.
`_survivorship_of` catches a subclass that skips `super().__init__()` by asking
whether the validated constructor ran; a class-level property answers `getattr`
whether it ran or not. Demonstrated: the guard **held** on the HTTP branch and was
**defeated** on the clone branch. Deleted, with
`test_a_subclass_that_skips_the_constructor_is_still_refused` now pinning it.

The other five, each now fixed and tested: a clone failure escaped the wrapper
that names *which chunk* failed, on the transport that makes 156-chunk backfills
routine; `_translate` was an unnamed third phantom-restatement door; the test
fixture claimed to be dolt's output while carrying the *other* transport's values
and the wrong JSON type for volume; `_DoltSql` had **no test coverage at all**, so
deleting its exit-code check left the suite green — and that check is what stops a
truncated multi-statement result being stamped `Success`; and the determinism test
was a tautology that promised row-order protection `sort_keys` does not provide.

### The next task — specified, ruled, and not started

**Finding 15, and the owner has already ruled on it**, so this is a build rather
than a decision. `fetch_and_record()` writes the bytes and *then* fails on an
empty series, leaving an orphaned file in an append-only store for every delisted
symbol — which on a `SURVIVORS_ONLY` source is the expected case, not an edge one.

**The ruling: validate before writing.** Fetch → check the answer is usable →
only then write. The owner's exact words, the three readings of "fill" that were
put to them, and why the dangerous one is barred by two existing ADRs, are all in
the finding-15 section above, along with a four-step build order. **Read that
section before starting; it is specified down to which existing test to copy.**

Two traps recorded there and worth repeating here:

- **`scripts/verify_clone.py` currently asserts the broken behaviour** under a
  `KNOWN` label. It must be *inverted* when the fix lands, not deleted — if it
  still passes, the fix did not work.
- **The check belongs in two places.** `fetch_record()` can be called directly and
  is the one that signs the artifact. The guard that covered only the ordinary
  path is exactly the one an independent pass broke this session.

That is the thing standing between Belay and a backfill over a symbol list.

### A small oddity, observed and not diagnosed

**One `scripts/status.py` run reported `583 passing, 1 failing` while `pytest -q`
reported `584 passing, 0 failing` moments earlier and moments later.** Three
subsequent `status.py` runs all reported 584/0, and three `pytest` runs all
reported 584. The one disagreeing run happened while
`reports/generated/status.html` was stale from an earlier genuinely-failing run.

**Recorded rather than explained, because it was not chased.** The suspicion is a
self-referential dependency — a test whose result depends on a generated file
that the suite does not itself regenerate — which would make suite success
sensitive to the order the two commands are run in. That is a guess and is
labelled as one. If a future session sees the two disagree again, this is the
second sighting rather than the first.

### One loose end, stated plainly

**A second independent verification pass was running when this session ended and
its results were never read.** It was checking the six fixes listed below plus
every numeric claim in these documents. Nothing in this session's work depends on
it, and the suite is green with a live fetch verified — but **the fixes in this
session have been verified once, not twice**, and the first pass found six
defect-grade errors in work its author had already declared finished. Treat the
`dolt_clone.py` docstrings as the least-verified prose in the repository until
someone re-runs that check.

### Vendor candidates, and the reason a longer list is not obviously better

**`massive.com`** — raised by the owner 2026-08-01 and recorded before it is
lost. A market data provider offering APIs over stocks, options, indices,
currencies and futures, co-located in exchange datacenters. **Nothing about it is
established.** The two questions that decide it are the two asked of every source
this session, and neither is answerable from a homepage: **does it retain
delisted instruments, and what does it cost?** Rule 9 refuses a source that
cannot state the first.

**"More sources is better" does not hold here, and the reason is the one that
settled IBKR.** *N* survivor-only sources are still survivor-only. Source count
is not the bottleneck; the delisted-prices property is, and a third source
lacking it adds nothing but three ways to get the same flattered answer.

Three costs specific to this repository:

- **Rule 9 charges rent per source.** Survivorship must be *established*, not
  assumed — real queries against the live database, as `dolthub.py`'s `basis`
  records. A source nobody has interrogated is worse than no source, because it
  sits in the codebase as a temptation.
- **Two sources that disagree is a ruling nobody has made.** If two vendors
  return different closes for the same day, which does Belay believe? Under
  ADR-011's central holding — no convention Belay was not told is ever defaulted
  — choosing silently *is* the ruling. **That needs an ADR before a second source
  feeds anything**, and ADR-013 did not make it.
- **Rule 3 weakens if provenance blurs.** Re-fetch, hash, compare works per
  source. A series assembled from whichever vendor answered first has no single
  provenance and no comparable hash.

**Where a second source genuinely earns its place is cross-validation.** Two
sources checking each other is evidence about the data; two sources feeding a
backtest interchangeably is a series nobody can reproduce. The first is worth
building and is not what "more sources" usually means.

### What NOT to do

- **Do not widen `MarketDataSource` to make the clone fit.** If the contract has
  to change to accommodate a second transport for the *same vendor*, the contract
  was wrong — and `framework/data/ibkr.py` exists precisely so that claim is
  testable against a genuinely different vendor.
- **Do not build a universe.** Still a Stage 3 concern, and the source cannot
  support one honestly — see the selection distinction above.
- **Do not write a sixth backtest metric.**
  `test_only_the_backtest_metrics_adr_011_scopes_in_are_built` turns the suite
  red if one appears, which is the prompt to write the ADR first.
- **Do not buy data yet.** The trigger is precise and Belay has not reached it:
  the first time it *selects* instruments rather than being handed them.
- **Do not run `framework/data/ibkr.py` against a live account.** It is
  fixture-tested only and says so in its own survivorship basis.

### Two things that are true and easy to misread

**The suite being green does not mean the data works.** 584 tests pass and not
one of them touches the network or spawns a subprocess, deliberately. The
transport ceiling was found by running a real fetch by hand, and nothing in the
suite would have caught it. **This held a second time on 2026-08-01:** the clone
transport's suite was green while its fixture carried the wrong JSON type for
`volume` and `_DoltSql` had no coverage at all. `python scripts/verify_clone.py`
is the real fetch for the clone path; run it before believing any transport
change.

**`framework/data/ibkr.py` is unverified against the live API.** Its unit tests
prove the contract accommodates it, not that the wire format is right. The
UTC-date conversion in `_bar` is the most likely thing to be wrong, and the
failure mode is a whole series shifted by one day.

### If the window has room afterwards

- **Finding 15**, the orphaned-bytes ruling, is the task above.
- **Finding 12** — the evidence classes have no class for observed fact. ADR-013
  rule 8 routes around it soundly and the routing holds only while nothing needs
  to weigh an observation against a simulation.
- **Finding 4** — the `ArtifactType` / identifier-prefix disagreement. Needs a
  ruling either way. Stage 2 did not widen it: the fetch record is a `REPORT` and
  takes the `RPT` prefix.
- **The Critic.** `Validation/Workflow.md` puts it *before* backtesting — its job
  is to falsify a hypothesis before resources are spent.

Do **not** start the promotion/demotion/retirement classifier ADR-004 mentions.
Still deferred deliberately, and **ADR-009 did not write it.** ADR-008 settled
self-transitions and ADR-009 rule 5 checks a *declared* outcome against a
*declared* stage pair — neither is the classifier, which has to derive a name
from a transition and cope with `Draft → Review → Approved`. That is not a
promotion, a demotion or a retirement, and `ArtifactLifecycle` still has no
vocabulary for what it is.

### Why Stage 2 mattered

Every artifact the metrics layer emitted carried, inside its own signature, a
`known_limitations` string saying the series was supplied by hand and described
no real instrument. **That sentence was true of every number Belay had ever
computed.** It is now false: `disclosure_from()` builds `data_source` and
`sample_period` from the fetch, and the survivorship caveat is a fixed constant
the caller cannot replace.

What it did **not** unlock is the dashboard. `Regime robustness`, `Execution
quality`, `Liquidity` and `Operational consistency` still need regime
classification, order and fill records, and a run history. Stage 2 was a
prerequisite for the first of those, not a completion of any.

---

### Where Stage 1 actually stands

`Validation/Backtesting.md` names **nine minimum metrics**. Four exist:

| Metric | State |
|---|---|
| CAGR | **built** — `framework/metrics/returns.py` |
| Sharpe | **built** — `framework/metrics/risk_adjusted.py` |
| Sortino | **built** — `framework/metrics/risk_adjusted.py` |
| Drawdown | **built** — `framework/metrics/drawdown.py` |
| Win Rate | needs a ruling: a *period* or a *trade*? |
| Exposure | needs trade or position records, which no return series carries |
| Trade Count | needs trade records; a return series contains no trades |
| Benchmark Comparison | needs a second return series |
| Tail Events | needs a threshold no document states |

**The bottom five are not an afternoon's work each.** Every one of them is
missing an input or a definition, and building one means inventing what is
missing. `test_only_the_backtest_metrics_adr_011_scopes_in_are_built` turns the
suite red if a sixth appears, which is the point of it — the red is the prompt
to write the ADR first.

**Two corrections, applied here rather than left in place.** This document
previously said `EvidenceRecord` already had fields for the four required
disclosures — it did not, and `Disclosure` in `framework/metrics/reporting.py`
now carries them. And it listed Win Rate, Exposure and Trade Count as computable
from a return series alone, which is false for the reasons the table gives.
`docs/ROADMAP.md:104-109` was right on both counts and this document was wrong;
see `Two claims in this document were wrong` above.

### The pattern to follow

**`framework/metrics/reporting.py` is now the pattern, not `drawdown.py`.**
Every metric goes through `metric_artifact`, which signs the number and refuses
to emit one without its four disclosures. `drawdown.py` was migrated onto it, so
all four metrics share one path and there is no second shape to copy by mistake.

Read `Disclosure` before writing a fifth metric. The disclosure block is not
metadata — `Validation/Backtesting.md:47` says "Outputs become evidence", and a
number that does not say what was assumed to produce it is not evidence of
anything.

`Backtest Reports` maps to `ArtifactType.REPORT`, which holds the `RPT` prefix,
so the trap in finding 4 does not bite on this path. Checked by running it.

**`metric_artifact` takes a `deliverable` and defaults it to `Backtest
Reports`.** ADR-012 rule 12 needed `Validation Reports` for a statistical review,
because `Validation/Workflow.md:15` makes Statistical Review a step distinct from
Backtesting. The artifact *type* is derived from the deliverable rather than
passed separately, so the pair cannot contradict itself and `ArtifactValidator`'s
ADR-010 rule 9 refusal can only ever fire on a caller's error.

**Anything under `framework/metrics/` that draws a conclusion rather than
describing a series is governed by ADR-012, not ADR-011.** Read rule 7 before
adding one: the assumptions and known-limitations strings are fixed module
constants with no parameter to override them, and that is the mechanism, not an
inconvenience to route around.

### What would move the dashboard next

`scripts/status.py` reports **3 of 7 promotion criteria computable**. The four
remaining are `Regime robustness`, `Execution quality`, `Liquidity` and
`Operational consistency` — and **all four need inputs that do not exist**,
which is a different situation from the two that were closed today.

- `Regime robustness` needs regime classification (`Research/RegimeDetection.md`,
  unbuilt) *and* returns segmented by regime, which needs dated data — Stage 2.
- `Execution quality` and `Liquidity` need order and fill records. Nothing in
  Belay has ever placed an order.
- `Operational consistency` needs a run history to be consistent *across*.

**So the next dashboard movement is gated on Stage 2, the market data boundary,
not on another metrics ADR.** That is the honest reading and it is a change from
this morning, when the answer was "write the metric".

`framework/metrics/statistics.py` now exists and holds what its name says.
The warning it used to carry still applies to the four above:
`implementation_state()` cannot see inside a file, so twenty lines of anything at
an expected path turns a criterion green. Four of those paths are still empty.

### Smaller things, if the window has room afterwards

- **The Critic.** `Validation/Workflow.md` puts it *before* backtesting: its job
  is to falsify a hypothesis before resources are spent.
- **The market data boundary**, so a price series carries provenance rather than
  being supplied by hand. **This now has a concrete landing point rather than
  being an abstraction:** every metric artifact carries a `data_source` and a
  `known_limitations` string, and today every one of them says the series was
  supplied by hand and describes no real instrument. Stage 2 is what makes those
  two fields say something else.
- **Finding 4** - the `ArtifactType` / identifier-prefix disagreement. Needs a
  ruling either way, and the finding sets out both directions.

Do **not** start the promotion/demotion/retirement classifier ADR-004 mentions.
It is still deferred deliberately, and **ADR-009 did not write it.** ADR-008
settled self-transitions and ADR-009 rule 5 checks a *declared* outcome against a
*declared* stage pair — neither of those is the classifier, which has to derive a
name from a transition and cope with `Draft → Review → Approved`. That is not a
promotion, a demotion or a retirement, and `ArtifactLifecycle` still has no
vocabulary for what it is. Settle that first, or the helper is guessed rather
than specified.

---

# Working Agreement

The repository owner is not a developer; Belay is their first coding project, and
they are learning alongside the work.

Explain what a component is and why Belay needs it before writing it, in plain
language, without dropping the specifics or the real numbers. Unpack jargon on first
use.

Confirm scope before large reads or long runs. Show the proposed work before doing
it. Stop and report when something fails rather than adjusting it unasked — a test
rewritten to pass is worth less than a failure that gets read.

Do not accept a claim about what a governing document says without opening it. Two
errors this session came from exactly that.

**Independent verification is not optional polish and it does not go last.** Four
sessions running, a fresh-context pass has found defect-grade errors that the
author's own review of the same work found none of — 4, 6, 6, then 19. It is not
a matter of reading more carefully: the defects live in the prose asserting the
code is right, and re-reading re-derives the reasoning that produced them. Budget
for the pass up front, and run it **before** anything irreversible lands — a
signed artifact, a permanent identifier, a committed history.

---

# Pre-Public Hardening (2026-09-20, late) — appended here so no line citation moves

Written by the session that ran the last scan before the owner made Belay
public. It is at the end of the file, against this file's usual order, because
every line above is cited by number somewhere and an insertion would move them.

**What the scan asked.** Not "are the rules right" but "what enforces each rule
if nobody reads it". For these the answer was "nothing":

- The files that *are* the guards (`.gitignore`, the agent instruction files,
  `pyproject.toml`) were not owner-only in `.github/CODEOWNERS`.
- The ruleset planned for `main` could not have worked. It required review from
  a code owner, the owner is the only code owner of the governance paths, GitHub
  does not let an author approve their own pull request, and every session so
  far has pushed as the owner. `.github/rulesets/` now holds two rulesets
  instead: one nobody can bypass (pull request, the five checks, no force-push,
  no deletion) and one for review that an organization owner can bypass through
  a pull request.
- Nothing told an agent that an Issue opened by a stranger is not a task.

**What `main: review` would not have done, before Part 15b.** Its bypass is
"any organization owner, through a pull request", and `docs/OperatorChecklist.md`
used to tell the owner to invite the second contributor as an organization
Owner. Had that been done, both people who can merge could have bypassed it, and
**the code-owner requirement would have bound nobody**. It binds the second
contributor because Part 15b makes them a Member with write access. GitHub counts a code owner only if they have write access,
and on 2026-09-20 `gh api repos/belay-systems/Belay/collaborators` listed the
owner alone. `main: checks` is unaffected either way: it has no bypass.

**What was put to the owner, and ruled the same session** — `docs/OwnerDecisions.md`
Part 15 has the owner's words: the second contributor is a Member with write
access, not an organization Owner, so `main: review` does bind them (15b);
passages naming a brokerage and a private project are redacted, and the
repository was rebuilt rather than force-pushed so that the redaction is real
(15a); Belay gets its own folder on the owner's machine (15c); the machine's
default commit address is a GitHub no-reply address (15d).

**Still owed by the owner:** the ADR-013 amendment (Issue #1).

**Not verified, and said so:** `scripts/public_settings.py --apply` has never
run, because GitHub refuses rulesets on a private repository in a free
organization. Two things the design rests on are inferred from GitHub's
documentation rather than stated in it: that a bypass applies only to the
ruleset granting it, and that an author cannot approve their own pull request.

**The by-hand fallback, if the script fails.** Settings, Rules, Rulesets, New
branch ruleset, target the default branch: require a pull request; require the
status checks `governance conformance`, `suite (py3.11)`, `suite (py3.12)`,
`suite (py3.13)`, `dashboard builds`; block force pushes; restrict deletions; no
bypass list. Then Settings, Code security: secret scanning, push protection and
private vulnerability reporting on. Then Settings, Actions, General: allow only
actions created by GitHub; require approval for first-time contributors;
workflow permissions read-only.

---

# Belay Is Public (2026-09-20) — appended here so that no line citation moves

Written by the session the owner told immediately after flipping visibility. It
is at the end of the file for the reason the section above gives: every line
above it is cited by number somewhere, and an insertion would move them.

**The section above is now partly superseded.** Its "Not verified, and said so"
paragraph at `:5465-5469` says `scripts/public_settings.py --apply` has never
run. It has. Of the two inferences it names, one is now proven and one is not.
Both corrections are below. That paragraph is left as written — Law VII.

## What was done

The owner merged pull requests #8 and #10 and made `belay-systems/Belay` public.
This session ran the flip-day steps in `docs/OperatorChecklist.md`.

**The first check was the irreversible one.** A personal address on a commit
cannot be withdrawn once a repository is public:

```
$ git log --all --format='%ae%n%ce' | sort -u
294590525+pewpewpressco-ux@users.noreply.github.com
noreply@github.com
```

Two addresses, both intended. Nothing personal is exposed.

**`scripts/public_settings.py --apply` ran for the first time.** Read-only
baseline immediately after the flip: 5 of 11. After applying: 11 of 11. What it
set, and what it does not cover, is recorded in the last section of
`docs/OperatorChecklist.md` rather than repeated here.

**The scheduled review routine moved to Belay** by partial update in place —
`job_config` and `name` only, `mcp_connections` not passed, never retired and
replaced. Same trigger id, `next_run_at` unchanged at 2026-09-25. The cadence
gate answers `SKIP — last review was 10 days ago`, so that firing will be DUE.

**Atlas's `README.md` now says development has moved.** The archive stays
private; marking it archived is still the owner's.

## What was tested, rather than asserted

`scripts/public_settings.py` compares its own tracked files to the API, which is
the script certifying itself. Four things were checked independently:

- Pull request #7 reports `mergeStateStatus: BLOCKED`, which is the test
  `docs/OperatorChecklist.md` asks for by name.
- CI was re-run on `main` **after** the Actions restriction was applied, since
  allowing only GitHub-owned actions could have broken it. Five jobs green, and
  their names match the five required check names exactly — a mismatch there
  would have wedged `main` permanently.
- `current_user_can_bypass` is `never` on `main: checks` and
  `pull_requests_only` on `main: review`, for one organization admin at one
  moment. **This settles the first of the two inferences above:** a bypass
  applies only to the ruleset granting it. The second — that an author cannot
  approve their own pull request — remains untested.
- The suite passes locally: 659 passed, 1 skipped, 5 xfailed.

## The independent pass, and what survived it

Five lenses — the settings, what is now world-readable, documents the flip made
false, the routine, and what a stranger can now do — then two refutation angles
on every finding. 81 agents. **38 raw findings, 11 survived both angles, 27 were
refuted or narrowed.** The session's own review of the same work had found one
thing. The Working Agreement records four earlier sessions with that shape at
`docs/HANDOFF.md:5417-5418` (4, 6, 6, then 19), and the pre-public pass of
2026-09-20 was another. This is the next. No running total is given here,
because the earlier counts were graded by different passes against different
definitions of "defect-grade" and adding them would invent a series.

It corrected this session as well as the repository: the claim that both bypass
inferences were unproven was written into `docs/OperatorChecklist.md` by this
session and is wrong, per the third bullet above.

### Open findings, for whoever picks them up

None is an emergency, and none was fixed here.

1. **`.github/CODEOWNERS:11` is invalid on the live repository.** `gh api
   repos/belay-systems/Belay/codeowners/errors` returns "Unknown owner" for
   `@eternalaether5`, who has no write access because the organization
   invitation is still pending. Three of the five lenses found this
   independently. It clears itself when the Write grant is made.
2. **ADR-013's privacy premise has a third occurrence that was never
   annotated.** `docs/DECISIONS.md:2978` carries the same sentence that
   `framework/data/dolthub.py:16-17` carries *with* an annotation. Part 14h
   named only two sites. **Issue #1's scope should widen to this line.** The ADR
   itself is the owner's and must not be amended by a session.
3. **Five Open blocks in `docs/OperatorChecklist.md` went false**, listed with
   line numbers in that file's last section. They were listed rather than
   rewritten, because the blocks sit at lines that two frozen reports cite —
   the same tension Issue #9 raises.
4. **The SKIP branch of `scripts/review_due.py` has no test**, and it is the
   branch running in production right now.
5. **Nothing re-checks the GitHub settings after today.** No CI step or schedule
   runs `scripts/public_settings.py`, and `_COMPARED` compares four of the
   twelve parameters GitHub returns.
6. **The untrusted-outside-text rule exists in exactly one place**,
   `AGENTS.md:345`, and the review skill never routes a reader to it. A
   Claude-run review reaches it through `CLAUDE.md`; an agent from another
   provider would not. On a public repository the fortnightly unattended review
   now reads Issues that strangers can open. `AGENTS.md:347`'s remedy, "report
   it to the person directing you", also names no addressee for an unattended
   run.

## Highest priority next task

**Nothing in the build advances until the owner acts on two things**, neither of
which a session may do: getting the organization invitation accepted, which
unblocks the Write grant and clears finding 1; and the ADR-013 amendment,
Issue #1, now widened by finding 2.

After that, the open Issues are the queue, and `python scripts/status.py`
outranks this prose.

## Session close, 2026-09-20

State at close, verified rather than assumed:

- **`main` is `0133748`, green.** Pull requests #11 and #12 both merged by the
  owner. The settings read back 11 of 11; the suite is 659 passed, 1 skipped,
  5 xfailed; the cadence gate answers `SKIP — last review was 10 days ago`,
  next due 2026-09-23, and the routine next fires 2026-09-25.
- **Nothing was merged unattended.** The owner merged both. A session does not
  merge here, and under `main: review` a session merging its own work would be
  exercising the owner's bypass — the one thing that rule exists to prevent.
- **#12 carried no independent pass and said so in its own description.** The
  owner merged it on that basis, which is theirs to decide; it is recorded
  because the decision, not just the change, is the thing worth keeping.
- The owner has asked the second contributor to accept the organization
  invitation. It was still pending at close, so `.github/CODEOWNERS:11` remains
  invalid on the live repository and the Write grant is still owed. **A session
  can make that grant once the invitation is accepted; it needs no ruling.**
- In the Atlas archive, the front-page notice saying development moved is on
  pull request #18, still open and the owner's to merge. The three stale agent
  worktrees there are unregistered and emptied; two empty directories survive a
  process lock and go on the next restart.

**A sequencing lesson, recorded because it cost a rewrite.** This block was
first written while #12 was open, and said so. The owner merged #12 a few
minutes later, which made the block false before it ever landed, and it had to
be rebuilt against the new `main`. **A session-close record should be written
against `origin/main` as fetched at the moment of writing, and re-checked
immediately before it is pushed** — not composed against the branch it is
travelling on, whose state someone else may change underneath it. That is the
same hazard `AGENTS.md`'s synchronize-first rule names, arriving inside a single
session rather than between two.

The next session starts the way `AGENTS.md` step 1 says, not from this
paragraph: fetch, read what moved, and list the open pull requests and Issues.
Two of this file's own older sections are superseded by the one above, which is
the normal shape here — later entries stand in front of earlier ones without
rewriting them.

## Session close, 2026-09-22

**The owner ruled all seven evidence-bar questions**, one at a time and each
with a recommendation, recorded as `docs/OwnerDecisions.md` Part 18 (18a-18g)
on pull request #19. While answering, **the owner stated that Belay is a product
for others**. Users buy it, download it and connect their own AI, and a human
says yes or no to each recommendation. That is recorded as Part 19, with the
contradictions it raised and the owner's answers (19c).

In brief:

- **18a** criterion coverage: option 3's grade per rung, plus one record per
  canonical promotion criterion on the three capital rungs. **The owner chose
  stricter than recommended.** Real money is closed until all seven criteria
  are computable (`python scripts/status.py`: 3 of 7 today).
- **18b** the floor binds upward moves only.
- **18c** every review outcome carries evidence, including every `Remain`.
  **Stricter than recommended.**
- **18d** paper-trading length is referred to the Investment Committee, and
  `Micro Capital` is closed until a number is ruled.
- **18e** every promotion states how many variants were tried.
- **18f** every qualifying record names a stored, signed report, as part of
  this ruling and not as follow-up.
- **18g** the bar is written as a separate ADR-016.
- **19c** Belay's rules are fixed minimums. Each user sets their own gates at
  onboarding and can change them, directly or through their AI, only upward.
  Each human decision is recorded as evidence.

**State at close.** Pull request #19 carries this session's records, CI green
on every push. **The owner authorized the session to merge it: "i approve you
to merge btw".** The 2026-09-20 close record says a session does not merge
here, because under `main: review` a session merging exercises the owner's
bypass. This merge is that bypass, used on the owner's explicit instruction in
this session, for this pull request only. It is not a standing permission. It
carried no independent pass, which the pull request states. That pass belongs
to ADR-016. Pull request #14 (Parts
16-17) is still open. That is why Part 18 is numbered 18. The cadence gate
said review due 2026-09-23. The routine fires 2026-09-25.

## Highest priority next task

1. **Draft ADR-016 (PROPOSED) from Part 18 and 19c**, and point ADR-015
   rule 4's table at it on pull request #7's branch. Carry every "What it does
   not settle" item from Parts 18 and 19c as an open item in the ADR, not as a
   decision.
2. **A fresh independent pass on ADR-015 and ADR-016 together**, told to
   falsify them, before either is put to the owner for ratification.
3. **Then the seven questions in `docs/proposals/sample-adequacy-definition.md`**,
   one at a time. Its question 7 (one ruling or two for backtest adequacy and
   paper length) is partly answered by 18d, which referred paper length to the
   Investment Committee. Put it with that stated.
4. **Part 19's open questions**, one at a time: whether an AI-made change to a
   user's gates needs that user's recorded yes; Belay's own minimum
   paper-trading length; what makes a thesis "no longer valid".

## Session, 2026-09-24 — the review gate's finding count (#29)

Appended here so that no line citation moves.

**What was done.** Pull request #29 (branch `claude/determined-meitner-9h8sx3`)
hardens `scripts/review_due.py`, part of item 2 ("Harden the gate") in the
close record on #28's branch:

- finding numbers are read in ASCII digits only;
- the body of a review report's `## Outside text` section is not counted;
- a line in that section that starts with a finding number above every counted
  one stops the gate;
- the gate stops at F-999 rather than issue an F-1000 it cannot read back.

On this repository the gate's answer is unchanged: `first finding: F-031`.

**Verification.**
- Two independent falsification passes ran, both fresh-context agents inside
  the authoring session. Their findings and what was done about each are on
  #29.
- The second pass showed that the first fix's mutation count, written in a
  commit message, did not reproduce. Recount mutation claims with the pass's
  own script, not the author's.

**Open.**
- **The owner decides** whether to keep the outside-text rule (with a stated
  limit, in `counted_text`'s docstring) or drop it and count everything. The
  question is on #29 and in `docs/OperatorChecklist.md`.
- **Not done here, from #28's item 2:**
  - match report names with `fullmatch`;
  - survive an invalid date;
  - make `REPORT`'s own `\d` ASCII.
- **For whichever of #23 and #29 merges second:**
  - #23's skill says "The gate counts digits in any script", which #29 makes
    false for non-ASCII digits;
  - #23 pins that text in a test, so the pinned constant changes with it.
