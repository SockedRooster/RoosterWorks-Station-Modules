"""Verify new large native exports, real stack sizes, EVA clearance and scaling."""
from pathlib import Path

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Source'))
from electric_charge_balance import check_preserved
import sys,math,json,hashlib
import numpy as np
from collections import Counter
from native_model import load,walk
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from build_family375 import ROLES,SCALE,VOLUME,AREA
from config_nodes import parse
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
for role in ROLES:
    old=load(MODELS/f'RW_{role}_250.mu');new=load(MODELS/f'RW_{role}_375.mu')
    old_nodes=list(walk(old.root));new_nodes=list(walk(new.root));assert len(old_nodes)==len(new_nodes)
    colliders=[];tags=[];tri_count=0
    for (_,a),(_,b) in zip(old_nodes,new_nodes):
        assert np.allclose(np.array(a['position'])*SCALE,b['position'],atol=2e-7)
        assert a['rotation']==b['rotation'] and a['scale']==b['scale'] and a['tag']==b['tag'] and a['layer']==b['layer']
        if a is not old.root:assert a['name']==b['name'],'Renderer/variant/trigger binding changed'
        if a['tag'] in ('Airlock','Ladder'):tags.append(b)
        for key in ('mesh','collider','light'):assert (key in a)==(key in b)
        if 'mesh' in a:
            am,bm=a['mesh'],b['mesh'];tri_count+=sum(len(t) for t in bm['submeshes'])
            assert am['submeshes']==bm['submeshes'] and am['normals']==bm['normals'] and am['uvs']==bm['uvs']
            assert np.allclose(np.array(am['vertices'])*SCALE,bm['vertices'],atol=4e-7)
            assert a['materials']==b['materials'] and len(bm['vertices'])<65535
        if 'light' in a:
            assert math.isclose(b['light']['range'],a['light']['range']*SCALE,abs_tol=3e-7)
            assert b['light']['intensity']==a['light']['intensity']
        if 'collider' in a:
            ac,bc=a['collider'],b['collider'];assert ac['type']==bc['type'] and ac['trigger']==bc['trigger']
            if ac['type']=='box':
                assert np.allclose(np.array(ac['size'])*SCALE,bc['size'],atol=2e-7)
                assert np.allclose(np.array(ac['center'])*SCALE,bc['center'],atol=2e-7)
            else:
                am,bm=ac['mesh'],bc['mesh'];assert am['submeshes']==bm['submeshes'] and ac['convex']==bc['convex']==1
                assert np.allclose(np.array(am['vertices'])*SCALE,bm['vertices'],atol=4e-7)
                colliders.append(bm);edges=Counter()
                for tri in bm['submeshes'][0]:
                    p,q,r=[bm['vertices'][i] for i in tri]
                    keys=[tuple(round(v,5) for v in t) for t in (p,q,r)]
                    for i in range(3):edges[tuple(sorted((keys[i],keys[(i+1)%3])))]+=1
                assert set(edges.values())=={2},('Open large collider',role)
    assert old.materials==new.materials
    for tex in new.textures:assert (MODELS/(tex['name']+'.png')).exists()
    if role in ('HAB','AIR'):
        assert len(tags)==2
        hatch=next(n for n in tags if n['tag']=='Airlock')
        x,y,z,w=hatch['rotation'];forward=(2*(x*z+w*y),2*(y*z-w*x),1-2*(x*x+y*y))
        length=math.sqrt(dot(hatch['position'],hatch['position']))
        radial=tuple(v/length for v in hatch['position'])
        hull=colliders[0]
        for direction in (forward,radial):
            # Check named hatch forward and the legacy validator's radial ray.
            origin=tuple(hatch['position'][i]-.5*direction[i] for i in range(3))
            for tri in hull['submeshes'][0]:
                p,q,r=[hull['vertices'][i] for i in tri];n=cross(sub(q,p),sub(r,p))
                assert dot(n,sub(origin,p))<0,('EVA ray origin outside large hull',role)
        assert hatch['layer']==21
    small=parse((ROOT/f'GameData/RoosterWorksStationModules/Parts/RW_{role}_250.cfg').read_text()).children[0]
    big=parse((ROOT/f'GameData/RoosterWorksStationModules/Parts/RW_{role}_375.cfg').read_text()).children[0]
    assert big.get('name')==f'RW_{role}_375' and big.get('rescaleFactor')=='1'
    assert 'size3' in big.get('bulkheadProfiles') and 'size2' not in big.get('bulkheadProfiles')
    assert small.get('CrewCapacity')==big.get('CrewCapacity')
    assert math.isclose(float(big.get('mass')),float(small.get('mass'))*VOLUME,abs_tol=1e-7)
    smods=[n.get('name') for n in small.children if n.header=='MODULE'];bmods=[n.get('name') for n in big.children if n.header=='MODULE']
    assert smods==bmods
    assert [n.get('name') for n in small.children if n.header=='INTERNAL']==[n.get('name') for n in big.children if n.header=='INTERNAL']
    for key,value in small.values:
        if not key.startswith('node_stack_'):continue
        source=[float(x.strip()) for x in value.split(',')];target=[float(x.strip()) for x in big.get(key).split(',')]
        assert np.allclose(np.array(source[:3])*SCALE,target[:3]) and source[3:6]==target[3:6] and target[6]==3
    print('PASS',role+'-375:',tri_count,'triangles; native geometry/collision scale, label assets, size-3 nodes, crew/IVA/equipment retained')
# Check actual emitted compatibility nodes, including greenhouse source copy.
patch=parse((ROOT/'GameData/RoosterWorksStationModules/Compatibility/LargeFamilyKerbalism.cfg').read_text())
for node in patch.children:
    assert '_250' not in node.header and ':NEEDS[Kerbalism,' in node.header
    def visit(n):
        if n.header=='@MODULE[Greenhouse]':
            assert n.get('@crop_size *')=='1.6875' and n.get('@ec_rate *')=='1.6875'
            assert n.get('%lamps')=='RW_GreenhouseLamps'
        for c in n.children:visit(c)
    visit(node)
golden=json.loads((ROOT/'Tools/large_family_baseline.json').read_text())
for path,digest in golden.items():check_preserved(ROOT,path,digest)
print('PASS baseline: original nine non-greenhouse parts, adapter, patches, textures and runtime preserved')
print('NOTE large stack fit, crew/EVA, Kerbalism operation, inspection-light switch and performance require KSP testing')
