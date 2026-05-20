'''
Machine source of truth for the v0.3 TD-prefixed building catalogue.

Each entry mirrors the master tables in `docs/catalogue.md` (flag table + wiring
table) and is what `scripts/add_building.py` reads to emit the rules.ini block.
The doc remains the human-readable reference; this file is the script's input.
If they drift, the script wins — fix the doc to match.

Field meanings and source:
  ininame      - canonical IniName, TD-prefixed (collides with vanilla otherwise).
                 Also used as the rules.ini Image= and XML tileset Name —
                 TD-prefix everywhere on the consumer side prevents collisions
                 with vanilla RA entries (e.g. WEAP, FIX, HPAD, SAM).
  logic        - RA donor IniName for the engine alias (Logic= in rules.ini)
  td_asset     - Original TD asset name in TEXTURES_TD_SRGB.MEG (e.g. "NUKE"
                 for the TD power plant). Drives MEG extraction in
                 bundle_assets.py and the internal `foo-NNNN.tga` frame
                 paths. Never appears in rules.ini.
  footprint    - named preset in bdata.cpp _presets[] table (unprefixed)
  shape_size   - (W, H) tuple in pixels for the Remastered launcher render
                 scale. Convention: W = Width()*24, H = Height()*24. MANDATORY
                 for every mod entry — without it, w/h=0 falls through to
                 TGA-native scale, which varies per asset. See ShapeSize block
                 in bdata.cpp's Read_INI for the override path.
  text_id_name - Launcher localization key for the sidebar display name
                 (e.g. TEXT_STRUCTURE_TITLE_GDI_POWER_PLANT). Missing
                 produces "<Missing> TDxxx" in the tooltip. Wired via
                 RABUILDABLES.XML; see scripts/bundle_assets.py.
  text_id_desc - Launcher localization key for the building description
                 (e.g. TEXT_STRUCTURE_DESC_GDI_POWER_PLANT).
  build_icon   - Tileset name resolving to the sidebar cameo TGA
                 (e.g. BuildIcon_TD_PowerPlant).
  name         - display name in the sidebar / select tooltip
  tech_level   - TD source "Build level" (sidebar gating)
  prereq       - TD-prefixed prerequisite IniName, or None for no prereq
  owner        - "GoodGuy", "BadGuy", or "GoodGuy,BadGuy"
  cost         - credits
  power        - signed: +N produces, -N consumes (engine converts -N to Drain=N)
  storage      - credit-storage capacity for refineries/silos. Integer; omit
                 (None) for non-storage buildings. TD-authentic baseline:
                 refinery 1000, silo 1500.
  points       - TD-authentic RISK/RWRD value. MANDATORY or AI ignores the
                 building (see docs/ai-targeting.md).
  sight        - cell radius (TD-authentic; smaller than RA equivalents)
  adjacent     - allowed build-distance from existing base structures
  sensors      - True for buildings that act as radar (reveal terrain in fog
                 + minimap). Emits Sensors=yes. Set on TDHQ (Comm Center) and
                 TDEYE (Adv Comm). None/False = no sensors.
  strength     - max HP
  armor        - one of: none, wood, aluminum, steel, concrete
  primary      - rules.ini weapon name for the primary slot, or None
  secondary    - rules.ini weapon name for the secondary slot, or None
  base_normal  - True for real base structures (always True in v0.3 catalogue)
  capturable   - engineer can capture
  crewed       - sell/destroy spawns infantry
  repairable   - wrench tool can target
  bib          - requires the cracked-dirt foundation bib
  idle_anim    - (start, count, rate) tuple for idle cycling, or None for static
  notes        - free-form, not emitted to rules.ini

License: GPL v3 (inherited from Vanilla Conquer base).
'''


# ---------------------------------------------------------------------------
# v0.3 catalogue entries
# ---------------------------------------------------------------------------

TDNUKE = {
    "ininame":     "TDNUKE",
    "logic":       "POWR",
    "td_asset":       "NUKE",
    "footprint":   "NUKE",
    "shape_size":  (48, 48),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_POWER_PLANT",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_POWER_PLANT",
    "build_icon":  "BuildIcon_TD_PowerPlant",
    "name":        "Power Plant",
    "tech_level":  0,
    "prereq":      None,
    "owner":       "GoodGuy,BadGuy",
    "cost":        300,
    "power":       100,
    "points":      50,
    "sight":       5,
    "adjacent":    1,
    "strength":    200,
    "armor":       "wood",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  True,
    "crewed":      True,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   (0, 4, 15),
    "notes":       "TD lvl 0; reference implementation for v0.3 phase-3a.",
}

