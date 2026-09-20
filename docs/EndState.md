# Belay End State

What Belay is for, what it will eventually have to do, and which of the decisions
between here and there have actually been made.

Written 2026-07-31.

---

## Amendment, 2026-07-31 (same day) — the owner answered

**Three of the rows below have been answered by the owner and one fact this
document said it could not determine has been determined. `docs/OwnerDecisions.md`
holds all of it.** Nothing here is rewritten — every original line stands, and the
amendment is recorded in the way ADR-007 amended ADR-002, by preserving the
superseded text rather than replacing it.

In brief, so a reader of the table below is not misled by it:

- **Row 1 is ANSWERED.** All three narrowing questions in its section were put to
  the owner and answered. Belay will never place orders in an account that is not
  its operator's; it will never run on hardware its operator does not control;
  and the repository is to become private.
- **Row 6 is ANSWERED at its small size** — the broker issues the tax documents
  and Belay reconciles against them — **conditional on one broker and one
  account.**
- **Row 13's missing fact is now known: the repository is public.** See the
  correction in row 13's own section below. The row itself stays OPEN; it is now
  answerable rather than blocked.
- **One decision is added that this document did not contemplate: row 16**, on
  whether Belay may be distributed to other operators as an application. Q1's
  answer closes the money-management question and opens this one, and they are
  different questions.

---

## Status of this document

**This document rules nothing.** It is a reading of the repository plus one
labelled section of analysis. Where it says a thing is decided it cites the file
and line that decides it. Where it says a thing is implied it gives the reasoning
and says plainly that nothing rules it. Where it says a thing is open it means no
document in this repository answers it and no amount of further reading will.

It lives in `docs/`, which is outside ADR-002's governance freeze. ADR-002
enumerates the governance layer at `docs/DECISIONS.md:127-131` as `constitution/`,
`departments/`, `workflows/`, `Knowledge/` and the markdown under `strategies/`,
and freezes the *addition of new governance documents* to that layer. `docs/` is
not in the enumeration. ADR-002's own Required Follow-Up section further *mandates*
an edit to `docs/Architecture.md`, which would be incoherent if `docs/` were
frozen. Confirmed by opening the file before writing this one.

---

# Part 1 — Belay in plain English

Belay is a system for deciding, with evidence, whether an investment strategy
deserves money.

A **strategy** here means a rule for buying and selling — *buy this when that
happens, sell it when this other thing happens*. Anyone can write one. The hard
part is not writing it. The hard part is knowing whether it works, or whether it
only *looked* like it worked because it got lucky. That second thing has a name —
luck mistaken for skill — and almost all of the machinery built so far exists to
catch it.

So Belay was built backwards on purpose. Before it may place a single trade, it
has to be able to answer questions like these:

- **How much did this actually grow the money?** Lose half your money and you then
  need to double it just to get level again. Averaging the ups and downs would
  report that as breaking even, so Belay refuses to average.
- **How rough was the ride?** Two strategies can finish in the same place and one
  of them was unbearable to hold. Belay measures the swings, and measures them a
  second way that counts only the falls — nobody needs compensating for an
  unexpected gain.
- **What was the worst stretch?** The deepest fall from a high point down to the
  low that followed it.
- **Could a coin flip have done this?** Try a hundred random rules and a few will
  look brilliant by pure accident. Belay calculates the probability that a record
  this good could have happened with no skill at all — and states, on every
  result, that its own answer is *optimistic*, because the mathematics behind it
  assumes markets behave more politely than they do.

All four exist today and are tested. What does not exist is anything that touches
money: no connection to a broker, no orders, no positions, no tax records. And
nothing Belay has ever computed describes a real company — every number so far
was fed in by hand, and every number says so about itself.

That ordering was deliberate, and it is the thing worth understanding. Building
the trading part first is easy and produces something impressive within days.
Building the judging part first produces nothing you can show anyone for months.
It is also the only order in which the trading part is ever safe: a system that
can trade before it can judge is just a fast way to act on bad ideas.

Everything Belay produces is stored as a permanent sealed record — what was
computed, what was assumed, where the data came from, and what the number cannot
be trusted to mean. Change one character afterwards and the seal breaks and the
system refuses it.

And Belay is not allowed to promote a strategy by itself. Its own constitution
settles that in four words: *Belay advises. Humans authorize.*

---

# Part 2 — The decision table

Fifteen decisions. Six are made, five are implied by documents that never quite
say them, and four cannot be settled by any amount of reading.

**DECIDED** means a document in this repository says it, at the cited line.
**IMPLIED** means the reasoning below holds but **nothing rules it** — every
IMPLIED row is a candidate for an ADR, not a fact to build on.
**OPEN** means no document answers it.

