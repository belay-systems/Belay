# Operator Checklist

**Actions only the repository owner can take.** Everything here is outside what a
session can do for itself: a GitHub setting, an account permission, a piece of
software installed on a machine, a decision that is the owner's by constitutional
right.

`AGENTS.md` step 14 makes keeping this current a required part of every session
close. A session that discovers an owner-only action and records it only in a
chat transcript has lost it — that is the same failure as work living on an
unmerged branch, which has now cost this repository twice.

**Format.** Newest block first. Tick a line by moving it to `## Done`, with the
date. Never delete a done item; this file is a record as well as a queue.

---

## Open

### Start the next session — one sentence, no prompt to keep

**Added 2026-08-27.** The next session's work is written down in the repository
rather than held in a chat transcript, following the pattern
`docs/proposals/F-007-session-brief.md` established. Open a fresh session and say:

> You are Belay. Read `docs/proposals/register-rebuild-session-brief.md` and work it.

That brief carries the phases, the stop gates, and the one fact a fresh session
cannot derive cheaply: which finding numbers belong to which review, after the
2026-08-14 and 2026-08-21 reviews collided over F-007..F-013.

**Do this after the merges above.** The brief refuses to start until
`reports/review/2026-08-14-review.md`, `docs/OwnerDecisions.md` Part 8,
`reports/review/2026-08-21-review.md` and `.github/workflows/conformance.yml` are
all on `main`.

**After that, the opener is just "You are Belay. Follow `AGENTS.md`."** Phase 2 of
the brief points `docs/HANDOFF.md`'s "Highest Priority Next Task" at itself, and
`AGENTS.md` steps 13 and 14 make every session hand off to the next by rule —
now held up by `tests/test_session_handoff.py` rather than by memory.

---

### Branch protection on `main` — blocks nothing, and nothing is gated until it is set

**Added 2026-08-27**, when `.github/workflows/conformance.yml` landed. CI now
*reports*; it does not yet *block*. Until this ruleset exists, a red suite can
still reach `main`.

**Still unset, reconfirmed 2026-09-19, and there is new information: the
picker above may not be reachable at all on this plan.** `gh api
repos/pewpewpressco-ux/Atlas/rulesets`, the endpoint the archive's settings page
used, returned `403`: `"Upgrade to GitHub Pro or make this repository public to
enable this feature."` This was not checked when the item was added on
2026-08-27. Whether the web UI's ruleset picker is gated by the same plan
restriction as the API is not established from here — that needs the owner to
actually open `settings/rules` and look — so this is recorded as a new fact
rather than as a rewrite of the steps below, which are kept unless the owner
finds they do not apply. **Nothing gates the canonical source today, and three
pull requests are about to merge into it** — #9, then #11 retargeted to
`main`, and eventually #10 once ADR-015 is ratified — which is what raises
this item's urgency rather than what it asks the owner to do.

**Do this only after PRs #5, #1, #2 and #3 are merged.** Those three review
branches were created before CI existed, so they carry no checks. Turning
protection on first blocks all of them and each would need its branch updated to
get unstuck. Protect last.

1. `https://github.com/belay-systems/Belay/settings/rules`
2. **New ruleset** → **New branch ruleset**
3. **Ruleset Name**: `main`
4. **Enforcement status**: `Disabled` → **`Active`**
5. **Target branches** → **Add target** → **Include default branch**
6. Under **Rules**, tick:
   - Require a pull request before merging
   - Require status checks to pass
   - Block force pushes
7. Under *Require status checks to pass* → **Add checks** → add all five:
   `governance conformance`, `suite (py3.11)`, `suite (py3.12)`,
   `suite (py3.13)`, `dashboard builds`
8. Tick **Require branches to be up to date before merging**
9. **Create**

**If the check names do not appear in the picker**, the workflow has not run on
`main` yet. Merging PR #5 triggers that run — watch the **Actions** tab, wait for
it to finish, then reopen the picker.

**Verification, so this is not self-certified:** open any new pull request. It
must read "Merging is blocked" until all five checks report green. If it does
not, the ruleset is not active on the default branch.

**Record it when done.** This changes who may write to the canonical source, which
makes it an owner ruling rather than a setting — it belongs in
`docs/OwnerDecisions.md` as its own Part, on the same footing as the other
rulings there.

---

### Merge order — PR #12, then the records pull request

**Added 2026-09-19 (evening), superseding the merge-order item now in
`## Done` below rather than editing it.** In order: merge PR #12
(`fix/review-skill-numbering`) to `main`; retarget the records pull request
(`records/2026-09-19-rulings`) from `fix/review-skill-numbering` to `main` and
merge it. **PR #10 stays a draft** until ADR-015 is ratified, unaffected by
either merge. `docs/OwnerDecisions.md:1385` (Part 10d) and `:1589` (Part 10j —
why this is an owner action rather than something the session did itself:
an unattended merge of PR #12 was refused by Claude Code's own permission
control).

