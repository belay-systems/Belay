# Session Records

One file per session, named `YYYY-MM-DD-short-name.md`, written at session
close. Each one says what was asked, what was done, what was verified and how,
and what is left open.

**A record is never edited after it merges.** A later session that finds it
wrong writes its correction in its own record and names the file it corrects.
The same rule already holds for `reports/review/`.

Records before 2026-09-25 are in `docs/HANDOFF.md`, which is frozen. The
current state is in `docs/NOW.md`, and the reasons for this layout are in
`AGENTS.md`, "Files that grow".

`tests/test_handoff_files.py` checks the file names and caps each record at 300
lines. A session that needs more is two pieces of work, or it belongs in a
proposal under `docs/proposals/`.
