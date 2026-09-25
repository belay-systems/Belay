# Belay

> An evidence-driven investment intelligence platform. Paper-first, by constitution.

**Status: foundation stage. Belay trades nothing today.** It has no strategy, no
backtester and no execution. What exists is the groundwork that has to be right
first. It is proprietary software, published to be read.

[![conformance](https://github.com/belay-systems/Belay/actions/workflows/conformance.yml/badge.svg)](https://github.com/belay-systems/Belay/actions/workflows/conformance.yml)
![status: alpha](https://img.shields.io/badge/status-alpha%20%C2%B7%20foundation-orange)
![python: 3.11 | 3.12 | 3.13](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)
![licence: proprietary](https://img.shields.io/badge/licence-proprietary-lightgrey)

> **Provenance.** Belay's git history begins with this repository's first
> commit. The platform was called Atlas and lived in a separate repository of
> that name until 2026-09-20, and its documents are reproduced here in full.
> **Commit ids, pull request numbers and Issue numbers dated before that first
> commit refer to that private archive and will not resolve here.** The full
> note is at the top of [`docs/HANDOFF.md`](docs/HANDOFF.md).

Belay is a framework for investment research, strategy validation, paper
trading, capital governance, and institutional knowledge. It is a trading
*platform*, not a trading bot: research is separated from execution, strategies
are plug-ins, risk can veto any signal, and every result is kept as evidence.

---

## Core philosophy

Capital is earned. Ideas are cheap. Evidence is expensive.

Every strategy must prove itself before it is trusted with capital, and no
strategy may skip a stage.

- Preserve capital.
- Maximize long-term compounded returns.
- Continuously improve through evidence.
- Avoid narrative-driven decision making.
- Maintain institutional knowledge.

## The lifecycle every strategy must climb

Idea → Research → Validation → Paper Trading → Promotion Review → Micro Capital → Limited Capital → Production

A strategy can be retired from any stage, and demoted from Promotion Review or
above (ADR-004 in `docs/DECISIONS.md` sets that floor: below it there is no
capital privilege to withdraw). The stages are defined in
`constitution/Paper_First_Capital_Doctrine.md`, and the code is held to them by
tests that read that document.

## Two promises the software makes

- **Deterministic.** The same inputs give the same outputs, on any machine.
  Live data is captured once, frozen, and everything is computed from the
  frozen copy.
- **Independent of any AI provider.** Belay is built with AI agents and depends
  on none of them. No part of it needs a particular AI service to run.

## Where things are

| Path | What it holds |
|---|---|
| `constitution/` | The governing documents. Everything else answers to these. |
| `departments/`, `Research/`, `Validation/`, `Operations/` | The governance layer's departments: who is responsible for what, in prose. |
| `workflows/`, `strategies/`, `Knowledge/` | Governance prose for processes, the strategy lifecycle, and the knowledge system. |
| `framework/` | The code (the mechanics layer): artifacts, identifiers, metrics, the market data boundary. `framework/workflows/` is code; `workflows/` is the prose it must answer to. |
| `tests/` | The suite, including tests that hold the code to the governing documents. |
| `scripts/` | The status dashboard and the review scheduling gate. |
| `artifacts/` | Stored, versioned, integrity-checked artifacts. |
| [`docs/README.md`](docs/README.md) | **Index of the documents in `docs/`, and which question each answers. Start here.** |
| `docs/Architecture.md` | How the pieces fit. |
| `docs/ROADMAP.md` | The stages of the build. |
| `docs/DECISIONS.md` | Architecture decision records, with their reasoning. |
| `docs/OwnerDecisions.md` | What the owner has ruled, in the owner's words. |
| `docs/NOW.md` | Current state and the next task. Open findings are in `docs/FINDINGS.md`; history in `docs/sessions/` and `docs/HANDOFF.md`. |
| `docs/research/` | Non-binding research notes. |
| `CHANGELOG.md` | What changed, and what each change got wrong along the way. |
| `reports/review/` | Adversarial reviews Belay has run against itself. |

## What is built, and what is not

Built: the artifact contract (immutable, versioned, integrity-checked), the
identifier scheme, a metrics library with mandatory disclosures, significance
and sample-adequacy statistics, and a market data boundary with a versioned
store and survivorship disclosure.

Not built: a backtester, a risk engine, any strategy, paper trading, execution.

For the real state at this moment, run the dashboard. It is re-derived from the
repository on every run and outranks this page.

## Getting started

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

The suite touches no network. On Windows, `refresh-status.cmd` builds and opens
the dashboard in one step.

## Contributing

Belay is built by a small group, each directing an AI agent of their choice.
People start at `CONTRIBUTING.md`. AI agents start at `AGENTS.md`, and the
instructions there are the same for every provider. Work is claimed through
Issues and lands only through reviewed pull requests.

Belay publishes the defects it finds in itself. The reviews under
`reports/review/` and the findings register in `docs/FINDINGS.md` are part of the
product, not an embarrassment.

## Security

See `SECURITY.md` for how to report a vulnerability privately.

## Licence

Proprietary. All rights reserved. The source is published to be read and so
that invited contributors can work on it. See `LICENSE`.

## Not investment advice

Nothing in this repository is investment, financial, legal or tax advice, a
recommendation, or an offer to buy or sell any security. Belay is unfinished
research software.

---

Version `v1.0.0-alpha` · Development status: Foundation
