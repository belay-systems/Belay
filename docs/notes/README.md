# Original Design Notes

These are the working notes from the first build of Belay. They were committed
without file extensions and scattered across the repository — at the root, inside
`framework/`, inside `framework/artifacts/`, and elsewhere.

A file with no extension is effectively invisible. It does not match a `*.md`
search, does not render on GitHub, and is skipped by most tooling. One of these
notes turned out to contain a repository-wide specification that no session had
ever read: the document metadata standard, now promoted to
[`docs/DocumentStandard.md`](../DocumentStandard.md).

They were renamed on 2026-07-26 so that cannot happen again. Content is unchanged;
`git log --follow` still reaches the original history. Filenames encode the original
location — `framework-workflows-Weekly-Research.md` was `framework/workflows/Weekly Research`.

---

## What is in here

**Directory listings** — `Directory.md`, `Knowledge-Directory.md`,
`departments-Directory.md`, `framework-directory.md`, `framework-departments.md`,
`framework-artifacts-Artifact-Framework.md`, `framework-services-New-Directory.md`,
`strategies-Directory.md`, `strategies-Strategy-Folder-Template.md`,
`workflows-Directory.md`.

Planned repository structures. Several describe directories that were never created
(`memory/`, `templates/`, `experiments/`, `reviews/`, `archive/`, `.github/`) and
modules that were never written. Two of them explain the broken imports recorded in
`docs/HANDOFF.md`: `framework-services-New-Directory.md` lists a planned
`backtesting.py`, and `framework-departments.md` describes a planned
`framework/departments/` package. The code that imports them is reaching for
structure that was designed and never built.

**Draft code** — `framework-First-Workflow.md`,
`framework-workflows-Promotion-Review.md`, `framework-workflows-Weekly-Research.md`,
`framework-workflows-The-Belay-Object.md`, `framework-artifacts-universe.md`.

Early sketches of the workflow engine and the Belay object. None of it runs;
`framework-artifacts-universe.md` would fail three ways, and is the origin of the
`UniverseReport` artifact type that the `ArtifactType` enum has never had.

Retained rather than deleted, per Immutable Law VII and
`constitution/Strategy_Retirement.md`: Belay never deletes research. These are
superseded, not worthless — they record what the framework was intended to become.

**Commit records** — `Commit-000007.md`, `Commit-Summary.md`. Historical.

---

These are history, not specification. Where a note disagrees with a document in
`constitution/`, `docs/`, or `Knowledge/`, the note is out of date.
