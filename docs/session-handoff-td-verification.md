# Session handoff — TD-source verification pass (2026-05-22)

**One-line summary:** Five plan docs covering all 9 fully-separated STRUCT_TDxxxx buildings. Zero code shipped. Pick any cargo to start implementation when back at the test rig.

---

## What this session produced

| Doc | Buildings | Type | Smallest cargo |
|---|---|---|---|
| `docs/td-tier1-verification.md` | TDNUKE, TDNUK2, TDPYLE, TDSILO | Verification | 4-line rules.ini (Sight stats + TDSILO Strength) |
| `docs/td-obli-verification.md` | TDOBLI | Verification | C1+C2 charge timing fix (~10 lines `building.cpp`) |
| `docs/td-gtwr-gun-verification.md` | TDGTWR, TDGUN | Verification | T7+T8 — `[TDAPDS]` projectile port (~5 min, zero behavior change) |
| `docs/td-atwr-deep-dive.md` | TDATWR | Deep dive | M1 flag fix in `ClassTdAtwr` |
| `docs/td-sam-deep-dive.md` | TDSAM | Deep dive | Full 8-step port (M1-M8); biggest scope |

---

## Cargo priority — smallest payoff first

1. **TDGUN projectile rename** (`td-gtwr-gun-verification.md` T7+T8). Create `[TDAPDS]` section (one line: `Image=120mm`), rebind `[TDTurretGun] Projectile=TDAPDS`. **Zero behavioral change.** ~5 min.

2. **Tier 1 stat corrections** (`td-tier1-verification.md` rules.ini block). 4-line diff: `[TDNUKE] Sight=2`, `[TDNUK2] Sight=2`, `[TDPYLE] Sight=3`, `[TDSILO] Strength=150`. Pure data. ~5 min + sight smoke test.

3. **TDOBLI charge timing** (`td-obli-verification.md` C1+C2). Per-building `Set_Rate` and `charge_complete_stage` dispatch at `building.cpp:6116-6128`. **5× balance fix** — Obelisk goes from 0.8s charge to TD's 4s. ~10 min + smoke test.

4. **TDATWR flag fix** (`td-atwr-deep-dive.md` M1). Four constructor args in `ClassTdAtwr`: `IsTurretEquipped=false`, `IsSimpleDamage=true`, `VerticalOffset=0x30`, `PrimaryOffset=0x40`, `DIR_N`. **Biggest visible bug fix** — resolves frozen visual + delayed firing + wrong muzzle. ~15 min + smoke test.

5. **TDPYLE engine dispatches** (`td-tier1-verification.md` E1+E2). Add `STRUCT_TDPYLE` to `Exit_Object` switch (building.cpp:2297) and `Crew_Type` switch (building.cpp:5423). Fixes infantry exit pathfinding + death-crew spawn. ~10 min + smoke test.

6. **TDSILO fill render** (`td-tier1-verification.md` E3). Extend `Shape_Number` STRUCT_STORAGE branch to `|| STRUCT_TDSILO` at building.cpp:712. TD-iconic empty→full visual feedback. ~5 min + smoke test.

7. **TDGTWR weapon port** (`td-gtwr-gun-verification.md` T1-T6). `[TDChainGun]` + `[TDSpreadfire]` + `VOC_TD_MINI` audio entry + `VerticalOffset=0x30` + rebind `[TDGTWR] Primary=TDChainGun`. **Measurable combat-output change** (TD-authentic 25 dmg vs current Vulcan-leaked 40). ~30 min + smoke test.

8. **TDSAM full port** (`td-sam-deep-dive.md` M1-M8). Biggest scope: dedicated `TdSamState` enum, port TD's 8-state Mission_Attack verbatim, Status-aware Shape_Number, `[TDNike]` + `[TDPatriot]` weapon/projectile, de-aliasing pass. **3-6 hours** + MP smoke (needs 2-Deck Tailscale setup).

Cargo 1-6 are independent of TDSAM and of each other — any order. Cargo 7 doesn't touch the engine, only rules.ini + audio.cpp. Cargo 8 is its own world.

---

## Open verifications during implementation

