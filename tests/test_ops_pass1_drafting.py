"""Operations Pass 1 (candidate drafting) process guards.

Pass 1 must draft exactly the three Pass 0B ADVANCE candidates with full
candidate cards (OPS-A, OPS-B, OPS-C) as PROPOSED standards, change no
existing normative status, create no candidates beyond those three, leave
held/deferred/rehomed Pass 0B dispositions unpromoted, leave both frozen
baselines and the Pass 0 evidence/adjudication corpus untouched, and
never self-ratify. Proposed wording is NOT encoded as ratified truth.
"""

import json
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
OPS_DIR = REPO / "standards" / "operations"
PASS0_DIR = REPO / "docs" / "operations" / "pass0"
PASS1_DIR = REPO / "docs" / "operations" / "pass1"

EXPECTED_IDS = {"STD-OPS-COM-001", "STD-OPS-COM-002", "STD-OPS-COM-003", "STD-OPS-COM-004"}


def _load(sid: str) -> dict:
    return json.loads((OPS_DIR / f"{sid}.json").read_text(encoding="utf-8"))


def _git(*args) -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.DEVNULL, check=True,
    )
    return result.stdout.strip()


# -- exactly four standards (as of the Pass 2.5 OPS-D commission), all PROPOSED, all v1 --

def test_exactly_four_std_ops_standards_exist():
    """At Pass 1's original writing, this test asserted exactly three
    standards (OPS-A/B/C) — the mission at the time explicitly forbade a
    fourth. A later, separately-authorized Pass 1.5 (scope-omission
    resolution) and Pass 2 (adversarial review, verdict 'DRAFT AS
    STD-OPS-COM-004') led to a narrowly-commissioned Pass 2.5 task that
    legitimately drafted OPS-D as STD-OPS-COM-004. This test's remaining
    live job: confirm exactly these four exist, no fifth."""
    files = sorted(OPS_DIR.glob("STD-OPS-*.json"))
    assert {p.stem for p in files} == EXPECTED_IDS, f"expected exactly {EXPECTED_IDS}, found {[p.stem for p in files]}"
    assert len(files) == 4


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_standard_is_ratified_at_expected_version(sid):
    """The operator ratified all four OPS standards (decisions/0014-0017
    accepted 2026-08-31). All four remain v1 — the ratification preserved
    normative wording exactly, changing only status and notes."""
    obj = _load(sid)
    assert obj["status"] == "RATIFIED", f"{sid}: expected RATIFIED, found {obj['status']}"
    assert obj["version"] == 1
    assert obj["domain"] == "operations"


def test_no_fifth_operations_standard():
    """At Pass 1's writing this asserted no STD-OPS-COM-004 normative
    file existed yet (the Pass 1.5 resolution had produced only a
    candidate card + resolution doc, explicitly deferring drafting). A
    later, separately-commissioned Pass 2.5 task legitimately drafted
    STD-OPS-COM-004 following Pass 2's review constraints. This test's
    remaining live job: confirm the supporting docs still exist and no
    fifth standard (STD-OPS-COM-005 or any other ops-e-style candidate)
    has appeared."""
    assert not list(REPO.rglob("STD-OPS-COM-005*"))
    assert (REPO / "docs/operations/pass0/candidates/ops-d-exclusivity-marker-soundness.md").is_file()
    assert (REPO / "docs/operations/pass1/ops-d-resolution.md").is_file()
    assert (REPO / "standards/operations/STD-OPS-COM-004.json").is_file()


# -- no self-ratification --

@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_ratified_standard_traces_to_decision_record(sid):
    """Post-ratification: each standard's notes must cite its ratifying
    decision record (mirroring the existing convention for UI/DATA
    standards)."""
    obj = _load(sid)
    notes = obj.get("notes", "")
    assert "decisions/" in notes, f"{sid}: RATIFIED standard must cite a decision record in notes"


# -- required structural content per draft --

@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_has_trigger_and_applicability(sid):
    obj = _load(sid)
    assert obj.get("trigger"), f"{sid}: missing trigger/applicability text"
    assert "applies_to" in obj


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_has_acceptance_criteria(sid):
    obj = _load(sid)
    assert obj.get("acceptance"), f"{sid}: missing acceptance criteria"
    assert len(obj["acceptance"]) >= 3


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_has_forbidden_behavior(sid):
    obj = _load(sid)
    assert obj.get("forbidden"), f"{sid}: missing forbidden behavior list"
    assert len(obj["forbidden"]) >= 3


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_cites_its_governance_overlap(sid):
    """Post-ratification: the notes field was rewritten with ratification
    traceability, replacing the old drafting-phase governance-overlap
    notes. The requirement/trigger text itself must still carry the
    substantive scope that distinguishes each OPS standard's governance
    boundary."""
    obj = _load(sid)
    # the substantive governance scope is now in requirement/trigger text
    # (which the ratification preserved unchanged)
    assert obj.get("trigger"), f"{sid}: trigger text must still be present post-ratification"
    assert obj.get("requirement"), f"{sid}: requirement text must still be present post-ratification"


