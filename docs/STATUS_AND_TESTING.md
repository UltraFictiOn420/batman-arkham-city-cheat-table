# Status and testing

Baseline: v3 for the previously tested core features. Latest development table: v5. The user now reports successfully reaching a phone with the countdown holding around 58-59 seconds, and Batarangs knocking out thugs in one shot. v5 inherits the v4 Batarang change. Remaining timer isolation/disable tests and gadget variants are listed below.

| Feature | Evidence / status |
| --- | --- |
| Infinite Health | User-confirmed with Catwoman and Batman |
| Super Damage, melee | User-confirmed |
| Batarang damage / knockout | User-confirmed one-shot results in v5; exact firing variant and active damage mode were not specified in this report |
| Extra-Long Grapple / Batarang distance | User-confirmed after earlier range corrections |
| Save / Teleport / Undo | User-confirmed |
| Other damaging gadgets / RC Batarang | Not assumed supported; separate tests needed |
| Freeze Enemies | Requires additional gameplay confirmation |
| Story / challenge timers, scores, speed | Experimental or unconfirmed in relevant modes |
| Zsasz telephone race countdown | User loaded v5 and reached the phone while it stayed around 58-59; independent table-only and disable tests remain |

## Known regressions and precautions

- Armor Full was suspected by the user of causing enemies to display only their lower bodies. It was removed in v3; after restart the user reported the visual issue had stopped. This is an observed association, not a proven internal mechanism.
- The annoying Cheat Engine output popup was addressed by removing runtime print/output calls. Status is shown in a read-only table row.
- Damage cheats can interfere with scripted fights. Disable them for tutorials, bosses, cutscenes, and progression-sensitive encounters. Older third-party tables reportedly caused early story stalls; that report is not proof this table is immune.
- v4 enables the reflected enemy bBatarangCanKill flag while a damage mode is active and restores only the relevant bit. Syntax, metadata inspection, and simulated write/restoration tests passed. Test writes were isolated in an overlay, not live game memory; this does NOT establish gameplay success.

## Next tests

1. On a subsequent phone race with the temporary helper absent, confirm the v5 toggle alone holds around 58-59. Briefly disable it while ample time remains and verify countdown resumes, then re-enable.
2. Record whether the successful Batarang test used One-Hit or Super Damage and quickfire or aimed throws; separately check the remaining combinations.
3. Disable both damage modes and verify restoration and ordinary enemy behavior.
4. Test RC Batarang and other gadgets separately; record unsupported cases explicitly.
5. Test freezes, other timers, challenge score persistence/medals, and speed individually.

Hotkeys retained: J/K/L for position actions, F1-F4 for teleport height, main-keyboard -/= for damage modes. Original version-specific notes are retained under docs/version-notes.

## Time-sensitive phone-race rescue, 2026-10-07

The user requested stopping the city phone-race countdown during an active race. Live metadata identified RSeqAct_ZsaszPhoneManager.raceTimer, not a general Riddler timer. An initial pause-bit write alone did not hold RemainingTime reliably. A temporary bounded helper then held RemainingTime and IntRemainingTime at 59; two live readings one second apart both showed 59. This is a direct memory observation, not user-confirmed visual or mission-completion behavior.

v5 discovers live phone managers, validates reflected offsets/masks, and edits only their linked timer during a started, running race. It does not change race state, completion triggers, unrelated HUD timers, or speed. Turning it off leaves the current time to resume, rather than reinstating a possibly expired original value. Existing code and new scoped-timer tests passed using read-only live reads and simulated writes. Complete a race, test toggle-off without the helper, and test a subsequent race before marking this feature confirmed.

The emergency helper runs for at most 20 minutes and exits if its linked timer ends/changes. Its source is research-only, requires a specifically validated live manager/timer pair, and is not an automatic portable cheat. After the user's success report, the helper was verified to have already exited cleanly (exit code 0; 'Phone countdown rescue stopped.'); no rescue process remained. Because it may have overlapped part of the first gameplay test, the next table-only and disable tests remain useful.

## User gameplay report, 2026-10-07

The user loaded v5, found the phone, and observed the timer stay around 58-59 seconds. They also reported Batarangs killed thugs in one shot. This supports successful gameplay results for those tested scenarios, not every gadget, firing mode, timer lifecycle, or mission-completion state. The user's statement that they found the phone is not independently treated as proof of every mission completion trigger.
