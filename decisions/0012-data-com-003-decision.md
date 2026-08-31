# 0012 — Data/Ontology ratification: STD-DATA-COM-003 (Entity identity conservatism)

Date: 2026-08-31
Status: AWAITING OPERATOR DECISION
Survey dossier: [../docs/data-ontology/pass3/ratification-survey.md](../docs/data-ontology/pass3/ratification-survey.md)
Standard: [../standards/data-ontology/STD-DATA-COM-003.json](../standards/data-ontology/STD-DATA-COM-003.json) (v2, PROPOSED)

An agent MUST NOT ratify this standard (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Survey outcome (Pass 3, from stored Pass 0A/0B/1/2 evidence — no recrawl)

- Evidence: STRONG — four independent, dated incidents escalating to
  severe (oem-radar's model_key merge and its recurrence in different
  code; feature-phone's IDENTITY_ANOMALY; tablet-clank's 48 false
  new_product events; semiconductor-intelligence's merged-entity artifact
  forcing an architectural rebuild), against watch-clank's zero-false-
  merge conservative counter-model.
- v2 confirms resolution of both Pass 2 REVISE tightenings: the
  conflicting-discriminator clause is scoped to records under
  consideration / the merged record (no world-knowledge requirement);
  automatic merges must record the performing mechanism/decision-path
  (making a recurring false-merge class detectable). No universal
  confidence threshold, key hierarchy, or identity algorithm was added;
  cross-Clank identity remains out of scope (C7 HOLD, ADR-0002).
- "Prefer a missed merge over a false merge" remains framed as a default
  posture, not an absolute: v2's own text defines the procedural
  consequence (insufficient evidence → records stay unresolved), and both
  oem-radar's gated cascade and semiconductor-intelligence's
  propose-aggressively/commit-conservatively layer conform.

## Recommendation

RATIFY AS WRITTEN (agent recommendation — operator decides). The v2
tightenings resolved the Pass 2 weaknesses without disturbing the
posture.

## Operator options

- **Option A — Ratify as written** (recommended). The posture framing is
  evidence-faithful; the audit requirements are the testable core.
- ~~Option B — Add a fleet-wide minimum evidence bar~~: not offered — it
  would be algorithm prescription (Pass 1/2 analyses concur; no universal
  bar survives across title-matching, model-number, and clustering
  domains).
- ~~Option C — Retire~~: not offered — four independent incidents with
  severity up to architectural rebuild are the opposite of insufficient
  evidence.
