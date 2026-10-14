"""Battery-reference arithmetic, EC-only edits and builder policy regression."""
from pathlib import Path
import sys,json,math,hashlib,ast
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from electric_charge_balance import policy,check_preserved
from config_nodes import parse
table=policy()['parts'];assert len(table)==19
for name,entry in table.items():
    expected=entry.get('override_base_ec',entry['reference_base_ec']*entry['proxy_factor']*1.05)
    assert math.isclose(expected,entry['target_base_ec'])
    path=ROOT/f'GameData/RoosterWorksStationModules/Parts/{name}.cfg';part=parse(path.read_text()).children[0]
    stores=[n for n in part.children if n.header=='RESOURCE' and n.get('name')=='ElectricCharge']
    assert len(stores)<=1
    if stores:
        assert math.isclose(float(stores[0].get('amount')),expected) and math.isclose(float(stores[0].get('maxAmount')),expected)
    else:assert expected==0
    assert int(part.get('CrewCapacity'))==entry['crew']
    print('PASS',name,format(expected,'.10g'),'base EC; expected Default',format(expected*(2.8 if entry['crew'] else 1),'.10g'))
for path,digest in json.loads((ROOT/'Tools/ec_balance_baseline.json').read_text()).items():check_preserved(ROOT,path,digest)
from build_family375 import part as build_part
# A config-only rebuild must preserve the explicit large EC policy instead of
# restoring the generic cubic scale. No mesh/texture rebuild needed for this test.
for role in ('HAB','LAB','CMD','HUB','CUP','LOG','AIR','PWR','GRN'):
    path=ROOT/f'GameData/RoosterWorksStationModules/Parts/RW_{role}_375.cfg'
    before=path.read_bytes();build_part(role);after=path.read_bytes();assert before==after,('Rebuild changed balanced config',role)
for path in (ROOT/'Source').rglob('*.py'):ast.parse(path.read_text(encoding='utf-8-sig'),filename=str(path))
print('PASS all pre-balance native models, lighting, textures, other resources, crew, costs/mass, rates and patches byte-preserved')
print('PASS config-only large rebuild retains explicit EC policy; Python source parses; actual KSP cache/old craft checks pending')