---

### Before making the repository public — six decisions, none blocking technically, all the owner's

**Added 2026-09-19 (evening).** `docs/OwnerDecisions.md:1516` (Part 10h)
records a read-only history scan run before the repository goes public: no
secrets found, no MUST-FIX item. These six remain, each the owner's call:

1. **The owner's own email address is the author on every commit to date**
   (291 at scan time). GitHub's commit-email-privacy setting protects *future*
   commits only; hiding the ones already made means rewriting history, which is
   a separate and riskier decision than this checklist should make for the
   owner.
2. **A Windows username appears in file paths in tracked documents.**
   Verified this session by `git grep`, and the count does not match what was
   reported at scan time: **5 places**, not 6 — `docs/HANDOFF.md`,
   `docs/OwnerDecisions.md`, and three files under `reports/review/`. (The
   username is not written here; this item exists so the owner can find and
   judge them, not so a session repeats them.)
3. **One cloud-routine trigger id and one cloud session id appear in tracked
   docs.** The trigger id is in this file, in the "review cadence gate" entry
   under `## Done`; the cloud session id is in `docs/HANDOFF.md`'s "Evening
   addendum" and "Completed This Session" sections. Both are identifiers, not
   credentials, and neither is reproduced again here.
4. **`LICENSE` is MIT with no name on the copyright line** (verified: it
   reads "Copyright (c) 2026" and nothing else). MIT permits anyone to reuse
   the whole framework, including commercially. Decide before going public
   whether that is intended, and put a name on the line if so.
5. **`.github/workflows/conformance.yml` is safe to run from an outside
   contributor's pull request, verified rather than assumed**: it triggers on
   `pull_request` (`:23-26`), not `pull_request_target`, and declares
   `permissions: contents: read` (`:29-30`) — no secrets are used and none
   could be exfiltrated through it. Once public, anyone can open a pull
   request and cause it to run; turn on "require approval for outside
   contributors' workflows" in repository settings regardless, as a second
   layer.
6. **Everything tracked becomes readable**, including six review reports
   under `reports/review/` that name every open defect this repository has
   found in itself. That is a feature of Law VII, not a bug, but it is a
   different kind of exposure than a secret and worth the owner seeing plainly
   stated once before deciding.

---

### Immediately after going public — a ruleset on `main` — DONE 2026-09-20

**Added 2026-09-19 (evening). Every item below was applied on 2026-09-20 by
`scripts/public_settings.py --apply`, which had never run before, so its first
run was its test. The account of that run is the last section of this file.
This block keeps its original length so that no line citation into it moves.**

1. Require a pull request before merging. — done, in `main: checks`.
2. Require the five conformance checks by name: `governance conformance`,
   `suite (py3.11)`, `suite (py3.12)`, `suite (py3.13)`, `dashboard builds`. — done.
3. Block force-pushes; restrict branch deletion. — done, both in `main: checks`.
4. Enable secret scanning and push protection. — done.
5. Enable commit-email privacy — the owner had already set it on the account.
6. Disable Issues if unused. — overruled; Issues are how work is claimed.

---

### Rulings owed

**Added 2026-09-19, updated in place the same evening rather than rewritten —
`docs/OwnerDecisions.md` Part 10 (10e-g) partially answered the first item
below.** What is still waiting on the owner, not on a session:

- **F-004 is ruled as to shape; its numbers are not. F-006's narrow fix is
  authorised; its wide question is ruled as "calendar proposal first", and the
  calendar itself is still owed.** `docs/HANDOFF.md:3559` (F-004) and
  `docs/HANDOFF.md:3590` (F-006) carry dated 2026-09-19 (evening) corrections
  in place; `docs/OwnerDecisions.md:988` (Part 8, as corrected) and Part 10e-g
  (`:1411`-`:1515`) are the authorities. **No code opens for F-004's numbers or
  F-006's wide question until they are ruled.**
- **Two research proposals, seven questions each, await the owner — ask one
  at a time, with a recommendation and the reasons, the format the owner
  asked for.** The evidence-bar proposal (section 10, evidence-bar-per-rung.md
  under `docs/proposals/` **on PR #10's branch only** — not a resolvable path
  on this branch, so named without backticks) and
  `docs/proposals/sample-adequacy-definition.md` (section 10, this branch).
  Both have had exactly one independent adversarial pass (17 defects/4
  blockers, and 15/5, respectively) and neither has had a second.
- **F-014's fix is unruled beyond Part 9e's shape selections.** F-014 is
  `docs/HANDOFF.md:4017`. `docs/OwnerDecisions.md:1215` (Part 9e) selects a
  *shape* for ADR-015, which covers F-014 together with F-007, and says
  plainly that this is not a ruling adopting it.
