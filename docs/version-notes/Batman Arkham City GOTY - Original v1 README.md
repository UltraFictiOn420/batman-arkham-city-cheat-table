# Batman Arkham City GOTY — Original v1

First testing version for the user's Steam/PC GOTY build (BatmanAC.exe).
Created October 7, 2026. The uploaded legacy table was read for feature leads;
the new scripts and Lua runtime were authored independently. The original
uploaded file is unchanged. No console unlock, binding edit, or game-file patch.

## Use

Open the `.CT` in Cheat Engine while the game is running. Enable the green
“[Required] Initialize Arkham City GOTY Table” entry first. Initialization may
take several seconds. Then enable only the cheats you want. Start by testing
Infinite Health, combat damage, and position hotkeys separately.

- Main keyboard `-`: Super Damage toggle.
- Main keyboard `=`: One-Hit Knockout toggle.
- `J`: save position; `K`: teleport back; `L`: undo/redo the last teleport.
- `F1`/`F2`/`F3`/`F4`: teleport up 1/2/5/10 body heights.

## Included

Infinite health; refill existing melee/ballistic armor; freeze enemies;
10x-equivalent damage; one-hit knockout; longer grapple and Batarang reach;
freeze total play time; 1.5x speed / 0.5x slow motion; experimental challenge
HUD score, challenge countdown pause/reset, and predator timer freeze/reset;
save/teleport/undo and upward teleports.

Player features follow the controlled character through its controller, including
Catwoman. Armor refill does not grant armor upgrades; it skips unavailable armor.
Damage modes reduce enemies' health to one tenth of normal or 1 HP, respectively;
they do not multiply every damage calculation. They modify Batarang projectile
damage too, but Batarang knockout/stun behavior still needs gameplay testing.

## Verification and limitations

XML and every Lua block passed syntax validation. The runtime initialized against
live read-only game memory and validated reflected field offsets. It identified
the controlled Catwoman and five loaded enemy actors. Simulated writes verified
health, damage, teleport/undo, masked flag restoration, and pointer/process guards.
These checks did not change the game. Cheat Engine's process was confirmed running,
but its window was absent from the UI tool inventory; in-CE activation and actual
gameplay behavior have not yet been verified.

All features therefore need gameplay testing. Challenge HUD score might be only
visual; medal/results persistence is not verified. Challenge timer pause/reset
targets challenge/modifier/bespoke HUD timers, not every timer in the game. Countdown
reset refills to its configured starting value, rather than setting it to zero.
Freeze Story Timer changes total-played time, not mission deadlines.

Back up saves and don't combine this with another table/trainer. Disable damage
and freeze cheats around scripted bosses or interrogations. Health reductions
already applied to enemies remain after disabling damage mode. Teleports do not
check walls or load a new map: use L to undo, and resave after a character/session
change. Disable speed modifiers during cutscenes if needed.

Fly/no-gravity, no-hitbox, combo/XP/upgrade points, waypoint teleport, and Riddler
scan/story-flag edits are intentionally omitted, following the final Asylum scope.
