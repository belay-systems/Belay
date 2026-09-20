# Document Metadata Standard

> **Status: specified, not applied.** Exactly one document carries this block —
> `strategies/StrategyTemplate.md` — and it uses `owner:` where this standard says
> `author:` and omits five required fields. (The count of documents is deliberately
> not stated: it was written as 81, and was 100 by 2026-07-31.
> `tests/test_governance_conformance.py` derives both figures instead.)
> Recorded in `docs/HANDOFF.md`. Until it is applied, tooling such as
> `scripts/status.py` must parse prose with regular expressions — which is exactly
> the cost this standard exists to remove.
>
> This file was named `NEW STANDARD`, with no extension, at the repository root.
> It was invisible to every search and every session until 2026-07-26.

Every document in Belay will begin with a standard metadata block.

Example:

---
id: STRAT-0017
title: Covered Premium Strategy
type: Strategy
status: Paper
version: 1.3.0
author: Belay
created: 2026-07-05
updated: 2026-07-05
evidence: B
regime:
  - Bull
  - Neutral
tags:
  - income
  - options
  - premium
relationships:
  created_from:
  validated_by:
  superseded_by:
---

This allows Claude Code to index every document deterministically without parsing prose.
