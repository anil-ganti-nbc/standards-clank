---
id: pid-namespace-unsafe-stale-lock-reclaim
domain: operations
topics: [10]
confidence: STRONG
priority: HIGH
---

## Concern

A run-lock implementation that reclaims a stale lock by checking whether
the PID recorded in the lock file is still "alive" is unsound wherever
every container/process boundary can independently produce PID 1 (Docker)
or where a differently-scoped PID can be reused (Windows). This produces
two opposite failure modes: a lock that can never be reclaimed (false
"still alive" forever) or a lock reclaimed while the real owner is still
running (false "dead," e.g. killing the wrong process).

## Current terminology

See [terminology-map.md](../terminology-map.md) "Locking" table.

## Repos surveyed

watch-clank, oem-radar, feature-phone-clank, korean-tech-wire,
semiconductor-intelligence, tablet-clank, smartwatch-clank,
diagnostic-clank (NAS incident record).

## Independent evidence

Three fleet members independently discovered and fixed the *identical*
bug shape:
- oem-radar (INC-009): a crash left `{"pid": 1, ...}`; every subsequent
  hourly fire (~81 of them) concluded the old run was still alive and
  refused to start, forever.
- watch-clank (INC-006): the inverse failure — a Windows `os.kill`
  liveness check could kill a *different* process that happened to reuse
  the recorded PID.
- smartwatch-clank: pre-fix PID/hostname-based reclaim logic was "proven
  broken in Docker's one-shot `run --rm` model" (every container is PID 1
  with a random hostname).

## Inherited evidence

This is the most explicitly-lineaged cluster in the whole corpus:
- oem-radar's fix was ported wholesale from Free Game Tracker's
  `newsroom/run_lock.py`.
- feature-phone-clank's `run_lock.py` was "ported verbatim from OEM
  Radar's `core/run_lock.py`."
- smartwatch-clank's `core/lock.py` explicitly cites Diagnostic Clank
  incident `5f280abf` (the oem-radar NAS canary, INC-009) plus Free Game
  Tracker and OEM Radar by name as the design source.
- tablet-clank's Windows `OpenProcess` liveness probe "mirrors
  feature-phone-clank core/run_lock.py."

The fix (an OS-level advisory file lock — `flock`/`msvcrt.locking` —
consulting no PID or liveness state at all) is now a de facto fleet
convention, propagated by direct code-porting rather than independent
re-invention, but **not yet unified into one shared library** — each
repo still carries its own copy.

## Incidents

INC-006, INC-009 (canonical instance — see
[incident-ledger.md](../incident-ledger.md) for full detail).

## Implementations

Fixed/current-good: oem-radar, feature-phone-clank, smartwatch-clank
(all OS-level flock, no PID consulted). korean-tech-wire and
semiconductor-intelligence's locks (`RunLock`, `LeaseManager`) were not
found to have suffered this specific bug — worth checking in Pass 0B
whether they were built lock-sound from the start or simply haven't hit
the failure yet. chinese-tech-wire has **no in-process lock at all** —
protection is external only (`flock` wrapping the cron invocation).

## Counterexamples

None — no repo argues PID-liveness locking is safe; every repo that has
examined the question has moved away from it or never used it.

## Harm if violated

~81 consecutive scheduled runs silently refusing to start (oem-radar) is
functionally identical to total starvation (overlaps cluster D) for as
long as the stale lock persists — in production this could run
indefinitely with no automatic recovery. The inverse failure (killing the
wrong process) is a correctness/safety hazard, not just an availability
one.

## Likely domain

Operations.

## Unresolved questions

- Should Standards Clank standardize the *mechanism* (OS-level advisory
  lock, no PID/liveness heuristic) or only the *consequence* (a lock
  reclaim decision must never depend on a liveness check that can be
  fooled by PID-namespace reuse)? The existing fleet convention (mirror
  data-ontology's precedent) is to constrain consequence, not algorithm —
  worth checking whether that precedent should hold here too, given how
  literally-identical the actual fix code is across repos.
- Should this be unified into one shared library (e.g. via
  `clank-architecture` or `diagnostic-clank`'s `clank_runtime` package)
  rather than each repo maintaining its own copy? That's an
  implementation-consolidation question, likely out of scope for a
  Standards Clank rule itself but worth flagging for the operator.
- chinese-tech-wire and korean-tech-wire were not confirmed to have hit
  this specific bug — is their current design actually safe, or
  untested-but-exposed? Pass 0B may want to note this as an open
  verification item rather than assume safety from absence of an
  incident.
