# DRAFT — ADR-016: The Evidence Bar — What Evidence Buys Each Rung, And What No User Setting Can Lower

Status:
**PROPOSED — drafted from owner rulings, revised 2026-09-24 after a falsification
pass and the owner's Part 25, and 2026-09-25 after a second pass and the owner's
Part 26. Not ratified. Not implemented in any part.**

Date:
2026-09-22 (revised 2026-09-24, 2026-09-25)

---

> **Where this lives, and why here.** ADR-015 is PROPOSED and lives only on public
> pull request #7's branch, `adr/015-stage-is-carried`, not on `main`. This draft
> fills ADR-015 rule 4's table, so it cannot be appended to `docs/DECISIONS.md` on
> `main` without citing an ADR that is not there. It is kept here, beside
> `docs/proposals/ADR-014-rule-5-amendment-DRAFT.md`, until the owner rules where
> both ADRs land.
>
> **ADR-015 is now cited by line** (finding N7): as "ADR-015 at `26f5d75`, lines
> n-m", meaning DECISIONS.md under docs/ on branch `adr/015-stage-is-carried` at
> commit 26f5d75. *(Repointed 2026-09-25 from `94815a2`, the previous revision.)* The file name and line numbers are written without backticks on
> purpose: the file on this branch is `main`'s, where ADR-015 does not exist, and the
> repository's citation test would read them against the wrong file. They go stale when that
> branch changes; repoint them when it does.

