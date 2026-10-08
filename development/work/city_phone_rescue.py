"""Temporary, bounded live rescue for the validated Zsasz phone-race timer.

Not a portable table. Stop the helper after handing control to the CE toggle.
"""
import sys, struct, time
from ue3_inspect import ProcessMemory

pid, manager = int(sys.argv[1]), int(sys.argv[2], 0)
pm = ProcessMemory(pid)
manager_identity = pm.read(manager + 0x18, 16)
timer = pm.u32(manager + 0x1D4)
timer_identity = pm.read(timer + 0x18, 16)
timer_index = pm.u32(timer + 4)
registry = pm.u32(0x1643CE0)
assert timer == int(sys.argv[3], 0)
assert pm.u32(registry + timer_index * 4) == timer
assert pm.u32(timer + 0xF4) & 2
print('Phone countdown rescue running: 59 seconds; bounded to 20 minutes.', flush=True)
deadline = time.monotonic() + 1200
try:
    while time.monotonic() < deadline:
        if pm.read(manager + 0x18, 16) != manager_identity:
            break
        if pm.u32(manager + 0x1D4) != timer:
            break
        if pm.read(timer + 0x18, 16) != timer_identity:
            break
        registry = pm.u32(0x1643CE0)
        if not registry or pm.u32(registry + timer_index * 4) != timer:
            break
        flags = pm.u32(timer + 0xF4)
        if flags is None or not flags & 2:
            break
        pm.write(timer + 0xEC, struct.pack('<f', 59.0))
        pm.write(timer + 0xF0, struct.pack('<i', 59))
        time.sleep(0.025)
finally:
    # Remove only the emergency pause bit on the original still-live timer.
    registry = pm.u32(0x1643CE0)
    if registry and pm.u32(registry + timer_index * 4) == timer and pm.read(timer + 0x18, 16) == timer_identity:
        flags = pm.u32(timer + 0xF4)
        if flags is not None:
            pm.write(timer + 0xF4, struct.pack('<I', flags & ~1))
    pm.close()
    print('Phone countdown rescue stopped.', flush=True)
