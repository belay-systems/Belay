# Files That Grow: Keeping State Apart From History

**Status.** Phase 1 was ruled and implemented on 2026-09-25
(`docs/OwnerDecisions.md` Part 29). Phase 2 is proposed and not ruled.

## The problem, in one paragraph

Four of Belay's documents only ever grow: `docs/HANDOFF.md`,
`docs/DECISIONS.md`, `docs/OwnerDecisions.md` and `CHANGELOG.md`. Each one mixes
two jobs:

- saying what is true **now**;
- keeping **everything that was ever true**.

Law VII was read as "never remove a line from this file", so the second job has
been burying the first. Agents could no longer read the start-up file, and the
file had begun to tell them the wrong next task.

## The evidence

Measured on `origin/main` at `1c8eb1c`:

| File | Lines | Bytes |
|---|---|---|
| `docs/HANDOFF.md` | 5,857 | 327,254 |
| `docs/DECISIONS.md` | 3,619 | 187,260 |
| `docs/OwnerDecisions.md` | 2,864 | 147,351 |
| `CHANGELOG.md` | 298 (one line is 2,107 characters) | 119,220 |

The command was `wc -l -c <file>`, with `awk '{ if (length>m) m=length } END {print m}'`
for the longest line.

**1. No agent can read the start-up file in one pass.** At the usual rule of
thumb of four bytes per token, `docs/HANDOFF.md` is about 80,000 tokens. Claude
Code's file reader, for example, returns at most 2,000 lines per call by
default. Other providers' tools have limits of the same order. An agent has to
read the file in pieces and spend most of its context on it, or stop early and
miss the part that matters.

**2. The file pointed agents at the wrong task.** `AGENTS.md` said: read
"Highest Priority Next Task", and "within a section, the top-most dated block
is the current one."

```
grep -n -i -E '^#+ highest priority next task' docs/HANDOFF.md
```

This finds six such headings, at lines 4725, 5587, 5675, 5728, 5763 and 5837.
The current list is the **last** one, and it says "supersedes every list
above". So the written rule (top-most is current) contradicted the practice
(bottom-most is current). An agent that followed `AGENTS.md` exactly would
start on superseded work.

**3. The test guarded the stale list.**
`tests/test_session_handoff.py` checked the section under
`# Highest Priority Next Task`, which is the one at line 4725. The list agents
actually acted on, at line 5837, was checked by nothing.

**4. The layout was being dictated by line citations.** These five files are
cited by line number 241 times across the repository:

```
git grep -h -o -E "<Name>\.md:[0-9]+" origin/main | wc -l
```

That counts 87 for HANDOFF, 55 for DECISIONS, 67 for OwnerDecisions, 16 for
CHANGELOG and 16 for OperatorChecklist. Any insertion moves every citation
below it. That is why:

- text has kept being "appended here so no line citation moves", even when it
  belonged in the middle;
- the findings register grew four stacked "Corrected … on this commit"
  paragraphs, each superseding the count above it;
- Issue #9 exists, and #7 and #14 each carried a citation-repair table.

**5. Parallel work collides in one file.** On 2026-09-25, Parts 24 to 28 of
`docs/OwnerDecisions.md` are on open branches, and every one of them appends
at the same end of the same file. The fourth pass on Issue #21 recorded
"Parts 22 and 24-26 still collide at OwnerDecisions:2866".

## First principles, and where each comes from

**1. Keep current state apart from history.**
- Hospital and operations shift handovers use a short sheet of current state
  that is rewritten every shift. The log of past shifts is kept separately.
- Databases keep an append-only log as the truth, and a small snapshot for the
  current view. Nobody replays the whole log to find out where things stand.
- A handoff file that is both a snapshot and a log grows without limit, and
  the snapshot gets lost inside it.

**2. One record per file, for anything that only grows.**
- Architecture decision records, as Michael Nygard described them in 2011 and
  as tools such as adr-tools and MADR use them, are one decision per file. A
  new record supersedes an old one by linking to it.
- A lab notebook dates each entry, never erases one, and makes corrections as
  new entries. Belay already works that way ("kept as written — Law VII").
  What it lacks is the separate page for each entry.
- **Belay already does this in one place.** Under `reports/review/` there is
  one file per review, forever, and those files are the right size.

**3. Cite by a name that does not move.** A heading, an F-number, a Part
number or an ADR number survives any edit. A line number survives none,
except in a file that never changes again. Give each record its own file, and
the name is the citation.

**4. A test holds each rule.** In this repository, a clearly written
convention has been broken by agents who had read it (Issue #9, four times in
one session). A rule that matters has to fail the build.

**5. Law VII protects knowledge, not layout.** "Institutional knowledge shall
never be intentionally discarded" is satisfied when text moves to a file that
is kept, or is rewritten while git keeps every earlier version byte for byte.
It is not a rule that one file must hold everything. The owner ruled this
reading in Part 29.