TDNUK2 = {
    "ininame":     "TDNUK2",
    "logic":       "APWR",
    "td_asset":       "NUK2",
    "footprint":   "NUK2",
    "shape_size":  (48, 48),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_ADV_POWER_PLANT",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_ADV_POWER_PLANT",
    "build_icon":  "BuildIcon_TD_AdvPowerPlant",
    "name":        "Advanced Power Plant",
    "tech_level":  5,
    "prereq":      "TDNUKE",
    "owner":       "GoodGuy,BadGuy",
    "cost":        700,
    "power":       200,
    "points":      75,
    "sight":       5,
    "adjacent":    1,
    "strength":    300,
    "armor":       "wood",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  True,
    "crewed":      True,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   (0, 4, 15),
    "notes":       "TD lvl 5; first manifest-driven generation.",
}


TDHQ = {
    "ininame":     "TDHQ",
    "logic":       "DOME",
    "td_asset":    "HQ",
    "footprint":   "HQ",
    "shape_size":  (48, 48),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_COMM_CENTER",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_COMM_CENTER",
    "build_icon":  "BuildIcon_TD_CommCenter",
    "name":        "Communications Center",
    "tech_level":  2,
    "prereq":      "TDPROC",
    "owner":       "GoodGuy,BadGuy",
    "cost":        1000,
    "power":       -40,
    "storage":     None,
    "points":      20,
    "sight":       10,
    "adjacent":    1,
    "sensors":     True,
    "strength":    500,
    "armor":       "wood",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  True,
    "crewed":      True,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   (0, 16, 4),
    "notes":       "TD Comm Center / Radar. Shared GDI+Nod (TD didn't differentiate visually). Sensors=yes is the radar reveal + cloak-detect flag. First entry exercising the new Sensors= manifest field.",
}


TDPROC = {
    "ininame":     "TDPROC",
    "logic":       "PROC",
    "td_asset":    "PROC",
    "footprint":   None,  # RA PROC donor is 3x3 (BSIZE_33); inherit donor shape.
    "shape_size":  (72, 72),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_REFINERY",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_REFINERY",
    "build_icon":  "BuildIcon_TD_Refinery",
    "name":        "Tiberium Refinery",
    "tech_level":  1,
    "prereq":      "TDNUKE",
    "owner":       "GoodGuy,BadGuy",
    "cost":        2000,
    "power":       -40,
    "storage":     1000,
    "points":      55,
    "sight":       4,
    "adjacent":    1,
    "sensors":     None,
    "strength":    900,
    "armor":       "wood",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  True,
    "crewed":      True,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   (0, 6, 4),
    "notes":       "TD Tiberium Refinery. Shared GoodGuy/BadGuy. Logic=PROC inherits free-harvester-on-build + dock/siphon cycles. First entry exercising Storage= field.",
}


TDSILO = {
    "ininame":     "TDSILO",
    "logic":       "SILO",
    "td_asset":    "SILO",
    "footprint":   None,  # RA SILO donor is 2x1 (BSIZE_21); inherit donor shape.
    "shape_size":  (48, 24),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_SILO",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_SILO",
    "build_icon":  "BuildIcon_TD_Silo",
    "name":        "Tiberium Silo",
    "tech_level":  1,
    "prereq":      "TDPROC",
    "owner":       "GoodGuy,BadGuy",
    "cost":        150,
    "power":       -10,
    "storage":     1500,
    "points":      16,
    "sight":       2,
    "adjacent":    1,
    "sensors":     None,
    "strength":    300,
    "armor":       "wood",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  True,
    "crewed":      False,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   None,
    "notes":       "TD Silo. No idle anim (capacity-based shape, not cycle). Crew=no per TD canon.",
}


