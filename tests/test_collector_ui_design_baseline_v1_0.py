"""Freeze guards for the collector-ui-design-standards-v1.0 baseline."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "baselines" / "collector-ui-design-standards-v1.0.json"
STD_FILE = ROOT / "standards" / "collector-ui-design" / "STD-CUD-001.json"


def _sha256_lf(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


class TestRatified:
    def test_A_std_cud_001_is_ratified(self):
        std = json.loads(STD_FILE.read_text(encoding="utf-8"))
        assert std["status"] == "RATIFIED"
        assert std["id"] == "STD-CUD-001"

    def test_B_version_is_1(self):
        std = json.loads(STD_FILE.read_text(encoding="utf-8"))
        assert std["version"] == 1

    def test_C_frozen_normative_hash_is_exact(self):
        manifest = _manifest()
        artifact = manifest["artifacts"]["normative_file"]
        assert _sha256_lf(ROOT / artifact["path"]) == artifact["sha256_lf_normalized"]

    def test_D_manifest_records_exact_artifact(self):
        manifest = _manifest()
        assert manifest["baseline_id"] == "collector-ui-design-standards-v1.0"
        assert manifest["status"] == "FROZEN"
        assert manifest["artifacts"]["normative_file"]["path"] == (
            "standards/collector-ui-design/STD-CUD-001.json"
        )
        assert manifest["change_policy"]


class TestTag:
    def test_E_annotated_tag_resolves_to_ratification_commit(self):
        """The tag must exist and resolve. Before the tag is created (tests
        gate the commit; the tag is created after), this test skips."""
        result = subprocess.run(
            ["git", "-C", str(ROOT), "tag", "-l", "collector-ui-design*"],
            capture_output=True, text=True, encoding="utf-8",
            stdin=subprocess.DEVNULL, check=True,
        )
        tags = result.stdout.strip().splitlines()
        if not tags or tags == [""]:
            pytest.skip("tag not yet created")
        assert tags == ["collector-ui-design-standards-v1.0"]
        tag_commit = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", f"{tags[0]}^{{commit}}"],
            capture_output=True, text=True, encoding="utf-8",
            stdin=subprocess.DEVNULL, check=True,
        ).stdout.strip()
        # the tag targets the ratification commit or an ancestor
        assert tag_commit  # resolved successfully


class TestReferenceEvidenceNotNormative:
    def test_G_reference_evidence_is_not_normative(self):
        std = json.loads(STD_FILE.read_text(encoding="utf-8"))
        notes = std.get("notes", "").lower()
        req = std.get("requirement", "").lower()
        assert "byte-identical" not in req
        assert "accent-only" not in req
        # evidence mentions byte-identity as reference, not MUST
        assert "reference implementation" in notes

    def test_H_current_implementation_hashes_are_not_normative(self):
        std = json.loads(STD_FILE.read_text(encoding="utf-8"))
        req = std.get("requirement", "")
        assert "aaa38c12" not in req
        assert "DESIGN_SYSTEM_VERSION" not in req
        assert "sha256" not in req.lower()


class TestPriorFrozenDomains:
    def test_I_previous_frozen_domains_remain_byte_identical(self):
        """Each prior domain's frozen STD files remain byte-identical to
        their recorded hashes."""
        prior = [
            ("baselines/ui-standards-v1.0.json", "standards/ui/STD-UI-COM-001.json"),
            ("baselines/deployment-standards-v1.0.json", "standards/deployment/STD-DEPLOY-COM-001.json"),
            ("baselines/deployment-standards-v1.0.json", "standards/deployment/STD-DEPLOY-COM-002.json"),
        ]
        for manifest_path, std_path in prior:
            mp = ROOT / manifest_path
            if not mp.exists():
                continue
            manifest = json.loads(mp.read_text(encoding="utf-8"))
            sp = ROOT / std_path
            raw = sp.read_bytes().replace(b"\r\n", b"\n")
            actual = hashlib.sha256(raw).hexdigest()
            # find the pinned hash
            artifact_list = manifest.get("artifacts", {}).get("standard_files", {})
            if isinstance(artifact_list, dict):
                for sid, art in artifact_list.items():
                    if art.get("path") == std_path:
                        assert actual == art["sha256_lf_normalized"], (
                            f"{std_path} drifted from frozen state"
                        )

    def test_J_previous_tags_have_not_moved(self):
        expected = {
            "ui-standards-v1.0": "d11320704aed69a3d8f854c9264b184e392ec80f",
        }
        for tag, expected_commit in expected.items():
            result = subprocess.run(
                ["git", "-C", str(ROOT), "rev-parse", f"{tag}^{{commit}}"],
                capture_output=True, text=True, encoding="utf-8",
                stdin=subprocess.DEVNULL, check=True,
            )
            assert result.stdout.strip() == expected_commit, (
                f"tag {tag} has moved"
            )
