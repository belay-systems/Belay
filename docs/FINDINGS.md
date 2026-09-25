# Findings Register

The live list of open findings, and of findings closed from 2026-09-25 on.
`python scripts/status.py` counts the rows under "Open" below. That count is the
one to trust.

**How this file is kept** (`docs/OwnerDecisions.md` Part 29):

- **One row per finding.** The row's title is the finding's name. Cite a finding
  by its title or its F-number, never by a line of this file. Rows move when
  findings close.
- **Closing a finding moves its row** from "Open" to "Closed", with the date and
  the pull request that closed it. Do not write the reasoning here. It belongs
  in that pull request and in the session record under `docs/sessions/`.
- **A new finding gets a row under "Open".** Its write-up lives in the file named
  in "Written up in", usually the review report that found it. The finding
  number comes from `python scripts/review_due.py`, never from this file.
- **"archive"** means the section of the same title under `# Open Findings` in
  `docs/HANDOFF.md`, which is frozen. Every finding open on 2026-09-25 is
  written up there.
- **Priority** is P1, P2 or P3. **Watched** says whether a strict `xfail` test
  will go red when the finding is fixed.

## Open

| Finding | Priority | Watched | Written up in |
|---|---|---|---|
| Document Metadata Standard Declared, Never Applied | P2 | yes | archive |
| Workflow Base Class Incomplete; Registry Empty | P2 | yes | archive |
| framework/registry.py Implements None Of The Registry Specification | P2 | no | archive |
| ArtifactType And The Identifier Prefixes Are Two Vocabularies That Disagree | P2 | yes | archive |
| Five Different Promotion Criteria Lists | P3 | no | archive |
| 22 Framework Modules Have No Test Reference | P3 | no | archive |
| Broken Imports In departments/ | P3 | no | archive |
| No Halt Mechanism; Demotion Runs At Review Speed | P2 | no | archive |
| Five Backtest Metrics Cannot Be Built Without A Ruling | P3 | no | archive |
| The Roadmap Does Not Reach The Mission | P2 | yes | archive |
| A Home Machine Cannot Guarantee A Halt Within Seconds | P2 | no | archive |
| The Evidence Classes Have No Class For Observed Fact | P3 | no | archive |
| A Fetch Stores Its Bytes Before Discovering The Series Is Empty | P2 | no | archive |
| A Statistical Review Cannot Carry The Survivorship Disclosure (F-003) | P2 | no | archive |
| sample_adequate Is Arithmetically Identical To significant (F-004) | P3 | no | archive |
| A Series With A Hole Discloses Full Coverage (F-006) | P3 | no | archive |
| An Identifier Reused At A New Version Is Silently Mis-Filed | P2 | no | archive |
| ADR-014 Rules 5 And 8 Cannot Both Be Executed As Written | P2 | no | archive |
| Rule 7's Orphan Check Is Vacuous On Every Machine But The One That Fetched | P2 | no | archive |
| The Store's Version Filenames Carry The Four-Digit Cap The Identifiers Shed | P3 | no | archive |
| Every Fetch Reads Every Stored Record | P3 | no | archive |
| A Strategy Can Still Be Signed Into Existence At Production (F-007) | P1 | no | archive |
| The Survivorship Guard Is Defeated Three Ways In Committed Code (F-008) | P2 | no | archive |
| A Suite That Could Not Run Is Reported As Zero Failing (F-009) | P3 | no | archive |
| The Dashboard's Import Health Scans Only `framework/` (F-010) | P3 | no | archive |
| The Roadmap Denies The Market Data Layer It Declares Complete (F-011) | P3 | no | archive |
| HANDOFF Describes A Working Tree That Exists On No Machine (F-012) | P3 | no | archive |
| `test_findings_are_ordered_by_priority` Cannot Fail (F-013) | P3 | no | archive |
| A Promotion Can Be Recorded With No Evidence Whatsoever (F-014) | P1 | no | archive |
| `belay doctor` Cannot Fail (F-015) | P2 | no | archive |
| `is_clean` Decides Whether The Survivorship Warning Prints, And Has No Test (F-016) | P2 | no | archive |
| The Significance Test's Two-Sidedness Is Asserted By Nothing (F-017) | P3 | no | archive |
| "Searched All 101 Documents" Has Rotted To 107 (F-018) | P3 | no | archive |
| The Citation For "Every Decision Requires Written Justification" Points At The Wrong Line In Nine Places (F-020) | P2 | no | archive |
| The Dashboard's "Could Not Run" Branch Destroys The Page Instead Of Reporting (F-023) | P3 | no | archive |
| Nothing Checks An Artifact's Identifier Prefix Against Its Type (F-024) | P3 | no | archive |
| A Significance Result Reports 1,000,000 Observations Where Its Own Function Refuses To Name Any Number (F-027) | P3 | no | archive |
| CI States The Dashboard Job Fails When The Regexes Stop Matching; It Does Not (F-028) | P3 | no | archive |
| ADR-002 Places `departments/` In A Layer That Remains Prose; It Holds Python, And `pyproject.toml` Ships It (F-029) | P3 | no | archive |
| `test_no_session_brief_is_orphaned` Counts `docs/proposals/` As Its Own Pointer Set (F-030) | P3 | no | archive |

## Closed

Findings closed from 2026-09-25 on. Earlier closures are recorded under
`# Closed Findings` in `docs/HANDOFF.md`.

| Finding | Closed | By |
|---|---|---|
| Eight Guards On The Capital And Provenance Path Are Asserted By Nothing (F-019) | 2026-09-25 | #24 |
