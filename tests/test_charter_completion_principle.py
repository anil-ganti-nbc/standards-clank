"""Guards for charter.md section F (Completion), added 2026-08-31 after
Operations reached v1 to make explicit that Standards Clank's finish
condition is evidence-based, not taxonomy-based: filling every chartered
domain (section B's list) is not the goal, and a domain absent standards
is not itself proof of a gap.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHARTER = REPO / "docs" / "charter.md"


def _text() -> str:
    return CHARTER.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    """Collapse markdown line-wrapping so a phrase spanning a wrapped
    line is still matchable as one contiguous string."""
    return re.sub(r"\s+", " ", text)


def test_charter_has_a_completion_section():
    text = _text()
    assert "## F. Completion" in text


def test_completion_section_states_the_evidence_based_finish_condition():
    section = _flat(_text().split("## F. Completion")[1])
    assert (
        "all materially evidenced fleet-wide normative concerns have "
        "been either standardized, explicitly rehomed, held with "
        "reopening triggers, or rejected"
    ) in section


def test_completion_section_states_the_taxonomy_corollary():
    section = _flat(_text().split("## F. Completion")[1])
    assert "New domains are created from evidence, not from taxonomy" in section
    assert "should not be populated merely because it exists in the original charter" in section


def test_completion_section_disclaims_empty_scaffolding_as_a_gap():
    section = _flat(_text().split("## F. Completion")[1])
    assert "does not require every chartered domain to contain standards" in section
    assert "not itself evidence of a standards gap" in section


def test_scope_section_cross_references_completion():
    """Section B's domain list is the exact thing readers could misread
    as a work list — it must point at section F rather than stand alone."""
    section_b = _flat(_text().split("## B. Scope")[1].split("## C. Non-goals")[0])
    assert "not a work list of domains it is obligated to fill" in section_b
    assert "section F" in section_b
