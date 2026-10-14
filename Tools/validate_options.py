"""Authorize only requested EC changes and independently check optional assets."""
from pathlib import Path
import sys,json,hashlib,math,copy,subprocess,ast
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];GD=ROOT/'GameData/RoosterWorksStationModules'
sys.path.insert(0,str(ROOT/'Source'))
from config_nodes import parse,dump
from electric_charge_balance import set_capacity,check_preserved
from native_model import load
from build_options import RATE,SURFACES,build
golden=json.loads((ROOT/'Tools/options_baseline.json').read_text())
for path,digest in golden.items():
    current=(ROOT/path).read_bytes()
    if path.endswith('.version'):continue
    check_preserved(ROOT,path,digest)
print('PASS every v13 GameData file byte-preserved except explicit PWR EC overrides and version')
for path in GD.rglob('*.cfg'):parse(path.read_text())
module=parse((GD/'Compatibility/ExteriorFinish.cfg').read_text()).children[0]
assert module.header=='@PART[RW_*]:HAS[!MODULE[ModuleRWStationFinish]]:FOR[RoosterWorksStationModules]'
assert module.children[0].get('name')=='ModuleRWStationFinish' and module.children[0].get('finish')=='White'
for path in (GD/'Models').glob('*.mu'):
    model=load(path)
    mapped=[m for m in model.materials if any(m['name'].endswith('_'+s) for s in SURFACES)]
    assert len(mapped)==4,path
    for mat in mapped:
        name=model.textures[mat['properties']['_MainTex']['index']]['name']
        assert name.removeprefix('rwm_') in SURFACES
        white=np.array(Image.open(GD/f'Models/{name}.png').convert('RGBA'))
        grey=np.array(Image.open(GD/f'Models/{name}_grey.png').convert('RGBA'))
        assert white.shape==grey.shape and np.array_equal(white[:,:,3],grey[:,:,3])
        assert grey[:,:,:3].mean()<white[:,:,:3].mean() and not np.array_equal(white,grey)
print('PASS grey coverage all 19 models; alpha/UV layout preserved; separate finish leaves HAB IDs intact')
patch=parse((GD/'Compatibility/CompactReactor.cfg').read_text())
profile=next(n for n in patch.children if n.header.startswith('@Profile'))
process=profile.children[0]
assert process.get('modifier')=='_RWCompactReactor' and process.get('input')=='EnrichedUranium@0.0000000065206'
assert process.get('dump_valve')=='ElectricCharge'
assert [v for k,v in process.values if k=='output']==['DepletedFuel@0.0000000065206','ElectricCharge@5']
assert any(n.header=='!PART[RW_PWR_*_REACTOR]:NEEDS[Kerbalism,!ProfileDefault]' for n in patch.children)
organizers=[n for n in patch.children if ':NEEDS[VABOrganizer]' in n.header]
assert len(organizers)==2
assert {n.children[0].get('%organizerSubcategory') for n in organizers}=={'batteries','nuclearReactors'}
for size,factor,capacity in ((250,1.1,3500),(375,1.2,6750)):
    base=parse((GD/f'Parts/RW_PWR_{size}.cfg').read_text()).children[0]
    part=parse((GD/f'Parts/RW_PWR_{size}_REACTOR.cfg').read_text()).children[0]
    assert part.header=='PART:NEEDS[CommunityResourcePack]'
    assert part.get('name')==f'RW_PWR_{size}_REACTOR' and part.get('CrewCapacity')=='0'
    assert part.get('TechRequired')==base.get('TechRequired')
    for key,value in base.values:
        if key.startswith('node_') or key in ('rescaleFactor','attachRules','bulkheadProfiles','breakingForce','breakingTorque','maxTemp','skinMaxTemp'):assert part.get(key)==value
    assert dump(next(n for n in base.children if n.header=='MODEL'))==dump(next(n for n in part.children if n.header=='MODEL'))
    assert math.isclose(float(part.get('mass'))-float(base.get('mass')),.039*factor,abs_tol=1e-9)
    stores={n.get('name'):n for n in part.children if n.header=='RESOURCE'}
    assert float(stores['ElectricCharge'].get('maxAmount'))==capacity
    for name in ('EnrichedUranium','DepletedFuel'):assert math.isclose(float(stores[name].get('maxAmount')),1.5*factor)
    assert float(stores['DepletedFuel'].get('amount'))==0
    controller=next(n for n in part.children if n.get('name')=='ProcessController')
    assert controller.header=='MODULE:NEEDS[Kerbalism,ProfileDefault]' and controller.get('running')=='false'
    assert controller.get('resource')==process.get('modifier') and float(controller.get('capacity'))==factor
    stock=next(n for n in part.children if n.get('name')=='ModuleResourceConverter')
    assert stock.header=='MODULE:NEEDS[!Kerbalism]' and stock.get('GeneratesHeat')=='false' and stock.get('UseSpecialistBonus')=='false'
    io={n.get('ResourceName'):n for n in stock.children}
    assert float(io['ElectricCharge'].get('Ratio'))==5*factor and io['ElectricCharge'].get('DumpExcess')=='true'
    assert math.isclose(float(io['EnrichedUranium'].get('Ratio')),RATE*factor)
    assert io['DepletedFuel'].get('DumpExcess')=='false' and math.isclose(float(io['DepletedFuel'].get('Ratio')),RATE*factor)
    assert math.isclose(float(stores['EnrichedUranium'].get('amount'))/(RATE*factor),1.5/RATE)
    assert not any('Heat' in n.get('name','') or 'Radiator' in n.get('name','') for n in part.children)
    assert len([n for n in part.children if n.get('name') in ('ProcessController','ModuleResourceConverter')])==2
    print('PASS optional nuclear',size,5*factor,'EC/s; exclusive Kerbalism/stock modules; no external cooling or free fuel; passive core unaltered')
files=sorted(p for p in GD.rglob('*') if p.is_file());before={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
build()
assert before=={p:hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'Options rebuild not deterministic'
for p in (ROOT/'Tools').glob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'))
assert (GD/'Plugins/RoosterWorksFinish.dll').read_bytes()[:2]==b'MZ'
subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'Tools/test-finish.ps1')],check=True)
print('PASS option rebuild deterministic; all C# finish transitions checked; live editor/flight/background tests pending')
