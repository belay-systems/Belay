# Contributing to Belay

Belay is built by a small number of people, each directing an AI coding agent.
This page is for the person. The agent's instructions are in `AGENTS.md`, and
they are the same whichever AI service you use.

Belay is proprietary. Read `LICENSE` before contributing: section 3 sets the
terms every contribution is submitted under.

**Contribution is by invitation.** Until the owner has invited you and told you
the repository is ready for outside work, read, but do not claim or start
anything.

## The short version

1. **Fork** the repository. Nobody pushes to `main`, including the owner.
2. **Claim a task.** Pick an open Issue and comment that you are taking it, or
   open a new Issue describing what you intend to do and wait for the owner to
   agree. One Issue, one branch, one person. If an Issue is claimed, leave it.
3. **Point your AI agent at `AGENTS.md`** and have it follow the session
   workflow there from step 1. Do not brief it from memory or from an old chat.
4. **Open a pull request** and fill in the template. Continuous integration runs
   on every pull request. A green run on your own machine does not count; the
   run on the pull request is the gate.
5. **Get an independent pass.** Before asking for a merge, have a *different*
   session or a different model try to break the change, and paste what it
   found into the pull request. See "Why the independent pass" below.
6. **The owner merges.** Anything that touches a governance record is the
   owner's decision alone (see the list in `AGENTS.md`).

## Setting up

Python 3.11, 3.12 or 3.13.

```bash
pip install -e ".[dev]"
```

```bash
python -m pytest -q
```

```bash
python scripts/status.py
```

The first installs Belay with its test tools. The second runs the whole suite;
it touches no network. The third builds the status dashboard, which re-derives
the project's real state from the repository on every run.

## What makes a good first task

Something self-contained whose result continuous integration can check: closing
one finding from the register in `docs/HANDOFF.md`, adding a missing test, or
running an independent pass on somebody else's open pull request or proposal.
An independent pass is real work here, not a courtesy.

## Why the independent pass

This project measured it. Across several sessions, an author's own review of
their work found almost no defects, and a fresh reviewer with no knowledge of
how the work was written found several defect-grade errors every time. The
record is in `docs/HANDOFF.md`. Two agents agreeing is still not validation:
it catches mistakes, and it replaces none of the evidence gates in
`constitution/`.

## What never goes in the repository

Passwords, tokens, API keys, account numbers, broker session files, personal
file paths, email addresses, balances, positions, trade history, or market data
whose licence forbids sharing it. The market data store is ignored by git on
purpose. If you are unsure, leave it out and ask in the Issue.

## Asking the owner something

Decisions belong to the owner and are recorded in `docs/OwnerDecisions.md`. Put
questions one at a time, in plain language, each with your recommendation and
the reasons. Record the owner's answer in their own words.
