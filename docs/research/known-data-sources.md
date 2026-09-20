# Known Data Sources and Known Gaps — leads for the data collection pipeline

**Status: research note. Non-binding. Nothing here is a decision, a
recommendation, or evidence.** Recorded 2026-09-19 at the owner's request, in
the owner's words: "not saying its the best or what Belay should do or needs to
do, just want to document the known sources and gaps in the repo accordingly",
so that nobody building the pipeline later starts from scratch.

## What this is

The owner runs a separate, private trading project that predates Belay. It has
already hit, and worked around, many of the problems Belay's later data
collection stage will meet. This note writes down what that project learned, so
that whoever builds Belay's pipeline starts from known ground.

**How to read every figure below.** Each was measured inside that other
project, on its own instruments and dates. **None has been reproduced in Belay.**
Under Belay's own evidence standards that makes each one a lead to test, not a
fact to cite. Any source Belay adopts still has to be established the way ADR-013
(`docs/DECISIONS.md`, "The Data Boundary") requires: its properties are
*queried*, not assumed.

**What is deliberately absent.** That project's code, credentials, account
details, strategies and results. Only the data plumbing is described, and
described so it can be rebuilt without access to the original.

**What Belay already records elsewhere, so it is not repeated here.** ADR-013
covers the data contract, the versioned store, the survivorship disclosure and
the first free source (DoltHub). `docs/OwnerDecisions.md` question 3 ("What can
you actually spend on market data each month?") covers budget and the vendor
candidates, and rules that Belay must buy survivorship-free data the first time
it *selects* instruments rather than being handed them.

---

## Two requirements every collection component must meet

The owner ruled both essential on 2026-09-19 (`docs/OwnerDecisions.md` Part 11).

1. **Deterministic.** Collection touches a live world, so it cannot be
   repeatable by itself. The rule that makes the *system* repeatable: **capture
   once, freeze the raw response, and compute only from the frozen file.** A
   collector's job ends when it has written exactly what the source returned,
   with a fetch record beside it. Everything after that is a pure function of
   frozen inputs and must give the same answer on every run.
2. **Independent of any AI provider.** A collector is plain code that any
   operator can run. It may not depend on a particular AI service's connectors,
   scheduled agents, tools or memory. One component in the other project breaks
   this rule; it is described in section 5 as a known trap, with the way out.

---

## 1. Yahoo Finance through the `yfinance` library — option chains and daily bars

- **Provides:** option chains (bid, ask, last, volume, open interest, implied
  volatility) and daily price bars.
- **Access:** an unofficial wrapper around a public website. No credentials, no
  cost, no published rate limit or service guarantee. It can change or stop
  without notice.
- **What had to be built, and why.** Snapshots taken shortly after the market
  opened looked complete and were not. The option feed was found to run roughly
  fifteen minutes behind, so an early snapshot captured the opening book: about
  a fifth of contracts had a two-sided quote, against roughly nine in ten late
  in the day. The fix was to move the morning snapshot later.
- **Replication path.** Snapshot the same chains at several times of day.
  For each, measure the share of contracts with both a bid and an ask. Move the
  collection time until that share stops improving. Record the measurement
  beside the schedule so the reason survives. Never treat a vendor's "current"
  flag as proof that a quote is fresh.
- **Other handling that mattered.** Missing values arrive as not-a-number and
  must be stored as explicit nulls. A contract with no quote is recorded as
  absent, never filled in.
- **Determinism.** Plain code. Two leaks: the run uses the wall clock to decide
  which session it is in, and the library version was not pinned. Belay should
  pin it and pass the clock in.

## 2. SEC EDGAR — insider filings, and a dead end on share float

- **Provides:** the daily index of Form 4 filings and each filing's ownership
  document; a public company-identifier-to-ticker map.
- **Access:** official public endpoints. No credentials, no cost. The SEC
  requires a descriptive User-Agent header and publishes a fair-access limit.
- **What had to be built, and why.** A single retrying fetch function that
  every call goes through: it holds requests under the SEC's limit, retries
  "too many requests" and server errors with growing delays, and gives up after
  a fixed number of attempts. Plus a fallback for naming the ticker: the
  filing's own symbol first, then the identifier map, cached once a day.
- **Replication path.** Route all SEC traffic through one function. Enforce the
  rate limit there. Retry only the transient error codes, with exponential
  backoff and a cap. Cache the identifier map daily. Store the raw filing.
- **Known failure, fully diagnosed.** On one day several filings could not be
  matched to a ticker. The causes were transient server errors plus one company
  name that matched the wrong identifier. **The project chose never to go back
  and re-ask for a past day**, because a later answer can contain information
  that was not available on the day, which is lookahead. Those rows stay
  unresolved on purpose. Belay should adopt the same rule: a gap discovered
  later is recorded as a gap.
- **Dead end worth knowing.** EDGAR's shares-outstanding figure is not float,
  is reported quarterly, and goes stale across reverse splits and dilution. In
  one case it differed from a broker's figure by more than tenfold. It was ruled
  out as a float source.
- **Environment trap.** The SEC's site was unreachable from one hosted
  execution environment, which forced collection onto a machine the operator
  controls. That agrees with the owner's standing rule that Belay runs only on
  hardware its operator controls.

## 3. Broker price history — an official interface, and an unofficial library

- **Provides:** daily bars for named instruments.
- **Access.** Two retail brokers, read-only: one through its own official
  interface, one through a community-written, unofficial library. Both routes
  need an operator's own credentials. **Belay should not depend on an unofficial
  route to any provider until that route's standing under the provider's terms
  has been established**; for a product that is sold, an official interface is
  the default.
- **What had to be built, and why.** The unofficial library, when its saved
  session had expired, fell back to asking for a username on the keyboard. On an
  unattended scheduled run that meant hanging until the scheduler killed it, and
  it looked like a stalled task, not a login failure. The fix wraps the login in
  a thread with a hard timeout and blocks keyboard input for its duration, so an
  expired session raises an error immediately.
- **Replication path.** Never call a vendor's login directly from a scheduler.
  Wrap it: run it in a worker thread, replace standard input so any prompt
  raises, join with a timeout, restore standard input even on failure, and turn
  a timeout into a named authentication error.
- **Known failure.** Saved sessions expire on a cycle of about a week. Removing
  the saved session to force a fresh login can look like a new device to the
  broker and draw a challenge. Expiry must be expected, detected and reported.
- **Survivorship.** Already recorded in Belay: a broker's history covers
  instruments that still exist. Interactive Brokers' own documentation says a
  delisted instrument has no history through its interface.

## 4. Cross-checking two price sources — the most transferable lesson

- **Why it was built.** No price source had ever been checked against another,
  and the errors were silent.
- **Method.** Pull the same symbols and window from two independent sources.
  From each, drop every bar the source itself flags as interpolated and every
  bar with zero volume, **and report how many were dropped per source**. Compare
  closes only on dates where both sources have a real bar. Treat any
  disagreement above half a percent as an open question. Never resolve it
  automatically.
- **What it found.** About four in ten bars from one broker carried the
  source's own "interpolated" flag, meaning the price was filled in, not traded.
  One fund returned hundreds of rows dated before the fund existed. A separate
  public vendor was found to have shipped wrong split adjustments that silently
  corrupted adjusted histories. After cleaning, the two brokers agreed on the
  instruments checked to within a quarter of a percent over three years.
- **Replication path.** Build the bad-bar filter as one shared function and use
  it everywhere. Cache the raw bars from both sources to disk so the comparison
  can be re-run with no further network calls.
- **For Belay.** ADR-013 already notes that two sources disagreeing about a
  price is a ruling nobody has made. This is the evidence that the question is
  not hypothetical. A second source earns its place as a cross-check, not as an
  interchangeable feed.

## 5. A daily market screen run by an AI agent — a known trap

- **What it does.** Once a day after the close, it screens for stocks meeting
  simple price and volume conditions, looks each one up at the SEC, and later
  fills in price history for the names it captured.
- **How it is run, and why that is the problem.** The engine that uses this data
  does no network access at all; it is a pure function over frozen files, which
  is exactly right. **But the collection itself is performed by a scheduled AI
  agent following a written prompt and calling one AI provider's broker and file
  storage connectors.** It was built that way because it was the quickest route
  from inside an AI workspace, and because one site was unreachable from the
  machine first used.
- **Why Belay must not copy it.** The step works only with that provider's
  connectors, so it fails the provider-independence requirement. And a language
  model is executing the query, so two runs are not guaranteed to do the same
  thing, which fails the determinism requirement. The other project contains
  the damage by freezing the agent's raw output and treating everything the
  agent reads as data, never as instructions. That containment is sound; the
  dependency is still not acceptable for Belay.
- **Replication path for Belay.** Write the screen as an ordinary scheduled
  script behind the ADR-013 contract, against a documented screening or market
  data interface, storing the raw response unchanged. Keep the two ideas that
  did work:
  - **Request and response as separate, create-only files keyed by a request
    identifier**, so a retry can never silently overwrite an answer, and the
    requester never widens its request after the fact.
  - **Read back every write to shared or synced storage and compare it byte for
    byte** before treating it as saved. One silently corrupt upload cost a
    failed run; this rule was the fix.
- **Gaps it recorded.**
  - A ticker that was renamed comes back "not found", and a naive reader takes
    that for a delisting. The fix is a hand-verified alias list, never an
    automatic one.
  - A symbol that returns nothing gets an explicit "delisted or unavailable"
    row and **stays in the sample**. Removing it would be survivorship bias
    introduced by the collector itself.
  - The screener's own relative-volume field disagreed with its own volume and
    average-volume fields in the large majority of rows. Derived fields from a
    screener should be recomputed from real bars, never trusted.

---

## Data that project wanted and never solved

- **A free, reliable share float.** Ruled dead. Float could not be measured to
  better than roughly one part in seven from any free source, the SEC does not
  publish it, and the screener's figure was sometimes larger than the whole
  company.
- **Price history for very cheap, thinly held stocks.** Structurally missing.
  That population delists at a high rate, so the vendors used under-represent
  it. This is survivorship bias inside the source, and it is the same wall
  Belay's own free source hits. It is a reason to expect that a paid,
  survivorship-free dataset is unavoidable for any strategy that selects from
  that population.
- **An authoritative trading calendar.** Not solved there either. Dropping
  flagged and zero-volume bars recovered one broker's calendar to within a bar
  on small stocks, which is a useful check and not a calendar. Belay's own
  calendar proposal is still owed (`docs/OwnerDecisions.md` Part 10g).

## Not established by this note

- Whether any source above permits the use Belay intends, including commercial
  use in a product that is sold. Every vendor's terms must be read before Belay
  depends on it. This matters more for Belay than for a personal project.
- Anything about intraday data, fundamentals, corporate actions as a dataset,
  or macroeconomic series. The other project did not collect them.
- Whether these lessons hold on other instruments, dates or library versions.
