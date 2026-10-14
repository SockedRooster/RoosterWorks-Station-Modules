"""Audit effective command patch precedence, scope, capacity and preservation."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from config_nodes import parse
from build_command_storage import build
GD=ROOT/'GameData/RoosterWorksStationModules'
before=json.loads((ROOT/'Tools/command_storage_baseline.json').read_text())
for path,digest in before.items():
    if path.endswith('.version'):continue
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('Unrelated command-storage change',path)
new='GameData/RoosterWorksStationModules/Compatibility/ZZZCommandStorage075.cfg'
assert {p.relative_to(ROOT).as_posix() for p in (ROOT/'GameData').rglob('*') if p.is_file()}==set(before)|{new}
p=ROOT/new;data=p.read_bytes();build();assert p.read_bytes()==data
tree=parse(data.decode());assert len(tree.children)==3
# Resolve the actual competing FINAL patches in lexicographic path order.
paths=sorted((GD/'Compatibility').glob('*.cfg'))
assert paths.index(p)>paths.index(GD/'Compatibility/StorageBalance.cfg')
assert paths.index(p)>paths.index(GD/'Compatibility/Family500.cfg')
for node,size in zip(tree.children,(250,375,500)):
    assert node.header==f'@PART[RW_CMD_{size}]:NEEDS[Kerbalism,FeatureScience]:FINAL'
    assert len(node.children)==1 and {k for k,v in node.values}=={'%description'}
    drive=node.children[0];assert drive.header=='%MODULE[HardDrive]' and not drive.children
    assert {k for k,v in drive.values}=={'%name','%dataCapacity','%effectiveDataCapacity','%maxDataCapacityFactor'}
    expected=200*(size/250)**3
    assert math.isclose(float(drive.get('%dataCapacity')),expected)
    assert float(drive.get('%effectiveDataCapacity'))==expected and drive.get('%maxDataCapacityFactor')=='5'
    effective={}
    for path in paths:
        for patch in parse(path.read_text()).children:
            if not patch.header.startswith('@PART[') or not patch.header.endswith(':FINAL'):continue
            names=patch.header.split(']',1)[0].split('[',1)[1].split(',')
            if f'RW_CMD_{size}' not in names:continue
            for child in patch.children:
                if child.header=='%MODULE[HardDrive]':effective.update(dict(child.values))
    assert float(effective['%dataCapacity'])==expected and effective['%maxDataCapacityFactor']=='5'
    print('PASS command archive',size,'native data steps:',[expected*i for i in range(1,6)])
assert json.loads((GD/'RoosterWorksStationModules.version').read_text())['VERSION']['BUILD']==4
print('PASS command storage: exact volume scaling, native five-step defaults/ceilings, final patch precedence, no sample changes; all 213 preceding GameData files protected except version')
