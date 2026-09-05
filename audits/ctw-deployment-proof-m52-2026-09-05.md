# Chinese Tech Wire — M52 DEPLOY-COM-001 live-proof admission

```json
{"clank":"chinese-tech-wire","date":"2026-09-05","findings":[{"standard":"STD-DEPLOY-COM-001","kind":"conformance","summary":"LIVE_PROOF_CONFIRMED at Chinese Tech Wire cfbd3158a5272aab6e67a2a9005be2c3a45544e6 on target NAS:/volume2/clank/chinese-tech-wire (DSM Task Scheduler hourly at :10 IST → host flock /tmp/ctw-nas-run.lock → Docker one-shot chinese-tech-wire-nas-soak → --full-once --scheduled): identity proven through a GitHub pinned-commit source tarball verified byte-identical to the canonical tree, OCI org.opencontainers.image.revision label, CTW_SOURCE_REVISION env, and --identity output all equal to cfbd315; the live DB (LEGACY_UNADOPTED under canon, NOT UNKNOWN) was promoted by the explicit operator-authorized --adopt-current-schema authority transition, scratch-proved first (mount-marker + resolved-URL targeting proof, all 21 tables row-identical, only schema_meta v1 added, indexes 41→41) then applied live with identical results; deployment pointer flipped 552ffff→cfbd315 with run.sh/scheduled-run.sh/compose byte-unchanged; authoritative natural proof is durable scheduled run id=581 (2026-09-05T02:40:04Z→02:41:18Z, SCHEDULED, SUCCESS, 13 canonical sources = 9 ok + 4 documented soft-blocks, articles+20, community+2, leads+100, alerts 0 sent/100 suppressed, 0 err/0 warn) with exact continuity (12,091→12,111 articles, 258→260 threads, +13 source_runs) and the schema_meta barrier HELD (still the single adopted row after normal canonical operation); delivery OFF, cadence/lock/mount unchanged, no rollback, dashboard NOT_DEPLOYED/NOT_APPLICABLE (no server-side GUI exists on this target)."}]}
```

This Standards-only M52 record admits `STD-DEPLOY-COM-001`
LIVE_PROOF_CONFIRMED / CLOSED at
`cfbd3158a5272aab6e67a2a9005be2c3a45544e6` for the exact target
`NAS:/volume2/clank/chinese-tech-wire` with the exact mechanism above.
Scope is exact: no generalization to Hetzner, future SHAs, Windows
surfaces, dashboard deployment, other NAS paths, or production maturity
(CTW remains a Tier B staging/soak clank with delivery deliberately OFF).
`STD-DEPLOY-COM-002` CONFORMS / CLOSED at `c340a45` (M17) is preserved,
not re-closed or re-scoped. `STD-OPS-COM-003` remains UNKNOWN;
`STD-UI-COM-007` and `STD-UI-COM-011` remain unresolved; no overall CTW
conformance is claimed.

## Authority cutover history (preserved, not rewritten)

- Hetzner (`~/staging/chinese-tech-wire`): staging checkout `9eec9f0`,
  image `9eec9f0`, cron line commented out **2026-08-27T13:46:55Z** with
  the operator's cutover note citing Diagnostic Clank incident
  `2a18c8ae-f887-4018-ae56-8b03b39141ee`; retained as documented
  rollback; its last run was id=431 SUCCESS at 2026-08-27T13:11Z.
- NAS (`/volume2/clank/chinese-tech-wire`): current host authority since
  the 2026-08-27 cutover.
- The 2026-08-19→08-27 dual-host parallel period left divergent run
  histories on the two hosts; that divergence is historical fact and was
  NOT merged. The NAS DB is the sole authority.
- The Diagnostic Clank incident record itself could not be retrieved
  (its governed desktop repo is unavailable at the documented path).
  This is historical evidence debt only; it does not block this
  admission, and nothing was fabricated to fill the gap.

## Pre-deploy NAS state

