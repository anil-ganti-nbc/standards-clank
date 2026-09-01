# watch-clank — M4H final cross-domain conformance re-audit and admission

```json
{"clank":"watch-clank","date":"2026-09-01","findings":[{"standard":"STD-DEPLOY-COM-001","kind":"conformance","summary":"LIVE_PROOF_CONFIRMED at Watch d03bc4b2f90289686331af0447d5ca4e8cf55822: independent target, full-SHA OCI/runtime provenance, congruent selector/config, 22/22 timer wiring, schema compatibility, complete convergence, and deployment-status COMPLETE (exit 0)."}]}
```

## Final result

**WATCH-CLANK FULLY CONFORMING TO APPLICABLE FROZEN V1 STANDARDS**

| State | Count |
| --- | ---: |
| CONFORMS | 25 |
| NON_CONFORMING | 0 |
| INSUFFICIENT_EVIDENCE | 0 |
| NOT_APPLICABLE | 0 |
| UNKNOWN | 0 |

This is a read-only Standards re-audit and evidence-admission pass.  Watch
source `d03bc4b2f90289686331af0447d5ca4e8cf55822` was not modified.  The
audited deployment target is
`hetzner/ubuntu-4gb-hel1-1:user-systemd-docker`, and the result is scoped to
that revision, target, and evidence point; it is not a permanent assertion
about future revisions or deployments.

## Takeover and frozen baselines

Standards Clank `HEAD` and `origin/master` were both
`528b51c2e494890439abcaac87ce4e64e386d252`; the tree was clean and the full
pre-audit suite was green (`793 passed`).  Watch `origin/main` remained
`d03bc4b2f90289686331af0447d5ca4e8cf55822`; its tree was clean and no Watch
operation occurred in this pass.

The four immutable v1.0 tags were present and unchanged, resolving to:

| Domain | Tag target commit |
| --- | --- |
| UI | `d11320704aed69a3d8f854c9264b184e392ec80f` |
| Data/Ontology | `464a8057ea5dc26ef83248a20bafa0be5aa31148` |
| Operations | `7100f294a83c30594f2ff9e953f7c9f77a95747f` |
| Deployment | `33cc38849180716fd4d06b1356cf70c49d3d41d2` |

The controlling M4G applicability ledger records all 25 frozen ratified
standards as `APPLIES` (25/0/0 for APPLIES/NOT_APPLICABLE/UNKNOWN), with no
trigger fact changed in this pass.  The frozen resolver's ratified set remains
the same 25 standards; this narrow closure pass does not rewrite the existing
profile fact map.

## Standard-by-standard ledger

The 24 prior conformances were regression-checked against the unchanged Watch
SHA and M4G closure evidence.  Each remains `STILL_CONFORMS`; no regression or
new insufficiency was found.

| Standard | Domain | Applicability | Final verdict | Regression basis |
| --- | --- | --- | --- | --- |
| STD-UI-COM-001 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-002 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-003 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-004 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-005 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-006 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-007 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-008 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-009 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-010 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-011 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-COM-012 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-NEWS-001 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-NEWS-002 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-UI-SKU-001 | UI | APPLIES | CONFORMS | M4G closure unchanged |
| STD-DATA-COM-001 | Data/Ontology | APPLIES | CONFORMS | M4G closure unchanged |
| STD-DATA-COM-002 | Data/Ontology | APPLIES | CONFORMS | M4G closure unchanged |
| STD-DATA-COM-003 | Data/Ontology | APPLIES | CONFORMS | M4G closure unchanged |
| STD-DATA-COM-004 | Data/Ontology | APPLIES | CONFORMS | M4G closure unchanged |
| STD-OPS-COM-001 | Operations | APPLIES | CONFORMS | M4G closure unchanged |
| STD-OPS-COM-002 | Operations | APPLIES | CONFORMS | M4G closure unchanged |
| STD-OPS-COM-003 | Operations | APPLIES | CONFORMS | M4G qualification closure |
| STD-OPS-COM-004 | Operations | APPLIES | CONFORMS | M4G lock closure unchanged |
| STD-DEPLOY-COM-001 | Deployment | APPLIES | CONFORMS / CLOSED | Confirmed live proof below |
| STD-DEPLOY-COM-002 | Deployment | APPLIES | CONFORMS | M4G closure unchanged |

## DEPLOY-COM-001 closure

The confirmed live-proof artifact
[`watch-clank-deploy-live-proof-2026-09-01-confirmed.md`](watch-clank-deploy-live-proof-2026-09-01-confirmed.md)
was audited field-by-field rather than accepted from its verdict label:

| Required facet | Evidence and result |
| --- | --- |
| A. Intended state | Watch GitHub canonical `main` at full SHA `d03bc4b2f90289686331af0447d5ca4e8cf55822`; Docker `GIT_REVISION`/OCI label convention is declared in the frozen repository. **Satisfied.** |
| B. Target scope | `hetzner/ubuntu-4gb-hel1-1:user-systemd-docker`, host `ubuntu-4gb-hel1-1`. **Satisfied.** |
| C. Material artifact observation | Target image ID `sha256:a091fbe7f1736c98004c63f45c1b2c1c5abb85733e6b95779de635e4c90c7bdf`; OCI label and runtime identity independently observed. **Satisfied.** |
| D. Revision equality | Intended and observed full SHA are identical. **Satisfied.** |
| E. Config congruence | Effective selector is `watch-clank:d03bc4b2f90289686331af0447d5ca4e8cf55822`; `WATCH_CLANK_CONFIG_MATCHES=true`. **Satisfied.** |
| F. Runtime wiring | 22/22 required user-systemd timers are loaded active/waiting. **Satisfied.** |
| G. Convergence | No mixed containers; one-shot architecture is fully represented by the selected immutable artifact and complete timer set. **Satisfied.** |
| H. Existing mechanism | `scripts/deployment_status.py` returned `state=COMPLETE`, `comparison_matches=true`, exit `0`. **Satisfied.** |
| I. Immutable provenance | `org.opencontainers.image.revision` and `WATCH_CLANK_SOURCE_REVISION` both equal the intended SHA, not `unknown`. **Satisfied.** |

Therefore `STD-DEPLOY-COM-001 = CONFORMS`, lifecycle `CLOSED`.

## OPS closure provenance retained

`STD-OPS-COM-003` remains `CONFORMS / CLOSED` through the M4G evidence chain:
authority-bound provenance, pre-event material reset, explicit prior/new
lineage, fail-closed delivery gating, and distinct reset/terminal records for
one execution.  `STD-OPS-COM-004` remains `CONFORMS / CLOSED` through its
grant-backed advisory lock authority and release-path evidence.  These were
regression-checked, not reimplemented or reopened.

## Live-proof chronology

1. The initial read-only proof recorded selector `watch-clank:5bc8020`, OCI
   revision `unknown`, and comparator `UNVERIFIED` / exit `2` in
   [`watch-clank-deploy-live-proof-2026-09-01.md`](watch-clank-deploy-live-proof-2026-09-01.md).
2. The separately authorized target remediation built the exact Watch SHA,
   verified provenance before deployment, applied committed additive migrations
   through `015_qualification_reset_lineage`, updated only the deploy-critical
   selector, and preserved a rollback DB copy.  No unrelated mutation,
   collector, event, or notification occurred.
3. The confirmed read-only proof observed full-SHA selector/provenance,
   schema `015`, DB integrity `ok`, 8,713 preserved watches, 22/22 timers, and
   comparator `COMPLETE` / exit `0`.

## Evidence admission and reference Clank

The smallest architecture-consistent admission is a new generated
`standards/deployment/known-evidence-index.json`.  Deployment previously had
no conformance audit, so its agent layer had no index; the UI index is
intentionally violation-only and was not repurposed.  The new index reuses the
existing fenced-audit JSON block and `superseded_by` convention and admits one
entry for `STD-DEPLOY-COM-001`, subject `watch-clank`, source
`audits/watch-clank-cross-domain-2026-09-01-final.md`, kind
`known_conformance`.  It is generated by
`tools.deployment_agent_layer.build_known_evidence_index()` and is deterministic.

The prior M4G audit remains verbatim as historical evidence and now carries a
`superseded_by` marker pointing to this final audit.  The earlier failed live
proof remains separately preserved; it is not erased or rewritten.  No frozen
standard file or tag was changed.

Watch is recorded here as the first fully wired/admitted reference Clank for
the descriptive workflow: frozen standards → applicability resolver → blind
audit → informed remediation → re-audit → live deployment proof → evidence
admission.  This is process documentation, not a new normative standard.
Reusable lessons are captured descriptively in this audit: provenance begins at
the authority boundary; downstream consumers do not invent it; material reset
precedes gated use; prior/new identities and reset/terminal facts stay
auditable; identifiers do not grant authority; and repository mechanism does
not substitute for live deployment proof.

## Verification boundary

The full Standards suite after the admission artifacts was run directly and
unpiped: `793 passed`.  No Watch source, deployment, host, database, timer,
collector, notification, or frozen standard/tag was changed in this pass.