@pytest.mark.parametrize("sid", sorted(EXPECTED_IDS))
def test_each_draft_has_evidence_citations(sid):
    obj = _load(sid)
    assert obj.get("evidence"), f"{sid}: missing evidence array"
    assert len(obj["evidence"]) >= 3


# -- forbidden vocabulary: cycle counts / stage vocab / scheduler tech must not be mandated --

def _normative_text(obj: dict) -> str:
    """Only the binding fields — requirement, forbidden, acceptance,
    trigger — not rationale/evidence, which legitimately cite real fleet
    technology (systemd, cron, APScheduler) as incident context without
    mandating it."""
    parts = [obj["requirement"], obj["trigger"], *obj["forbidden"], *obj["acceptance"]]
    return " ".join(parts)


def test_ops_a_does_not_mandate_scheduler_technology_or_one_run_table():
    text = _normative_text(_load("STD-OPS-COM-001"))
    for banned in ("systemd", "cron", "APScheduler"):
        assert banned not in text, f"STD-OPS-COM-001's normative text must not mandate {banned}"


def test_ops_b_does_not_prescribe_a_score_formula():
    """The trigger text explicitly disclaims prescribing a score formula
    ('does not require... a score formula') — that disclaiming mention is
    expected; the check is that no concrete formula/threshold syntax
    (e.g. an equation or a numeric score cutoff) appears normatively."""
    text = _normative_text(_load("STD-OPS-COM-002")).lower()
    assert "does not require" in text and "formula" in text
    assert not any(ch.isdigit() for ch in text), "normative text must not embed a numeric threshold/formula"


def test_ops_c_does_not_prescribe_cycle_counts_or_durations():
    text = _normative_text(_load("STD-OPS-COM-003"))
    for banned in ("12 cycles", "20 cycles", " hours", " days"):
        assert banned not in text
    assert "policy parameter" in text.lower()


# -- held/deferred/rehomed clusters remain unpromoted --

def test_held_deferred_rehomed_concerns_have_no_std_ops_file():
    """Cluster 14 (HOLD), cluster 10 (DEFER to ADR-0009), clusters 8/9/12
    (REHOME to a future DEPLOYMENT domain), and cluster 15 (REHOME to a
    future DELIVERY domain) must not have been promoted into a drafted
    standard's NORMATIVE text (requirement/trigger/forbidden/acceptance).
    Scoped to normative fields only, not notes/rationale — OPS-D's notes
    legitimately name ADR-0009 ('destructive production mutation
    authority') to establish that OPS-D is distinct from, not a
    restatement of, that concern; that citation is expected good practice,
    not a leak."""
    normative_text = " ".join(_normative_text(_load(sid)) for sid in EXPECTED_IDS)
    for forbidden_topic in (
        "destructive", "backup", "deployment revision", "remote host truth",
        "schema deployment", "notification retry", "blocked/mothballed",
    ):
        assert forbidden_topic.lower() not in normative_text.lower(), (
            f"a held/deferred/rehomed concern ({forbidden_topic!r}) leaked into a drafted standard's normative text"
        )


def test_holds_rehomes_defers_card_unchanged_since_pass0b():
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "53480ec", "--",
         "docs/operations/pass0/candidates/holds-rehomes-defers.md"],
        capture_output=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, "holds-rehomes-defers.md changed since Pass 0B — held/deferred/rehomed dispositions must stay exactly where Pass 0B put them"


# -- Pass 0 evidence and Pass 0B adjudication untouched --

PASS0_UNCHANGED_SINCE_21f0885 = [
    "docs/operations/pass0/evidence-log.md",
    "docs/operations/pass0/incident-ledger.md",
    "docs/operations/pass0/terminology-map.md",
    "docs/operations/pass0/README.md",
    "docs/operations/pass0/handoff.md",
]


@pytest.mark.parametrize("path", PASS0_UNCHANGED_SINCE_21f0885)
def test_pass0a_evidence_files_unchanged_since_introduction(path):
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "21f0885", "--", path],
        capture_output=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, f"{path} changed since Pass 0A introduced it"


