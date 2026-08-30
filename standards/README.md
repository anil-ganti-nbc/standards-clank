# Standards

One subdirectory per domain. Each standard is one JSON file conforming to
[../schemas/standard.schema.json](../schemas/standard.schema.json), named
after its `id` (e.g. `STD-UI-COM-001.json`).

| Domain | Directory | Status |
|---|---|---|
| GUI/UI | [ui/](ui/) | scaffolded only, not populated — see below |
| Collector behaviour | [collectors/](collectors/) | empty |
| Specialist source scoping / authority | [sources/](sources/) | empty |
| Classification | [classification/](classification/) | empty |
| Event semantics / novelty | [events/](events/) | empty |
| Provenance / evidence | [evidence/](evidence/) | empty |
| Health | [health/](health/) | empty |
| Delivery / Discord | [delivery/](delivery/) | empty |
| Soak | [soak/](soak/) | empty |
| Security / secrets | [security/](security/) | empty |
| Operator workflow / feedback / QC | [operator-workflow/](operator-workflow/) | empty |

No standard in this repository is `RATIFIED` yet. The `ui/` directory in
particular exists to hold the schema/tooling scaffolding for a future GUI
standards ratification exercise — it is deliberately empty of actual rules.
See the repository root README for why.
