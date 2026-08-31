"""Operations Pass 0B (adversarial adjudication) process guards.

The adjudication must cover all 15 clusters with exactly one disposition
and one recommendation each, give every ADVANCE candidate a counterexample
test, classify every Fleet-Law-overlapping cluster's authority model, keep
non-Operations rehomes explicit, create no STD-OPS normative files, and
leave the frozen baselines and Pass 0A evidence untouched.
"""

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ADJUDICATION = REPO / "docs" / "operations" / "pass0" / "adjudication.md"
CANDIDATES = REPO / "docs" / "operations" / "pass0" / "candidates"

DISPOSITIONS = ("KEEP DISTINCT", "MERGE", "SPLIT", "REHOME", "REJECT", "HOLD")
RECOMMENDATIONS = ("ADVANCE", "HOLD", "REHOME", "DEFER", "REJECT")
ADVANCE_CARDS = {
    "ops-a-execution-materialization-truth.md",
    "ops-b-health-honesty-two-axis.md",
    "ops-c-promotion-soak-evidence-integrity.md",
}


def _adjudication() -> str:
    return ADJUDICATION.read_text()


def test_adjudication_exists():
    assert ADJUDICATION.is_file()
    assert len(_adjudication()) > 4000


def test_all_15_clusters_appear_in_the_disposition_table():
    text = _adjudication()
    rows = [
        line for line in text.splitlines()
        if re.match(r"^\| \d+ \|", line)
    ]
    assert len(rows) == 15, f"expected 15 cluster rows, found {len(rows)}"
    numbers = [int(row.split("|")[1].strip()) for row in rows]
    assert numbers == list(range(1, 16))


def test_every_cluster_row_has_exactly_one_disposition_and_one_recommendation():
    text = _adjudication()
    for line in text.splitlines():
        if not re.match(r"^\| \d+ \|", line):
            continue
        cells = line.split("|")
        disposition_cell = cells[4] if len(cells) > 4 else ""
        recommendation_cell = cells[6] if len(cells) > 6 else ""
        dispositions = [d for d in DISPOSITIONS if d in disposition_cell]
        recommendations = [r for r in RECOMMENDATIONS if r in recommendation_cell]
        assert len(dispositions) == 1, f"dispositions {dispositions} in {line!r}"
        assert len(recommendations) == 1, f"recommendations {recommendations} in {line!r}"


def test_every_high_cluster_is_adjudicated_in_prose():
    text = _adjudication()
    covered = set()
    for m in re.finditer(r"^### ([0-9+]+)\.", text, flags=re.MULTILINE):
        for part in m.group(1).split("+"):
            covered.add(int(part))
    assert {1, 2, 3, 4, 5, 6, 7, 13} <= covered, (
        f"ADVANCE-candidate clusters missing prose sections: {({1, 2, 3, 4, 5, 6, 7, 13}) - covered}"
    )


def test_all_three_advance_cards_exist_with_counterexamples():
    for name in ADVANCE_CARDS:
        text = (CANDIDATES / name).read_text()
        assert "**Recommendation: ADVANCE" in text, name
        assert text.count("**Recommendation:") == 1, name
        assert "Counterexample test" in text or "Strongest plausible counterexample" in text, name
        assert "Why it survives" in text or "Survives" in text, name


def test_fleet_law_authority_models_classified():
    text = _adjudication()
    table = text.split("Fleet-Law / ADR reconciliation table")[1].split("## ")[0]
    required_rows = (
        "ADR-0008", "Fleet Law 3", "Fleet Law 8", "Fleet Law 5",
        "ADR-0006", "ADR-0009", "Fleet Law 9",
    )
    for row_key in required_rows:
        assert row_key in table, f"reconciliation table missing {row_key}"
    for model in ("complement", "defer", "rehome"):
        assert model in table.lower(), f"authority model {model!r} missing"


def test_destructive_action_defers_to_adr0009_and_flags_agent_class():
    text = _adjudication()
    assert "DEFER to ADR-0009" in text
    assert "agent" in text.lower()
    assert "PROPOSED — REVIEWED DRAFT" in text or "PROPOSED" in text


def test_no_std_ops_normative_files_exist():
    std_ops = list(REPO.rglob("STD-OPS-*"))
    assert not std_ops, f"Pass 0B must not create normative files: {std_ops}"


def test_non_operations_rehomes_are_explicit():
    text = _adjudication()
    assert "future DEPLOYMENT domain" in text
    assert "future DELIVERY domain" in text


def test_promotion_candidate_avoids_cycle_count_prescription():
    card = (CANDIDATES / "ops-c-promotion-soak-evidence-integrity.md").read_text()
    assert "not standardized" in card or "explicitly not standardized" in card or "policy parameters" in card
