# Standards

One subdirectory per domain. Each standard is one JSON file conforming to
[../schemas/standard.schema.json](../schemas/standard.schema.json), named
after its `id` (e.g. `STD-UI-COM-001.json`).

| Domain | Directory | Status |
|---|---|---|
| GUI/UI | [ui/](ui/) | 12 `RATIFIED`, 3 `PROPOSED` — see below |
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

As of Operator Ratification Decision 002 (2026-08-30), 12 standards under
`ui/` are `RATIFIED`; 3 were returned for revision and remain `PROPOSED`
(v2), all awaiting re-review. See
[../docs/gui-ratification-pass-1.md](../docs/gui-ratification-pass-1.md) and
[../docs/gui-ratification-pass-2.md](../docs/gui-ratification-pass-2.md) for
evidence, and
[../decisions/0003-operator-ratification-decision-001.md](../decisions/0003-operator-ratification-decision-001.md)
and
[../decisions/0004-operator-ratification-decision-002.md](../decisions/0004-operator-ratification-decision-002.md)
for the two ratification decisions made so far. Ratification does not
authorize remediation of any existing Clank against these rules — that is
separate, not-yet-commissioned work.
