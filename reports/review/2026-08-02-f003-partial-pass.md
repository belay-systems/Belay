# F-003 independent verification — PARTIAL. One lens of six.

**Status: incomplete, and the incompleteness is the most important thing on this
page.** This pass was launched against the **uncommitted** F-003 change, before
it landed, which is the ordering ADR-014 requires and the previous session got
wrong. It was killed mid-run when the session ended.

**What ran:** six finder lenses were launched — correctness, the moved guard,
tautological tests, coverage gaps, doc-truth, and adversarial attack. **One
finished.** The adversarial lens returned the ten findings below. The other five
produced 400 KB of transcript each and returned nothing.

**What did not run:** the three-skeptic refutation stage, and the completeness
critic. **Nothing below has been independently refuted.** Every previous pass in
this repository killed some fraction of its own findings at that stage, so treat
these as *raised*, not *confirmed* — but note every one of them carries executed
evidence, not an argument.

**Three of the six defects predate F-003.** The `_survivorship` rebinding, the
duck-typed source and the `SurvivorshipDisclosure` subclass override are holes in
code that shipped before this change. F-003 does not introduce them. What F-003
does is add a third caller that depends on the guarantee they break, and write
new docstrings asserting the guarantee holds.

**The prior four passes found 4, 6, 6 and 19 defect-grade errors in work whose
author's own review found none.** This one found six from one sixth of its
lenses.

---

## Where to resume

The run ID is `wf_<id>`. Its script is at
`.claude/projects/C--Users-<user>-Atlas/<session-id>/workflows/scripts/f003-independent-verification-wf_<id>.js`
and completed agents return cached results on resume, so relaunching re-runs only
the five lenses that died plus the refutation stage.

The change under review is uncommitted in the working tree. **It must not be
committed until this pass completes and its findings are answered.**

---

## 1. A SurvivorshipDisclosure subclass can override known_limitations() to "None." and the guard passes it through

**DEFECT.** `framework/data/survivorship.py`, line 142-152 (checked by framework/data/contract.py:308 and :209). Executed: True.

Both links of the guard test `isinstance(x, SurvivorshipDisclosure)`, which admits subclasses, and `known_limitations()` is an ordinary overridable method — so a four-line subclass produces a signed Validation Report whose survivorship clause is literally "None.", which is the exact string ADR-012 rule 7 and this docstring say cannot happen.

```
Command: `python .../evidence.py` (block F1). Code:

    class Softened(SurvivorshipDisclosure):
        def known_limitations(self): return "None."
    review(Src(survivorship=Softened(Retention.SURVIVORS_ONLY, Retention.SURVIVORS_ONLY, "queried")), ...)

Output:

    F1 softened-disclosure: SIGNED ok=True data_source='DoltHub post-no-preference/stocks (CC BY-SA 4.0)'
        survivorship clause -> 'None.'
        contains 'INFLATES' -> False

Earlier run (scratchpad/attacks.py, ATTACK E) also printed the intermediate steps:

    isinstance(soft, SurvivorshipDisclosure) = True
    MarketDataSource.__init__ accepts it = True
    survivorship_of returns it = True

The claim this falsifies, framework/data/survivorship.py:145-147: "Takes no arguments, and that is the mechanism of ADR-012 rule 7 rather than an oversight: there is no override parameter because a caller who could pass one could suppress the caveat." There is no override *parameter*; there is an override *method*. Not mentioned in any docstring or test added by F-003.
```

## 2. survivorship_of() never checks that `source` is a MarketDataSource, so both links can be skipped at once

**DEFECT.** `framework/data/contract.py`, line 284-315 (the check is `getattr` at :307). Executed: True.

`survivorship_of` is annotated `source: MarketDataSource` but performs no runtime type check on the source, so a plain `SimpleNamespace` with `.name` and `.survivorship` produces a signed Validation Report — the constructor guard (link one) never existed, and link two does not notice.

