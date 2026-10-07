# Original v2 — October 7, 2026

Before loading v2, disable the green Initialize entry in v1. This shuts down its
timer and restores its reversible settings. Then open v2 and initialize it.
Existing health reductions on enemies are not undone by disabling damage cheats.

## Changes

- Removed every `print()` call from the table runtime, including initialization,
  failed teleport actions, and timer errors. No Lua output window is intentionally
  opened. Errors are retained in `AC.lastResult` / `AC.lastError`.
- Fixed gadget discovery: v1 only selected the exact base-class names RBatarang
  and RGrappleGun. Live Batman uses RGrappleGunBm, RBatarangBm, and additional
  Batarang subclasses. Those are now recognized through their class hierarchy.
- Range writes no longer reduce a limit that is already larger than 50,000 or
  replace negative engine sentinel settings. Valid grapple points and engine
  targeting/visibility constraints still apply: this does not attach to arbitrary
  walls or bypass the world-streaming system.
- Changed enemy freeze to pause controller AI and pin movement while keeping
  pawn animation/mesh updates active. This is a preventative improvement, not a
  confirmed explanation for the reported missing upper bodies: the user reports
  Freeze Enemies was not enabled when that bug occurred.

## Verification

XML and Lua syntax pass. Read-only live-memory tests find Batman, his grapple,
and three Batarang gadgets. Simulated range writes/restoration, health, damage,
teleport/undo, AI/movement freeze, and stale-pointer/process guards pass. Tests
write only to a Python overlay, never to the game. Gameplay testing of v2 remains
necessary. Infinite Health, Super Damage, and teleports in v1 were user-confirmed
working for both Batman and Catwoman.

## Still investigating: missing upper bodies

Enabled scripts reported: Infinite Health, Keep Combat/Ballistic Armor Full,
Super Damage, Extra-Long Grapple, and Extra-Long Batarang. No cause established.
V1's range discovery skipped the active Batman gadgets, so those intended range
writes were not applied. Armor refill is scoped to the controlled player's two
armor-array elements; it does not directly edit enemy meshes.

Please supply a screenshot and check newly encountered enemies with Super Damage
disabled. To get a clean comparison, disable the v1 initializer before loading
v2; if a model remains malformed, reload the checkpoint with only Infinite Health
enabled. Then add Armor and Super Damage individually. A model already changed
by the game may not reset merely because a cheat is disabled. Keep combat cheats
off during scripted progression sequences.

Hotkeys remain J/K/L, F1–F4, and the main keyboard -/= keys.