TDFIX = {
    "ininame":     "TDFIX",
    "logic":       "FIX",
    "td_asset":    "FIX",
    "footprint":   None,  # RA FIX donor is 3x3 (BSIZE_33); inherit donor shape.
    "shape_size":  (72, 72),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_REPAIR_FACILITY",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_REPAIR_FACILITY",
    "build_icon":  "BuildIcon_TD_RepairFacility",
    "name":        "Service Depot",
    "tech_level":  5,
    "prereq":      "TDNUKE",
    "owner":       "GoodGuy,BadGuy",
    "cost":        1200,
    "power":       -30,
    "storage":     None,
    "points":      46,
    "sight":       3,
    "adjacent":    1,
    "sensors":     None,
    "strength":    800,
    "armor":       "wood",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  True,
    "crewed":      True,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   None,
    "notes":       "TD Service Depot. Logic=FIX gives vehicle-repair behaviour. Image=TDFIX shadows vanilla RA FIX.",
}


TDWEAP = {
    "ininame":     "TDWEAP",
    "logic":       "WEAP",
    "td_asset":    "WEAP",
    # TD-authentic 3×3 footprint: bottom 6 cells occupied, top row overlap
    # (matching TD's ListWeap / OListWeap). Also overrides ExitCoordinate +
    # ExitList to straight-south of the bottom row — RA WEAP donor's exit is
    # calibrated for 3×2 and would land vehicles inside the new 3rd row.
    "footprint":   "WEAP",
    "shape_size":  (72, 72),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_WEAPONS_FACTORY",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_WEAPONS_FACTORY",
    "build_icon":  "BuildIcon_TD_WeaponsFactory",
    "name":        "Weapons Factory",
    "tech_level":  2,
    "prereq":      "TDPROC",
    "owner":       "GoodGuy",
    "cost":        2000,
    "power":       -30,
    "storage":     None,
    "points":      86,
    "sight":       3,
    "adjacent":    1,
    "sensors":     None,
    "strength":    1000,
    "armor":       "aluminum",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  True,
    "crewed":      True,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   None,
    "notes":       "TD GDI Weapons Factory. Logic=WEAP → vehicle factory. Image=TDWEAP shadows vanilla WEAP (IniName-collision class).",
}


TDHPAD = {
    "ininame":     "TDHPAD",
    "logic":       "HPAD",
    "td_asset":    "HPAD",
    "footprint":   None,  # RA HPAD donor matches TD (2x2 BSIZE_22).
    "shape_size":  (48, 48),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_HELIPAD",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_HELIPAD",
    "build_icon":  "BuildIcon_TD_Helipad",
    "name":        "Helipad",
    "tech_level":  6,
    "prereq":      "TDPYLE",
    "owner":       "GoodGuy,BadGuy",
    "cost":        1500,
    "power":       -10,
    "storage":     None,
    "points":      65,
    "sight":       3,
    "adjacent":    1,
    "sensors":     None,
    "strength":    800,
    "armor":       "wood",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  True,
    "crewed":      False,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   None,
    "notes":       "TD Helipad. Shared GDI+Nod per TD canon. Crew=no, no idle anim. Image=TDHPAD shadows vanilla HPAD.",
}


TDGTWR = {
    "ininame":     "TDGTWR",
    "logic":       "PBOX",
    "td_asset":    "GTWR",
    "footprint":   None,  # RA PBOX donor is 1x1 (BSIZE_11); matches TD.
    "shape_size":  (24, 24),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_GUARD_TOWER",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_GUARD_TOWER",
    "build_icon":  "BuildIcon_TD_GuardTower",
    "name":        "Guard Tower",
    "tech_level":  2,
    "prereq":      "TDPYLE",
    "owner":       "GoodGuy",
    "cost":        500,
    "power":       -10,
    "storage":     None,
    "points":      25,
    "sight":       3,
    "adjacent":    1,
    "sensors":     None,
    "strength":    200,
    "armor":       "wood",
    # RA donor weapon (PBOX = M16 / anti-infantry). TD-authentic is
    # WEAPON_CHAIN_GUN (no RA equivalent yet); donor's MG is close enough
    # for the GDI anti-infantry tower feel. See docs/weapon-ports.md.
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  False,
    "crewed":      True,
    "repairable":  True,
    "bib":         False,
    "idle_anim":   None,
    "notes":       "TD GDI Guard Tower. Logic=PBOX (Allied Pillbox donor). Cap=no, bib=no (1x1 doesn't take bib). Inherits donor weapon — TD-authentic Vulcan port is in weapon-ports.md.",
}


