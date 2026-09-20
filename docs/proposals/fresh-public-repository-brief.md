# Session brief — build "Belay", the fresh public repository

**Status: a brief for the next session. It decides nothing.** The rulings it
rests on are `docs/OwnerDecisions.md` Parts 11, 12 and 13. Written 2026-09-19.

## What is being done, in plain language

Atlas's code and documents are copied, without their git history, into a new
repository named **Belay**. Belay becomes the public, day-to-day home for the
two owners and their AI agents. The Atlas repository keeps that name, stays
private for good, and is the archive. Nothing is lost: every old commit,
branch and pull request stays here.

Why a copy and not this repository: four independent passes found no secret
anywhere, but this repository's *history* holds things no file edit removes
(Part 12b lists them).

## Before building: three questions still to put, one at a time

Each with a recommendation and the reasons, per `AGENTS.md`.

1. **Whose account holds Belay: the owner's personal account, or a free GitHub
   organization both owners belong to?** Recommendation to offer: an
   organization. Both owners are then owners in GitHub's eyes, the project does
   not hang off one personal account, and branch protection is free for a public
   repository either way. Cost: a few minutes of setup by the owner, who must
   create it personally.
2. **Does the platform keep the name "Atlas" inside Belay** (the Python package
   `atlas`, the constitution's wording, every document), with "Belay" as the
   repository and venture name? Recommendation to offer: yes for now. Renaming
   the platform touches hundreds of lines that tests read, and buys nothing
   until there is something to sell.
3. **Does the scheduled fortnightly review move to Belay?** Recommendation to
   offer: yes, once Belay is the working repository, by editing the existing
   routine in place. Never recreate it: a recreated routine attaches every
   connector on the account, which once included one able to place orders.

Also needed from the owner, as facts and not decisions: the second
contributor's GitHub username (for `.github/CODEOWNERS` if they are to review,
and for the invitation), and confirmation that "Keep my email addresses
private" is switched on in the owner's GitHub email settings.

## Build steps

1. **Export, do not clone.** `git archive` of `main` into a new folder outside
   this repository. A clone would carry the history along.
2. **Edit the snapshot for its new home.** Repository URLs and the CI badge in
   `README.md`; owner handles in `.github/CODEOWNERS`; any sentence that says
   "this repository is private". Add one provenance note, in `README.md` and at
   the top of `docs/HANDOFF.md`: commit ids and pull request numbers dated
   before Belay's first commit refer to a private archive and will not resolve.
   Do not rewrite the old citations themselves.
3. **Include the review reports and the full findings register** (Part 13a),
   subject to step 5.
4. **`git init`, set the commit identity to GitHub's no-reply address before the
   first commit**, and make exactly one commit. Check it:
   `git log --format='%an|%ae|%cn|%ce'` must show no personal address.
5. **Two independent passes on the snapshot, by different models, before it is
   pushed anywhere.** Told to falsify, not to review. At minimum: personal names,
   usernames, home-directory paths, email addresses, relationship words, account
   or broker identifiers, routine, session and workflow ids, anything from the
   owner's other project beyond `docs/research/known-data-sources.md`; and that
   the history is one commit. "Safe to publish" in Part 13a means these passes
   report nothing that must be fixed.
6. **Run the whole suite in the snapshot.** Three tests shell out to git and
   need the `git init`; `scripts/review_due.py` reads git history and may behave
   differently with one commit. A failure here is a finding, not noise.
7. **Create Belay as a PRIVATE repository first**, push, and confirm all five
   conformance checks pass there.
8. **The owner makes Belay public personally.** Then, the same day, the ruleset
   on `main`: require a pull request; require the five checks by name; require
   review from Code Owners; block force-pushes and deletion; secret scanning
   and push protection on; private vulnerability reporting on; Issues on;
   Actions set to require approval for first-time contributors (Part 13c).
9. **Seed the first Issues.** Candidates already known: the second independent
   pass owed on the evidence-bar proposal and on
   `docs/proposals/sample-adequacy-definition.md`; ADR-011's misquotation of
   `docs/HANDOFF.md`, repeated in a test comment; the stale suite count in
   `CHANGELOG.md`.
10. **Carry the two open drafts across** as fresh pull requests in Belay: the
    ADR-015 proposal and the Windows fix for `scripts/review_due.py`.
11. **Close this repository down as a workplace.** Its `README.md` gains one
    line saying development moved. The owner may mark it archived (read-only) on
    GitHub. On the owner's machine, the old folder is renamed and Belay is
    cloned into the path the old one had, so that tools which key their
    settings to a folder path keep working.

## What this brief must not be read as doing

It creates nothing and publishes nothing. Making Belay public is the owner's own
action, after step 5 reports clean.
