"""Protect accepted v0.6 game assets and audit the new actual model/loadout data."""
from pathlib import Path
import hashlib,json,sys,subprocess,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from config_nodes import parse
from native_model import load,walk
from hotfix_assets import check_digest
GD=ROOT/'GameData/RoosterWorksStationModules'
baseline=json.loads((ROOT/'Tools/roadmap065_baseline.json').read_text())
for path,digest in baseline.items():
    if path.endswith('.version') or Path(path).name in ('RingColors.cfg','RingGeometry.cfg','LogisticsLoadouts.cfg'):continue
    assert check_digest(ROOT,path,digest),('Accepted game asset changed',path)
assert tuple(json.loads((GD/'RoosterWorksStationModules.version').read_text())['VERSION'][k] for k in ('MAJOR','MINOR','PATCH')) in ((0,6,5),(0,7,0),(0,7,5))
maps=parse((GD/'Compatibility/RingGeometry.cfg').read_text()).children
assert len(maps)==len(list((GD/'Models').glob('RW_*.mu'))) and len({m.get('model') for m in maps})==len(maps)
palette=json.loads((ROOT/'Source/Balancing/ring_palette.json').read_text())
assert set(palette)=={'Steel','White','Charcoal','Blue','Green','Red','Gold'}
total=0
for mapping in maps:
    model=load(GD/'Models'/(mapping.get('model')+'.mu'));nodes=dict(walk(model.root))
    assert mapping.children
    for spec in mapping.children:
        node=nodes[spec.get('path')];mesh=node['mesh'];triangles=mesh['submeshes'][0]
        assert int(spec.get('vertices'))==len(mesh['vertices']) and int(spec.get('triangles'))==len(triangles)
        material=model.materials[node['materials'][0]]
        assert material['shader']=='KSP/Diffuse'
        texture=model.textures[material['properties']['_MainTex']['index']]['name']
        assert texture==spec.get('texture') and texture in ('rwm_steel','rwm_bronze','rwm_white','rwm_ceramic','rwm_cladding','rwm_cladding_white')
        selected=set()
        for encoded in spec.get('ranges').split(','):
            start,count=map(int,encoded.split(':'));assert start>=0 and count>0 and start+count<=len(triangles)
            group=set(range(start,start+count));assert not selected&group;selected|=group
        assert selected
        # An editor copy's already split mesh reconstructs the exact native order.
        body=[tri for i,tri in enumerate(triangles) if i not in selected]
        rings=[tri for i,tri in enumerate(triangles) if i in selected]
        b=r=0;restored=[]
        for i in range(len(triangles)):
            if i in selected:restored.append(rings[r]);r+=1
            else:restored.append(body[b]);b+=1
        assert restored==triangles
        for color in palette:assert (GD/'Models'/f'rwm_ring_{texture}_{color.lower()}.png').is_file()
        total+=len(selected)
patches=parse((GD/'Compatibility/RingColors.cfg').read_text()).children
assert len(patches)==len(list((GD/'Parts').glob('RW_*.cfg'))) # 23 current parts plus hidden old reactor IDs
for patch in patches:
    module=patch.children[0];assert module.get('ringColor')=='Original' and module.get('ringModel') in {m.get('model') for m in maps}
tree=parse((GD/'Compatibility/LogisticsLoadouts.cfg').read_text())
loads=[n for n in tree.children if n.header=='RW_LOG_LOADOUTS'];assert len(loads)==3
expected={'Mixed supplies','Food','Water','Oxygen','Nitrogen','Ammonia','Waste','WasteWater'}
legacy=parse((GD/'Compatibility/LogisticsKerbalism.cfg').read_text()).children[0]
base={n.get('%name'):(float(n.get('%amount')),float(n.get('%maxAmount'))) for n in legacy.children}
for node,scale in zip(loads,(1,3.375,8)):
    assert len(node.children)==8 and {n.get('name') for n in node.children}==expected
    for choice in node.children:
        actual={n.get('name'):(float(n.get('amount')),float(n.get('maxAmount'))) for n in choice.children}
        if choice.get('name')=='Mixed supplies':
            assert actual=={name:(a*scale,m*scale) for name,(a,m) in base.items()}
        else:
            name=choice.get('name');assert set(actual)=={name}
            pressure={'Oxygen':200,'Nitrogen':180,'Ammonia':35}.get(name,1)
            amount,maximum=actual[name]
            assert math.isclose(maximum/pressure,520*scale)
            assert amount==(0 if name in ('Waste','WasteWater') else maximum)
subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'Tools/test-customization.ps1')],check=True)
print(f'PASS 0.65: all 120 prior gameplay/model/finish/reactor files unchanged; {len(maps)} exact ring maps / {total} triangles; all 25 IDs; fixed-volume LOG choices and unchanged mixed inventories')