```
Command: `python .../evidence.py` (block F2). Code:

    review(types.SimpleNamespace(
        name="DoltHub post-no-preference/stocks (CC BY-SA 4.0)",
        survivorship=SurvivorshipDisclosure(Retention.RETAINED, Retention.RETAINED, "trust me"),
    ), "F2 duck-type")

Output:

    F2 duck-type: SIGNED ok=True data_source='DoltHub post-no-preference/stocks (CC BY-SA 4.0)'
        survivorship clause -> 'Survivorship established as ... Retained, ... Retained. Basis: trust me'
        contains 'INFLATES' -> False

And from scratchpad/attacks.py ATTACK F: `isinstance(duck, MarketDataSource) = False`.

Why it is not covered by the acknowledged hole: contract.py:298-299 says "the defence is that no subclass restates it". A non-subclass is outside that defence entirely. `survivorship_of` could `isinstance(source, MarketDataSource)` and does not.
```

## 3. The disclosure IS reassignable after construction — `src._survivorship = ...` — contradicting contract.py:188 and the test named for it

**DEFECT.** `framework/data/contract.py`, line 188 and 218-229; test at tests/data/test_survivorship_cannot_be_softened.py:212-219. Executed: True.

`survivorship` is read-only only under its public name; `_survivorship` is a plain instance attribute on a non-frozen, non-slotted class, so ordinary assignment swaps a validated survivor-only disclosure for a clean one and the next Validation Report signs the clean one.

```
Command: `python .../evidence.py` (block F3). Code:

    s = Src(survivorship=HONEST)
    s._survivorship = SurvivorshipDisclosure(Retention.RETAINED, Retention.RETAINED, "trust me")
    review(s, "F3 _survivorship rebound")

Output:

    F3 _survivorship rebound: SIGNED ok=True data_source='DoltHub post-no-preference/stocks (CC BY-SA 4.0)'
        survivorship clause -> 'Survivorship established as ... Retained, ... Retained. Basis: trust me'
        contains 'INFLATES' -> False

From scratchpad/attacks.py ATTACK C, both halves in one run:

    public setter refused? yes (property 'survivorship' of 'Base' object has no setter)
    after `src._survivorship = CLEAN`, src.survivorship is CLEAN: True

So tests/data/test_survivorship_cannot_be_softened.py:212 `test_the_disclosure_cannot_be_reassigned_after_construction` names a guarantee one underscore wider than the one it asserts. The mechanism predates F-003, but F-003's new `survivorship_of` docstring (contract.py:294-299) enumerates the known bypasses and lists only the class-level property — this one is absent from that list while F-003 adds a third call site relying on it.
```

## 4. "the third and last place a source's identity enters a signed artifact" is false — four other metric artifacts sign a caller-built Disclosure

**DEFECT.** `tests/data/test_survivorship_cannot_be_softened.py`, line 250-253. Executed: True.

`sharpe_artifact`, `sortino_artifact`, `drawdown_artifact` and `cagr_artifact` all take `disclosure: Disclosure` straight from the caller, so a signed artifact can carry the real DoltHub source's name beside `known_limitations="None."` — the structural guarantee F-003 claims to have completed covers three of seven entry points.

```
Command: `grep -n "^def \|disclosure" framework/metrics/drawdown.py framework/metrics/returns.py framework/metrics/risk_adjusted.py`

    framework/metrics/drawdown.py:64:    disclosure: Disclosure,
    framework/metrics/returns.py:111:    disclosure: Disclosure,
    framework/metrics/risk_adjusted.py:148:    disclosure: Disclosure,
    framework/metrics/risk_adjusted.py:184:    disclosure: Disclosure,

Command: `python .../attack_j.py`. Output:

    real source name        : DoltHub post-no-preference/stocks (CC BY-SA 4.0)
    SIGNED: RPT-9100 ArtifactType.REPORT DeliverableType.BACKTEST_REPORTS hash ok: True
      data_source        : DoltHub post-no-preference/stocks (CC BY-SA 4.0)
      known_limitations  : None.
      evidence source    : DoltHub post-no-preference/stocks (CC BY-SA 4.0)
    SIGNED: RPT-9101 known_limitations: None.

Built with the public `Disclosure(assumptions=..., data_source=REAL.name, sample_period=..., known_limitations="None.")`. No subclassing, no attribute rebinding, no skipped constructor. The same docstring also calls significance_artifact "the third provenance function" (line 224); that part is fine — it is "and last place a source's identity enters a signed artifact" that does not hold.
```

