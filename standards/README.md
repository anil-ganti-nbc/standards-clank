# Standards

One subdirectory per domain. Each standard is one JSON file conforming to
[../schemas/standard.schema.json](../schemas/standard.schema.json), named
after its `id` (e.g. `STD-UI-COM-001.json`).

| Domain | Directory | Status |
|---|---|---|
| GUI/UI | [ui/](ui/) | 9 candidate standards, all `PROPOSED` — see below |
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

No standard in this repository is `RATIFIED` (or even `REVIEWED`) yet. The
`ui/` directory holds 9 evidence-backed `PROPOSED` candidates from GUI
Ratification Pass 1 (2026-08-30) — see
[../docs/gui-ratification-pass-1.md](../docs/gui-ratification-pass-1.md) for
the full ratification table and evidence. They remain proposals until the
operator explicitly moves them through review and ratification per
[../docs/governance.md](../docs/governance.md).
