# Session handoff — Phase W1 weapons port + building-separation scoping

**Session date:** 2026-05-21 (afternoon)
**Pickup state:** Phase W1 first weapon (TOW_TWO) ported under Option B, build green, uncommitted. Building-separation plan documented for future decision. Ready to either commit-and-deploy or continue to the next weapon (TdTurretGun, OBELISK_LASER).

---

## Decisions made this session

1. **Weapons port: Option B (full data isolation).** Every TD weapon gets its own `WEAPON_*` enum, its own `WeaponTypeClass` heap entry, its own rules.ini `[Name]` section, AND its own `VOC_TD_*` sound enum + audio.cpp entry. Never reuse RA's Report=MISSILE1 / Report=GUN8 as a stand-in. Anim_* entries added the same way when ports need muzzle flashes.

2. **Buildings stay Logic= aliased for v0.4.x.** Full STRUCT_TDxxxx separation is documented in `docs/building-separation-plan.md` as a 3-5 week M1-M6 plan. Decision deferred until weapons phase + unit catalogue stabilise.

3. **TDGUN gets its own [TdTurretGun] weapon** (not an override of RA's `[TurretGun]`). Same pattern as TOW_TWO — independent damage/ROF/Range knobs without touching vanilla Allied gameplay.

---

## What landed this session (uncommitted)

### TOW_TWO weapon port (Phase W1, building #1 of 2)

End-to-end ported, build green, ready for Deck playtest. Replaces TDATWR's Hellfire/ZSU-23 dual-role interim with a single TD-authentic missile that hits both ground and air.

Files touched:

- `redalert/defines.h` — added `WEAPON_TOW_TWO` (before `WEAPON_COUNT`), `BULLET_SSM` (before `BULLET_COUNT`), `VOC_TD_ROCKET2` (before `VOC_COUNT`)
- `redalert/bbdata.cpp` — `new BulletTypeClass("SSM")` registration in `Init_Heap`
- `redalert/rules.cpp` — `new WeaponTypeClass("TowTwo")` registration after AirAssault
- `redalert/audio.cpp` — `{"ROCKET2", 1, IN_NOVAR}` SoundEffectName entry
- `resources/remaster_mods/Vanilla_RA/CCDATA/rules.ini`:
  - new `[TowTwo]` weapon section (Damage=60, ROF=40, Range=6.5, Projectile=SSM, Speed=30, Warhead=HE, Report=ROCKET2)
  - new `[SSM]` projectile section (Arm=7, High=yes, AA=yes, AG=yes, Image=DRAGON, ROT=5, Rotates=yes, Inaccurate=yes, Translucent=yes)
  - `[TDATWR]` Primary= swapped from `Hellfire` to `TowTwo`
- `scripts/buildings_manifest.py` — TDATWR entry: primary swapped to `"TowTwo"`, secondary dropped to `None`, old dual-role comment replaced with W1 port note

### Building-separation scope doc (new file)

`docs/building-separation-plan.md` — covers what gets ported from `tiberiandawn/`, adapter glue needed, per-building work breakdown for the 17 entries, classic-mode SHP payoff, 6 incremental milestones, risk register, decision points before starting. Doc-only deliverable, no code.

### Catalogue cleanup

`docs/catalogue.md` "Building bugs found during 2026-05-20 playtest" — items #1, #3, #4, #5 marked done and removed (per user "1,3,4,5 done"). Items remaining (renumbered):
- #1 TDPROC idle anim after harvester dock — superseded by [[project-td-harvester-dock-plan]]
- #2 TDTMPL slow buildup then snap

"Deferred architectural items" — confirmed Spain→HOUSE_GOOD (GDI) and Turkey→HOUSE_BAD (Nod) launcher swaps both wired in `dllinterface.cpp:905-910`. Memory [[project-country-modifiers-removal]] already reflects this pairing.

---

## What's NOT done (the to-do list when picking up)

Tasks still pending, in priority order:

1. **Deploy & playtest TOW_TWO on the Deck** — `./deploy.sh`, then build TDATWR in skirmish and verify: (a) it fires a missile (not a cannon shell), (b) the missile sound is the TD ROCKET2.AUD (not RA's MISSILE1 — they're distinguishable), (c) it hits both ground armor and air. If sound is silent, that means `ROCKET2.AUD` isn't accessible via the default mix-file path and we need to bundle it (CONFIG.MEG extract → mod mixfile).

2. **#7 [TdTurretGun] for TDGUN** — Phase W1's third small port. TD-authentic stats (Damage=40, ROF=60 vs RA's 50, Range=6, Projectile=Cannon, Warhead=AP). Add VOC_TD_TANK4 enum + ROCKET2-pattern audio entry. New manifest field `primary="TdTurretGun"` for TDGUN. No new BulletType needed — Cannon is close enough to TD's BULLET_APDS visually.

3. **#2/#3/#4 OBELISK_LASER (Phase W1 big lift)** — the hard one. Three sub-pieces:
   - Data: WEAPON_OBELISK_LASER + BULLET_LASER + WARHEAD_LASER (100%-vs-all-armor) + VOC_TD_LASER (OBELRAY1.AUD) + VOC_TD_LASER_POWER (OBELPOWR.AUD)
   - Engine: port TD's laser-line draw path from `tiberiandawn/techno.cpp:2481-2514` — globals `Lines[3][5]`, `LineCount`, `LineFrame`, `LineMaxFrames`, per-frame display hook, `Fire_At` BULLET_LASER branch, scorch smudge stamp. RA has none of this rendering infrastructure (`LineCount` exists in RA's `list.cpp` but it's a UI list widget, unrelated).
   - Hookup: TDOBLI manifest Primary=Hellfire → OblsLaser swap.

4. **#6 TDTMPL buildup-rate fix** — small. Replace hardcoded `rate=2` in `scripts/add_building.py` (line ~143) with engine-matched formula `max(1, round(BuildupTime_ticks / count))`. Cross-reference TDNUKE (19 frames) / TDFACT (32 frames) — both land correctly at rate=2 because their total durations stay inside the engine's BuildupTime budget; TDTMPL's 36 frames don't.

5. **#8 TDGUN turret rotation** — TDGUN fires statically instead of rotating to face targets. Likely Logic=GUN donor's `BuildingClass::Draw_It` turret-draw path isn't firing for our mod entry. Investigate when looking at TDGUN anyway for #7.

6. **Building-separation green-light decision** — review `docs/building-separation-plan.md`, decide: all 17 entries or partial, start timing, atomic vs flag-gated approach. Defer until after Phase W1 weapons land.

---

## Commit suggestion when resuming

Two natural commits to break up the uncommitted working tree:

**Commit 1: TOW_TWO weapon port (Phase W1 — building #1 of 2)**
```
redalert/defines.h
redalert/bbdata.cpp
redalert/rules.cpp
redalert/audio.cpp
resources/remaster_mods/Vanilla_RA/CCDATA/rules.ini
scripts/buildings_manifest.py
```
Message: `v0.4.1-phase-w1a: TOW_TWO weapon port — TDATWR fires TD-authentic AA+AG missile`

**Commit 2: docs — building-separation scope + catalogue cleanup**
```
docs/building-separation-plan.md (new)
docs/catalogue.md
```
Message: `docs: building-separation scope plan + catalogue playtest-bug cleanup`

Or one combined commit if Luke prefers the smaller log. Both options are clean.

---

## Open questions for next session

- Does ROCKET2.AUD play in-game, or do we need to ship it in a mod mixfile? (Tells us whether OBELRAY1 / OBELPOWR / TANK4 etc. need bundling too.)
- Is the SSM bullet's `Image=DRAGON` visually right for TOW, or do we want a different missile sprite? (TD's BULLET_SSM uses DRAGON internally despite being for TOW/TOMAHAWK/MAMMOTH_TUSK, so this is TD-authentic — but worth eyeballing on the Deck.)
- Building-separation: thumbs-up or thumbs-down on starting after Phase W1 completes?

---

## Related docs / memory

- `docs/weapon-ports.md` — Phase W1/W2/W3 plan; W1 is what we're executing
- `docs/building-separation-plan.md` — the new 3-5 week scope plan (this session)
- `docs/catalogue.md` — current building catalogue + playtest bug list
- `docs/cargo-plane-port.md` — TDAFLD reference (already shipped in v0.4)
- [[project-workshop-publish-state]] — v0.4 live on Workshop as item 3729834253
- [[project-td-harvester-dock-plan]] — superseded by either M4 of separation plan OR a targeted harvester unit port
