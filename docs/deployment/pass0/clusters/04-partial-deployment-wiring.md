---
cluster: partial-deployment-wiring
likely_domain: DEPLOYMENT
priority: MEDIUM
evidence_strength: MODERATE
---
# Partial deployment and runtime wiring

**Concern:** code, scheduler, wrapper, service unit, container, and dependent runtime components can change on different paths, creating a partially deployed topology.

- **Supporting incidents:** DEP-INC-004, DEP-INC-007.
- **Positive implementations:** feature-phone’s disjoint lane resources; smartwatch verifies units, schedules, and persistence before/after rollout.
- **Lineage:** independent incidents, though scheduler authority is shared governance.
- **Strongest evidence:** a corrected code/config path did not repair the separate production wrapper.
- **Contrary evidence:** deliberate multi-lane coexistence is safe when DB/volume/lock/credentials are structurally isolated.
- **Overlap:** Operations, Architecture; Fleet Law 5 ACTIVE and CI-backed.
- **Severity / recurrence:** medium-high / medium-high.
- **Candidate standardisation risk:** likely duplicates active single-authority law; could remain an implementation/audit concern.
- **Unanswered questions:** does deployment need a separate topology verification requirement beyond Law 5?
