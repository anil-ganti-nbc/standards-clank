from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.fleet_standards_resolver import audit_plan, resolve
p=argparse.ArgumentParser(description="Resolve frozen Standards Clank applicability (no conformance verdicts).")
p.add_argument("clank_id"); p.add_argument("--json", action="store_true"); p.add_argument("--audit-plan", action="store_true")
a=p.parse_args(); result=audit_plan(a.clank_id) if a.audit_plan else resolve(a.clank_id)
if a.json or a.audit_plan: print(json.dumps(result, indent=2, sort_keys=True))
else:
 print(f"{result['clank_id']} ({result['profile']})")
 for s in result['standards']: print(f"{s['applicability']:14} {s['id']} — {s['reason']}")
