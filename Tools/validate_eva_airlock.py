#!/usr/bin/env python3
"""Validate the binary EVA airlock collider KSP needs to spawn crew outside."""
from pathlib import Path
import math, struct

ROOT=Path(__file__).resolve().parents[1]
mu=(ROOT/'GameData/RoosterWorksStationModules/Models/RW_HAB_250.mu').read_bytes()
part=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_HAB_250.cfg').read_text()
source=(ROOT/'Source/build_hab250.py').read_text()


def decode_mu_string(buf, start):
    pos=start
    shift=0
    length=0
    while True:
        v=buf[pos];pos+=1
        length |= (v&0x7f)<<shift
        if v&0x80==0: break
        shift+=7
        assert shift<=28
    return buf[pos:pos+length].decode('utf-8'),pos+length

name='RW_HAB250_EVA_Airlock'
marker=bytes([len(name)])+name.encode('utf-8')
assert mu.count(marker)==1, 'Expected exactly one physical airlock transform'
i=mu.index(marker)+len(marker)
x,y,z,rx,ry,rz,rw,sx,sy,sz=struct.unpack_from('<10f',mu,i)
i+=40
assert struct.unpack_from('<i',mu,i)[0]==24; i+=4
label,i=decode_mu_string(mu,i)
assert label=='Airlock',label
layer=struct.unpack_from('<i',mu,i)[0];i+=4
assert layer==21,layer # Part Triggers
assert struct.unpack_from('<i',mu,i)[0]==28;i+=4 # BoxCollider2
trigger=mu[i];i+=1
assert trigger==1, 'EVA collider must be a trigger rather than a solid obstruction'
a,b,c,ox,oy,oz=struct.unpack_from('<6f',mu,i)
assert abs(a-.72)<1e-5 and abs(b-.78)<1e-5 and abs(c-.4)<1e-5
assert max(abs(ox),abs(oy),abs(oz))<1e-5
assert (sx,sy,sz)==(1,1,1)
expected_y=(-1.730+2*(3.460/8)+.014 + -1.730+3*(3.460/8)-.014)*.5
assert abs(y-expected_y)<1e-5
assert abs(math.hypot(x,z)-1.43)<1e-5, 'Airlock spawn not clear of hull'
angle=math.tau*2/12
assert abs(math.atan2(x,z)-angle)<1e-5
assert abs(ry-math.sin(angle/2))<1e-5 and abs(rw-math.cos(angle/2))<1e-5
assert abs(rx)+abs(rz)<1e-6
assert 'RW_HAB250_EVA_Airlock =' not in part, 'Do not switch the airlock off in stock PartVariants; KSP caches it at Part.Awake'
assert 'WindowBankStandard = false' in part and 'SideHatch = true' in part
assert 'CrewCapacity = 4' in part
assert 'tag=\'Airlock\',layer=21,trigger=True' in source
print('PASS KSP native EVA Airlock: trigger collider, layer 21, outward alignment, native trigger preserved; runtime gates access by variant')
print('NOTE: KSP runtime EVA/reboarding require confirmation; SideHatch permits access, Standard disables access at runtime.')
