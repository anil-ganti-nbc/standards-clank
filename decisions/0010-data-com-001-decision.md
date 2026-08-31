# 0010 — Data/Ontology ratification: STD-DATA-COM-001 (Continuity/epoch explicitness)

Date: 2026-08-31
Status: Accepted (operator ruling, 2026-08-31)
Survey dossier: [../docs/data-ontology/pass3/ratification-survey.md](../docs/data-ontology/pass3/ratification-survey.md)
Standard: [../standards/data-ontology/STD-DATA-COM-001.json](../standards/data-ontology/STD-DATA-COM-001.json) (v1, PROPOSED)

An agent MUST NOT ratify this standard (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Survey outcome (Pass 3, from stored Pass 0A/0B/1/2 evidence — no recrawl)

- Evidence: STRONG — four independent implementations (watch OperationalEpoch,
  oem-radar documented cutover, feature-phone + smartwatch core/continuity.py;
  three with no cross-citation to each other or ADR-0006, which smartwatch
  explicitly inherited) plus the TIMEX catalogue backfill burst incident.
- Trigger: correctly scoped to Clanks deriving novelty/alerting/editorial
  state from local prior history; stateless and no-novelty Clanks are out.
- Pass 2 approved it unmodified; the region-change example was confirmed
  safe (conditional, binds only break-representability, presupposes no
  regional-identity model).
- Known consequence if ratified: korean-tech-wire (derives alerting from
  local history, no continuity representation today) gains an expected
  remediation-backlog item — the same legitimate consequence pattern as
  watch-clank's COM-007 badge. Separately (pre-existing, unrelated to
  ratification): watch-clank's production epoch-table exposure remains an
  open operator flag from Pass 0B.

## Recommendation

RATIFY AS WRITTEN (agent recommendation — operator decides).

## Operator options

- **Option A — Ratify as written** (recommended). No surveyed
  implementation changes except expected backlog items.
- **Option B — Ratify with the region-change example removed** from the
  discontinuity-trigger list. Supportable only as extra caution while the
  regional-variant-identity cluster stays HELD; Pass 2 found the example
  non-prescriptive and safe, so B is not evidence-forced.

## Operator ruling — ACCEPTED, Option A (2026-08-31)

The operator ratified STD-DATA-COM-001 as written. Recorded reasoning:
the evidence bar has been met across independent lineages (watch-clank,
oem-radar, feature-phone-clank, smartwatch-clank), the region-change
example was confirmed by Pass 2 as non-prescriptive of regional identity,
and Pass 3 found no remaining counterexample or domain-boundary problem
strong enough to justify another drafting cycle. STD-DATA-COM-001 is
therefore RATIFIED at v1, text unchanged; traceability recorded in the
standard's notes. korean-tech-wire's resulting backlog item is an
expected consequence of ratification, not itself evidence of a violation
— any conformance finding against a specific Clank still requires a
normal audit, not an assumption from this ruling.