- **Whether an explicit owner instruction may override the review gate's SKIP
  verdict is unruled.** See "Owner glance items" below, item (d).
- **ADR-015 itself is unratified**, and ratification is blocked on the
  evidence-bar ruling above — see PR #10's own Open item on that branch,
  which this item does not duplicate: that ruling arrives with PR #10.

---

### Owner glance items — small, but the owner's call rather than a session's

**Added 2026-09-19.** Four things worth a look rather than a decision-blocking
ruling — (d) was added later the same day, with the review-skill numbering fix:

- **(a) A correction may be mapped onto the wrong finding.** The 2026-08-21
  report's correction block maps its F-010 onto the 2026-08-14 review's
  F-008, though only the trailing clause of the two actually overlaps. The
  register copies the correction faithfully rather than re-deriving it. If
  the owner disagrees with the mapping, the remedy is a **new durable
  number**, never a renumbering — renumbering is exactly the mechanism that
  cost seven claimed numbers on 2026-08-21.
- **(b) The twelve priorities on F-019..F-030 are this registration's own
  derivation, not the reports' own grading.** Neither
  `reports/review/2026-09-04-review.md` nor
  `reports/review/2026-09-11-review.md` states a priority for any finding —
  only a severity. The owner may re-grade any of the twelve; nothing here is
  a ruling that the mapping is right.
- **(c) ADR-015 leaves "Remain at current stage" reviews evidence-optional**,
  on the draft's author's own judgement rather than on an owner instruction —
  the owner's "Evidence for everything" selection (`docs/OwnerDecisions.md`
  Part 9e-v) named promotions, demotions and retirements as needing evidence,
  and did not name "remain" reviews either way. Worth a glance before
  ratification, not a blocker recorded as one.
- **(d) On SKIP the review skill now says do not run at all — should the owner
  be able to override that?** Added 2026-09-19, with the numbering fix.
  `.claude/skills/belay-review/SKILL.md:42-79` tells a reviewer that a SKIP
  from `python scripts/review_due.py` means the review does not run and no
  finding number is allocated. That is right for the scheduled routine and for
  anyone running it unattended, and `scripts/review_due.py:5` already exits 1
  to say so. But it leaves **no override path for an off-cadence review the
  owner explicitly asks for in a separate turn**, which is a different question
  from cadence discipline and is **unruled**. A session did not decide it
  either way; the instruction as written is the conservative reading. If the
  owner wants an override, the shape worth ruling is the one this skill already
  uses for fixes: an explicit instruction in a separate turn, recorded, with
  the number still coming from the gate.

---

### Do not run a manual `/belay-review` yet — the numbering hazard is still in the skill

**Added 2026-09-19.** `.claude/skills/belay-review/SKILL.md:250-252` still
instructs a reviewer to "number them continuously across reviews — if the
last report ended at F-014, this one starts at F-015" — numbering from the
previous report's *headings*, which is the exact collision mechanism that
cost seven already-claimed numbers on 2026-08-21. The **scheduled** cloud
routine is protected from this because its prompt takes the number from
`scripts/review_due.py` rather than from the skill's own instruction; a
manually-run `/belay-review` is not. Editing the skill is a proposal for the
owner to approve, not a session's call to make unilaterally, because it
changes how every future review numbers its findings.

**Updated in place 2026-09-19 — the owner approved that edit in chat, and it
is written.** The selection was two choices and nothing wider: correct the
skill's finding-numbering instruction, and take F-025's hardcoded counts in the
same file. **The approval itself is not yet on file in `docs/OwnerDecisions.md`
— a records pull request follows this one.** Until that lands, the record of
the authority is this block, the closing entry in `docs/HANDOFF.md` and the
`CHANGELOG.md` entry, and nothing in the register where the other Parts are. The instruction the paragraph above quotes is gone;
`.claude/skills/belay-review/SKILL.md:285-305` now says the first finding takes
the number `python scripts/review_due.py` prints and that the number is never
derived from where a previous report's headings ended, and
`tests/test_session_handoff.py:287-445` holds both halves of that.

**This item stays Open because the fix is on a branch.** It is on
`fix/review-skill-numbering`, as a draft pull request. Until that merges, a
`/belay-review` run from a checkout of `main` still reads the old instruction,
so the caution above still applies there. **Move this block to `## Done`, dated,
when the pull request merges** — that is the owner action this item is now
asking for, in place of the original one.

---

### Opening Belay to a second contributor — the owner's own steps

**Added 2026-09-19 (night).** `docs/OwnerDecisions.md` Part 11 records the
rulings behind these. Placed last under `## Open` so that no existing line
citation into the sections above it moves.

