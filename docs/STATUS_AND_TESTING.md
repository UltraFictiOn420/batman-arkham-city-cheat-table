# Status and testing

Baseline: v3 for user-tested core features. v4 is a Batarang knockout experiment awaiting gameplay confirmation.

| Feature | Evidence / status |
| --- | --- |
| Infinite Health | User-confirmed with Catwoman and Batman |
| Super Damage, melee | User-confirmed |
| Batarang damage / knockout | v3 did not produce the desired effect with quickfire or aimed Batarangs; v4 unconfirmed |
| Extra-Long Grapple / Batarang distance | User-confirmed after earlier range corrections |
| Save / Teleport / Undo | User-confirmed |
| Other damaging gadgets / RC Batarang | Not assumed supported; separate tests needed |
| Freeze Enemies | Requires additional gameplay confirmation |
| Story / challenge timers, scores, speed | Experimental or unconfirmed in relevant modes |

## Known regressions and precautions

- Armor Full was suspected by the user of causing enemies to display only their lower bodies. It was removed in v3; after restart the user reported the visual issue had stopped. This is an observed association, not a proven internal mechanism.
- The annoying Cheat Engine output popup was addressed by removing runtime print/output calls. Status is shown in a read-only table row.
- Damage cheats can interfere with scripted fights. Disable them for tutorials, bosses, cutscenes, and progression-sensitive encounters. Older third-party tables reportedly caused early story stalls; that report is not proof this table is immune.
- v4 enables the reflected enemy bBatarangCanKill flag while a damage mode is active and restores only the relevant bit. Syntax, metadata inspection, and simulated write/restoration tests passed. Test writes were isolated in an overlay, not live game memory; this does NOT establish gameplay success.

## Next tests

1. Use v4 alone, with One-Hit active alone, against ordinary unarmored thugs: quickfire and aimed Batarang.
2. Repeat with Super Damage alone; check melee behavior remains correct.
3. Disable both modes and verify restoration and ordinary enemy behavior.
4. Test RC Batarang and other gadgets separately; record unsupported cases explicitly.
5. Test freezes, timers, challenge score persistence/medals, and speed individually.

Hotkeys retained: J/K/L for position actions, F1-F4 for teleport height, main-keyboard -/= for damage modes. Original version-specific notes are retained under docs/version-notes.