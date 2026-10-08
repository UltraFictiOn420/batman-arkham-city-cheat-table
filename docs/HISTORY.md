# Development history

## v1

Original UE3-object-based table. The user confirmed health, melee damage, and teleports with Catwoman and Batman. Initial reach lookup missed relevant gadget subclasses.

## v2

Expanded gadget subclass handling and adjusted runtime/freeze behavior. Removed print output after the user reported an annoying popup. The half-body visual issue was investigated; the active script list did not include Freeze Enemies.

## v3

Removed Armor Full following the user's report. After restart, health, melee Super Damage, extra-long reach, and teleports were confirmed. Quickfire and aimed Batarangs still did not receive the desired damage behavior.

## v4 - awaiting gameplay test

Added the live-reflected RBMPawnAI.bBatarangCanKill flag (+0x850, mask 0x100), referenced by the Batarang projectile collision path. Preserve neighboring bits on restoration. Existing core behavior is unchanged; Armor Full remains absent. No console workflow is required by the table. See retained v4 notes for exact test conditions.

## v5 - phone-race countdown

Responded to a live time-sensitive telephone race. Identified the Zsasz phone manager's raceTimer link and active-race flag through reflected metadata. A pause-only rescue did not reliably stop the countdown; a bounded temporary helper held it at 59. Added a table toggle that writes only the active phone race's remaining float/integer values. Syntax and simulated targeting/active-race/disable tests passed; user gameplay confirmation is still pending. v4 Batarang behavior remains unconfirmed.

## Development source

development/work/build_city_table.py now generates v5 from arkham_city_runtime.lua and requires luaparser. It expects development/outputs to exist before writing. test_city_runtime.py requires lupa, a live matching game PID, the phone-mission area loaded, and the research memory reader; its writes are simulated in an overlay. Other inspection scripts may require capstone or pefile and local tool paths. Dependencies and third-party binaries are not bundled. The source is preserved as a research snapshot, not advertised as a portable one-command build.
