# 2026-09-25 — Independent pass on the 2026-09-25 review, then the fixes

Issue #35. Branch `claude/brave-pascal-e7401x`. Written once; never edited after
this merges (`AGENTS.md`, "Files that grow").

## What was asked

Falsify all five findings of `reports/review/2026-09-25-review.md` (F-032 to
F-036) from a clean checkout, fix only what survives, and stop at the two that
need the owner's ruling. That report had no independent pass; its own pull request
(#34) said so.

## Step 1 — what the falsification pass found

**All five findings survive.** None was overturned. Environment: fresh checkout,
`pip install -e ".[dev]"`, baseline reconfirmed at `704 passed, 1 skipped, 5
xfailed`. Mutations were applied one at a time to a clone under a scratch
directory outside the repository, `__pycache__` cleared before each run.

### F-032 — stands, and the report understates it

All three mutations reproduce exactly. Each was applied alone by replacing the
guard's condition with `if False:`:

```
MUTANT [review.py:271  DEMOTE-on-a-climb guard removed] -> 704 passed, 1 skipped, 5 xfailed
MUTANT [review.py:235  move-to-RETIRED guard removed]   -> 704 passed, 1 skipped, 5 xfailed
MUTANT [validator.py:215 ADR-010 rule 9 pair removed]   -> 704 passed, 1 skipped, 5 xfailed
```

Every `path:line` in the finding points at what it claims. The unmutated code
refuses all five constructed records; each mutant admits **only** its own guard's
shape, which is the cross-check that shows the three probes are independent:

```
MUTANT review.py:271   ACCEPTED: Demote | Micro Capital -> Limited Capital | signed 74bee36a47e7
MUTANT review.py:235   ACCEPTED: Remain Current Stage | Retired -> Retired | signed 85db177b60f6
                       REFUSED : Demote | Production -> Retired | tuple.index(x): x not in tuple
MUTANT validator.py:215 ACCEPTED: type=Regime deliverable=Universe Report validates=True
```

The process claim holds. `bdeffe8`'s commit message lists the two review guards
`#24` tested — "Retire on a legal climb; Promote on a legal demotion" — so the
`DEMOTE`-on-a-climb guard and the move-to-`RETIRED` guard were never in its scope.
The list came from F-019's enumeration, not from the code.

**Defect found in the report (1 of 3).** F-032 says of the guard at
`framework/artifacts/review.py:271`: "The two branches are six lines apart. Only
one of them has a test." That is wrong, and the truth is sharper.
`tests/artifacts/test_review_decision.py:195`,
`test_a_demotion_that_climbs_is_refused`, is named for precisely that guard. It
cannot fail for it: its movement `Micro Capital -> Production` also skips a stage,
so `validate_transition` refuses it once the guard is gone, and the bare
`pytest.raises(ValueError)` accepts either error. Proved by running that one test
against the mutant:

```
$ python -m pytest -q tests/artifacts/test_review_decision.py::test_a_demotion_that_climbs_is_refused
1 passed          # with review.py:271 removed
   ValueError: Invalid lifecycle transition: MICRO_CAPITAL -> PRODUCTION
```

A test bearing a guard's name that cannot fail for it is worse than no test: it is
how the gap looked closed. Recorded here because it changes how F-032 should be
read, not because it weakens it.

### F-033 — stands as a finding; two defects in its write-up

The fact reproduces. A hand-built `Disclosure`, `data_source="I made these up"`,
eight figures typed by hand:

```
validates:         True
evidence_level:    EvidenceLevel.HISTORICAL
signed:            7e437f18dba84f62
data_source:       I made these up
known_limitations: none
```

**Defect (2 of 3): the primary breach citation does not support the claim.**
F-033 is graded High on `constitution/Evidence_Standards.md:39`, "Evidence
hierarchy may never be reversed." Read with the two lines that gloss it — `:41`
"Hypotheses do not invalidate production evidence" and `:43` "Production evidence
may invalidate hypotheses" — that clause governs *precedence between classes when
they conflict*. It says nothing about how a grade is assigned when an artifact is
emitted. Mis-grading mislabels a member of the hierarchy; it does not reverse the
hierarchy. The breaches that do hold are `:45` ("Every conclusion must reference
supporting evidence" — the grade is a conclusion nothing supports) and
`constitution/Operational_Constraints.md:5`, both of which the report cites only
secondarily.

**Severity High is nonetheless correct**, by the review skill's own table: High is
"breaches `Evidence_Standards.md` or `Governance.md`", and `:45` is breached.
Medium is reserved for doc-vs-code drift. The grade stands on a different line
than the one cited.

**Defect (3 of 3): it does not overturn the 2026-08-21 pass, as it claims.** That
bullet (`reports/review/2026-08-21-review.md:801-810`) is headed "Evidence-level
**inflation** on any live path (B5)" and asks whether a caller can mint a grade
*stronger* than C. Its answer — no, the level is hardcoded, nothing mints A or
B — is still correct today. It never asked whether C fits a series that was
supplied by nothing. The two findings are compatible. **So F-033 is not
withdrawn**, and the earlier pass was not wrong; the report's framing of it as an
overturned decision is.

Also: the title's "a Sharpe of 17.6" is a property of which eight numbers were
typed, not of the defect. The same construction here returned 133.4.

### F-034 — stands, all four parts

- `disclosure_from` has exactly one non-test occurrence, its own definition:
  `grep -rn 'disclosure_from' --include='*.py' . | grep -v '^./tests'` returns
  `./framework/data/fetch_record.py:446:def disclosure_from(`.
- `docs/HANDOFF.md:2054` heads F-002 "CLOSED 2026-08-02".
- `docs/DECISIONS.md:3091` reads "Accepted and implemented, 2026-08-02, in all
  nine rules."
- The register gap is real. `docs/HANDOFF.md:2728-2733` withdrew the 2026-08-21
  report's F-012 as a duplicate of F-011; F-011's write-up
  (`docs/HANDOFF.md:3915-3933`) cites `docs/ROADMAP.md:43` against `:156` and
  `:165-167` only and scopes out the rest. Searching every `docs/` and
  `reports/review/` file for the two shed claims finds them in the withdrawn
  finding and nowhere open.

### F-035 — stands

The prompt's suggested check no longer works, and that is correct behaviour rather
than a defect: the 2026-09-25 report is now on `main`, so
`python scripts/review_due.py` returns `SKIP` with exit 1 and allocates no number.
Verified two other ways instead.

The gap: `docs/FINDINGS.md`'s highest registered number was F-030 and the report
allocates from F-032. Where the missing one went:

```
$ for ref in $(git for-each-ref --format='%(refname)' refs/remotes/origin/); do
    for f in $(git ls-tree -r --name-only $ref -- reports docs | grep '\.md$'); do
      git show $ref:$f 2>/dev/null | grep -q 'F-031' && echo "$ref :: $f"
    done
  done | sort -u
refs/remotes/origin/claude/great-turing-v2d0x8 :: docs/NOW.md
refs/remotes/origin/claude/great-turing-v2d0x8 :: docs/sessions/2026-09-25-final-text-round.md
```

Four mentions across those two files, all naming the gate's next number in
passing; zero finding headings and zero `docs/FINDINGS.md` rows. `e788cac`
changed two lines in two files and recorded no rule.

### F-036 — stands

No file under `framework/`, `scripts/`, `tests/` or `departments/` imports
`pandas`, `jinja2` or `dateutil`. `numpy` is imported nowhere either, so removing
`pandas` breaks nothing today — the risk the finding names is prospective, and it
is stated that way. `pip install -e ".[dev]"` in this container pulled
`pandas-3.0.6` and `numpy-2.4.6`, confirming the transitive-install reasoning.

Minor: the finding cites `docs/HANDOFF.md:1157-1159` for Belay's rejection of
`numpy` but misses a live copy of the same reasoning in code, at
`framework/metrics/distributions.py:11-15`. The code comment is the load-bearing
one, because it sits where a developer reads it.

## What the report skipped, attacked here — two new guards survive

The report's "Not found" section named what it did not do. Two of those gaps were
worked, and both produced results. **Neither has a finding number: the gate
returns `SKIP` today and allocates none, and inventing one is the mistake F-035
is about.** They are recorded here and in `docs/NOW.md` for the next review to
number.

**A mutation sweep over the three data modules the report left alone** —
`framework/data/dolthub.py`, `dolt_clone.py`, `contract.py`, fifteen guards, one
mutation at a time. Thirteen are caught by the suite. Two are not:

- **`framework/data/dolt_clone.py:376`**, `if not isinstance(body, dict):` —
  survives at `704 passed`. This is the sharper of the two. With it removed, a
  bare `null` envelope from `dolt` produces a fully constructed `FetchedSeries`
  for AAPL carrying **zero bars**, whose signed payload asserts success:

  ```
  CONSTRUCTED FetchedSeries: symbol=AAPL bars=0
  payload signed over: b'{"envelope":1,...,"query_execution_status":"Success","rows":[],...'
  period() REFUSES (lazily): the series for AAPL is empty and covers no period
  ```

  That is the exact failure `_rows_of`'s own docstring
  (`framework/data/dolt_clone.py:404-418`) says the module was written to prevent:
  an unrecognised exit-0 answer becoming "a clean empty success…
  indistinguishable from a delisting". The empty series is only caught later, by
  `DailyBarSeries.period()` — a method, so only if something calls it. Same shape
  and same breach as F-032.
- **`framework/data/contract.py:244`**, `if end < start:` — survives at `704
  passed`. Removing it lets an inverted fetch window reach the adapter.

**A partial tautological-test survey.** 22 of 143 `pytest.raises` calls under
`tests/` are bare `pytest.raises(ValueError)` with no `match=`; 14 of those are in
`tests/artifacts/test_review_decision.py`. That shape is what let the misnamed
test above look like coverage. Not a full survey — 709 tests is more than this
pass read.

**`python scripts/verify_clone.py` still could not run:** `which dolt` returns
nothing. Fifth consecutive review to leave the live data path unverified. Noted in
passing: it exits 0 when there is no clone, so it reports success having verified
nothing — the shape of F-009 and F-015. Not investigated further.

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
  `tests/artifacts/test_validator_integrity.py`. Each mutation re-applied
  afterwards: **exactly its own test fails and nothing else**, which is the check
  `bdeffe8` ran. The existing `test_a_demotion_that_climbs_is_refused` was left
  unpinned on purpose and its docstring now says why — pinning it to either
  message would make it a second test failing on one mutation.
  `docs/FINDINGS.md`'s "How this file is kept" gains the rule that closes the gap:
  a "guards asserted by nothing" finding closes against a list re-derived from the
  code.
- **F-034.** `docs/ROADMAP.md`'s Stage 2 close-out rewritten, and its
  disclosure-boundary paragraph rewritten to say that the capability exists and
  nothing requires it (F-003). `docs/ROADMAP.md:43`'s "No market data layer" line
  was **not** touched — that is open finding F-011. Plus the conformance test
  proposed twice and never built, in `tests/test_governance_conformance.py`:
  `test_a_complete_stage_does_not_call_an_implemented_adr_unimplemented`, confirmed
  red against the reinstated defect and green without it.
- **F-035.** A rule in `AGENTS.md` under "Files that grow"; the sentence in
  `docs/NOW.md` that restated the gate's answer deleted rather than corrected; and
  `test_no_doc_names_a_finding_number_above_the_register` in
  `tests/test_handoff_files.py`, confirmed red on a planted number above the
  register and confirmed to exempt the bracketed `F-[NNN]` quoting form.

  **That test caught this record while it was being written.** The paragraph above
  originally named the planted number in full — `F-[037]`, written here in the
  bracketed form — which is precisely the burn the rule forbids, committed by the
  session writing the rule down. It is the strongest evidence available that the
  mechanism works, and it is why F-035's fix had to be a test rather than another
  sentence: `e788cac` wrote the sentence and the same mistake recurred within a
  fortnight.

## Step 3 — not this session's, and not implemented

Two questions are in `docs/OperatorChecklist.md`, each with a recommendation:
**F-033**, what Level C should mean (a ruling, and probably an ADR, because
`constitution/Evidence_Standards.md` is frozen by ADR-002), and **F-036**, whether
to drop the three unused dependencies (`AGENTS.md` makes `pyproject.toml`
dependencies the owner's alone). Neither is implemented here.

## Verification

```
$ python -m pytest -q
709 passed, 1 skipped, 5 xfailed
$ python scripts/status.py      # exit 0, 45 open findings
```

Each F-032 mutation re-applied against the finished branch:

```
MUTANT review.py:271    -> FAILED test_a_demotion_recorded_on_a_legal_climb_is_refused        (1 failed, 706 passed)
MUTANT review.py:235    -> FAILED test_remaining_at_retired_is_refused                        (1 failed, 706 passed)
MUTANT validator.py:215 -> FAILED test_a_deliverable_contradicting_its_artifact_type_...      (1 failed, 706 passed)
```

## What is open

- The owner's two rulings above. F-033 and F-036 cannot be worked until they land.
- The two new surviving guards, awaiting a finding number from the next gate run.
- A full tautological-test survey over `tests/`, and the 22 unpinned
  `pytest.raises` calls.
- The live data path, still unverified for want of `dolt`.
- **This session's own work needs an independent pass before it lands**
  (`AGENTS.md` point 4). Being the falsifying pass on someone else's work does not
  make this work self-verified.
