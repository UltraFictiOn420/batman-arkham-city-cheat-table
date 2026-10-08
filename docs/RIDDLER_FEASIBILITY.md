# Riddler one-key helper - feasibility only

Status: research; no cheat implemented or game function called.

The user asked whether one key could solve the puzzle near the player. A hotkey
can invoke one action, but that does not mean all puzzle completion logic shares
a single safe completion flag.

## Evidence from the loaded game

Read-only reflected metadata showed RRiddlerRewardCage.Open and BlendToOpen,
plus bOpen, CurrentTimeOpen, and OpenTime fields. The live game also exposes
separate Riddler progression/unlock checks. This suggests a scoped cage-opening
helper might be feasible, but opening a cage is not demonstrated to award its
collectible or correctly finish an entire puzzle/mission.

Only metadata names/layouts were inspected. Function bodies, native calling
conventions, required parameters, object lifetimes, linked puzzle sequences,
collection triggers, and persistence have NOT been verified for a solver.
Do not call the functions or flip broad progression flags based only on names.

The [official PC manual](https://cdn.akamai.steamstatic.com/steam/apps/57400/manuals/BAC_GFW_Manint_ENG_102011.pdf?t=1372817607)
describes environmental scanning separately from Riddler trophies. The
[GOTY manual](https://cdn.akamai.steamstatic.com/steam/apps/200260/manuals/Manual_EN_STM.pdf)
also describes district-by-district puzzle and trophy tracking. These support
distinguishing puzzle mechanisms, clue scans, collectible awards, and tracked
progress rather than treating every nearby Riddler object as one operation.

## Suggested first scope, if the user requests implementation

Open ONE nearest loaded trophy cage within a short radius, leave collection to
normal gameplay, and exclude hostage/story rooms and unrelated mission objects.
Use a specific nearby example to validate its native path and save persistence.
If it is safe, expand deliberately to other puzzle types instead of advertising
an untested universal solver. A no-target action should fail harmlessly; do not
apply global unlocks or mass-completion edits.

This is a candidate approach, not a promise that it will work. No new hotkey has
been assigned and no puzzle-solving toggle is included in v6.
