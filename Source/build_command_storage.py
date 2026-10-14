"""Adjustable command data archives: five editor tiers, volume-scaled by size."""
from pathlib import Path
from config_nodes import Node,dump
ROOT=Path(__file__).resolve().parents[1];GD=ROOT/'GameData/RoosterWorksStationModules'
def build():
    out=Node('ROOT')
    for size,factor in ((250,1),(375,3.375),(500,8)):
        data=200*factor
        description=f'RoosterWorks {size/100:g} m station command core with retained control, communications, IVA and warm-white cabin lighting. Kerbalism editor data archive selectable from {data:g} to {data*5:g} MB in five steps. White/Grey surface and independent ring colors; existing pressure, supply and electrical balance retained.'
        out.children.append(Node(f'@PART[RW_CMD_{size}]:NEEDS[Kerbalism,FeatureScience]:FINAL',[('%description',description)],children=[Node('%MODULE[HardDrive]',[('%name','HardDrive'),('%dataCapacity',format(data,'.10g')),('%effectiveDataCapacity',format(data,'.10g')),('%maxDataCapacityFactor','5')])]))
    (GD/'Compatibility/ZZZCommandStorage075.cfg').write_text('// Command archives: five independent editor data tiers; no sample-storage changes.\n// Decimal MB/GB; native Kerbalism selectors and persisted flight archives retained.\n'+dump(out),encoding='utf-8')
if __name__=='__main__':build()
