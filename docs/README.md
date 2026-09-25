# Documents

Belay's documents are the product, not notes about it. This page says which one
answers which question, so you do not have to open eleven files to find out.

**New here?** Read [`../README.md`](../README.md), then
[`../constitution/README.md`](../constitution/README.md), then stop. Everything
below is reference you consult, not reading you do up front.

## Start here, in this order

| Read | To learn |
|---|---|
| [`../README.md`](../README.md) | What Belay is, and what it deliberately is not yet |
| [`../constitution/README.md`](../constitution/README.md) | The rules capital is governed by. Frozen by ADR-002; only the owner changes them |
| [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | How to claim work and land a change, if you are a person |
| [`../AGENTS.md`](../AGENTS.md) | The same, if you are an AI agent. Start here, whichever provider you are |

## The ones you will actually reach for

| Document | Answers |
|---|---|
| [`NOW.md`](NOW.md) | What state is the project in and what is next. **Start here**; it is short by rule. Open findings: [`FINDINGS.md`](FINDINGS.md). What happened in each session: [`sessions/`](sessions/). Everything before 2026-09-25: [`HANDOFF.md`](HANDOFF.md), a frozen archive |
| [`DECISIONS.md`](DECISIONS.md) | Every architectural decision, as numbered ADRs, with the reasoning and the alternatives rejected |
| [`ROADMAP.md`](ROADMAP.md) | What is built, what is next, and the order |
| [`Architecture.md`](Architecture.md) | How the pieces fit together |
| [`Glossary.md`](Glossary.md) | What a word means here, when it means something specific |

## Governance and the record

| Document | Answers |
|---|---|
| [`OwnerDecisions.md`](OwnerDecisions.md) | Every question put to the owner and the answer given, in the owner's own words, with what each ruling does *and does not* settle |
| [`OperatorChecklist.md`](OperatorChecklist.md) | Actions only the owner can take, open and done |
| [`EndState.md`](EndState.md) | What Belay is trying to become, and which questions are still open. **Its answers are dated: several were settled while the Atlas archive was private** |
| [`Principles.md`](Principles.md) | The six design principles Belay is built around |
| [`DocumentStandard.md`](DocumentStandard.md) | How these documents are written and cited |
| [`ENGINEERING_AGENT.md`](ENGINEERING_AGENT.md) | The engineering agent layer, and what it may and may not do |

## Evidence, and work not yet ruled on

| Where | What is in it |
|---|---|
| [`../reports/review/`](../reports/review/) | Every adversarial review, dated, in full — including the findings against Belay's own code. Included deliberately |
| [`proposals/`](proposals/) | Drafts and session briefs. **Nothing here is ruled.** A proposal is not a decision |
| [`research/`](research/) | Non-binding notes and leads. Nothing here has been reproduced in Belay |
| [`notes/`](notes/) | The original design notes, kept as written |

## Two things worth knowing before you read anything

**Citations are by line number**, in the form `docs/HANDOFF.md:1536`. They are
partly checked by a test — but it only proves a line number is in range, not
that the citation points at the right line, and it falls back to any file of the
same name when the named path does not exist.

**Ids and numbers dated before this repository's first commit will not resolve
here.** They refer to a private archive. See the provenance note at the top of
[`HANDOFF.md`](HANDOFF.md).
