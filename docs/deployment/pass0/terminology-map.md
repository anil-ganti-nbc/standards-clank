# Deployment Pass 0A — Terminology Map

| Term | Observed meanings and semantic difference |
|---|---|
| deploy / release | smartwatch uses a documented host rollout; watch compose may start a stale tag. A command exit is an action result, not runtime truth. |
| production / staging / experimental | smartwatch and feature-phone use lane isolation; a name such as “staging” is explicitly not authority to destroy state (ADR-0009). |
| host / remote / target | an enumerated machine/instance, not an inferred fleet. Tablet’s missed Hetzner host proves a sweep must state coverage. |
| runtime / revision / version / artifact | runtime identity is a process/CLI/OCI fact; repo HEAD and branch names are source facts. Fleet Law 6 requires host evidence. |
| image / artifact provenance | OCI revision labels and immutable digests can map artifact to source; mutable or default tags cannot establish that mapping. |
| config / materialise | committed YAML/environment is intended input; a copied, loaded, and observed service setting is materialised config. Garmin wrapper divergence is the counterexample. |
| restart / reload / service / scheduler / systemd / cron | installing code does not prove unit reload, enablement, old-authority removal, or correct execution path. |
| migration / schema | Alembic/schema head is persisted-state compatibility, not merely successful code install. `create_all()` can conceal the migration reality. |
| readiness / health / smoke test | post-deploy checks range from service health to five-way parity. Health can be green while a revision/config is stale; readiness must identify what is checked. |
| rollback / recovery | a source checkout revert is distinct from schema/data recovery. Compatible rollback artifacts and restore proof were mostly planning/checklist evidence. |
| container / volume | containers are replaceable artifacts; volumes are persistent state. Volume names do not prove ownership, lane, or disposability. |
| environment / secrets | environment settings can be deploy wiring (Garmin proxy) or security material; this pass counts only the former where state transition is causal. |

**Key distinction:** “deploy command succeeded” means the command returned its
defined result. “Intended state is materially running” requires target identity,
artifact/revision, loaded configuration, relevant schema/state compatibility,
and execution-path verification appropriate to the deployment.
