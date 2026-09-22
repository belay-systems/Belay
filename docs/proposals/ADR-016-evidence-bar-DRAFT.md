# DRAFT — ADR-016: The Evidence Bar — What Evidence Buys Each Rung, And What No User Setting Can Lower

Status:
**PROPOSED — drafted from owner rulings, not ratified. Not implemented in any part.**

Date:
2026-09-22

---

> **Where this lives, and why here.** ADR-015 is PROPOSED and lives only on public
> pull request #7's branch, `adr/015-stage-is-carried`, not on `main`. This draft
> fills ADR-015 rule 4's empty table, so it cannot be appended to
> `docs/DECISIONS.md` on `main` without citing an ADR that is not there. It is kept
> here, beside `docs/proposals/ADR-014-rule-5-amendment-DRAFT.md`, until the owner
> rules where both ADRs land. ADR-015 is cited by description, never by line.

> **What the owner ruled, and what the drafter chose.** Every rule below carries
> one of two marks:
>
> - **RULED** — the owner's ruling, cited to `docs/OwnerDecisions.md` Part 18 or
>   19, where the owner's words are quoted.
> - **DRAFTER** — a choice this draft makes to turn a ruling into something code can
>   check. The owner has not seen or ruled it. Each one is listed again under
>   "Put to the owner at ratification".
>
> Nothing marked DRAFTER may be read as ruled.

> **Nothing here has had an independent pass.** `AGENTS.md` (How work is claimed
> and landed, point 4) requires one before anything is called verified, and every
> ADR in `docs/DECISIONS.md` that had a second reader lost claims to it. The next
> step is that pass, told to falsify this draft.

---

## Context

**ADR-015 closes F-007 and F-014 and leaves one hole open on purpose.** Its rule 4
requires every stage move to carry evidence, and reserves an empty table for the
minimum grade each rung needs. Until that table is filled, "a single Level D
record, `constitution/Evidence_Standards.md:31-35`, 'Hypothesis. Research only.',
satisfies it for a promotion into real capital." The owner blocked ADR-015's
ratification on researching a bar first. The research is
evidence-bar-per-rung.md under docs/proposals/ on pull request #7's branch (not on
`main`, so named without backticks). It ended in seven questions.

**On 2026-09-22 the owner answered all seven** (`docs/OwnerDecisions.md` 18a-18g)
and, while answering, stated that Belay is a product for others: bought,
downloaded, and connected to the buyer's own AI, with a human saying yes or no to
each recommendation (Part 19). Part 19c ruled that Belay's rules are minimums no
user can lower.

**18g ruled that the bar is its own decision record**, so that it can change
without reopening how the ladder works. This is that record.

**What the rulings demand that nothing in Belay can check today:**

1. **ADR-015's gate reads one grade.** Rule 4's check is `strongest_evidence_level`
   (`framework/artifacts/enums.py:29-43`) compared against a table. It cannot count
   records or see what any record is about, so 18a's "one record per criterion" has
   no mechanism.
2. **An evidence record's `provenance` is free text**
   (`framework/artifacts/evidence.py:12-18`). Its seal proves the record is
   unedited, not that anything it names exists (18f).
3. **`EvidenceRecord` cannot gain a field.** Its hashed payload is pinned by a
   literal digest (`tests/artifacts/test_evidence_hashing.py:18`). A new field
   would stop historical evidence verifying.
4. **No REVIEW has ever been stored.** ADR-015 rule 5 verified that only
   `artifacts/RPT-0001/1.0.0.yaml` was ever committed, so REVIEW `content` is still
   free to change. After the first review is saved, every change is a migration of
   permanent records.

Points 3 and 4 together decide where this ADR puts everything new: **on the REVIEW's
signed `content`, never on `EvidenceRecord`.**

---

## Decision

### Rule 1 — The floor per rung, upward moves only

**RULED** (18a, 18b). This fills ADR-015 rule 4's table.

