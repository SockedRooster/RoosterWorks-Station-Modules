"""Validate actual native power geometry, passive battery and accepted baseline."""
from pathlib import Path

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Source'))
from electric_charge_balance import check_preserved
from collections import Counter
import math,json,hashlib,re,sys
from native_model import load,walk
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
import build_pwr250 as b
model=load(b.MODELS/(b.PART+'.mu'));solids=[];count=0
def sub(a,c):return tuple(x-y for x,y in zip(a,c))
def dot(a,c):return sum(x*y for x,y in zip(a,c))
def cross(a,c):return (a[1]*c[2]-a[2]*c[1],a[2]*c[0]-a[0]*c[2],a[0]*c[1]-a[1]*c[0])
for _,node in walk(model.root):
    assert node['tag']=='Untagged' and node['layer']==0,'Unexpected EVA/ladder trigger'
    if 'collider' in node:
        assert node['collider']['trigger']==0 and node['collider']['convex']==1
        solids.append(node['collider']['mesh'])
    if 'mesh' not in node:continue
    m=node['mesh'];count+=sum(len(tris) for tris in m['submeshes'])
    assert len(m['vertices'])<65535 and len(m['vertices'])==len(m['normals'])==len(m['uvs'])
    assert all(math.isfinite(x) for p in m['vertices']+m['normals']+m['uvs'] for x in p)
    assert all(abs(p[1])<=1.200001 and math.hypot(p[0],p[2])<1.30 for p in m['vertices'])
    for tris,material_id in zip(m['submeshes'],node['materials']):
        material=model.materials[material_id];assert material['shader']=='KSP/Diffuse'
        tex=model.textures[material['properties']['_MainTex']['index']]['name']
        assert tex!='rwm_glass','Crewless power core has no windows'
        for a,c,d in tris:
            p,q,r=[m['vertices'][i] for i in (a,c,d)]
            normal=cross(sub(q,p),sub(r,p));assert dot(normal,m['normals'][a])>1e-15,'Inverted face'
            if tex in ('rwm_crest','rwm_pwrlabel','rwm_pwrpanel','rwm_detail','rwm_cladding','rwm_cladding_white'):
                u1,v1=sub(m['uvs'][c],m['uvs'][a]);u2,v2=sub(m['uvs'][d],m['uvs'][a])
                assert u1*v2-u2*v1<0,(tex,'Mirrored label')
assert count==21772 and len(solids)==1
mesh=solids[0];assert len(mesh['submeshes'][0])==96
edges=Counter();vertices=mesh['vertices']
for tri in mesh['submeshes'][0]:
    p,q,r=[vertices[i] for i in tri];n=cross(sub(q,p),sub(r,p))
    assert dot(n,p)>0
    assert max(dot(n,sub(v,p)) for v in vertices)<1e-6,'Nonconvex solid'
    keys=[tuple(round(x,6) for x in v) for v in (p,q,r)]
    for i in range(3):edges[tuple(sorted((keys[i],keys[(i+1)%3])))]+=1
assert set(edges.values())=={2}
for tex in model.textures:assert (b.MODELS/(tex['name']+'.png')).exists()
cfg=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_PWR_250.cfg').read_text()
assert 'MODULE' not in cfg and 'INTERNAL' not in cfg
resources=re.findall(r'RESOURCE\s*\{([^{}]+)\}',cfg)
assert len(resources)==1 and 'name = ElectricCharge' in resources[0]
for field in ('amount = 2980','maxAmount = 2980'):assert field in resources[0]
for field in ('mass = 2.5','CrewCapacity = 0','vesselType = Station','category = Electrical','TechRequired = largeElectrics','attachRules = 1,0,1,1,0','node_stack_top = 0, 1.2, 0, 0, 1, 0, 2','node_stack_bottom = 0, -1.2, 0, 0, -1, 0, 2'):assert field in cfg
golden=json.loads((ROOT/'Tools/power_baseline.json').read_text())
for path,digest in golden.items():check_preserved(ROOT,path,digest)
print('PASS PWR:',count,'visual triangles; outward meshes, readable badges, one watertight convex 96-triangle collider, 2.4m stack envelope')
print('PASS PWR: passive 2980 EC battery; 0 crew; no generator, cooling module, command, IVA, EVA, light toggle or Habitat; prior seven modules preserved except authorized EC balance')
print('NOTE charge/discharge, Kerbalism electricity, external mounts and visual acceptance require KSP tests')
