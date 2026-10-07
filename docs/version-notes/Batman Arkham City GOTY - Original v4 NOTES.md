# v4 — Batarang knockout test

The game exposes RBMPawnAI.bBatarangCanKill at +0x850, bit 0x100. This was located
in live reflected metadata, including its mask, and found referenced by the
RBatarangProjectile.Touch collision bytecode. V3 increased projectile DefaultDamage
but did not enable this enemy flag. V4 enables the flag for loaded villain pawns
while Super Damage or One-Hit is active and restores only this bit when both modes
are off. Full neighboring flag words are not overwritten on restoration.

The existing melee, health, range, and teleport logic is unchanged. Armor Full
remains absent, following the user's report that the visual bug stopped without it.
No print/output-window calls or console changes were added.

Disable v3's Initialize entry before opening/initializing v4. No restart is needed
just to replace this table. Test One-Hit alone with quick-fire and aimed Batarangs
on ordinary unarmored thugs; then test Super Damage alone. RC Batarangs remain a
separate gameplay test, and other gadgets are not assumed supported. Disable
combat modifiers for boss/tutorial/scripted encounters.

Syntax, live reflected metadata validation, and simulated writes/restoration
passed, including the Batarang KO bit and preservation of adjacent bits. The
development tests were read-only against the live game; all test writes remained
in a Python overlay. Actual Batarang behavior still requires user confirmation.

Hotkeys remain J/K/L, F1–F4, and main-keyboard -/=.
