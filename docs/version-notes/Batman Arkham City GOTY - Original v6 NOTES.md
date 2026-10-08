# v6 release

Removed the entire Gameplay / Time category and its three scripts:

- Freeze Story / Total Play Timer
- Game Speed 1.5x
- Slow Motion 0.5x

Their runtime branches and now-unused reflected metadata requirements were
removed too, rather than simply hiding the checkboxes. Historical versions are
preserved so these ideas can be revisited later.

The separate Zsasz phone-race hold at 59 seconds is retained. Challenge Modes
and its challenge/predator timers remain, because they were not under the
category the user asked to remove. Health, damage including the Batarang KO
change, gadget reach, all position actions, and their hotkeys are unchanged.

Disable the old initializer before loading v6. This lets the old table restore
any active speed edit; the new runtime no longer manages global game speed.

The user previously reported the v5 phone timer staying around 58-59 while
reaching the phone, and one-shot Batarangs. Remaining variants and phone toggle
disable tests are still documented separately. v6 is a cleanup revision, not
a claim that all challenge features have been gameplay-confirmed.