| Rung reached (`to_stage`) | Minimum `EvidenceLevel` — upward moves only | Also required on this rung |
|---|---|---|
| Research | D | — |
| Validation | D | — |
| Paper Trading | C | rule 3 binding |
| Promotion Review | B | rule 3 binding |
| Micro Capital | B | rule 2 criterion coverage; rule 3 binding; rule 5 closure |
| Limited Capital | A | rule 2 criterion coverage; rule 3 binding |
| Production | A | rule 2 criterion coverage; rule 3 binding |
| Retired | no floor — a retirement is never upward | — |

**Direction is computed exactly as ADR-015 rule 4 already drafts it**: a move to
`Retired` is classified first and is never upward; otherwise a move is upward when
`STRATEGY_LADDER.index(to_stage) > STRATEGY_LADDER.index(from_stage)`
(`framework/artifacts/enums.py:107-109`). Grades compare through
`EVIDENCE_STRENGTH` (`framework/artifacts/enums.py:21-26`), never through
declaration order.

**Why these grades.** They are the proposal's option 3: each rung needs the grade
the last evidence-producing stage before it is defined to produce. That mapping is
an inference from names, which the proposal states in its section 9 and the owner
ruled knowingly. Level A on `Limited Capital` is not a deadlock: `Micro Capital`
trades real capital, and so produces Level A (`Knowledge/EvidenceRegistry.md:9`).

### Rule 2 — On the three capital rungs, one record per promotion criterion

**RULED** (18a). An upward move into `Micro Capital`, `Limited Capital` or
`Production` carries, for **each** of the seven criteria of
`constitution/Promotion_Pipeline.md:75-81`, at least one evidence record at or
above that rung's floor. The list is exactly:

> Statistical performance · Risk-adjusted returns · Drawdown behavior · Regime
> robustness · Execution quality · Liquidity · Operational consistency

The spellings in `strategies/PromotionCriteria.md` and `Validation/CapitalReview.md`
do not change the list (18a).

**DRAFTER — the mechanism.** The REVIEW's `content` gains a key
**`criterion_evidence`**: a mapping from each of the seven criterion names, spelled
as above, to a non-empty list of evidence-record hashes. The check refuses the
review unless:

1. all seven names are present, and no other name;
2. every listed hash is the `hash` of a record in the review's `Artifact.evidence`;
3. for each criterion, at least one listed record's `level` meets the rung's floor.

**What this does not check, stated so nobody assumes it does:** that a record is
*about* the criterion it is listed under. That is the reviewer's declaration,
signed and attributable, and nothing more. Rule 3 makes it a declaration about a
real, stored report. Checking a report's topic is Required Follow-Up item 3.

### Rule 3 — Qualifying evidence names a stored, signed report

**RULED** (18f): each qualifying record names a stored, signed report by
identifier, version and integrity hash, and Belay refuses a record whose report
does not resolve or whose hash does not match.

**DRAFTER — which records qualify.** Every evidence record on an **upward** move
whose destination is `Paper Trading` or above. That is where the proposal placed it
(its section 7), and where Level C or better is required, so a stored report can
exist. Records on `Research` and `Validation` promotions are Level D notes with no
report behind them. Records on downward moves (18b) and on `Remain` (18c) are not
bound by this draft; see "Put to the owner", item 2.

**DRAFTER — the mechanism.** The REVIEW's `content` gains a key
**`evidence_reports`**: a mapping from each qualifying evidence record's `hash` to
three strings, `report_id`, `report_version` and `report_integrity_hash`. This is
ADR-015 rule 1's three-part reference, the same shape one level down. On `save()`
and on `get()`, the repository resolves each reference and refuses the review when:

- a qualifying record has no entry;
- the named artifact does not exist at that version;
- its `type` is not REPORT;
- its stored `integrity_hash` differs from `report_integrity_hash`.

It resolves one level only. It checks that the report exists and is unedited. It
does not re-open the report's own inputs. That bound matches ADR-015 rule 3c, which
the owner selected as "Yes, check on load".

