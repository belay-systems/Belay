# Belay Red-Team Checklist

Every entry here names a failure mode that either has already occurred in this
repository, or would not be caught by the existing suite. Generic code review
finds none of them.

Work each entry by trying to **construct** the failure. The question is never
"is this handled?" — it is "what input, what dataset, what regime makes this
wrong, and can I show that input exists?"

Absence of a finding is only reportable if you can say what you looked at.

---

## A. Data integrity

The dataset is the most dangerous thing in Belay, because a defect here is
invisible in every downstream number and makes every strategy look better than
it is.

**A1. Survivorship — the dataset, not the code path.**
`tests/data/test_survivorship.py` and
`tests/data/test_survivorship_cannot_be_softened.py` guard the *code*. They
prove Belay refuses to accept a series that declares itself survivorship-free
when it is not, and that the refusal cannot be weakened. They cannot prove the
vendor's database contains delisted names.

Check: for whatever data has actually landed, can you name one company that was
delisted inside the sample window and confirm it is present? If not, the guard
is passing over a dataset nobody has verified. That is the single most expensive
possible defect in this project and it will not turn a test red.

**A2. Lookahead.** For each rule, identify the bar on which the decision is made
and the bar the data comes from. A rule that uses a session's close to decide a
trade in that same session is free money that does not exist. Check every
`shift`, every window alignment, every join on date.