> **What changed in this revision (2026-09-25).** A second pass on the redrafts
> (Issue #21, the comment "Second supplementary pass: the redrafts, ADR-015 at
> `94815a2` (#7) and ADR-016 at `bad17de` (#20), read against Part 25") found
> nothing blocking of its own in this draft and called it "ready after fixes", but
> not ratifiable before ADR-015. Against this draft it found should-fix 2N5-2N9 and
> 2N13 (its labels were N5-N9 and N13; this draft writes "2N" because the first
> pass used N1-N7 for its nits). The owner then ruled **Part 26 (26a-26f),
> 2026-09-24: "Aligned"**. This revision separates reports a review *considered*
> from reports it *binds* (2N5), ties each allowlisted metric to the grade its
> producing module writes (2N6), makes `bar_version` non-decreasing along a ladder
> (2N7), replaces the fixed trial cap of 18 with one computed from each significance
> report's degrees of freedom at 5% (26b, 2N8), counts only the reviews each ladder
> names in the variant lineage (2N9), adds `README.md` to the Required Follow-Up
> (2N13), and keeps every capital rung closed until a human authorization can be
> verified (26f). "Changes this makes to ADR-015" is rewritten against ADR-015 at
> `26f5d75`. The scratch model that checked these rules is described under "Findings
> and rulings".
>
> **What changed in the 2026-09-24 revision (kept as history).** A falsification pass on this
> draft and ADR-015 together (Issue #21, the comment "Supplementary falsification
> pass on ADR-015 (#7) and ADR-016 (#20), taken together") found both not ready.
> Against this draft: B4, one made-up evidence record listed under all seven
> criteria passed every rule for a capital rung (executed); B5, a bound report
> pinned neither the grade, the strategy it is about, nor its verdict; B6, drafter
> choices were labeled RULED; B3 and B7, shared with ADR-015. The owner then ruled
> ten principles, **Part 25 (25a-25j), 2026-09-24: "aligned to all 10
> recommendations".** "Findings and rulings, and where each is resolved", at the
> end, maps every finding and every ruling to the rule that resolves it.

> **Where the rulings this draft rests on are recorded.**
>
> - Parts 18, 19 and 23 are on `main` (`docs/OwnerDecisions.md`).
> - **Part 22 (sample adequacy) is on this branch and not yet on `main`.**
> - **Parts 25 and 26 are recorded on branch `claude/kind-knuth-9g7xlr` and are not
>   yet on `main` or on this branch.** Every rule below that cites 25x or 26x rests
>   on that record. If it does not reach `main` as written, those rules revert to
>   DRAFTER.
> - **Only Parts 18, 19, 22, 23, 25 and 26 are cited as RULED.** Anything else is
>   DRAFTER, and every number no Part rules is `None`, which keeps its rung closed.

> **What the owner ruled, and what the drafter chose.** Every rule below carries
> one of two marks, and a rule with parts of each marks each part:
>
> - **RULED (Part n)** — the owner's ruling, cited to `docs/OwnerDecisions.md`,
>   where the owner's words are quoted.
> - **DRAFTER** — a choice this draft makes to turn a ruling into something code can
>   check. The owner has not seen or ruled it. Each one is listed again under
>   "Put to the owner at ratification".
>
> Nothing marked DRAFTER may be read as ruled. *(Finding B6: the previous revision
> marked rule 1's whole table RULED, including a column that 18f says "is not
> ruled", and restated 19c's minimums in words 19c does not use. Both are
> corrected below.)*

> **Nothing in this revision has had an independent pass.** The scratch model below
> was written by the author, so it is not one. `AGENTS.md` (How work is
> claimed and landed, point 4) requires one before anything is called verified. The
> owner's chosen different-AI pass on Issue #21 is still owed (Part 25, "What it
> does not settle").

---

## Context

**ADR-015 closes F-007 and F-014.** Its rule 4 requires every review outcome to carry
evidence, and reserves a table for the minimum each rung needs. The research the
owner asked for is evidence-bar-per-rung.md under docs/proposals/ on pull request
#7's branch (not on `main`, so named without backticks). It ended in seven
questions.

**On 2026-09-22 the owner answered all seven** (`docs/OwnerDecisions.md` 18a-18g)
and, while answering, stated that Belay is a product for others: bought,
downloaded, and connected to the buyer's own AI, with a human saying yes or no to
each recommendation (Part 19). Part 19c ruled that Belay's minimums are ones no
user can lower. **18g ruled that the bar is its own decision record**, so that it can
change without reopening how the ladder works. This is that record.

**On 2026-09-24 the owner ruled Part 25** after the falsification pass above, and
then **Part 26** after the second pass.

**What the rulings demand that nothing in Belay can check today:**

1. **ADR-015's gate reads one grade.** Its check is `strongest_evidence_level`
   (`framework/artifacts/enums.py:29-43`) against a table. It cannot count records
   or see what any record is about, so 18a's "one record per criterion" has no
   mechanism.
2. **An evidence record's `provenance` is free text**
   (`framework/artifacts/evidence.py:12-18`). Its seal proves the record is
   unedited, not that anything it names exists (18f).
3. **A REPORT names no strategy.** `metric_artifact()` writes `metric`, `value`,
   `observations`, the caller's parameters and the four disclosures into `content`
   (`framework/metrics/reporting.py:219-232`), and nothing that says which strategy
   the series came from.
4. **Every metric report is graded C.** `metric_artifact()` grades its own evidence
   `HISTORICAL` unconditionally (`framework/metrics/reporting.py:210-217`).
5. **No REVIEW has ever been stored.** ADR-015 rule 5 verified that only
   `artifacts/RPT-0001/1.0.0.yaml` was ever committed, so REVIEW `content` is still
   free to change. After the first review is saved, every change is a migration of
   permanent records.

**Where new fields go.** This draft puts every new review field on the REVIEW's signed
`content` (point 5), and adds `subject_id` and `subject_integrity_hash` to REPORT
`content` (point 3). **DRAFTER.** The previous revision also said a new
`EvidenceRecord` field was impossible because the record's hashed payload is
pinned by a literal digest (`tests/artifacts/test_evidence_hashing.py:18`). **That
reason was overstated (finding S9) and is withdrawn:** a new optional field left out
of `canonical_payload` when unset (`framework/artifacts/evidence.py:62-75`) would not
move any existing digest. Both routes are open, and 18f leaves the choice to the
implementing change. The reasons this draft still prefers the REVIEW are weaker and
stated as such: the per-criterion mapping, the subject check and the "every report
since the previous step" check (rule 3) are properties of one review, not of one
record. The cost of that choice: a record does not itself commit to its report, so
the same record could be bound to different reports on different reviews. Rule 3's
grade check and rule 2's distinctness check limit what that buys.

---

## Decision

### Rule 1 — The grade floor per rung, upward moves only

**RULED (18a, 18b).** This fills ADR-015 rule 4's table (ADR-015 at `26f5d75`, lines
4827-4845).

| Rung reached (`to_stage`) | Minimum `EvidenceLevel` — upward moves only |
|---|---|
| Research | D |
| Validation | D |
| Paper Trading | C |
| Promotion Review | B |
| Micro Capital | B |
| Limited Capital | A |
| Production | A |
| Retired | no floor — a retirement is never upward |

**The grades are RULED** (18a: "destination `Research` D, `Validation` D, `Paper
Trading` C, `Promotion Review` B, `Micro Capital` B, `Limited Capital` A,
`Production` A"). **Upward only is RULED** (18b). *(The previous revision had a third
column, "Also required on this rung", under the same RULED mark. It is removed: which
other rules bind which rung is set in each rule below, with its own mark.)*

**Direction is computed exactly as ADR-015 rule 4 drafts it** (ADR-015 at `26f5d75`,
lines 4871-4904): a move to `Retired` is classified first and is never upward;
otherwise a move is upward when `STRATEGY_LADDER.index(to_stage) >
STRATEGY_LADDER.index(from_stage)` (`framework/artifacts/enums.py:107-109`). Grades
compare through `EVIDENCE_STRENGTH` (`framework/artifacts/enums.py:21-26`), never
through declaration order.

**Why these grades.** They are the proposal's option 3: each rung needs the grade
the last evidence-producing stage before it is defined to produce. That mapping is
an inference from names, which the proposal states in its section 9 and the owner
ruled knowingly. Level A on `Limited Capital` is not a deadlock: `Micro Capital`
trades real capital, and so produces Level A (`Knowledge/EvidenceRegistry.md:9`).

### Rule 2 — On the three capital rungs, seven distinct records backed by seven distinct reports

**RULED (18a, 25a).** An upward move into `Micro Capital`, `Limited Capital` or
`Production` carries, for **each** of the seven criteria of
`constitution/Promotion_Pipeline.md:75-81`, an evidence record at or above that
rung's floor. The list is exactly:

> Statistical performance · Risk-adjusted returns · Drawdown behavior · Regime
> robustness · Execution quality · Liquidity · Operational consistency

The spellings in `strategies/PromotionCriteria.md` and `Validation/CapitalReview.md`
do not change the list (18a). **25a: "'One evidence record per promotion criterion'
(18a) means seven distinct records. Each is backed by its own stored report, of a
kind suited to its criterion."**

**DRAFTER — the mechanism** (finding B4). The REVIEW's `content` gains
**`criterion_evidence`**: a mapping from each of the seven criterion names, spelled
as above, to exactly one evidence-record hash. The check refuses the review unless:

1. all seven names are present, and no other name;
2. every listed hash is the `hash` of a record in the review's `Artifact.evidence`;
3. **the seven hashes are distinct** — no record is listed under two criteria;
4. each listed record meets the rung's floor (rule 1);
5. each listed record is bound under rule 3 to a report, and **the seven reports
   are distinct**, compared by `(report_id, report_version)`;
6. **each bound report's `metric` is in its criterion's allowlist, and the report's
   grade is exactly the grade that entry says its producing module writes** (below;
   second-pass finding 2N6).

**The per-criterion allowlist — DRAFTER, tied to the modules that exist.** `metric`
is the `content` key `metric_artifact()` writes
(`framework/metrics/reporting.py:220`). **Each entry names its producing module and
the grade that module writes.** Every entry today is Level C, because
`metric_artifact()` grades its own evidence `HISTORICAL` unconditionally
(`framework/metrics/reporting.py:210-217`), and all three modules go through it.

| Criterion | Allowed `metric` | Producing module | Grade it writes |
|---|---|---|---|
| Statistical performance | `statistical_significance`, and rule 8 applies | `framework/metrics/statistics.py:355` | C |
| Risk-adjusted returns | `sharpe_ratio` | `framework/metrics/risk_adjusted.py:161` | C |
| Risk-adjusted returns | `sortino_ratio` | `framework/metrics/risk_adjusted.py:195` | C |
| Drawdown behavior | `max_drawdown` | `framework/metrics/drawdown.py:89` | C |
| Regime robustness | *none — empty* | no working module (`scripts/status.py:48-56`) | — |
| Execution quality | *none — empty* | no working module | — |
| Liquidity | *none — empty* | no working module | — |
| Operational consistency | *none — empty* | no working module | — |

**A report whose `evidence_level`, as the validator re-derives it, differs from its
entry's grade is refused (2N6).** Without this the grade check of rule 3 moved down
one level: a hand-built REPORT could grade itself A, and a record graded A could then
bind to it. The pass executed that with the four empty allowlists filled: seven
hand-built reports self-graded A passed rules 2 and 3. The scratch model re-ran it
against this wording (scenario B): all seven are refused, each naming its module and
the grade it writes. **What this does not check:** that the report really came from
the module named. A hand-built report that grades itself C passes this check, and is
then limited by rule 1's floor and rule 3 check 4: a record bound to a C report is at
most C, below every capital rung's floor. So a capital rung needs a module that
writes B or A, which none does today. **An entry is added only with its module and
its grade, as an amendment of this ADR and a new `bar_version`.**

**An empty allowlist refuses every report for that criterion**, so every capital
rung stays closed until all four missing criteria have a module and a ruled entry
here. That is 18a's "Real money is closed until all seven can be measured", made
checkable. `cagr` (`framework/metrics/returns.py:124`) is in no list: a growth rate
is not risk-adjusted. **Adding a metric to a list is an amendment of this ADR and a
new `bar_version` (rule 10), never a code change a session makes.**

**B4's executed attack, and why it now fails.** One `EvidenceRecord`, self-graded A,
source "I made this up", empty methodology, listed under all seven criteria and
bound to `RPT-0001` (28 daily bars). It fails check 3 (one hash under seven names),
check 5 (one report for seven criteria), check 6 (`RPT-0001`'s metric, and four empty
allowlists), and rule 3's grade check (an A record bound to a report graded C).

**What this still does not check:** that a report *measures well* what its metric
names. The allowlist checks the report's declared kind; the report's own numbers are
as trustworthy as the run that produced them. Required Follow-Up item 3.

### Rule 3 — Qualifying evidence names a stored report that resolves, is about this strategy, and is no weaker than the record

**RULED (18f):** each qualifying record names a stored, signed report by identifier,
version and integrity hash, and Belay refuses a record whose report does not resolve
or whose hash does not match. **RULED (25a)** that each capital-rung criterion record
is backed by its own report; **RULED (25b)** that the Paper Trading and capital rungs
rest on a significance report (rule 8).

**DRAFTER — which records qualify.** Every evidence record on an **upward** move whose
destination is `Paper Trading` or above. 18f says which records qualify "is not
ruled"; 25a and 25b rule it for the capital-rung criterion records and for the
significance report, and this draft extends it to every record on those moves and to
`Promotion Review`. Records on `Research` and `Validation` promotions are Level D
notes with no report behind them. **Records on downward moves and on `Remain` are
not bound** (DRAFTER): binding them would put a step before a demotion, which 18b
and 25d argue against. See "Put to the owner", items 2 and 3.

**DRAFTER — the mechanism.** The REVIEW's `content` gains two keys (second-pass
finding 2N5 separated them):

- **`evidence_reports`, the reports the review _binds_**: a mapping from each
  qualifying record's `hash` to three strings, `report_id`, `report_version` and
  `report_integrity_hash` — ADR-015 rule 1's three-part reference, one level down.
  A bound report is *support*: the review rests on it.
- **`reports_considered`, the reports the review _lists_**: every stored REPORT in
  **the subject's range** (check 5 defines it), each as the same three strings.
  A listed report is a *disclosure*: the review says it exists, and rests nothing on
  it. Every bound report is also listed.

On `save()` and `get()` of the review, in ADR-015 rule 3c where it reads the last
rung's review (26e), and in ADR-015 rule 3f's sweep, the repository refuses the
review when:

1. **a qualifying record has no `evidence_reports` entry;**
2. **a bound or listed report does not resolve through `get(report_id,
   report_version)`** (finding S8). Resolution goes through `get()`, which
   recomputes the hash from the stored contents
   (`framework/artifacts/repository.py:185-190`), and then compares the returned
   artifact's `integrity_hash` with `report_integrity_hash`. **Reading the stored
   `integrity_hash` field and comparing it is not resolution**: a file edited after
   storing keeps its old field. The resolved report is then run through
   `ArtifactValidator().validate()`, because ADR-015 rule 3.0 does not put REPORTs
   in `get()`'s validation scope;
3. **a bound or listed report's `type` is not `REPORT`;**
4. **a bound record's grade is stronger than its report's** (finding B5): the
   record's `level` must be at or below the report's `evidence_level`, as the
   validator re-derives it, compared through `EVIDENCE_STRENGTH`. A record
   self-graded A cannot bind to a report the code grades C;
5. **a bound or listed report is outside the subject's range** (finding B5). REPORT
   `content` gains **`subject_id`** and **`subject_integrity_hash`**, written by
   `metric_artifact()` and inside the report's signature. **The subject's range** is
   every stored REPORT whose `subject_id` equals the review's `subject_id` and whose
   `subject_integrity_hash` is the `integrity_hash` of a stored version of that
   strategy whose ladder is a prefix of the reviewed version's ladder. A report with
   no subject, or about another strategy, can be neither bound nor listed;
6. **a bound report omits a disclosure** (finding S15): any of `assumptions`,
   `data_source`, `sample_period_start`, `sample_period_end` or `known_limitations`
   is missing or blank in its `content` (`framework/metrics/reporting.py:124-133`,
   `:227-231`);
7. **a stored report in the subject's range is not listed** (finding S14, below).

**Checks 4 and 6, and rule 2's checks 5 and 6, apply only to bound reports.** A
listed report need only resolve, be a REPORT and be in range. *(Second-pass finding
2N5: under the previous revision every stored report since the last step had to be
bound, and binding applied the grade and disclosure checks, so one stored junk
report about a strategy blocked every promotion of it.)*

**The listing's range is exactly check 5's range — 2N5.** Under the previous
revision the listing covered only reports tagged with a version at the subject's
current ladder length, while check 5 accepted any version on the history. So a
failed report tagged with an older subject version could be left out of the listing
and still be eligible for binding. Now one definition, "the subject's range", serves
both, from `Idea` onwards.

**`variants_tried` is at least the number of significance reports listed — 2N5.**
Every listed report whose `metric` is `statistical_significance` is one variant that
was tested. A `Promote` whose `variants_tried` is smaller is refused, naming both
numbers. This is what makes the listing bite: a failed trial that is stored is
counted, whether or not the review binds it. **The cost, stated:** anyone who can
write the store can store significance reports about a strategy and so push its
lower bound above rule 6's cap, which refuses the promotion. That is a denial of
capital, not a grant.

**Cost, stated:** check 7 needs a listing of the store by subject, which the
repository does not have (`framework/artifacts/repository.py:69-84` lists one
identifier's versions). It is the subject index ADR-015 rule 3h also needs (ADR-015
at `26f5d75`, lines 4672-4679), derived from the store and never a separately
maintained file. Required Follow-Up.

**The "never stored" residual — named, and not closed (2N5).** Check 7 sees only
what is stored with a subject in range. Three kinds of trial escape it: a report
computed and never saved; a report saved with no `subject_id`, or with one that
names no version in range; and a computation run with other software. Nothing in
Belay can see any of them. Only `variants_tried` records them, and it is
self-declared (rule 6). **Whether this falls under 25j: DRAFTER, no, in part.** 25j
rules out of scope "trading done outside Belay". A backtest run with Belay's own
code and then discarded is neither trading nor outside Belay, so this draft does not
treat it as covered by 25j; it is a residual of this ADR, stated here and put to the
owner (item 12). A computation run entirely outside Belay is closer to 25j's reason,
but 25j names trading, not research, so that reading is the owner's to make.

**What binding does not prove — survivorship and lookahead (finding S15).** Check 6
proves the report *discloses*; it does not check what the disclosure says. The
survivorship guard is defeated three ways in committed code (F-008, open, with F-003
and F-016), so a report can carry a softened survivorship caveat. Nothing in Belay
detects lookahead. **This draft therefore does not claim a bound report is free of
either.** Whether the Paper Trading and capital rungs should stay closed until F-003,
F-008 and F-016 are closed is put to the owner (item 9). The capital rungs are closed
today on other grounds (rules 2 and 5).

**It resolves one level only.** It checks that each report exists, is unedited, is
about this strategy and says what it is. It does not re-open the report's own
inputs.

### Rule 4 — Every review outcome carries evidence, `Remain` included

**RULED (18c).** All four outcomes — `Promote`, `Remain Current Stage`, `Demote`,
`Retire` — carry at least one verifying evidence record, in both of `Remain`'s
senses: a promotion rejected, and a strategy kept on the stage it holds. Applied in
ADR-015 rule 4 (ADR-015 at `26f5d75`, lines 4700-4709).

**DRAFTER:** `review_artifact()`'s `evidence` parameter is required (ADR-015 at
`26f5d75`, lines 4726-4733).

**No grade floor on `Remain` — DRAFTER.** A `Remain` is not an upward move, so rule 1
does not reach it. Whether keeping a strategy on capital must meet the floor of the
rung it holds was not ruled (18c, "What it does not settle"). See "Put to the owner",
item 1.

### Rule 5 — The rungs that stay closed until a number is ruled

**RULED (18d): "Until the Committee rules a number, no strategy may enter `Micro
Capital`. A blank number closes the rung. It never means 'any length'."**
**RULED (25e): "Limited Capital and Production stay closed until a minimum live
duration is ruled, in the same way as Part 18d's minimum for paper trading."**
**RULED (26f): "The capital rungs stay closed until a human authorization can be
verified, not only declared."**

**DRAFTER — the mechanism.** Four module constants beside rule 1's table, each
`None`:

| Constant | Closes | Rests on |
|---|---|---|
| `MINIMUM_PAPER_TRADING = None` | every upward move into `Micro Capital` | 18d, 19c |
| `MINIMUM_MICRO_CAPITAL_DURATION = None` | every upward move into `Limited Capital` | 25e |
| `MINIMUM_LIMITED_CAPITAL_DURATION = None` | every upward move into `Production` | 25e |
| `HUMAN_AUTHORIZATION_VERIFIER = None` | every upward move into `Micro Capital`, `Limited Capital` and `Production`, and every confidence change on a capital stage (ADR-015 rule 3g, 26c) | 26f, 25f |

**The fourth constant is 26f's closure.** Rule 9's `human_authorization` is a
declaration: nothing in `framework/` authenticates who wrote it. 26f keeps the
capital rungs closed until it can be verified. `HUMAN_AUTHORIZATION_VERIFIER` is
filled only by an amendment of this ADR that names a verification mechanism — how an
authorization is checked against something the author of the review cannot produce
alone. **26f leaves the mechanism open ("How a human authorization is verified"), so
this draft proposes none.** A number or a name typed into the constant without that
amendment is a lowered bar, and rule 10's conformance test turns red.

While a constant is `None`, the validator refuses every upward move into the rung it
closes, with a message naming this rule and the Part. **The check needs nothing but
the review**, so ADR-015 rule 3c runs it on every read of a strategy (finding B3;
ADR-015 at `26f5d75`, lines 4274-4293). **`None` wins over any user setting** (rule
7). Filling a constant is an amendment to this ADR and a new `bar_version`, never a
code change a session makes. Its unit, and what report proves a duration, are
decided when it is filled. **No number is proposed here** (25, "What it does not
settle": "the live duration minimums in 25e"; 26, "What it does not settle": "How a
human authorization is verified").

### Rule 6 — Every promotion states how many variants were tried, and a count the hurdle cannot cover is refused

**RULED (18e):** "Every promotion states how many strategy variants were tried. A
promotion that leaves it blank is refused." **Every `Promote` is RULED, not a drafter
choice** (finding N2: the previous revision marked it DRAFTER). The count corrects
nothing; ADR-012 rule 10 (`docs/DECISIONS.md:2244-2250`) is unchanged.

**RULED (25h): "A `variants_tried` count above what the 3.0 hurdle covers is refused
until the owner rules on a correction."**

**RULED (26b): "The trial cap uses an overall false-positive rate of 5%. It is
computed from each significance report's own degrees of freedom, not from a fixed
count. It applies only where 25b's 3.0 hurdle applies: Paper Trading and the capital
rungs."**

A `Promote` review's `content` carries **`variants_tried`**. **DRAFTER — the checks**
(finding S4):

1. **An `int`, and not a `bool`.** `type(value) is int`, so `True` — which is an
   `int` in Python and passed an earlier revision's check (executed) — is refused.
   At least 1. **On every `Promote`** (18e).
2. **At most the cap, on an upward move into `Paper Trading`, `Micro Capital`,
   `Limited Capital` or `Production` only (26b).** Below those rungs, and into
   `Promotion Review`, there is no cap. *(Replaced 2026-09-25, second-pass finding
   2N8: this was a fixed `MAXIMUM_VARIANTS_TRIED = 18`, a number no Part ruled, derived
   from the normal tail although the test is Student's t, and applied to `Idea →
   Research` as well.)*
3. **At least the number of significance reports listed** in `reports_considered`
   (rule 3, 2N5).
4. **Never decreasing along the ladder.** `save()` refuses a `Promote` whose count is
   below the count on any earlier `Promote` review **named by a rung of the subject's
   ladder**.
5. **Following `Derived From` lineage, counting only the reviews each ladder names
   (second-pass finding 2N9).** A new identifier saved under ADR-015 rule 3g carries
   a `Derived From` edge to the strategy it came from. For each identifier in that
   ancestry, the counts considered are those on the `Promote` reviews named by the
   rungs of the ladder of the version **ADR-015's current-stage read returns** for
   it (ADR-015 at `26f5d75`, lines 4545-4691), and nothing else. `save()` refuses a
   `Promote` whose count is below the largest such count, plus one for each
   identifier between. A new identifier does not reset the count. This overcounts
   when several identifiers came from one batch of trials, which errs toward less
   capital. *(Changed 2026-09-25: this counted "any `Promote` review of any
   identifier in its `Derived From` ancestry", so one stored review about an
   ancestor, named by no ladder, with a count above the cap, froze every
   descendant.)*

**The cap (26b; the formula is DRAFTER).** For a significance report `r` with `n_r`
observations, `metric_artifact()` records `observations`
(`framework/metrics/reporting.py:219-222`), and the test has `df_r = n_r - 1`
degrees of freedom (`framework/metrics/statistics.py:41-45`, "with n-1 degrees of
freedom"). Let

    p_r = P(|T_{df_r}| > 3.0)     the two-sided Student's t tail at the 3.0 hurdle,
                                  computed by student_t_two_sided_p(3.0, df_r)
                                  (framework/metrics/distributions.py:120),
                                  the function statistics.py itself uses
    cap_r = floor(0.05 / p_r)     Bonferroni at an overall false-positive rate of 5%

and **the cap is the smallest `cap_r` over every significance report the review
lists** in `reports_considered`. ADR-015 rule 3c, which reads only the bound reports
(26e), applies it over those; `save()` and the sweep apply it over every listed one.
**Why each piece:**

- **Student's t, two-sided, `n - 1` degrees of freedom**, because that is the test
  `framework/metrics/statistics.py` runs and ADR-012 rule 4 rules it two-sided. The
  normal tail understates `p_r` at every finite sample, so the fixed 18 was too
  loose below about 860 observations.
- **3.0**, because 25h caps what "the 3.0 hurdle covers" and 22h makes 3.0 the
  minimum. A report tested against a stricter critical value still uses 3.0 here,
  which gives a smaller cap than its own value would (DRAFTER; toward less capital).
- **Bonferroni rather than Šidák** (DRAFTER). Bonferroni's cap is never larger,
  so it errs toward refusal.
- **The smallest over every listed report**, because a family of trials that
  includes a short one is more likely to have produced a lucky pass.

**Worked example, executed.** Command, run from the repository root on this branch:

    python -c "from framework.metrics.distributions import student_t_two_sided_p as p
    for n in (120, 252, 860, 2520):
        a = p(3.0, n - 1); print(n, n - 1, a, 0.05 / a, int(0.05 // a))"

Output:

    120 119 0.0032890643575484756 15.201891652028303 15
    252 251 0.00297154742571006 16.826250043124368 16
    860 859 0.002777775564536278 18.000014341816346 18
    2520 2519 0.0027262551966163785 18.34017595346768 18

So a review listing one significance report over ten years of daily data (2,520
observations, the span Part 22b requires) may state at most 18 variants; one whose
listing also holds a report over one year (252 observations) may state at most 16.
**No number here is a ruled constant.** The 5% and the 3.0 are ruled (26b, 25h);
the cap is computed from them and from each report, so there is no constant to fill.

Checks 1 and 2 need only the review and its bound reports, and run in ADR-015 rule
3c. Checks 3-5 read the listing, other reviews or other identifiers, and run in
`save()` and the sweep.

**`Derived From` is self-declared (2N9), stated.** Nothing checks that a new
identifier which carries rules from an old one names it. A new identifier that
leaves the edge out starts its count at whatever it states. ADR-015 rule 3g's
specification comparison runs only between versions of one identifier, so nothing
compares specifications across identifiers. The edge raises the cost of resetting
the count by one honest act and stops nothing dishonest.

**What is still not settled:** what counts as one "variant" (18e, "What it does not
settle"), and whether variants a user's AI generated and discarded are counted. The
count is self-reported; checks 3-5 make it harder to understate, not impossible.

### Rule 7 — Belay's bar is a floor no user setting can lower, and `None` beats every setting

**RULED (19c):** "Belay sets the minimums; users can only be stricter." **19c names
what the minimums are: "Belay's constitution and Part 18 are fixed minimums in the
product."** *(Finding B6: the previous revision said "Rules 1 to 6 are those
minimums", which is a drafter's restatement, not 19c's words.)* Part 25's rulings are
of the same kind, and this draft treats them as minimums too (DRAFTER).

**DRAFTER — which constants a user may not lower.** Every constant and every rule of
this ADR that implements the constitution, Part 18, Part 25 or Part 26: the rule 1
grades, rule 2's seven criteria and allowlists with their grades, rule 5's closures
(including 26f's), rule 6's cap and the 5% rate it is computed from, rule 8's
hurdle, rule 9's authorization.

**DRAFTER — the shape.** The effective bar for any check is the stricter of Belay's
and the user's, computed per rule: the higher grade, the larger duration, the smaller
cap on variants (a user may set a lower family rate, never a higher one), the higher
critical value.

**`None` wins over any user setting (finding S6).** "The stricter of" a closed rung
and a number is undefined, so it is defined here: **when Belay's constant is `None`,
the rung is closed, whatever the user has set.** 19c lets a user's Investment
Committee "set any number Belay leaves open, such as 18d's paper-trading length, on
the strict side of Belay's floor" — and 19c also says that until Belay's own minimum
exists, "18d keeps `Micro Capital` closed". A user's number counts only once Belay's
constant is a number, and only when it is stricter.

A user setting weaker than Belay's is refused when the settings are loaded, never
silently clamped: a clamp would hide from the user that their setting did nothing.
The ADR-012 amendment's DRAFTER item 1 refuses a weaker alpha the same way. No
settings mechanism exists in Belay today, so this rule binds whatever is built; it
builds nothing.

### Rule 8 — The Paper Trading rung and every capital rung rest on a significance report that passed at 3.0 and is adequate

**RULED (25b): "The Paper Trading rung and every capital rung rest on a significance
report that passed at a critical value of at least 3.0. It must also have enough
data, as amended ADR-012 defines."** Finding B5 (verdict).

**DRAFTER — the mechanism.** An upward move into `Paper Trading`, `Micro Capital`,
`Limited Capital` or `Production` binds, under rule 3, at least one report with
`metric` `statistical_significance` (on the capital rungs, the one listed under
"Statistical performance" in rule 2) whose `content` records:

1. `significant` is `true`;
2. **the critical value it was tested against is at least 3.0** — the value the
   amended ADR-012 rule 3 bounds (Part 22h; draft
   `docs/proposals/ADR-012-amendment-sample-adequacy-DRAFT.md`, "Rule 3, amended");
3. `sample_adequate` is `true` **under amended ADR-012 rule 8** (Part 22a-22g, 22i),
   **with every condition's floor, measured value and result recorded**, as that
   draft's DRAFTER item 7 requires. A report without those recorded conditions was
   produced before the amendment, when `sample_adequate` was the significance test
   restated (F-004), and it is refused;
4. `mean_return` is above `null_return_per_period` — DRAFTER: a result significant in
   the losing direction is not an edge.

**Where it runs.** On `save()` and `get()` of the review, in the sweep, and — RULED
(26e) — in ADR-015 rule 3c whenever a strategy's stage is read (ADR-015 at
`26f5d75`, lines 4260-4270).

**Consequence, stated.** The ADR-012 amendment is itself PROPOSED and unimplemented,
so no report today can carry item 3's record. **Until it is ratified and implemented,
nothing can enter `Paper Trading`.** That follows from 25b; it is not an extra rule.

**Not `Promotion Review`** — 25b names Paper Trading and the capital rungs. Whether
`Promotion Review` should also rest on one is put to the owner (item 8). A strategy
reaching it has already passed rule 8 at `Paper Trading`.

### Rule 9 — A human authorizes every capital rung, and an AI is never the approving reviewer

**RULED (25f): "A recorded human yes is required before any capital rung, and an AI is
never the approving reviewer of one."** Finding S7. Part 19c item 2: "record human
interraction evidence there" — what the human was shown, and what they decided.

**DRAFTER — the mechanism.** On an upward move into `Micro Capital`, `Limited Capital`
or `Production`, the REVIEW's `content` carries **`human_authorization`**, a mapping
with:

- `authorized_by` — a non-blank name, equal to the review's `reviewer`, so the
  approving reviewer is the human who said yes;
- `authorizer_kind` — exactly `"human"`. **`"ai"`, any other value, or its absence
  is refused.** This is the check that an AI is never the approving reviewer;
- `decision` — exactly `"yes"`. A no is recorded as a `Remain Current Stage` review,
  which rule 4 already requires to carry evidence;
- `shown` — a non-empty list of `(artifact_id, version, integrity_hash)`
  references to what the human was shown: at least every report bound under rule 3,
  and the recorded AI recommendation where there is one (19b item 3). Each resolves
  through `get()`, as in rule 3.

The first three need only the review and run in ADR-015 rule 3c; `shown` is resolved
on save and in the sweep.

**The same `human_authorization` authorizes a confidence change on a capital stage
— RULED (26c): "Changing a funded strategy's confidence needs a recorded human yes,
as in 25f."** ADR-015 rule 3g (ADR-015 at `26f5d75`, lines 4496-4521) requires it on
the `Remain Current Stage` review a capital-stage Revision names, and on the review
of an Append that changes confidence.

**A declared authorization does not open a capital rung — RULED (26f).** Rule 5's
`HUMAN_AUTHORIZATION_VERIFIER` is `None`, so every upward move into a capital rung
is refused whatever `human_authorization` says, until an amendment names how an
authorization is verified.

**Downward moves need no authorization** (DRAFTER): 25d, "It never refuses in a way
that would block a demotion", and 18b. A `Remain` that keeps capital deployed does
not either (DRAFTER; put to the owner, item 4).

**What this cannot do, stated.** `authorizer_kind` is a declaration, like the grade
letter, which is why 26f keeps it from opening capital on its own. Nothing in `framework/` authenticates an author; `review_artifact()` checks
only that `reviewer` is not blank (`framework/artifacts/review.py:123-124`). An AI
that writes `"human"` is refused by nothing but the record it leaves. What Belay must
record about a human decision is itself unruled beyond 19c item 2 (Required
Follow-Up item 1).

### Rule 10 — The bar has a version, and a raised bar applies from each strategy's next step

**RULED (25g): "A raised bar applies from each strategy's next step. It does not
re-judge past steps. No strategy holds capital today."** Finding S1.

**DRAFTER — the mechanism.**

- A module constant `BAR_VERSION`, starting at `1` on ratification, and a table of
  every ratified version's constants (rules 1, 2, 5, 6, 8). Every amendment of this
  ADR that changes a constant adds a version; none edits an old one.
- **Every review records `bar_version`**, on every outcome. `save()` accepts only the
  current version. A stored review is validated against the constants of the version
  it records — never against a later one — so raising a floor does not make an old
  review unreadable, and does not re-judge the step it bought (25g). An unknown
  version is refused.
- **`bar_version` never decreases along a ladder's reviews** (second-pass finding
  2N7). A review is refused when its `bar_version` is below that of any review named
  by an earlier rung of the subject's ladder. Without it, a hand-written review
  (which never passes through `save()`'s "current version only") could claim an
  older, laxer version of the bar. It reads other reviews, so it runs in `save()`
  and the sweep, not in ADR-015 rule 3c. **Limit, stated:** it cannot stop a
  forged review at the first rung of a ladder from naming an old version; while
  only version 1 exists there is nothing older to name.
- **A conformance test pins each version's constants to the ratified text** of this
  ADR, parsed from `docs/DECISIONS.md` once it lands there. A constant changed in
  code without an amendment turns the suite red, which is how a *lowered* bar is
  detected. **That test, not a promotion test, is what catches a `D` floor removed
  outright** (finding N4): nothing is below `D`, so no grade test can see the
  difference between a `D` floor and none.

---

## What these rules do not reach — trading outside Belay

**RULED (25j): "Trading done outside Belay, for example by a user's own connected AI,
is out of scope for these ADRs. Belay's documents state that limitation plainly."**

So, plainly: **every rule here governs what Belay records and what Belay acts on.**
None of it can stop a user, or a user's connected AI, from trading a strategy through
an account or a tool Belay does not control, at any size, whatever stage Belay reads.
A strategy closed at every capital rung by this ADR can still be traded outside it.
Reports produced outside Belay and never stored are invisible to rule 3's check 7
(and so are some produced inside it; rule 3, "The 'never stored' residual"). ADR-015
rule 8 (ADR-015 at `26f5d75`, lines 5068-5105) states the same limit for the capital
read. **`README.md` does not yet state this limit**, which 25j requires of "Belay's
documents"; that is Required Follow-Up item 13, left to a change that edits the
README.

---

## Which checks run where (findings B3 and 2N12)

ADR-015 rule 3c reads the last rung's review through the full validator, and — RULED
(26e) — resolves that review's bound reports and applies rule 8 (ADR-015 at
`26f5d75`, lines 4260-4293). The validator does no I/O. The checks that read other
reviews, the listing, or other identifiers run where the store is available.

| Check | Validator: on save, on `get()` of the review, and in ADR-015 rule 3c | Bound reports: on save, `get()` of the review, ADR-015 rule 3c (26e) and 3f | Store-wide: `save()` and ADR-015 rule 3f only |
|---|---|---|---|
| Rule 1 floor | yes | — | — |
| Rule 2 checks 1-4 | yes | — | — |
| Rule 2 checks 5-6 (distinct reports; allowlist and grade, 2N6) | — | yes | — |
| Rule 3 check 1 | yes | — | — |
| Rule 3 checks 2-6 on bound reports | — | yes | — |
| Rule 3 checks 2, 3, 5 on listed reports, and check 7 | — | — | yes |
| Rule 4 | yes | — | — |
| Rule 5 closures, including 26f's | yes | — | — |
| Rule 6 check 1 | yes | — | — |
| Rule 6 check 2 (the cap) | — | over bound significance reports | over every listed one |
| Rule 6 checks 3-5 | — | — | yes |
| Rule 8 | — | yes | — |
| Rule 9, all but `shown` | yes | — | — |
| Rule 9, `shown` | — | — | yes |
| Rule 10, the version is known | yes | — | — |
| Rule 10, never decreasing (2N7) | — | — | yes |

**The residual the previous revision stated here is gone, not reworded** (2N12,
26e). It was: "a forged review whose bound reports do not exist passes ADR-015 rule
3c". Rule 3c now resolves them. What is left to the sweep is the store-wide column:
a hand-written review whose listing leaves out a stored report, whose count is below
an earlier one, or whose `bar_version` goes down, passes rule 3c and is caught by
`save()` if it went through it and by the sweep if it did not. None of those can
reach capital today, because rule 5 closes every capital rung in the validator
column.

---

## Changes this makes to ADR-015 — every one, and where it was applied (findings B7 and 2N12)

Every row is applied on pull request #7's branch. **"Now" is ADR-015 at `26f5d75`**,
checked line by line against that commit for this revision (`git show
26f5d75:docs/DECISIONS.md`). Rows 1-17 are the 2026-09-24 revision's changes, whose
lines moved; rows 18-26 are this revision's. "Was" is where the first pass found the
text (its "PR7:" citations); "—" where the text is new.

| # | Change | Was (PR7:) | Now (lines) |
|---|---|---|---|
| 1 | Rule 4's table points at this ADR in every cell, now naming rule 6 on every row (26b) | 4248-4258 | 4827-4845 |
| 2 | Rule 4's paragraph making `Remain` optional replaced by 18c | 4185-4193 | 4700-4709 |
| 3 | Rule 4(a): `evidence` required, not defaulted | 4197-4200 | 4726-4733 |
| 4 | Rule 4(b): the construction refusal covers all four outcomes | 4201-4203 | 4734-4738 |
| 5 | Rule 5: `FIELDS` grows by this ADR's six keys, to nineteen (2N5 added `reports_considered`) | 4381-4382 | 4979-4985 |
| 6 | Rule 5: outcome-specific keys hold `None` where they do not apply, now including `reports_considered` and `human_authorization` on a confidence review | — | 4987-4997 |
| 7 | The three places to reconcile at ruling time, now each ruled | 4312-4333 | 4915-4924 |
| 8 | "Until it is filled… a single Level D record… satisfies it" | 4335-4339 | 4926-4929 |
| 9 | Test 21: four outcomes, twelve tests | 4518-4520 | 5176-5179 |
| 10 | Test 22: `Remain` with empty evidence refused, not saved | 4521-4522 | 5180-5184 |
| 11 | Tests 23a and 23b: run, not `xfail`; example moved to `Paper Trading` | 4526-4529 | 5188-5209 |
| 12 | Consequences: the signature grows by four, plus this ADR's six keys | 4622-4623 | 5430-5435 |
| 13 | Rejected Alternatives: "mandatory `evidence`" no longer rejected | 4729-4731 | 5578-5582 |
| 14 | Required Follow-Up: the bar is ruled; S12's claim corrected | 4755-4761 | 5638-5646 |
| 15 | Still Open: the bar and `Remain` items settled | 4786-4804 | 5688-5694 |
| 16 | Rule 3c reads the last review through the full validator (B3) | 4050-4051 | 4274-4293 |
| 17 | The Status block: what blocks ratification | 3622-3623 | 3622-3696 |
| 18 | Rule 3c resolves the last review's bound reports and applies rule 8 (26e, 2N12) | — | 4260-4270 |
| 19 | Rule 3c's cost against 9e(iii)'s "two extra reads", restated for the bound reports | — | 4295-4299 |
| 20 | Rule 3f: the "bound reports that do not exist" residual removed (26e) | — | 4461-4468 |
| 21 | Rule 3g: a confidence change on a capital stage needs rule 9's `human_authorization` (26c) and is closed by rule 5's verifier (26f) | — | 4496-4521 |
| 22 | Rule 3h: the subject index, shared with rule 3 check 7 | — | 4672-4679 |
| 23 | Rule 4: `bar_version` never decreases along a ladder (2N7, rule 10) | — | 4847-4856 |
| 24 | Rule 4(f): compares each bound report's data window (rule 3 check 6's `sample_period_start`) with the demotion's anchor (26d) | — | 4750-4801 |
| 25 | Residual risk: three files buy at most `Validation`, and a declared authorization does not open capital (26e, 26f) | — | 5490-5514 |
| 26 | Required Follow-Up: the subject index as required infrastructure | — | 5665-5669 |

## Tests this implies

Each is written red first, against the rule it names, and each asserts the named
refusal, never a bare exception type.

**Rule 1**

1. An upward move into each rung with evidence one grade below its floor is refused,
   naming the floor and the grade. The same move at the floor is accepted, for every
   row.
2. `Production → Limited Capital` and `Micro Capital → Paper Trading` with only a
   Level D record are **accepted** (18b).
3. A move to `Retired` from `Production` with one Level D record is accepted.

**Rule 2 (B4)**

4. **B4's executed attack**: one self-graded A record, source "I made this up", empty
   methodology, under all seven criteria, bound to one report. Refused, naming the
   repeated hash (check 3). With seven distinct records all bound to one report:
   refused naming the repeated report (check 5).
5. Six of seven criteria: refused naming the missing one. An eighth, unknown name:
   refused. A listed hash not on the artifact: refused.
6. A report whose `metric` is outside its criterion's allowlist (`cagr` under
   Risk-adjusted returns): refused naming both. Any report under Regime robustness:
   refused naming the empty allowlist.
6a. **2N6, the scratch model's scenario B.** Seven distinct records self-graded A,
   bound to seven hand-built REPORTs self-graded A, with all seven allowlists filled
   for the test: each report is refused naming its producing module and the grade it
   writes (C). The same reports graded C pass this check and are refused by rule 3
   check 4 instead (records A, reports C).

**Rule 3 (B5, S8, S14, S15)**

7. A qualifying record with no `evidence_reports` entry: refused.
8. An entry naming a report that is not stored: refused, by `save()` and by `get()`.
9. **S8.** A stored report edited on disk after storing, whose stored
   `integrity_hash` field still equals the reference: refused, because `get()`
   recomputes. A test that compared stored fields would pass it.
10. An entry naming an artifact whose `type` is not REPORT: refused.
11. **B5, grade.** A Level A record bound to a `metric_artifact()` report (graded C):
    refused naming both grades.
12. **B5, subject.** A report with no `subject_id`; one about another strategy; one
    whose `subject_integrity_hash` names no stored version, or a version whose ladder
    is not a prefix of the reviewed version's: each refused, naming the field.
13. **S14 and 2N5.** Two reports stored in the subject's range, one bound and the
    other neither bound nor listed: refused naming the unlisted one. With it listed
    and not bound: accepted, if rule 8 is met by the bound one. A failed report
    tagged with an **older** subject version on the ladder, left out of the listing:
    refused (the listing's range is check 5's). A stored junk report in range with a
    blank `known_limitations`, listed and not bound: accepted, because checks 4 and
    6 apply to bound reports only. A `Promote` listing three significance reports
    and stating `variants_tried: 2`: refused naming both numbers.
14. **S15.** A report whose `known_limitations` is blank: refused naming it.

**Rule 4**

15. A `Remain Current Stage` review with no evidence: refused (ADR-015 test 22).

**Rule 5 (18d, 25e, 26f)**

16. Every upward move into `Micro Capital`, `Limited Capital` and `Production` is
    refused while its constant is `None`, even with every other requirement met,
    naming the constant and the Part. Run through ADR-015 rule 3c as well
    (ADR-015 tests 49-50).
16a. **26f.** With every duration constant set in the test to a number, an upward
    move into each capital rung carrying a complete `human_authorization` is still
    refused, naming `HUMAN_AUTHORIZATION_VERIFIER` and 26f; and so is a capital-stage
    confidence Revision (ADR-015 test 59).

**Rule 6 (S4, 25h, 26b)**

17. `variants_tried` missing, `0`, `-1`, `"3"` and `True`: each refused on every
    `Promote`, `Idea → Research` included. `1` accepted.
17a. **26b, the cap.** Into `Paper Trading`, with one listed significance report of
    2,520 observations: `18` accepted, `19` refused naming the cap and the report's
    degrees of freedom (2,519). With a second listed report of 252 observations:
    `17` refused, `16` accepted. The expected caps are computed in the test from
    `student_t_two_sided_p`, not typed in, and the test also asserts them against the
    worked example's printed values, so a change to either side turns it red.
17b. **26b, where it applies.** `Idea → Research` and `Paper Trading → Promotion
    Review` with `variants_tried: 500`: not refused by the cap (no significance
    report is required there).
18. A `Promote` whose count is below an earlier `Promote`'s on the same ladder:
    refused, naming both counts.
19. A new identifier with a `Derived From` edge whose first `Promote` states a count
    at or below its ancestor's largest: refused, naming the ancestor.
19a. **2N9.** A stored `Promote` review about the ancestor, named by no rung of the
    ladder the ancestor's current-stage read returns, with `variants_tried: 10000`:
    it does not raise the descendant's lower bound.

**Rule 7 (S6)**

20. A user setting of any number for the paper-trading length, while
    `MINIMUM_PAPER_TRADING` is `None`: the rung stays closed. A user grade weaker than
    rule 1's: refused on load, never clamped.

**Rule 8 (25b)**

21. An upward move into `Paper Trading` with a bound significance report that has
    `significant: false`; one tested at a critical value below 3.0; one with no
    recorded adequacy conditions (a pre-amendment report); one significant with
    `mean_return` below the null: each refused, naming the item.

**Rule 9 (25f, S7)**

22. An upward move into `Micro Capital` with no `human_authorization`; with
    `authorizer_kind: "ai"`; with `decision: "no"`; with `authorized_by` different
    from `reviewer`: each refused, naming the field.
23. A demotion from `Limited Capital` into `Micro Capital` with no
    `human_authorization`: **accepted** (25d, 18b).

**Rule 10 (25g, S1, N4)**

24. A review stored under bar version 1 still validates after a hypothetical version
    2 raises a floor; a new review saved under version 1 is refused naming the current
    version; an unknown version is refused.
24a. **2N7.** Under a hypothetical version 2, a review at the second rung that records
    version 1 while the first rung's review records version 2: refused naming both.
25. **Mutation check, through the conformance test.** Changing any constant — a floor
    by one grade, **the `D` floor removed**, a criterion deleted, an allowlist
    widened or an entry's grade changed, a rule 5 constant filled (including
    `HUMAN_AUTHORIZATION_VERIFIER`), the 5% rate or the 3.0 in rule 6's cap raised —
    turns the conformance test red.

---

## Consequences

**Real money is closed for the foreseeable future, by the owner's choice.** Four of
rule 2's allowlists are empty: `python scripts/status.py` reports "promotion criteria
3 of 7 computable", and regime robustness, execution quality, liquidity and
operational consistency have no working module (`scripts/status.py:48-56`). Rule 5
closes all three capital rungs independently of that. Rule 1 needs Level B, which
needs a paper-trading engine that does not exist (`docs/ROADMAP.md:247`).

**`Paper Trading` is closed too, until the ADR-012 amendment is ratified and
implemented** (rule 8). **`Promotion Review` is effectively closed** until a report
graded B can be produced (rule 3 check 4), which also waits on a paper-trading
engine.

**Promotion gets heavier:** seven distinct reports on a capital rung, every stored
report about the strategy listed, a human authorization that must also be
verifiable, a non-decreasing variant count, and on `Paper Trading` and the capital
rungs a variant count no larger than the reports' degrees of freedom allow (26b).

**Capital also waits for a way to verify a human** (26f, rule 5). That is a fourth
closure, independent of the durations and of the four missing modules.

**Rules that are never exercised rot.** The proposal's author said so of its own
recommendation (section 9). The mitigation is the tests above: the suite exercises
every rule now, while nothing in production does.

### Residual risk, stated rather than buried

- **Grades, allowlisted metrics, the variant count and `authorizer_kind` are
  declarations.** Rule 3 ties each record to a real, unedited report about this
  strategy, no stronger than it. It does not prove the report is right.
- **A report can be produced to order.** Binding raises the cost of forging from
  typing a sentence to producing and storing a signed report about this strategy. It
  does not remove it.
- **Survivorship and lookahead are not checked** (rule 3, S15).
- **Trading outside Belay is not reached** (25j, above).
- **Trials that were never stored are invisible** (rule 3, "The 'never stored'
  residual"); only `variants_tried`, self-declared, records them.
- **`Derived From` is self-declared** (rule 6). Leaving it out resets the lineage.
- **Anyone who can write the store can deny capital**: stored significance reports
  raise `variants_tried`'s lower bound (rule 3), and ADR-015's forged downward rungs
  lower the read. Each is a denial of capital, never a grant.

---

## Rejected Alternatives

- **Putting the bar inside ADR-015.** The owner ruled against it (18g).
- **A parsed format inside `provenance`.** Turns free text into a hidden schema that
  every existing record silently fails to follow, and that `verify()` cannot tell
  apart from prose.
- **"A new `EvidenceRecord` field breaks the pinned digest" as a reason.** Withdrawn
  (S9): it does not, if the field is left out of the hashed payload when unset. The
  choice between the record and the REVIEW is open; see Context.
- **Clamping a weaker user setting up to Belay's minimum.** Hides from the user that
  their setting had no effect. Refusing it tells them.
- **Raising the hurdle for a large `variants_tried` instead of refusing it.** 25h
  chose refusal until a correction is ruled; ADR-012 rule 10 still applies none.
- **A fixed `MAXIMUM_VARIANTS_TRIED`.** The previous revision's 18 was derived from
  the normal tail, applied below `Paper Trading`, and was a number no Part ruled
  (2N8). 26b rules the cap computed from each report's degrees of freedom.
- **Binding every stored report**, as the previous revision did. One stored junk
  report blocked every promotion (2N5). Listing without binding keeps the disclosure
  and drops the veto.
- **Re-judging past promotions when the bar is raised.** 25g ruled against it.
- **A single report binding several criteria.** 25a rules seven distinct reports.

---

## Put to the owner at ratification — DRAFTER choices, not rulings

1. **`Remain` on capital:** no grade floor (rule 4). Alternative: the floor of the
   rung held.
2. **Report binding on downward moves and `Remain`:** not required (rule 3).
3. **Which records are bound:** every record on an upward move into `Paper Trading`
   or above, including `Promotion Review`, which 25a and 25b do not name (rule 3).
4. **Human authorization on a `Remain` that keeps capital deployed:** not required
   (rule 9).
5. **The mechanisms:** `criterion_evidence`, the allowlists and their grades,
   `evidence_reports`, `reports_considered`, report `subject_id` and
   `subject_integrity_hash`, the listing check, the `human_authorization` shape,
   `bar_version` and its non-decreasing rule.
6. **How rule 6's cap is computed from 26b's 5%:** Bonferroni rather than Šidák, at
   3.0 even for a report tested at a stricter value, and the smallest over every
   listed significance report (rule 6). *(Was: `MAXIMUM_VARIANTS_TRIED = 18`, removed
   under 26b.)*
7. **Weaker user settings are refused, not clamped**, and Part 25's rulings are
   minimums a user cannot lower (rule 7).
8. **Whether `Promotion Review` also rests on a rule 8 significance report.**
9. **Whether the Paper Trading and capital rungs stay closed until F-003, F-008 and
   F-016 (the survivorship surface) are closed** (rule 3, S15).
10. **Where the binding lives:** on the REVIEW, not the record (Context, S9).
11. **Where both ADRs land in `docs/DECISIONS.md`**, and in which order.
12. **Whether 25j covers trials that were never stored**; this draft reads it as
    not covering a backtest run with Belay's own code and discarded (rule 3).
13. **`variants_tried` at least the number of significance reports listed**, with
    its cost: a writer of the store can push the lower bound over the cap (rule 3).
14. **`Derived From` lineage counted through each ancestor's current-stage read**
    (rule 6, 2N9).

## Required Follow-Up (ADR-016)

1. **The shape of a recorded human decision** beyond rule 9's minimum (19c item 2).
2. **Recording the connected AI's recommendation once, never re-asking it** (19b
   item 3, `AGENTS.md` Determinism).
3. **Checking what a bound report measures**, so that the allowlist stops being a
   declared kind.
4. **Belay's own minimum paper-trading length** (19c), which fills
   `MINIMUM_PAPER_TRADING`.
5. **The live duration minimums** (25e), which fill the other two rule 5 constants.
6. **A correction for trial counts** (25h), which would replace rule 6's refusal.
7. **Whether an AI-made change to a user's gates needs that user's recorded yes**
   (19c).
8. **What counts as one variant** (18e).
9. **A store index by subject**, which rule 3's check 7 and ADR-015 rule 3h step 5
   need; derived from the store, never a separately maintained file. It is required
   infrastructure for both ADRs (ADR-015 at `26f5d75`, lines 5665-5669).
10. **`metric_artifact()` writes `subject_id` and `subject_integrity_hash`**, and the
    ADR-012 amendment's reported conditions (rule 8).
11. **Parts 25 and 26 merged to `main`**, and this draft revised again if either
    changes.
12. **A fresh independent pass** on this ADR and ADR-015 together. The owner's chosen
    different-AI pass on Issue #21 is still owed.
13. **`README.md` states 25j's limit** (second-pass finding 2N13). 25j requires that
    "Belay's documents state that limitation plainly", and the README, the first
    document a buyer reads, does not. It is not edited by this draft; the change that
    edits it says, in plain words, that Belay cannot stop trading done outside it,
    including by a user's own connected AI, whatever stage Belay reads.
14. **A way to verify a human authorization** (26f, "What it does not settle"), which
    fills `HUMAN_AUTHORIZATION_VERIFIER` and is the fourth thing capital waits for.
15. **`metric_artifact()` writes each module's grade as this ADR's allowlist states**,
    and the allowlist's conformance test reads both (rule 2, 2N6).

---

## Findings and rulings, and where each is resolved

**The first falsification pass (Issue #21).** Findings against ADR-015 alone are
resolved on pull request #7's branch and listed in ADR-015's revision history
(ADR-015 at `26f5d75`, lines 3771-3795 for this pass; lines 3797-3837 for the
second). The second column below names where each finding sits in this revision.

| Finding | Resolved here in | Also in ADR-015 at `26f5d75` |
|---|---|---|
| B1 | — | rule 3g, tests 39-43 |
| B2 | — | rules 3e, 3h, tests 44-47 |
| B3 | "Which checks need nothing but the review" | rules 3c, 3f, tests 48-51 |
| B4 | rule 2; test 4 | — |
| B5 | rule 3 checks 4-5 (grade, subject); rule 8 (verdict); tests 11, 12, 21 | — |
| B6 | the marks legend; rule 1; rule 7 | rule 7's "It is ruled" corrected |
| B7 | "Changes this makes to ADR-015" | all seventeen applied |
| S1 | rule 10; test 24 | rule 4, "Which ADR-016 version applies" |
| S2 | — | rule 3b, downward append; test 46 |
| S3 | rule 3 check 5 (makes it checkable) | rule 4(f); test 52 |
| S4 | rule 6; tests 17-19 | — |
| S5 | rule 5 | — |
| S6 | rule 7; test 20 | — |
| S7 | rule 9; tests 22-23 | — |
| S8 | rule 3 check 2; test 9 | — |
| S9 | Context; Rejected Alternatives | — |
| S10, S11, S12, S13 | — | rule 4; rule 8; Required Follow-Up; rule 2 step 6 |
| S14 | rule 3 check 7 and "The listing's range is exactly check 5's range"; test 13 | — |
| S15 | rule 3 check 6 and "What binding does not prove"; test 14; owner item 9 | — |
| N1, N3, N6 | — | Context; rule 5; rule 1 |
| N2 | rule 6 | — |
| N4 | rule 10; test 25 | rule 4, the note under the table |
| N5 | `main` merged into both branches | — |
| N7 | the "Where this lives" block; every ADR-015 citation | — |

**The owner's Part 25.**

| Ruling | Resolved here in | Also in ADR-015 at `26f5d75` |
|---|---|---|
| 25a Distinct evidence | rule 2 | — |
| 25b Part 22 joined to the ladder | rule 8 | — |
| 25c Fixed specification | rule 6 check 4 (`Derived From` lineage) | rule 3g |
| 25d Fail toward less capital | rule 3 (no binding on downward moves); rule 9 (no authorization on downward moves) | rules 3b, 3e, 3h, 8 |
| 25e Live rungs closed | rule 5 | rule 3c runs it (B3) |
| 25f A human authorizes capital | rule 9 | residual risk note |
| 25g Raised bar applies from next step | rule 10 | rule 4, "Which ADR-016 version applies" |
| 25h Refuse trial counts beyond the hurdle | rule 6 | — |
| 25i No reuse after a demotion | rule 3 check 5 (report subject position) | rule 4(f) |
| 25j Trading outside Belay out of scope | "What these rules do not reach" | rule 8 |

**The second pass (Issue #21, 2026-09-24).** Its labels N1-N13 are written 2N1-2N13
here, because the first pass used N1-N7.

| Finding | Resolved here in | Also in ADR-015 at `26f5d75` |
|---|---|---|
| 2N1, 2N2, 2N3, 2N4 | — (ADR-015's) | rule 3h (lines 4545-4691); rule 3c (lines 4247-4259); rule 3e (lines 4389-4432); tests 53-58 |
| 2N5 | rule 3: `reports_considered`, "The listing's range is exactly check 5's range", `variants_tried` at least the significance reports listed, "The 'never stored' residual"; test 13 | rule 5 (lines 4979-4997) |
| 2N6 | rule 2: the allowlist names each module and its grade; test 6a | — |
| 2N7 | rule 10, "never decreases"; test 24a | rule 4 (lines 4847-4856) |
| 2N8 | rule 6 check 2 and "The cap"; tests 17-17b | rule 4's table (lines 4827-4845) |
| 2N9 | rule 6 check 5 and "`Derived From` is self-declared"; test 19a | — |
| 2N10, 2N11 | — (ADR-015's) | rule 3g (lines 4496-4521); rule 4(f) (lines 4750-4801); tests 59-60 |
| 2N12 | "Which checks run where"; rule 8, "Where it runs" | rule 3c (lines 4260-4299); rule 3f (lines 4461-4468) |
| 2N13 | Required Follow-Up item 13 | — |
| nit: HANDOFF edited in place at 5683-5684 (`d592e7f`) | restored to `main`'s text on this branch, 2026-09-25 | — |
| nit: ADR-015 D15:4290, :3766, :3784 | — | revision history (lines 3797-3837) |

**The owner's Part 26.**

| Ruling | Resolved here in | Also in ADR-015 at `26f5d75` |
|---|---|---|
| 26a An unresolved downward step lowers the read only | — | rule 3h steps 4 and 6; rule 3e; rule 4(f) |
| 26b The trial cap at 5%, from each report's degrees of freedom, only where 3.0 applies | rule 6 | rule 4's table |
| 26c Confidence on a capital stage needs a human yes | rule 9, and rule 5's verifier closes it | rule 3g |
| 26d 25i's evidence means the data | rule 3 check 6 supplies the window | rule 4(f) |
| 26e Reading a stage re-checks its evidence | "Which checks run where"; rule 8 | rule 3c |
| 26f Capital waits for verification | rule 5 (`HUMAN_AUTHORIZATION_VERIFIER`); rule 9 | residual risk (lines 5490-5514) |

**How this revision was checked.** The second pass's executable model was extended
to encode both ADRs' revised rules as worded, using the real `Artifact`,
`EvidenceRecord`, `ArtifactIntegrity.sign`, `ArtifactValidator`,
`ArtifactRepository` and `student_t_two_sided_p`. It is a scratch model written by
the author, not in the repository and not an independent pass. Against it: scenario
A (one made-up record bound to `RPT-0001`) is refused on nine grounds; B (seven
self-graded A reports, every allowlist filled) is refused by 2N6 on all seven and,
independently, by rule 5; C raises (zero capital); C2 reads `Paper Trading`,
flagged; D reads `Retired`, flagged, with the honest version still the frontier and
nothing in rule 4(f)'s index; E prints the caps in rule 6's worked example; F reads
`Paper Trading` after the demoted version file is deleted and `Production` only when
its review is deleted too, which is ADR-015's stated residual. It also found one
defect in ADR-015's first wording of the fix for 2N1, recorded in ADR-015 rule 3h.
