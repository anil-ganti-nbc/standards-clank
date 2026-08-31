# 0013 — Data/Ontology ratification: STD-DATA-COM-004 (Provenance tier separation)

Date: 2026-08-31
Status: Accepted (operator ruling, 2026-08-31)
Survey dossier: [../docs/data-ontology/pass3/ratification-survey.md](../docs/data-ontology/pass3/ratification-survey.md)
Standard: [../standards/data-ontology/STD-DATA-COM-004.json](../standards/data-ontology/STD-DATA-COM-004.json) (v1, PROPOSED)

An agent MUST NOT ratify this standard (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Survey outcome (Pass 3, from stored Pass 0A/0B/1/2 evidence — no recrawl)

- Evidence: STRONG — the strongest independent convergence in the corpus:
  8 of 9 surveyed Clanks built a 3–5 tier observation→fact→change→decision
  stack with zero cross-citation, and oem-radar's Stage 11 incident
  (evidence observations flooding the canonical change table to 44.6% of
  "alerts") demonstrates the collapse harm mode directly.
- v1 unchanged since Pass 2 approval; all Pass 2 checks confirmed:
  tier separation is trigger-scoped (pure pass-through Clanks out; absent
  operator-decision layers exclude only that clause); a discriminator
  column on one table conforms; inferred/derived values stay
  distinguishable from source-explicit claims; canonical facts remain
  traceable to supporting observations (URL + content hash + extraction
  record or equivalent — unlimited raw-payload retention is NOT required);
  retention duration correctly remains per-Clank operations policy; the
  relationship to STD-UI-COM-002 is COMPLEMENTARY (UI-COM-002 is the
  stricter, UI-specific instance of the general decision-tier
  traceability requirement).
- Verified against both a high-volume SKU Clank (oem-radar: per-SKU
  configurations, restock subsystem, Stage 11 collapse-and-fix history)
  and a news/intelligence Clank (semiconductor-intelligence:
  Claim/Evidence/ClaimEvent stack, EXPLAINABILITY_CONTRACT) from stored
  evidence — both conform as-is.

## Recommendation

RATIFY AS WRITTEN (agent recommendation — operator decides). The
separation + traceability invariant is convergently implemented fleet-wide
and the standard deliberately prescribes no shapes (ADR-0002 respected).

## Operator options

- **Option A — Ratify as written** (recommended). No surveyed
  implementation changes.
- ~~Option B — Add a retention-duration clause~~: not offered — retention
  is lifecycle/operations policy (oem-radar hash-on-disk vs
  chinese-tech-wire in-DB retention both conform); the standard already
  requires only that traceability hold while a fact is claimed.
- ~~Option C — Adopt diagnostic-clank's EventEnvelope shape~~: not
  offered — ADR-0002 DO_NOT_STANDARDISE forbids schema unification; the
  envelope remains a Pass 1 reference only.

## Operator ruling — ACCEPTED, Option A (2026-08-31)

The operator ratified STD-DATA-COM-004 as written. Recorded reasoning:
the evidence bar has been met — the strongest independent convergence in
the entire Pass 0 corpus (8 of 9 Clanks, zero cross-citation), verified
against both a high-volume SKU Clank and a news/intelligence Clank from
stored evidence, and Pass 2/Pass 3 found no remaining counterexample or
domain problem. STD-DATA-COM-004 is therefore RATIFIED at v1, text
unchanged; traceability recorded in the standard's notes.