**Why on the REVIEW and not on the record** (Context points 3 and 4): a new
`EvidenceRecord` field breaks the pinned digest, and a parsed format inside
`provenance` would turn a free-text field into a hidden schema that old records do
not follow. REVIEW `content` is still free to change and already signed.

### Rule 4 — Every review outcome carries evidence, `Remain` included

**RULED** (18c). ADR-015 rule 4 requires evidence for `Promote`, `Demote` and
`Retire` and leaves `Remain Current Stage` optional as the drafter's judgement.
**That optional is replaced: all four outcomes carry at least one verifying
evidence record**, in both of `Remain`'s senses: a promotion rejected, and a
strategy kept on the stage it holds.

Consequence for ADR-015 rule 4(a): `review_artifact()`'s `evidence` parameter no
longer has a reason to default to empty. **DRAFTER:** it becomes required.

**No grade floor on `Remain`.** A `Remain` is not an upward move, so rule 1 does not
reach it. Whether keeping a strategy on capital must meet the floor of the rung it
holds was not ruled (18c); see "Put to the owner", item 1.

### Rule 5 — `Micro Capital` is closed until a paper-trading length is ruled

**RULED** (18d, 19c). How long a paper track record must be is referred to the
Investment Committee. **Until a number is ruled, no upward move into
`Micro Capital` is accepted.** A blank number closes the rung and never means "any
length".

**DRAFTER — the mechanism.** A module constant, `MINIMUM_PAPER_TRADING = None`,
beside the rule 1 table. While it is `None`, the check refuses every upward move
into `Micro Capital` with a message naming this rule and 18d. Filling it is an
amendment to this ADR, not a code change a session makes. What unit it takes, and
what report proves a duration, is decided when it is filled.

### Rule 6 — Every promotion states how many variants were tried

**RULED** (18e). A `Promote` review's `content` carries **`variants_tried`**. The
check refuses a `Promote` whose count is missing, not an integer, or less than 1.
The count corrects nothing. ADR-012 rule 10 (`docs/DECISIONS.md:2244-2250`) is
unchanged: no multiple-testing correction is applied until one is ruled.

**DRAFTER:** required on every `Promote`, not only upward moves into capital.
Luck enters at the first backtest, not at the first dollar.

### Rule 7 — Belay's bar is a floor no user setting can lower

**RULED** (19c). In the product, each user sets their own gates at onboarding and
may change them at any time, directly or through their connected AI, **only at or
above Belay's minimums**. Rules 1 to 6 are those minimums.

**DRAFTER — the shape, and nothing more.** The effective bar for any check is the
stricter of Belay's and the user's, computed per rule: the higher grade, the
larger count, the longer duration. A user setting weaker than Belay's is refused
when the settings are loaded, never silently clamped: a clamp would hide from the
user that their setting did nothing. No settings mechanism exists in Belay today,
so this rule binds whatever is built; it builds nothing.

---

## Changes this makes to ADR-015 (to be applied on pull request #7's branch)

1. Rule 4's table: every *to be ruled* cell replaced by a pointer to ADR-016 rule 1.
2. Rule 4's paragraph making `Remain` optional: replaced by ADR-016 rule 4.
3. Rule 4(a): `evidence` stops defaulting to empty.
4. Rule 5: REVIEW `content` grows by `criterion_evidence`, `evidence_reports` and
   `variants_tried`, all in `FIELDS` (`framework/artifacts/review.py:56-67`), so
   writer and reader cannot drift apart.
5. The Status block: ratification is no longer blocked on the evidence-bar ruling.
   It is blocked on this draft's independent pass and the owner's ratification of
   both.

---

## Tests this implies

Each is written red first, against the rule it names.

1. An upward move into each rung with evidence one grade below its floor is
   refused. The same move at the floor is accepted, for every row of rule 1.
2. `Production → Limited Capital` and `Micro Capital → Paper Trading` with only a
   Level D record are **accepted** (rule 1 binds upward only).
3. A move to `Retired` from `Production` with one Level D record is accepted.
4. A capital-rung promotion with six of seven criteria in `criterion_evidence` is
   refused, and the message names the missing one.
