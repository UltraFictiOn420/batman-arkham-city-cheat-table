"""Execute actual table Lua against live READ-ONLY memory plus a write overlay.
No allocation, game-memory write, input, or in-game action takes place.
"""
import sys,struct,time
from pathlib import Path
from lupa import LuaRuntime
from ue3_inspect import ProcessMemory

pm=ProcessMemory(int(sys.argv[1]));pid=int(sys.argv[1]);current=[pid]
lua=LuaRuntime(unpack_returned_tuples=True);g=lua.globals();overlay={};writes=[];symbols={}
def read(a,n):
    if 0x7fe00000<=a<0x7fe10000:return bytes(overlay.get(a+j,0) for j in range(n))
    data=pm.read(a,n)
    return bytes(overlay.get(a+j,b) for j,b in enumerate(data))
def ri(a):
    raw=read(int(a),4);return struct.unpack('<I',raw)[0] if len(raw)==4 else None
def rf(a):
    raw=read(int(a),4);return struct.unpack('<f',raw)[0] if len(raw)==4 else None
def write(a,v,kind):
    raw=struct.pack('<f' if kind=='float' else '<I',v if kind=='float' else int(v)&0xffffffff)
    overlay.update({int(a)+i:b for i,b in enumerate(raw)});writes.append((int(a),v,kind));return True
def rs(a,n,wide=False):
    raw=read(int(a),int(n)*(2 if wide else 1))
    return raw.decode('utf-16le' if wide else 'latin1',errors='ignore').split('\0')[0] if raw else None
g.openProcess=lambda _:None;g.getOpenedProcessID=lambda:current[0];g.getAddressSafe=lambda _:0x400000
g.readInteger=ri;g.readFloat=rf;g.readString=rs
g.readBytes=lambda a,n,t:lua.table_from(list(read(int(a),int(n))))
g.writeInteger=lambda a,v:write(a,v,'int');g.writeFloat=lambda a,v:write(a,v,'float')
alloc=[0x7fe00000]
def allocate(_):
    value=alloc[0];alloc[0]+=0x1000;return value
g.allocateMemory=allocate;g.registerSymbol=lambda n,a,*_:symbols.update({n:a})
def ws(a,s,wide=False):
    raw=s.encode('utf-16le' if wide else 'latin1');overlay.update({int(a)+i:b for i,b in enumerate(raw)});return True
g.writeString=ws
g.unregisterSymbol=lambda n:symbols.pop(n,None);g.deAlloc=lambda _:None
g.createTimer=lua.eval('function() return {Enabled=false, destroy=function() end} end')
source=(Path(__file__).parent/'arkham_city_runtime.lua').read_text(encoding='utf-8')
start=time.monotonic();lua.execute(source);C=g.AC
p=C.pawn();assert p and C.live(p,'RPawnPlayer')
print('INITIALIZED',round(time.monotonic()-start,2),'seconds','PLAYER',hex(p),C.cn(p),'ENEMIES',len(C.enemies),'PROJECTILES',len(C.projectiles))
assert len(writes)==1 and writes[0][0]==0x7fe00000,'Initializer must not modify gameplay'
# Snapshot/teleport calculations in the overlay; never touch real game memory.
C.save();saved=C.saved;C.up(1);assert abs(rf(p+0x50)-saved.z)>10
C.undoTeleport();assert abs(rf(p+0x50)-saved.z)<0.01
C.teleport();assert abs(rf(p+0x48)-saved.x)<0.01
print('POSITION TESTS PASSED',saved.x,saved.y,saved.z)
C.flags.health=True;write(p+0x2c4,5,'int');C.loop();assert ri(p+0x2c4)==ri(p+0x2c8)
print('HEALTH TEST PASSED')
e=C.enemies[1];write(e+0x2c4,100,'int');write(e+0xb00,100.0,'float')
koInitial=ri(e+0x850);write(e+0x850,koInitial&~0x100,'int');koInitial=ri(e+0x850)
C.classes[C['class'](e)]='StaleClass';C.setFlag('superDamage',True)
assert C.cn(e)!='StaleClass','Activation must invalidate streamed class caches'
C.loop();assert ri(e+0x2c4)==10
assert ri(e+0x850)&0x100
assert (ri(e+0x850)&~0x100)==(koInitial&~0x100),'KO flag must not change neighboring flags'
C.setFlag('superDamage',False);C.setFlag('oneHit',True);C.loop();assert ri(e+0x2c4)==1
C.flags.oneHit=False;C.flags.freeze=True
initial=ri(e+0xa0);C.loop();assert ri(e+0xa0)==initial,'Must not disable pawn animation ticks'
assert ri(e+0x850)==koInitial,'KO flag must restore when both damage modes are off'
print('BATARANG KO FLAG / MASK RESTORE TESTS PASSED')
controller=ri(e+0x1cc)
if controller and C.live(controller,'Controller'):assert ri(controller+0xa0)&64
assert C.frozen[e] is not None
C.flags.freeze=False;C.loop();assert ri(e+0xa0)==initial
assert C.frozen[e] is None
grapples=[v for _,v in C.gadgets.items() if C.live(v,'RGrappleGun')]
brangs=[v for _,v in C.gadgets.items() if C.live(v,'RBatarang')]
assert grapples and brangs,'Must discover live Batman gadget subclasses'
C.flags.grappleRange=True;C.flags.batarangRange=True;C.loop()
for o in grapples:assert rf(o+0x3d0)==50000
for o in brangs:assert rf(o+0x3fc)==50000
C.flags.grappleRange=False;C.flags.batarangRange=False;C.loop()
print('GADGET SUBCLASS / RANGE TESTS PASSED',len(grapples),len(brangs))
print('COMBAT AND MASKED RESTORE TESTS PASSED')
before=len(writes);current[0]=pid+1;C.loop();assert len(writes)==before
current[0]=pid
write(p+4,0xffffffff,'int');before=len(writes);C.loop();assert len(writes)==before
print('RETARGET / STALE POINTER GUARDS PASSED')
C.status('TEST STATUS');assert rs(C.statusAddress,500)=='TEST STATUS'
assert C.damageWrites>0
print('QUIET STATUS / ACTIVATION RESCAN TESTS PASSED')
C.shutdown();pm.close()
print('All writes stayed in Python simulation. Live game unchanged.')
