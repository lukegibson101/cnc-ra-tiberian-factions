# Building sound routing (TD-authentic audio for GDI/Nod)

How RA building audio is triggered, which events have TD equivalents worth
routing for GDI/Nod, and the routing pattern. Complements
`td-audio-routing-recipe.md` (the SFXEvent/launcher mechanics) and
`reference-td-eva-routing` (EVA voices).

## The routing pattern

The engine sends **one** VOC name per sound; the Remastered launcher just plays
the mapped clip and cannot know the player's faction. **Faction-routing must
happen in the DLL.** Two keys are available:

- **Building-keyed:** `Class->Type >= STRUCT_TDOBLI && Class->Type < STRUCT_COUNT`
  — true for all separated TD structures. Use when the sound belongs to a
  building (placement, construction).
- **Player-keyed:** `PlayerPtr->ActLike == HOUSE_GOOD || == HOUSE_BAD` — use for
  player-global UI sounds (credit tick).

Then add a new `VOC_TD_*` (`defines.h` enum + `audio.cpp` table — **append to
both, index-aligned**), dispatch the TD VOC in the gated branch, and register
`RAC_SFX_<NAME>` / `RAR_SFX_<NAME>` SFXEvents in `SFXEVENTSNONLOCALIZED.XML`
pointing at the TD WAVs (which already ship in the base MEGs).

## Event-by-event map

| Event | RA sound | TD equivalent | Status |
|---|---|---|---|
| **Placement slam** | `VOC_PLACE_BUILDING_DOWN`=`PLACBLDG` (`house.cpp` place, `unit.cpp` MCV deploy) | `VOC_SLAM`=`HVYDOOR1` (TD `HOUSE.CPP:2933`) | **Shipped** `VOC_TD_PLACE_BUILDING_DOWN`, building-keyed |
| **Construction loop** | `VOC_CONSTRUCTION`=`BUILD5` | `VOC_TD_CONSTRUCTION`=`CONSTRU2` (`building.cpp` Mission_Construction) | Shipped earlier |
| **Credit tick** | `VOC_MONEY_UP/DOWN`=`CASHUP1/CASHDN1` (`credits.cpp:104/106`, sent unconditionally) | `VOC_UP/DOWN`=`TONE15`/`TONE16` (TD `CREDITS.CPP:98/100`) | **Planned** — player-keyed on `PlayerPtr->ActLike` |
| **Damaged** | *none* — RA plays no building hit-SFX | — | No action |
| **Sell** | `VOC_CASHTURN` + EVA voice | `VOC_CASHTURN` (TD `HOUSE.CPP:4761`) — same | No action |
| **Destroyed** | `VOC_KABOOM22` + `VOC_CRUMBLE` | none — TD's BUILDING/TECHNO play no building-death VOC; `KABOOM22` not in TD's table | Left as-is (user choice) |

## Gotcha that cost us a session

The "double construction sound" on GDI/Nod was **not** a bug in one trigger — it
was two *separate, legitimate* sounds stacking: the **placement slam** (`PLACBLDG`)
fires the instant you drop the building, then the **construction loop**
(`CONSTRU2`) starts over it. RA factions sounded fine only because `PLACBLDG` +
`BUILD5` are both RA-flavoured. The fix was routing the slam to TD's `HVYDOOR1`,
not silencing anything. **When chasing a "doubled" sound, first confirm whether
it's one trigger firing twice or two different triggers in the same flow.**
