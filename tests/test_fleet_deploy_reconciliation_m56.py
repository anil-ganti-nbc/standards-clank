"""M56 fleet-wide DEPLOY-COM-001 reconciliation guards.

M56 was an independent adversarial reconciliation: it admitted no new
conformance fact, rewrote no admission, changed no historical verdict, and
altered no frozen standard. These guards pin the reconciliation's structural
findings and the honesty properties it was commissioned to protect.

Deliberately NOT pinned: current source-canon SHAs. Those are a volatile
observation at an instant (recorded in the artifact as evidence, explicitly
never as law). Pinning them here would manufacture false test debt the moment
any fleet repo legitimately moves — which is the very drift this audit exists
to describe rather than forbid.
"""

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
RECON_MD = REPO / "audits" / "fleet-deploy-com-001-reconciliation-m56-2026-09-05.md"
RECON_JSON = REPO / "audits" / "fleet-deploy-com-001-reconciliation-m56-2026-09-05.json"
DEPLOY_INDEX = REPO / "standards" / "deployment" / "known-evidence-index.json"
UI_FACTS = REPO / "standards" / "ui" / "evidence-facts.json"

NAMED_TARGETS = {
    "watch-clank", "korean-tech-wire", "tablet-clank", "feature-phone-clank",
    "oem-radar", "smartwatch-clank", "smartphone-clank", "chinese-tech-wire",
    "semiconductor-intelligence",
}

VALID_CLASSIFICATIONS = {
    "CURRENT_CANON_LIVE",
    "HISTORICAL_EXACT_PROOF",
    "CANON_MOVED_PROOF_STILL_VALID_HISTORICALLY",
    "SOURCE_MOVED_REVERIFY_LIVE_RECOMMENDED",
    "IDENTITY_GAP",
    "EVIDENCE_CONFLICT",
}

VALID_RELATIONSHIPS = {
    "EXACT_CURRENT", "BEHIND_CURRENT", "DIVERGENT", "HISTORICAL_ONLY", "UNKNOWN",
}


