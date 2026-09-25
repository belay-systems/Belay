## What this changes, and why

<!-- Plain language. Link the Issue this pull request claims: "Closes #123". -->

## Evidence

<!-- Paste the exact commands and queries you ran, and their output. A count,
a rate, or an "appears nowhere" claim without its query beside it will be sent back. -->

## Independent pass

<!-- Who or what tried to break this, other than its author? A different session
or a different model. Paste what it found and what you did about each item.
"None run yet" is an acceptable answer on a draft, never on a merge request. -->

## Checklist

- [ ] Continuous integration is green **on this pull request** (a local green does not count)
- [ ] Same inputs give the same outputs: no unrecorded call to an AI model, no unpinned "now", no network in tests
- [ ] Nothing here depends on one AI provider's tools, memory, connectors or file formats
- [ ] No change to `constitution/`, `docs/OwnerDecisions.md`, `LICENSE` or an ADR's status, or the owner asked for it (link)
- [ ] Every line citation I added or moved still points at the line it means
- [ ] No secrets, account identifiers, personal paths, email addresses or licensed data
- [ ] At a session close: `docs/NOW.md` rewritten, a `docs/sessions/` record added, `docs/FINDINGS.md` updated for any finding opened or closed, and `docs/OperatorChecklist.md` if the owner now has something to do

**Authored with:** <!-- the AI service and model that did the work, and who directed it -->
