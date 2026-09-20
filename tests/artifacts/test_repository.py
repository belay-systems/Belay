"""Persistence. Until 2026-07-26 none of this code had ever been executed.

The suite reported 46 passing while `ArtifactRepository.save()` had never run
once, because no test referenced it and the module could not even be imported —
pyyaml was declared in pyproject.toml but not installed.
"""

import subprocess
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path

import pytest
import yaml

from framework.artifacts.artifact import Artifact
from framework.artifacts.enums import ArtifactType
from framework.artifacts.factory import ArtifactFactory
from framework.artifacts.integrity import ArtifactIntegrity
from framework.artifacts.repository import ARTIFACT_ROOT, ArtifactRepository
from framework.artifacts.serializer import ArtifactSerializer

FIXED_TIME = datetime(2026, 1, 1, tzinfo=timezone.utc)


def _artifact(**kwargs):
    kwargs.setdefault("created", FIXED_TIME)
    kwargs.setdefault("updated", FIXED_TIME)
    kwargs.setdefault("content", (("value", 0.5),))
    return ArtifactFactory().create(
        identifier="RPT-0001",
        title="Max drawdown",
        artifact_type=ArtifactType.REPORT,
        **kwargs,
    )


def test_save_writes_a_file_that_parses(tmp_path):
    repo = ArtifactRepository(tmp_path)

    path = repo.save(_artifact())

    assert path.exists()
    parsed = yaml.safe_load(path.read_text(encoding="utf8"))
    assert parsed["id"] == "RPT-0001"
    assert parsed["integrity_hash"]


def test_save_paths_by_identifier_and_version(tmp_path):
    repo = ArtifactRepository(tmp_path)

    path = repo.save(_artifact(version="1.2.3"))

    assert path == tmp_path / "RPT-0001" / "1.2.3.yaml"


def test_a_new_version_does_not_destroy_the_previous_one(tmp_path):
    """The defect this module was rewritten to fix.

    Saving to `{id}.yaml` meant version 2 silently overwrote version 1.
    Immutable Law VII: institutional knowledge shall never be intentionally
    discarded.
    """
    repo = ArtifactRepository(tmp_path)

    first = repo.save(_artifact(version="1.0.0", content=(("value", 0.5),)))
    second = repo.save(_artifact(version="2.0.0", content=(("value", 0.9),)))

    assert first.exists()
    assert second.exists()
    assert repo.versions("RPT-0001") == ["1.0.0", "2.0.0"]

    assert yaml.safe_load(first.read_text(encoding="utf8"))["content"] == [
        ["value", 0.5]
    ]


def test_rewriting_an_existing_version_is_refused(tmp_path):
    repo = ArtifactRepository(tmp_path)
    repo.save(_artifact(version="1.0.0", content=(("value", 0.5),)))

    with pytest.raises(FileExistsError, match="never overwritten"):
        repo.save(_artifact(version="1.0.0", content=(("value", 999.0),)))


def test_saving_the_same_artifact_twice_is_harmless(tmp_path):
    repo = ArtifactRepository(tmp_path)
    artifact = _artifact()

    assert repo.save(artifact) == repo.save(artifact)


def test_unsigned_artifacts_are_refused(tmp_path):
    repo = ArtifactRepository(tmp_path)
    unsigned = Artifact(id="RPT-0002", title="Unsigned", type=ArtifactType.REPORT)

    with pytest.raises(ValueError, match="unsigned"):
        repo.save(unsigned)


def test_tampered_artifacts_are_refused(tmp_path):
    repo = ArtifactRepository(tmp_path)
    forged = replace(_artifact(), content=(("value", 999.0),))

    with pytest.raises(ValueError, match="does not match"):
        repo.save(forged)


def test_versions_of_an_unknown_artifact_is_empty(tmp_path):
    assert ArtifactRepository(tmp_path).versions("RPT-9999") == []