1. **Merge the co-contributor readiness pull request**
   (`hardening/co-contributor-readiness`) after reading the independent passes
   pasted into it.
2. **Item 4 of the six publication decisions above is answered**: the licence
   is now a proprietary notice in the name "The Belay project owners" (Part
   11c). The other five are still owed, and are to be put one at a time.
3. **A seventh publication decision, new tonight, and the one that matters
   most: publish this repository's history, or a fresh one.** Four independent
   passes ran before publication (their findings are pasted into the pull
   request). None found a secret. But the history itself carries things that
   editing today's files cannot remove: the MIT licence text in every earlier
   commit; the owner's email address and working hours in every commit's
   metadata; a Windows username, a cloud-routine id and session ids in dozens of
   earlier file versions and in four old pull request descriptions; nineteen
   branches, most abandoned; and seven orphaned commits on GitHub that belong to
   no branch and that no branch-based scan can see, but that anyone holding
   their id could fetch once the repository is public. **Recommended: create a
   new public repository from a cleaned snapshot of `main`, committed under
   GitHub's no-reply address, and keep the Atlas repository private as the full
   archive.** Cost: commit ids and pull request numbers cited in these documents
   will resolve only in the private archive, and a note must say so. The
   alternative is to publish this repository as it is and accept all of the
   above, permanently. **RULED the same night: a fresh repository — `docs/OwnerDecisions.md` Part 12b. What it leaves open is listed there.** **Those points were answered at close of night (Part 13): all six publication decisions are now answered, and the build is briefed in `docs/proposals/fresh-public-repository-brief.md`. Still yours alone: switching on "Keep my email addresses private" before Belay's first commit, creating the organization if you choose one, and the public flip itself.**
4. **Have a professional read `LICENSE`** before Belay is sold or anyone outside
   the two owners contributes. An AI agent wrote it as a conservative placeholder.
5. **Write down, privately, how Belay is owned between you and the second contributor**,
   before their first contribution merges. Nothing in the repository decides it.
6. **When you flip the repository public**, add to the ruleset on `main`
   described above: "Require review from Code Owners". `.github/CODEOWNERS`
   names the owner alone for every governance path, so this is what makes those
   a rule GitHub enforces rather than a convention.
7. **Set your commit email to GitHub's no-reply address** for future commits
   (GitHub, Settings, Emails, "Keep my email addresses private"), then tell the
   next session so it can set the same address in this clone's git
   configuration. This protects future commits only; see decision 1 above for
   the ones already made.
8. **Keep Issues switched on.** The ruleset list above says "Disable Issues if
   unused"; they are now how work is claimed, so that line no longer applies.
   Also switch on "Private vulnerability reporting" (Settings, Code security),
   which `SECURITY.md` relies on.
9. **Give the second contributor the repository link once it is public.** They fork it and
   need no invitation and get no write access. Point them at `CONTRIBUTING.md`.

---

### Create the `belay-systems` organization and Belay itself — ADDED 2026-09-20

Ruled in `docs/OwnerDecisions.md` Part 14a. **Only the owner can do steps 1
to 3**; an agent cannot create a GitHub organization.

1. **Create the free organization**: `https://github.com/organizations/plan` →
   **Free**. Name it `belay-systems`. GitHub shares one namespace between
   users and organizations, so if the name is free for a user it is free for an
   organization; you will find out at creation.
2. **Invite the second contributor**, `Eternalaether5` (canonical login
   `eternalaether5`), as an
   organization **Member**, and give them Write access to Belay once they
   accept. Ruled in Part 15b, which overrules the "Owner" this entry once said.
3. **Create the repository** `Belay` inside it, **PRIVATE**, with no README, no
   `.gitignore` and no licence. The snapshot supplies all three, and any file
   GitHub adds at creation would break the single-commit requirement.
4. Then tell the session, which pushes the snapshot and confirms the five
   checks pass. **Not before two independent passes on the snapshot report
   clean** — `docs/OwnerDecisions.md` Part 13a makes that the owner's own
   condition on publishing the findings register.

### Make Belay public, then apply the ruleset the same day — DONE 2026-09-20

**The owner flipped Belay public on 2026-09-20 and told the session, which ran
`python scripts/public_settings.py --apply`.** Baseline after the flip was 5 of
11 checks passing. After applying, 11 of 11.

The table was read rather than the "ok", as this block demanded, and then the
result was tested against GitHub's own behaviour rather than against the
script's comparison of its own files: a pull request that now reports blocked,
and a fresh CI run that stays green under the new Actions restriction. The
account is the last section of this file. The by-hand fallback was not needed
and is still the last section of `docs/HANDOFF.md`.

### Close Atlas down as a workplace — ADDED 2026-09-20, ONE ITEM LEFT

