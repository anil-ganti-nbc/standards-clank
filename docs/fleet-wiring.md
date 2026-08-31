# Fleet wiring M0

This governance-only layer maps a registered Clank to the frozen UI,
Data/Ontology, Operations, and Deployment v1.0 baselines. It is not a runtime
dependency: target applications never import this repository, call it over the
network, or change their schedulers or databases for it.

`profiles/fleet-adoption.json` records profile membership and only evidenced
trigger facts. A profile selects family candidates; each standard is then
resolved as `APPLIES`, `NOT_APPLICABLE`, or `UNKNOWN`. `UNKNOWN` means a fact
is not evidenced, never that a trigger is absent or that a target is deficient.

The resolver uses `git show <immutable-tag>:<path>` to obtain the frozen
manifest, normative payload, and generated checklist. Forward commits cannot
silently change an audit input. A later v2 baseline requires a new explicit
registry baseline selection; M0 never upgrades a target automatically.

`--audit-plan` implements the blind boundary: frozen standards, constitutions
and checklists, and registry facts may be supplied to an auditor. Prior
findings, target history, and remediation proposals belong only to a later,
separately-authorized informed remediation workflow. Future conformance reports
consume this plan and record their evidence independently; applicability is not
a conformance verdict.
