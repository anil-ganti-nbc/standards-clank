---
cluster: materialisation-truth
likely_domain: DEPLOYMENT
priority: HIGH
evidence_strength: STRONG
---
# Materialisation truth

**Concern:** repository configuration, unit files, wrappers, and image inputs do
not become true merely by being committed; the actual execution path must load
the intended state.

- **Supporting incidents:** DEP-INC-001, DEP-INC-004, DEP-INC-006, DEP-INC-009.
- **Positive implementations:** feature-phone’s isolated deployment; smartwatch’s five-way check; Diagnostic phase0 checklist.
- **Lineage:** three independent incidents; no shared fix. DEP-INC-006 is reused Operations evidence.
- **Strongest evidence:** Garmin production/soak wrapper divergence, which silently changed the effective proxy.
- **Contrary evidence:** intentional dev/experimental divergence exists when isolated and explicit.
- **Overlap:** Operations (scheduler), Security (environment values), Fleet Laws 5/6; Law 6 is ACTIVE.
- **Severity / recurrence:** high / high.
- **Candidate standardisation risk:** may duplicate Law 6 or prescribe deployment tooling.
- **Unanswered questions:** must verification inspect every configuration value, or only declared deploy-critical inputs?
