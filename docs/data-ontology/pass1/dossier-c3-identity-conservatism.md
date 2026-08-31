# Pass 1 drafting dossier — C3: Entity identity conservatism

**Candidate ID**: C3 (Pass 0B) → **STD-DATA-COM-003** (this pass)

**Source Pass 0 cluster(s)**: `entity-identity-coarse-key-merge`
(STRONG/HIGH)

**Adjudication result** (Pass 0B): KEEP DISTINCT + ADVANCE — posture and
consequence-level invariant, algorithm-neutral.

## Strongest evidence

Four independent, dated incidents of the same shape, escalating in
severity: oem-radar's coarse `model_key` merge (recurred a second time in
different code); feature-phone-clank's `IDENTITY_ANOMALY` bug;
tablet-clank's 48 false `new_product` events from un-deduplicated carrier
URLs; semiconductor-intelligence's merged-entity artifact becoming the
database's highest-scored "story," forcing a full architectural rebuild.
Against these, watch-clank's conservative, evidence-gated allowlist policy
produced zero confirmed false merges.

## Strongest counterexample

"Two sources report the same product with trivially different model
numbers; strict conservatism misses a real merge forever, and the
operator never sees it — conservatism has a real cost too." Tested in the
Pass 0B candidate card: survives, narrowed. The standard does not ban
merges — it bans *ungated, unauditable, irreversible* ones. The asymmetry
(a missed merge surfaces as a visible, benign duplicate; a false merge
silently corrupts canon and propagates downstream) justifies the default
posture without banning aggressive matching outright — oem-radar's
confidence-scored cascade and semiconductor-intelligence's
propose-aggressively/commit-conservatively proposal layer both conform,
because both gate the *commit* step even where the *candidate-surfacing*
step is aggressive.

## Exact semantic boundary

Binds the **consequence** of an identity decision, never the matching
algorithm: (1) insufficient evidence must leave records unresolved rather
than forced together, (2) a candidate-surfacing signal is not itself
grounds for a committed merge, (3) any automatic merge must be
evidence-gated, auditable, and reversible/information-preserving. Does
not choose a canonical-identity mechanism (model number, source ID,
region+model, fingerprint, alias table, compound key, manual resolution
are all left free) and does not resolve the separate, still-HELD question
of regional-variant identity (`regional-variant-identity` cluster) —
explicitly cross-referenced, not restated.

## Overlap analysis

- Explicitly out of scope: **cross-Clank entity identity** (Pass 0B
  candidate C7, HOLD/DEFER, blocked by clank-architecture's ADR-0002
  `DO_NOT_STANDARDISE`). This standard binds within-Clank merges only —
  stated directly in the drafted `notes` field to prevent scope creep at
  ratification time.
- No overlap with any ratified `STD-UI-*` standard — none of the UI
  standards govern identity/merge logic; STD-UI-SKU-001 (availability
  disposition vocabulary) is adjacent in subject matter (both concern the
  SKU/product domain) but governs the QC-review vocabulary layer, not
  entity-identity resolution.
- Related to **STD-DATA-COM-004** (provenance tiers): a merge decision's
  auditability/reversibility requirement is a specific instance of
  COM-004's "operator/system decisions must remain traceable to the state
  they were made against" — drafted as a separate standard because C3's
  invariant (conservative posture, gated commit) is substantively about
  *when* to merge, while C4/COM-004 is about *how facts stay traceable*
  regardless of whether a merge ever happens. A Clank with no merging at
  all is out of C3's scope but may still be in COM-004's.

## Draft rationale

"False merges are worse than missed merges" (chinese-tech-wire's stated
philosophy, independently validated by every repo that violated it being
burned) was adopted as the standard's underlying posture rather than
quoted verbatim, since chinese-tech-wire itself is outside this pass's
four candidates and the phrase is being generalized from one repo's
stated design principle to a fleet-wide default, which the evidence
supports but which deserves to be stated as this standard's own reasoning
rather than attributed as if fleet-wide already.

## Unresolved wording questions

1. "Reversible or otherwise information-preserving" is deliberately
   disjunctive (the task's own guidance: "reversibility... if physical
   deletion is not used") — is this precise enough, or does it need a
   concrete minimum bar (e.g. "the pre-merge records must be
   reconstructable from retained data, an audit log, or an equivalent
   mechanism")? Drafted with both the disjunctive framing and a concrete
   acceptance criterion naming several conforming mechanisms; flagged for
   review on whether the list is exhaustive enough to be useful without
   becoming prescriptive.
2. Is "insufficient evidence" itself testable, or does it need a
   fleet-wide minimum evidentiary bar? Deliberately left undefined — the
   task's own guidance says "is 'same normalized title' ever enough
   universally? likely no," and this pass agrees: any fleet-wide
   evidentiary threshold would itself be an algorithm prescription this
   standard is designed to avoid. Left for reviewers to judge whether this
   makes the standard too vague to test, or correctly implementation-
   neutral.

## Recommendation: READY FOR REVIEW