| # | Decision | Verdict | Anchor |
|---|---|---|---|
| 1 | Is Belay single-operator, family, or a product for others? | **OPEN** | nothing in the repository names a beneficiary |
| 2 | May a model decide a promotion? (No) | **IMPLIED** | `Immutable_Laws.md:15-17`; `Operational_Constraints.md:31-35`; ADR-012 rule 11 |
| 3 | May a model generate hypotheses? (Yes) | **IMPLIED** | `constitution/README.md:5`; `Evidence_Standards.md:31-35` |
| 4 | May a model sit anywhere in the *explanation* path? | **OPEN** | Law II's strictness is genuinely undecided |
| 5 | Is tax-aware *evaluation* in scope? | **IMPLIED** | `Mission.md:7` — "purchasing power", not "return" |
| 6 | Is tax *accounting and filing* in scope? | **OPEN** | depends on row 1 for its size |
| 7 | Is the broker a swappable adapter? | **IMPLIED** | `Immutable_Laws.md:51` (Law VII); `DECISIONS.md:136-137` |
| 8 | Does one adapter ruling also cover market data? | **OPEN** | partly — see the argument below |
| 9 | Is execution / broker integration in scope? | **DECIDED** | `docs/ROADMAP.md:210-223`; `scripts/status.py:53` |
| 10 | Is a halt mechanism in scope, and must it not lag execution? | **DECIDED** | `docs/ROADMAP.md:219-221`, `:225-240` |
| 11 | Is the daily operating loop in scope? | **DECIDED** | `docs/ROADMAP.md:241-254`; thirteen documents under `workflows/` |
| 12 | Does `AGENTS.md` carry doctrinal authority? | **OPEN** | ADR-002's own follow-up to assign every directory a layer is unresolved |
| 13 | Is a fetched price series stored inside the repository? | **OPEN** | blocks Stage 2 — see Part 3 |
| 14 | Must the market data source include instruments that no longer trade? | **IMPLIED** | `Research/UniverseDiscovery.md:7`; `Evidence_Standards.md:23-27` |
| 15 | Is `docs/` outside ADR-002's freeze? | **DECIDED** | `docs/DECISIONS.md:127-131` |

**Rows 1, 6 and 13 are superseded by the amendment above.** Their verdicts are
left as written because the reasoning under each is what a later ADR needs;
`docs/OwnerDecisions.md` carries the answers and a sixteenth row this table does
not have.

---

## 1. Who Belay is for — **OPEN**

Query run, verbatim:

```
grep -rniE "\b(client|customer|investor|subscriber|end.?user|limited partner|family|household|spouse|multi.?user|tenant|SaaS|commercial|licen[cs]e|deploy|deployment|credential|API key|account holder|operator|owner)\w*" --include=*.md
```

Nothing in `constitution/`, `departments/`, `Knowledge/`, `Operations/`,
`Research/`, `strategies/`, `Validation/` or `workflows/` names a beneficiary, a
client, an investor, or more than one person.

The one near-signal is `docs/ENGINEERING_AGENT.md:27`, the only organisation chart
in the repository, which puts a singular **"Human Owner"** at the top. It does not
rule this question, for three reasons: it is in `docs/` and not in the governance
layer; it governs who approves *software changes*, not whose capital is at risk;
and it is contradicted in spirit by `constitution/Governance.md:3` — "Belay is
governed by process rather than hierarchy" — which is the constitution
deliberately declining to name a person. Ruling row 1 from that line would be
extending a document rather than applying one, which is the failure this
repository has now recorded three times.

**This needs the owner. But it does not need the owner to answer the question as
posed.** "Single-operator, family, or product" is a hard question about identity.
Three narrower questions determine everything the finding says follows from it,
and each has a yes/no answer:

- **Will Belay ever place orders in an account that is not yours?** This decides
  credential architecture, and it is a legal question before it is a technical
  one. `constitution/Operational_Constraints.md:3` — "Belay shall operate
  lawfully" — makes it constitutional rather than optional. Managing money for
  other people is a regulated activity in most jurisdictions and the answer must
  come from a professional, not from this repository.
- **Will Belay ever run on hardware you do not control?** This decides secrets
  handling, cost and monitoring.
- **Will this repository ever be public?** This decides data licensing — and it
  bites *today*, at single-operator scale. See row 13.

Answering those three collapses rows 6, 8 and 13 and most of Part 4.

## 2–4. The runtime model question

Query run, verbatim:

```
grep -rniE "\b(LLM|language model|GPT|Claude|Anthropic|OpenAI|AI |artificial intelligence|neural|machine learning|ML model|prompt|inference|autonomous|agent)\w*" --include=*.md
```

`framework/` contains no model call of any kind. Today Claude is the builder, not
a component.

### Row 2 — a model may not decide a promotion. **IMPLIED, strongly.**

