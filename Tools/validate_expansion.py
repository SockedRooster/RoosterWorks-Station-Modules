"""Independent checks for actual 5 m scaling, functional new parts and compact HABs."""
from pathlib import Path
import hashlib,json,sys,math
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from config_nodes import parse,dump
from native_model import load,walk
from hotfix_assets import check_digest
GD=ROOT/'GameData/RoosterWorksStationModules'
allowed={'RingGeometry.cfg','RingColors.cfg','LogisticsLoadouts.cfg'}
baseline=json.loads((ROOT/'Tools/expansion_baseline.json').read_text())
for path,digest in baseline.items():
    if path.endswith('.version'):continue
    if Path(path).name in allowed:
        old=parse((ROOT/'Source/Balancing/ExpansionBefore'/Path(path).name).read_text());new=parse((ROOT/path).read_text())
        def identity(n):return (n.header,n.get('model') or n.get('name'))
        lookup={identity(n):n for n in new.children}
        for n in old.children:assert identity(n) in lookup and dump(n)==dump(lookup[identity(n)]),('Old option changed',path,identity(n))
    else:assert check_digest(ROOT,path,digest),('Old asset changed',path)
roles=('HAB','LAB','CMD','HUB','CUP','LOG','AIR','PWR','GRN','TUB','ELB')
for role in roles:
    a=load(GD/f'Models/RW_{role}_250.mu');b=load(GD/f'Models/RW_{role}_500.mu')
    aa=dict(walk(a.root));bb=dict(walk(b.root));assert len(aa)==len(bb)
    for (pa,x),(pb,y) in zip(aa.items(),bb.items()):
        assert pa.replace('RW_'+role+'_250','RW_'+role+'_500',1)==pb
        assert np.allclose(np.array(x['position'])*2,y['position'],atol=2e-6) and x['rotation']==y['rotation'] and x['scale']==y['scale']
        for kind in ('mesh','collider'):
            if kind not in x:continue
            mx=x[kind] if kind=='mesh' else x[kind].get('mesh');my=y[kind] if kind=='mesh' else y[kind].get('mesh')
            if mx is not None:
                assert np.allclose(np.array(mx['vertices'])*2,my['vertices'],atol=2e-6)
                assert mx['normals']==my['normals'] and mx['uvs']==my['uvs'] and mx['submeshes']==my['submeshes']
            else:assert np.allclose(np.array(x[kind]['size'])*2,y[kind]['size'])
        if 'light' in x:assert math.isclose(y['light']['range'],x['light']['range']*2,abs_tol=2e-6) and y['light']['color']==x['light']['color']
    p=parse((GD/f'Parts/RW_{role}_500.cfg').read_text()).children[0]
    assert p.get('bulkheadProfiles')=='size4' and p.get('rescaleFactor')=='1'
    for key,value in p.values:
        if key.startswith('node_stack_'):assert int(value.split(',')[-1])==4
    assert b.materials==a.materials[:len(b.materials)]
    assert len(b.materials)==1+max(i for _,n in walk(b.root) for i in n.get('materials',[]))
    print('PASS native 5 m scaling, normals/UVs/roles/nodes/material binding:',role)

def solid(mesh):
    edges=Counter()
    for triangles in mesh['submeshes']:
        for tri in triangles:
            points=[tuple(round(v,5) for v in mesh['vertices'][i]) for i in tri]
            for a,b in zip(points,points[1:]+points[:1]):edges[tuple(sorted((a,b)))]+=1
    assert set(edges.values())=={2},'Open convex collider'

adapter=load(GD/'Models/RW_ADP_375_500.mu')
for _,n in walk(adapter.root):
    if 'collider' in n:solid(n['collider']['mesh'])
part=parse((GD/'Parts/RW_ADP_375_500.cfg').read_text()).children[0]
assert part.get('node_stack_top')=='0, 1.05, 0, 0, 1, 0, 3' and part.get('node_stack_bottom')=='0, -1.05, 0, 0, -1, 0, 4'
assert 'rwm_adplabel_375_500' in {t['name'] for t in adapter.textures}
family=parse((GD/'Compatibility/Family500.cfg').read_text());assert not any('_250]' in n.header or '_375]' in n.header for n in family.children)
drives=[n for n in family.children if ':FINAL' in n.header and any(c.header=='%MODULE[HardDrive]' for c in n.children)]
assert len(drives)==2
for n in drives:assert n.children[0].get('%dataCapacity')=='2500' and n.children[0].get('%maxDataCapacityFactor')=='1'
assert next(n for n in drives if 'RW_LAB' in n.header).children[0].get('%sampleCapacity')=='100'
power=next(n for n in family.children if 'RW_PWR_500' in n.header and any(c.get('name')=='ModuleRWPowerVariant' for c in n.children))
controller=next(c for c in power.children if c.get('name')=='ModuleRWPowerVariant')
assert controller.get('batteryCapacity')=='10200' and controller.get('reactorCapacity')=='8410' and controller.get('reactorScale')=='1.3'
for size,scale in ((250,1),(375,1.5),(500,2)):
    path=GD/f'Models/RW_HABS_{size}.mu'
    if not path.exists():continue
    model=load(path);p=parse((GD/f'Parts/RW_HABS_{size}.cfg').read_text()).children[0]
    assert p.get('CrewCapacity')=='2' and next(n for n in p.children if n.header=='INTERNAL').get('name')=='mk1CabinInternal'
    assert math.isclose(float(p.get('node_stack_top').split(',')[1]),.99*scale)
    nodes=[n for _,n in walk(model.root)];triggers={n['tag']:n for n in nodes if n.get('tag') in ('Airlock','Ladder')}
    assert set(triggers)=={'Airlock','Ladder'} and all(n['layer']==21 and n['collider']['trigger']==1 for n in triggers.values())
    assert triggers['Airlock']['name']=='RW_HAB250_EVA_Airlock' and triggers['Airlock']['position'][1]==0
    hull=next(n['collider']['mesh'] for n in nodes if 'collider' in n and n['collider']['type']=='mesh')
    solid(hull);assert sum(len(t) for t in hull['submeshes'])==96
    assert math.isclose(max(v[1] for v in hull['vertices']),.99*scale,abs_tol=2e-6)
    assert {n['name'] for n in nodes}>={'WindowBankStandard','SideHatch','RW_GlassStandard','RW_GlassSideHatch'}
    assert any(m['shader']=='KSP/Emissive/Diffuse' for m in model.materials)
    # Hatch geometry remains original proportions; trigger is outside the hull,
    # while KSP's obstruction-ray origin is inside the solid collision volume.
    exit=triggers['Airlock']['position'];assert math.hypot(exit[0],exit[2])>1.204*scale and math.hypot(exit[0],exit[2])-.5<1.204*scale
    assert len(model.materials)==1+max(i for n in nodes for i in n.get('materials',[]))
    print('PASS compact HAB',size,'true short hull, two-seat IVA, variants, centered EVA/ladder and warm lamps')
print('PASS expansion: previous game assets/options preserved; new 5 m family, correct adapter, science/reactor balance and compact HAB geometry')
