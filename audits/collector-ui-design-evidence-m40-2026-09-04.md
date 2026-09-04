# Collector UI Design System v1 — proposal evidence and fleet gap audit — 2026-09-04

```json
{"clank":"standards-clank","date":"2026-09-04","findings":[]}
```

This is a **Standards-only proposal and audit pass** (M40). No source Clank was
modified, no deployment occurred, no frozen standard was changed, no evidence
was admitted under an unratified standard, and no ratification occurred.

## Proposal

`standards/collector-ui-design/STD-CUD-001.json` — **PROPOSED**, version 1.
Covers the shared Collector UI design system contract for the six
collector-family Clanks. Not ratified; awaits operator review.

## Reference implementation evidence

All six collector Clanks carry a **byte-identical** `collector_ui.py` design
system module (SHA-256 `aaa38c12…`, 423 lines, `DESIGN_SYSTEM_VERSION =
"collector-ui-v1"`), pinned by per-Clank test suites
(`tests/test_collector_ui_design_system.py`). The only visual token a Clank
overrides is its accent (--accent, --accent-soft). Navigation grammar, table
treatment, empty-state helper, badge text-carrying guarantee, shell structure,
and footer identity surface are shared.

| Target | Current SHA | Shared module | Accent override | Design tests |
| --- | --- | --- | --- | --- |
| smartphone-clank | e514c45 | dashboard/collector_ui.py | #4c8dff / #16283f | tests/test_collector_ui_design_system.py |
| smartwatch-clank | cc80aaf | src/smartwatch_clank/collector_ui.py | (per-Clank accent) | tests/test_collector_ui_design_system.py |
| feature-phone-clank | bbd2845 | src/feature_phone_clank/collector_ui.py | (per-Clank accent) | tests/test_collector_ui_design_system.py |
| tablet-clank | 2b1ba6e | native/macos/collector_ui.py | (per-Clank accent) | tests/test_collector_ui_design_system.py |
| watch-clank | 4d0413c | app/collector_ui.py | (per-Clank accent) | tests/test_collector_ui_design_system.py |
| oem-radar | 070914c | src/oem_radar/dashboard/collector_ui.py | (per-Clank accent) | tests/test_collector_ui_design_system.py |

## Normative / reference / domain / incidental classification

**NORMATIVE (MUST):** byte-identical shared module; DESIGN_SYSTEM_VERSION
match; status text-carrying guarantee; full Clank identity in the shell;
meaningful empty states (never bare "Empty"); accent-only per-Clank override;
prohibited Phase-0 scaffold / generic-only branding / bare "Empty" /
colour-only status / dead navigation; desktop-first layout usable at
1080p/1440p; consistent navigation grammar for equivalent concepts.

**REFERENCE PATTERN (informative):** specific spacing scale values (s1–s7);
specific font stack; specific responsive breakpoint (1000px); KPI grid
sizing; sticky-header opt-in pattern; specific hover/transition effects.

**DOMAIN-SPECIFIC (per-Clank):** accent colour choice; navigation items;
panel content and layout; empty-state wording; which collectors are
production vs experimental; delivery surface presence.

**INCIDENTAL (non-normative):** CSS selector names; pseudo-element
implementation; specific transition curves; component helper function
signatures.

## Fleet Standards gap audit

### DEPLOY-COM-001 live-proof matrix

| Target | Status | Evidence |
| --- | --- | --- |
| watch-clank | LIVE_PROOF_CONFIRMED | audits/watch-clank-deploy-live-proof-2026-09-01-confirmed.md |
| smartwatch-clank | LIVE_PROOF_CONFIRMED | audits/smartwatch-deployment-proof-m22-2026-09-02.md |
| feature-phone-clank | LIVE_PROOF_CONFIRMED | audits/feature-phone-deployment-proof-m25-2026-09-02.md |
| tablet-clank | LIVE_PROOF_CONFIRMED | audits/tablet-deployment-proof-m28-2026-09-03.md |
| korean-tech-wire | LIVE_PROOF_CONFIRMED | audits/ktw-deployment-proof-m22-2026-09-04.md |
| oem-radar | UNRESOLVED | — |
| semiconductor-intelligence | UNRESOLVED | — |
| chinese-tech-wire | UNRESOLVED | — |
| smartphone-clank | UNRESOLVED | — |

### DEPLOY-COM-002 compatibility matrix

All eight SQLite-family targets CLOSED: Semiconductor (M11), KTW (M12),
Tablet (M13), Feature Phone (M14), OEM Radar (M15), Smartwatch (M18),
CTW (M17). Watch is not SQLite-family.

### Source drift against admitted exact-SHA evidence

The six collector Clanks moved after M36 due to the visual overhaul and
post-overhaul cleanup:

| Target | M36-admitted SHA | Current SHA | Drift |
| --- | --- | --- | --- |
| watch-clank | 386568ce | 4d0413c1 | MOVED (visual overhaul + benchmark reconciliation + delivery receipts) |
| oem-radar | b9f76a48 | 070914c8 | MOVED (visual overhaul + timezone convention + delivery granularity) |
| semiconductor | 53cb3f1f | 53cb3f1f | UNCHANGED |
| chinese-tech-wire | 24c0b797 | 24c0b797 | UNCHANGED |
| korean-tech-wire | f49bd02e | f49bd02e | UNCHANGED (since M22-KTW proof) |
| feature-phone | a608d847 | bbd28450 | MOVED (visual overhaul + COM-009 fix) |
| smartphone | 5684cf2c | e514c45d | MOVED (visual overhaul + collection invariant tests) |
| smartwatch | a4e08e90 | cc80aaf2 | MOVED (visual overhaul + garmin relay) |
| tablet | b3088ebc | 2b1ba6ec | MOVED (QC archive adoption path + visual overhaul) |

**Impact on M36-admitted UI evidence:** the six collector-family targets'
M36 facts are exact-SHA-scoped and now stale. The visual overhaul was
specifically implementing the UI standards (not regressing them), and each
target's per-Clank suite ran green at the new SHA. However, a superseding
evidence pass is needed to re-admit the facts at the new SHAs.

**Impact on COM-002 compatibility facts:** none of the six collector targets'
COM-002 facts are invalidated — the visual overhaul was additive (new
collector_ui.py + test file) and did not modify the compatibility barrier or
the persistent-state machinery closed by M11–M18.

**Non-UI facts:** Semiconductor's M11/M6 facts are unaffected (source
unchanged). CTW's M17 facts are unaffected (source unchanged). KTW's M22
COM-001 proof and M12 COM-002 facts are unaffected (source unchanged since
the proof).

### Remaining unresolved findings

- STD-DEPLOY-COM-001: OEM Radar, Semiconductor, CTW, Smartphone (4 remaining)
- STD-DEPLOY-COM-002: none remaining (all closed)
- STD-UI-COM-011: Smartphone (feature-phone has a recorded boundary; smartwatch
  structurally N/A; KTW/CTW/Semiconductor/OEM Radar/Tablet resolved or N/A)
- STD-UI-COM-007: Smartphone (M1 insufficiency, unresolved)
- STD-OPS-COM-003: CTW (UNKNOWN — resolver trigger fact not established)
- Semiconductor red-CI caveat (NON-UI, unrelated to any standard)
- Smartwatch dcrainmaker test staleness (NON-UI, pre-existing)