def test_versions_orders_by_semantic_precedence_not_by_filename(tmp_path):
    """The defect: `sorted()` over strings compares character by character.

    `0.10.0` is the tenth minor release and `0.9.0` the ninth, but `"1" < "9"`,
    so a lexicographic sort puts the newer one first and the last element stops
    being the newest version. Since ADR-004 a strategy can move backward, so its
    current stage is no longer the highest stage it ever held — it can only be
    read from its most recent version. This ordering answers a capital question.
    """
    repo = ArtifactRepository(tmp_path)
    for version in ("0.9.0", "0.10.0", "0.2.0"):
        repo.save(_artifact(version=version))

    assert repo.versions("RPT-0001") == ["0.2.0", "0.9.0", "0.10.0"]


def test_versions_orders_every_component_numerically(tmp_path):
    """Major, minor and patch each cross the double-digit boundary independently."""
    repo = ArtifactRepository(tmp_path)
    for version in ("1.0.0", "1.0.10", "1.0.9", "1.10.0", "1.9.0", "10.0.0", "9.0.0"):
        repo.save(_artifact(version=version))

    assert repo.versions("RPT-0001") == [
        "1.0.0",
        "1.0.9",
        "1.0.10",
        "1.9.0",
        "1.10.0",
        "9.0.0",
        "10.0.0",
    ]


def test_latest_returns_the_newest_version_not_the_last_filename(tmp_path):
    repo = ArtifactRepository(tmp_path)
    repo.save(_artifact(version="0.9.0"))
    repo.save(_artifact(version="0.10.0"))

    assert repo.latest("RPT-0001") == "0.10.0"


def test_latest_of_an_unknown_artifact_is_none(tmp_path):
    assert ArtifactRepository(tmp_path).latest("RPT-9999") is None


@pytest.mark.parametrize(
    "version",
    ["draft", "1.0", "1.0.0.0", "v1.0.0", "01.0.0", "1.0.0-rc1", "1.0.x", ""],
)
def test_save_refuses_a_version_that_is_not_semantic(tmp_path, version):
    """Caught at the write boundary because it can never be caught later.

    Storage is append-only, so a version string that cannot be ordered can
    never be corrected or removed — Immutable Law VII and
    `Knowledge/Versioning.md` both forbid removing it. One such filename would
    break that artifact's ordering permanently, with no remedy. `save()`
    already refuses unsigned and tampered artifacts at this same boundary.

    `01.0.0` is refused for the same reason leading zeros are refused
    generally: it denotes the same version as `1.0.0` but is a different
    filename, so both could exist forever and nothing could say which is
    current.
    """
    repo = ArtifactRepository(tmp_path)

    with pytest.raises(ValueError, match="semantic versioning"):
        repo.save(_artifact(version=version))


def test_an_unorderable_stem_stays_searchable_but_never_reads_as_latest(tmp_path):
    """A file placed by hand bypasses `save()`, so ordering must absorb it.

    `Knowledge/Versioning.md` requires that historical versions remain
    searchable, so `versions()` lists it rather than hiding it. It sorts below
    every valid version, so it can never present itself as the newest.
    """
    repo = ArtifactRepository(tmp_path)
    repo.save(_artifact(version="1.0.0"))
    (tmp_path / "RPT-0001" / "draft.yaml").write_text("{}", encoding="utf8")

    assert repo.versions("RPT-0001") == ["draft", "1.0.0"]
    assert repo.latest("RPT-0001") == "1.0.0"


def test_latest_refuses_to_guess_when_no_version_is_orderable(tmp_path):
    """Raising beats returning a plausible wrong answer.

    A silent fallback looks exactly like a working parser — the failure mode
    that put a wrong figure on the dashboard for two sessions.
    """
    folder = tmp_path / "RPT-0001"
    folder.mkdir(parents=True)
    (folder / "draft.yaml").write_text("{}", encoding="utf8")

    with pytest.raises(ValueError, match="no stored version is a semantic version"):
        ArtifactRepository(tmp_path).latest("RPT-0001")


# --------------------------------------------------------------- get()
#
# The repository could store an artifact and never hand one back. `latest()`
# returns a version *string* because until `ArtifactSerializer.load()` landed
# with ADR-009 there was nothing else it honestly could return.
#
# Written before `get()` existed and run against the unchanged code to prove
# they fail rather than pass vacuously: 9 failed, 22 passed.