Pre-M51 live source: `552ffff` (image tag + `.deployed-id` + `.env`
IMAGE_TAG + OCI label, all equal). DB `state/ctw.db`, 28,147,712 bytes,
sha256 `63cd4b78fc35347ba9598dbf76cc9b47830c818feacc1ab77bef1d03e9f184ac`,
quick_check ok, 21 tables, `schema_meta` absent — classified
**LEGACY_UNADOPTED under canonical cfbd315** (structurally complete
pre-M17 shape, marker-less), explicitly NOT UNKNOWN.

## Privilege-path correction

M50 initially inferred Docker on the NAS required a passworded sudo. M51
established the actual pre-existing authorized path:
`(ALL) NOPASSWD: /usr/local/bin/docker`. Bare `docker` (PATH-resolved)
did not match the path-specific rule and fell through to the
password-required `(ALL) ALL` grant.
`EARLIER_INFERENCE_SUPERSEDED_BY_STRONGER_EVIDENCE`. No sudoers, group,
socket, daemon, or credential changes occurred in any mission.

## Backup

`state/backups/ctw-pre-m51-20260905T011627Z.db`, 28,147,712 bytes,
sha256 `63cd4b78…f184ac` — SHA-identical to the live DB at capture
(verified both on-host and after transfer). Prior backups (2026-08-19,
2026-08-27 ×2) untouched.

## Canonical source artifact

The NAS has no git binary. Canonical `cfbd3158a5272aab6e67a2a9005be2c3a45544e6`
was delivered as the GitHub pinned-commit source tarball (sha256
`e09fc9f081e6258e3f23c6f045e893cc39ae97d2701ed971f1fda738233e27a2`),
verified byte-identical to the canonical git tree via
`git -c core.autocrlf=false archive` comparison — the initial CRLF
difference was a Windows `core.autocrlf` archive artifact, corrected and
re-verified to TREES-IDENTICAL — and SHA-verified after transfer to the
NAS. **No git checkout on the NAS exists or is claimed.** The stale
`build/src` plain-copy tree was not used.

## Build incident (procedural evidence, not a source defect)

First image build from a `/volume2` build context produced mode-000
application files inside the image (Synology NFSv4 ACLs on the context
present as 000 through the build path) and the container failed with
`entrypoint.sh: Permission denied`. That image was **rejected and never
deployed**. The source was re-extracted to a clean `/tmp` context with
correct modes and rebuilt successfully (image id `5e7019a25f20`).

## Dependency gate

`DEPENDENCIES_COMPATIBLE`: requirements.txt diff `552ffff..cfbd315` is
empty; the change adds `requirements.lock`, which the canonical
Dockerfile consumes with `pip install --require-hashes`; no
model/entity schema changes; no host Python mutation (CTW is
containerised).

## Scratch targeting + adoption + health (distinct from the Smartphone Alembic incident)

Before any scratch mutation: the scratch bind mount was proven by a
marker file read from inside the container plus a captured resolved
`DATABASE_URL` (`sqlite:////app/data/ctw.db` mapping to
`build/scratch-m51/`), with uid/ownership aligned to the live container
contract (10001) and the live DB excluded.
`SCRATCH_TARGET_PROVEN_BEFORE_MUTATION`.

Canonical `--adopt-current-schema` on scratch:
`{"adopted": true, "state": "COMPATIBLE", "expected_schema_version": 1,
"verified_tables": 22}`, exit 0. Added exactly `schema_meta`
(version 1, source `legacy-adoption`); all 21 original tables'
row counts unchanged; indexes 41 → 41; 0 views/triggers before and
after; quick_check ok. Canonical `--health` on the adopted scratch:
healthy, COMPATIBLE, empty status_reasons — the explicit adoption
reaches the same gate canonical runtime uses.

## Final old-source checkpoint

Run id=580 (the 07:10 IST fire, `552ffff`): trigger SCHEDULED, SUCCESS,
ended 07:11:12 IST — the LAST old-source run. Not used as canonical
proof.

