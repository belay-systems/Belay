# Belay Architecture

Belay is two layers joined by one contract.

Recorded per ADR-002, `docs/DECISIONS.md`.

---

## Governance Layer

Belay has four permanent departments.

Research

Validation

Operations

Knowledge

The four departments are the governance layer, not the whole system.

The governance layer specifies what evidence is required and who may promote.

It comprises `constitution/`, `departments/`, `workflows/`, `Knowledge/` and the
markdown under `strategies/`.

It remains prose.

---

## Mechanics Layer

The mechanics layer produces the evidence the governance layer requires.

It comprises `framework/`.

All new code belongs here.

---

## The Contract

The Artifact is the contract between the two layers.

Mechanics emit Artifacts.

Governance consumes Artifacts.

Neither layer reaches across the boundary by any other means.

---

Departments communicate through structured reports rather than unrestricted memory.

This minimizes bias and improves reproducibility.

No department owns capital.

Capital is governed exclusively through the Constitution.