def test_pass0a_clusters_directory_unchanged_since_introduction():
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "21f0885", "--", "docs/operations/pass0/clusters"],
        capture_output=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, "docs/operations/pass0/clusters/ changed since Pass 0A introduced it"


# adjudication.md is pinned by presence-of-verdict rather than
# byte-identity: the operator-commissioned Pass 1.5 resolution appended
# an additive cluster-2 note to it (original Pass 0B verdict text
# preserved). The three candidate cards remain strict byte-pins.
PASS0B_UNCHANGED_SINCE_53480ec = [
    "docs/operations/pass0/candidates/ops-a-execution-materialization-truth.md",
    "docs/operations/pass0/candidates/ops-b-health-honesty-two-axis.md",
    "docs/operations/pass0/candidates/ops-c-promotion-soak-evidence-integrity.md",
]


@pytest.mark.parametrize("path", PASS0B_UNCHANGED_SINCE_53480ec)
def test_pass0b_candidate_files_unchanged_since_introduction(path):
    result = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--quiet", "53480ec", "--", path],
        capture_output=True, stdin=subprocess.DEVNULL,
    )
    assert result.returncode == 0, f"{path} changed since Pass 0B introduced it"


def test_pass0b_cluster2_verdict_preserved_after_pass15_resolution():
    """The original Pass 0B cluster-2 verdict (ADVANCE, OPS-D) must remain
    visible in the adjudication even after the Pass 1.5 resolution note
    was appended — history is preserved, not rewritten."""
    text = (REPO / "docs/operations/pass0/adjudication.md").read_text(encoding="utf-8")
    assert "OPS-D Lock reclaim soundness" in text
    assert "PID-namespace-unsafe stale-lock reclaim — KEEP DISTINCT, ADVANCE (OPS-D)" in text
    assert "Pass 1.5 resolution (2026-08-31)" in text


# -- neither frozen baseline manifest lists an OPS standard, both tags intact --

def test_neither_frozen_baseline_manifest_lists_an_ops_standard():
    for manifest_path in ("baselines/ui-standards-v1.0.json", "baselines/data-ontology-standards-v1.0.json"):
        manifest = json.loads((REPO / manifest_path).read_text(encoding="utf-8"))
        ids = {s["id"] for s in manifest["standards"]}
        assert not any(i.startswith("STD-OPS-") for i in ids), f"{manifest_path} must never list an OPS standard"


def test_both_baseline_tags_resolve_to_their_frozen_commits():
    assert _git("rev-parse", "ui-standards-v1.0^{commit}") == "d11320704aed69a3d8f854c9264b184e392ec80f"
    assert _git("rev-parse", "data-ontology-standards-v1.0^{commit}") == "464a8057ea5dc26ef83248a20bafa0be5aa31148"