## Live adoption + pointer transition

After run 580 with the flock free, the explicitly operator-authorized
`--adopt-current-schema` ran against live `state/ctw.db` and **matched
scratch exactly** (schema_meta v1 / legacy-adoption added, COMPATIBLE,
quick_check ok, articles 12,091 and ingestion_runs 580 preserved,
indexes unchanged). This is the canonical explicit authority transition
— **not** an automatic migration. The pointer then moved
`552ffff → cfbd3158a5272aab6e67a2a9005be2c3a45544e6` (`.deployed-id`,
`.env`), with run.sh, scheduled-run.sh, compose, cadence, state mount,
and delivery settings byte-unchanged (hashes equal to the pre-deploy
freeze).

Identity surfaces, all resolving to `cfbd315…`: the pinned verified
source artifact, the image OCI `org.opencontainers.image.revision`
label, the `CTW_SOURCE_REVISION` env, and `--identity` output. No git
HEAD on the NAS is claimed.

## Scheduler / lock / delivery (unchanged contract)

DSM Task Scheduler hourly at :10 IST; `--full-once --scheduled`; host
lock `flock -n /tmp/ctw-nas-run.lock`; release channel `nas-soak`;
delivery OFF (`DISCORD_WEBHOOK_URL` empty); state bind mount
`state/ctw.db`; 13 active sources; no duplicate schedule; Hetzner
remained disabled throughout.

## Authoritative natural proof

Run **id=581**: trigger SCHEDULED, status SUCCESS,
2026-09-05T02:40:04Z → 02:41:18Z (~73.9s) at source `cfbd315` — the
first DSM fire after the pointer flip and the authoritative
DEPLOY-COM-001 proof. Results: articles +20, community threads +2,
leads +100, alerts sent 0 / suppressed 100, 0 errors, 0 warnings.
Exactly the canonical 13-source scope executed (benchlife, chiphell,
coolaler, expreview, hkepc, ithome, jd, jiwei, mobile01, mydrivers,
technews, xfastest, zol); ptt and geekbench are canonically DISABLED and
absent; 9 ok + 4 documented soft-blocks (xfastest/chiphell/mobile01
stream resets etc.) — documented source health, not deployment failure.

## Continuity / false novelty

articles 12,091 → 12,111 (+20 exact); community threads 258 → 260 (+2
exact); source_runs +13 (7,540 → 7,553). No replay, no identity reset,
no false-novelty flood, no history discontinuity, no source scope
expansion. The NAS DB remains the sole authority; the historical
Hetzner divergent data was not merged.

## Compatibility barrier

After normal canonical run 581, `schema_meta` remained exactly the
single adopted row `(1, '2026-09-05 01:42:24', 'legacy-adoption')` —
**BARRIER_HELD**. Normal operation did not rewrite compatibility
authority.

## Post-run state

quick_check ok; `--health` healthy with total_runs 581, last SUCCESS,
database_writable true, revision `cfbd315…`; delivery still OFF;
rollback not triggered; the old `552ffff` image retained; Hetzner still
disabled. Post-run DB sha256
`e39b65a34b2b799c497b24ed98bceeeea27d1b9b91010ff8a50ff7fba0d922d5`.

## Dashboard applicability

No server-side CTW dashboard is deployed on this target:
**DASHBOARD = NOT_DEPLOYED / NOT_APPLICABLE**. The canonical uvicorn
logging fix has no live surface at this exact target and is not a
DEPLOY-COM-001 obligation here.

## Evidence summary

Exactly one narrow CTW DEPLOY-COM-001 fact is admitted. The prior CTW
COM-002 fact, all other targets' facts, and CTW's M1 insufficiency
history remain preserved. No NAS access, deploy, adoption, task
restart, Hetzner change, source-Clank modification, or frozen
standards/tag change occurred in this Standards-only recording pass.
