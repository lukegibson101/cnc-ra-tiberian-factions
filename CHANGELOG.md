# Changelog

All notable changes to this mod will be documented here.

This project follows a `version_high.version_low.patch` scheme matching the `ccmod.json` fields.

## [Unreleased]

## [0.3.0-phase2] — 2026-05-18 — Branch reconciliation

Combined the v0.2.0 faction-bitmask work (`feature/house-good-differentiation`) with the v0.3.0 phase-1 Logic-aliased mod-building pipeline (`feature/emc-integration`). Both branches diverged from `vanilla` independently; this consolidates them onto a single trunk.

### Cherry-picked from feature/house-good-differentiation

- `42ef816` Initial rebrand: README, `README-VANILLA-CONQUER.md`, `deploy.sh`, rebranded `ccmod.json`.
- `42f75ce` v0.2.0-alpha: `HOUSEF_GOOD`/`HOUSEF_BAD` detached from `HOUSEF_ALLIES`/`HOUSEF_SOVIET` in `defines.h`; `HOUSEF_GDI`/`HOUSEF_NOD` aliases added; France country slot routed to `HOUSE_GOOD` in `dllinterface.cpp`.
- `946fb9c` v0.2.0-beta: 4-side-aware Unlimbo dispatch in `building.cpp`; `CNC_Set_Multiplayer_Data` debug dump retained.

### Dropped (explicitly superseded)

- `2717861` v0.2.0 revert marker — CHANGELOG/version-only, no code.
- `7c24666` v0.3.0-alpha — the parked hardcoded-enum approach (`STRUCT_GDI_CONST`, `STRUCT_GDI_POWER`, `UNIT_GDI_MCV`) plus 17 MB of vendored TD-Assets ZIPs. Superseded by the Logic-aliased pipeline (phase 1a-f) which adds new building types via INI rather than DLL enum extension.
- `18b5e03` "Pivot to EMC" marker — obsolete now that the pipeline shipped.

### State after reconciliation

- Engine pipeline (phase 1a-f) is in place: INI-defined `[NewBuildings]` entries with `Logic=<donor>` aliasing produce buildable, sidebar-rendered, art-correct buildings. Verified with `NUK2` as GDIPowerPlant on 2026-05-18.
- Faction bitmasks are detached: `Owner=allies` no longer pulls in `HOUSE_GOOD`. Owner= semantics for the catalogue design can now target `good` / `bad` / `gdi` / `nod` for true faction separation. Effect on test data: existing `Owner=allies` entries (e.g. NUK2 testbed) need updating to target the GDI faction explicitly once catalogue design lands.
- France country selection still routes to `HOUSE_GOOD` at the DLL boundary. Launcher UI still shows "France".

### Verification

- Built clean with the mingw remaster preset (145/145 objects, no errors).
- Full Steam Deck regression test deferred until catalogue work begins — current testbed (`tiberian-factions-emc-test` Deck folder) is not affected by this consolidation since it ships its own DLL/data; the reconciled trunk deploys to a fresh `Vanilla_RA` folder per `deploy.sh`.

## [0.2.0-beta] — 2026-05-16

### Engine

- Updated `BuildingClass::Unlimbo` in `redalert/building.cpp` to be 4-side-aware. The TD-era dispatch only checked `HOUSEF_GOOD` / `HOUSEF_BAD` for the building's side identity, which collapsed to "Soviet placeholder" for *every* building once GDI/Nod were detached in v0.2.0-alpha. Now dispatches on the RA side bits (`HOUSEF_ALLIES`, `HOUSEF_SOVIET`) plus our new `HOUSEF_GDI` / `HOUSEF_NOD`, and preserves the building's initial `ActLike` (= owner's identity) when the building has no side bits set — letting HOUSE_GOOD / HOUSE_BAD players retain their own side identity through to the sidebar query.
- Verified end-to-end on the Steam Deck: vanilla Allied (England) and Soviet (USSR) players get their normal tech trees back; France → HOUSE_GOOD player gets an empty / sparse build menu (no buildings carry the HOUSEF_GOOD bit yet — that's v0.2.0 final).
- Retained the `CNC_Set_Multiplayer_Data` debug dump for the next investigation phase. Will remove once we no longer need per-building Ownable inspection.

### Known issues / next steps

- HOUSE_GOOD has no buildable items. v0.2.0 final will add HOUSEF_GOOD to a starter set (Power Plant, Construction Yard, Refinery, Barracks) so GDI has a real tech tree.
- Voice prefix issue persists: HouseGood's `'G'` prefix maps to Soviet voicelines (no `'G'`-prefixed RA voice files; falls back to Soviet). Separate fix.

## [0.2.0-alpha] — 2026-05-16

### Engine

- Detached `HOUSE_GOOD` from `HOUSEF_ALLIES` and `HOUSE_BAD` from `HOUSEF_SOVIET` in `redalert/defines.h`. Vanilla RA bundled the TD houses into the RA side bitmasks, causing them to silently inherit the Allied / Soviet tech trees. With this change, the TD houses form their own (initially empty) factions.
- Added `HOUSEF_GDI` and `HOUSEF_NOD` aliases for clarity in subsequent commits.

### Status

- France country slot is hijacked into HOUSE_GOOD at the DLL boundary via [[spike branch reference]] (not yet wired into `main`). Result: France player will see a near-empty build menu — proof of detachment. Re-granting buildables comes in v0.2.x.
- Nod (HOUSE_BAD) detachment is symmetric but untested in this commit — only HOUSE_GOOD has a launcher route via the swap.

## [0.1.0] — Initial scaffolding (not separately tagged)

- Forked Vanilla Conquer as the DLL build base.
- Rebranded `ccmod.json` for "Tiberian Factions for Red Alert".
- Added `deploy.sh` for build + Steam Deck deploy over Tailscale.