5. `criterion_evidence` listing a hash that is not on the artifact is refused.
6. `criterion_evidence` with an eighth, unknown name is refused.
7. A qualifying record with no `evidence_reports` entry is refused.
8. An `evidence_reports` entry naming a report that is not stored is refused, by
   `save()` and by `get()`.
9. An entry whose `report_integrity_hash` differs from the stored report's is
   refused. So is one naming an artifact whose `type` is not REPORT.
10. A `Remain Current Stage` review with no evidence is refused (rule 4).
11. Any upward move into `Micro Capital` is refused while `MINIMUM_PAPER_TRADING`
    is `None`, even with every other requirement met.
12. A `Promote` with `variants_tried` missing, `0`, `-1` or `"3"` is refused. With
    `1` it is accepted.
13. **Mutation check.** Changing any floor in the rule 1 table by one grade turns at
    least one test red. So does deleting any criterion name from rule 2's list.

---

## Consequences

**Real money is closed for the foreseeable future, by the owner's choice.** Rule 2
needs all seven criteria measurable. `python scripts/status.py` reports "promotion
criteria 3 of 7 computable", and regime robustness, execution quality, liquidity
and operational consistency have no working module (`scripts/status.py:48-56`).
Rule 5 closes `Micro Capital` independently of that. Rule 1 needs Level B, which
needs a paper-trading engine that does not exist (`docs/ROADMAP.md:247`).

**Rules that are never exercised rot.** The proposal's author said so of its own
recommendation (section 9). The mitigation is the tests above: the suite exercises
every rule now, while nothing in production does.

### Residual risk, stated rather than buried

- **Grades, criterion labels and the variant count are declarations.** Rule 3 ties
  each to a real, unedited report. It does not prove the report is right, that it
  measures the criterion it is listed under, or that the count is honest.
- **A report can be produced to order.** Binding raises the cost of forging from
  typing a sentence to producing and storing a signed report. It does not remove
  it.
- **The human's yes is not recorded yet.** Part 19c rules that it is, and nothing
  here builds it. Required Follow-Up item 1.

---

## Rejected Alternatives

- **Putting the bar inside ADR-015.** The owner ruled against it (18g).
- **A new `EvidenceRecord` field for the report reference.** Breaks the pinned
  digest (`tests/artifacts/test_evidence_hashing.py:18`) and every stored record's
  verification.
- **A parsed format inside `provenance`.** Turns free text into a hidden schema that
  every existing record silently fails to follow, and that `verify()` cannot tell
  apart from prose.
- **Clamping a weaker user setting up to Belay's minimum.** Hides from the user
  that their setting had no effect. Refusing it tells them.

---

## Put to the owner at ratification — DRAFTER choices, not rulings

1. **`Remain` on capital:** no grade floor (rule 4). Alternative: the floor of the
   rung held.
2. **Report binding on downward moves and `Remain`:** not required (rule 3).
   Required on those would add a step before a demotion, which 18b's reasoning
   argues against.
3. **The mechanism for criterion coverage:** the `criterion_evidence` key (rule 2),
   and the choice that it checks declarations, not topics.
4. **Where the binding lives:** on the REVIEW (rule 3), not the record.
5. **`variants_tried` on every `Promote`**, not only on capital rungs (rule 6).
6. **Weaker user settings are refused, not clamped** (rule 7).
7. **Where both ADRs land in `docs/DECISIONS.md`**, and in which order.

## Required Follow-Up (ADR-016)

1. **Recording each human decision** (19c item 2): what the human was shown, and
   their yes or no, as evidence. That needs its own ruling on shape.
2. **Recording the connected AI's recommendation once, never re-asking it** (19b
   item 3, `AGENTS.md` Determinism).
3. **Checking what a bound report measures**, so that rule 2's criterion labels
   stop being declarations.
4. **Belay's own minimum paper-trading length** (19c), which fills rule 5.
5. **Whether an AI-made change to a user's gates needs that user's recorded yes**
   (19c).
6. **What counts as one variant** (18e).
