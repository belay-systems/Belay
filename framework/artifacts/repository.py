"""Durable storage for artifacts. Append-only.

`save()` wrote to `{id}.yaml` until 2026-07-26, so saving a second version of an
artifact silently destroyed the first. Ten documents forbid that, among them
Immutable Law VII, `constitution/Strategy_Retirement.md`,
`Knowledge/Versioning.md` ("No version is overwritten. Historical versions remain
searchable"), `Knowledge/KnowledgeGraph.md` ("the graph is append-only. History is
never destroyed") and `AGENTS.md`.

Artifacts are now stored one directory per identifier, one file per version, and a
write that would change an existing version is refused rather than performed.
"""

from __future__ import annotations

from pathlib import Path

from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.primitives import is_semantic_version, version_key
from framework.artifacts.serializer import ArtifactSerializer
from framework.identifiers import identifier_key

# ADR-014 rule 1. Relative, so the artifacts travel with a clone — and unlike
# `framework/data/store.py`'s `STORE_ROOT`, so do their contents: rule 2 tracks
# everything under here, because `constitution/Governance.md:27` makes
# institutional memory mandatory and a record on one machine is not that.
#
# **A constant rather than a caller's argument, which is the actual finding.**
# `__init__` took `root` with no default until 2026-08-02, so every caller chose
# one and no two had to agree — which is why "where do artifacts live" had no
# answer in code or in any document, and why `.gitignore` could not name a
# directory. The argument stays for tests and for diagnostics; what changed is
# that there is a default and it is written down.
ARTIFACT_ROOT = Path("artifacts")