@pytest.fixture(scope="module")
def recon():
    return json.loads(RECON_JSON.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def deploy_index():
    return json.loads(DEPLOY_INDEX.read_text(encoding="utf-8"))


# -- artifact exists and admits nothing --

def test_reconciliation_artifacts_exist():
    assert RECON_MD.is_file()
    assert RECON_JSON.is_file()
    assert len(RECON_MD.read_text(encoding="utf-8")) > 4000


def test_reconciliation_admits_no_new_fact(recon):
    """The whole point: a reconciliation records, it does not admit."""
    assert recon["admits_new_facts"] is False
    assert recon["rewrites_admissions"] is False
    assert recon["alters_frozen_standards"] is False


def test_reconciliation_findings_block_is_empty():
    """The audits/*.md structured block must parse under the fleet-wide
    convention (all three agent-layer builders scan it) and must contribute
    zero facts to every index."""
    import re

    text = RECON_MD.read_text(encoding="utf-8")
    match = re.search(r"```json\s*\n(.*?)\n```", text, re.DOTALL)
    assert match, "reconciliation audit must carry a leading ```json findings block"
    block = json.loads(match.group(1))
    for key in ("clank", "date", "findings"):
        assert key in block, f"findings block missing required key {key!r}"
    assert block["findings"] == [], "a reconciliation must contribute no findings"


# -- exactly 9 named COM-001 closure subjects, 16 facts preserved --

def test_exactly_nine_com_001_closure_subjects(deploy_index):
    subjects = [e["subject"] for e in deploy_index if e["standard"] == "STD-DEPLOY-COM-001"]
    assert set(subjects) == NAMED_TARGETS
    assert len(subjects) == 9


def test_no_duplicate_com_001_target(deploy_index):
    subjects = [e["subject"] for e in deploy_index if e["standard"] == "STD-DEPLOY-COM-001"]
    assert len(subjects) == len(set(subjects)), f"duplicate COM-001 subject: {subjects}"


def test_all_sixteen_deployment_facts_preserved(deploy_index):
    assert len(deploy_index) == 16
    com1 = [e for e in deploy_index if e["standard"] == "STD-DEPLOY-COM-001"]
    com2 = [e for e in deploy_index if e["standard"] == "STD-DEPLOY-COM-002"]
    assert len(com1) == 9
    assert len(com2) == 7
    assert len(com1) + len(com2) == 16, "16 facts must be exactly the COM-001 + COM-002 split"


def test_reconciliation_records_the_sixteen_fact_accounting(recon):
    acc = recon["deployment_fact_accounting"]
    assert acc["total_facts"] == 16
    assert acc["com_001_facts"] == 9
    assert acc["com_002_facts"] == 7
    for zero_field in ("duplicates", "conflicting_closures", "shadow_facts",
                       "rescoped_facts", "missing_target_identity"):
        assert acc[zero_field] == 0


def test_com_002_coverage_gaps_recorded(recon):
    """The two COM-002 asymmetries must be recorded, not silently smoothed."""
    gaps = {g["subject"] for g in recon["deployment_fact_accounting"]["com_002_coverage_gaps"]}
    assert gaps == {"watch-clank", "smartphone-clank"}


# -- current-vs-historical matrix completeness --

def test_matrix_covers_every_named_target(recon):
    targets = {t["target"] for t in recon["targets"]}
    assert targets == NAMED_TARGETS
    assert len(recon["targets"]) == 9


def test_every_matrix_row_is_complete(recon):
    required = {
        "target", "admitted_proof_sha", "current_canon_sha_observed", "relationship",
        "exact_target", "target_authority_role", "proof_categories", "classification",
        "closure_fact_valid", "fresh_proof_recommended", "identity_strength",
    }
    for row in recon["targets"]:
        missing = required - row.keys()
        assert not missing, f"{row['target']}: matrix row missing {missing}"
        assert row["relationship"] in VALID_RELATIONSHIPS
        assert row["classification"] in VALID_CLASSIFICATIONS


def test_no_matrix_row_is_identity_gap_or_evidence_conflict(recon):
    bad = [r["target"] for r in recon["targets"]
           if r["classification"] in {"IDENTITY_GAP", "EVIDENCE_CONFLICT"}]
    assert bad == [], f"unresolved matrix rows: {bad}"


def test_no_identity_strength_is_insufficient(recon):
    bad = [r["target"] for r in recon["targets"] if r["identity_strength"] == "INSUFFICIENT"]
    assert bad == [], f"insufficient identity: {bad}"


# -- invalidation analysis: canon movement is not fact invalidation --

def test_no_admitted_fact_invalidated(recon):
    inv = recon["invalidation_analysis"]
    assert inv["admitted_deployment_fact_invalidated"] == 0
    assert all(r["closure_fact_valid"] is True for r in recon["targets"])


def test_source_canon_moved_is_distinguished_from_invalidation(recon):
    """SOURCE_CANON_MOVED and ADMITTED_DEPLOYMENT_FACT_INVALIDATED are not the
    same thing and the artifact must not collapse them."""
    inv = recon["invalidation_analysis"]
    assert inv["source_canon_moved"] > 0
    assert inv["admitted_deployment_fact_invalidated"] == 0
    obs = recon["current_canon_observation"]
    assert obs["exact_current"] + obs["behind_current"] + obs["divergent"] \
        + obs["historical_only"] + obs["unknown"] == 9


def test_current_canon_shas_are_marked_volatile(recon):
    """Guard against a future pass promoting the observation into law."""
    notice = recon["current_canon_observation"]["volatility_notice"]
    assert "NEVER normative law" in notice or "never normative law" in notice.lower()


def test_verdict_is_one_of_the_four_permitted_values(recon):
    assert recon["fleet_verdict"] in {
        "FLEET_DEPLOY_COM_001_RECONCILED_9_OF_9",
        "FLEET_DEPLOY_COM_001_CLOSED_HISTORICALLY_BUT_CURRENT_DRIFT_EXISTS",
        "FLEET_DEPLOY_COM_001_EVIDENCE_CONFLICT",
        "FLEET_DEPLOY_COM_001_NOT_CLOSED",
    }


def test_verdict_is_consistent_with_the_matrix(recon):
    """If any target's canon moved past its proof and no fresh live proof was
    taken at the new canon, the verdict may not claim plain 9/9 reconciliation."""
    moved = [r for r in recon["targets"] if r["relationship"] != "EXACT_CURRENT"]
    if moved:
        assert recon["fleet_verdict"] != "FLEET_DEPLOY_COM_001_RECONCILED_9_OF_9", (
            "canon drift exists; the verdict must not claim full current reconciliation"
        )


# -- honesty properties this audit was commissioned to protect --

def test_smartphone_procedural_deviation_preserved(recon):
    row = next(r for r in recon["targets"] if r["target"] == "smartphone-clank")
    dev = row["procedural_deviation"]
    assert "LIVE" in dev.upper()
    assert "scratch" in dev.lower()
    assert "NOT a scratch-first success" in dev
    md = RECON_MD.read_text(encoding="utf-8")
    assert "unintended mutation path" in md


def test_ctw_authority_history_preserved(recon):
    row = next(r for r in recon["targets"] if r["target"] == "chinese-tech-wire")
    role = row["target_authority_role"]
    assert "NAS" in role and "sole authority" in role
    assert "Hetzner" in role and "rollback" in role


def test_semiconductor_test_debt_classification_preserved(recon):
    debt = recon["semiconductor_test_debt_sanity"]
    assert debt["standards_claims_suite_green"] is False
    assert debt["retained_classification"] == "CURRENT_FAILURE_REPRODUCED_DEPLOYMENT_IRRELEVANT"
    assert debt["substantive_property_intact"] is True
    assert debt["laundering_detected"] is False


def test_semiconductor_source_revision_unknown_limitation_preserved(recon):
    row = next(r for r in recon["targets"] if r["target"] == "semiconductor-intelligence")
    assert "source_revision='unknown'" in row["recorded_limitation"]


def test_evidence_debt_register_present_and_complete(recon):
    reg = recon["historical_evidence_debt_register"]
    assert len(reg) >= 10
    ids = {d["id"] for d in reg}
    assert {"D1", "D2", "D3", "D4", "D5"} <= ids
    assert all(d["resolved"] is False for d in reg), "M56 must not resolve debts by inference"
    subjects = {d["subject"] for d in reg}
    assert {"chinese-tech-wire", "smartphone-clank", "semiconductor-intelligence"} <= subjects


# -- CUD-001 integrity: 6 CONFORMS, untouched by the deployment admissions --

def test_all_six_cud_facts_remain_conforms():
    facts = json.loads(UI_FACTS.read_text(encoding="utf-8"))
    cud = [f for f in facts if f.get("standard_id") == "STD-CUD-001"]
    assert len(cud) == 6
    assert all(f["verdict"] == "CONFORMS" for f in cud)
    assert all(f["role"] == "CURRENT" for f in cud)
    assert all(f["provenance"]["kind"] == "source_verification" for f in cud), (
        "CUD facts are source-level evidence and must not be re-typed as live proof"
    )


def test_cud_cross_domain_finding_recorded(recon):
    cud = recon["cud_001_cross_domain"]
    assert cud["fact_count"] == 6
    assert cud["all_verdicts_conforms"] is True
    assert cud["provenance_kind"] == "source_verification"
    assert cud["not_an_evidence_conflict"] is True
    assert "NOT proven materially running" in cud["finding"]


# -- frozen integrity recorded --

def test_frozen_integrity_recorded(recon):
    fi = recon["frozen_integrity"]
    assert fi["tags_verified"] == 5
    assert fi["normative_files_byte_identical"] is True
    assert set(fi["tag_dereferences"]) == {
        "ui-standards-v1.0", "deployment-standards-v1.0", "operations-standards-v1.0",
        "data-ontology-standards-v1.0", "collector-ui-design-standards-v1.0",
    }


@pytest.mark.parametrize("tag,expected", [
    ("ui-standards-v1.0", "d11320704aed69a3d8f854c9264b184e392ec80f"),
    ("deployment-standards-v1.0", "33cc38849180716fd4d06b1356cf70c49d3d41d2"),
    ("operations-standards-v1.0", "7100f294a83c30594f2ff9e953f7c9f77a95747f"),
    ("data-ontology-standards-v1.0", "464a8057ea5dc26ef83248a20bafa0be5aa31148"),
    ("collector-ui-design-standards-v1.0", "f81f4ffa91e9a7af2f80195339d2762180a3154e"),
])
def test_all_five_frozen_tags_unmoved(tag, expected):
    import subprocess

    out = subprocess.run(
        ["git", "-C", str(REPO), "rev-parse", f"{tag}^{{commit}}"],
        capture_output=True, text=True, encoding="utf-8",
        stdin=subprocess.DEVNULL, check=True,
    ).stdout.strip()
    assert out == expected, f"{tag} moved: {out}"
    assert recon_tag_matches(tag, expected)


def recon_tag_matches(tag: str, expected: str) -> bool:
    data = json.loads(RECON_JSON.read_text(encoding="utf-8"))
    return data["frozen_integrity"]["tag_dereferences"][tag] == expected


def test_all_frozen_normative_standard_files_unchanged():
    """Every STD-*.json in every frozen domain must be byte-identical to its
    tag. Additive evidence-layer files alongside them are expected and fine."""
    import subprocess

    tags = {
        "ui": "ui-standards-v1.0",
        "data-ontology": "data-ontology-standards-v1.0",
        "operations": "operations-standards-v1.0",
        "deployment": "deployment-standards-v1.0",
        "collector-ui-design": "collector-ui-design-standards-v1.0",
    }

    def git(*args):
        return subprocess.run(
            ["git", "-C", str(REPO), *args], capture_output=True, text=True,
            encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
        ).stdout.strip()

    checked = 0
    for domain, tag in tags.items():
        listing = git("ls-tree", "-r", "--name-only", tag, "--", f"standards/{domain}")
        for path in listing.splitlines():
            name = path.rsplit("/", 1)[-1]
            if not (name.startswith("STD-") and name.endswith(".json")):
                continue
            assert git("rev-parse", f"{tag}:{path}") == git("rev-parse", f"HEAD:{path}"), (
                f"frozen normative file changed: {path}"
            )
            checked += 1
    assert checked == 26, f"expected 26 frozen normative standard files, checked {checked}"


# -- domain closure answers must be internally consistent --

def test_domain_closure_answers_recorded_and_consistent(recon):
    a = recon["domain_closure_answers"]
    assert a["A_all_nine_supported_by_valid_closures"] is True
    assert a["C_frozen_standards_intact"] is True
    assert a["D_any_admitted_fact_invalidated"] is False
    # E and F must be answerable differently: the programme can be closed
    # under the evidence model while not every latest canon is live.
    assert a["E_every_latest_canon_currently_live"] is False
    assert a["F_programme_closed_under_evidence_model"] is True
    assert a["G_fresh_revalidation_recommended"] is True


def test_revalidation_recommendations_partition_the_fleet(recon):
    rec = recon["revalidation_recommendations"]
    allocated = rec["high"] + rec["optional"] + rec["not_needed"]
    assert set(allocated) == NAMED_TARGETS
    assert len(allocated) == 9, "every named target must appear exactly once"


def test_no_host_or_source_actions_taken(recon):
    actions = " ".join(recon["actions_not_taken"]).lower()
    for forbidden in ("no deployment", "no host access", "no service restart",
                      "no database migration", "no source-clank modification",
                      "no frozen-standard alteration", "no re-ratification"):
        assert forbidden in actions
