from pathlib import Path
import json
from config_nodes import Node,dump
ROOT=Path(__file__).resolve().parents[1];GD=ROOT/'GameData/RoosterWorksStationModules'
def build():
    root=Node('ROOT')
    for role in ('CMD','LAB'):
        n=Node(f'@PART[RW_{role}_250,RW_{role}_375]:NEEDS[Kerbalism,FeatureScience]:FINAL')
        drive=Node('%MODULE[HardDrive]',[('%name','HardDrive'),('%dataCapacity','2500'),('%effectiveDataCapacity','2500'),('%maxDataCapacityFactor','1')])
        if role=='LAB':drive.values.extend([('%sampleCapacity','100'),('%effectiveSampleCapacity','100'),('%maxSampleCapacityFactor','1')])
        n.children.append(drive);root.children.append(n)
    policy=json.loads((ROOT/'Source/Balancing/power_capacity_policy.json').read_text())['parts']
    for size in (250,375):
        e=policy[str(size)]
        n=Node(f'@PART[RW_PWR_{size}_REACTOR]:FINAL',children=[Node('@RESOURCE[ElectricCharge]',[('@amount',str(e['nuclear'])),('@maxAmount',str(e['nuclear']))])]);root.children.append(n)
        root.children.append(Node(f'@PART[RW_PWR_{size}]:NEEDS[!Kerbalism]:FINAL',[('%description',f'Passive power and service core with {e["battery"]} EC storage. Current battery balance; white/grey exterior. Generation supplied separately.')]))
    (GD/'Compatibility/StorageBalance.cfg').write_text('// Explicit limits after the Kerbalism/default drive passes; MB uses decimal GB.\n'+dump(root))
if __name__=='__main__':build()
