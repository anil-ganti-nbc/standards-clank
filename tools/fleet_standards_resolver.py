"""Resolve frozen Standards Clank applicability; never audit a target runtime."""
from __future__ import annotations
import json, subprocess, tarfile
from functools import lru_cache
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).parent.parent
REGISTRY = ROOT / "profiles" / "fleet-adoption.json"
DOMAINS = {"ui": "ui-standards-v1.0", "data-ontology": "data-ontology-standards-v1.0", "operations": "operations-standards-v1.0", "deployment": "deployment-standards-v1.0"}
FACTS = {
 "STD-UI-COM-001":"has_gui", "STD-UI-COM-002":"has_operator_qc", "STD-UI-COM-003":"has_qc_queue", "STD-UI-COM-004":"has_qc_queue", "STD-UI-COM-005":"has_maturity_tier", "STD-UI-COM-006":"has_bulk_collector_control", "STD-UI-COM-007":"has_manual_collector_controls", "STD-UI-COM-008":"has_source_health_surface", "STD-UI-COM-009":"has_per_run_phase_data", "STD-UI-COM-010":"displays_ambiguous_timestamps", "STD-UI-COM-011":"has_delivery_outcomes", "STD-UI-COM-012":"has_primary_operator_surface",
 "STD-DATA-COM-001":"local_history_novelty", "STD-DATA-COM-002":"has_novelty_consumer", "STD-DATA-COM-003":"canonical_entity_merge", "STD-DATA-COM-004":"derives_canonical_state",
 "STD-OPS-COM-001":"has_collection_trigger", "STD-OPS-COM-002":"has_source_output", "STD-OPS-COM-003":"has_promotion_soak", "STD-OPS-COM-004":"has_ownership_marker",
 "STD-DEPLOY-COM-001":"meaningful_deployment_transition", "STD-DEPLOY-COM-002":"persistent_structured_state"}

def _show(tag, path):
    return subprocess.run(["git", "show", f"{tag}:{path}"], cwd=ROOT, text=True, capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout
def _json(tag, path): return json.loads(_show(tag, path))
def _tag_tree(tag, directory):
    archive = subprocess.run(["git", "archive", "--format=tar", tag, directory], cwd=ROOT, capture_output=True, check=True, stdin=subprocess.DEVNULL).stdout
    with tarfile.open(fileobj=BytesIO(archive)) as tar:
        return {m.name: json.loads(tar.extractfile(m).read()) for m in tar.getmembers() if m.isfile() and m.name.endswith(".json")}
def _domain_path(domain): return f"baselines/{DOMAINS[domain]}.json"
def load_registry(): return json.loads(REGISTRY.read_text(encoding="utf-8"))
@lru_cache(maxsize=1)
def frozen_standards():
    rows=[]
    for domain, tag in DOMAINS.items():
        manifest=_json(tag, _domain_path(domain))
        tree=_tag_tree(tag, f"standards/{domain}")
        # Some early tags predate generated checklist files. Normative payload
        # always comes from the tag; the repository's checked-in generated
        # agent layer supplies the question wording for those historical tags.
        checklist_path=f"standards/{domain}/agent-checklist.json"
        try: checklist_data=tree[checklist_path]
        except KeyError: checklist_data=json.loads((ROOT / checklist_path).read_text(encoding="utf-8"))
        checklist={x["standard"]:x for x in checklist_data}
        for entry in manifest["standards"]:
            if entry["status"] != "RATIFIED": continue
            source_file=f"standards/{domain}/{entry['id']}.json"
            payload=tree[source_file]
            summary={"id": entry["id"], "version": entry["version"], "source_file": source_file, "requirement_summary": payload["requirement"]}
            rows.append({"domain":domain,"baseline":tag,"standard":payload,"summary":summary,"checklist":checklist[entry["id"]]})
    return rows
def resolve(clank_id):
    registry=load_registry(); clank=next((x for x in registry["clanks"] if x["id"]==clank_id), None)
    if not clank: raise KeyError(f"unknown registered Clank: {clank_id}")
    profiles=[clank["primary_profile"], *clank.get("secondary_profiles", [])]
    out=[]
    for row in frozen_standards():
        standard=row["standard"]; sid=standard["id"]; scope=standard.get("applies_to", [])
        if scope and not set(scope).intersection(profiles):
            disposition, reason = "NOT_APPLICABLE", f"profile(s) {profiles} do not match family scope {scope}"
        else:
            fact=FACTS.get(sid); value=clank.get("facts", {}).get(fact, "UNKNOWN") if fact else "TRUE"
            if value == "TRUE": disposition, reason = "APPLIES", f"trigger fact {fact} is recorded TRUE"
            elif value == "FALSE": disposition, reason = "NOT_APPLICABLE", f"trigger fact {fact} is recorded FALSE"
            else: disposition, reason = "UNKNOWN", f"needs explicit trigger fact {fact}; absence is not FALSE"
        out.append({"id":sid,"version":standard["version"],"domain":row["domain"],"baseline":row["baseline"],"applicability":disposition,"reason":reason,"trigger_fact":FACTS.get(sid),"trigger_fact_sources":clank["fact_sources"],"normative_payload":standard})
    return {"clank_id":clank_id,"profile":clank["primary_profile"],"secondary_profiles":clank.get("secondary_profiles",[]),"baselines":registry["baselines"],"standards":out}
def audit_plan(clank_id):
    plan=[]
    resolved_by_id={x["id"]:x for x in resolve(clank_id)["standards"]}
    for row in frozen_standards():
        resolved=resolved_by_id[row["standard"]["id"]]
        if resolved["applicability"] != "APPLIES": continue
        s=row["standard"]; c=row["checklist"]
        plan.append({"standard_id":s["id"],"version":s["version"],"invariant":row["summary"]["requirement_summary"],"inspect":c["question"],"would_establish_conformance":"Inspectable target evidence satisfies the stated invariant.","would_establish_nonconformance":c["failure_means"],"forbidden_inference":s.get("forbidden", ["Do not infer from absent evidence."])[0],"reference":f"docs/{row['domain']}/constitution.md; {row['summary']['source_file']}; standards/{row['domain']}/agent-checklist.json"})
    return {"clank_id":clank_id,"mode":"BLIND_AUDIT_PLAN","items":plan}
