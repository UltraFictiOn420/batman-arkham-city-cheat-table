# v3 testing revision

October 7, 2026.

- Removed Keep Combat / Ballistic Armor Full completely. Its involvement in
  invisible upper bodies is suspected from the user's on/off test, not established
  by a controlled reproduction. No replacement armor writes are made.
- Rebuild class/hierarchy caches during every object scan to avoid retaining class
  classifications across streamed class destruction/address reuse.
- Enabling either damage mode immediately refreshes enemies and resumes a paused
  runtime timer. The underlying damage method remains health capping (10% of max
  HP for Super Damage; 1 HP for One-Hit), not a verified native damage multiplier.
- Added Runtime Status inside the table, with tick, detected player, enemy count,
  damage mode, and successful HP-write count. A runtime failure now displays
  PAUSED ERROR there instead of silently stopping or opening a log popup.
- Kept v2's gadget subclass fix and animation-preserving freeze approach.

## Clean test

Disable the old table's Initialize entry first so reversible patches are restored.
Restart the game, load v3, and initialize it. Use Infinite Health, then test One-Hit
alone on an ordinary unarmored thug with a normal punch. Do not combine damage
modes or test in a scripted boss/tutorial encounter. Then test Super Damage alone.

If either mode still fails, report the exact Runtime Status text while standing
near those enemies. The Tick value should change; it should show the selected
damage mode, and HP edits should increase when a live enemy above the cap is found.
The count measures successful writes, not hits or knockouts. Batarangs may retain
their special nonlethal/stun behavior and remain experimental.

Syntax validation and read-only live-memory/simulated-write tests passed for this
revision, including Batman and gadget discovery, health capping, positions,
range restoration, freeze, process/stale-pointer guards, and the status row.
No live game memory was written during development tests. In-CE runtime failure
state could not be inspected because the UI tool did not expose its window.
The cause of the reported damage failure is not conclusively established;
this revision includes defensive fixes and diagnostics for the next gameplay test.

J/K/L, F1–F4, and main-keyboard -/= hotkeys are unchanged. Re-save with J after
the restart. Old applied enemy-health reductions do not revert when a damage mode
is disabled, so a clean restart is recommended for comparison.
