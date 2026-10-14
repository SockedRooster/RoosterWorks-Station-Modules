"""Native AIR exit/ladder, closed collider, readable UVs and part semantics."""
from pathlib import Path

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Source'))
from electric_charge_balance import check_preserved
from collections import Counter
import sys,math,json,hashlib
from native_model import load,walk
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
import build_air250 as b
model=load(b.MODELS/(b.PART+'.mu'));nodes={n['name']:n for _,n in walk(model.root)}
air=nodes['RW_AIR250_EVA_Airlock'];ladder=nodes['RW_AIR250_EVA_Ladder']
for node,tag,size,rotation in ((air,'Airlock',(.72,.78,.40),(0,0,0,1)),(ladder,'Ladder',(.86,1.64,.70),(0,1,0,0))):
    assert node['tag']==tag and node['layer']==21
    assert node['rotation']==rotation and node['scale']==(1,1,1)
    assert abs(node['position'][1]+.15)<1e-6 and abs(node['position'][2]-1.43)<1e-6 and node['position'][0]==0
    assert node['collider']['type']=='box' and node['collider']['trigger']==1
    assert all(abs(x-y)<1e-6 for x,y in zip(size,node['collider']['size']))
solids=[n for n in nodes.values() if 'collider' in n and not n['collider']['trigger']]
assert len(solids)==1 and solids[0]['collider']['convex']==1
mesh=solids[0]['collider']['mesh'];triangles=mesh['submeshes'][0];vertices=mesh['vertices'];edges=Counter()
assert len(triangles)==96
def sub(a,c):return tuple(x-y for x,y in zip(a,c))
def dot(a,c):return sum(x*y for x,y in zip(a,c))
origin=(0,-.15,1.43-.5)
for tri in triangles:
    p,q,r=[vertices[i] for i in tri]
    u=sub(q,p);v=sub(r,p);normal=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
    assert max(dot(normal,sub(a,p)) for a in vertices)<1e-6
    assert dot(normal,sub(origin,p))<0,'EVA clearance ray starts outside solid hull'
    points=[tuple(round(x,6) for x in a) for a in (p,q,r)]
    for i in range(3):edges[tuple(sorted((points[i],points[(i+1)%3])))]+=1
assert set(edges.values())=={2}
for node in nodes.values():
    if 'mesh' not in node:continue
    m=node['mesh'];assert len(m['vertices'])<65535
    assert all(abs(p[1])<=1.200001 for p in m['vertices'])
    for tri in m['submeshes'][0]:
        a,c,d=tri;p,q,r=[m['vertices'][i] for i in tri]
        u=sub(q,p);v=sub(r,p);n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
        assert dot(n,m['normals'][a])>1e-15,'Inverted visual triangle'
        tex=model.textures[model.materials[node['materials'][0]]['properties']['_MainTex']['index']]['name']
        if tex in ('rwm_crest','rwm_airlabel','rwm_detail','rwm_cladding','rwm_cladding_white'):
            u1,v1=sub(m['uvs'][c],m['uvs'][a]);u2,v2=sub(m['uvs'][d],m['uvs'][a])
            assert u1*v2-u2*v1<0,'Mirrored badge'
for tex in model.textures:assert (b.MODELS/(tex['name']+'.png')).exists()
assert nodes['RW_AirGlass']['materials']
cfg=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_AIR_250.cfg').read_text()
for value in ('CrewCapacity = 2','mass = 1.85','vesselType = Station','InventorySlots = 2','packedVolumeLimit = 120','amount = 0','includedRenderer = RW_AirGlass','mk2CockpitStandardInternals'):
    assert value in cfg,value
for value in ('ModuleCommand','ModuleDockingNode','ModulePartVariants','ModuleRWStationHatch','ModuleAnimateGeneric'):assert value not in cfg
assert 'node_stack_top = 0, 1.2, 0, 0, 1, 0, 2' in cfg and 'node_stack_bottom = 0, -1.2, 0, 0, -1, 0, 2' in cfg
golden=json.loads((ROOT/'Tools/airlock_baseline.json').read_text())
for path,digest in golden.items():check_preserved(ROOT,path,digest)
patch=(ROOT/'GameData/RoosterWorksStationModules/Compatibility/AirlockKerbalism.cfg').read_text()
assert 'NEEDS[Kerbalism,FeatureHabitat]' in patch and '%volume = 6' in patch and '%surface = 20' in patch
print('PASS AIR native geometry, one closed convex hull, ray-origin containment, outward exit, inward ladder, readable badges and light renderer')
print('PASS AIR two seats, 2.4m stack envelope, stock inventory/external station power, conditional Habitat; accepted six-module GameData preserved except EC balance')
print('NOTE actual stock EVA/auto-grab/climb/boarding, IVA and Kerbalism pressure require KSP flight tests')
