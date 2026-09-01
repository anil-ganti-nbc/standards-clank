# watch-clank — M4C qualification timing re-audit

```json
{"clank":"watch-clank","date":"2026-09-01","findings":[]}
```

Read-only re-audit of Watch `f78575a903d64c75bcee62cb81cbe9e70f3f9db7`
against Standards `aa9b58c53e94a0d5db6dc009f0ac4ada53566cdb`. Both working
trees were clean. No Watch source, deployment, host, frozen standard or tag,
or known-evidence index was changed.

## Result

| State | Count |
|---|---:|
| CONFORMS | 23 |
| NON_CONFORMING | 1 |
| INSUFFICIENT_EVIDENCE | 1 |

All 25 resolver standards remain applicable. The 22 pre-existing conforming
standards still conform; OPS-COM-004 still conforms. DEPLOY-COM-001 remains
`LIVE_PROOF_PENDING`: no host observation was authorized.

## OPS-COM-003 — still open

M4B supplies useful structural evidence: execution records include execution
identity, material identity, outcome and caller provenance; migration 014
preserves old rows while relabelling unproven legacy NATURAL provenance to
UNKNOWN; and each pipeline entry point calls the material reset before
collector/event processing. The focused Watch check passed (`8 passed`).

But `QualificationService.delivery_allowed()` remains the real external-
delivery boundary and, when no evidence exists, creates a new record with
`provenance="NATURAL"`. That is provenance fabricated downstream rather than
provenance supplied by the execution path. Its direct regression still asserts
that behaviour. Thus required implementation check G is **NO** only if no
fabrication occurs; the source proves G is **YES**. In addition, the reset row
holds only the new material identity; it does not retain an explicit previous
identity field on the reset record. These are essential qualification-contract
gaps, so OPS-COM-003 cannot be closed.

## Recommendation

**DO NOT ADMIT — GAPS REMAIN.** Do not modify the known-evidence index. The
next action is one bounded Watch correction: eliminate delivery-side NATURAL
creation and carry both prior and new material identities in the reset record,
with a real-path regression. Then re-audit. Host observation remains a
separate authorization prerequisite for DEPLOY-COM-001.
