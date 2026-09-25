# 2026-09-22 to 2026-09-23 — ADR-016 drafted, sample adequacy ruled (#20)

**Moved here word for word on 2026-09-25.** This branch had appended the text
below to `docs/HANDOFF.md`. Pull request #32 freezes that file as an archive
(`docs/OwnerDecisions.md` Part 29, on #32), so the same text is kept here
instead, unchanged from the line below the rule. "Above" in it means the end
of `docs/HANDOFF.md` as it stood on `main` at `1c8eb1c`. Nothing cited these
lines by number.

---

**Added 2026-09-22, after #19 merged.** Pull request #19 was merged by the
session on the owner's instruction (recorded above), as `1590b34`. Next task 1,
drafting ADR-016, is started: `docs/proposals/ADR-016-evidence-bar-DRAFT.md`,
PROPOSED and not ratified. It marks each rule RULED or DRAFTER, and lists seven
DRAFTER choices the owner has not seen. **Next task 2 is now the next thing
owed: a fresh independent pass told to falsify ADR-016 and ADR-015 together.**
ADR-015's pointer to ADR-016 is not yet applied on pull request #7's branch.
The draft lists the five changes it needs.
**The owner chose the second contributor's agent for that pass** ("second
contributors agens"), as a different AI. It is Issue #21, assigned to them.

## Session close, 2026-09-22 (final) — supersedes the blocks above for today

Written against `origin/main` at `1590b34`, fetched at close, and the open pull
requests and Issues as listed at close. **Re-derive before trusting it:**
`git log --oneline -3 origin/main`, the open pull requests, `python
scripts/review_due.py`.

**On `main`:** #19 only, with Parts 18 and 19 (the evidence bar; Belay is a
product). Suite 659 passed, 1 skipped, 5 xfailed. `python scripts/status.py`:
open findings 41, promotion criteria 3 of 7 computable. Review gate: `SKIP —
last review was 11 days ago … Next due 2026-09-23`. The scheduled routine
fires 2026-09-25.

**Open, all from this session, all CI green, all waiting on the second
contributor. Merge #23 first, because it has a deadline:**

| PR | What | Needs | By |
|---|---|---|---|
| #23 (`claude/review-untrusted-input`) | The review treats outside text as data and records it under `## Outside text` | His approval, then the owner merges | **Before the 2026-09-25 run** |
| #22 (`claude/second-review-settings`) | Part 20: no bypass on `main: review`; both owners are code owners on governance paths, him as reviewer only; `carriers: review` for `adr/**` | His approval; then the owner's five steps in `docs/OperatorChecklist.md` (merge with `--admin` one last time, sync `main` into `adr/015-stage-is-carried`, `--apply`, verify) | — |
| #20 (`claude/pensive-hypatia-nu6j3j`) | ADR-016 draft, and this record | Issue #21, his independent pass | — |

**Also waiting on him:** #7, where he is asked to support or remove the
"independent regression check" claim his corrections make
(`https://github.com/belay-systems/Belay/pull/7#issuecomment-5784292984`); and
#14.

**Expect merge conflicts in `docs/HANDOFF.md` and `docs/OperatorChecklist.md`**
between #20 and #22, which both append to them. Resolve by keeping both
appended blocks. Nothing in either is shared logic.

**What this session found in the second contributor's recent work**, kept
here because it was never on file. #15, #17 and #18 went into ADR-015's branch
merged by their author with no review. That was allowed, because both rulesets
covered `main` only; Part 20 closes it. The substance was correct: every
figure was recomputed and every citation checked. One defect: a claim of an
"independent regression check" with no record behind it, which now sits in
ADR-015.

**What a session did here that the rules otherwise forbid, and on whose
word.** It merged #19 on the owner's explicit instruction, using the Owner
bypass (recorded above). It pushed two branches beyond its designated one,
also on the owner's explicit instruction ("yes - push approved", "yes close
risk 1"). None of the three is a standing permission.

## Highest priority next task — 2026-09-22 (final)

1. **Get #23 merged before 2026-09-25.** If it cannot be, the 25th review runs
   without the outside-text rule. Say so to the owner rather than let it pass
   silently.
2. **When the second contributor's pass on ADR-016 lands (Issue #21)**, verify
   every finding, fix what is real on #20, and put the seven DRAFTER choices to
   the owner one at a time.
3. **After #22 is applied**, check with `python scripts/public_settings.py`
   that every ruleset row reads PASS and that `current_user_can_bypass` is
   `never` on `main: review`. Then close Issue #16 as fixed by Part 20.
4. Then the list above from its item 3: the sample-adequacy questions, from
   PR #7's branch, and Part 19's open questions.

## Added 2026-09-23 — the sample-adequacy numbers are ruled (Part 22)

The owner answered ten questions, the proposal's seven plus three its answers
opened, as `docs/OwnerDecisions.md` Part 22 (22a–22j), on pull request #20.
In brief: backtest only; a 10-year span; the longer of that and the declared
target's minimum track record length; no flat count; 95% complete; no gap over
7 calendar days; a minimum hurdle of 3.0 in both significance and adequacy
(an amendment to ADR-012 rule 3); fail closed when the formula has no answer.
Part 22's closing paragraph states it in full.

**Next, in order:** draft the ADR-012 amendment (rules 3 and 8) from Part 22,
each line marked RULED or DRAFTER, the same way ADR-016 was drafted; then an
independent pass on it; then the owner ratifies. Step 4 of the Stage 3 order
(F-004 with F-006's narrow fix) and step 5's F-027 build from it, and F-027
lands in the same change as F-004's numbers (the proposal's §9).
**Started 2026-09-23:** the ADR-012 amendment draft is
`docs/proposals/ADR-012-amendment-sample-adequacy-DRAFT.md`, PROPOSED, with
each rule marked RULED or DRAFTER and eight DRAFTER choices listed for the
owner. The next step is its independent pass.
**The owner added it to Issue #21** ("add it"): the second contributor's
independent pass now covers ADR-016 and the ADR-012 amendment draft together,
as scoped in a comment on that Issue.

**Parked by the owner, 2026-09-23, for a later conversation, with no action
now:** the owner is concerned that the start-up reading (`AGENTS.md` plus
`docs/HANDOFF.md`, which is nearly 5,800 lines long because nothing in it is
ever deleted) has become too large. Raise it with the owner when there is time
to hash it out. Do not restructure these files before then.

**#23 goes through on the owner's own authority, 2026-09-23.** Asked whether a
fresh session can act as the independent reviewer, the session answered: yes
for the independent pass (`AGENTS.md` point 4 allows "a different session"),
no for the merge approval, because every session here runs under the owner's
GitHub login, which is also #23's author, and 20a (on pull request #22) asks
for "a review by someone other than its author". The owner answered: **"lets
get passed these gates. ill approve myself after i run this"**, meaning: run
the fresh-session falsification pass on #23, then merge it on the owner's own login. GitHub
refuses self-approval, so the merge is the owner's bypass on `main: review`,
which exists until #22 is applied. **This is a one-off exception to 20a, for
#23 only, taken so the outside-text rule is on `main` before the unattended
review of 2026-09-25.** It is not a standing permission, and the second
contributor's review of #22 and #24 is still required.
