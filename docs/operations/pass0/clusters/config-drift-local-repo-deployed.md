---
id: config-drift-local-repo-deployed
domain: operations
topics: [7]
confidence: STRONG
priority: HIGH
---

## Concern

Configuration that exists in three potentially-divergent places — a
local/operator edit, the committed repository state, and what's actually
deployed on a remote host — drifts, and the drift is usually discovered
by accident (a cross-check performed for an unrelated reason) rather than
by a systematic gate.

## Current terminology

No shared vocabulary. Each incident below is described in the surveying
repo's own terms.

## Repos surveyed

smartphone-clank, oem-radar, chinese-tech-wire, korean-tech-wire,
smartwatch-clank, tablet-clank, semiconductor-intelligence,
`diagnostic-clank` (both sources), `clank-architecture`.

## Independent evidence

- smartphone-clank (INC-014): repo-committed config shipped with
  collectors `enabled: true` while a local-only edit had disabled them;
  the repo state was never permanently flipped, so extracting/re-cloning
  would silently restore the enabled state. Root-caused, fixed via a
  scope gate independent of the enabled flag.
- oem-radar: DB backups silently inherited WAL journal-mode state,
  breaking read-only restores (INC-011) — a narrower, mechanism-specific
  drift instance.
- chinese-tech-wire: self-flagged, *accepted* drift vector — a version
  constant duplicated across two files rather than imported, "documented
  as needing to stay in sync... flagged rather than silently risking
  drift." Also: the Windows dev-machine production checkout deliberately
  never receives GitHub changes, by explicit policy, creating permanent,
  intentional divergence from Hetzner.
- korean-tech-wire: a documented example config
  (`config.example.yaml`) and the actual local config
  (`config.local.yaml`) were found, by direct diff during this survey,
  to have already diverged (a documented key entirely missing from the
  local file) — no incident narrative attached; this is live,
  undetected drift discovered by the survey itself.
- smartwatch-clank (INC-034): two independently-maintained deploy
  wrapper scripts (one tracked, one initially untracked) had to be
  manually kept in sync for one environment variable and drifted,
  silently disabling a proxy in production.
- tablet-clank (INC-031): Hetzner's live deployment ran a stale
  three-source allowlist while the repository already reflected a
  four-source allowlist — an ongoing, acknowledged drift at time of
  survey.
- semiconductor-intelligence (INC-025): a disposable smoke-test run
  overwrote a config file also read by production, silently redirecting
  a populated database checkpoint at an empty smoke database.
- diagnostic-clank (NAS): a registry DB filename had drifted from the
  live-verified inner name, caught only because two independent sources
  happened to be cross-checked during an unrelated pass
  (`CTW_ONBOARDING_DOGFOOD.md`).

## Inherited evidence

`clank-architecture/docs/FLEET_INVENTORY.md`: "An exact `source_sha`
means only that the repository head was inspected. It is not evidence
that the commit is deployed" — a fleet-level articulation of exactly this
gap, informing the design of `operations/phase0`'s deployment-truth
placeholders (see cluster I, which overlaps significantly with this one
on the deployed-vs-claimed axis specifically).

## Incidents

INC-011, INC-014, INC-025, INC-031, INC-034, plus the korean-tech-wire
and diagnostic-clank/NAS drift instances discovered directly by this
survey (not previously incident-logged anywhere).

## Implementations

No repo was found with a systematic, automated config-drift detector
covering all three layers (local/repo/deployed) at once. Every example
found is either a point fix for one specific drift instance, or an
accepted/documented tradeoff (chinese-tech-wire's intentional
dev-machine/GitHub split).

## Counterexamples

None disputing the concern; several repos treat *some* drift as
acceptable by explicit policy (chinese-tech-wire's dev-machine
checkout), which is a legitimate design choice, not a counterexample to
the general risk.

## Harm if violated

Ranges from silent production config reverting to a wrong default
(INC-014) to a production feature silently disabled (INC-034) to total
loss of a populated database's apparent contents (INC-025, though
recovered). This cluster's evidence is unusually broad (8 of 9 fleet
Clanks plus diagnostic-clank all show at least one instance) — among the
best-evidenced concerns in the corpus by repo-count, even though no
single incident here was catastrophic.

## Likely domain

Operations.

## Unresolved questions

- Given how many *different* specific drift mechanisms were found
  (config files, deploy wrapper scripts, DB filenames, WAL headers,
  allowlists), is there a single standardizable consequence here (e.g.
  "a value duplicated across more than one file/host must have an
  explicit, checked synchronization mechanism, not a comment promising
  to keep it in sync"), or does this cluster actually decompose into
  several narrower, more specific rules?
- korean-tech-wire's example/local config drift was found only by this
  survey, not previously known to the operator — should Pass 0B flag
  this as a live finding worth remediating regardless of whether it
  becomes a standard?
