# Data/Ontology Pass 1 — Candidate Standards Drafting (2026-08-31)

Drafts the four candidates Pass 0B advanced (`docs/data-ontology/pass0/adjudication.md`,
Advancement summary table). All four standards were written to
`standards/data-ontology/` with `status: PROPOSED` — **nothing in this
pass was ratified, reviewed, or self-approved.** Every other Pass 0B
candidate (C4, C6, C7, and the MEDIUM/LOW clusters) remains exactly
`HOLD`, `REHOME`, or `REJECT` — none were promoted.

## Candidate → standard mapping

| Task label | Pass 0B ID | Standard | Dossier |
|---|---|---|---|
| A — Continuity/epoch explicitness | C1 | [STD-DATA-COM-001](../../../standards/data-ontology/STD-DATA-COM-001.json) | [dossier-c1-continuity-explicitness.md](dossier-c1-continuity-explicitness.md) |
| B — First-seen vs novelty, read-side exclusion | C2 | [STD-DATA-COM-002](../../../standards/data-ontology/STD-DATA-COM-002.json) | [dossier-c2-novelty-read-side-exclusion.md](dossier-c2-novelty-read-side-exclusion.md) |
| C — Conservative entity identity / reversible merges | C3 | [STD-DATA-COM-003](../../../standards/data-ontology/STD-DATA-COM-003.json) | [dossier-c3-identity-conservatism.md](dossier-c3-identity-conservatism.md) |
| D — Provenance tier separation and traceability | C5 | [STD-DATA-COM-004](../../../standards/data-ontology/STD-DATA-COM-004.json) | [dossier-c5-provenance-tier-separation.md](dossier-c5-provenance-tier-separation.md) |

## Domain and ID convention chosen

The task's recommended provisional IDs (`STD-DATA-COM-001..004`) were used
as-is. **Domain**: `data-ontology`, added to `schemas/standard.schema.json`'s
domain enum (additive only — verified by
`tests/test_pass1_drafting.py::test_data_ontology_domain_enum_extension_is_additive_only`).
This was a genuine choice among alternatives, recorded here:

The original charter already named three narrower, still-empty domains
that could have hosted parts of this work: `events` ("event semantics /
novelty" — a near-exact fit for candidate B), `evidence` ("provenance /
evidence" — a near-exact fit for candidate D), and `classification`
("finalized/experimental/retired... classification" — a poor fit for
candidate C, which is about entity identity, not collector maturity
classification). Splitting the four candidates across three existing
folders (plus inventing a fourth for candidate C, which has no existing
home at all) was rejected because the four were evidenced, adjudicated,
and drafted together as one coherent domain pass, cross-reference each
other directly (C2 cites STD-DATA-COM-001's baseline concept; C3 and C5
both concern merge/change provenance), and splitting them would scatter
one coherent effort across mismatched pre-existing folders for a
resemblance-of-fit that doesn't actually hold for half of them. A single
new `data-ontology` domain keeps the four together, mirrors how `ui`
already holds many sub-concerns (QC, collector controls, health,
timestamps, delivery) under one domain rather than one-per-concern, and
leaves room for HOLD candidates (C4, C7, confidence-and-certainty,
canonical-fact-overwrite, regional-variant-identity) to land in the same
domain later without a second migration.

## Trigger field

The task's drafting principles required a "trigger/applicability" element
distinct from `applies_to` (which the existing schema scopes to
profiles/Clank names — a narrower concept than "does this Clank have the
architectural feature this standard binds at all"). A new optional
`trigger` string field was added to `schemas/standard.schema.json` for
exactly this. Existing `STD-UI-*` standards are unaffected (the field is
optional; none of them set it).

## What this pass explicitly did not do

- Did not ratify, review, or self-approve any of the four drafts.
- Did not promote any HOLD, REHOME, or REJECT Pass 0B candidate.
- Did not create any decisions/ record — per the existing convention
  (decisions/0003-0009 are all operator rulings, not agent-drafted
  placeholders), an operator ruling on these four drafts would need to be
  authored by the operator, mirroring how the UI domain's Pass 3 dossiers
  preceded, rather than co-shipped with, decisions/0007-0009.
- Did not re-crawl the fleet. Every claim below traces to Pass 0A
  evidence or Pass 0B adjudication; no new repo was inspected.
- Did not modify the frozen UI baseline (tag `ui-standards-v1.0`) or any
  target Clank.