After Belay is live and public:

- Atlas's `README.md` now says development has moved to Belay — done
  2026-09-20. **Marking that repository archived (read-only) on GitHub is
  still the owner's, and it stays private either way** — Part 12b, permanent.
- On the owner's machine, Belay is cloned into its own `Belay` folder (Part
  15c, overruling 14d). Done 2026-09-20, and the git-ignored market data store
  was moved across with it. The old folder stays, as the archive's clone.
- **The scheduled review routine moved to Belay on 2026-09-20** (Part 14c), by
  partial-update in place — never retired and replaced. Same trigger id, same
  next firing, `mcp_connections` not passed. What it points at now, and the
  evidence that it carries no connectors at all, is in the last section of
  this file and in Issue #3.


### Decide whether GitHub Discussions is enabled — ADDED 2026-09-20, UNASKED

**This has not been put to the owner.** It is listed so it is not lost, which is
how it nearly was: `docs/OwnerDecisions.md` Part 14e claimed it was already
listed here when it was not, and an independent pass caught the claim.

Part 14e ruled the **wiki** stays off, because a wiki is a separate repository
that no pull request, no check and no ruleset on `main` reaches — a second
source of truth, which Part 11a rules against. **Discussions is not the same
thing**: it holds conversation rather than record, so it does not compete with
the repository as a source of truth. It is still the owner's call, and on a
public repository it is also a place strangers can post.


## Done

### Merge order for the three register/ADR pull requests — DONE 2026-09-19

**Added 2026-09-19, closed the same day (evening).** In order: PR #9 merged
as `2f44c19`; PR #11, retargeted from `register/2026-08-21-corrected` to
`main`, merged as `3080848`; PR #4 (`register/2026-08-21-findings`) closed as
superseded by #9 — closed, not deleted, per Immutable Law VII. All three
verified this session via `gh pr list --state all`. **PR #10 stayed a draft
throughout**, as this item required. `docs/OwnerDecisions.md:1300` (Part 10a)
and `:1360` (Part 10c) are the owner's selections that authorised this.

**Superseded by, not the same item as, "Merge order — PR #12, then the
records pull request" above** — that is a new merge, not a re-opening of this
one.

---

### A local pre-push guard was installed — DONE 2026-09-19

**Added and closed the same evening.** `.git/hooks/pre-push` refuses any
direct push to `main` from this clone, printing a message and exiting 1;
every other push is unaffected. **This clone only** — untracked, no effect on
the cloud routine or on any other machine, removed by deleting the file.
`docs/OwnerDecisions.md:1620` (Part 10k).

---

### The review cadence gate reads only the default branch — DONE 2026-09-19

**Added 2026-08-27, closed 2026-09-19 in two halves**, because it was always two
problems wearing one entry.

*The repository half.* PR #6 merged as `a4e7a2a`. `scripts/review_due.py`
enumerates `reports/review/` across every `origin/*` ref rather than the working
tree, fetches before it reads, and answers both questions the gate asks — whether
a review is due, and what number its first finding takes. It is standard library
only, so it runs before any `pip install`.

*The account half.* The gate's prose lived in the stored prompt of cloud routine
`trig_<id>` ("Belay Review — biweekly red team", cron
`0 6 * * 5`). Its Step 1 now runs `python scripts/review_due.py` and obeys the
exit code — 0 run, 1 skip — and is told explicitly not to fall back to listing
`reports/review/` by hand.

**Two further defects in the same stored prompt were fixed while it was open**,
both read out of the 2026-09-18 run log rather than inferred:

- Step 2 instructed `pip install -e .` on a dependency failure, which installs the
  runtime and no test runner. The 2026-09-18 run followed it, got
  `No module named pytest`, and had to retry with `pip install -e ".[dev]"`.
  `pyproject.toml` makes pytest an optional extra, and this is the third occasion
  the distinction has cost a session time.
- Step 3 instructed the reviewer to "continue the F-NNN finding numbers from where
  the most recent report left off". That instruction **is** the collision
  mechanism: a report's headings are what one pass called its findings, not the
  durable series, and `reports/review/2026-08-21-review.md` heads F-007..F-015
  while its own correction block renumbers them F-014..F-018. The number now comes
  from the gate, which reads all prose across all refs.

**The 2026-09-18 firing is the evidence this was worth closing.** It was the
fourth consecutive firing authorised on a wrong answer — the working tree showed
`2026-08-21` at 28 days while the real newest was `2026-09-11` at 7, on an
unmerged branch. It did not produce a fourth duplicate review, but not because
the gate worked: it proceeded past Step 1, went looking at remote refs on its own
initiative, ran the then-unmerged `review_due.py` out of `/tmp`, and stopped.
Judgment caught it four firings running, which is not a control.

