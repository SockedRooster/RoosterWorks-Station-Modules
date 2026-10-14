"""Independent structural/state checks for the authorized 0.75 dev2 changes."""
from pathlib import Path
import sys,math,hashlib,json,subprocess
from collections import Counter
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from config_nodes import parse,dump
from native_model import load,walk
from hotfix_assets import check_digest
GD=ROOT/'GameData/RoosterWorksStationModules'
for path,digest in json.loads((ROOT/'Tools/editor075_baseline.json').read_text()).items():
    assert check_digest(ROOT,path,digest),('Existing accepted asset changed',path)
assert len(list((GD/'Models').glob('RW_*.mu')))==41
assert len(list((GD/'Parts').glob('RW_*.cfg')))==43
for size,scale in ((250,1),(375,1.5),(500,2)):
    p=parse((GD/f'Parts/RW_TUBL_{size}.cfg').read_text()).children[0]
    old=parse((GD/f'Parts/RW_TUB_{size}.cfg').read_text()).children[0]
    assert p.get('CrewCapacity')=='0' and p.get('rescaleFactor')=='1'
    for key in ('mass','cost','entryCost'):assert math.isclose(float(p.get(key)),2*float(old.get(key)))
    assert float(p.get('node_stack_top').split(',')[1])==2*scale
    assert float(p.get('node_stack_bottom').split(',')[1])==-2*scale
    model=load(GD/f'Models/RW_TUBL_{size}.mu');nodes=[n for _,n in walk(model.root)]
    solids=[n['collider']['mesh'] for n in nodes if 'collider' in n]
    assert len(solids)==1
    collider=solids[0];assert math.isclose(max(v[1] for v in collider['vertices']),2*scale,abs_tol=1e-6)
    assert math.isclose(max(math.hypot(v[0],v[2]) for v in collider['vertices']),1.198*scale,abs_tol=1e-6)
    edges=Counter()
    for tri in collider['submeshes'][0]:
        points=[tuple(round(x,5) for x in collider['vertices'][i]) for i in tri]
        for a,b in zip(points,points[1:]+points[:1]):edges[tuple(sorted((a,b)))]+=1
    assert set(edges.values())=={2},'Open collider'
    assert len(model.materials)==1+max(i for n in nodes for i in n.get('materials',[])), 'Trailing unused MU materials'
    assert f'rwm_tublabel_long_{size}' in {t['name'] for t in model.textures}
    for n in nodes:
        if 'mesh' not in n:continue
        assert np.allclose(np.linalg.norm(n['mesh']['normals'],axis=1),1,atol=1e-5)
        assert len(n['mesh']['vertices'])==len(n['mesh']['uvs'])
    print('PASS long native tube',size,'nodes, closed collision, diameter, UVs, mass/cost')
science=parse((GD/'Compatibility/ZZZScienceStorage075.cfg').read_text())
for n,size,factor in zip(science.children,(250,375,500),(1,3.375,8)):
    assert n.header==f'@PART[RW_LAB_{size}]:NEEDS[Kerbalism,FeatureScience]:FINAL'
    d=n.children[0];assert float(d.get('%dataCapacity'))==250*factor
    assert d.get('%maxDataCapacityFactor')=='10' and d.get('%maxSampleCapacityFactor')=='10'
    assert float(d.get('%effectiveDataCapacity'))==250*factor
    assert float(n.children[1].get('volumeFactor'))==factor
    assert not any(c.header=='RESOURCE' for c in n.children)
    assert 'CMD' not in n.header
assert 'ZZZScienceStorage075.cfg'>max('StorageBalance.cfg','Family500.cfg')
ui=parse((GD/'Compatibility/EditorAppearance.cfg').read_text())
assert ui.children[1].header.endswith(':NEEDS[B9PartSwitch]:FOR[RoosterWorksStationModules]')
assert [len(c.children) for c in ui.children[1].children]==[2,8]
for switch in ui.children[1].children:
    assert switch.get('switchInFlight')=='false'
    for s in switch.children:assert s.header=='SUBTYPE' and not s.children and not s.get('transform') and not s.get('tankType')
subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'Tools/test-editor-menu.ps1')],check=True)
print('PASS dev2: 200 prior GameData assets protected except version/ring registrations; LAB-only ten-step proportional storage, optional cosmetic swatches, 41 current native parts')