Four independent constitutional points converge on it:

- **`constitution/Immutable_Laws.md:15-17`** (Law II) — "Every investment decision
  must be explainable. Black-box reasoning is prohibited."
- **`constitution/Operational_Constraints.md:31-35`** — "Human oversight remains
  the final authority. / Belay advises. / Humans authorize." This already rules
  that *Belay as a whole* does not authorize. A component of Belay therefore
  cannot.
- **`constitution/Immutable_Laws.md:9`** (Law I) — "Evidence always overrides
  opinion", read against `constitution/Evidence_Standards.md:45`, "Every
  conclusion must reference supporting evidence."
- **`constitution/README.md:11-13`** — "The Constitution may only be amended
  through explicit human approval. Belay does not self-amend its governing
  principles."

**The argument that settles it is one Belay has already made, and it works from
the other direction.** ADR-012 rule 11 (`docs/DECISIONS.md:2252-2259`) forbids
`framework/metrics/statistics.py` from deciding a promotion, and a test enforces
it by refusing any exported name containing `passes`, `promote`, `approve`,
`verdict`, `gate` or `decision`. That module is thirty-five lines of arithmetic
pinned against a printed table — it is the most explainable component in the
repository, and it is *still* not permitted to decide. If fully deterministic,
hand-verifiable arithmetic may not decide a promotion, a model whose reasoning
cannot be reproduced plainly may not either.

So this is not a new restriction on models. It is the existing restriction on
every Belay component, applied to one more component. **Nothing rules it.**

### Row 3 — a model may generate hypotheses. **IMPLIED.**

**`constitution/README.md:5` is the load-bearing line and it has never been cited
for this:** *"No department, workflow, script, report, strategy, or **AI process**
may violate the Constitution."* The Constitution already contemplates an AI
process operating inside Belay and pre-commits it to every Immutable Law. A
runtime model is therefore not prohibited outright — the constitution made room
for one before anybody asked.

And `constitution/Evidence_Standards.md:31-35` already defines the class such an
output belongs to: **Level D, "Hypothesis. Research only."** A model-generated
idea has a lawful home in the existing evidence hierarchy. It enters at the bottom
and climbs by the same route as any other hypothesis, or it does not climb.
Nothing new is required to accommodate it. **Nothing rules it.**

### Row 4 — how strict is "explainable"? **OPEN.**

This is the crux, and it is the reason rows 2 and 3 are not enough for an ADR on
their own.

Law II says every investment decision must be explainable and black-box reasoning
is prohibited. There are two readings:

- **The weak reading:** an output is explainable if it cites the evidence it
  rests on. A model that proposes a hypothesis and names the data behind it
  satisfies Law II.
- **The strict reading:** the *reasoning process* must itself be inspectable.
  **ADR-012 rule 5 already took the strict reading once** — it refused `scipy`
  and hand-implemented Student's t distribution on the ground that "the library
  said so" is the answer Law II forbids. If a well-tested numerical library is a
  black box in the sense Law II means, a language model certainly is, and the
  strict reading would bar a model from the explanation path entirely — including
  from writing a `known_limitations` string that ends up inside an artifact's
  signature.

Two further boundary questions the ADR must settle:

- **`constitution/Capital_Authority.md:11-18` names six inputs that determine
  capital** — Confidence, Statistical edge, Regime compatibility, Portfolio
  exposure, Correlation, Drawdown limits. If a model produced one of those, has
  it decided? Row 2 says a model may not decide a promotion; it says nothing
  about a model *sizing* a position, and `Capital_Authority.md:5` — "Approval does
  not imply allocation" — makes those two separate decisions.
- **`AGENTS.md:199-200` requires "deterministic behavior" and "reproducibility".** A
  model call is neither. Does recording the exact prompt, model identifier and
  response satisfy reproducibility, or does reproducibility require that
  re-running produces the same answer? These are different standards and the
  second one no model meets.

**Rows 2, 3 and 4 are rulable from documents alone. They need no input from the
owner and should be one ADR.**

## 5–6. Tax

Query run, verbatim:

```
grep -rniE "\b(tax|taxes|taxable|wash sale|cost basis|1099|tax lot|lot selection|capital gain)\b" --include=*.md
```

Hits appear only in `docs/ROADMAP.md`, `docs/HANDOFF.md` and `CHANGELOG.md` —
all three being this repository's own record of the finding. Confirmed again
today: **zero hits in any governing document.**

### Row 5 — tax-aware evaluation. **IMPLIED, and this is the strongest implication of the four.**

`constitution/Mission.md:7` states that Belay "seeks to maximize long-term
compounded **purchasing power** while preserving capital".

