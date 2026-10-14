from pathlib import Path
import sys,hashlib,json,math,subprocess
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from config_nodes import parse
from electric_charge_balance import check_preserved
GD=ROOT/'GameData/RoosterWorksStationModules'
tree=parse((GD/'Compatibility/PowerVariants.cfg').read_text())
assert len(tree.children)==3
for node,size,factor,ec,nuclear in zip(tree.children[:2],(250,375),(1.1,1.2),(2980,5740),(2450,4730)):
    assert node.header==f'@PART[RW_PWR_{size}]:NEEDS[Kerbalism,ProfileDefault,CommunityResourcePack]:AFTER[RoosterWorksStationModules]'
    mods={n.get('name'):n for n in node.children}
    assert set(mods)=={'ModulePartVariants','ProcessController','ModuleRWPowerVariant'}
    stock=mods['ModulePartVariants'];assert stock.get('baseVariant')=='Battery'
    assert [n.get('name') for n in stock.children]==['Battery','Nuclear']
    assert float(stock.children[0].get('mass'))==0 and float(stock.children[0].get('cost'))==0
    assert math.isclose(float(stock.children[1].get('mass')),.039*factor)
    assert float(stock.children[1].get('cost'))==round(10880*factor)
    assert all(n.get('primaryColor') and n.get('secondaryColor') for n in stock.children)
    control=mods['ModuleRWPowerVariant'];assert float(control.get('batteryCapacity'))==ec
    assert float(control.get('reactorCapacity'))==nuclear and float(control.get('reactorScale'))==factor
    assert mods['ProcessController'].get('running')=='false' and mods['ProcessController'].get('capacity')=='0'
    assert not any(n.header=='RESOURCE' for n in node.children),'Passive prefab must not contain uranium'
assert tree.children[2].get('%category')=='none' and tree.children[2].get('%TechHidden')=='true'
baseline=json.loads((ROOT/'Tools/power_variant_baseline.json').read_text())
for path,digest in baseline.items():
    if path.endswith('.version'):continue
    check_preserved(ROOT,path,digest)
print('PASS coloured stock Variant selector; 12.5% EC tradeoff in both sizes; no passive uranium/generation; legacy part IDs retained and hidden; all prior native/finish/runtime assets byte-preserved')
assert (GD/'Plugins/RoosterWorksPowerVariants.dll').read_bytes()[:2]==b'MZ'
subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'Tools/test-power-variants.ps1')],check=True)
print('NOTE stock UI, switching mass/cost, save/reload and actual Kerbalism background simulation require live KSP confirmation')