TDATWR = {
    "ininame":     "TDATWR",
    "logic":       "AGUN",
    "td_asset":    "ATWR",
    "footprint":   None,  # RA AGUN donor is 1x2 (BSIZE_12); matches TD.
    "shape_size":  (24, 48),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_ADV_GUARD_TOWER",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_ADV_GUARD_TOWER",
    "build_icon":  "BuildIcon_TD_AdvGuardTower",
    "name":        "Advanced Guard Tower",
    "tech_level":  4,
    "prereq":      "TDHQ",
    "owner":       "GoodGuy",
    "cost":        1000,
    "power":       -20,
    "storage":     None,
    "points":      30,
    "sight":       4,
    "adjacent":    1,
    "sensors":     None,
    "strength":    300,
    "armor":       "aluminum",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  False,
    "crewed":      True,
    "repairable":  True,
    "bib":         False,
    "idle_anim":   None,
    "notes":       "TD GDI Advanced Guard Tower. Logic=AGUN (anti-air gun donor). TD-authentic is dual-role anti-armor + anti-air (TurretGun + Nike); v0.3 inherits donor AA weapon. Weapon split is in weapon-ports.md.",
}


TDEYE = {
    "ininame":     "TDEYE",
    "logic":       "MSLO",
    "td_asset":    "EYE",
    # RA MSLO donor is BSIZE_21 (2x1); TD is 2x2. Inherit donor for v0.3 —
    # sprite at 2x2 will overhang the 2x1 footprint slightly. Authentic 2x2
    # preset is a follow-up. Superweapon behaviour works regardless.
    "footprint":   None,
    "shape_size":  (48, 48),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_ADV_COMM_CENTER",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_ADV_COMM_CENTER",
    "build_icon":  "BuildIcon_TD_AdvCommCtr",
    "name":        "Advanced Communications Center",
    "tech_level":  7,
    "prereq":      "TDHQ",
    "owner":       "GoodGuy",
    "cost":        2800,
    "power":       -200,
    "storage":     None,
    "points":      100,
    "sight":       10,
    "adjacent":    1,
    "sensors":     True,
    "strength":    500,
    "armor":       "wood",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  False,
    "crewed":      True,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   (0, 16, 4),
    "notes":       "TD GDI Advanced Comm / Ion Cannon host. Logic=MSLO grants superweapon timer; visual is Atom Bomb placeholder (Ion Cannon beam-strike effect is v0.4 engine work). Cap=no per TD canon (superweapon hosts can't be captured). -200 power drain is TD-authentic and intentional.",
}


TDPYLE = {
    "ininame":     "TDPYLE",
    "logic":       "TENT",
    "td_asset":       "PYLE",
    "footprint":   "PYLE",
    "shape_size":  (48, 48),
    "text_id_name": "TEXT_STRUCTURE_TITLE_GDI_BARRACKS",
    "text_id_desc": "TEXT_STRUCTURE_DESC_GDI_BARRACKS",
    "build_icon":  "BuildIcon_TD_Barracks",
    "name":        "Barracks",
    "tech_level":  1,
    "prereq":      "TDNUKE",
    "owner":       "GoodGuy",
    "cost":        300,
    "power":       -20,
    "points":      60,
    "sight":       4,
    "adjacent":    1,
    "strength":    400,
    "armor":       "wood",
    "primary":     None,
    "secondary":   None,
    "base_normal": True,
    "capturable":  True,
    "crewed":      True,
    "repairable":  True,
    "bib":         True,
    "idle_anim":   None,
    "notes":       "TD GDI Barracks. Donor BARR provides factory + infantry-build behaviour. Owner: HOUSE_GOOD only (Nod gets TDHAND later). Sight bumped 3->4 for RA reveal scale.",
}


# ---------------------------------------------------------------------------
# Registry — add new entries here so --all picks them up.
# Order = rules.ini emission order when running with --all.
# ---------------------------------------------------------------------------

ALL = [
    TDNUKE,
    TDNUK2,
    TDPROC,
    TDSILO,
    TDPYLE,
    TDHQ,
    TDFIX,
    TDWEAP,
    TDHPAD,
    TDGTWR,
    TDATWR,
    TDEYE,
]


def by_name(ininame):
    '''Return the manifest entry for `ininame`, or raise KeyError.'''
    for entry in ALL:
        if entry["ininame"] == ininame:
            return entry
    raise KeyError(ininame)