Not "return". Not "pre-tax return". **Purchasing power is an after-tax,
after-inflation quantity.** A pre-tax growth rate is not a measure of purchasing
power at all, and the mission sentence would read differently if it were meant to
be. Set beside `constitution/Mission.md:38` — "Belay optimizes for decades—not
days" — the point sharpens: over decades, the gap between a strategy's pre-tax and
after-tax compounded growth is not a rounding error, and it is driven by turnover,
which is a property of the strategy under evaluation.

So a promotion decision made on a pre-tax figure, for a strategy that will be held
in a taxable account, is a decision made on a number that does not describe the
outcome. Law I — "Evidence always overrides opinion" — makes that a defect rather
than a simplification.

**Nothing rules it.** One word in one line of the Mission is doing all of this
work, and reading a scope commitment out of a single adjective is exactly the sort
of inference this repository requires an ADR for.

### Row 6 — tax accounting and filing records. **OPEN, and its size depends on row 1.**

`constitution/Operational_Constraints.md:3` ("Belay shall operate lawfully") and
`:5` ("Belay shall maintain accurate records") reach filing obligations — but only
if Belay is the **system of record**. Two very different stages hide under one
name:

- If a broker issues the tax documents and Belay reads them back, Stage 9 is a
  *reconciliation* problem: check that what Belay thinks it holds matches what the
  broker reported. Small, and it needs Stage 7 rather than a new discipline.
- If Belay is the system of record — multiple accounts, an entity, or any
  situation where no single broker sees the whole picture — Stage 9 is real lot
  accounting: cost basis per lot, a lot-selection policy, and wash-sale tracking
  across accounts. Large.

Row 1 decides which. **And a caution that belongs in the ADR rather than in the
code:** naming a tax concept is not ruling its treatment. Whether wash-sale rules
apply to a given account, and how, is a matter for a tax professional in the
relevant jurisdiction. Belay may record the facts; it may not decide the law.

## 7–8. The adapter question

Query run, verbatim:

```
grep -rniE "\bbroker" . --exclude-dir=.git --exclude-dir=.pytest_cache -l
```

Four files: `CHANGELOG.md`, `docs/HANDOFF.md`, `docs/ROADMAP.md`, and the
generated `reports/generated/status.html`. **No governing document names a broker,
a venue, or the adapter pattern.**

### Row 7 — broker as a swappable adapter. **IMPLIED — but not for the reason it is usually given.**

The obvious citation is `AGENTS.md:201` and `AGENTS.md:240-246`, which list
"explicit interfaces" and "dependency inversion" among the things Belay prefers.
**That citation is weaker than it looks, and this session found out why.**
ADR-002 enumerates the governance layer and the mechanics layer;
`AGENTS.md` sits at the repository root and belongs to neither, and ADR-002's own
Required Follow-Up — "assign each remaining top-level directory to exactly one
layer" — is still open. So `AGENTS.md`'s authority is itself unassigned. That is
row 12, and it means the adapter pattern **cannot be ruled doctrine on
`AGENTS.md` alone.**

What does imply it, from documents that are unambiguously governance:

- **`constitution/Immutable_Laws.md:51`** (Law VII) — "Institutional knowledge
  shall never be intentionally discarded." **This is the real argument.** If
  fills, positions, prices and cost basis exist only inside a broker's systems,
  then changing broker discards institutional knowledge — not by accident, but as
  a direct consequence of the architecture. Law VII therefore requires Belay to
  keep its own signed record of every fact a venue tells it. That obligation *is*
  the substance of the adapter pattern, reached from the constitution rather than
  from software taste.
- **`docs/DECISIONS.md:136-137`** — "Mechanics emit Artifacts. Governance consumes
  Artifacts. **Neither layer reaches across the boundary by any other means.**" A
  broker call embedded anywhere a governance component can see would breach this.
  So the broker must sit behind *a* boundary. Note carefully what this does and
  does not give you: it argues for a boundary, not for a *swappable* one.

**So the ruling should be narrower and better founded than "broker as swappable
adapter":** Belay keeps its own signed record of every fact a venue tells it
(Law VII), and no component above the boundary may hold a venue-specific type
(ADR-002). Swappability then *falls out* as a consequence rather than being
asserted as a preference. That reframing is what converts the owner's preference
into something the constitution actually supports. **Nothing rules it today.**

### Row 8 — does ruling the pattern once cover market data too? **Partly. Ruling it once as a single pattern is a false economy.**

**What genuinely generalises — rule this once, and it covers both.** Both a
broker and a data vendor are an outside party telling Belay a fact, and both are
governed by the same two obligations: `Validation/Backtesting.md:35-43` requires
every backtest to record its Data Source, and `Immutable_Laws.md:51` requires
Belay to keep its own copy. The machinery is already half-built —
`Disclosure.data_source` at `framework/metrics/reporting.py:58` is enforced
non-blank and sits inside the artifact's integrity hash. **The provenance
obligation is one ruling and it covers everything that crosses the boundary.**

