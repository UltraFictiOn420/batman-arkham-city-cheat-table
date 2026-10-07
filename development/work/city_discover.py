import sys,struct
from ue3_inspect import ProcessMemory
import pefile

pm=ProcessMemory(int(sys.argv[1]))
p=pefile.PE(r'C:\Program Files (x86)\Steam\steamapps\common\Batman Arkham City GOTY\Binaries\Win32\BatmanAC.exe')
base=p.OPTIONAL_HEADER.ImageBase
raw=bytearray(p.OPTIONAL_HEADER.SizeOfImage)
for address,size,protect,kind in pm.regions():
    lo=max(address,base); hi=min(address+size,base+len(raw))
    if lo<hi:
        chunk=pm.read(lo,hi-lo)
        raw[lo-base:lo-base+len(chunk)]=chunk
print('base',hex(base),'size',hex(len(raw)),flush=True)
for pat in ('7F 0A 8B 4C 24 0C 89 01 59 C2 08 00','29 03 8B 1B 8B 4C 24 14','01 03 8B 1B 8B 4C 24 14','F3 0F 11 86 EC 00 00 00 89 96'):
    needle=bytes.fromhex(pat); start=0; hits=[]
    while True:
        index=raw.find(needle,start)
        if index<0:break
        hits.append(hex(base+index));start=index+1
    print('AOB',pat,hits,flush=True)
for i in range(0,len(raw)-12,4):
    data,count,maximum=struct.unpack_from('<Iii',raw,i)
    if not (5000<count<=maximum<500000 and data>0x10000): continue
    sample=pm.read(data,32)
    if len(sample)<32:continue
    ptrs=struct.unpack('<8I',sample)
    for off in (8,12,16):
        vals=[pm.read(a+off,32).split(b'\0')[0] for a in ptrs[:4] if a]
        if vals and (vals[0]==b'None' or pm.read(ptrs[0]+off,10)==b'N\0o\0n\0e\0\0\0'): print('NAMES',hex(base+i),hex(data),count,'offset',off,vals,flush=True)
    vals=[pm.read(a,48) for a in ptrs if a]
    if len(vals)>4 and all(len(v)==48 and base<=struct.unpack_from('<I',v)[0]<base+len(raw) for v in vals):
        print('OBJECTS',hex(base+i),hex(data),count,'first',[(hex(a),v.hex()) for a,v in zip(ptrs,vals)][:2],flush=True)
pm.close()
