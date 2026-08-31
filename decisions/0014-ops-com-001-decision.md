# 0014 — Operations ratification: STD-OPS-COM-001 (Execution materialization truth)

Date: 2026-08-31
Status: AWAITING OPERATOR DECISION
Survey dossier: [../docs/operations/pass3/ratification-survey.md](../docs/operations/pass3/ratification-survey.md)
Standard: [../standards/operations/STD-OPS-COM-001.json](../standards/operations/STD-OPS-COM-001.json) (v1, PROPOSED)

An agent MUST NOT ratify this standard (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Survey outcome (Pass 3, from stored Pass 0A/0B/1/2 evidence — no recrawl)

- Evidence: STRONG — five independent mechanisms (watch-clank, oem-radar,
  chinese-tech-wire, korean-tech-wire, semiconductor-intelligence), each
  built without cross-citation to a shared implementation. The corpus's
  most severe incident (INC-027: one root-privileged redeploy silently
  broke cron across three Clanks for ~36 hours) anchors it, alongside
  INC-002, INC-021, and INC-012.
- Trigger: correctly scoped to any Clank firing collection from any
  trigger mechanism; scheduler technology and location are explicitly out
  of scope, so an externally-scheduled Clank still binds.
- Pass 2 approved unmodified: acceptance criterion 3 splits the exact
  INC-027 failure shape (invocation recorded, outcome recorded, neither
  inferred from the other); acceptance criterion 4 turns INC-028's
  false-positive shape (a monitor over-inferring a gap from a
  legitimately empty cycle) into a positive no-work-record requirement,
  closing the one real counter-incident found in the corpus.
- Known consequence if ratified: none of the surveyed evidence describes
  a specific Clank's current non-conformance in enough detail to name a
  remediation-backlog item here — any specific-Clank finding requires a
  normal audit, not an assumption from this survey.

## Recommendation

RATIFY AS WRITTEN (agent recommendation — operator decides).

## Operator options

- **Option A — Ratify as written** (recommended). No surveyed
  implementation issue or unresolved counterexample remains.
- **Option B — Ratify with the duplicate/zombie-automation detectability
  clause (forbidden-list item 4) removed**, narrowing the standard to
  pure invocation/outcome recording and leaving detectability of
  duplicate triggers entirely to Fleet Law 5. Supportable only as extra
  caution against reading this standard as reaching into Law 5's
  single-authority territory; Pass 1's own dossier flagged this exact
  question for adversarial review and it was not specifically contested
  at Pass 2, so B is not evidence-forced.