**Not yet verified by a real firing.** The next scheduled run is 2026-09-25, and
the gate returns SKIP until 2026-09-23.

---

### Point the scheduled review task at `scripts/review_due.py` — DONE 2026-09-19

**Added 2026-08-29, done 2026-09-19.** It was dated against a 2026-09-02 firing it
did not reach; the edit landed three firings late. The substance is in the entry
above.

**This entry recorded something false, and the error is worth keeping.** It stated
that the routine "is account configuration — no session can read or edit it,
confirmed by `CronList` returning nothing for it", and asked for a guided
walkthrough on that basis. A session edited it directly on 2026-09-19 with the
`RemoteTrigger` tool — `{action: "get"}` then `{action: "update"}` against the
trigger id — having read its 2026-09-18 run log the same way.

**The confirmation was drawn from the wrong instrument.** `CronList` lists only
jobs created by `CronCreate` *within the current session*, so it returns nothing
for any pre-existing routine and cannot tell "does not exist" from "not mine".
`mcp__scheduled-tasks__list_scheduled_tasks` misses it too — that tool sees local
scheduled tasks, and this is a cloud routine. Two tools returned nothing, and the
absence was read as a fact about permissions rather than about their coverage.
The walkthrough this entry demanded was therefore never necessary.

**Standing note for whoever edits it next: update in place, never retire and
replace.** A rebuilt routine can come back without connector access, and this one
uses a GitHub connector in its Step 4. Partial-update `job_config` alone; do not
pass `mcp_connections` or `clear_mcp_connections`.

---

# The public flip, 2026-09-20 — appended here so that no line citation moves

This section sits at the end, against this file's "newest block first" format,
for the reason `docs/HANDOFF.md`'s own last section gives: lines above are cited
by number from `docs/HANDOFF.md`, from `docs/OwnerDecisions.md` (which an agent
may not edit), and from two frozen reports under `reports/review/`. Moving a
block down to `## Done` would shift them. The three blocks this session finished
are marked DONE in place instead, each kept at its original length.

## How the owner merges a pull request, now that `main` is ruled

**Put first because it is the thing an owner needs at the moment they are
stuck, and because it was not written down and cost two attempts on the day the
rulesets went live.**

A plain merge is refused:

```
> & "C:\Program Files\GitHub CLI\gh.exe" pr merge <N> --repo belay-systems/Belay --merge
X Pull request belay-systems/Belay#<N> is not mergeable: the base branch policy prohibits the merge.
```

The merge that works adds `--admin`:

```
> & "C:\Program Files\GitHub CLI\gh.exe" pr merge <N> --repo belay-systems/Belay --merge --admin
```

**`--admin` does not skip the tests, and cannot.** It reaches exactly one rule.

- `main: checks` — the five checks, no force-push, no deletion. Its bypass list
  is empty and GitHub reports `current_user_can_bypass: never` for the owner.
  `--admin` does not move it. It does not need to when the checks are green.
- `main: review` — the review requirement. This one grants the owner
  `pull_requests_only`, deliberately: the owner is the only code owner, GitHub
  refuses a self-approval, and without the bypass nothing could ever merge.
  `--admin` is how that bypass is exercised from the command line.

So a refusal here is the unbypassable ruleset working, and `--admin` is the
designed path rather than a way around it. **Do not use `--auto`**, which `gh`
also offers: it queues the merge to happen later, unattended, which is not what
an owner clicking merge means.

**This stops being needed** once a second person has write access: a real
reviewer satisfies `main: review` and the bypass goes unused. Until then, every
merge takes `--admin`.

The commands are given in PowerShell form on purpose. The Run button in the
owner's desktop app opens PowerShell, and a bash-form command pasted there
fails.

## What was applied

The owner made Belay public. A session then ran `python
scripts/public_settings.py --apply` — its first run ever. Read-only baseline
immediately after the flip: 5 of 11. After applying: 11 of 11.

Both rulesets from `.github/rulesets/` are active on the default branch:
`main: checks` (a pull request, the five checks, no force-push, no deletion)
with an **empty bypass list**, and `main: review` (one approving review,
code-owner review, stale reviews dismissed on push) which an organization owner
may bypass through a pull request.

## What was checked against behaviour, rather than against the script

`scripts/public_settings.py` compares its own tracked JSON to the API, which is
the script certifying itself. Three things were checked independently of it:

- `GET repos/belay-systems/Belay/rules/branches/main` lists both rulesets' rules
  as applying to the default branch.
- Pull request #7 now reports `mergeStateStatus: BLOCKED`, which is the test the
  "Branch protection on `main`" block above asks for by name.
- CI was re-run on `main` **after** the Actions restriction was applied, because
  allowing only GitHub-owned actions could have broken it. All five jobs green,
  and their names match the five required check names exactly — a mismatch there
  would have wedged `main` permanently.

