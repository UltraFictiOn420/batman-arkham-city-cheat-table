# v5 - Zsasz phone-race countdown

Adds Side Missions / Phone Races -> Zsasz Phone Race Countdown = 59 Seconds.
This is the city telephone race, not a general Riddler puzzle timer.

The runtime discovers live RSeqAct_ZsaszPhoneManager instances, verifies their
reflected field offsets and masks on activation, and follows raceTimer (+0x1D4).
Only a started race (bRaceStarted, +0x1C8 / mask 0x4000) with a running live
RSeqAct_HUDTimer is edited. RemainingTime (+0xEC) and IntRemainingTime (+0xF0)
are held at 59. No challenge, story, count-up, mission-state, completion, or
global-speed flags are modified by this toggle. Disabling it stops writes and
leaves the current remaining time to count down naturally; it does not restore
an expired pre-cheat time. Completion logic and phone interactions are untouched.

The game's pause bit alone did not stop the observed countdown reliably, so
the final toggle continuously holds the countdown instead of trusting that bit.
An emergency Python helper is temporarily holding the current live race at 59;
it is bounded to 20 minutes and ends if the timer stops/changes. It removes only
the emergency pause bit when exiting. This temporary helper must be stopped
after the user enables v5, or it would mask toggle-disable tests until it exits.

Disable the previous table initializer, load v5, enable its initializer, then
enable the new phone toggle. Runtime Status reports Phone timers held 1 while
it has a matching active race. Zero means no started/running phone race was
found. Load the phone-mission area before enabling if metadata is unavailable.

Live inspection verified the phone-manager link, field offsets, masks, and
temporary helper hold at 59 on two readings one second apart. Table gameplay,
race completion, timer replacement, and toggle-disable behavior still require
user confirmation. The v4 Batarang experiment remains unconfirmed.

Update after user testing, 2026-10-07: the user loaded v5 and reached the phone
with the countdown holding around 58-59 seconds. Batarangs also knocked out
thugs in one shot. The temporary rescue helper was verified to have exited
cleanly afterward. A subsequent table-only phone race and toggle-disable test
remain advisable because the helper may have overlapped the first test. Exact
Batarang firing variant/damage mode, RC Batarangs, and other gadgets remain
separate tests. This report did not require any script changes.
