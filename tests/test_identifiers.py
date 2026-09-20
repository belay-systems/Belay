"""Identifier format and prefixes, per Knowledge/Identifiers.md."""

import pytest

from framework.artifacts.enums import ArtifactType
from framework.artifacts.factory import ArtifactFactory
from framework.identifiers import (
    PREFIXES,
    VALID_PREFIXES,
    build,
    identifier_key,
    is_valid,
    validate,
)


def test_build_pads_to_four_digits():
    assert build("report", 217) == "RPT-0217"
    assert build("strategy", 1) == "STRAT-0001"


def test_build_rejects_an_unknown_kind():
    with pytest.raises(ValueError, match="Unknown artifact kind"):
        build("drawdown", 1)


def test_the_eight_documented_prefixes_are_present():
    assert VALID_PREFIXES == {
        "STRAT",
        "EXP",
        "RS",
        "REV",
        "RPT",
        "REGIME",
        "WF",
        "DOC",
    }
    # REGIME and DOC were missing from this module until 2026-07-26.
    assert "REGIME" in PREFIXES.values()
    assert "DOC" in PREFIXES.values()


@pytest.mark.parametrize(
    "identifier", ["STRAT-0001", "EXP-0014", "RS-0081", "REGIME-0010", "RPT-0217"]
)
def test_documented_examples_are_valid(identifier):
    # Every example given in Knowledge/Identifiers.md.
    assert is_valid(identifier)


@pytest.mark.parametrize(
    "identifier",
    [
        "DD-0001",  # the prefix the drawdown tests used; it never existed
        "1",
        "RPT-1",  # not four digits
        "rpt-0001",  # lowercase
        "RPT0001",  # no separator
        "",
        None,
    ],
)
def test_malformed_identifiers_are_rejected(identifier):
    assert not is_valid(identifier)
    with pytest.raises(ValueError, match="Invalid artifact identifier"):
        validate(identifier)


# ------------------------------------------------- beyond ten thousand, ADR-014


def test_an_identifier_may_carry_more_than_four_digits():
    """Four digits capped every prefix at 10,000 identifiers for all time.

    `Knowledge/Identifiers.md:3-5` makes identifiers permanent and never reused,
    and ADR-014 rule 4 mints one per stored series version — so a 6,000-symbol
    backfill would spend 60% of the RPT space in a single run. The document
    states no digit count; every one of its seven examples happens to use four,
    and this module turned that into a rule.
    """
    assert is_valid("RPT-10000")
    assert is_valid("STRAT-123456")


def test_build_and_validate_agree_past_ten_thousand():
    """`build` pads to a minimum of four rather than a width of four, so the two
    halves of this module must not disagree about what it produced."""
    assert build("report", 10000) == "RPT-10000"
    assert validate(build("report", 10000)) == "RPT-10000"


def test_a_number_padded_past_the_four_digit_form_is_refused():
    """`RPT-00217` and `RPT-0217` denote the same number and are two different
    directories under `ArtifactRepository.path_for`.

    Already refused before the pattern was widened — this is the guard on the
    widening rather than a defect it fixed. `\\d{4,}` would have admitted both,
    and identifiers are permanent, so the ambiguity could never be corrected.
    """
    assert not is_valid("RPT-00217")
    assert not is_valid("RPT-010000")


def test_identifiers_order_by_number_rather_than_by_string():
    """Sorting the strings puts `RPT-10000` before `RPT-9999`.

    The same defect `version_key` exists for, and the same one that makes the
    data store zero-pad its version filenames. A fixed width hid it here; the
    width is no longer fixed.
    """
    identifiers = ["RPT-10000", "RPT-9999", "RPT-0217", "STRAT-0001"]

    assert sorted(identifiers) == ["RPT-0217", "RPT-10000", "RPT-9999", "STRAT-0001"]
    assert sorted(identifiers, key=identifier_key) == [
        "RPT-0217",
        "RPT-9999",
        "RPT-10000",
        "STRAT-0001",
    ]


def test_an_unorderable_identifier_never_sorts_as_the_newest():
    """`version_key`'s convention, for the same reason: history stays searchable,
    but nothing unorderable may present itself as the most recent."""
    ordered = sorted(["RPT-0217", "not-an-identifier", "DD-0001"], key=identifier_key)

    assert ordered[-1] == "RPT-0217"


@pytest.mark.parametrize(
    "identifier",
    [
        "RPT-٠١٢٣",  # Arabic-Indic digits
        "RPT-०१२३",  # Devanagari digits
        "RPT-0001\n",  # `$` matches before a trailing newline; `\Z` does not
    ],
)
def test_a_non_ascii_or_newline_terminated_identifier_is_refused(identifier):
    """Found by an independent pass over the widening that was meant to close
    exactly this class of hole, one commit after it landed.

    `\\d` is Unicode-aware, so all three of these validated and produced the
    *same* `identifier_key` as `RPT-0123` — three directories for one number,
    reachable through `ArtifactRepository.save()`, and permanent because
    identifiers are never corrected. The `[1-9]` branch was already ASCII-only,
    which made the four-digit branch the looser of the two and nothing said so.
    """
    assert not is_valid(identifier)
    assert identifier_key(identifier)[0] == 0, "and it must not sort as a valid one"


def test_factory_rejects_a_malformed_identifier():
    """An identifier is permanent — the one field that cannot be corrected
    later — so it is checked at creation rather than at validation."""
    with pytest.raises(ValueError, match="Invalid artifact identifier"):
        ArtifactFactory().create(
            identifier="DD-0001",
            title="Max drawdown",
            artifact_type=ArtifactType.REPORT,
        )
