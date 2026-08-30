# 0008 — Pass 3 disposition: STD-UI-COM-007

Date: 2026-08-31
Status: AWAITING OPERATOR DECISION
Dossier: [../docs/pass3-proposed-standards/com-007-dossier.md](../docs/pass3-proposed-standards/com-007-dossier.md)

An agent MUST NOT ratify, retire, or alter this standard's normative
status (see [0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Survey outcome (summary)

Nine Clanks surveyed. The v2 conditional structure resolves the Pass 1
fleet split: policy-permitting implementations that label maturity at the
control (korean-tech-wire, tablet-clank, feature-phone-clank) conform;
policy-forbidding implementations conform (smartwatch-clank 400
`not_finalized`; oem-radar structural exclusion); no-maturity and
no-controls Clanks (chinese-tech-wire, semiconductor-intelligence,
smartphone-clank) are cleanly N/A by the trigger clause.

**Material consequence to weigh:** watch-clank — whose policy permits
manual experimental runs, with exemplary bulk isolation — does **not**
render maturity at its RUN NOW control (operations.html shows only a
LAYER badge and health state). Ratifying as written therefore creates an
immediate, small remediation-backlog item for watch-clank (a non-production
badge on that control). The dossier recommends accepting that: four other
lineages already practice control-adjacent maturity labeling, and the
visibility clause is the rule's load-bearing content.

PARTIALLY OVERLAPS COM-006 by design (bulk isolation cross-references it);
the single-control visibility and policy-forbids clauses are distinct
content. Not redundant.

## Recommendation

RATIFY AS WRITTEN (agent recommendation — operator decides), accepting the
watch-clank remediation-backlog consequence.

## Operator options

- **Option A — Ratify as written.** STD-UI-COM-007 becomes RATIFIED v2;
  watch-clank gains a small remediation-backlog item (maturity badge at
  the RUN NOW control). No other surveyed Clank changes.
- **Option B — Ratify a narrowed visibility clause** (e.g. allowing
  identification "in the same control table" instead of "at the point of
  the control"). The dossier advises against this: watch's table row
  still shows LAYER, not maturity, so even this narrowing would not bring
  watch into conformance — it would only weaken the invariant.
- **Option C — Retire, relying on COM-006.** Rejected by the dossier:
  COM-006 covers only the bulk case; the single-control visibility and
  policy-forbids clauses would be lost.
- ~~Option D — Hold~~: not offered. All nine implementations were
  surveyed; there is no missing evidence source.
