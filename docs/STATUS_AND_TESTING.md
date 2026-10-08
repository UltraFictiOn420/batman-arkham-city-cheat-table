# Status and testing

## Project state - paused, 2026-10-08

The user chose to take a break and begin a separate Batman Arkham Origins project. Keep v6 as the current release. Final v7 was proposed but was not built or released, and remaining Test labels must not be removed merely because work is paused. No existing scripts were changed for this handoff.

Resume checklist: freeze/unfreeze ordinary enemies; test both damage modes with aimed/quickfire Batarangs and their disable behavior; verify phone hold/disable without the exited helper; confirm challenge score affects results/medals; test pause/reset/resume in combat, Shock and Awe, and predator challenges. Other gadgets remain separately unconfirmed.

Current release: v6, a requested cleanup of v5 with Gameplay / Time removed. v3 is the historical baseline for previously tested core features. The user reports successfully reaching a phone in v5 with the countdown holding around 58-59 seconds, and Batarangs knocking out thugs in one shot. v6 preserves those implementations. Remaining timer isolation/disable tests and gadget variants are listed below.

| Feature | Evidence / status |
| --- | --- |
| Infinite Health | User-confirmed with Catwoman and Batman |
| Super Damage, melee | User-confirmed |
| Batarang damage / knockout | User-confirmed one-shot results in v5; exact firing variant and active damage mode were not specified in this report |
| Extra-Long Grapple / Batarang distance | User-confirmed after earlier range corrections |
| Save / Teleport / Undo | User-confirmed |
| Other damaging gadgets / RC Batarang | Not assumed supported; separate tests needed |
| Freeze Enemies | Requires additional gameplay confirmation |
| Story / total-play-time freeze and global speed | Removed from v6 at the user's request |
| Challenge / predator timers and scores | Retained; experimental or unconfirmed in relevant modes |
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
5. Test freeze/unfreeze, challenge score persistence/medals, and challenge pause/reset/resume separately in combat, Shock and Awe, and predator modes. Global speed was removed in v6 and is not part of the current test plan.

Hotkeys retained: J/K/L for position actions, F1-F4 for teleport height, main-keyboard -/= for damage modes. Original version-specific notes are retained under docs/version-notes.

## Time-sensitive phone-race rescue, 2026-10-07

The user requested stopping the city phone-race countdown during an active race. Live metadata identified RSeqAct_ZsaszPhoneManager.raceTimer, not a general Riddler timer. An initial pause-bit write alone did not hold RemainingTime reliably. A temporary bounded helper then held RemainingTime and IntRemainingTime at 59; two live readings one second apart both showed 59. This is a direct memory observation, not user-confirmed visual or mission-completion behavior.

v5 discovers live phone managers, validates reflected offsets/masks, and edits only their linked timer during a started, running race. It does not change race state, completion triggers, unrelated HUD timers, or speed. Turning it off leaves the current time to resume, rather than reinstating a possibly expired original value. Existing code and new scoped-timer tests passed using read-only live reads and simulated writes. Complete a race, test toggle-off without the helper, and test a subsequent race before marking this feature confirmed.

The emergency helper runs for at most 20 minutes and exits if its linked timer ends/changes. Its source is research-only, requires a specifically validated live manager/timer pair, and is not an automatic portable cheat. After the user's success report, the helper was verified to have already exited cleanly (exit code 0; 'Phone countdown rescue stopped.'); no rescue process remained. Because it may have overlapped part of the first gameplay test, the next table-only and disable tests remain useful.

## User gameplay report, 2026-10-07

The user loaded v5, found the phone, and observed the timer stay around 58-59 seconds. They also reported Batarangs killed thugs in one shot. This supports successful gameplay results for those tested scenarios, not every gadget, firing mode, timer lifecycle, or mission-completion state. The user's statement that they found the phone is not independently treated as proof of every mission completion trigger.

## v6 cleanup checks

Removed category ID 40 and entries 41-43. Removed their runtime write branches and unused metadata requirements, while keeping challenge timer entries 53-56 and phone entry 71. Builder assertions verify all these conditions. Lua syntax and the existing live-read/simulated-write regression suite passed, including health, damage/KO masked restoration, ranges, teleports, phone race guards/disable behavior, and process/pointer guards. No live game writes or console changes were performed for the v6 cleanup. Release finalization changed only comments and documentation; the executable scripts remain identical to the already checked v6 build. Disable the old initializer to restore any old speed changes before loading this release.
