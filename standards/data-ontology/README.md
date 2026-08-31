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
adversarial adjudication, Pass 1 drafting, Pass 2 adversarial review,
Pass 2.5 revisions, Pass 3 ratification survey) and groups its four
standards together because they were evidenced, adjudicated, drafted, and
ratified as one coherent pass, cross-reference each other, and share a
lineage back to the same evidence corpus. See
[docs/data-ontology/pass1/README.md](../../docs/data-ontology/pass1/README.md)
for why a single new domain was chosen over splitting these four across
the pre-existing `events`/`evidence`/`classification` folders.

**4 `RATIFIED`, 0 `PROPOSED`, as of the 2026-08-31 ratification closure.**
Building or auditing data/ontology behavior in a Clank? Start with
[docs/data-ontology/constitution.md](../../docs/data-ontology/constitution.md)
(the compact, agent-facing summary of all four RATIFIED rules, with
inline citations) rather than these raw JSON files one at a time.
[ratified-index.json](ratified-index.json) and
[agent-checklist.json](agent-checklist.json) are generated from the files
below by `tools/data_ontology_agent_layer.py` — see
`scripts/generate_data_ontology_agent_layer.py` to regenerate them after
any change.

| id | title | version | status | decision |
|---|---|---|---|---|
| [STD-DATA-COM-001](STD-DATA-COM-001.json) | Continuity/epoch state must be explicit | v1 | RATIFIED | [0010](../../decisions/0010-data-com-001-decision.md) |
| [STD-DATA-COM-002](STD-DATA-COM-002.json) | First-seen is not novelty; default novelty views must exclude baseline records by construction | v2 | RATIFIED | [0011](../../decisions/0011-data-com-002-decision.md) |
| [STD-DATA-COM-003](STD-DATA-COM-003.json) | Entity-identity merges must be conservative, evidence-gated, auditable, and reversible | v2 | RATIFIED | [0012](../../decisions/0012-data-com-003-decision.md) |
| [STD-DATA-COM-004](STD-DATA-COM-004.json) | Observation, canonical-fact/change, and operator-decision records must stay separable and traceable | v1 | RATIFIED | [0013](../../decisions/0013-data-com-004-decision.md) |

Full evidence, adjudication, drafting, and review trail:
[docs/data-ontology/pass0/](../../docs/data-ontology/pass0/) (evidence +
adjudication), [pass1/](../../docs/data-ontology/pass1/) (drafting
dossiers), [pass2/](../../docs/data-ontology/pass2/) (adversarial review),
[pass3/](../../docs/data-ontology/pass3/) (ratification survey). Every
other Pass 0B candidate (C4 availability-honesty, C6 timestamp-shaped
values, C7 cross-Clank identity, and the MEDIUM/LOW clusters) remains
exactly `HOLD`, `REHOME`, or `REJECT` — none were promoted by this
closure.

**Not frozen.** Unlike the UI domain (`ui-standards-v1.0`), this
ratification closure does not itself declare a `data-ontology-standards-v1.0`
baseline — several candidates remain explicitly HELD, and the next step
is a targeted gap/hold-resolution audit asking whether those HOLDs are
genuinely required before v1 or can safely stay deferred.