Things flagged in the docs that need a 5-minute lookup *when porting*, not as separate research tasks:

- **TDOblsLaser Speed=255** — confirm matches `MPH_LIGHT_SPEED`. Cross-check against existing RA laser-speed weapons.
- **TDTurretGun Speed=40** — confirm matches `MPH_VERY_FAST` per TD's `BULLET_APDS`. Likely no-op; verify via RA's `[90mm]` or similar fast-tank weapon.
- **`[TDLaser] Verses=100%,100%,100%,100%,100%`** — cross-check against TD `const.cpp` `Warheads[WARHEAD_LASER]` armor modifier table. May need updating.
- **TDSAM `[TDPatriot]` `Speed=`** — what RA integer corresponds to TD's `MPH_VERY_FAST` for BULLET_SAM.
- **TDSAM `[TDPatriot]` `Homing=yes`** — confirm that's RA's rules.ini field name for `BulletTypeClass::IsHoming`.
- **TDChainGun `Anim=GUNFIRE` vs `ANIM_GUN_N`** — RA has `GUNFIRE` mapped to `ANIM_MUZZLE_FLASH`; TD's CHAIN_GUN uses 8-direction `ANIM_GUN_N`. Either visual works; pick during port.

---

## Pre-existing uncommitted work in the tree

The working tree has 7 modified files from the M3 Tier 2 separation session (commit a8217c9's follow-up). These are the *subject* of the deep-dive docs — not changes this verification session made:

```
modified:   redalert/bdata.cpp           (ClassTdGtwr/Atwr/Gun/Sam declarations)
modified:   redalert/building.cpp        (M3 dispatch sites, some still aliased)
modified:   redalert/defines.h           (STRUCT_TDGTWR..TDSAM enum)
modified:   redalert/techno.cpp          (SAM grounded-aircraft filter)
modified:   resources/.../TFASSETS.MIX   (M3 SHP bundle)
modified:   resources/.../rules.ini      (M3 rules.ini entries)
modified:   scripts/buildings_manifest.py (M3 manifest)
```

**Don't commit this as-is.** The deep-dive docs prescribe specific edits to it. The plan is to apply the doc-described edits, build, smoke-test, then commit the modified files together with the cargo they implement.

Recommended approach when picking up cargo 1-8:
1. `git diff <file>` to remind yourself what's already there
2. Apply the cargo's specific edits on top
3. Build via the Linux mingw recipe (see CLAUDE.md)
4. Deploy to Steam Deck via `deploy.sh`
5. Smoke test the acceptance criteria from the relevant doc
6. Commit the cargo (engine changes + the existing M3 dispatch work get bundled if related)

---

## Memory anchors

All findings are captured in `~/.claude/projects/.../memory/`. Future-Luke's session will auto-load these:

- `[[feedback-no-donor-for-td-separation]]` — the rule this whole pass enforces
- `[[project-tdsam-deep-dive-pending]]`
- `[[project-tdatwr-deep-dive-pending]]`
- `[[project-tdgtwr-tdgun-verification]]`
- `[[project-tdobli-verification]]`
- `[[project-tdtier1-verification]]`
- `[[project-building-separation-committed]]` (pre-existing, broader framework)

---

## What's deferred (not part of this pass)

The 7 still-Logic=-aliased entries are known not separated:

```
TDHQ    (Logic=DOME)
TDPROC  (Logic=PROC)
TDFIX   (Logic=FIX)
TDWEAP  (Logic=WEAP)
TDHPAD  (Logic=HPAD)
TDEYE   (Logic=MSLO)
TDFACT  (Logic=FACT)
```

These get verified during their *individual separation* passes, not as part of this verification pass. Following the same M3-M5 plan in `docs/building-separation-plan.md`.

---

## Continuation guidance

**Start a new session** when back. The plan docs are self-contained with line numbers, exact constructor-arg values, rules.ini snippets, and TD-source citations. Future-Luke + memory entries will pick up cleanly. This conversation's research context isn't needed for implementation work.

If a future session needs to *revise* a plan (e.g. playtest reveals an unforeseen issue with a TD-authentic value), edit the relevant doc — they're living documents.