## One inference is now proven; the other is not

This session first wrote here that both were unproven. An independent pass
settled the first, and this block supersedes that claim. GitHub reports it per
ruleset, for the calling user:

```
$ gh api repos/belay-systems/Belay/rulesets/23744225 --jq '.current_user_can_bypass'
never                # main: checks
$ gh api repos/belay-systems/Belay/rulesets/23744226 --jq '.current_user_can_bypass'
pull_requests_only   # main: review
```

One account, an organization admin, at one moment: `never` on the ruleset with
an empty bypass list, `pull_requests_only` on the ruleset granting it a bypass.
**A bypass applies only to the ruleset that grants it.** That is GitHub's own
answer rather than a reading of its prose.

**The second is still unproven:** that an author cannot approve their own pull
request. Nothing here tested it. The next real pull request settles it.

**Do not check the bypass design with `rules/branches/main` alone.** That
endpoint lists rules the caller can bypass beside rules it cannot, without
distinguishing them, so it cannot answer this question. Use
`current_user_can_bypass` on each ruleset.

## What the checks do not cover

Found by the same pass. None of these is a live misconfiguration today; each is
something the green table does not actually prove.

- `_COMPARED` in `scripts/public_settings.py:95-100` compares four of the twelve
  parameters GitHub returns for these rules, while line 134 prints "active and
  matches `.github/rulesets/`". Three values the tracked files pin are outside
  that comparison.
- `.github/rulesets/main-review.json` declares `"actor_id": 1`; GitHub stores
  `null`. `_shape()` compares only `actor_type` and `bypass_mode`.
- `--apply` switches dependency alerts on at `:233`; `run_checks()` never reads
  them back, so "11 of 11" does not cover that setting. It is on.
- `main-checks.json:25` sets `strict_required_status_checks_policy: false`, so a
  pull request cut from an older `main` can merge on checks that never ran
  against the tree that lands. A tradeoff rather than an error, but it is the one
  gap in an otherwise unbypassable ruleset.
- **Nothing re-runs `scripts/public_settings.py` on a schedule or in CI.** If any
  of these settings is changed later, nothing notices.

## `.github/CODEOWNERS` is invalid while the invitation is pending

```
$ gh api repos/belay-systems/Belay/codeowners/errors
line 11, "Unknown owner": make sure @eternalaether5 exists and has write access
```

`.github/CODEOWNERS:11` is the catch-all. Until the invitation is accepted it
resolves to the owner alone — which `:6-7` already anticipates — but GitHub
reports the file as containing an error, and on a public repository that report
is visible to anyone. **It clears itself when the Write grant below is made.**
Three of the five lenses in the 2026-09-20 pass reported this independently.

## Open blocks above that the flip and the rebuild made false

Listed rather than rewritten. Most of these blocks sit at line numbers that
`docs/HANDOFF.md`, `docs/OwnerDecisions.md` and two frozen reports under
`reports/review/` cite, so editing them in place would make those citations
quote text that was never there. Whoever clears them should decide that
question first — it is the same one Issue #9 raises.

- `:44-97` "Branch protection on `main`" — says "Still unset" and gives by-hand
  steps. Both rulesets are live. Following those steps would create a third,
  overlapping one. Its preconditions name Atlas pull request numbers.
- `:99-111` "Merge order — PR #12" — those pull requests do not exist on Belay;
  the change was folded into the first commit.
- `:113-153` "Before making the repository public" — the gate is behind us, and
  four of its six decisions describe the Atlas archive rather than Belay. Its
  counts (an email on 291 commits, a username in five files, two live
  identifiers) are all zero here.
