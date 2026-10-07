# Development history

## v1

Original UE3-object-based table. The user confirmed health, melee damage, and teleports with Catwoman and Batman. Initial reach lookup missed relevant gadget subclasses.

## v2

Expanded gadget subclass handling and adjusted runtime/freeze behavior. Removed print output after the user reported an annoying popup. The half-body visual issue was investigated; the active script list did not include Freeze Enemies.

## v3

Removed Armor Full following the user's report. After restart, health, melee Super Damage, extra-long reach, and teleports were confirmed. Quickfire and aimed Batarangs still did not receive the desired damage behavior.

## v4 - awaiting gameplay test

Added the live-reflected RBMPawnAI.bBatarangCanKill flag (+0x850, mask 0x100), referenced by the Batarang projectile collision path. Preserve neighboring bits on restoration. Existing core behavior is unchanged; Armor Full remains absent. No console workflow is required by the table. See retained v4 notes for exact test conditions.

## Development source

development/work/build_city_table.py generates v4 from arkham_city_runtime.lua and requires luaparser. It expects development/outputs to exist before writing. test_city_runtime.py requires lupa, a live matching game PID, and the research memory reader; its writes are simulated in an overlay. Other inspection scripts may require capstone or pefile and local tool paths. Dependencies and third-party binaries are not bundled. The source is preserved as a research snapshot, not advertised as a portable one-command build.