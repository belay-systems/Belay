# Belay Repository AI Development Guide

## Purpose

This document defines repository-level operating instructions for AI-assisted development on Belay.

GitHub is the canonical source of truth.

Do not rely on conversation history when repository state can be verified directly.

---

# Session Workflow

Every Belay engineering session must follow this sequence:

1. Synchronize with the repository.
2. Review this AGENTS.md file.
3. Review docs/HANDOFF.md.
4. Review constitution/README.md.
5. Review docs/Architecture.md.
6. Review docs/ROADMAP.md.
7. Review docs/DECISIONS.md.
8. Understand the existing implementation before changing it.
9. Produce an implementation plan before significant changes.
10. Implement.
11. Verify.
12. Update documentation affected by changes.
13. Update docs/HANDOFF.md at session close.
14. Update docs/OperatorChecklist.md with any action only the owner can take.

---

# Any Agent, Any Provider

Belay is worked on by more than one person, each directing their own AI agent,
and those agents come from different providers. These instructions apply to all
of them equally. Nothing in this repository may assume which AI service is
reading it. The owner ruled this on 2026-09-19 (`docs/OwnerDecisions.md`
Part 11).

**Step 1 of the workflow is not optional, and "synchronize" means all of:**

- fetch the remote and compare your `main` with it;
- read the commits made since you, or your notes, last saw the repository;
- list the open pull requests and the open Issues.

Another contributor may have changed `main` an hour ago. **Anything you
remember, and anything a provider's memory feature tells you, is a dated
snapshot that the repository overrules.** Do not act on it until you have
checked it against the repository.

**Shared knowledge lives here, not in a provider's memory.** If you learn
something the next agent needs, write it into the repository: state into
`docs/HANDOFF.md`, owner rulings into `docs/OwnerDecisions.md`, lessons that
bind every agent into this file. A lesson that exists only in one provider's
memory, skills or project settings is invisible to every other contributor, and
for Belay's purposes it does not exist. Provider-specific files (for example
`CLAUDE.md` or `.claude/skills/`) may exist as thin conveniences. They must
never be the only place a rule is written.

**`docs/HANDOFF.md` is thousands of lines long, because nothing in it is ever
deleted.** You do not need all of it to start. Read "Belay Session Handoff" (the
opening section), "Highest Priority Next Task", and "Working Agreement"; consult
"Open Findings" for the finding you are working on. The rest is the archive of
earlier sessions. Later entries stand in front of earlier ones without rewriting
them, so within a section, the top-most dated block is the current one.

**The adversarial review is a procedure, not a product feature.** Some documents
refer to it by one provider's command name (`/belay-review`). For any other
agent it is: run `python scripts/review_due.py` to learn whether a review is due
and which finding numbers to use, then follow
`.claude/skills/belay-review/SKILL.md` and its `references/red-team-checklist.md`
by hand. They are plain instructions.

## How work is claimed and landed

1. Work from a fork, and only once the owner has invited you to start. Nobody
   pushes to `main`.
2. One Issue, one branch, one claimant. Claim the Issue before starting. If it
   is already claimed, pick something else.
3. Open a pull request using the template. **The continuous integration run on
   the pull request is the gate. A green run on your own machine is not.** It
   has already happened here that files present only on one machine made a
   local run pass while the pull request failed.
4. **Get an independent pass before calling anything verified.** A different
   session or a different model, told to falsify the work: mutate the source and
   confirm a test goes red, run the real thing, recount every number. Never
   report work as verified on the strength of your own review. This repository
   has measured that an author's own pass finds almost nothing and a fresh one
   finds several defect-grade errors every time. Run it before the change lands,
   not after.
5. Two agents agreeing is not validation. Cross-review catches mistakes. It
   replaces none of the evidence gates in `constitution/`.

## What only the owner may change

`constitution/`, `departments/`, `workflows/`, `Knowledge/`, the markdown under
`strategies/` (all frozen by ADR-002), `docs/OwnerDecisions.md`, the status of
any ADR in `docs/DECISIONS.md`, `LICENSE`, and the repository's settings. An
agent may *propose* a change to any of these in a pull request. It may not treat
its own proposal as ruled. When the owner rules, record the owner's own words.

## Asking the owner

One question at a time, in plain language, each with a recommendation and the
reasons. The owner is not a software developer and delegates repository
mechanics; do not hand a check back to the owner that you can run yourself.

## Citations and counts

- Paste the exact query or command beside any count, rate, or "this appears
  nowhere" claim. A paraphrased search has produced false claims here twice.
- Never state a count you did not count, or a rate whose denominator a reader
  cannot reconstruct.
- After any inventory produced by a smaller or cheaper model, verify at least
  one of its facts yourself before building on it. One such inventory here was
  invented, with line numbers.
- Inserting lines into a long document moves every line citation that points
  below the insertion. Repoint them in the same change.

## Secrets, accounts and brokers

