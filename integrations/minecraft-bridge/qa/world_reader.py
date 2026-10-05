from __future__ import annotations
import gzip, io, re, struct, zlib
from collections import OrderedDict
from pathlib import Path

TAG_End=0; TAG_Byte=1; TAG_Short=2; TAG_Int=3; TAG_Long=4; TAG_Float=5; TAG_Double=6; TAG_Byte_Array=7; TAG_String=8; TAG_List=9; TAG_Compound=10; TAG_Int_Array=11; TAG_Long_Array=12
class Tag:
    __slots__=('type','value')
    def __init__(self,t,v): self.type=t; self.value=v

def _ru8(f): return struct.unpack('>B',f.read(1))[0]
def _ri8(f): return struct.unpack('>b',f.read(1))[0]
def _ri16(f): return struct.unpack('>h',f.read(2))[0]
def _ri32(f): return struct.unpack('>i',f.read(4))[0]
def _ri64(f): return struct.unpack('>q',f.read(8))[0]
def _rf32(f): return struct.unpack('>f',f.read(4))[0]
def _rf64(f): return struct.unpack('>d',f.read(8))[0]
def _rstr(f):
    n=struct.unpack('>H',f.read(2))[0]
    return f.read(n).decode('utf-8')
def _payload(f,t):
    if t==TAG_Byte:return _ri8(f)
    if t==TAG_Short:return _ri16(f)
    if t==TAG_Int:return _ri32(f)
    if t==TAG_Long:return _ri64(f)
    if t==TAG_Float:return _rf32(f)
    if t==TAG_Double:return _rf64(f)
    if t==TAG_Byte_Array:
        n=_ri32(f); return f.read(n)
    if t==TAG_String:return _rstr(f)
    if t==TAG_List:
        et=_ru8(f); n=_ri32(f); return et,[Tag(et,_payload(f,et)) for _ in range(n)]
    if t==TAG_Compound:
        d=OrderedDict()
        while True:
            et=_ru8(f)
            if et==0:break
            name=_rstr(f); d[name]=Tag(et,_payload(f,et))
        return d
    if t==TAG_Int_Array:return [_ri32(f) for _ in range(_ri32(f))]
    if t==TAG_Long_Array:return [_ri64(f) for _ in range(_ri32(f))]
    raise ValueError(t)
def read_nbt(data):
    f=io.BytesIO(data); t=_ru8(f); name=_rstr(f); return name,Tag(t,_payload(f,t))

class RegionFile:
    def __init__(self,path:Path):
        self.path=path
        m=re.match(r'r\.(-?\d+)\.(-?\d+)\.mca$',path.name)
        self.rx,self.rz=int(m.group(1)),int(m.group(2)); self.data=path.read_bytes()
    @staticmethod
    def index(cx,cz): return (cx%32)+(cz%32)*32
    def has(self,cx,cz):
        i=self.index(cx,cz)*4; return int.from_bytes(self.data[i:i+3],'big')!=0
    def read(self,cx,cz):
        i=self.index(cx,cz)*4; off=int.from_bytes(self.data[i:i+3],'big')
        if not off:return None
        p=off*4096; ln=int.from_bytes(self.data[p:p+4],'big'); ctype=self.data[p+4]; payload=self.data[p+5:p+4+ln]
        raw=zlib.decompress(payload) if ctype==2 else gzip.decompress(payload) if ctype==1 else bytes(payload)
        return read_nbt(raw)

class Chunk:
    def __init__(self,root):
        self.root=root; self.sections={s.value['Y'].value:s for s in root.value['sections'].value[1]}; self.cache={}
    @staticmethod
    def _key(p):
        d=p.value; name=d['Name'].value
        props=tuple(sorted((k,v.value) for k,v in d.get('Properties',Tag(TAG_Compound,{})).value.items())) if 'Properties' in d else ()
        return name,props
    def _decode(self,sy):
        if sy in self.cache:return self.cache[sy]
        s=self.sections[sy]; bs=s.value['block_states'].value; pals=bs['palette'].value[1]; palette=[self._key(p) for p in pals]
        if len(palette)==1 or 'data' not in bs: vals=[0]*4096
        else:
            bits=max(4,(len(palette)-1).bit_length()); vpl=64//bits; mask=(1<<bits)-1; vals=[]
            for raw in bs['data'].value:
                w=raw & ((1<<64)-1)
                for j in range(vpl):
                    vals.append((w>>(j*bits))&mask)
                    if len(vals)==4096:break
                if len(vals)==4096:break
            vals += [0]*(4096-len(vals))
        self.cache[sy]=(palette,vals); return palette,vals
    def block_state(self,x,y,z):
        sy=y//16
        if sy not in self.sections:return ('minecraft:air',())
        palette,vals=self._decode(sy); idx=(y&15)*256+(z&15)*16+(x&15); return palette[vals[idx]]
    def block(self,x,y,z): return self.block_state(x,y,z)[0]

class WorldReader:
    def __init__(self,world_dir:Path):
        self.world_dir=Path(world_dir); self.regions={}; self.chunks={}
        for p in (self.world_dir/'region').glob('r.*.*.mca'):
            r=RegionFile(p); self.regions[(r.rx,r.rz)]=r
    def chunk(self,x,z):
        cx,cz=x//16,z//16; key=(cx,cz)
        if key not in self.chunks:
            reg=self.regions.get((cx//32,cz//32))
            if reg is None or not reg.has(cx,cz): return None
            q=reg.read(cx,cz)
            if q is None:return None
            self.chunks[key]=Chunk(q[1])
        return self.chunks[key]
    def block_state(self,x,y,z):
        ch=self.chunk(x,z); return ch.block_state(x,y,z) if ch else ('minecraft:air',())
    def block(self,x,y,z): return self.block_state(x,y,z)[0]
