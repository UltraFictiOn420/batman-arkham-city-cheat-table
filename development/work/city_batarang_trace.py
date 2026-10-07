import sys,struct
from functools import lru_cache
from ue3_inspect import ProcessMemory
pm=ProcessMemory(int(sys.argv[1]))
nd=pm.u32(0x16019c8);nc=pm.u32(0x16019cc)
np=struct.unpack('<%dI'%nc,pm.read(nd,nc*4))
od=pm.u32(0x1643ce0);oc=pm.u32(0x1643ce4)
ops=set(struct.unpack('<%dI'%oc,pm.read(od,oc*4)))
@lru_cache(None)
def name(o):
    if not o:return '?'
    i=pm.u32(o+0x1c)
    if i is None or i>=nc:return '?'
    e=np[i];r=pm.read(e+16,128)
    return r.decode('utf-16le',errors='ignore').split('\0')[0] if (pm.u32(e+8) or 0)&1 else r.split(b'\0')[0].decode('latin1')
def path(o):return name(pm.u32(o+0x18))+'.'+name(o)
for o in ops:
    if not o:continue
    if name(pm.u32(o+0x24))=='Function' and path(o) in ['RPawnVillain.HitByBatarang','RBatarangProjectile.Touch','RPawnVillain.TakeDamage']:
        data=pm.u32(o+0x44);size=(pm.u32(o+0x48) or 0)&0xffff
        raw=pm.read(data,size);print('\nFUNCTION',path(o),hex(o),'DATA',hex(data),'SIZE',size)
        for i in range(max(0,len(raw)-3)):
            ref=struct.unpack_from('<I',raw,i)[0]
            if ref and ref in ops:
                print(hex(i),path(ref),name(pm.u32(ref+0x24)),raw[max(0,i-6):min(len(raw),i+16)].hex(' '))
pm.close()