- `:245-277` "Do not run a manual `/belay-review` yet" — its stated exit
  condition is met on `main`, but its closing trigger ("when the pull request
  merges") can never fire, because no such branch or pull request exists here.
- `:279-329` item 9 tells the owner to give the second contributor a link to
  fork from; Part 15b made them a Member with Write instead.

## The scheduled review routine

Moved to Belay the same day by `RemoteTrigger` partial update — `job_config` and
`name` only, `mcp_connections` not passed, never retired and replaced. Same
trigger id; `next_run_at` unchanged at 2026-09-25. It now names the Belay
repository as its source, reads `.claude/skills/belay-review/`, and titles its
pull request "Belay Review". The cadence gate answers correctly in this clone —
SKIP at 10 days, next due 2026-09-23 — so the 2026-09-25 firing will be DUE.

Reading it also produced evidence for Issue #3: `mcp_connections` and
`mcp_servers` are both empty and `allowed_tools` is five built-ins, so the
routine carries no connectors at all, and the clause at `:490-491` saying "this
one uses a GitHub connector in its Step 4" is false as the routine is
configured. That evidence is posted on Issue #3 rather than resolving it, since
the other document's claim is about creation and was not tested.

## Open — grant the second contributor Write access

**Added 2026-09-20.** `eternalaether5`'s organization invitation is still
**pending** (sent 2026-09-20, role Member, which is what Part 15b rules). Write
access cannot be granted until they accept. Until then `main: review` binds
nobody but the owner, because GitHub counts a code owner only if they have write
access. The owner's part is getting the invitation accepted; a session grants
the Write once it has been.

# 2026-09-22 — owner items from the evidence-bar rulings (`docs/OwnerDecisions.md` Parts 18-19)

Appended so that no line citation moves.

## Open — merge pull request #19

It records Parts 18a-18g and 19 in the owner's words. It changes no code and no
ADR status. No independent pass was run on it: it records rulings, and the pass
that counts is on ADR-016 once it is drafted.

## Open — Belay's licence terms (Part 19c, item 4)

Belay is sold and then downloaded. `LICENSE` still forbids running it. The
terms a buyer receives are the owner's to write or commission. No session may
change `LICENSE`.

## Open — legal advice on selling investment recommendations (Part 19b, item 5)

Software that recommends investments to other people may carry legal
obligations. No session can assess that. It needs a lawyer.

## Later — ratify ADR-015 and ADR-016

Neither is ready yet. Each needs drafting from Part 18, then a fresh
independent pass, before it is put to the owner.

# 2026-09-24 — owner items from the outside-text review (#23, #25, #26, #27)

## Open — how #23 and #26 reach `main`

Both passed independent falsification passes and are green. Neither can be
approved by an agent, because agents post under the owner's login. The choice
is the second contributor's review, or the owner telling a session "merge #23"
(and "merge #26"), which uses the owner bypass for that pull request only. #23
matters before the scheduled review fires on 2026-09-25 06:07 UTC.

## Open — declare `markdown-it-py` as a dev dependency, or accept it as it is

#23's tests parse markdown with it. Today it arrives only because `rich`, a
runtime dependency, requires it. Declaring it under `dev` in `pyproject.toml`
(an owner-only file) makes the dependency visible. Recommendation: declare it.

## Open — the review routine's stored prompt can be rewritten by any session

The review skill trusts the stored prompt as the run's own instructions. Any
agent session on the owner's account can rewrite that prompt, or append a turn
to a firing. Check the prompt against a known copy before relying on a
scheduled review. Do not paste the prompt or its identifier into this
repository.

## Closed 2026-09-24 — #23 reached `main`

On the owner's word ("merge"), a session merged #23 through the owner bypass at
`22d2d81`, for that pull request only. #26 is still open, as above.

# 2026-09-24 — owner items from hardening the review gate (#29)

## Open — keep or drop the gate's "outside text" rule

Pull request #29 makes `scripts/review_due.py` skip the body of a review
report's `## Outside text` section, so a stranger's number quoted there cannot
move the finding series. Two independent passes each found shapes where a
real finding number in or after that section was silently not counted, and
an uncounted number is issued again. The concrete shapes they found are
fixed. One stated limit remains: a real number inside the section that does
not start its line, with nothing after it that closes the section, and
written nowhere else.

The choice: **keep the rule** and accept that limit, or **drop it and count
everything**. Since #29 also stops the gate at finding number 999, counting everything can
no longer re-issue a number silently. A stranger's quoted number only leaves a
gap, and a quoted number 999 stops the gate until that report is edited. The
question, the trade-off and a recommendation are on #29.

## Open — code-owner review of #29

#29 changes `.claude/skills/belay-review/SKILL.md`, where the owner is the
only code owner. It only repoints citations and states what the gate reads.

## Closed 2026-09-24 — keep the Outside-text rule, or count everything

Owner ruled "count everything" (`docs/OwnerDecisions.md` Part 23). The rule is
removed on #29. Still open for #29: your code-owner review of
`.claude/skills/belay-review/SKILL.md` and `docs/OwnerDecisions.md`.

**Correction to "Open — code-owner review of #29" above.** #29 now does more
than repoint citations. In `.claude/skills/belay-review/SKILL.md` it rewrites
the gate paragraph (`:287-295`) and one sentence of the outside-text rule
(`:383`). It also appends Part 23 to `docs/OwnerDecisions.md`. Both files need
your code-owner review.

## Open — 2026-09-22 (final): what the owner needs to chase

- **Ask the second contributor to review #23 before 2026-09-25**, then merge
  it (with `--admin` until #22's settings are applied). It protects the
  scheduled review that runs that day.
- Then #22, and its five steps in the section "no one merges alone" once that
  PR has merged.
- #20 waits on his independent pass (Issue #21). #7 and #14 wait on his reply.
