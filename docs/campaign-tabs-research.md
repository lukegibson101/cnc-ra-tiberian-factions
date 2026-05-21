# Campaign-tabs research — adding GDI / Nod / Covert Ops to Mission Select

Research-only notes from a 2026-05-21 investigation into whether the Remastered
Mission Select screen can be modified to expose TD campaigns (GDI, Nod, Covert
Ops, console missions, Dinosaur Fun Park) alongside the existing RA campaigns.

**No code changes have been made.** This document is decision-support for a
future implementation pass.

## TL;DR

- The campaign tabs on the Mission Select screen are **XML-driven**, not
  Unity-baked. Editing data is realistic; editing the side-select screen is not.
- All TD campaign XMLs already ship in the same `CONFIG.MEG` archive that RA
  uses. We're not creating campaigns from scratch — we'd be re-pointing or
  re-exposing existing manifests.
- The single load-bearing unknown is whether the ccmod system lets us
  **override** these XMLs from a mod's `ccdata/` folder. If yes, this is an
  evening's work. If no, we need a MEG repacker.

## What's in `CONFIG.MEG`

`Data/CONFIG.MEG` carries (among ~3974 other entries) the following
campaign-related files:

```
DATA/XML/CAMPAIGNS.XML                       master campaign manifest
DATA/XML/CAMPAIGNS/RA_ALLIES.XML             + RA_ALLIES_MISSIONS.XML
DATA/XML/CAMPAIGNS/RA_USSR.XML               + RA_USSR_MISSIONS.XML
DATA/XML/CAMPAIGNS/RA_AFTERMATH.XML          + RA_AFTERMATH_MISSIONS.XML
DATA/XML/CAMPAIGNS/GDI.XML                   + GDI_MISSIONS.XML
DATA/XML/CAMPAIGNS/NOD.XML                   + NOD_MISSIONS.XML
DATA/XML/CAMPAIGNS/CONSOLE.XML               + CONSOLE_MISSIONS.XML   (PS missions)
DATA/XML/CAMPAIGNS/FUNPARK.XML               + FUNPARK_MISSIONS.XML   (Dinosaur)
DATA/XML/CAMPAIGNS/ANT.XML                   + ANT_MISSIONS.XML       (Giant Ants)

DATA/ART/GUI/UI_CAMPAIGNMENU.BUI             campaign-menu layout (Unity binary)
DATA/ART/GUI/UI_CAMPAIGNSELECT.BUI           side-select layout (Unity binary)
DATA/ART/GUI/RA/RA_CAMPAIGN_SELECT.BUI       RA side-select skin
DATA/ART/GUI/CNC/CNC_CAMPAIGN_SELECT.BUI     TD side-select skin
```

No `RA_COUNTERSTRIKE.XML` was observed — Counterstrike content likely lives
inside `RA_ALLIES.XML` / `RA_USSR.XML` rather than its own manifest.

Per-tab game data (the MIX files containing scenarios, briefings, etc.) lives
under `Data/CNCDATA/RED_ALERT/{CD1, COUNTERSTRIKE, AFTERMATH, COMMUNITY,
CUSTOMMAPS}/` and `Data/CNCDATA/TIBERIAN_DAWN/{CD1, CD2, CD3, CONSOLE_1,
CONSOLE_2, COMMUNITY, CUSTOMMAPS}/`. Each tab maps cleanly to one of these
folders.

## What we control vs. what we don't

| Surface | Format | Editable? |
|---|---|---|
| Campaign manifest (`CAMPAIGNS.XML`) | XML | Yes, if we can override |
| Per-campaign metadata (`GDI.XML` etc.) | XML | Yes, if we can override |
| Mission lists (`*_MISSIONS.XML`) | XML | Yes, if we can override |
| Tab icons | Texture in `TEXTURES_*.MEG` | Yes, asset swap |
| Side-select screen layout (`*_CAMPAIGN_SELECT.BUI`) | Unity binary UI | **No** — would need Unity asset modding |
| Per-tab game data | `.MIX` files in `Data/CNCDATA/` | Yes, standard mod surface |

## The repurpose plan (assumes XML override works)

Replace RA's 6 tabs with a 4-faction layout:

| Slot | Stock content | Proposed content |
|---|---|---|
| 1 | Allied Campaign | GDI Campaign |
| 2 | Soviet Campaign | Nod Campaign |
| 3 | Counterstrike | TD Extras (Covert Ops + Dinosaur + Console) |
| 4 | Aftermath | Allied Campaign |
| 5 | (5th tab) | Soviet Campaign |
| 6 | Custom Missions | RA Extras (Counterstrike + Aftermath) |

Trade-off: we lose the Custom Missions slot. Acceptable for a four-faction
total-conversion mod — players who want Workshop mission content can disable
the mod.

The side-select screen would still show only two emblems ("Allies" / "Soviet").
That cosmetic mismatch is the cost of staying out of Unity-asset modding.

## Unresolved

1. **Does ccmod let us override XMLs from `ccdata/`?**
   The decisive experiment. Drop a hand-modified `CAMPAIGNS.XML` (or one of the
   per-campaign XMLs) into a test mod's `ccdata/DATA/XML/CAMPAIGNS/` and check
   whether the shell prefers it over the MEG version. Binary yes/no answer.

2. **Does `CAMPAIGNS.XML` declare a `game_type` per campaign?**
   Strongly implied yes (clicking "Allies" in RA doesn't list GDI missions, so
   there's a filter somewhere), but unconfirmed. Requires successful MEG
   extraction.

3. **MEG file-table format.**
   The header decodes (magic `0xFFFFFFFF`, seed, data_offset, num_files,
   filename_table_size). The filename table decodes cleanly. The file-record
   table (20 bytes/entry × 3974 entries) didn't yield sensible offsets/sizes
   under the documented MEG v3 layout — possibly partial encryption, possibly
   a Remastered-specific packing. Look for an existing community tool before
   reimplementing.

4. **MEG repack path** (only relevant if #1 fails).
   If the shell ignores ccmod XML overrides, we'd need to repack `CONFIG.MEG`
   with modified XMLs. Investigate `CnCTDRAMapEditor.exe` (ships next to the
   install) and the wider Remastered modding community for a known-good
   round-trip tool.

## Recommended next step

Run experiment #1. It's cheap, definitive, and determines whether the rest of
this project is "an evening of XML editing" or "a Unity / MEG archaeology
project". Until that question is answered, no further investigation is the
best use of time.
