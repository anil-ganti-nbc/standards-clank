# 0009 — Pass 3 disposition: STD-UI-SKU-001

Date: 2026-08-31
Status: Accepted (operator ruling, 2026-08-31)
Dossier: [../docs/pass3-proposed-standards/sku-001-dossier.md](../docs/pass3-proposed-standards/sku-001-dossier.md)

An agent MUST NOT ratify, retire, or alter this standard's normative
status (see [0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Survey outcome (summary)

Nine Clanks surveyed. Wherever availability is in scope, availability-
negative is kept distinct from false-positive/not-useful — via three
encodings: a terminal OUT_OF_STOCK disposition (watch, smartwatch, tablet,
feature-phone — one documented lineage), an availability data-model +
AVAILABILITY_CHANGED change-type + TEMPORARY_STOCK_CHANGE reason-code pair
(oem-radar — an independent derivation that v2's encoding clause was
written to accommodate), and automatic availability-negative event types.
Wherever availability is out of scope (semiconductor-intelligence,
korean-tech-wire, smartphone-clank), the disposition is absent, with
semiconductor-intelligence's enums docstring independently recording why
("OUT_OF_STOCK … has no honest equivalent here"). No conflation incident
was found; the invariant is supported by independent design reasoning and
zero counter-implementations rather than operator harm. DISTINCT from
NEWS-001 (novelty axis vs stock axis); no overlap with other ratified
rules. UI-domain fit is resolved by v2's scoping to the QC disposition
layer (the same layer NEWS-001 governs); underlying availability data
models stay un-normated.

## Recommendation

RATIFY AS WRITTEN (agent recommendation — operator decides). v2 already
contains the Pass 1 narrowing; no surveyed implementation requires any
change.

## Operator options

- **Option A — Ratify as written.** STD-UI-SKU-001 becomes RATIFIED v2.
  No implementation in the surveyed fleet changes.
- **Option B — Retire / rehome to a future data-ontology standards
  domain.** The dossier assesses this as unnecessary: the invariant v2
  governs lives in the QC disposition vocabulary (an operator-facing
  review axis, the same layer NEWS-001 governs); the data-model side is
  already outside the standard's scope. Rehoming would leave the
  QC-vocabulary invariant unratified with nothing to rehome it into.
- **Option C — Hold for incident evidence** (ratify only after a real
  operator conflates an availability-negative with false-positive/
  not-useful in a live queue). Honest but weak: no concrete fetchable
  evidence source exists, all current evidence already points one way,
  and the cost of ratifying is zero changes anywhere. Offered for
  completeness because the dossier's "no incident found" caveat is real.

## Operator ruling — ACCEPTED, Option A (2026-08-31)

The operator ratified STD-UI-SKU-001 as written. Recorded reasoning: the
independent OEM Radar encoding (availability change-type + reason code,
never folded into the verdict axis) shows the invariant is not merely a
copied OUT_OF_STOCK enum tradition; where availability is in scope,
availability-negative and false-positive/not-useful are different semantic
axes and must remain distinguishable, and the current trigger avoids
imposing availability tracking on Clanks that do not model it.
STD-UI-SKU-001 is therefore RATIFIED at v2, text unchanged; traceability
recorded in the standard's notes.
