---
id: stale-duplicate-automation-surviving-migration
domain: operations
topics: [9]
confidence: STRONG
priority: HIGH
---

## Concern

An old scheduling/automation mechanism (a cron entry, a systemd timer, a
Task Scheduler task) survives a migration to its replacement and keeps
firing — invisibly, redundantly, or destructively — because nobody
located and disabled it as part of the migration. This is distinct from
cluster A (scheduler-fired ≠ outcome-recorded): this cluster is about
*forgotten or duplicate* automation specifically, not about verifying a
single automation's own truth.

## Current terminology

No shared vocabulary. `clank-architecture`'s Golden Incident Corpus uses
"ZOMBIE-AUTHORITY" and "AUTHORITY-BYPASS" as named incident classes.

## Repos surveyed

watch-clank, smartphone-clank, smartwatch-clank, `clank-architecture`,
`diagnostic-clank` (fleet.yaml + NAS incidents).

## Independent evidence

- watch-clank (INC-002): a stale pre-migration cron launcher fired
  invisibly in parallel with the new systemd-timer architecture for
  days; root cause explicitly stated as "migration built and verified
  the new architecture but never located and disabled the old cron entry
  it was replacing" — and explicitly noted as *not unique to Watch
  Clank*, citing smartphone-clank's prior identical fix.
- smartphone-clank (INC-015): a stale PID file meant a health-check job
  could spawn a duplicate daemon without detecting the still-running
  original — two daemon process groups found running concurrently
  against the same production DB.
- smartwatch-clank (INC-035): a type collapsed "collector tier" and
  "invocation scope," so a new experimental soak timer began silently
  re-running four production-tier collectors on its own independent
  cadence, in addition to their real production cron — same collectors,
  two live schedules, discovered only because the new timer's existence
  exposed the pre-existing latent bug.
- feature-phone-clank: **preventive, not incident-evidenced** — cron
  entries deliberately placed under a different OS user than production
  specifically so an experimental schedule is "physically incapable" of
  colliding with production's; explicit anticipation of this exact risk
  class.

## Inherited evidence

`clank-architecture/conformance/GOLDEN_INCIDENTS.md` registers this as a
named, CI-tracked incident class: "ZOMBIE-AUTHORITY | disabled timer
still fires | Smartwatch fleet snapshot" and "AUTHORITY-BYPASS | cron
bypasses registered scheduler | SemInt fleet snapshot." `FLEET_LAWS.md`
Law 5 (single-scheduler-authority, referenced but not read in full this
pass) lists violators: "smartwatch dual-lane (cron kept, systemd
retired)." `diagnostic-clank/fleet.yaml` independently records a live
instance: `smartwatch-hetzner-soak-timer-retired` — a systemd timer that
fired every cycle and failed every time until discovered and disabled
during a Phase 2A repair, with an explicit guard note against
re-enabling it while a cron lane still exists.

## Incidents

INC-002, INC-015, INC-035, plus `fleet.yaml`'s
`smartwatch-hetzner-soak-timer-retired` entry (same underlying repo as
INC-035, a related but distinct occurrence — a *failing*, not merely
*duplicate*, timer left unnoticed).

## Implementations

The only clean preventive design found (as opposed to reactive fix) is
feature-phone-clank's cross-user cron isolation. Every other instance in
this cluster is a fix applied *after* the stale/duplicate automation was
discovered, sometimes by accident (smartwatch-clank's duplicate schedule
was only exposed because a second, unrelated timer's rollout made the
pre-existing bug visible).

## Counterexamples

None.

## Harm if violated

Ranges from wasted duplicate work (smartwatch-clank, "nothing corrupted
because both schedules shared one lock") to a genuinely invisible
multi-day parallel execution (watch-clank, INC-002) to concurrent writers
against the same production DB (smartphone-clank, INC-015). The
"nothing corrupted only because X happened to also be true" pattern
recurs across multiple incidents in this cluster — the harm was avoided
by luck/an unrelated safeguard as often as by design.

## Likely domain

Operations.

## Unresolved questions

- Should a standard require an explicit "old automation decommission"
  step as part of any migration to a new scheduling mechanism (a
  positive checklist item), or is the more general "single scheduler
  authority per lane" consequence (already named as `clank-architecture`
  Fleet Law 5) the right level to standardize at?
- This cluster overlaps meaningfully with cluster A (scheduler-truth) —
  should Pass 0B consider merging them, or does the "forgotten/duplicate"
  framing warrant staying separate given the distinct remediation shape
  (decommissioning discipline vs. execution-truth verification)?
