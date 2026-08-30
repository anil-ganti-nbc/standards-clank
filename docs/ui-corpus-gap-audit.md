# Final UI Corpus Gap Audit — 2026-08-31

Audit question (the only question): **is any ESSENTIAL operator-facing
contract missing from the current 15-rule UI corpus?**

Audited against: standards-clank `25e6044`; nine Clank repositories at the
origin HEADs listed below (identical to the HEADs surveyed in Pass 3
earlier the same day, so the Pass 3 file:line evidence is current and is
reused here; incremental checks in this audit re-verified HEADs and probed
the two investigation areas Pass 3 had not covered).

## 1. Corpus coverage map (15 ratified rules by concern)

| Concern | Rules |
|---|---|
| Mutation / authority | COM-001 (GUI never triggers collection), COM-002 (QC decision write contract: atomic, provenance, race-guarded, truthful commit) |
| Review / QC | COM-002, COM-003 (decided items leave the queue), COM-004 (QC history surface), NEWS-001 (DUPLICATE as news fourth action), SKU-001 (availability-negative kept distinct) |
| History | COM-004 |
| Promotion / maturity | COM-005 (explicit out-of-band promotion only) |
| Bulk execution | COM-006 (bulk run excludes non-production) |
| Manual control lifecycle | COM-007 (controls follow and expose lifecycle policy) |
| Source health / coverage | COM-008 (distinct, separately-labeled dimensions) |
| Run observability | COM-009 (per-run stage detail reachable; no collapsing) |
| Time semantics | COM-010 (role + zone unambiguous) |
| Delivery | COM-011 (per-item/channel outcomes incl. suppressed/failed distinct from never-eligible) |
| Overview / implied health | COM-012 (primary surface must not imply unmeasured health) |
| News-family semantics | NEWS-001 (vocabulary), NEWS-002 (live queue reachability) |
| SKU-family semantics | SKU-001 (availability-negative disposition) |
| Cross-cutting | Constitution J (specialist flexibility / trigger-scoping), governance (no self-ratification, exceptions doctrine) |

Gaps were identified only after this map. The map's deliberate shape:
the corpus governs **mutation authority, review semantics, observability,
and family vocabularies** — it does not (and should not) govern visual
design, framework choice, or product features.

## 2. Survey scope

All nine fleet repos, read-only, at origin HEAD (re-verified during this
audit): watch-clank `fbf228f`, smartphone-clank `5684cf2`, oem-radar
`9546465` (experimental/japan-mini-pc-hetzner-soak), chinese-tech-wire
`1a47220`, korean-tech-wire `afb4aad`, semiconductor-intelligence
`8a356a3`, smartwatch-clank `08a23f9`, tablet-clank `41282f7`,
feature-phone-clank `4051b64`. Evidence base: the Pass 3 nine-repo survey
(same HEADs, file:line-cited), the watch-clank and smartphone-clank
conformance audits, plus supplemental probes for alert acknowledgment and
retry concepts.

## 3. Investigation areas and dispositions

Every area from the investigation prompt, with its outcome:

| # | Area | Findings | Disposition |
|---|---|---|---|
| 1 | Alert severity / acknowledgment | ctw "Alerts" nav item is alert *performance* reporting, not acknowledgment; alert acknowledgment in the fleet IS the QC review contract (oem-radar's alert review queue with QC archive, watch's EventReview, fp's QC decisions) | COVERED (COM-002/003/004) |
| 2 | Blocked / degraded source visibility | Universal: ctw SourceRun statuses, ktw HEALTHY/STALE/BLOCKED, semi sourceHealthLabels, oem health chips, tablet HEALTH_CLASS, fp health metrics, smartwatch/watch health cards | COVERED (COM-008) |
| 3 | Stale data / freshness | Real, incident-backed distinction (discovery novelty ≠ editorial freshness; EPOCH1_FRESHNESS incident) — but it lives in data/pipeline semantics, not UI presentation | REHOME → DATA/ONTOLOGY |
| 4 | Baselining vs novelty | Epochs/baseline machinery (watch, smartphone, feature-phone, tablet); "baseline is not news" doctrine; same incident family | REHOME → DATA/ONTOLOGY |
| 5 | Evidence reachability | Universal independent practice: watch evidence pages, smartphone dossier evidence + export, oem-radar evidence pages, semi Claims & Evidence. No failure evidence; absence-risk speculative | REJECTED (recorded observation) |
| 6 | Destructive actions | No fleet dashboard exposes destructive actions (refusals are fail-closed: oem `auto_crawl_on_start` Fleet Law 5, smartphone read-only posture); destruction lives in CLI/ops with its own guards | REJECTED (no UI surface; no evidence) |
| 7 | Retry semantics | Transport-internal (delivery.py retry/backoff; CollectorRun.retries) or run-level; visible through COM-009 run records | COVERED (COM-009) |
| 8 | Partial success | Status vocabularies include PARTIAL/DEGRADED/ZERO_ITEMS across watch, smartphone, tablet, oem-radar; surfaced via COM-009 surfaces and health factors | COVERED (COM-009) |
| 9 | Source identity / region | Per-config truth (oem-radar), region fields — data/ontology, product-specific | REJECTED (implementation/product detail) |
| 10 | Configuration drift | fp `config_drift` maintenance alert, watch maintenance channel — visibility exists ad hoc; drift is an ops concern | REHOME → OPERATIONS |
| 11 | Scheduler state | watch scheduler page (derived + live schtasks views), semi "Automation & Health" with explicit degraded-automation check, ctw scheduled tasks — real visibility, no documented operator harm from its absence | REHOME → OPERATIONS |
| 12 | Suppression reasons | Strongly covered: COM-011 acceptance 2 requires suppressed distinguishable from never-eligible; watch records `editorial_eligibility_reasons`/deprioritization reasons visible via opt-in + history (COM-004); smartphone persists suppression with evidence; fp/korean badge suppression at controls. "No silent candidate death" remains architectural doctrine — per prior operator guidance it is deliberately NOT a fabricated UI rule | COVERED (COM-011, COM-004) |
| 13 | Data-confidence presentation | Universal practice (confidence values + derivations; smartphone ledger drift check, watch confidence_label/completeness). No harm evidence | REJECTED (recorded observation) |
| 14 | Maintenance / mothball state | fp `MOTHBALLED`, tablet retired badge, ctw disabled sources ("Disabled Geekbench is not a failure"), watch disabled legacy collectors | COVERED (COM-005 maturity + COM-008 disabled/quiet states) |
| 15 | Unknown / unavailable state | A real, semi-independent "honest unknown" pattern: smartphone/watch release-state "unknown — not inferred from novelty", oem-radar's UNKNOWN non-transition doctrine, tablet's MANUAL_UNDATED ("a human ingested this without dating it"), ktw UNKNOWN health state. But it is fundamentally a never-invent DATA/ONTOLOGY invariant; its UI slice is partially covered by COM-008 (quiet ≠ unhealthy) and COM-010 (ambiguous time), and no UI-presentation failure was found | REHOME → DATA/ONTOLOGY (strongest future candidate) |
| 16 | Manual overrides | COM-007 (visibility at control) + COM-006 (bulk exclusions/overrides) | COVERED (COM-006/007) |
| 17 | Cross-Clank handoff | Motherclank ingests analyst_actions/QC rows read-only; consumption visibility does not exist in any UI and no harm evidence — inter-Clank architecture territory | PRODUCT BACKLOG |

## 4. Rejected candidates

| Candidate | Why rejected |
|---|---|
| Alert acknowledgment standard | Acknowledgment IS the QC review contract (COM-002/003/004) wherever queues exist; severity reporting is reporting, with no harm evidence |
| Evidence-reachability standard | Four independent implementations already surface evidence chains, but zero documented operator harm from absence — convergence alone is "several dashboards happen to show this" |
| Data-confidence presentation standard | Universal practice, no failure evidence; smartphone's ledger-drift check is a specialist surface to preserve, not a fleet minimum |
| Destructive-action confirmation standard | No dashboard exposes destructive actions; the concern lives in CLI/ops guardrails |
| Retry / partial-success standard | COM-009 already expresses both (status enums incl. PARTIAL; stage-attributable counters) |
| Suppression-reason standard | COM-011 acceptance 2 and COM-004 already require and enable exactly this; elevating "no silent candidate death" to a rule was explicitly reserved to the operator |
| Source identity / region standard | Product/implementation detail; no semantic gap |

## 5. Domain-rehome candidates (explicitly non-UI)

| Candidate concern | Target domain | Evidence strength |
|---|---|---|
| Discovery-novelty vs editorial-freshness; baselining vs novelty | DATA / ONTOLOGY STANDARD | Incident-backed (EPOCH1_FRESHNESS; smartphone catalogue-pollution doctrine) |
| Honest-unknown / never-invent state preservation | DATA / ONTOLOGY STANDARD | ≥4 independent implementations; no incident |
| Scheduler / automation visibility | OPERATIONS STANDARD | Moderate; semi's degraded-automation check is the strongest artifact |
| Configuration-drift visibility | OPERATIONS STANDARD | Moderate; fp maintenance alerts |

## 6. Surviving UI-standard candidates

**None.** No candidate satisfied the §8 threshold (≥2 independent
evidence lines or an exceptional incident/safety invariant) *and* passed
the overlap test against the existing corpus.

## 7. Special note: watch-clank COM-007 consequence

Watch-clank's unlabeled RUN NOW maturity context (ratification-created
backlog from decisions/0008) is proof that COM-007 has real consequences —
it is **not** evidence of a missing standard. COM-007 covers it.

## 8. Final conclusion

**A. NO ESSENTIAL UI CONTRACT MISSING.**

The 15-rule corpus covers every operator-facing concern for which the
fleet shows concrete, independently-supported need. The investigated
out-of-corpus areas either fall under existing rules, lack operator-harm
evidence, or belong to other standards domains (recorded above as rehome
candidates). Per the audit's own standard: a mature corpus stops growing.
No Pass 4 is recommended, and nothing here justifies reopening any
settled rule.
