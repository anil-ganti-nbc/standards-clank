# data-ontology

Standards about what information *means* and how truth is represented —
first-seen vs. novelty, continuity/epoch state, entity identity and
merges, and evidence/provenance traceability. Distinct from the `events`,
`evidence`, and `classification` domains named in the original charter:
those pre-existed as empty scaffolding for narrower concerns (event
plumbing, raw evidence retention, collector/source maturity
classification); `data-ontology` is the domain that emerged from the
dedicated [Data/Ontology evidence-mining
program](../../docs/data-ontology/) (Pass 0A evidence inventory, Pass 0B
adversarial adjudication, Pass 1 drafting) and groups its four surviving
candidates together because they were evidenced, adjudicated, and
drafted as one coherent pass, cross-reference each other, and share a
lineage back to the same evidence corpus. See
[docs/data-ontology/pass1/README.md](../../docs/data-ontology/pass1/README.md)
for why a single new domain was chosen over splitting these four across
the pre-existing `events`/`evidence`/`classification` folders.

4 candidate standards, all `PROPOSED` as of Pass 1 (2026-08-31). None are
ratified.

| id | title | status |
|---|---|---|
| [STD-DATA-COM-001](STD-DATA-COM-001.json) | Continuity/epoch state must be explicit | PROPOSED |
| [STD-DATA-COM-002](STD-DATA-COM-002.json) | First-seen is not novelty; default novelty views must exclude baseline records by construction | PROPOSED |
| [STD-DATA-COM-003](STD-DATA-COM-003.json) | Entity-identity merges must be conservative, evidence-gated, auditable, and reversible | PROPOSED |
| [STD-DATA-COM-004](STD-DATA-COM-004.json) | Observation, canonical-fact/change, and operator-decision records must stay separable and traceable | PROPOSED |

Full evidence, adjudication, and drafting trail:
[docs/data-ontology/pass0/](../../docs/data-ontology/pass0/) (evidence +
adjudication) and
[docs/data-ontology/pass1/](../../docs/data-ontology/pass1/) (drafting
dossiers). Every other Pass 0B candidate remains HOLD, REHOME, or REJECT
— none of those were promoted in this pass.
