# 2026-09-25 — Independent pass on the 2026-09-25 review, then the fixes

Issue #35, branch `claude/brave-pascal-e7401x`. Written once; never edited after merge.

## What was asked

Falsify all five findings of `reports/review/2026-09-25-review.md` (F-032 to F-036)
from a clean checkout, fix only what survives, and stop at the two needing the owner's
ruling. That report had no independent pass; its own pull request (#34) said so.

## Step 1 — what the falsification pass found

**All five findings survive.** None was overturned. Fresh checkout, baseline
reconfirmed at `704 passed, 1 skipped, 5 xfailed`, mutations applied one at a time to
a clone outside the repository.

### F-032 — stands, and the report understates it

All three mutations reproduce exactly — each applied alone, guard condition replaced
with `if False:`, `__pycache__` cleared — each leaving `704 passed, 1 skipped, 5
xfailed`: `review.py:271` (DEMOTE-on-a-climb), `review.py:235` (move-to-RETIRED),
`validator.py:215` (ADR-010 rule 9). Every `path:line` points at what it claims.

The unmutated code refuses all five constructed records, and each mutant admits
**only** its own guard's shape — the cross-check showing the probes are independent.
Under mutant 1, `Demote | Micro Capital -> Limited Capital` is accepted and signed;
under 2, `Remain Current Stage | Retired -> Retired` is accepted while
`Demote`/`Promote` to `RETIRED` hit `tuple.index(x): x not in tuple`; under 3, a
`Regime` carrying a `Universe Report` validates `True`. Transcripts on #36.

The process claim holds: `bdeffe8`'s message lists the two review guards `#24` tested
("Retire on a legal climb; Promote on a legal demotion"), so these two were never in
its scope — the list came from F-019's enumeration, not from the code.

**Defect found in the report (1 of 3) — the only one of this session's three to
survive its own independent pass.** F-032 says of `framework/artifacts/review.py:271`:
"The two branches are six lines apart. Only one of them has a test." Wrong, and the
truth is sharper: `tests/artifacts/test_review_decision.py:195`,
`test_a_demotion_that_climbs_is_refused`, is named for that guard and cannot fail for
it — its movement `Micro Capital -> Production` also skips a stage, so
`validate_transition` refuses it once the guard is gone and the bare
`pytest.raises(ValueError)` accepts either error. With `:271` removed that test still
passes, catching `Invalid lifecycle transition`. A test bearing a guard's name that
cannot fail for it is worse than no test: it is how the gap looked closed.

### F-033 — stands, and this session's two objections to it were both wrong

The fact reproduces. A hand-built `Disclosure`, `data_source="I made these up"`,
eight figures typed by hand:

```
validates:         True
evidence_level:    EvidenceLevel.HISTORICAL
signed:            7e437f18dba84f62
data_source:       I made these up
known_limitations: none
```

**Defect 2 and Defect 3 as first written were both WRONG, and are withdrawn.** The
independent pass on this session's work (#36, 14:21 UTC) refuted both. The original
text is in git at `5e7d456`; it is described, not restated, because what it argued was
mistaken.

They argued that `constitution/Evidence_Standards.md:39` ("Evidence hierarchy may
never be reversed") concerns *precedence between classes in conflict* rather than
grade assignment at emission — and from that, that F-033's primary citation was wrong
and that F-033 did not overturn the 2026-08-21 pass. Both fail on one fact: the
repository has already written down what `:39` covers, in the checklist `AGENTS.md`
binds every reviewer to.

```
$ sed -n '85,88p' .claude/skills/belay-review/references/red-team-checklist.md
**B5. Evidence level inflation.** `constitution/Evidence_Standards.md:39` — the
hierarchy may never be reversed. Look for anything labelled B (paper validated)
whose support is actually C (historical simulation), or C whose support is
really D. The label is a claim and needs a citation like any other.
```

"C whose support is really D" **is** assignment at emission, and the clause cited for
it **is** `:39`. F-033 is verbatim that case; B3 four lines above gives the same shape
("Level D dressed as Level C"), the report's own phrasing. **F-033's breach citation
as the report wrote it is correct.** Defect 3 falls with it, and the pass caught the
contradiction before the evidence did: Defect 3 depended on the 2026-08-21 bullet
being a B5 bullet while Defect 2 denied B5's clause reached this. Both could not hold.
Under B5 as written that bullet *was* asking F-033's question, and answered it by
assuming a "supplied series" had been supplied by something. **F-033 does overturn it,
as the report claimed.**

**What survives, as additions rather than corrections:** `:45` and
`constitution/Operational_Constraints.md:5` are also breached; High is right either way
by the skill's severity table; the title's "Sharpe of 17.6" is a property of which
eight numbers were typed (this construction returned 133.4); and the 2026-08-21 bullet
begins at `:801`, not the cited `:802`. **The lesson is the one this session was
convened to apply:** both withdrawn defects were prose asserted without opening the
governing document — the failure mode F-019 and F-032 are about, committed by the pass
sent to catch it.

### F-034 — stands, all four parts

`disclosure_from` has exactly one non-test occurrence, its own definition at
`framework/data/fetch_record.py:446`. `docs/HANDOFF.md:2054` heads F-002 "CLOSED
2026-08-02". `docs/DECISIONS.md:3091` reads "Accepted and implemented, 2026-08-02, in
all nine rules." The register gap is real: `docs/HANDOFF.md:2728-2733` withdrew the
2026-08-21 report's F-012 into F-011, whose write-up (`docs/HANDOFF.md:3915-3933`)
cites `docs/ROADMAP.md:43` against `:156` and `:165-167` only and scopes out the rest.
Searching every `docs/` and `reports/review/` file for the two shed claims finds them
in the withdrawn finding and nowhere open.

### F-035 — stands

The prompt's suggested check no longer works, and that is correct behaviour rather
than a defect: the 2026-09-25 report is now on `main`, so `scripts/review_due.py`
returns `SKIP` with exit 1 and allocates no number. Verified two other ways instead.

`docs/FINDINGS.md`'s highest registered number was F-030 and the report allocates
from F-032. Sweeping every `origin` ref for the missing one (`git for-each-ref` +
`git ls-tree` + `git show … | grep -q`) returns exactly two files, both on the single
unmerged branch `claude/great-turing-v2d0x8`: `docs/NOW.md` and
`docs/sessions/2026-09-25-final-text-round.md`. Four mentions between them, all
naming the gate's next number in passing; zero finding headings and zero register
rows. `e788cac` changed two lines in two files and recorded no rule.

### F-036 — stands

No file under `framework/`, `scripts/`, `tests/` or `departments/` imports `pandas`,
`jinja2` or `dateutil`; `numpy` is imported nowhere either, so removing `pandas` breaks
nothing today and the finding says the risk is prospective. `pip install -e ".[dev]"`
here pulled `pandas-3.0.6` and `numpy-2.4.6`, confirming the transitive reasoning.
Minor: it cites `docs/HANDOFF.md:1157-1159` for the `numpy` rejection but misses a live
copy of the same reasoning at `framework/metrics/distributions.py:11-15` — the
load-bearing one, because it sits where a developer reads it.

## What the report skipped, attacked here — two new guards survive

The report's "Not found" section named what it skipped. Two of those gaps were worked.
**Neither result has a finding number: the gate returns `SKIP` and allocates none
before 2026-10-07, and inventing one is the mistake F-035 is about.** Both are carried
in `docs/NOW.md` for the next review to number.

**A mutation sweep over the three data modules the report left alone** —
`framework/data/dolthub.py`, `dolt_clone.py`, `contract.py`, fifteen guards, one
mutation at a time. Thirteen are caught by the suite. Two are not:

- **`framework/data/dolt_clone.py:376`**, `if not isinstance(body, dict):` —
  survives at `704 passed`. With it removed, a bare `null` envelope from `dolt` gives
  a fully constructed `FetchedSeries` for AAPL with **zero bars**, over a payload
  asserting `"query_execution_status":"Success"`. That is the shape `_rows_of`'s own
  docstring (`framework/data/dolt_clone.py:404-418`) says the module was written to
  prevent: an unrecognised exit-0 answer becoming "a clean empty success…
  indistinguishable from a delisting".

  **Corrected by the independent pass: this reaches no signed artifact, and an
  earlier draft of this bullet said "signed" twice.** `FetchedSeries` carries no
  signature — its fields are `series` and `payload` — and the signing path refuses
  first: through `fetch_and_record` the same mutant gives `ValueError: the series for
  AAPL is empty and covers no period`. The guard is genuinely asserted by nothing and
  worth a finding, but the reachable exposure is a zero-bar `FetchedSeries` handed to
  a **direct** caller of `fetch_daily_bars`. Grade it on that; "signed" was carrying
  severity the construction had not earned.

- **`framework/data/contract.py:244`**, `if end < start:` — survives at `704
  passed`. Removing it lets an inverted fetch window reach the adapter.

**A partial tautological-test survey, and its first count was misleading.** A
paren-balanced scan of every `pytest.raises(...)` under `tests/` gives **59 of 146
carrying no `match=` at all** — 22 `ValueError`, 15 `TypeError`, 5
`FrozenInstanceError`, 8 across two-type tuples, 2 bare `Exception`, and 9 others.
Not the "22 of 143" first written: that counted only `pytest.raises(ValueError)`,
while the defect it sizes is *any* `raises` loose enough to accept an error the test
was not written for. 40%, not 15%, and the first figure erred in the flattering
direction in the one paragraph whose job is to say what the survey did not cover. The
two-type tuples and bare `Exception` are *looser* than the 22 counted. Corrected by
the independent pass; 14 of the 22 are in `tests/artifacts/test_review_decision.py`.

**`python scripts/verify_clone.py` still could not run:** `which dolt` returns
nothing. Fifth consecutive review to leave the live data path unverified.

**A claim here was false and is withdrawn.** This paragraph originally added that the
script "exits 0 when there is no clone, so it reports success having verified nothing
— the shape of F-009 and F-015." It does not; it exits **1**, loudly, with the remedy
(`scripts/verify_clone.py:60` is the `return 1`). **The cause was a shell error in
this session's own check:** the status was read after a pipe —
`python scripts/verify_clone.py 2>&1 | head -8; echo "exit=$?"` — which reports
`head`'s status, not Python's, and so printed 0. A wrong command produced a confident
claim inventing a defect in working code, and named two real findings as its family,
lending it credibility it had not earned. `AGENTS.md`, "Citations and counts", exists
for this: paste the exact command, and make sure the command measures what the
sentence says. Found by the independent pass.

## Step 2 — what was changed

Registered F-032 to F-036 in `docs/FINDINGS.md` under "Open", severity mapped per
`docs/HANDOFF.md:2755-2757`. **None is marked closed.** `bdeffe8` set that
precedent for this exact finding family: "F-019 is not marked closed here; it
closes after an independent pass and merge."

- **F-032.** Three regression tests, no production code touched:
  `test_a_demotion_recorded_on_a_legal_climb_is_refused` and
  `test_remaining_at_retired_is_refused` in
  `tests/artifacts/test_review_decision.py`;
  `test_a_deliverable_contradicting_its_artifact_type_fails_validation` in
  `tests/artifacts/test_validator_integrity.py`. Each mutation re-applied:
  **exactly its own test fails and nothing else**, the check `bdeffe8` ran. The
  existing `test_a_demotion_that_climbs_is_refused` was left unpinned on purpose and
  its docstring now says why — pinning it either way would make it a second test
  failing on one mutation. `docs/FINDINGS.md`'s "How this file is kept" gains the
  rule that closes the gap: a "guards asserted by nothing" finding closes against a
  list re-derived from the code.
- **F-034.** Stage 2's close-out and its disclosure-boundary paragraph rewritten.
  `docs/ROADMAP.md:43`'s "No market data layer" line **not** touched — open finding
  F-011. Plus the conformance test proposed twice and never built,
  `test_a_complete_stage_does_not_call_an_implemented_adr_unimplemented`. The
  independent pass found **two real bugs in it and one in the prose**, all fixed and
  re-proved: it classified ADR-006 as implemented (its Status reads "Not yet
  implemented", containing `implemented` but not the contiguous `not implemented`) and
  so flagged a *true* sentence; it missed both a claim split across a full stop and the
  "has not been implemented" verb form; and the rewritten prose asserted "Nothing here
  gates a bulk backfill" while citing, as evidence, a list containing `Every Fetch
  Reads Every Stored Record` — which the archive says is "a defensible trade at today's
  scale and not at a universe backfill's". That last is F-034's own failure mode
  reintroduced by F-034's fix. The test now carries a one-sentence look-back and a
  wider negation set, with its two remaining limits stated in its docstring; the prose
  names the cost instead of denying it.
- **F-035.** A rule in `AGENTS.md` under "Files that grow"; the sentence in
  `docs/NOW.md` that restated the gate's answer deleted rather than corrected; and
  `test_no_doc_names_a_finding_number_above_the_register`, confirmed red on a planted
  number above the register and confirmed to exempt the bracketed `F-[NNN]` form.

  **That test caught this record while it was being written**, which named the
  planted number in full — the exact burn the rule forbids, by the session writing
  the rule down. It is why F-035's fix had to be a test: `e788cac` wrote the sentence
  and the mistake recurred within a fortnight. Note the test is a point-in-time push
  gate, not a durable one: once #36 raises the register to F-036, F-031 is no longer
  *above* it, so the burned number sits in #33's `docs/NOW.md` unremarked and nothing
  will require the rewording. Said plainly so the next session does not read the test
  as covering it.

## Step 3 — not this session's, and not implemented

Two questions are in `docs/OperatorChecklist.md`, each with a recommendation:
**F-033**, what Level C should mean (a ruling and probably an ADR, because
`constitution/Evidence_Standards.md` is frozen by ADR-002), and **F-036**, whether to
drop the three unused dependencies (`AGENTS.md` makes `pyproject.toml` dependencies
the owner's alone). Neither is implemented here.

## Corrections to the frozen archive

`AGENTS.md`, "Files that grow": the archive is never edited — the correction goes in
the finding session's own record, naming the lines. This is that.

**`docs/HANDOFF.md:4156` now cites the wrong lines, and this session moved them.** It
reads "which `docs/ROADMAP.md:214-219` anticipates — the contract must carry both
questions…". This session inserted 13 lines at `docs/ROADMAP.md:166` and 19 at `:231`,
so everything from `:208` down shifted. The passage it means — "**And the adapter
contract must carry both survivorship questions from day one**…" — was at `:214-219`
and is now at **`docs/ROADMAP.md:227-232`**; `:214-219` is now a different bullet.

Found by the independent pass, which is the point: `AGENTS.md` says to repoint moved
citations in the same change, and this session's pull-request checklist restated that
rule *narrower* — "every line citation **I added or moved**" — which excludes exactly
the citations an insertion invalidates without touching. That is how it was missed.

Already stale before this branch, so not attributable here: other
`docs/ROADMAP.md:NNN` citations in the archive, among them `:225-240` as "Stage 7".
Live citations in code are unaffected — the three pointing into `docs/ROADMAP.md` all
target `:104`/`:107`, above both insertions. `docs/ROADMAP.md:43` is byte-identical to
`origin/main`, so F-011 is untouched.

## Verification

`python -m pytest -q` → **709 passed, 1 skipped, 5 xfailed**.
`python scripts/status.py` → exit 0, 45 open findings.

Each F-032 mutation re-applied against the **finished** branch, one at a time:

```
MUTANT review.py:271    -> FAILED test_a_demotion_recorded_on_a_legal_climb_is_refused   (1 failed, 708 passed)
MUTANT review.py:235    -> FAILED test_remaining_at_retired_is_refused                   (1 failed, 708 passed)
MUTANT validator.py:215 -> FAILED test_a_deliverable_contradicting_its_artifact_type_... (1 failed, 708 passed)
```

**First recorded as `706 passed`, which was wrong** and is corrected here: 706 + 1 =
707, the intermediate tree carrying only the three F-032 tests, before the two
conformance tests existed. The conclusion held — exactly one test fails per mutation,
and it is the right one — but the stated tree was not what shipped, and this is the
block a reader uses to judge that. Found by the independent pass.

## What is open

- The owner's two rulings. F-033 and F-036 cannot be worked until they land.
- The two new surviving guards, awaiting a number from the next gate run.
- A full tautological-test survey: 59 of 146 `pytest.raises` carry no `match=`; and
  the live data path, still unverified for want of `dolt`.
- **The burned number F-031 stops being caught** once this branch raises the register
  to F-036 (Step 2, under F-035). #33's four prose mentions want rewording and nothing
  will require it.
- The independent pass on this work **has run** (#36, 14:21 UTC): three blocking, five
  defects, four notes, each verified and acted on. **Two of this session's own three
  reported defects were withdrawn as wrong.** That ratio, on a session whose subject
  was other people's unchecked prose, is the argument for the pass.
