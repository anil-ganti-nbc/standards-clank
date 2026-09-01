# OEM Radar — M9 `STD-OPS-COM-003` applicability checkpoint

```json
{
  "clank": "oem-radar",
  "date": "2026-09-01",
  "findings": [
    {
      "standard": "STD-OPS-COM-003",
      "kind": "not_applicable",
      "summary": "NOT_APPLICABLE: OEM Radar is a stateless one-shot telemetry system with durable crawler-run history but no promotion/soak qualification lifecycle or reusable qualification gate. This checkpoint records applicability only; it admits no conformance evidence and performs no remediation."
    }
  ]
}
```

## Scope and decision

This is a read-only applicability checkpoint against frozen Operations
Standards at `d65e67a5fa4e48f788220596408ee867ffa52f36`. The canonical OEM
Radar `main` and `origin/main` revision is
`d720e0635894ddcc9a39f116e2aa4a1768090042`; its working tree was clean. No
OEM Radar source, database, scheduler, deployment, host, resolver, frozen
standard, tag, or known-evidence index was changed.

The decision is **`NOT_APPLICABLE`** for `STD-OPS-COM-003`. The standard is
scoped to a Clank that uses reusable soak/promotion evidence to justify a
production decision. OEM Radar's actual workflow is stateless one-shot
collection and telemetry, not qualification. Its README explicitly keeps
production promotion frozen/unverified and describes `oem-radar run` as a
one-shot CLI invoked by an external scheduler; that posture is not an
application-level qualification gate.

## Execution model

The normal path is:

`OS scheduler (systemd/cron/Task Scheduler) or explicit CLI/dashboard action
→ execute_crawl → run_all → run_started → run_source → run_finished → notifier.drain`.

Systemd and cron examples invoke the same one-shot command. The dashboard's
`CrawlController` uses the same `execute_crawl` assembly and keeps `trigger`
(`auto` or `manual`) only in an in-memory status snapshot; it is not passed to
`run_all` or persisted in `crawler_runs`. The run lock serializes concurrent
work but is not a qualification authority.

Each source execution does have a durable integer `crawler_runs.id`, with
start/finish timestamps, terminal status, statistics, and related `run_errors`.
The database also persists snapshots, change events, notifications, evidence
observations, and source-health calculations. These records support run
telemetry, catalog diffs, alerting, and dashboard history.

## Why the persisted state is not OPS-COM-003 evidence

`source_due`, `has_completed_run`, and the pipeline's prior-successful-run
health baseline consume telemetry to decide whether a source is due or how a
collection behaved. They do not establish a maturity state, count a soak
window, or authorize a promotion decision. Product/content hashes identify
observed catalog state; they are not release/configuration material identity.

The SQLite `crawler_runs` schema has no trigger/provenance, material-identity,
qualification-epoch, reset, or gate-agreement fields. No downstream path reads
prior qualification evidence because no such evidence or gate exists. The
separate Evidence Fusion documentation explicitly says that an evidence
promotion path and delivery rule have not been built. The documented Epoch 1 /
Epoch 2 database archive/reset procedure is operational data-lifecycle
bookkeeping; it explicitly has no `epoch` column and is not a qualification
epoch. Likewise, the plugin guide's manual `CANARY` → `LIVE_VALIDATED` wording
is editorial/source rollout policy, not a soak gate for `STD-OPS-COM-003`.

Therefore there is no stale reusable qualification evidence for a material
code/config/source change to invalidate, no qualification reset boundary to
trace, and no trusted downstream provenance that could be fabricated. Adding
qualification tables, epochs, or reset logic would create a new lifecycle and
governance obligation rather than repair an existing OEM Radar defect.

The real governed behavior is telemetry and output/run health, which belongs
in the Operations invocation/health territory of `STD-OPS-COM-001` and
`STD-OPS-COM-002`; this checkpoint does not re-audit or admit either standard.

## Resolver trigger-fact finding

`tools/fleet_standards_resolver.py` maps `STD-OPS-COM-003` to the
`has_promotion_soak` fact. OEM Radar's `profiles/fleet-adoption.json` entry
has an empty `facts` object and cites only the generic `sku-based` profile.
The M1 sweep therefore retained the target as unresolved/insufficient rather
than treating a missing fact as `FALSE`; its raw resolver counts were
`APPLIES: 1`, `NOT_APPLICABLE: 2`, `UNKNOWN: 22`. The source inspection in
this checkpoint supplies the missing semantic fact: no promotion/soak
lifecycle exists. This is a target applicability-record correction to make in
a separately authorized Standards recording pass, not a resolver redesign or
an implementation defect in OEM Radar.

## Guarded outcome

- Final verdict: **`NOT_APPLICABLE`**.
- Remediation required: **No**; do not begin an M10 qualification pass.
- No conformance or non-conformance evidence is admitted. The
  `not_applicable` finding is intentionally ignored by the generated
  Operations known-evidence index.
- No target tests or collectors were run; this pass is source inspection only.
- The paired JSON record contains the complete machine-readable trace. A
  narrow Standards guard was added and the full Standards suite was run
  directly/unpiped after the artifacts were created: **834 passed, 0 skipped,
  0 failed, exit 0**.

The next action is a separately authorized Standards-only recording pass to
correct OEM Radar's applicability record to `NOT_APPLICABLE`, followed by the
remaining independent deployment/compatibility audit work. No qualification
remediation, compatibility remediation, or deployment live proof starts from
this checkpoint.
