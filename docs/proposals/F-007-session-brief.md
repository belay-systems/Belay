# F-007 — session brief

**Status: authorized work, not a proposal.** Ruled for fix by the owner
2026-08-14 (`docs/OwnerDecisions.md` Part 8). Raised in
`reports/review/2026-08-14-review.md` as Critical.

This brief exists so the session doing the work starts from executed evidence
rather than re-deriving it. Everything below was run against `main` at `dbfd07f`.

---

## The defect in one sentence

`ArtifactFactory.create()` refuses to mint a STRATEGY artifact past `IDEA`;
`Artifact(...)` followed by `ArtifactIntegrity.sign()` mints exactly the same
artifact, and it validates, verifies, persists and reloads intact standing at
`PRODUCTION`.

## Reproduce it before changing anything

```python
from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import ArtifactType, StrategyLifecycle
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.validator import ArtifactValidator
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.repository import ArtifactRepository
import tempfile

# The guarded path — refuses, as F-001 intended.
try:
    ArtifactFactory().create(identifier="STRAT-0001", title="Newborn",
                             artifact_type=ArtifactType.STRATEGY,
                             strategy_stage=StrategyLifecycle.PRODUCTION)
except ValueError as e:
    print("factory refused:", e)

# The unguarded path — same destination, two lines.
art = Artifact(id="STRAT-0002", title="Born at production",
               type=ArtifactType.STRATEGY,
               strategy_stage=StrategyLifecycle.PRODUCTION)
signed = ArtifactIntegrity.sign(art)
print("stage           ", signed.strategy_stage)
print("integrity ok    ", ArtifactIntegrity.calculate_hash(signed) == signed.integrity_hash)
print("validates       ", ArtifactValidator().validate(signed))

repo = ArtifactRepository(root=tempfile.mkdtemp())
repo.save(signed)
loaded = repo.get("STRAT-0002")
print("reloaded stage  ", loaded.strategy_stage)
```

Observed output on `dbfd07f`:

```
factory refused: a strategy cannot be created at stage <StrategyLifecycle.PRODUCTION: ...>
stage            StrategyLifecycle.PRODUCTION
integrity ok     True
validates        True
reloaded stage   StrategyLifecycle.PRODUCTION
```

## Why the existing defence does not cover it

`framework/artifacts/factory.py:55-60` argues the round trip is safe because "the
repository verifies the integrity hash on read, so a stage that was earned
survives the round trip while a hand-edited one does not."

**The hand-editing half is true.** Verified both ways — editing
`strategy_stage: Idea` to `Production` in a saved strategy's YAML, and editing
`observations: 28` to `2800` in a copy of `artifacts/RPT-0001/1.0.0.yaml`. Both
are refused by `ArtifactRepository.get()` with "integrity hash does not match its
content".

**The gap is that nobody has to hand-edit.** `ArtifactIntegrity.sign()`
(`framework/artifacts/integrity.py:71`) is a public classmethod that computes and
attaches the hash for any artifact handed to it. The constructor's output is
signed by the same function the repository later verifies against, so the
signature agrees with the content and the read-time check has nothing to catch.
The check defends against *tampering*, not against *construction*.

## The pattern to copy is in the file next door

`framework/artifacts/validator.py:227-232` already does this for `evidence_level`
— it re-derives the grade from the evidence records and refuses a mismatch. Its
comment states the reasoning verbatim:

> Without this an artifact built by calling `Artifact()` directly could claim
> Level A while carrying nothing but hypotheses, and that claim is what a
> promotion gate reads.

`strategy_stage` is the same kind of claim, read by the same kind of gate.
`_validate_lifecycle` (`framework/artifacts/validator.py:145-168`) checks that it
*is* a `StrategyLifecycle`, that STRATEGY artifacts have one and that others do
not — never *which*.

## What was ruled, and what was not

**Ruled:** a STRATEGY artifact cannot come into existence past `IDEA` by any
construction path, sanctioned or not. The check belongs where the claim is *read*
(the validator), not only where it is *issued* (the factory).

**Not ruled, and attack this first:** the proposal's test for "birth" is *version
`1.0.0` with no `parent_hash`*. That is the reviewer's construction and no
constitutional document states it. Two known ways it could be wrong:

- A legitimate artifact might be re-issued at `1.0.0` in a fresh repository after
  a migration, with a stage it genuinely earned elsewhere.
- The version chain, not the version *number*, may be the real carrier of "this
  was climbed" — `ArtifactRepository.latest()` already reasons this way
  (`framework/artifacts/repository.py:86-113`: "A strategy can now move backward,
  so its current stage is no longer the highest stage it ever reached").

If the version test is wrong, **the finding is still real and the fix is still
owed** — only its shape changes. Say so in the commit rather than quietly
widening scope.

**Also not ruled:** whether `ArtifactFactory` keeps its own guard. The proposal
says keep it for the earlier and clearer error message. That is a preference.

## Definition of done

1. **Tests first, run red against unchanged code**, and record that they were red.
   This repository's standing practice; `CHANGELOG.md:124` is the precedent —
   "Against the pre-fix source the nine refusal cases all reported `DID NOT RAISE
   ValueError`, which is the defect stated as a test result."
2. Every construction path refuses a post-`IDEA` birth: `ArtifactFactory.create()`,
   direct `Artifact(...)` through `ArtifactValidator`, and the repository's
   read path.
3. Legitimate movement still works — a strategy that climbs through
   `validate_transition` reaches every later stage and round-trips through
   `ArtifactRepository` unharmed. This is the test most likely to be forgotten and
   the one that stops the fix from being a wall.
4. `ArtifactSerializer.load()` (`framework/artifacts/serializer.py:134`) still
   reconstructs an earned late-stage artifact. If the new check breaks
   deserialization, that is a design problem with the check, not an acceptable
   cost.
5. Suite green from 626 with the new tests added.
6. `docs/FINDINGS.md`: move `A Strategy Can Still Be Signed Into Existence At
   Production (F-007)` from Open to Closed, with the date and pull request.
   **And correct the F-001 entry** (`docs/HANDOFF.md:2150-2194`), which reads
   as though the hole is closed. That archive is frozen (Part 29): write the
   correction in this session's `docs/sessions/` record, and name the lines.
7. `CHANGELOG.md` entry in the existing style.

## Hard constraints

- **One finding, one branch.** F-008 through F-013 are ruled for fix too and are
  not this session's work. `docs/OwnerDecisions.md` Part 8 gives the recommended
  order and the reasoning for it.
- **The independent verification pass runs BEFORE the change lands, not after.**
  This is the standing rule in `docs/HANDOFF.md`, earned on 2026-08-02: where two
  documents disagree about when a check happens, the stricter one governs. Four
  consecutive sessions have shipped work whose author's own review found nothing
  and an independent pass then found 4, 6, 6 and 19 defect-grade errors. Signing
  your own work is the exact shape of this finding.
- Do not touch `origin/f003-awaiting-verification`. F-003's fix is gated on its
  own unfinished pass and this ruling does not release that gate.
