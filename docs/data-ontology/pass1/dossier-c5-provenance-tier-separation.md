# Pass 1 drafting dossier — C5: Provenance tier separation

**Candidate ID**: C5 (Pass 0B) → **STD-DATA-COM-004** (this pass; note
the Pass 0B candidate numbering skips to C5 because C4 was split/held —
this pass's fourth standard ID, `STD-DATA-COM-004`, is unrelated to that
numbering gap)

**Source Pass 0 cluster(s)**: `evidence-provenance-granularity`
(STRONG/HIGH)

**Adjudication result** (Pass 0B): KEEP DISTINCT + ADVANCE — the
envelope-shape prescription is explicitly out of scope.

## Strongest evidence

The strongest independent-convergence evidence in the entire Pass 0
corpus: 8 of 9 surveyed Clanks independently built a 3-to-5 tier
observation→fact→change→decision stack with zero cross-citation between
implementations. chinese-tech-wire's `EXPLAINABILITY_CONTRACT.md` and
semiconductor-intelligence's Claim/Evidence/ClaimEvent stack are mature
enough to function as reference templates. oem-radar's Stage 11 incident
directly demonstrates the harm mode this standard forbids: evidence
observations flooded the canonical change-event table to 44.6% of all
"alerts," burying real signal, before being split back into a separate
table.

## Strongest counterexample

"A single-collector Clank appends everything to one ledger and has never
had a burial problem — the tier mandate is ceremony." Tested in the Pass
0B candidate card: survives, narrowed. The standard requires that
observation records and canonical change records be *distinguishable and
separately consumable* — separate tables are the common mechanism, not
the requirement itself, and a discriminator column on one table would
satisfy it equally. The traceability half (canonical fact → supporting
observations) already holds trivially in any Clank that retains evidence
at all. A Clank with no derived canonical state (pure pass-through
logging) is out of scope by trigger, not exempted by argument.

## Exact semantic boundary

Binds **separation and traceability**, never tier count (3-5 observed,
all conformant) or storage shape. Three sub-requirements: (1) observation
and canonical-fact/change and (where present) operator-decision records
stay distinguishable and separately consumable, (2) every canonical fact
traces back to supporting observations at explanatory granularity, (3) an
inferred/derived value is never presented as a direct source claim.
Deliberately does not require unlimited raw-payload retention — a
content hash, extraction record, or source-observation reference all
satisfy traceability without mandating storage cost a Clank's own
retention needs don't call for.

## Overlap analysis

- **STD-UI-COM-002** (QC decisions must be atomic, provenance-bearing,
  race-guarded) governs the write-contract and UI-truthfulness of the
  *decision* tier specifically, at the operator-action layer. This
  standard's decision-tier clause is a generalization one level down: any
  Clank's operator-decision records (not only QC decisions reached
  through a ratified UI) must stay traceable to what they were made
  against. STD-UI-COM-002 is one conforming, already-ratified instance of
  this broader data-layer requirement — this standard does not restate or
  weaken STD-UI-COM-002's stronger, UI-specific atomicity/race-guard
  requirements.
- **STD-UI-COM-009** (run/stage observability), **STD-UI-COM-010**
  (timestamp semantic role + timezone), **STD-UI-COM-011** (delivery
  state observability) all govern what an operator-facing UI must expose
  — none require or restate anything about the underlying data-tier
  separation this standard binds. Checked explicitly per the task's
  instruction; no restatement found.
- **STD-DATA-COM-003** (identity conservatism): related, not overlapping
  — see that dossier's overlap section.

## Draft rationale

diagnostic-clank's draft `EventEnvelope` (unwritten, PROPOSED-adjacent) is
cited as a Pass 1 reference in the standard's evidence array, explicitly
not adopted or incorporated by reference — recommending a fleet-wide
envelope shape now would trespass on clank-architecture's own adopted
ADR-0002 (`DO_NOT_STANDARDISE`) position against schema unification, which
this pass is instructed to respect, not override.

## Unresolved wording questions

1. "At a granularity sufficient to explain why the Clank believes it" is
   deliberately qualitative rather than enumerating required fields
   (URL, hash, extraction-method, etc. are offered as acceptance-criteria
   examples, not a mandated minimum set). Flagged for review: is this too
   soft to test, or correctly resistant to becoming a schema
   prescription?
2. The standard says nothing about retention *duration* — only that
   traceability must be reconstructable while it's claimed to hold. Is a
   retention-window clause needed, or is that legitimately each Clank's
   own operational decision (as oem-radar's raw-payload-on-disk-by-hash
   approach and chinese-tech-wire's in-DB retention both suggest,
   independently)?

## Recommendation: READY FOR REVIEW