def test_get_returns_the_artifact_that_was_saved(tmp_path):
    """The round trip that closes the loop, checked through the signature.

    Field equality is the weaker assertion — a value that renders to the same
    text and hashes differently would satisfy it. `verify_hash` would not.
    """
    repo = ArtifactRepository(tmp_path)
    saved = _artifact()
    repo.save(saved)

    loaded = repo.get("RPT-0001")

    assert loaded.id == "RPT-0001"
    assert loaded.integrity_hash == saved.integrity_hash
    assert ArtifactIntegrity.verify_hash(loaded)


def test_get_returns_the_latest_version_when_none_is_named(tmp_path):
    """Which is the point. ADR-004 made "what is this strategy's current stage"
    a capital question, and it can only be read from the genuinely newest
    version — `0.10.0`, not the last filename alphabetically."""
    repo = ArtifactRepository(tmp_path)
    repo.save(_artifact(version="0.9.0", content=(("value", 0.5),)))
    repo.save(_artifact(version="0.10.0", content=(("value", 0.9),)))

    loaded = repo.get("RPT-0001")

    assert loaded.version == "0.10.0"
    assert loaded.content == (("value", 0.9),)


def test_get_returns_the_version_it_is_asked_for(tmp_path):
    """Storage is append-only so that superseded versions stay readable."""
    repo = ArtifactRepository(tmp_path)
    repo.save(_artifact(version="0.9.0", content=(("value", 0.5),)))
    repo.save(_artifact(version="0.10.0", content=(("value", 0.9),)))

    assert repo.get("RPT-0001", "0.9.0").content == (("value", 0.5),)


def test_get_of_an_unknown_artifact_is_none(tmp_path):
    """The empty case. `latest()` returns None rather than raising when nothing
    is stored, and `get()` follows it rather than inventing a second convention
    for the same situation."""
    assert ArtifactRepository(tmp_path).get("RPT-9999") is None


def test_get_of_an_identifier_with_no_stored_versions_is_none(tmp_path):
    """A directory that exists and holds nothing is still "nothing stored".

    Distinct from the case above: `versions()` takes a different branch —
    `is_dir()` succeeds and the glob comes back empty — and the two could
    diverge without anything noticing.
    """
    (tmp_path / "RPT-0001").mkdir(parents=True)

    assert ArtifactRepository(tmp_path).get("RPT-0001") is None


def test_get_of_a_version_that_was_never_stored_is_none(tmp_path):
    repo = ArtifactRepository(tmp_path)
    repo.save(_artifact(version="1.0.0"))

    assert repo.get("RPT-0001", "2.0.0") is None


def test_get_refuses_to_guess_when_no_version_is_orderable(tmp_path):
    """Matching `latest()`, which is where the refusal actually comes from.

    `get()` asks `latest()` which version is current, so it inherits both of
    that method's conventions — None for nothing stored, a raise for nothing
    orderable — rather than deciding again and risking a different answer.
    """
    folder = tmp_path / "RPT-0001"
    folder.mkdir(parents=True)
    (folder / "draft.yaml").write_text("{}", encoding="utf8")

    with pytest.raises(ValueError, match="no stored version is a semantic version"):
        ArtifactRepository(tmp_path).get("RPT-0001")


def test_get_refuses_an_artifact_altered_after_it_was_stored(tmp_path):
    """The decision recorded in `get()`: reading is a gate, not only writing.

    `save()` refused this artifact's forged twin at the write boundary, so
    everything that entered through `save()` was intact when it landed. That
    says nothing about the file afterwards. This edit happens on disk, after
    storage, where no write-time check can reach it — and the read is the only
    place left that can notice.

    `ArtifactSerializer.load()` still loads it. That is deliberate and unchanged:
    a parser should return what is on disk so the tampering is visible. What is
    refused is the repository presenting it as a sound record.
    """
    repo = ArtifactRepository(tmp_path)
    path = repo.save(_artifact())

    path.write_text(
        path.read_text(encoding="utf8").replace("Max drawdown", "Min drawdown"),
        encoding="utf8",
    )

    assert ArtifactSerializer().load(path.read_text(encoding="utf8")).title == "Min drawdown"
    with pytest.raises(ValueError, match="does not match"):
        repo.get("RPT-0001")


