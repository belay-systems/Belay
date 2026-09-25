# DRAFT — ADR-016: The Evidence Bar — What Evidence Buys Each Rung, And What No User Setting Can Lower

Status:
**PROPOSED — drafted from owner rulings, revised 2026-09-24 after a falsification
pass and the owner's Part 25, 2026-09-25 after a second pass and the owner's Part 26,
again 2026-09-25 after a third pass and the owner's Part 27, and a last time
2026-09-25 after a fourth pass and the owner's Part 28, then for the owner's Part 32
(rule 10 and the passages that depend on it). Not ratified. Not implemented in any
part.**

Date:
2026-09-22 (revised 2026-09-24, 2026-09-25, and three more times on 2026-09-25)

---

> **Where this lives, and why here.** ADR-015 is PROPOSED and lives only on public
> pull request #7's branch, `adr/015-stage-is-carried`, not on `main`. This draft
> fills ADR-015 rule 4's table, so it cannot be appended to `docs/DECISIONS.md` on
> `main` without citing an ADR that is not there. It is kept here, beside
> `docs/proposals/ADR-014-rule-5-amendment-DRAFT.md`, until the owner rules where
> both ADRs land.
>
> **ADR-015 is now cited by line** (finding N7): as "ADR-015 at `ddda627`, lines
> n-m", meaning DECISIONS.md under docs/ on branch `adr/015-stage-is-carried` at
> commit ddda627. *(Repointed in the fifth revision from `61789bc`, which had
> replaced `26f5d75` and `94815a2`.)* The file name and line numbers are written without backticks on
> purpose: the file on this branch is `main`'s, where ADR-015 does not exist, and the
> repository's citation test would read them against the wrong file. They go stale when that
> branch changes; repoint them when it does.

> **What changed for Part 32 (2026-09-25).** The three readings Part 31 left open
> were put to the owner, who ruled **Part 32** (on branch `claude/great-turing-v2d0x8`
> until it merges). **32a, "Today's bar"**, overrules 25g's "It does not re-judge past
> steps": rule 10 now judges every stored review by the current version's constants,
> so a raised bar lowers a strategy's read at once, with its cost stated; test 24 is
> rewritten to match, and ADR-015 rule 4's "Which ADR-016 version applies" is
> rewritten line for line (Changes rows 36-38). **32b**: rule 6 says 25h and 26b amend
> 18e. **32c**: item 12 of "Put to the owner at ratification" requires the fresh pass
> on the text as ratified. Nothing else is redesigned (32, "Session readings").

> **What changed in the fifth revision (2026-09-25).** A fourth pass (Issue #21, the
> comment "Fourth supplementary pass: ADR-015 at `61789bc` (#7), ADR-016 at `7855303`
> (#20)") again found nothing blocking of its own in this draft ("ready after fixes";
> it cannot be ratified before ADR-015). Its blocking F4-3 was shared: ADR-015 rule 5
> forbade the `human_authorization` that this draft's rule 9 and ADR-015 rule 3h
> require on supersessions and repair reviews, and this draft's Changes row 6 missed
> it. The owner then ruled **Part 28 (28a-28e), 2026-09-25: "aligned, yes to the
> plan"**. 28e makes this the final text round, with no redesign; the current-stage
> read is then built as code with every Issue #21 attack as a test that must fail, and
> both ADRs are conformed to the code. This revision:
> - adds the F4-3 row to "Changes this makes to ADR-015" (row 32), with rows 33-35 for
>   28a-28c, and a test (22a);
> - applies 28b to rule 5's verifier and rule 9 (a repair or supersession that raises
>   a funded strategy's confidence), 28a to rule 9 (the review at a pending demotion's
>   position names it and carries a yes), and 28c to rule 9 (a re-anchoring repair);
> - states 28d in rule 6 check 5, with a visited set on the `Derived From` walk and
>   3N16's cost (F4-9);
> - adds the Implementation item 18 to the Required Follow-Up (28e);
> - repoints every ADR-015 citation to `ddda627`.
>
> **What changed in the fourth revision (2026-09-25, kept as history).** A third pass (Issue #21, the
> comment "Third supplementary pass: ADR-015 at `26f5d75` (#7), ADR-016 at `34844d6`
> (#20)") again found nothing blocking of its own in this draft, calling it "ready
> after fixes". It cannot be ratified before ADR-015. Against this draft it found
> should-fix 3N4, 3N7 and 3N8, and nits 3N11, 3N13, 3N14 and 3N16. The owner then
> ruled **Part 27 (27a-27g), 2026-09-25: "aligned"**. This revision:
> - applies the allowlist, and the check of the grade the producing module writes,
>   to every bound report on every rung that binds reports (3N4, rule 3 check 8);
> - refuses a report whose data window ends after the report was made (3N5, rule 3
>   check 6);
> - states the cost of short significance reports, refuses a report of fewer than
>   two observations as a significance report, and counts distinct report
>   identifiers (3N7, rule 6);
> - counts each ancestor's listed significance reports in the lineage floor (3N8), and
>   refuses a promotion when an ancestor's read raises (3N16);
> - records trials run and never stored as a stated residual of this ADR (RULED 27c);
> - uses rule 9's authorization for the supersessions and repairs ADR-015 now allows
>   (27d, 27g);
> - repoints every ADR-015 citation to `61789bc` and adds this revision's rows to
>   "Changes this makes to ADR-015".
>
> 27a (which supersedes 26d), 27b, 27e and 27f are applied in ADR-015. The scratch
> models that checked these rules are described under "Findings and rulings".
>
> **What changed in the first 2026-09-25 revision (kept as history).** A second pass on the redrafts
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
> - **Parts 25-28 are recorded on branch `claude/kind-knuth-9g7xlr` and are not yet
>   on `main` or on this branch.** Every rule below that cites 25x, 26x, 27x or 28x
>   rests on that record. If it does not reach `main` as written, those rules
>   revert to DRAFTER. **27a supersedes 26d**; where 26d is mentioned below, it is
>   marked superseded.
> - **Only Parts 18, 19, 22, 23 and 25-28 are cited as RULED.** Anything else
>   is DRAFTER, and every number no Part rules is `None`, which keeps its rung closed.

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
> claimed and landed, point 4) requires one before anything is called verified. A
> fresh session satisfies it; a different AI is welcome, never waited for (Part 30b).

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
then **Part 26** after the second pass; **on 2026-09-25, Part 27** after the third.

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

**RULED (18a, 18b).** This fills ADR-015 rule 4's table (ADR-015 at `ddda627`, lines
5338-5356).

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

