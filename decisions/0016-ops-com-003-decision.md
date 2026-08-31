# 0016 — Operations ratification: STD-OPS-COM-003 (Promotion/soak evidence integrity)

Date: 2026-08-31
Status: AWAITING OPERATOR DECISION
Survey dossier: [../docs/operations/pass3/ratification-survey.md](../docs/operations/pass3/ratification-survey.md)
Standard: [../standards/operations/STD-OPS-COM-003.json](../standards/operations/STD-OPS-COM-003.json) (v1, PROPOSED)

An agent MUST NOT ratify this standard (see
[0002-no-agent-self-ratification.md](0002-no-agent-self-ratification.md)).

## Survey outcome (Pass 3, from stored Pass 0A/0B/1/2 evidence — no recrawl)

- Evidence: STRONG jointly across the four merged facets (trigger
  provenance, soak-clock reset semantics, promotion-gate drift,
  distinguishable interventions); facet 1 (trigger provenance) alone is
  MODERATE — no confirmed harm incident exists for it in isolation, a
  caveat carried honestly from the candidate card through the Pass 1
  dossier into this survey rather than smoothed over. Facet 1 is credited
  as the verifiability foundation the other facets' incident (INC-013)
  depends on, and semiconductor-intelligence's scheduler-routing design
  proves the structural form is achievable.
- Trigger: correctly scoped to any Clank with a soak/promotion lifecycle;
  a Clank with everything production-immediately is out of scope,
  confirmed survivable at both drafting and Pass 2 review.
- Pass 2 approved unmodified on a fresh adversarial read of whether the
  four facets cohere as one invariant (they do) and whether facet 1's
  weaker evidence undermines the whole (it does not — it is accepted as
  the dependency foundation of facet 4's INC-013 evidence, and cycle-count/
  retention-duration standardization was correctly avoided, left
  per-Clank policy).
- Known consequence if ratified: none of the surveyed evidence describes
  a specific Clank's current non-conformance in enough detail to name a
  remediation-backlog item here — any specific-Clank finding requires a
  normal audit, not an assumption from this survey.

## Recommendation

RATIFY AS WRITTEN (agent recommendation — operator decides).

## Operator options

- **Option A — Ratify as written** (recommended). The widest merge of
  the four OPS candidates (four source clusters), and the one candidate
  Pass 1's own dossier flagged as having the weakest single facet — but
  Pass 2's adversarial review specifically tested facet coherence and
  facet-1 sufficiency and found no revision needed.
- **Option B — Ratify with facet (1) (trigger provenance) split into a
  SHOULD-level acceptance criterion rather than MUST-level**, reflecting
  its standalone MODERATE evidence strength versus the STRONG evidence
  behind facets 2-4. Supportable as a proportionality argument (weaker
  standalone evidence, softer obligation); not evidence-forced, since
  Pass 0B/1/2 all treated the four facets as one coherent invariant
  rather than four independently-graded ones, and facet 1's dependency
  relationship to INC-013 (a MUST-worthy incident) argues against
  softening it specifically.