class ArtifactRepository:

    def __init__(self, root=ARTIFACT_ROOT, serializer=None):
        self.root = Path(root)
        self.serializer = serializer or ArtifactSerializer()

    def identifiers(self) -> list[str]:
        """Return every identifier with something stored, in identifier order.

        Ordered by `identifier_key` rather than by filename, because four digits
        stopped being the width on 2026-08-02 and `RPT-10000` sorts before
        `RPT-9999` as a string. Nothing is hidden: a directory whose name is not
        a valid identifier is listed, ordered below every valid one, on the same
        convention `versions()` uses for unorderable version stems.
        """
        if not self.root.is_dir():
            return []
        return sorted(
            (folder.name for folder in self.root.iterdir() if folder.is_dir()),
            key=identifier_key,
        )

    def path_for(self, identifier: str, version: str) -> Path:
        """Return where a given version of an artifact lives.

        `{root}/{id}/{version}.yaml`. One directory per artifact, so listing
        the directory answers "what versions of this exist" — which is what
        `Knowledge/Versioning.md` means by historical versions remaining
        searchable.
        """
        return self.root / identifier / f"{version}.yaml"

    def versions(self, identifier: str) -> list[str]:
        """Return every stored version of an artifact, oldest first.

        Ordered by semantic precedence, not by filename. Sorting the filenames
        placed `0.10.0` before `0.9.0`, which made the last element something
        other than the newest version.

        Nothing on disk is hidden: `Knowledge/Versioning.md` requires that
        historical versions remain searchable. A stem that is not a semantic
        version is listed, ordered below every valid version so that it can
        never be read as the newest. Use `latest()` rather than indexing.
        """
        folder = self.root / identifier
        if not folder.is_dir():
            return []
        return sorted((path.stem for path in folder.glob("*.yaml")), key=version_key)

    def latest(self, identifier: str) -> str | None:
        """Return the newest stored version of an artifact, or None if it has none.

        `versions()` used to be the only ordering the repository offered, so
        anything needing the current version of an artifact had to index into
        it and get the ordering right on its own.

        That question became a capital fact when ADR-004 landed. A strategy can
        now move backward, so its current stage is no longer the highest stage
        it ever reached — it can only be read from its genuinely most recent
        version. A wrong "latest" yields a wrong current stage.

        Raises if no stored version is orderable. The repository does not guess
        which of them is current: a plausible wrong answer here is worse than a
        refusal, because nothing downstream could tell the two apart.
        """
        stored = self.versions(identifier)
        if not stored:
            return None

        newest = stored[-1]
        if not is_semantic_version(newest):
            raise ValueError(
                f"Cannot determine the latest version of {identifier!r}: "
                f"no stored version is a semantic version ({', '.join(stored)}). "
                "Knowledge/Versioning.md requires MAJOR.MINOR.PATCH."
            )
        return newest

    def get(self, identifier: str, version: str | None = None):
        """Return a stored artifact, or None if there is no such version.

        With no `version`, returns the current one — `latest()` chooses it, so
        this inherits that method's two conventions rather than inventing a
        second set. Nothing stored gives None; nothing *orderable* stored raises,
        because the repository does not guess which of several unorderable files
        is current.

        Until `ArtifactSerializer.load()` landed with ADR-009 there was nothing
        to return. `latest()` hands back a version *string* for exactly that
        reason, and a caller wanting a strategy's current stage had to open the
        file itself. This is the method that question actually wanted.

        **Reading verifies integrity. The decision, and why.**

        `save()` already refuses unsigned and tampered artifacts, so everything
        that entered through the write boundary was intact when it landed. That
        is the whole of what a write-time check can promise: it says nothing
        about the file afterwards. A YAML edited by hand on disk, or a byte lost
        to the filesystem, is invisible to every check `save()` performs, and the
        read is the only place left that can notice.

        The alternative was to let the validator stay the only gate — `load()`
        deliberately does not re-sign, so a tampered file loads successfully and
        then fails `ArtifactValidator`. That is the right behaviour for `load()`,
        which is a parser and should hand back exactly what is on disk so the
        tampering is *visible* rather than hidden. It is the wrong behaviour
        here. `get()` is not a parser; it is the repository vouching for a
        record, and its likeliest caller is a promotion gate asking for a
        strategy's current stage. Returning a hand-edited stage with no signal,
        on the assumption that every caller remembers to validate, is the silent
        wrong answer this repository has been bitten by three times — most
        recently by a dashboard parser whose fallback looked exactly like a
        working parse.

        Verifying here does not contradict "loading is not signing". It depends
        on it: because `load()` keeps the stored hash instead of computing a
        fresh one, there is something here left to check. Had `load()` re-signed,
        this check would pass unconditionally and mean nothing.

        Nor is it a second gate reimplementing the first. It is one line —
        `ArtifactIntegrity.verify_hash`, the same call `save()` makes — and it
        covers integrity only. `ArtifactValidator` still owns identifiers,
        relationships, evidence grades and lifecycle rules, and callers that need
        those still run it.

        Nothing is hidden by refusing. The file stays on disk, `versions()` still
        lists it — `Knowledge/Versioning.md` requires historical versions to
        remain searchable — and `ArtifactSerializer.load()` remains available to
        anyone who needs to read a damaged artifact to diagnose it. What is
        refused is this method silently presenting it as a sound record.
        """
        if version is None:
            version = self.latest(identifier)
            if version is None:
                return None

        path = self.path_for(identifier, version)
        if not path.exists():
            return None

        artifact = self.serializer.load(path.read_text(encoding="utf8"))

        if artifact.integrity_hash is None:
            raise ValueError(
                f"Refusing to return unsigned artifact {identifier!r} "
                f"version {version!r} from {path}. It did not enter through "
                "save(), which refuses unsigned artifacts."
            )
        if not ArtifactIntegrity.verify_hash(artifact):
            raise ValueError(
                f"Refusing to return artifact {identifier!r} version {version!r} "
                f"from {path}: integrity hash does not match its contents. "
                "It was altered after it was stored."
            )
        return artifact

    def save(self, artifact) -> Path:
        """Write an artifact to disk. Never overwrites a differing version.

        Re-saving a byte-identical artifact is a no-op and returns the existing
        path, so saving twice is harmless. Writing *different* content to a
        version that already exists raises: that is a history rewrite, and the
        repository is the boundary where history becomes durable.
        """
        # An unsigned artifact must not enter durable storage. This is the same
        # rule the validator enforces, applied at the point where an artifact
        # stops being a value in memory and becomes a record.
        if artifact.integrity_hash is None:
            raise ValueError(
                f"Refusing to store unsigned artifact {artifact.id!r}. "
                "Build it through ArtifactFactory, which signs."
            )
        if not ArtifactIntegrity.verify_hash(artifact):
            raise ValueError(
                f"Refusing to store artifact {artifact.id!r}: "
                "integrity hash does not match its contents."
            )

        # A version that cannot be ordered is a permanent defect once written.
        # Storage is append-only, so the file can never be corrected or removed
        # — Immutable Law VII and `Knowledge/Versioning.md` both forbid it — and
        # every later attempt to answer "what is the current version of this
        # artifact" inherits the ambiguity. Before it lands is the only place to
        # catch it, which is why this sits beside the other two refusals rather
        # than in the validator.
        if not is_semantic_version(artifact.version):
            raise ValueError(
                f"Refusing to store {artifact.id!r} at version {artifact.version!r}. "
                "Knowledge/Versioning.md requires semantic versioning: "
                "MAJOR.MINOR.PATCH, for example 1.2.4."
            )

        path = self.path_for(artifact.id, artifact.version)
        payload = self.serializer.dump(artifact)

        if path.exists():
            if path.read_text(encoding="utf8") == payload:
                return path
            raise FileExistsError(
                f"{artifact.id} version {artifact.version} already exists and differs. "
                "Versions are never overwritten; increment the version instead."
            )

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf8")
        return path
