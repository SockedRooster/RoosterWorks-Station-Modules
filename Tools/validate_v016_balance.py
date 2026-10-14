from pathlib import Path
import sys,json,hashlib,math
from decimal import Decimal,ROUND_HALF_UP
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from config_nodes import parse,dump
from electric_charge_balance import check_preserved,policy
GD=ROOT/'GameData/RoosterWorksStationModules'
def rounded(before,multiplier):return float((Decimal(str(before))*Decimal(str(multiplier))/10).quantize(Decimal('1'),rounding=ROUND_HALF_UP)*10)
for name,before,target in (('RW_HAB_250',420,290),('RW_HAB_375',787.5,550)):
    assert rounded(before,.7)==target and policy()['parts'][name]['target_base_ec']==target
powers=json.loads((ROOT/'Source/Balancing/power_capacity_policy.json').read_text())['parts']
for e in powers.values():
    assert rounded(e['previous_battery'],.85)==e['battery'] and rounded(e['previous_nuclear'],.8)==e['nuclear']
    assert e['battery']>e['nuclear']>0
storage=parse((GD/'Compatibility/StorageBalance.cfg').read_text())
for role in ('CMD','LAB'):
    patch=next(n for n in storage.children if n.header.startswith(f'@PART[RW_{role}_250,'))
    assert patch.header.endswith(':NEEDS[Kerbalism,FeatureScience]:FINAL')
    drive=patch.children[0];assert drive.header=='%MODULE[HardDrive]'
    assert drive.get('%dataCapacity')=='2500' and drive.get('%effectiveDataCapacity')=='2500' and drive.get('%maxDataCapacityFactor')=='1'
    if role=='LAB':assert drive.get('%sampleCapacity')=='100' and drive.get('%effectiveSampleCapacity')=='100' and drive.get('%maxSampleCapacityFactor')=='1'
    else:assert drive.get('%sampleCapacity') is None,'CMD sample storage was not requested to change'
for size in (250,375):
    patch=next(n for n in storage.children if n.header.startswith(f'@PART[RW_PWR_{size}_REACTOR]'))
    assert patch.children[0].get('@maxAmount')==str(powers[str(size)]['nuclear'])
baseline=json.loads((ROOT/'Tools/v016_baseline.json').read_text())
for path,digest in baseline.items():
    if path.endswith('.version'):continue
    if path.endswith('/RoosterWorksPowerVariants.dll'):continue # only GetInfo changes; source delta checked below
    if path.endswith('/PowerVariants.cfg'):
        old=(ROOT/'Source/Balancing/PowerVariants-v015.cfg').read_bytes();assert hashlib.sha256(old).hexdigest()==digest
        before=parse(old.decode());now=parse((ROOT/path).read_text())
        for a,b in zip(now.children,before.children):
            if a.get('%description') is not None:a.set('%description',b.get('%description'))
            for module in a.children:
                if module.get('name')!='ModuleRWPowerVariant':continue
                original=next(n for n in b.children if n.get('name')=='ModuleRWPowerVariant')
                for key in ('batteryCapacity','reactorCapacity'):module.set(key,original.get(key))
        assert dump(now)==dump(before),'PWR change outside authorized capacities/description'
    else:check_preserved(ROOT,path,digest)
old=(ROOT/'Source/Balancing/PowerVariant-v015.cs.txt').read_bytes()
now=(ROOT/'Source/PowerVariant.cs').read_bytes().replace(b'Reactor exchanges a battery bay; capacities follow the current storage balance.',b'Reactor reserves one of eight battery bays (12.5% less EC storage).')
assert now==old,'Power runtime logic changed outside GetInfo text'
assert 'Ground-base modules' in (ROOT/'ROADMAP.md').read_text(encoding='utf-8') and 'Adjustable legs' in (ROOT/'ROADMAP.md').read_text(encoding='utf-8')
print('PASS HAB -30%, passive PWR -15%, nuclear PWR -20%, round-to-ten arithmetic; 2.5 GB CMD/LAB ceilings and 100 LAB slots; legacy limits; all other prior GameData/native/finish/hatch assets preserved; roadmap recorded')
