#!/usr/bin/env python3
"""Regenerate standards/deployment/ratified-index.json and
standards/deployment/agent-checklist.json from the authoritative
standards/deployment/*.json files. Run this after any RATIFIED standard
changes, and after updating tools/deployment_agent_layer.py's
SUMMARIES/CHECKLIST_ITEMS for a new or reworded RATIFIED standard.

Usage: python scripts/generate_deployment_agent_layer.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.deployment_agent_layer import (
    STANDARDS_DEPLOYMENT_DIR,
    build_agent_checklist,
    build_ratified_index,
)


def main() -> None:
    index_path = STANDARDS_DEPLOYMENT_DIR / "ratified-index.json"
    checklist_path = STANDARDS_DEPLOYMENT_DIR / "agent-checklist.json"

    index_path.write_text(json.dumps(build_ratified_index(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    checklist_path.write_text(json.dumps(build_agent_checklist(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Wrote {index_path}")
    print(f"Wrote {checklist_path}")


if __name__ == "__main__":
    main()
