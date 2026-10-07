import sys,struct,re
from functools import lru_cache
from ue3_inspect import ProcessMemory

pm=ProcessMemory(int(sys.argv[1]))
nd=pm.u32(0x16019c8); nc=pm.u32(0x16019cc)
np=struct.unpack('<%dI'%nc,pm.read(nd,nc*4))
od=pm.u32(0x1643ce0); oc=pm.u32(0x1643ce4)
op=struct.unpack('<%dI'%oc,pm.read(od,oc*4))
@lru_cache(None)
def name(i):
    if i is None or i>=nc:return '?'
    e=np[i];raw=pm.read(e+16,256)
    if (pm.u32(e+8) or 0)&1:return raw.decode('utf-16le',errors='ignore').split('\0')[0]
    return raw.split(b'\0')[0].decode('latin1')
@lru_cache(None)
def oname(o):return name(pm.u32(o+0x1c)) if o else '?'
@lru_cache(None)
def cn(o):return oname(pm.u32(o+0x24))
def path(o):
    parts=[]
    for _ in range(10):
        if not o:break
        parts.append(oname(o));o=pm.u32(o+0x18)
    return '.'.join(reversed(parts))

mode=sys.argv[2];pattern=re.compile(sys.argv[3],re.I)
owner=re.compile(sys.argv[4] if len(sys.argv)>4 else '.*',re.I)
for idx,o in enumerate(op):
    if not o:continue
    n=oname(o);c=cn(o)
    if mode=='instances' and pattern.search(c):print(hex(o),c,path(o))
    if mode=='combat' and pattern.search(c) and not n.startswith('Default__'):
        raw=pm.read(o,0xB10)
        if len(raw)==0xB10:
            print(hex(o),c,'HP',struct.unpack_from('<i',raw,0x2C4)[0],'MAX',struct.unpack_from('<f',raw,0xB00)[0],'FLAGS',hex(struct.unpack_from('<I',raw,0xA0)[0]),'POS',struct.unpack_from('<fff',raw,0x48),path(o))
    if mode=='classes' and c=='Class' and pattern.search(n):
        print(hex(o),n,'super',oname(pm.u32(o+0x2c)))
    if mode=='functions' and c=='Function' and pattern.search(n) and owner.search(oname(pm.u32(o+0x18))):
        raw=pm.read(o,0x90)
        print(hex(o),path(o),' '.join(f'{j:x}:{struct.unpack_from("<I",raw,j)[0]:x}' for j in range(0x38,0x90,4)))
    if mode=='properties' and c.endswith('Property') and pattern.search(n):
        own=oname(pm.u32(o+0x18))
        if owner.search(own):
            raw=pm.read(o,0x80)
            packed=struct.unpack_from('<I',raw,0x3c)[0]
            print(hex(o),c,own,n,'offset',hex(packed>>16),'size',packed&65535,'mask',hex(struct.unpack_from('<I',raw,0x58)[0]))
pm.close()