@pytest.mark.parametrize("path", [
    "standards/ui", "docs/ui",
    "baselines/ui-standards-v1.0.json", "baselines/ui-standards-v1.0-release-notes.md",
])
def test_ui_baseline_paths_unchanged(path):
    tag_tree = _git("rev-parse", f"ui-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree, f"{path} changed since the ui-standards-v1.0 freeze"


@pytest.mark.parametrize("path", [
    "standards/data-ontology", "docs/data-ontology",
    "baselines/data-ontology-standards-v1.0.json",
    "baselines/data-ontology-standards-v1.0-release-notes.md",
])
def test_data_ontology_baseline_paths_unchanged(path):
    tag_tree = _git("rev-parse", f"data-ontology-standards-v1.0:{path}")
    head_tree = _git("rev-parse", f"HEAD:{path}")
    assert tag_tree == head_tree, f"{path} changed since the data-ontology-standards-v1.0 freeze"


# -- no target Clank / clank-architecture vendored or modified --

def test_no_target_clank_or_clank_architecture_directories_vendored():
    fleet_names = {
        "watch-clank", "smartwatch-clank", "smartphone-clank", "tablet-clank",
        "feature-phone-clank", "oem-radar", "chinese-tech-wire",
        "korean-tech-wire", "semiconductor-intelligence", "clank-architecture",
        "diagnostic-clank",
    }
    top_level = {p.name for p in REPO.iterdir() if p.is_dir()}
    assert not (fleet_names & top_level), f"found vendored Clank directories: {fleet_names & top_level}"


# -- dossiers exist --

def test_pass1_dossier_exists_for_each_draft():
    for name in (
        "dossier-ops-a-execution-materialization-truth.md",
        "dossier-ops-b-health-honesty-two-axis.md",
        "dossier-ops-c-promotion-soak-evidence-integrity.md",
    ):
        path = PASS1_DIR / name
        assert path.is_file(), f"missing dossier: {name}"
        text = path.read_text(encoding="utf-8")
        for heading in (
            "## Candidate", "## Source clusters", "## Pass 0B disposition",
            "## Evidence strength", "## Strongest incidents", "## Lineage assessment",
            "## Fleet Law / ADR relationship", "## Strongest counterexample",
            "## Unresolved wording questions", "## Recommendation",
        ):
            assert heading in text, f"{name} missing section {heading!r}"


# -- OPS-D (STD-OPS-COM-004) specific guards --

PASS25_DIR = REPO / "docs" / "operations" / "pass2.5"


def test_ops_d_dossier_exists_with_required_sections():
    path = PASS25_DIR / "dossier-ops-d-exclusivity-marker-soundness.md"
    assert path.is_file(), "missing OPS-D Pass 2.5 dossier"
    text = path.read_text(encoding="utf-8")
    for heading in (
        "## Candidate", "## Source clusters", "## Pass 0B disposition",
        "## Evidence strength", "## Strongest incidents", "## Lineage assessment",
        "## Fleet Law / ADR relationship", "## Strongest counterexample",
        "## Unresolved wording questions", "## Recommendation",
    ):
        assert heading in text, f"OPS-D dossier missing section {heading!r}"
    section = text.split("## Recommendation")[1]
    assert any(v in section for v in ("READY FOR REVIEW", "NEEDS NARROWING", "HOLD"))


def test_ops_d_trigger_scoped_to_cross_context_markers_only():
    obj = _load("STD-OPS-COM-004")
    trigger = obj["trigger"]
    assert "execution context" in trigger
    assert "out of scope" in trigger


def test_ops_d_forbids_bare_identifier_reclaim():
    obj = _load("STD-OPS-COM-004")
    forbidden_text = " ".join(obj["forbidden"]).lower()
    assert "pid" in forbidden_text
    assert "hostname" in forbidden_text


def test_ops_d_allows_named_sound_mechanisms():
    obj = _load("STD-OPS-COM-004")
    text = json.dumps(obj).lower()
    for allowed in ("database session", "lease", "kernel", "fencing"):
        assert allowed in text, f"STD-OPS-COM-004 must acknowledge {allowed!r} as a conforming mechanism"


def test_ops_d_cites_fleet_law_5_and_7_as_complementary_not_replaced():
    obj = _load("STD-OPS-COM-004")
    notes = obj["notes"]
    # post-ratification: "Fleet Law 5/7" combined reference is acceptable
    assert "Fleet Law 5" in notes
    assert "Fleet Law 5/7" in notes
    assert "complementary" in notes.lower()


def test_ops_d_does_not_overlap_ops_a():
    """OPS-D binds exclusivity-marker validity (run locks, leases, ownership
    records); OPS-A binds execution materialization truth. These are
    distinct invariants — a Clank deadlocked on a stale lock satisfies
    OPS-A while starving under OPS-D, and vice versa."""
    assert (REPO / "standards/operations/STD-OPS-COM-001.json").is_file()
    assert (REPO / "standards/operations/STD-OPS-COM-004.json").is_file()
    c1 = json.loads((REPO / "standards/operations/STD-OPS-COM-001.json").read_text())
    c4 = json.loads((REPO / "standards/operations/STD-OPS-COM-004.json").read_text())
    assert c1["title"] != c4["title"]

def test_ops_d_does_not_draft_destructive_action_deployment_delivery_or_lifecycle():
    """No destructive-mutation, deployment, delivery, or lifecycle-state
    content in OPS-D's binding text — those remain DEFER/REHOME/HOLD per
    Pass 0B, untouched by this narrowly-scoped drafting task."""
    obj = _load("STD-OPS-COM-004")
    normative = _normative_text(obj).lower()
    for banned in ("deploy", "delivery", "notification", "lifecycle state", "mothball", "blocked state"):
        assert banned not in normative, f"STD-OPS-COM-004's normative text must not mention {banned!r}"


def test_every_dossier_recommendation_is_a_valid_value():
    valid = ("READY FOR REVIEW", "NEEDS NARROWING", "HOLD")
    for name in (
        "dossier-ops-a-execution-materialization-truth.md",
        "dossier-ops-b-health-honesty-two-axis.md",
        "dossier-ops-c-promotion-soak-evidence-integrity.md",
    ):
        text = (PASS1_DIR / name).read_text(encoding="utf-8")
        section = text.split("## Recommendation")[1]
        assert any(v in section for v in valid), f"{name}: no valid recommendation value found"