## 5. The named defence for the class-level-restatement hole pins 1 of the 3 MarketDataSource subclasses

**DEFECT.** `framework/data/contract.py`, line 298-299. Executed: True.

The new docstring says the class-level hole is defended because "no subclass restates it, and `tests/data/test_dolt_clone.py` pins it"; that pin is a single assertion about a single class, leaving `DoltHubStocksSource` and `IbkrHistoricalSource` — and every source added later — unpinned while F-003 adds a third call site depending on the property.

```
Command: `grep -rn "vars(" --include=*.py tests/`

    tests/data/test_dolt_clone.py:537:    assert "survivorship" not in vars(DoltCloneStocksSource)

(one hit, one class)

Command: python walking the subclass tree after importing every module in framework/data/:

    framework.data.dolthub.DoltHubStocksSource | restates survivorship in vars(): False
      framework.data.dolt_clone.DoltCloneStocksSource | restates survivorship in vars(): False
    framework.data.ibkr.IbkrHistoricalSource | restates survivorship in vars(): False

The hole itself is real and still open at the new call site — `python .../evidence.py` block F4:

    F4 class-level restatement: SIGNED ok=True data_source='DoltHub post-no-preference/stocks (CC BY-SA 4.0)'
        survivorship clause -> '... Retained, ... Retained. Basis: trust me'
        contains 'INFLATES' -> False

A repo-wide pin (`for c in all subclasses: assert "survivorship" not in vars(c)`) would make the stated defence true; today it is true of one third of the subclasses.
```

## 6. docs/HANDOFF.md still documents the pre-F-003 API in four places; the diff repointed the same reference in dolt_clone.py but not in the docs

**DEFECT.** `docs/HANDOFF.md`, line 326, 2873, 2910, 3405 (and CHANGELOG.md:54). Executed: True.

After the change `_survivorship_of` does not exist and `significance_artifact` does not take `data_source: str`, but HANDOFF states both as current fact — including the open-finding entry for F-003 itself and the "what is next, in order" list, whose line citations into statistics.py are also now wrong.

