#!/usr/bin/env python3
"""Regenerate standards/operations/ratified-index.json and
standards/operations/agent-checklist.json from the authoritative
standards/operations/*.json files. Run this after any RATIFIED standard
changes, and after updating tools/operations_agent_layer.py's
SUMMARIES/CHECKLIST_ITEMS for a new or reworded RATIFIED standard.

Usage: python scripts/generate_operations_agent_layer.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.operations_agent_layer import (
    STANDARDS_OPERATIONS_DIR,
    build_agent_checklist,
    build_ratified_index,
)


def main() -> None:
    index_path = STANDARDS_OPERATIONS_DIR / "ratified-index.json"
    checklist_path = STANDARDS_OPERATIONS_DIR / "agent-checklist.json"

    index_path.write_text(json.dumps(build_ratified_index(), indent=2) + "\n", encoding="utf-8")
    checklist_path.write_text(json.dumps(build_agent_checklist(), indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {index_path}")
    print(f"Wrote {checklist_path}")


if __name__ == "__main__":
    main()
