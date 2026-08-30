#!/usr/bin/env python3
"""Regenerate standards/ui/ratified-index.json and standards/ui/agent-checklist.json
from the authoritative standards/ui/*.json files. Run this after any RATIFIED
standard changes, and after updating tools/ui_agent_layer.py's SUMMARIES/
CHECKLIST_ITEMS for a new or reworded RATIFIED standard.

Usage: python scripts/generate_ui_agent_layer.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.ui_agent_layer import (
    STANDARDS_UI_DIR,
    build_agent_checklist,
    build_known_evidence_index,
    build_ratified_index,
)


def main() -> None:
    index_path = STANDARDS_UI_DIR / "ratified-index.json"
    checklist_path = STANDARDS_UI_DIR / "agent-checklist.json"
    evidence_path = STANDARDS_UI_DIR / "known-evidence-index.json"

    index_path.write_text(json.dumps(build_ratified_index(), indent=2) + "\n")
    checklist_path.write_text(json.dumps(build_agent_checklist(), indent=2) + "\n")
    evidence_path.write_text(json.dumps(build_known_evidence_index(), indent=2) + "\n")

    print(f"Wrote {index_path}")
    print(f"Wrote {checklist_path}")
    print(f"Wrote {evidence_path}")


if __name__ == "__main__":
    main()