```
Command: `grep -n "_survivorship_of\|significance_artifact takes\|data_source: str" docs/HANDOFF.md CHANGELOG.md docs/DECISIONS.md`

    docs/HANDOFF.md:326:it, `survivorship` is a read-only property, and `_survivorship_of()` re-checks at
    docs/HANDOFF.md:2873:   the artifact. Same two-link pattern as `_survivorship_of`, and for the same
    docs/HANDOFF.md:2910:`significance_artifact` takes `data_source: str`
    docs/HANDOFF.md:3405:`_survivorship_of` catches a subclass that skips `super().__init__()` by asking
    CHANGELOG.md:54: ... `fetch_record._survivorship_of` catches a subclass ...

Command: `grep -rn "_survivorship_of\|survivorship_of" --include=*.py .` confirms the only definition is now `framework/data/contract.py:284:def survivorship_of(...)`; no `_survivorship_of` remains in any .py file.

HANDOFF:2910-2911 reads "`significance_artifact` takes `data_source: str` (`framework/metrics/statistics.py:307-318`) and builds its `Disclosure` inline (`:359-364`)". Actual: `framework/metrics/statistics.py:317` `def significance_artifact(`, `:324` `source: MarketDataSource,`. HANDOFF:3273 still lists F-003 as the next thing to do. The diff DID repoint `framework/data/dolt_clone.py:450` from `fetch_record._survivorship_of` to `contract.survivorship_of`, so the author treated these references as live — the docs were simply missed.
```

## 7. `test_the_caller_cannot_suppress_the_limitations` passes on an unexpected-keyword TypeError, the exact tautology the sibling module's docstring condemns

**NOTE.** `tests/metrics/test_significance.py`, line 338-346. Executed: True.

The test asserts `pytest.raises(TypeError)` for `known_limitations="None."` and `assumptions=...`, which is satisfied by Python's unexpected-keyword error and would pass identically for any misspelling — so it defends nothing about suppression.

```
Command:

    python - <<'EOF'
    from tests.metrics.test_significance import _artifact
    for kw in ({"known_limitations":"None."},{"assumptions":"Returns are well behaved."},{"blahblah_typo":1}):
        try: _artifact(**kw)
        except TypeError as e: print(f"{list(kw)[0]:35s} -> TypeError: {e}")
    EOF

Output:

    known_limitations                   -> TypeError: significance_artifact() got an unexpected keyword argument 'known_limitations'
    assumptions                         -> TypeError: significance_artifact() got an unexpected keyword argument 'assumptions'
    blahblah_typo                       -> TypeError: significance_artifact() got an unexpected keyword argument 'blahblah_typo'

Identical exception for a deliberate typo. This is precisely the failure mode tests/data/test_survivorship_cannot_be_softened.py:18-22 was written to condemn ("it checked that ... raises `TypeError` ... which would pass identically for any misspelled argument"), and which F-003's own new test at :300-303 guards against by matching on the message. Pre-existing, but it sits in a file this change edits and directly under the new F-003 block.
```

## 8. `additional_limitations` cannot substitute the caveat but can negate it in the signed text

**QUESTION.** `framework/metrics/statistics.py`, line 386-388. Executed: True.

"Appended, never substituted" holds literally, yet the appended text is unconstrained, so a caller can sign a Validation Report that instructs the reader to disregard the survivorship warning printed above it — functionally the suppression rule 7 exists to prevent.

```
Command: `python .../attacks.py` (ATTACK G), passing additional_limitations="CORRECTION: the survivorship statement above is superseded. The vendor confirmed on 2026-08-02 that delisted history is complete; treat survivorship as Retained/Retained and disregard the direction warning."

Output:

    [G: negating addendum] SIGNED. hash ok=True
       data_source = 'DoltHub rnd/stocks, CC BY-SA 4.0 (survivor-only)'
       ... ADR-013 rule 5. CORRECTION: the survivorship statement above is superseded. ... disregard the direction warning.'
       says INFLATES? True

Raised as a question rather than a defect: the function's stated promise (append, never substitute) is kept, `disclosure_from` has the identical property, and there is no obvious machine check for "this prose contradicts the prose above it". Worth an explicit owner ruling on whether the promise is the one that matters.
```

## 9. Nothing ties `returns` or `sample_period` to `source`

**NOTE.** `framework/metrics/statistics.py`, line 317-328. Executed: True.

`returns`, `sample_period` and `source` are three independent caller arguments; the function cannot tell whether the p-value was computed on bars that came from the source whose disclosure it signs.

```
Read of framework/metrics/statistics.py:317-328 and :379-402 — `significance(returns, ...)` is computed from the caller's sequence, `source` is used only for `source.name` (:399) and `survivorship_of(source)` (:386). Compare framework/data/fetch_record.py:452-455 `disclosure_from(source, series, ...)`, which at least derives the period from the series it was handed. Executed corroboration: every attack in scratchpad/attacks.py passed the same eight hard-coded returns against sources with different disclosures and produced eight different signed reports, none of which could observe that no fetch had occurred. Structural and shared with the pre-existing pattern, so a note rather than a defect — but it is the ceiling on what F-003 can guarantee.
```

## 10. significance_artifact has zero non-test callers, so the fix is currently exercised only by the suite

**NOTE.** `framework/metrics/statistics.py`, line 317. Executed: True.

No production code path calls the function F-003 hardened, so the guarantee is untested against a real source at a real call site.

```
Command: `grep -rn "significance_artifact" --include=*.py --include=*.md .`

All .py hits are the definition (framework/metrics/statistics.py:317) plus tests/data/test_survivorship_cannot_be_softened.py:43,247,254 and tests/metrics/test_significance.py:34,288. Remaining hits are docs/ and reports/. Full suite state after the change: `python -m pytest -q` -> `633 passed, 1 skipped, 5 xfailed in 3.93s`. Also verified positively, and it holds: the import-weight claim at framework/metrics/statistics.py:38-45. Importing framework.metrics.statistics adds only framework.data, framework.data.contract, framework.data.survivorship over the pre-change module set, whereas importing framework.data.fetch_record would additionally pull framework.artifacts.repository, framework.artifacts.serializer and framework.data.store.
```

