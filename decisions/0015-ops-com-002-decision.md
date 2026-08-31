# 0015 — Operations ratification: STD-OPS-COM-002 (Health-honesty two-axis complement)

Date: 2026-08-31
Status: Accepted (operator ruling, 2026-08-31)
Survey dossier: [../docs/operations/pass3/ratification-survey.md](../docs/operations/pass3/ratification-survey.md)
Standard: [../standards/operations/STD-OPS-COM-002.json](../standards/operations/STD-OPS-COM-002.json) (v1, PROPOSED)

An agent MUST NOT ratify this standard (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Survey outcome (Pass 3, from stored Pass 0A/0B/1/2 evidence — no recrawl)

- Evidence: STRONG — the single most convergently-independently-adopted
  pattern found across the entire Operations survey (7 of 9 fleet
  Clanks), anchored by INC-006 (ZERO_ITEMS masking 20 consecutive empty
  runs) and INC-022 (korean-tech-wire's independently-built found-vs-new
  distinction correctly catching an 8.5-day zero-new-observations block).
- Trigger: correctly scoped to any Clank whose health/alerting depends on
  distinguishing liveness from output; a pure analysis tool with neither
  axis is out of scope, confirmed at Pass 2 via a hybrid-parser-break
  test that passed.
- Pass 2 approved unmodified as a **narrow complement**, not a
  restatement, of `clank-architecture` Fleet Law 3 (ACTIVE,
  CI-enforced) — the standard ratifies only the axis-vocabulary and
  conflation-forbidden slice Law 3 leaves open across nine differently-named
  fleet implementations; Law 3's own health-honesty principle is
  deliberately not restated in the requirement text.
- Known consequence if ratified: smartphone-clank's `health_score()`
  computation is documented, corpus-cited evidence for the gap this
  standard addresses, and would be a plausible remediation-backlog
  candidate — but naming it as a conformance finding requires a normal
  audit, not an assumption from this survey.

## Recommendation

RATIFY AS WRITTEN (agent recommendation — operator decides).

## Operator options

- **Option A — Ratify as written** (recommended). Governance-overlap risk
  (Pass 1's flagged MED standardization risk against Fleet Law 3) was
  Pass 2's primary adversarial question and the drafted wording survived
  it — no evidence-forced revision remains.
- **Option B — Ratify with an explicit textual cross-reference to Fleet
  Law 3 added to the `requirement` field itself** (currently the Law 3
  relationship lives only in `rationale`/`notes`), making the narrow-complement
  boundary visible without opening the standard file. Supportable
  as a documentation-clarity improvement; not evidence-forced, since the
  boundary is already stated in full in fields a reader of the standard
  will see.

## Operator ruling — ACCEPTED (2026-08-31)

The operator ratified STD-OPS-COM-002 as written.
See the ratification closure commit for full traceability.
