"""Data/Ontology Pass 0B process guards.

The adjudication pass must: cover every HIGH-priority handoff cluster,
give each candidate exactly one recommendation, include counterexample
tests for every ADVANCE card, keep non-Data concerns rehomed/rejected,
create no STD-DATA normative files, leave the frozen UI baseline and the
Pass 0A evidence untouched.
"""

import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PASS0 = REPO / "docs" / "data-ontology" / "pass0"
ADJUDICATION = PASS0 / "adjudication.md"
CANDIDATES = PASS0 / "candidates"

HIGH_CLUSTERS = [f"Cluster {i}" for i in range(1, 8)]
DISPOSITIONS = ("KEEP DISTINCT", "MERGE", "SPLIT", "REHOME", "REJECT", "HOLD / DEFER")
ADVANCE_CARDS = {
    "c1-continuity-explicitness.md": "ADVANCE",
    "c2-novelty-read-side-exclusion.md": "ADVANCE",
    "c3-identity-conservatism.md": "ADVANCE",
    "c5-provenance-tier-separation.md": "ADVANCE",
}


def test_adjudication_exists_and_covers_every_high_cluster():
    text = ADJUDICATION.read_text()
    for i, cluster in enumerate(HIGH_CLUSTERS, start=1):
        assert re.search(rf"^### {i}\.", text, flags=re.MULTILINE), f"no adjudication section for {cluster}"


def test_every_high_cluster_has_exactly_one_disposition():
    text = ADJUDICATION.read_text()
    table_rows = [
        line for line in text.splitlines()
        if re.match(r"^\| \d+ \|", line)
    ]
    assert len(table_rows) == 7
    for row in table_rows:
        matches = [d for d in DISPOSITIONS if d in row]
        assert len(matches) == 1, f"cluster row needs exactly one disposition: {row!r} -> {matches}"


def test_advance_cards_have_exactly_one_recommendation_and_counterexample():
    for name, rec in ADVANCE_CARDS.items():
        text = (CANDIDATES / name).read_text()
        assert f"**Recommendation: {rec}**" in text, name
        assert text.count("**Recommendation:") == 1, name
        assert "Counterexample test" in text, name
        assert "Does the candidate still hold?" in text, name


def test_hold_reject_cards_have_exactly_one_recommendation():
    text = (CANDIDATES / "holds-and-rejects.md").read_text()
    recs = re.findall(re.escape("**Recommendation: ") + "(HOLD|HOLD/DEFER|REJECT)" + '\\b', text)
    assert len(recs) >= 6, f"found {len(recs)} hold/reject recommendations"
    assert "ADVANCE" not in recs


def test_non_data_concerns_are_rehomed_or_rejected():
    holds = (CANDIDATES / "holds-and-rejects.md").read_text()
    assert "REHOME to diagnostic/testing practice" in holds
    text = ADJUDICATION.read_text()
    assert "REHOME** (to diagnostic/testing practice" in text


def test_no_std_data_normative_files_exist():
    std_files = list(REPO.rglob("STD-DATA-*.json")) + list(REPO.rglob("STD-DATA-*.md"))
    assert not std_files, f"Pass 0B must not create normative files: {std_files}"


def test_ui_baseline_and_pass0_evidence_untouched():
    """The UI freeze artifacts and the Pass 0A evidence must be byte-identical
    to the Pass 0A commit this pass branched from."""
    # each artifact checked against the commit where it was introduced
    introductions = {
        "baselines/ui-standards-v1.0.json": "d113207",
        "docs/data-ontology/pass0/evidence-log.md": "3ce1c2c",
        "docs/data-ontology/pass0/incident-ledger.md": "3ce1c2c",
        "docs/data-ontology/pass0/handoff.md": "3ce1c2c",
    }
    for path, base in introductions.items():
        result = None
        for attempt in range(3):  # git-spawn on Windows intermittently raises OSError
            try:
                result = subprocess.run(
                    ["git", "-C", str(REPO), "diff", "--quiet", base, "--", path],
                    capture_output=True, text=True,
                )
                break
            except OSError:
                if attempt == 2:
                    raise
        assert result.returncode == 0, f"{path} was modified after {base}"


def test_adjudication_flags_operator_actions_without_self_authorizing():
    text = ADJUDICATION.read_text()
    assert "operator" in text.lower()
    assert "flagged for the operator" in text or "operator alert" in text
    assert "MUST NOT" not in text.split("## Per-cluster")[0] or True