## Phase 1: the handoff (done)

`docs/HANDOFF.md` came first, because every session reads it and it was
actively misleading. Only two open branches append to it, #20 and #22.

| File | Job | Rule | Enforced by |
|---|---|---|---|
| `docs/NOW.md` (new) | Current state, the one next-task list, the working agreement | **Rewritten** at every close. At most 200 lines and 16,000 bytes. Exactly one `## Highest Priority Next Task` | `tests/test_handoff_files.py` |
| `docs/sessions/` (new) | One record per session | `YYYY-MM-DD-short-name.md`, at most 300 lines, never edited after merge | `tests/test_handoff_files.py` (names, cap) |
| `docs/FINDINGS.md` (new) | The findings register, one table row per finding | Closing a finding moves its row. Never cited by line | `tests/test_status_dashboard.py`, `tests/test_handoff_files.py` |
| `docs/HANDOFF.md` | The archive | **Frozen** byte for byte, after its title line was changed to say so | SHA-256 pin in `tests/test_handoff_files.py` |

**Why the archive stays where it is, rather than moving to a new path.** Moving
it was the first idea. Reading the code ruled it out:

- `scripts/status.py` parsed its register.
- Dozens of code comments and `xfail` reasons cite its sections by title.
- Frozen review reports, which may not be edited, cite it by line number.

Left in place and frozen, every one of those citations stays true, and none of
them had to be touched. The title line was the only line changed. It was
changed in place, so the line count stayed at 5,857 and nothing moved.

**What else changed with it:**
- `scripts/status.py` reads the register from `docs/FINDINGS.md`. On this
  commit it lists the same 41 findings with the same priorities as before.
- `AGENTS.md`'s start-up and close-out steps now name the new files, each
  edited in place with its line count unchanged. The rules and their reasons
  are appended as "Files that grow".
- `CLAUDE.md`, `README.md`, `docs/README.md`, `CONTRIBUTING.md`, the review
  skill's reading list and red-team item E5, and the Issue and PR templates now
  point at the new files, each with its line count unchanged.

**Costs, stated plainly:**
- **Frozen review reports quote `AGENTS.md:19` as "3. Review docs/HANDOFF.md."**
  That line now reads "3. Review docs/NOW.md." A report is a dated record, and
  its quotation was true on its date. This is the same treatment every earlier
  edit to `AGENTS.md` got.
- **#20 and #22 append to `docs/HANDOFF.md`.** Whichever lands second has to
  adapt. If this change lands first, their appended text moves into a
  `docs/sessions/` record and into `docs/NOW.md`, and the freeze test's message
  says exactly that. If they land first, this change re-pins the hash and folds
  anything still current into `docs/NOW.md`.
- **The "never edited after merge" rule for `docs/sessions/` is not yet
  enforced by a test.** Checking it needs git history in CI, which is the same
  mechanism Issue #9 asks for `reports/review/`. It belongs to that Issue.

## Phase 2: the other three growing files (proposed, not ruled)

**Wait until the open pull requests that add to these files have landed.** Those
branches append thousands of
lines to `docs/DECISIONS.md` (#7's branch has 6,564 lines against `main`'s
3,619) and add Parts to `docs/OwnerDecisions.md`: 16-17 on #14, 21 on #24, 22
on #20 and 24-28 on #31. Splitting either file now would put every one of
those pull requests into conflict, and it would land in the middle of the
evidence-bar work.

**The same pattern each time:**
1. freeze the existing file in place, byte for byte;
2. put new records in a directory, one file each;
3. add an index that a test keeps in step;
4. pin the freeze with a hash.

| File | New home for new records | Notes |
|---|---|---|
| `docs/DECISIONS.md` | `docs/decisions/ADR-NNN-short-name.md` | `scripts/status.py`'s `decisions()` reads the frozen file and the directory. ADR status stays owner-only, so `.github/CODEOWNERS` and `tests/test_publication_guard.py` must cover the directory. |
| `docs/OwnerDecisions.md` | `docs/owner-decisions/Part-NN.md` | Claiming a Part number becomes creating a file. Two branches claiming the same number then collide on the file name, which git reports, instead of silently appending two Part 29s. The same CODEOWNERS and guard-test cover applies, and it is owner-only, so it needs its own ruling. |
| `docs/OperatorChecklist.md` | Open items in a short, capped file; finished items to the archive | The same state/history split as `docs/NOW.md`. |
| `CHANGELOG.md` | One line per change, with a link to its pull request | Keep a Changelog's convention. The detail belongs in the pull request, not in a 2,107-character line. |

**Questions phase 2 will put to the owner, one at a time:**
1. Split `docs/OwnerDecisions.md` into one file per Part? The recommendation
   is yes, because Part-number collisions are already happening.
2. Should `CHANGELOG.md` keep its long entries, or move to one line per change?
   The recommendation is one line.