def test_get_refuses_an_unsigned_artifact_placed_by_hand(tmp_path):
    """`save()` cannot be the only guard, because a file can bypass it.

    The repository already assumes hand-placed files exist —
    `test_an_unorderable_stem_stays_searchable_but_never_reads_as_latest` is
    built on one. An unsigned artifact reaching a promotion gate through `get()`
    would carry no proof of who produced it or when.
    """
    repo = ArtifactRepository(tmp_path)
    unsigned = replace(_artifact(version="1.0.0"), integrity_hash=None)

    path = repo.path_for("RPT-0001", "1.0.0")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(ArtifactSerializer().dump(unsigned), encoding="utf8")

    with pytest.raises(ValueError, match="unsigned"):
        repo.get("RPT-0001")


# ------------------------------------------- ADR-014 rules 1 and 2: where, and git


def test_the_repository_has_a_default_root():
    """`__init__` took `root` with no default until 2026-08-02, so every caller
    chose one and no two had to agree — which is why "where do artifacts live"
    had no answer in code or in any document, and why `.gitignore` could not name
    a directory in the claim it was making about them."""
    assert ArtifactRepository().root == ARTIFACT_ROOT
    assert ARTIFACT_ROOT == Path("artifacts")


def test_the_artifact_root_is_relative_so_it_travels_with_a_clone():
    """`framework/data/store.py:36-39`'s reason, applied to the other half: an
    absolute path would make this machine-specific and silently empty everywhere
    else."""
    assert not ARTIFACT_ROOT.is_absolute()


def test_the_default_artifact_root_is_tracked_by_git():
    """ADR-014 rule 2, and the exact inverse of
    `test_the_default_store_root_is_ignored_by_git`.

    Asked of git rather than by reading `.gitignore`, for that test's reason. It
    passed before rule 2 was implemented — nothing ignored `artifacts/` because
    nothing wrote there — so this is the guard on the ruling rather than the
    proof of it: `constitution/Governance.md:27` makes institutional memory
    mandatory, and an ignored artifact root would put every signed record on
    exactly one machine, which is F-002 again by a different route.
    """
    probe = ARTIFACT_ROOT / "RPT-0001" / "1.0.0.yaml"

    result = subprocess.run(
        ["git", "check-ignore", "-q", str(probe)],
        cwd=Path(__file__).resolve().parents[2],
        capture_output=True,
    )

    # `== 1`, not `!= 0`. `git check-ignore` answers 0 for ignored and 1 for not
    # ignored, and returns 128 when it cannot run at all — outside a work tree,
    # or in a `git archive` export. `!= 0` reported success from a git invocation
    # that had errored, which is the tautology shape this repository keeps
    # shipping; the store's own test asserts `== 0` and fails correctly there.
    assert result.returncode == 1, (
        f"{probe} is ignored by git, or git could not answer (exit "
        f"{result.returncode}). ADR-014 rule 2 tracks every artifact: a record "
        "that exists on one machine is not institutional memory."
    )


def test_identifiers_are_listed_in_identifier_order(tmp_path):
    """Ordered by number rather than lexicographically, because four digits
    stopped being the width on 2026-08-02 and `RPT-10000` sorts before
    `RPT-9999` as a string."""
    repo = ArtifactRepository(tmp_path)
    for identifier in ("RPT-9999", "RPT-10000", "RPT-0217"):
        (tmp_path / identifier).mkdir()

    assert repo.identifiers() == ["RPT-0217", "RPT-9999", "RPT-10000"]


def test_listing_identifiers_of_an_absent_root_is_empty_rather_than_an_error(tmp_path):
    assert ArtifactRepository(tmp_path / "nothing-here").identifiers() == []