**A3. Point-in-time.** Fundamentals get restated. A rule reading today's
revenue figure for a decision five years ago is using information that did not
exist. Does the store version restatements (ADR-013 rule 4 counts "the number of
times the vendor's answer changed") or overwrite them?

**A4. Provenance.** ADR-013 requires a fetch record carrying a content hash.
Check every series in use has one, and that the hash was verified rather than
merely recorded. `.gitignore:46-49` leans on this: the bytes are not committed
*because* the signed record is considered sufficient. If the record is not
actually verified, that reasoning is hollow and the data is unreproducible.
(Cited as `:39-42` until 2026-09-19, and that citation was **wrong when it was
written**, not rotted: `git show 079f43a:.gitignore` — the commit that created
this checklist — already has the unbounded-growth argument at `:39-42` and the
record-sufficiency claim at `:46-49`. ADR-014 (`a19c24e`) later rewrote
`:46-49` in place. Nothing moved; the line was miscounted once and repeated
for six weeks. Read the file, not this number.)

**A5. Silent gaps.** Missing bars, holidays, halts. Does a gap propagate as
missing, or as a flat return? A flat return is a fabricated observation.

---

## B. Statistical validity

**B1. Multiple testing.** However many rules exist — count them, this repository
has held zero for its whole life so far — how many were tried and discarded to
get them? If that number is not recorded anywhere, the significance of the
survivors cannot be computed, and every p-value in the repo is optimistic by an
unknown factor. ADR-012 governs what Belay may conclude; check it is applied to
the *search*, not just the individual result.

This is the finding most likely to be true and least likely to be looked for.

**B2. Sample adequacy.** `tests/metrics/test_sample_period.py` and ADR-012
define the standard. Check the standard is enforced at the point of promotion,
not merely computed and displayed. A number on a dashboard that nothing gates on
is decoration.

**B3. Regime coverage.** Law IV — past performance is evidence, never proof.
Does the sample contain a genuine drawdown regime, or only the expansion? A
strategy validated exclusively on a bull tape is Level D dressed as Level C.

**B4. Metric conventions.** ADR-011 requires conventions be stated, never
defaulted. Check each metric declares its annualization factor, its risk-free
rate, and its return basis. A Sharpe with an implicit convention cannot be
compared to any other Sharpe, including its own value last month.

**B5. Evidence level inflation.** `constitution/Evidence_Standards.md:39` — the
hierarchy may never be reversed. Look for anything labelled B (paper validated)
whose support is actually C (historical simulation), or C whose support is
really D. The label is a claim and needs a citation like any other.

---

## C. The green-test trap

The suite passes. That is compatible with the suite testing nothing.

**C1. Tautological tests.** For each test, ask: does it assert the *requirement*
or restate the *implementation*? A test that computes the expected value using
the same function under test passes forever, including after the function
becomes wrong.

**C2. Break it mentally.** Pick a function. Invent a plausible bug — an
off-by-one in a window, a flipped comparison, a dropped edge case. Now find the
test that fails. If none does, the coverage is nominal.

**C3. The count is not the signal.** A rising test count measures effort, not
correctness. Never report it as health, and be suspicious of any document that
does.

**C4. Assertion-free tests.** Tests that call code and assert nothing, or assert
only that no exception was raised. They pass by definition.

**C5. What has no test at all.** More useful than reviewing what does. Compare
the modules in `framework/` against `tests/` and name the gaps.

---

## D. Governance conformance

**D1. Any path to capital that skips validation.** Law V, and the reason the
project exists. Trace `StrategyLifecycle`: is there any transition, flag,
override, or test helper that reaches a capital stage without passing through
VALIDATION? A back door in a test fixture is still a back door.

**D2. Zero capital at birth.** `Paper_First_Capital_Doctrine.md:5` — every
strategy begins with zero. Check no default, no constructor argument, and no
deserialization path can produce a strategy that starts funded.

**D3. Human authorization.** `Operational_Constraints.md:31-35` — Belay advises,
humans authorize. Find every code path that could place an order. Confirm each
terminates at a human approval that cannot be configured away.

**D4. Explainability.** Law II prohibits black-box reasoning. Can every
promotion decision produce the evidence it rested on, after the fact, from
stored artifacts rather than from logs that rotate?

**D5. Research/execution independence.** Law VI. Does any execution component
import from research, or share mutable state with it? `AGENTS.md:225` forbids
hidden shared state on architectural grounds; Law VI forbids it on
constitutional ones.

**D6. Retirement preserves.** `Strategy_Retirement.md:22` — Belay never deletes
research. Check retirement archives rather than removes, and that nothing
prunes.

---

## E. Documentary honesty

This section has the highest historical hit rate in this repository.

**E1. Decorative status.** `scripts/belay.py:21` prints four checkmarks and
checks nothing. Find every other health signal, badge, count, or "✓" and read
its source. A status display that cannot fail is worse than none, because it
manufactures the confidence Belay is built to withhold.

**E2. Uncited numbers.** `docs/DocumentStandard.md:5-7` records a count written
as 81 that was 100 by the time anyone checked — and the fix was to have the
conformance suite *derive* it rather than restate it. Find every hardcoded
figure in prose. Each is either derived, cited, or rotting.

**E3. ADR cross-citations.** Check each resolves to text that exists. ADR-002
cited a group of eight items that its source document does not contain, and the
false citation survived inside an Accepted decision until ADR-007
(`constitution/Promotion_Pipeline.md:96-99`).

**E4. Claimed but not built.** Walk `docs/ROADMAP.md` and `docs/EndState.md` for
anything described in the present tense. Confirm each exists. Aspiration written
as fact is how a project loses track of what it is.

**E5. HANDOFF as claim.** `docs/NOW.md` and `docs/sessions/` are a session's
account of its own work. Spot-check their most load-bearing assertions against
the code. They are the documents with the strongest incentive to be generous.

**E6. Prose the tooling must parse.** `docs/DocumentStandard.md` exists to let
tooling index documents deterministically; it is unapplied, so `scripts/status.py`
parses prose with regular expressions. Every such regex is a silent failure
waiting for someone to rewrite a sentence. Enumerate them.

---

## F. Compounding and capital

**F1. Costs.** Are commission, spread, slippage, and borrow modelled — or
assumed zero? A zero-cost backtest is not a conservative estimate, it is a
different strategy.

**F2. Capacity and liquidity.** Would the position size actually fill? A rule
validated on names that trade thin is untradeable at any size that matters.

**F3. Capital preservation precedence.** `Capital_Authority.md:22-28` — when
preservation and return conflict, preservation wins, always. Find any code where
a return objective can override a drawdown limit.

**F4. Correlation.** Ten rules that all express one factor is one strategy with
ten names and ten times the concentration risk anyone thinks they have.

---

## G. Meta

**G1. What did the last review miss?** Read the previous report and attack it
rather than continue it. Which of its findings were comfortable? Which sections
were thin because they were hard?

**G2. What is not checkable?** Name the claims in Belay that no test could
currently falsify. That list is the roadmap for the conformance suite, and it is
more valuable than most findings.
