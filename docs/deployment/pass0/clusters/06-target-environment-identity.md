---
cluster: target-environment-identity
likely_domain: DEPLOYMENT
priority: LOW
evidence_strength: LIMITED
---
# Target-environment identity

**Concern:** a deploy/verification operation needs an explicit target host and lane, rather than an assumption based on local state or partial inventory.

- **Supporting incidents:** DEP-INC-008, DEP-INC-010.
- **Positive implementations:** Diagnostic phase0 stable-instance checklist and explicit UNKNOWN/HOLD values.
- **Lineage:** one independent missed-host incident plus shared Diagnostic governance.
- **Strongest evidence:** tablet sweep never included the one live Hetzner target.
- **Contrary evidence:** no confirmed wrong-host deployment occurred in inspected sources.
- **Overlap:** Diagnostic, Architecture, Operations.
- **Severity / recurrence:** high if it occurs / uncertain.
- **Candidate standardisation risk:** insufficient independent incident evidence; may be a narrow acceptance criterion of cluster 02.
- **Unanswered questions:** should this merge into running revision identity instead of surviving separately?