Never commit, print, or copy into a pull request: credentials, tokens, session
files, account identifiers, personal file paths, email addresses, balances,
positions or trade history. No agent connects Belay to a broker, places an
order, or attaches a trading-capable tool to an unattended process. Belay is
paper-first, and order placement is outside every contributor's remit until the
constitution's gates say otherwise.

---

# Determinism and Provider Independence

The owner ruled both essential for any supporting work on 2026-09-19
(`docs/OwnerDecisions.md` Part 11). They bind the software as well as the people
building it.

**Deterministic.** The same inputs must give the same outputs, on any machine,
on any day.

- No test touches the network. Adapters take an injected transport.
- Code that needs the time, a random number, or an environment setting receives
  it as an input. It does not reach out for it.
- Collection from a live source is the one place the world leaks in. Contain it:
  capture once, store the raw response unchanged with a fetch record, and compute
  only from the stored file.
- Pin what results depend on: data versions, library versions where behaviour
  differs, and the parameters of any run.
- Storing a model's answer does not make the step deterministic. If re-running
  Belay would call a model again, or if a stored model answer *decides* anything
  (a promotion, a trade, a risk verdict) rather than being weighed as evidence
  by deterministic code, the change breaks this rule.
- **An AI model's output is not reproducible.** A model may help *build* Belay.
  It may not sit inside Belay's decision path as a live call. `docs/EndState.md`
  records what is and is not yet settled about models at run time; until the
  owner rules further, treat any model output that Belay consumes as an input
  that must be captured, frozen, and attributed like any other evidence, and
  never as a step that is re-run.

**Independent of any AI provider.**

- Nothing under `framework/`, `scripts/` or `tests/` may require a particular AI
  service, its connectors, its scheduled agents, its memory, or its file formats
  in order to run.
- Anything an operator must run on a schedule is an ordinary script that any
  operator can run on hardware they control.
- If a provider-specific convenience exists (a skill, a routine, a prompt file),
  the rule it encodes is also written here or in `docs/`, in plain language, so
  an agent from another provider can follow it.

---

# Engineering Priorities

Prioritize decisions in this order:

1. Architectural integrity
2. Correctness
3. Capital preservation
4. Reproducibility
5. Maintainability
6. Simplicity
7. Extensibility
8. Performance

Do not sacrifice architecture for short-term implementation speed.

---

# Belay Principles

Belay is a production-grade, evidence-driven autonomous trading platform.

The system must prioritize:

- evidence before capital
- validation before promotion
- deterministic behavior
- reproducibility
- explicit interfaces
- immutable state transitions
- clear ownership boundaries

---

# Architecture Rules

## Artifact-Centric Design

Artifacts are the primary communication boundary between Belay components.

Services should follow:

Input Artifact

↓

Processing

↓

Output Artifact

Do not introduce hidden shared state between services.

---

## Immutability

Prefer immutable data structures.

Do not silently mutate historical records.

Changes to evidence, validation, or lifecycle state should create new versions or new artifacts.

---

## Dependency Design

Prefer:

- composition over inheritance
- dependency inversion
- explicit interfaces
- small cohesive components
- strongly typed models

Avoid:

- global mutable state
- magic values
- duplicated abstractions
- parallel implementations
- hidden coupling

---

# Evidence Standards

Belay is evidence-driven.

Any recommendation, promotion decision, or capital allocation process should be supported by measurable evidence.

Avoid opinion-based system behavior.

Evidence should maintain:

- provenance
- reproducibility
- validation history
- confidence information

---

# Capital and Strategy Governance

No trading strategy should advance based only on implementation readiness.

Strategies must progress through documented evidence gates.

Capital allocation authority belongs to the governance layer defined by the Belay Constitution.

---

# Documentation Requirements

Documentation is part of the product.

Update relevant documents when architecture changes:

```
constitution/          governance layer, 11 documents; frozen by ADR-002
docs/
├── Architecture.md
├── ROADMAP.md
├── DECISIONS.md
└── HANDOFF.md
```

The constitution is a directory, not a single file. `constitution/README.md` is its
entry point.

Important architectural decisions must be recorded in DECISIONS.md.

---

# Testing Expectations

New functionality should include appropriate verification.

Prioritize tests for:

- domain contracts
- artifact integrity
- validation logic
- serialization
- lifecycle transitions
- persistence boundaries

---

# Change Discipline

Before adding new functionality:

1. Verify whether an existing abstraction already solves the problem.
2. Avoid creating duplicate systems.
3. Prefer refactoring existing architecture over adding parallel paths.
4. Document significant tradeoffs.

---

# Current Priority

This file does not name the current priority, on purpose. It named one until
2026-09-19 ("strengthening the Artifact Framework") and that went stale while
the work moved on, so an agent following this file literally would have started
on finished work.

The current priority is whatever `docs/HANDOFF.md` says under "Highest Priority
Next Task", narrowed by the open Issues on GitHub. Run `python scripts/status.py`
to see the repository's real state; it is re-derived on every run and outranks
any prose, including this file.