**Direction is computed exactly as ADR-015 rule 4 drafts it** (ADR-015 at `ddda627`,
lines 5382-5415): a move to `Retired` is classified first and is never upward;
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
   second-pass finding 2N6). Rule 3 check 8 applies the second half to every bound
   report on every rung that binds reports. Check 6 adds that the metric must be in
   *this criterion's* list.

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
   `:227-231`); **or its window ends after the report's own `created`**, or starts
   after it ends (DRAFTER; third-pass finding 3N5). The window is declared, because
   `significance_artifact()` takes `sample_period` separately from `returns`
   (`framework/metrics/statistics.py:307-316`). A window that ends after the report
   was made states data the report cannot have had. After 27a the window gates one
   thing, ADR-015 rule 4(f)'s paper-or-live check, and that rule states the
   residual;
7. **a stored report in the subject's range is not listed** (finding S14, below).
   `save()` applies this to the store as it is at the save. **The sweep applies it as
   of each review** (DRAFTER; third-pass nit 3N11): a report counts only if its
   `created` is at or before the review's. Without that, every report stored after a
   review would make the old review fail the sweep;
8. **a bound report's grade is not the grade its producing module writes** (DRAFTER;
   third-pass finding 3N4). Its `metric` must name an entry of rule 2's allowlist, in
   any criterion, and its `evidence_level`, as the validator re-derives it, must equal
   that entry's grade. This applies on **every rung that binds reports**, `Paper
   Trading`, `Promotion Review` and the capital rungs, not only the capital ones.
   Under the previous revision it ran only inside rule 2, so three files and
   hand-built reports that graded themselves `B` bought `Promotion Review`, whose
   floor is `B`. Now a record bound to a report is no stronger than the report (check
   4), the report is no stronger than its module writes (this check), and no
   allowlisted module writes `B`. So `Promotion Review` stays closed until one does.

**Checks 4, 6 and 8, and rule 2's checks 5 and 6, apply only to bound reports.** A
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
was tested, **counted once per `report_id`**: the versions of one report are one trial
(DRAFTER; third-pass finding 3N7). A report of fewer than two observations is **not a
significance report** for this count or for rule 6's cap (rule 6). A `Promote` whose
`variants_tried` is smaller is refused, naming both numbers. This is what makes the listing bite: a failed trial that is stored is
counted, whether or not the review binds it. **The cost, stated:** anyone who can
write the store can store significance reports about a strategy and so push its
lower bound above rule 6's cap, which refuses the promotion. That is a denial of
capital, not a grant.

**Cost, stated:** check 7 needs a listing of the store by subject, which the
repository does not have (`framework/artifacts/repository.py:69-84` lists one
identifier's versions). It is the subject index ADR-015 rule 3h also needs (ADR-015
at `ddda627`, lines 5104-5111), derived from the store and never a separately
maintained file. Required Follow-Up.

**The "never stored" residual — named, and not closed (2N5). RULED (27c): "Unsaved
trials are a stated gap in the evidence bar, not a 25j matter. A trial run but never
stored is a stated residual of ADR-016. Follow-up: Belay's own tools store every run
automatically."** Check 7 sees only what is stored with a subject in range. Three
kinds of trial escape it: a report computed and never saved; a report saved with no
`subject_id`, or with one that names no version in range; and a computation run with
other software. Nothing in Belay can see any of them. Only `variants_tried` records
them, and it is self-declared (rule 6). **This is a residual of this ADR, not a 25j
matter** (27c), and it is listed under "Residual risk". The follow-up 27c names,
Belay's own tools storing every run automatically, is Required Follow-Up item 16. It
closes the first kind for runs made with Belay's own code. It does not close the other
two. *(Replaced in the fourth revision: this paragraph read 25j as not covering the
residual "in part" and put the question to the owner as item 12. 27c answered it.)*

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
ADR-015 rule 4 (ADR-015 at `ddda627`, lines 5140-5149).

**DRAFTER:** `review_artifact()`'s `evidence` parameter is required (ADR-015 at
`ddda627`, lines 5166-5173).

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
| `HUMAN_AUTHORIZATION_VERIFIER = None` | every upward move into `Micro Capital`, `Limited Capital` and `Production` (26f, 25f); every repair or supersession that raises a funded strategy's confidence (28b); and, DRAFTER, every other confidence change on a capital stage (ADR-015 rule 3g, 26c) and every supersession or repair that raises the read into a capital stage (ADR-015 rule 3h, 27d, 27g) | 26f, 25f, 28b; the other extensions DRAFTER |

**The fourth constant is 26f's closure.** Rule 9's `human_authorization` is a
declaration: nothing in `framework/` authenticates who wrote it. 26f keeps the
capital rungs closed until it can be verified. **26f names the capital rungs.
Extending the closure to capital-stage confidence changes, and to raises into a
capital stage by supersession or repair, is the drafter's reading** (third-pass nit
3N13). The reading is that each one moves capital as a promotion does (26c, 27g).
**One of them is now ruled — RULED (28b): "A repair or supersession that raises a
funded strategy's confidence needs the verified human yes of 26f, like any other
confidence change on a capital stage (26c)."** Fourth-pass finding F4-4: a repair
raised a funded strategy's confidence on a declared yes, while a Revision making the
same change needed the verifier. `HUMAN_AUTHORIZATION_VERIFIER` is
filled only by an amendment of this ADR that names a verification mechanism — how an
authorization is checked against something the author of the review cannot produce
alone. **26f leaves the mechanism open ("How a human authorization is verified"), so
this draft proposes none.** A number or a name typed into the constant without that
amendment is a lowered bar, and rule 10's conformance test turns red.

While a constant is `None`, the validator refuses every upward move into the rung it
closes, with a message naming this rule and the Part. **The check needs nothing but
the review**, so ADR-015 rule 3c runs it on every read of a strategy (finding B3;
ADR-015 at `ddda627`, lines 4464-4483). **`None` wins over any user setting** (rule
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

**RULED (32b): 25h and 26b amend 18e.** The owner chose "Yes, say it amends 18e",
whose text was: "The count still corrects no result, but a count above the cap is
refused." 18e's "The count corrects nothing and claims nothing" still holds of the
result; it no longer holds of the promotion, which the count can now block.

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
3. **At least the number of significance reports listed** in `reports_considered`,
   counted once per `report_id` (rule 3, 2N5, 3N7).
4. **Never decreasing along the ladder.** `save()` refuses a `Promote` whose count is
   below the count on any earlier `Promote` review **named by a rung of the subject's
   ladder**.
5. **Following `Derived From` lineage, counting only the reviews each ladder names
   (second-pass finding 2N9).** A new identifier saved under ADR-015 rule 3g carries
   a `Derived From` edge to the strategy it came from. For each identifier in that
   ancestry, the counts considered are those on the `Promote` reviews named by the
   rungs of the ladder of the version **ADR-015's current-stage read returns** for
   it (ADR-015 at `ddda627`, lines 4801-5131), and nothing else. **Each ancestor
   also contributes the number of distinct significance-report identifiers in its
   range** (rule 3 check 5's range, taken for the version its read returns; DRAFTER,
   third-pass finding 3N8). Without it, an ancestor's failed trials that were listed
   and never bound were dropped at the new identifier. An ancestor's value is the
   larger of its largest named count and its distinct significance reports. `save()`
   refuses a `Promote` whose count is below the largest ancestor's value, plus one for
   each identifier between. A new identifier does not reset the count. This overcounts
   when several identifiers came from one batch of trials, which errs toward less
   capital. **If an ancestor's current-stage read raises, the `Promote` is refused**
   (DRAFTER; third-pass nit 3N16): its count cannot be established, and reading it as
   zero would be the reset this check exists to stop. **The cost, stated (fourth-pass
   nit F4-9):** one forged file under an ancestor whose `parent_hash` names nothing
   makes that ancestor's read raise, and then every descendant's `Promote` is refused
   until a person sets the file aside with a repair review about the ancestor. **The
   ancestry is walked with a visited set** (DRAFTER; F4-9): each identifier is read
   once, and an edge to one already visited ends that branch, so a cycle of `Derived
   From` edges cannot loop. **A Retired strategy may be re-registered and climb again
   — RULED (28d): "A Retired strategy may be re-registered and climb again, carrying
   its lineage (27e) and every bar that follows it. The ADRs say so."** Its new
   identifier's `Derived From` edge names the retired one (ADR-015 rule 3g), so this
   check carries the retired identifier's count to it, as it does for any ancestor.
   *(Changed 2026-09-25: this
   counted "any `Promote` review of any identifier in its `Derived From` ancestry", so
   one stored review about an ancestor, named by no ladder, with a count above the
   cap, froze every descendant.)*

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

**Short reports, and fewer than two observations — third-pass finding 3N7. DRAFTER.**
- **Fewer than two observations is not a significance report.** At one observation
  the test has zero degrees of freedom, and `student_t_two_sided_p` refuses it
  ("a single observation supports no test",
  `framework/metrics/distributions.py:120-140`). `significance()` cannot produce such
  a report, so only a hand-built one exists. It is refused as a significance
  report: it cannot be bound under rule 8, and it counts toward neither the cap nor
  check 3. It is still listed, because every report in range is listed (rule 3 check
  7).
- **The cost of a short report, stated.** The cap is the smallest over every listed
  report, so one short report sets it. Executed with the same function:

      observations    2 (df    1): cap 0
      observations    4 (df    3): cap 0
      observations   10 (df    9): cap 3
      observations   30 (df   29): cap 9

  At four observations or fewer the cap is 0, and every upward move into `Paper
  Trading` or a capital rung is refused **for that identifier, for good**, because
  the report stays listed. That follows from 26b's "computed from each significance
  report's own degrees of freedom": a trial at 3 degrees of freedom has a two-sided
  tail above 5% at 3.0 on its own, so no family containing it meets 5%. **The way
  out is a new identifier** with a `Derived From` edge, and with the same
  specification digest it must name the original anyway (ADR-015 rule 3g, 27e). Its
  count starts at the ancestor's value (check 5), which includes the short report as
  one trial. Its cap is set by its own reports only. **So the short report's large
  tail stops counting at the new identifier, which errs toward more capital, and is
  stated.** The alternative is to carry ancestors' listed reports into the cap too.
  Then one short report locks every descendant for good, and no honest strategy that
  once ran a four-day test could ever reach `Paper Trading`. Put to the owner (item
  15).

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
`ddda627`, lines 4450-4460).

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
as in 25f."** ADR-015 rule 3g (ADR-015 at `ddda627`, lines 4704-4744) requires it on
the `Remain Current Stage` review a capital-stage Revision names, and on the review
of an Append that changes confidence.

**A declared authorization does not open a capital rung — RULED (26f).** Rule 5's
`HUMAN_AUTHORIZATION_VERIFIER` is `None`, so every upward move into a capital rung
is refused whatever `human_authorization` says, until an amendment names how an
authorization is verified.

**The same `human_authorization` authorizes a supersession or a repair that raises
the read — RULED (27d, 27g).** ADR-015 rule 3h steps 5 and 6 require it on a review
that names a stored downward review in `supersedes` and would raise the read by doing
so, and on every repair review. On a raise into a capital stage, rule 5's verifier
must also pass it (DRAFTER; 3N13). *(Added in the fifth revision:)* **RULED (28a):**
an upward rung cancels a pending stored `Demote` or `Retire` only when the review at
that position names it and carries this authorization, at any stage. **RULED
(28b):** a repair or supersession that raises a funded strategy's confidence needs
rule 5's verifier too. **RULED (28c):** a repair review carrying it may correct a
mistaken or future-dated demotion date, which re-anchors ADR-015 rule 4(f). **The
key is allowed on any review whose `supersedes` is not empty** (ADR-015 rule 5;
fourth-pass finding F4-3). Before this revision ADR-015 rule 5 refused it there, so
every repair and every raising supersession this rule authorizes was refused.

**Downward moves need no authorization** (DRAFTER): 25d, "It never refuses in a way
that would block a demotion", and 18b. A `Remain` that keeps capital deployed does
not either (DRAFTER; put to the owner, item 4).

**What this cannot do, stated.** `authorizer_kind` is a declaration, like the grade
letter, which is why 26f keeps it from opening capital on its own. Nothing in `framework/` authenticates an author; `review_artifact()` checks
only that `reviewer` is not blank (`framework/artifacts/review.py:123-124`). An AI
that writes `"human"` is refused by nothing but the record it leaves. What Belay must
record about a human decision is itself unruled beyond 19c item 2 (Required
Follow-Up item 1).

### Rule 10 — The bar has a version, and every read judges every step by today's bar

**RULED (32a), overruling 25g's "It does not re-judge past steps".** Asked which
bar a stage read judges each past step by, the owner chose **"Today's bar"**, whose
text was: "Every read re-judges every past step against the current bar, so raising
the bar immediately drops any strategy that no longer meets it." **RULED (25g), the
words that stand:** "A raised bar applies from each strategy's next step. [...] No
strategy holds capital today." Finding S1.

**DRAFTER — the mechanism.**

- A module constant `BAR_VERSION`, starting at `1` on ratification. Every amendment
  of this ADR that changes a constant (rules 1, 2, 5, 6, 8) adds a version. The code
  holds the current version's constants only; an earlier version's are in the text
  of the amendment that replaced them.
- **Every review records `bar_version`**, on every outcome: the version it was saved
  under, kept as a record. `save()` accepts only the current version. A version the
  code does not know, or one above the current version, is refused.
- **Every stored review is judged by the current version's constants**, on every
  read (ADR-015 rule 3c) and in every sweep (ADR-015 rule 3f), never by the version
  it records (32a). A raised floor therefore lowers a strategy's read at once: a
  review that no longer meets it fails 3c, and the read falls to the lowest stage it
  can establish, as for any review that fails (25d). The strategy climbs back only
  through new reviews that meet today's bar. A lowered bar also applies at once; the
  conformance test below is what makes a lowering visible. *(Replaced 2026-09-25 by
  32a: the previous text judged each review by the version it records, so a raised
  bar applied only from each strategy's next step.)*
- **The cost, stated (32a).** Raising any constant can take a strategy off its
  stage, a capital stage included, as soon as code carrying the new constant runs.
  No strategy holds capital today (25g). Downward moves carry no bar (rule 1), so a
  raised bar never blocks a demotion.
- **`bar_version` never decreases along a ladder's reviews** (second-pass finding
  2N7). A review is refused when its `bar_version` is below that of any review named
  by an earlier rung of the subject's ladder. **Under 32a it no longer decides which
  bar applies**, because every review is judged by today's. It is kept as a check
  on the record: `save()` accepts only the current version, so only a hand-written
  file can break the order, and the sweep then names it. It reads other reviews, so
  it runs in `save()` and the sweep, not in ADR-015 rule 3c. *(The previous text's
  "Limit, stated", that a forged first-rung review could name an older, laxer
  version, no longer applies: a review naming an older version is judged by
  today's constants all the same.)*
- **A conformance test pins the current version's constants to the ratified text** of this
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
rule 8 (ADR-015 at `ddda627`, lines 5631-5672) states the same limit for the capital
read. **`README.md` does not yet state this limit**, which 25j requires of "Belay's
documents"; that is Required Follow-Up item 13, left to a change that edits the
README.

---

## Which checks run where (findings B3 and 2N12)

ADR-015 rule 3c reads the last rung's review through the full validator, and — RULED
(26e) — resolves that review's bound reports and applies rule 8 (ADR-015 at
`ddda627`, lines 4450-4483). The validator does no I/O. The checks that read other
reviews, the listing, or other identifiers run where the store is available.

**On a capital stage the current-stage read runs the first two columns on every
version back to `Idea`, not only the last — RULED (27f)**, in ADR-015 rule 3h step 3
(ADR-015 at `ddda627`, lines 4801-5131). The store-wide column still runs only in
`save()` and the sweep.

| Check | Validator: on save, on `get()` of the review, and in ADR-015 rule 3c | Bound reports: on save, `get()` of the review, ADR-015 rule 3c (26e) and 3f | Store-wide: `save()` and ADR-015 rule 3f only |
|---|---|---|---|
| Rule 1 floor | yes | — | — |
| Rule 2 checks 1-4 | yes | — | — |
| Rule 2 checks 5-6 (distinct reports; allowlist and grade, 2N6) | — | yes | — |
| Rule 3 check 1 | yes | — | — |
| Rule 3 checks 2-6 and 8 on bound reports (check 8: 3N4) | — | yes | — |
| Rule 3 checks 2, 3, 5 on listed reports, and check 7 (in the sweep, as of each review: 3N11) | — | — | yes |
| Rule 4 | yes | — | — |
| Rule 5 closures, including 26f's | yes | — | — |
| Rule 6 check 1 | yes | — | — |
| Rule 6 check 2 (the cap) | — | over bound significance reports | over every listed one |
| Rule 6 checks 3-5 (check 5 with each ancestor's significance reports, 3N8, and refused when an ancestor's read raises, 3N16) | — | — | yes |
| Rule 8 | — | yes | — |
| Rule 9, all but `shown` | yes | — | — |
| Rule 9, `shown` | — | — | yes |
| Rule 9 on a supersession or repair review (27d, 27g) | yes | — | — |
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

Every row is applied on pull request #7's branch. **"Now" is ADR-015 at `ddda627`**,
checked line by line against that commit for this revision (`git show
ddda627:docs/DECISIONS.md`). Rows 1-17 are the 2026-09-24 revision's changes, rows
18-26 the first 2026-09-25 revision's, rows 27-31 the fourth revision's, rows
32-35 the fifth revision's, and rows 36-38 the Part 32 revision's; the lines of the earlier rows moved and are repointed. "Was" is where the first pass found the
text (its "PR7:" citations); "—" where the text is new.

| # | Change | Was (PR7:) | Now (lines) |
|---|---|---|---|
| 1 | Rule 4's table points at this ADR in every cell, now naming rule 6 on every upward row (26b; the `Retired` row names rule 1 only, third-pass nit 3N14) | 4248-4258 | 5338-5356 |
| 2 | Rule 4's paragraph making `Remain` optional replaced by 18c | 4185-4193 | 5140-5149 |
| 3 | Rule 4(a): `evidence` required, not defaulted | 4197-4200 | 5166-5173 |
| 4 | Rule 4(b): the construction refusal covers all four outcomes | 4201-4203 | 5174-5178 |
| 5 | Rule 5: `FIELDS` grows by this ADR's six keys, to nineteen (2N5 added `reports_considered`), and to twenty with ADR-015's `supersedes` (27d) | 4381-4382 | 5490-5497 |
| 6 | Rule 5: outcome-specific keys hold `None` where they do not apply, now including `reports_considered` and `human_authorization` on a confidence review | — | 5532-5551 |
| 7 | The three places to reconcile at ruling time, now each ruled | 4312-4333 | 5426-5435 |
| 8 | "Until it is filled… a single Level D record… satisfies it" | 4335-4339 | 5437-5440 |
| 9 | Test 21: four outcomes, twelve tests | 4518-4520 | 5743-5746 |
| 10 | Test 22: `Remain` with empty evidence refused, not saved | 4521-4522 | 5747-5751 |
| 11 | Tests 23a and 23b: run, not `xfail`; example moved to `Paper Trading` | 4526-4529 | 5755-5776 |
| 12 | Consequences: the signature grows by four, plus this ADR's six keys | 4622-4623 | 6141-6146 |
| 13 | Rejected Alternatives: "mandatory `evidence`" no longer rejected | 4729-4731 | 6320-6324 |
| 14 | Required Follow-Up: the bar is ruled; S12's claim corrected | 4755-4761 | 6401-6409 |
| 15 | Still Open: the bar and `Remain` items settled | 4786-4804 | 6472-6478 |
| 16 | Rule 3c reads the last review through the full validator (B3) | 4050-4051 | 4464-4483 |
| 17 | The Status block: what blocks ratification | 3622-3623 | 3622-3766 |
| 18 | Rule 3c resolves the last review's bound reports and applies rule 8 (26e, 2N12) | — | 4450-4460 |
| 19 | Rule 3c's cost against 9e(iii)'s "two extra reads", restated for the bound reports | — | 4485-4489 |
| 20 | Rule 3f: the "bound reports that do not exist" residual removed (26e) | — | 4669-4676 |
| 21 | Rule 3g: a confidence change on a capital stage needs rule 9's `human_authorization` (26c) and is closed by rule 5's verifier (26f); compared with the read's confidence (27b, 3N3) | — | 4704-4744 |
| 22 | Rule 3h: the subject index, shared with rule 3 check 7 | — | 5104-5111 |
| 23 | Rule 4: `bar_version` never decreases along a ladder (2N7, rule 10) | — | 5358-5367 |
| 24 | Rule 4(f): rebuilt on 27a (26d superseded). A climb back binds a paper or live report whose grade rule 3 check 8 fixes, with a window rule 3 check 6 allows; each ancestor is read as rule 6 check 5 reads it (27e) | — | 5190-5312 |
| 25 | Residual risk: three files buy at most `Validation`, now true of `Promotion Review` too because of rule 3 check 8 (3N4), and a declared authorization does not open capital (26e, 26f) | — | 6211-6249 |
| 26 | Required Follow-Up: the subject index as required infrastructure | — | 6440-6444 |
| 27 | Rule 3b: an upward Append sets aside a stored downward review only when rule 9 allows its review to supersede it (3N2, 27d, 27g) | — | 4405-4416 |
| 28 | Rule 3h step 5: a supersession that raises the read carries rule 9's `human_authorization`, and on a capital stage passes rule 5's verifier (27d, 27g) | — | 4879-4952 |
| 29 | Rule 3h step 6: the repair review carries rule 9's `human_authorization`, with rule 5's verifier on a raise into a capital stage (27g, 3N10) | — | 4953-5021 |
| 30 | Rule 5: `supersedes`, the key 27d's save rule reads | — | 5499-5530 |
| 31 | Required Follow-Up: the repair review and `supersedes`, the paper-and-live module that derives its window, and the specification digest index | — | 6445-6453 |
| 32 | Rule 5: `human_authorization` may also be set on a review whose `supersedes` is not empty, which covers every repair review and every supersession that raises the read, so the validator no longer refuses what rule 9 and rule 3h require (fourth-pass finding F4-3; 27d, 27g). It was lines 5357-5358 at `61789bc` | — | 5537-5549 |
| 33 | Rule 3h step 5: an upward rung cancels a pending stored `Demote` or `Retire` only when its review names it and carries rule 9's `human_authorization`, passing rule 5's verifier on a capital stage (28a, F4-10) | — | 4894-4924 |
| 34 | Rule 3h steps 5 and 6: a supersession or repair that raises a capital-stage confidence passes rule 5's verifier (28b, F4-4) | — | 4916-4920, 4993-5001 |
| 35 | Rule 4(f): a repair review carrying rule 9's `human_authorization` re-anchors a mistaken or future-dated demotion date (28c, F4-6) | — | 5224-5239 |
| 36 | Rule 4, "Which ADR-016 version applies": every read and every sweep judges every stored review by the current version's constants, and a raised bar lowers the read at once; the non-decreasing `bar_version` is kept as a check on the record (32a, rule 10). Same lines as row 23, rewritten line for line | — | 5358-5367 |
| 37 | The Status line: revised once more, for Part 32 | — | 3623 |
| 38 | Required Follow-Up: Part 32 is the record not yet on `main` (Parts 25-28 merged with #31); a fresh session satisfies the independent pass, a different AI is never waited for (30b), and 32c adds one on the text as ratified | — | 6421-6423, 6427-6428 |

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
6b. **3N4.** Three files bringing a strategy to `Promotion Review`, the review binding
   a hand-built `sharpe_ratio` report graded `B`: refused by rule 3 check 8, naming
   `framework/metrics/risk_adjusted.py` and the grade it writes (C). The same at
   `Paper Trading`. The test fails if check 8 is moved back inside rule 2.
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
13a. **3N11.** The sweep over a store in which a report was stored in the subject's
    range after a review was saved, and is not in that review's listing: the sweep
    does not flag the review. A report stored before the review and left out: it
    does.
14. **S15.** A report whose `known_limitations` is blank: refused naming it.
14a. **3N5.** A bound report whose `sample_period_end` is after its own `created`:
    refused naming both dates.

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
17c. **3N7, fewer than two observations.** A hand-built significance report with
    `observations: 1` listed beside a good one: the review is not refused for it,
    the cap is the good report's, and it does not count toward check 3. Bound under
    rule 8, it is refused, naming 3N7.
17d. **3N7, distinct identifiers.** Two versions of one significance report listed:
    check 3's lower bound counts one. A report of four observations listed: the cap
    is 0 and an upward move into `Paper Trading` is refused naming it. The test's
    docstring says this is the stated cost, and names the way out (a new identifier,
    `Derived From`).
17b. **26b, where it applies.** `Idea → Research` and `Paper Trading → Promotion
    Review` with `variants_tried: 500`: not refused by the cap (no significance
    report is required there).
18. A `Promote` whose count is below an earlier `Promote`'s on the same ladder:
    refused, naming both counts.
19. A new identifier with a `Derived From` edge whose first `Promote` states a count
    at or below its ancestor's largest: refused, naming the ancestor.
19b. **3N8.** An ancestor with three significance reports listed in its range, none
    bound, and a largest named count of 1: a descendant's first `Promote` stating 3
    is refused (the floor is 3 + 1), and 4 is accepted.
19c. **3N16.** A descendant whose ancestor's current-stage read raises: its
    `Promote` is refused, naming the ancestor.
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
22a. **F4-3.** A repair review, and a `Demote` naming a stored `Retire`, each
    carrying `human_authorization`: accepted by the validator. A `Remain Current
    Stage` review naming nothing and carrying one: refused, naming ADR-015 rule 5. A
    repair review raising a `Limited Capital` strategy's confidence with a declared
    authorization that the test verifier does not pass: the read's confidence is
    unchanged (28b; ADR-015 tests 74 and 77).
23. A demotion from `Limited Capital` into `Micro Capital` with no
    `human_authorization`: **accepted** (25d, 18b).

**Rule 10 (32a, 25g, S1, N4)**

24. **32a.** A strategy at `Micro Capital` whose reviews met version 1: under a
    hypothetical version 2 that raises `Micro Capital`'s floor above that review's
    grade, the current-stage read falls to the lowest stage it can establish below
    `Micro Capital`, with no new file written. The same strategy under version 1
    reads `Micro Capital` (the mutation: judging by the recorded version keeps it
    there). A new review saved under version 1 is refused naming the current
    version; an unknown version is refused.
24a. **2N7.** Under a hypothetical version 2, a review at the second rung that records
    version 1 while the first rung's review records version 2: refused naming both,
    by `save()` and by the sweep.
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
implemented** (rule 8). **`Promotion Review` is closed** until an allowlisted module
writes a report graded B: a bound record is no stronger than its report (rule 3
check 4), and the report no stronger than its module writes (rule 3 check 8). That
also waits on a paper-trading engine. *(Corrected in the fourth revision, third-pass
finding 3N4: this said "effectively closed … (rule 3 check 4)", which was false while
a hand-built report could grade itself B. Check 8 makes it true.)* **So does every
climb back above `Paper Trading` after a demotion** (ADR-015 rule 4(f), 27a), which
needs a paper or live report written after it.

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
- **Trials that were never stored are invisible** — RULED (27c) a stated residual of
  this ADR (rule 3, "The 'never stored' residual"); only `variants_tried`,
  self-declared, records them, until Belay's own tools store every run
  automatically (Required Follow-Up item 16).
- **A short significance report closes `Paper Trading` for its identifier** (rule
  6, 3N7), and a new identifier escapes its tail while keeping its count.
- **A paper or live report's dates are declared** until the module that writes it
  derives them (ADR-015 rule 4(f), 27a; Required Follow-Up item 17).
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
- **Judging each step by the bar of its time.** The previous revision did this,
  on 25g's words. 32a ruled against it: every read uses today's bar.
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
12. ~~**Whether 25j covers trials that were never stored**; this draft reads it as
    not covering a backtest run with Belay's own code and discarded (rule 3).~~
    **Settled by 27c**: a residual of this ADR, not a 25j matter.
13. **`variants_tried` at least the number of significance reports listed**, with
    its cost: a writer of the store can push the lower bound over the cap (rule 3).
14. **`Derived From` lineage counted through each ancestor's current-stage read**
    (rule 6, 2N9), now including each ancestor's distinct significance reports (3N8),
    and refused when an ancestor's read raises (3N16).
15. **Short reports** (rule 6, 3N7). A report of fewer than two observations is
    not a significance report. Distinct report identifiers are counted. The cap
    stays the smallest over the reports listed on this identifier only, so a short
    report closes `Paper Trading` for its identifier and a new identifier escapes its
    tail. The alternative carries ancestors' reports into the cap, and then a short
    report locks every descendant for good.
16. **Rule 3 check 8 on every rung that binds reports** (3N4), and check 6's refusal
    of a window that ends after `created` (3N5).
17. **Check 7 in the sweep, as of each review** (3N11).
18. **Rule 5's verifier also closing capital-stage confidence changes and raises
    into a capital stage by supersession or repair** (3N13). *(Fifth revision: a
    repair or supersession that raises a funded strategy's confidence is now RULED,
    28b. The rest stays DRAFTER.)*
19. **The visited set on the `Derived From` walk**, and the stated cost of 3N16's
    refusal: one forged file under an ancestor blocks every descendant until a repair
    (rule 6 check 5, F4-9).

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
   infrastructure for both ADRs (ADR-015 at `ddda627`, lines 6440-6444).
10. **`metric_artifact()` writes `subject_id` and `subject_integrity_hash`**, and the
    ADR-012 amendment's reported conditions (rule 8).
11. **Parts 25-28 merged to `main`**, and this draft revised again if any
    changes.
12. **A fresh independent pass** on this ADR and ADR-015 together, on the exact text
    to be ratified, after 28e's step 2 has conformed both to the code, and right
    before ratification (18g, confirmed by 32c). A fresh session satisfies it; a
    different AI is welcome, never waited for (30b).
13. **`README.md` states 25j's limit** (second-pass finding 2N13). 25j requires that
    "Belay's documents state that limitation plainly", and the README, the first
    document a buyer reads, does not. It is not edited by this draft; the change that
    edits it says, in plain words, that Belay cannot stop trading done outside it,
    including by a user's own connected AI, whatever stage Belay reads.
14. **A way to verify a human authorization** (26f, "What it does not settle"), which
    fills `HUMAN_AUTHORIZATION_VERIFIER` and is the fourth thing capital waits for.
15. **`metric_artifact()` writes each module's grade as this ADR's allowlist states**,
    and the allowlist's conformance test reads both (rule 2, 2N6).
16. **Belay's own tools store every run automatically** — RULED (27c) as the
    follow-up to the "never stored" residual. Every significance computation made
    with Belay's code is stored with its subject, so check 7 sees it and it counts
    toward `variants_tried`'s lower bound.
17. **A module that writes paper and live reports, deriving each report's window
    from the timestamps of the observations it recorded** (ADR-015 rule 4(f), 27a;
    3N5). It is what closes the declared-date residual, and until it exists no report
    is graded B or A.
18. **Implementation — RULED (28e): "The current-stage read is then built as code.
    Every attack from the falsification passes on Issue #21 becomes a test that must
    fail, and the ADRs describe what the code does."** This revision is 28e's final
    text round. ADR-015's current-stage read is built next, with the checks of this
    ADR that it runs (rule 3c's column and the bound-reports column of "Which checks
    run where"). Every attack from the Issue #21 passes against this draft (B4-B6,
    2N5-2N9, 3N4, 3N7, 3N8, 3N16, and F4-3's shared half) is written first as a test
    that fails by design against the unchanged code, beside tests 1-25. This ADR is
    then conformed to the code in a later change, and any disagreement is recorded.
    The code is capital-path code: it lands through review like any other and opens
    no capital rung, because every rung stays closed by rule 5's `None` constants
    (28, "What it does not settle").

---

## Findings and rulings, and where each is resolved

**The first falsification pass (Issue #21).** Findings against ADR-015 alone are
resolved on pull request #7's branch and listed in ADR-015's revision history
(ADR-015 at `ddda627`, lines 3841-3865 for this pass; lines 3867-3901 for the
second; lines 3903-3944 for the third). The second column below names where each
finding sits in this revision.

| Finding | Resolved here in | Also in ADR-015 at `ddda627` |
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

| Ruling | Resolved here in | Also in ADR-015 at `ddda627` |
|---|---|---|
| 25a Distinct evidence | rule 2 | — |
| 25b Part 22 joined to the ladder | rule 8 | — |
| 25c Fixed specification | rule 6 check 5 (`Derived From` lineage) | rule 3g |
| 25d Fail toward less capital | rule 3 (no binding on downward moves); rule 9 (no authorization on downward moves) | rules 3b, 3e, 3h, 8 |
| 25e Live rungs closed | rule 5 | rule 3c runs it (B3) |
| 25f A human authorizes capital | rule 9 | residual risk note |
| 25g Raised bar applies from next step; "does not re-judge past steps" overruled by 32a | rule 10 | rule 4, "Which ADR-016 version applies" |
| 25h Refuse trial counts beyond the hurdle | rule 6 | — |
| 25i No reuse after a demotion | rule 3 check 5 (report subject position); rule 3 check 8 (the grade that makes a report paper or live, for 27a) | rule 4(f) |
| 25j Trading outside Belay out of scope | "What these rules do not reach" | rule 8 |

**The second pass (Issue #21, 2026-09-24).** Its labels N1-N13 are written 2N1-2N13
here, because the first pass used N1-N7.

| Finding | Resolved here in | Also in ADR-015 at `ddda627` |
|---|---|---|
| 2N1, 2N2, 2N3, 2N4 | — (ADR-015's) | rule 3h (lines 4801-5131); rule 3c (lines 4437-4449); rule 3e (lines 4585-4640); tests 53-58 |
| 2N5 | rule 3: `reports_considered`, "The listing's range is exactly check 5's range", `variants_tried` at least the significance reports listed, "The 'never stored' residual"; test 13 | rule 5 (lines 5490-5551) |
| 2N6 | rule 2: the allowlist names each module and its grade; test 6a | — |
| 2N7 | rule 10, "never decreases"; test 24a | rule 4 (lines 5358-5367) |
| 2N8 | rule 6 check 2 and "The cap"; tests 17-17b | rule 4's table (lines 5338-5356) |
| 2N9 | rule 6 check 5 and "`Derived From` is self-declared"; test 19a | — |
| 2N10, 2N11 | — (ADR-015's) | rule 3g (lines 4704-4744); rule 4(f) (lines 5190-5312); tests 59-60 |
| 2N12 | "Which checks run where"; rule 8, "Where it runs" | rule 3c (lines 4450-4489); rule 3f (lines 4669-4676) |
| 2N13 | Required Follow-Up item 13 | — |
| nit: HANDOFF edited in place at 5683-5684 (`d592e7f`) | restored to `main`'s text on this branch, 2026-09-25 | — |
| nit: ADR-015 D15:4290, :3766, :3784 | — | revision history (lines 3867-3901) |

**The owner's Part 26.**

| Ruling | Resolved here in | Also in ADR-015 at `ddda627` |
|---|---|---|
| 26a An unresolved downward step lowers the read only | — | rule 3h steps 4 and 6; rule 3e; rule 4(f) |
| 26b The trial cap at 5%, from each report's degrees of freedom, only where 3.0 applies | rule 6 | rule 4's table |
| 26c Confidence on a capital stage needs a human yes | rule 9, and rule 5's verifier closes it | rule 3g |
| 26d 25i's evidence means the data — **superseded by 27a** | rule 3 check 6 supplies the window; since 27a it gates only the paper-or-live check | rule 4(f), rebuilt on 27a |
| 26e Reading a stage re-checks its evidence | "Which checks run where"; rule 8 | rule 3c |
| 26f Capital waits for verification | rule 5 (`HUMAN_AUTHORIZATION_VERIFIER`); rule 9 | residual risk (lines 6211-6249) |

**The third pass (Issue #21, 2026-09-25).** Its labels are written 3N1-3N17 here.

| Finding | Resolved here in | Also in ADR-015 at `ddda627` |
|---|---|---|
| 3N1, 3N2, 3N3, 3N5, 3N6, 3N9, 3N10, 3N12, 3N15, 3N17 | — (ADR-015's), but rule 9 authorizes the supersessions and repairs (27d, 27g), and rule 3 check 6 refuses a window that ends after `created` (3N5) | rule 3h (lines 4801-5131); rule 3b (lines 4336-4416); rule 3g (lines 4704-4799); rule 4(f) (lines 5190-5312); rule 5 (lines 5499-5530); tests 61-73 |
| 3N4 | rule 3 check 8; "Which checks run where"; Consequences; test 6b | residual risk (lines 6211-6249) |
| 3N7 | rule 3 (counted once per `report_id`); rule 6 check 3 and "Short reports, and fewer than two observations"; tests 17c-17d; owner item 15 | — |
| 3N8 | rule 6 check 5 (each ancestor's significance reports); test 19b | — |
| 3N11 | rule 3 check 7 (the sweep, as of each review); test 13a | — |
| 3N13 | rule 5 (the fourth constant's extensions marked DRAFTER) | — |
| 3N14 | this table (25c's row names check 5); "Changes this makes to ADR-015", row 1 | — |
| 3N16 | rule 6 check 5 (refused when an ancestor's read raises); test 19c | rule 4(f) (lines 5190-5312) |

**The owner's Part 27.**

| Ruling | Resolved here in | Also in ADR-015 at `ddda627` |
|---|---|---|
| 27a A climb back needs new paper or live evidence; backtests reuse history (supersedes 26d) | rule 3 checks 6 and 8 supply the window rule and the grade | rule 4(f) (lines 5190-5312) |
| 27b Keep `current_stage`; it reports the approved confidence | — | rule 3h; rule 3g; rule 8 |
| 27c Unsaved trials are a residual of this ADR | rule 3, "The 'never stored' residual"; Residual risk; Required Follow-Up item 16 | — |
| 27d A later review names what it supersedes | rule 9 (a supersession that raises) | rule 3h step 5; rule 5 (`supersedes`) |
| 27e The bar follows a strategy across identifiers | rule 6 check 5 (its ancestors) | rule 4(f); rule 3g (the specification digest) |
| 27f Reading a capital stage verifies the whole chain | "Which checks run where" (rule 3c's checks on every version of a capital read) | rule 3h step 3 |
| 27g Raising a stage is a capital decision | rule 9 (a repair review); rule 5 (a raise into a capital stage) | rule 3h step 6 |

**The fourth pass (Issue #21, 2026-09-25).** Its labels are F4-1 to F4-10.

| Finding | Resolved here in | Also in ADR-015 at `ddda627` |
|---|---|---|
| F4-3 | "Changes this makes to ADR-015", row 32; rule 9 ("The key is allowed on any review whose `supersedes` is not empty"); test 22a | rule 5 (lines 5537-5549); test 74 |
| F4-1, F4-2, F4-5, F4-6, F4-7, F4-8, F4-10 | — (ADR-015's) | rules 3e, 3g, 3h, 4(f) and 5; tests 75-81; revision history (lines 3946-3986) |
| F4-4 | rule 5 (the verifier, 28b); rule 9; test 22a | rule 3h steps 5 and 6 (lines 4916-4920, 4993-5001); test 77 |
| F4-9 | rule 6 check 5 (a visited set; 3N16's cost); owner item 19 | rule 3h ("Cost, stated"); rule 4(f); test 83 |

**The owner's Part 28.**

| Ruling | Resolved here in | Also in ADR-015 at `ddda627` |
|---|---|---|
| 28a A hand-written upward step cannot cancel a pending demotion | rule 9 | rule 3h step 5 (lines 4894-4924); test 80 |
| 28b A repair or supersession raising capital confidence needs 26f's verifier | rule 5; rule 9; test 22a | rule 3h steps 5 and 6; test 77 |
| 28c A wrong date is repairable | rule 9 | rule 4(f) (lines 5224-5239); test 79 |
| 28d A Retired strategy may be re-registered | rule 6 check 5 | rule 3g; test 82 |
| 28e How it is finished | the Status block; Required Follow-Up item 18 | Status block; Required Follow-Up ("Implementation") |
| 32a Today's bar: every read judges every step by the current constants | rule 10; test 24 | rule 4, "Which ADR-016 version applies" (lines 5358-5367) |
| 32b 25h and 26b amend 18e | rule 6 | — |
| 32c 18g's fresh pass stands, on the text as ratified | Put to the owner at ratification, item 12 | Required Follow-Up (lines 6427-6428) |

**How the fifth revision was checked.** The fourth pass's own abstract model of
ADR-015, extended with both ADRs' fifth-revision rules as worded, and run under the
hypothetical bar. It is a scratch model written by the author, not in the repository
and not an independent pass. What it showed for this draft's share: a repair review
carrying `human_authorization` passes rule 5's key rule, and a `Remain` naming
nothing does not (F4-3); a repair raising a `Limited Capital` strategy's confidence
from `0.3` to `0.5` is ignored on a declared yes and applied on a verified one (F4-4,
28b). The rest is in ADR-015's revision history.

**How the fourth revision was checked (kept as history).** Two scratch models, neither in the
repository and both written by the author, so neither is an independent pass. One is
the third pass's own abstract model (X1-X6); the other is the previous revision's
model, which uses the real framework classes. Both were extended with this
revision's rules as worded, and each was run under today's bar and under a
**hypothetical** bar with rule 5's constants filled and a verifier for 26f. Against
them: A is refused on nine grounds; a `Promotion Review` bought with a hand-built
report graded `B` is refused by rule 3 check 8, naming `risk_adjusted.py` and C
(3N4); the caps print as in rule 6, with 0 at four observations and a refusal at one;
C raises; C2, C3 and D read `Paper Trading` or `Retired`, flagged; F reads `Paper
Trading` until both files are deleted. Under today's bar nothing reaches a capital
stage. Under the hypothetical bar, X1 re-climbs to `Production` and X1b to `Micro
Capital` once a person records a yes. An honest strategy climbs `Idea` to `Promotion
Review`, is demoted, is refused a re-climb on paper evidence from before the
demotion, and climbs back on paper evidence from after it.

**How the first 2026-09-25 revision was checked (kept as history).** The second pass's executable model was extended
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
