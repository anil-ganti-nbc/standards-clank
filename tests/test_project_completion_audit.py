"""Guards for the Charter §F project-level residual evidence audit."""

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
AUDIT = REPO / "docs" / "project-completion-audit.md"
TAGS = {
    "ui-standards-v1.0": "d11320704aed69a3d8f854c9264b184e392ec80f",
    "data-ontology-standards-v1.0": "464a8057ea5dc26ef83248a20bafa0be5aa31148",
    "operations-standards-v1.0": "7100f294a83c30594f2ff9e953f7c9f77a95747f",
    "deployment-standards-v1.0": "33cc38849180716fd4d06b1356cf70c49d3d41d2",
}


def text():
    return AUDIT.read_text(encoding="utf-8")


def test_all_baselines_and_immutable_tags_exist():
    for domain in ("ui", "data-ontology", "operations", "deployment"):
        assert (REPO / "baselines" / f"{domain}-standards-v1.0.json").is_file()
    for tag, expected in TAGS.items():
        actual = subprocess.run(["git", "rev-parse", f"{tag}^{{}}"], cwd=REPO, capture_output=True, text=True, check=True, stdin=subprocess.DEVNULL).stdout.strip()
        assert actual == expected


def test_audit_accounts_for_final_domain_residuals_and_delivery_is_explicit():
    body = text()
    for marker in ("Operations lifecycle", "ADR-0009", "Fleet Law 6", "Law 9", "config congruence", "partial wiring", "schema migration mechanics", "Data/Ontology", "UI"):
        assert marker in body
    assert "DELIVERY DOMAIN CREATION HELD" in body
    assert "confirmed Delivery-adjacent incident lineage" in body
    assert "No `STD-DELIVERY-*` is created" in body
    assert not list(REPO.glob("standards/**/STD-DELIVERY-*.json"))


def test_holds_rehomes_empty_domains_and_completion_verdict_are_unambiguous():
    body = text()
    assert "harmful lifecycle ambiguity/mispromotion" in body
    assert "not ACTIVE" in body
    assert "NO EVIDENCED DOMAIN GAP" in body
    assert body.count("**STANDARDS CLANK COMPLETE**") == 1
    assert "**STANDARDS CLANK COMPLETE UNDER CHARTER §F**" in body
    assert "**NO UNRESOLVED MATERIALLY EVIDENCED NORMATIVE CONCERN**" in body


def test_audit_does_not_vendor_or_modify_target_or_architecture_repositories():
    assert not (REPO / "clank-architecture").exists()
    assert not ({"watch-clank", "oem-radar", "smartphone-clank", "diagnostic-clank"} & {path.name for path in REPO.iterdir() if path.is_dir()})