**What does not generalise — and each of these three is load-bearing:**

1. **Direction, and the consequence of being wrong.** Market data is a *read*. A
   broker adapter *writes to the world*, and the write moves money irreversibly.
   An interface designed for reads has no vocabulary for the things that make
   writes dangerous: idempotency, partial fills, cancel-in-flight races, and the
   halt path. `docs/ROADMAP.md:225-240` requires a halt to stop a strategy "within
   seconds" — a halt is a *write* with a latency requirement, and no data adapter
   has one. Designing the dangerous one in the language of the safe one is exactly
   how the vocabulary for the danger goes missing.
2. **Opposite failure policies.** A market-data adapter can be retried freely;
   retrying is *how* you recover from a dropped connection. A broker adapter that
   retries a submit can double a position. Their correct defaults are opposites, so
   a shared base class has to pick one and be wrong for the other.
3. **`constitution/Immutable_Laws.md:45`** (Law VI) — "Research and execution
   remain independent." The two adapters sit on opposite sides of that law. Market
   data feeds research; the broker *is* execution. A shared abstraction is a shared
   dependency across a boundary the constitution declares independent. This is the
   sharpest argument, and it is constitutional rather than aesthetic.

`docs/ROADMAP.md:219-221` is itself evidence for the split: it constrains the
ordering of the broker work ("Must not land before Stage 7's halt mechanism, or
alongside it") and imposes no such constraint on market data. A rule that applies
to one and not the other is a rule about two objects.

**Conclusion: rule the provenance obligation once; rule the two adapter contracts
separately.** Treating "a swappable adapter" as one decision looks like an economy
and is two decisions wearing one name.

## 9–11. What is already decided

These three are DECIDED and should stop being discussed as though they were open.

- **Row 9 — execution is in scope.** `docs/ROADMAP.md:210-223` is Stage 6, and
  `scripts/status.py:53` names `framework/services/execution.py` as the component
  expected to make the constitutional criterion `Execution quality` computable.
  A constitutional promotion criterion depends on it. It is not optional.
- **Row 10 — the halt mechanism is in scope and must not lag execution.**
  `docs/ROADMAP.md:219-221` and `:225-240`. The ordering constraint is the
  decision, and it is the one thing in this whole plan that is a safety property
  rather than a preference.
- **Row 11 — the daily operating loop is in scope.** `docs/ROADMAP.md:241-254`,
  and thirteen workflow documents already exist under `workflows/` including
  `Daily/MarketOpen`, `Daily/MiddayReview` and `Daily/MarketClose`. This has been
  specified all along. It was never sequenced.

## 12. Does `AGENTS.md` carry doctrinal authority? — **OPEN**

Surfaced by row 7. ADR-002's Required Follow-Up says "assign each remaining
top-level directory to exactly one layer", and that follow-up is still open.
`AGENTS.md` is currently cited as though it were binding — it is what tells every
session to prefer explicit interfaces, avoid parallel implementations, and treat
Artifacts as the communication boundary — while sitting outside both layers ADR-002
defines. It is a small question with a wide blast radius, because the answer
decides whether "explicit interfaces" is doctrine or advice.

## 13. Is a fetched price series stored in the repository? — **OPEN, and it blocks Stage 2**

Not on finding 10's list, and it should have been. Three documents pull in
different directions and none of them is about software:

- `Immutable_Laws.md:51` (Law VII) says institutional knowledge is never
  discarded, which argues for keeping every series ever fetched.
- `Knowledge/Versioning.md` will have opinions about a stored series, as
  `docs/HANDOFF.md` already predicts of Stage 2.
- A vendor's licence may forbid redistribution — and **the remote is
  `https://github.com/pewpewpressco-ux/Atlas.git`.** Whether that repository is
  public could not be determined from inside it during this session (`gh` was
  unavailable), and it is the single fact that decides whether committing a
  fetched price series is redistribution. **If the repository is public, this
  bites at single-operator scale and row 1 never enters into it.**

  > **Determined later the same day: the repository is public.** `gh` is still
  > not installed, so the check was made against the API instead, verbatim:
  >
  > ```
  > curl -s -o /dev/null -w "%{http_code}\n" https://api.github.com/repos/pewpewpressco-ux/Atlas
  > ```
  >
  > **`200`, with no credentials presented.** A private repository returns `404`
  > to an anonymous caller. So the conditional above resolves: this bites at
  > single-operator scale, today, and row 1 never enters into it.
  >
  > Two things follow, both in `docs/OwnerDecisions.md`. **The repository is
  > public on a false premise** — the owner made it public believing Claude Code
  > required it for access, and it does not; this repository is read from local
  > disk and the remote is never fetched for content. And **nothing of substance
  > has been exposed**: 185 tracked files, no credentials, no market data, no
  > account identifiers. The exposure was of every future commit rather than of
  > anything already made.
  >
  > **Fixed the same day. The repository is private, and the same query now
  > returns `404`.** So this row's recommended answer changes: while the
  > repository was public, committing a fetched series *was* redistribution and
  > no free or retail licence tolerates it. Private storage is not
  > redistribution, so ADR-013 can weigh Law VII's retention obligation against
  > `Knowledge/Versioning.md` on the merits, with a per-vendor licence check
  > rather than a categorical bar. **The row stays OPEN — it is now a design
  > question rather than a blocked one.**

## 14. Must the data source include instruments that no longer trade? — **IMPLIED**

Treated in full in Part 3, because it is a Stage 2 acceptance criterion rather
than a general principle.

## 15. Is `docs/` outside the freeze? — **DECIDED**

`docs/DECISIONS.md:127-131`. Covered at the top of this document.

---

# Part 3 — What actually blocks Stage 2

Stage 2 is the market data boundary. `docs/ROADMAP.md:155-162` defines its whole
deliverable as *"A defined boundary for obtaining a price series, with provenance
recorded on the resulting evidence."*

The expectation put to this session was that **only** row 1 plausibly blocks it,
via data licensing and redistribution, and that saying so plainly beats a long
list. **The shape of that expectation is right and the identity of the blocker is
wrong.** One of the four blocks Stage 2. It is row 7/8, the adapter question — not
row 1.

## Row 8 blocks Stage 2, and it blocks it directly

Stage 2's deliverable is *a defined boundary*. A boundary **is** an adapter
contract. You cannot build Stage 2 without answering "what shape does the thing
behind this boundary have, and can there be more than one of them?" — which is
row 8's market-data half, asked directly rather than by analogy.

Someone could of course write a single hard-coded fetcher and call Stage 2 done.
But by this repository's own standard that *is* the ruling, made silently:
ADR-011's central holding is that **no convention Belay was not told is ever
defaulted**. A single hard-coded source defaults the convention that there is only
ever one source. `docs/HANDOFF.md` already warns that Stage 2 should "expect a
ruling". This is the ruling it means.

## Row 1 blocks only the choice of first vendor, and only if row 8 is left unruled

The licensing concern is real but it does not bind on the *boundary* — an
interface is licence-agnostic. It binds on two concrete things:

- **Which vendor is implemented first.** Free and retail-tier feeds are typically
  personal-use and non-redistribution. *If row 8 is ruled* — multiple
  implementations behind one contract — then picking a personal-use source first is
  a reversible decision, and row 1 stops blocking anything. **Ruling row 8 is what
  un-blocks Stage 2 from row 1.**
- **Whether the data is committed to the repository.** That is row 13, and as
  noted it is live regardless of how row 1 is answered.

## Rows 2–4 do not block Stage 2 at all

Fetching a price involves no model under any reading of Law II. Even the most
permissive ruling on rows 2–4 changes nothing about Stage 2. Clean no.

## Rows 5–6 do not block Stage 2, but should constrain exactly one field of it

Tax needs fills and lots, which need Stages 6 and 7. But there is one cheap
forward dependency worth honouring now.

`Disclosure.sample_period` at `framework/metrics/reporting.py:59` is today a
free-form `str`, validated only as non-blank. Tax years are calendar-bounded and
jurisdiction-specific. If Stage 2 fills that field with prose, no later stage can
derive a tax year from it without parsing prose — which is the same defect
`docs/DocumentStandard.md` exists to prevent elsewhere in this repository. Making
the sample period machine-readable is nearly free now and expensive to retrofit
after artifacts carrying the prose form have been signed and made permanent.

That is row 6 earning a seat at Stage 2's design review without blocking it.

## Survivorship bias

Query run, verbatim, over the whole repository including code:

```
grep -rniE "survivorship|delisted" . --exclude-dir=.git --exclude-dir=.pytest_cache
```

**Zero hits.** Not one, anywhere. The related term `look-ahead` appears exactly
once, at `docs/ROADMAP.md:169`, in Stage 3's description of the backtester.

**A backtest run only on companies that still exist is a backtest that lies in
your favour**, and here is why that is a requirement rather than a preference.

**1. It is a property of the source, not of the backtester, so Stage 2 is the only
place it can be caught.** By the time Stage 3 exists the source has been chosen,
and no amount of care in the backtester recovers returns for a company whose data
the vendor deleted when it stopped trading. Either this is a Stage 2 acceptance
criterion or it is nothing.

**2. `Research/UniverseDiscovery.md:7` makes it constitutional, not merely
statistical.** "Tradable universes must be discovered through evidence." A
universe discovered from a survivor-only source has been filtered by the very
outcome under prediction — the evidence has been selected on the thing it is
supposed to be evidence *about*. `Research/UniverseDiscovery.md:25` even requires
Belay to "Evaluate survivability" of a candidate, which it cannot honestly do
from a dataset that has already removed everything that failed to survive.

**3. It is not merely weak evidence — it is evidence about a different
population.** `constitution/Evidence_Standards.md:23-27` grades historical
simulation Level C, "Moderate confidence". A survivor-only backtest does not
deserve a lower grade within Level C; it describes an experiment that could not be
run in advance, because nobody knew in advance which companies would survive.
Grading it C would be precisely the "reassuring half-truth" `scripts/status.py`
exists to prevent.

**4. The bias has a known direction, which is the pattern Belay has already ruled
on.** ADR-012 rule 7 did not merely disclose an assumption — it disclosed the
assumption's *direction*, that the p-value is **optimistic**. Survivorship has the
same property and then some: it inflates every return measure in the strategy's
favour, **and it deflates drawdown and tail measures**, so it flatters the return
and understates the risk simultaneously. And ADR-012 rule 10
(`docs/DECISIONS.md:2244-2250`) already ruled the correct response to a bias that
cannot be corrected: refuse to produce a number that "looks adjusted and is not",
and disclose instead.

**5. Therefore the machinery already exists and needs no invention.**
`Disclosure.known_limitations` at `framework/metrics/reporting.py:60` is enforced
non-blank and sits inside the artifact's integrity hash. The rule that falls out
is ADR-012 rule 7's shape applied to data: **if the source excludes instruments
that no longer trade, that fact is a fixed constant on every artifact derived from
it — not a caller-supplied string — and it names the direction of the bias.** A
source that includes them says so, in the same field. Either way the number
carries its own provenance and cannot be softened afterwards.

**6. And the requirement has two halves, which is the part most people get
wrong.** "Includes delisted names" is not one property:

- **Delisted *prices*** — can the source return a price history for a ticker that
  no longer trades, if you already know to ask for it?
- **Delisted *membership*** — does the source know which instruments were in a
  universe *on a past date*, as opposed to which are in it today?

A source can pass the first and fail the second, and the second is the one that
causes the damage in a universe-driven strategy. `Research/UniverseDiscovery.md`
makes Belay universe-driven by design. So the Stage 2 acceptance criterion is not
"does the source have delisted data" — it is **"can the adapter answer both
questions, and is the answer recorded rather than assumed?"**

## The short version

**Row 8 blocks Stage 2. Row 1 does not, once row 8 is ruled. Row 13 blocks it and
was not on the list. Rows 2–6 do not block it, though row 6 should be allowed to
shape one field. Survivorship is a Stage 2 acceptance criterion with two halves,
and Belay already owns the machinery to record the answer honestly.**

---

# Part 4 — External services and rough costs

> **This entire section is my analysis, not a reading of the repository.** No
> Belay document names a vendor, a service, a platform or a price. Nothing below
> is quoted from anything. The figures are order-of-magnitude bands as I
> understand the market on 2026-07-31, they are not quotes, they are not
> recommendations, and every one of them must be re-verified against a current
> price list before any commitment is made. Where I do not know, I say so rather
> than estimating.
>
> No vendor is named anywhere in this section, deliberately. Naming one would put
> a supplier into the repository that no decision has chosen.

Two columns throughout: **personal scale** means you, your own money, your own
hardware. **Multi-user scale** means any arrangement where Belay touches an
account that is not yours, or runs somewhere you do not control.

## The costs

| Service | Why Belay needs it | Personal scale | Multi-user scale |
|---|---|---|---|
| Historical daily price data, survivorship-free | Stage 2, and the requirement in Part 3 | **This is the expensive one.** Free tiers are generally survivor-biased. Retail tiers with some delisted coverage sit in the low tens of dollars per month; genuine point-in-time universe membership is the step change, typically hundreds to low thousands per month, and academic-grade datasets are annual site licences well into five figures | same product, but a **redistribution or commercial licence**, which is usually a different contract rather than a higher tier — commonly an order of magnitude more, sometimes negotiated rather than listed |
| Real-time / intraday market data | Stages 6–8, if Belay trades intraday | Exchange fees are charged per exchange and per user, and are billed separately for *non-professional* and *professional* status. Non-professional is typically single-digit to low-tens of dollars per exchange per month | **Managing money for others typically triggers "professional" status at the exchange level**, which is commonly an order of magnitude higher per exchange. This is the most direct, checkable cost link between row 1 and money |
| Corporate actions / reference data | splits and dividends must be applied correctly or every long-horizon return is wrong | often bundled with the price feed; standalone, tens to hundreds of dollars per month | as above, plus licence terms |
| Brokerage / execution | Stage 6 | commission on US equities is frequently zero at retail; options are usually per-contract. **The real cost is implicit** — spread and financing — and does not appear on any invoice | entity accounts, or one account per person, plus API rate limits that scale with neither |
| Compute / always-on hosting | Stage 8, the daily loop, which must run whether or not you are at the machine | a small always-on machine or a modest cloud instance: roughly $5–$50 per month | redundancy, monitoring, alerting and someone to answer them: roughly $100–$1,000+ per month before staff |
| Secrets handling | broker credentials must not sit in the repository | operating-system keychain or an encrypted local file: effectively $0 | managed secrets service plus per-user credential isolation, encryption at rest and key rotation: modest in dollars, **significant in engineering** |
| Model inference, *if* rows 2–4 rule it in | hypothesis generation only | usage-based; at a few calls per day, single-digit to low-tens of dollars per month | scales with users. **The constitutional cost is larger than the inference cost:** `AGENTS.md:199-200` requires reproducibility, so every prompt, model identifier and response has to be stored and retained, which is a storage and audit obligation rather than an API bill |
| Backup and archival | `Immutable_Laws.md:51` makes retention mandatory, not optional | tens of gigabytes, a few dollars per month | versioned, geographically redundant, with a written retention policy |
| Tax preparation | Stage 9 | consumer tax software or an accountant: low hundreds to low thousands per year | entity returns and multi-account reconciliation: materially higher and entirely jurisdiction-specific |
| Legal and regulatory | only if Belay touches someone else's account | **not applicable** | **I will not estimate this.** It is a professional's question and the answer determines whether the rest of the table is even legal |

## What actually changes between the two columns

Not much of it is the monthly bill. Three things change in kind rather than in
degree:

1. **Data licensing changes contract, not price tier.** Personal-use and
   redistribution are usually separate agreements. This is the concern behind row
   1 and it is correctly identified — but note again that row 13 exposes the same
   risk at personal scale, if the repository is public.
2. **Exchange "professional" status is a cliff, not a slope.** It is determined by
   what you do, not by how much data you consume, and managing money for others
   commonly triggers it.
3. **Regulation is a different category of question entirely.**
   `constitution/Operational_Constraints.md:3` says "Belay shall operate
   lawfully", which makes this constitutional rather than discretionary. It is not
   an engineering decision and this document does not attempt it.

The engineering cost of multi-user is larger than the invoice: credential
isolation, per-user data segregation, audit retention, and an on-call
expectation for a system that `docs/ROADMAP.md:225-240` says must be able to stop
a strategy within seconds.

---

# Part 5 — What this document does not do

It rules nothing. Every IMPLIED row above is an argument, not a decision, and
every one of them says so.

**What can be ruled without asking the owner anything:** rows 2, 3 and 4 — the
runtime model question — and rows 7 and 8 — the boundary question. Both rest
entirely on documents that already exist.

**What cannot be ruled from any document:** row 1, and rows 6 and 13 that hang off
it. Row 1 does not need to be answered as posed; the three narrower questions in
its section do the same work.

**What should be ruled first, and why.** Rows 7 and 8, because Stage 2 is the next
build session and Part 3 shows it is the thing standing in the way. The runtime
model ADR is more interesting and less urgent — nothing is blocked on it, and
`framework/` contains no model call to govern.

A proposed ADR-013 on the boundary would need to rule, at minimum:

> **Superseded later the same day. ADR-013 exists and is Accepted, and it has
> *ten* rules rather than the five below.** The five here are real and all five
> are in it; what this list could not see were the identity question, the
> instrument-shape question, the evidence-grade question, the refusal of a source
> that will not state its properties, and the `Market Snapshot` exclusion. None
> was visible without opening `Knowledge/Identifiers.md`,
> `framework/artifacts/enums.py` and `constitution/Evidence_Standards.md`
> together. Left in place because the gap between what this document could
> predict and what the drafting found is the useful part.

1. Provenance is one obligation covering everything that crosses into Belay from
   outside — the generalisation Part 3 argues is real.
2. Market-data adapters and execution adapters are two contracts, not one — the
   generalisation Part 3 argues is false, on Law VI, on retry semantics, and on
   the halt path.
3. Whether a fetched price series is stored inside the repository (row 13).
4. The survivorship acceptance criterion, in both halves, and its fixed-constant
   disclosure in the ADR-012 rule 7 shape.
5. Whether `sample_period` becomes machine-readable now.

**No ADR is drafted in this session.** The session constraint was to give a token
estimate before drafting one and to leave any ruling Proposed rather than
implemented; a full ADR-013 with the verification pass this repository requires is
roughly 60–90k tokens and belongs in its own session, before Stage 2 rather than
during it.
