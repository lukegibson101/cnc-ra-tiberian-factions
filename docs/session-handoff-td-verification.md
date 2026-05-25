# Session handoff — TD-source verification pass (2026-05-22)

**Status as of 2026-05-25:** **CLOSED.** All cargo shipped — TDSAM port (commit `b267742`) + smoke fixes (commit `18b39b4`) landed 2026-05-25, completing M3 Tier 2.

---

## What this session produced

| Doc | Buildings | Type |
|---|---|---|
| `docs/td-tier1-verification.md` | TDNUKE, TDNUK2, TDPYLE, TDSILO | Verification ✅ shipped |
| `docs/td-obli-verification.md` | TDOBLI | Verification ✅ shipped |
| `docs/td-gtwr-gun-verification.md` | TDGTWR, TDGUN | Verification ✅ shipped |
| `docs/td-atwr-deep-dive.md` | TDATWR | Deep dive ✅ shipped |
| `docs/td-sam-deep-dive.md` | TDSAM | Deep dive ✅ shipped (commits `b267742`, `18b39b4`) |

---

## Resolved during TDSAM implementation

- **`[TDPatriot]` `Speed=`** — TD's `MPH_VERY_FAST` = raw MPHType 100. `Speed=100` in rules.ini works when the **weapon** ([TDNike]) is flagged `IsTDPort=true` so the value parses as raw MPHType (TD source convention) rather than RA's 0-100 percentage. Without the flag, `Speed=100` becomes MPH_LIGHT_SPEED, triggers the bullet.cpp:1022 `speed = MPH_IMMOBILE` swap, and the missile fails to move. Documented in `docs/td-port-playbook.md` §3.1 (extreme case).
- **`[TDPatriot]` `Homing=yes`** — confirmed; `BulletTypeClass::Read_INI` (bbdata.cpp:344) reads `"Homing"` into `IsHoming`.

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
