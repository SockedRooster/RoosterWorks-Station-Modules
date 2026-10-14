"""Stock Variant selector, one battery bay exchanged for internally cooled reactor.

Patch base parts rather than replacing their persistent IDs or native models.
Keep old reactor IDs hidden for saved craft compatibility.
"""
from pathlib import Path
import json
from config_nodes import parse,dump,Node
ROOT=Path(__file__).resolve().parents[1];GD=ROOT/'GameData/RoosterWorksStationModules'
def build():
    tree=Node('ROOT')
    policy=json.loads((ROOT/'Source/Balancing/power_capacity_policy.json').read_text())['parts']
    for size in (250,375):
        entry=policy[str(size)];factor=entry['reactor_scale'];ec=entry['battery'];nuclear_ec=entry['nuclear']
        patch=Node(f'@PART[RW_PWR_{size}]:NEEDS[Kerbalism,ProfileDefault,CommunityResourcePack]:AFTER[RoosterWorksStationModules]')
        patch.values=[('%description',f'Power and service core with Battery / Nuclear editor variants. Battery {ec} EC; nuclear {nuclear_ec} EC and {5*factor:g} EC/s. Nuclear hardware replaces a battery bay and applies the current independent storage balance. Includes cooling and starts off. White/grey finish is independent.')]
        variants=Node('MODULE',[('name','ModulePartVariants'),('baseVariant','Battery'),('useMultipleDragCubes','false')])
        for name,color,mass,cost in (('Battery','#DDE1DF',0,0),('Nuclear','#D49A41',.039*factor,round(10880*factor))):
            variants.children.append(Node('VARIANT',[('name',name),('displayName','Battery only' if name=='Battery' else 'Integrated nuclear'),('primaryColor',color),('secondaryColor','#536675'),('mass',format(mass,'.10g')),('cost',str(cost))]))
        patch.children.append(variants)
        patch.children.append(Node('MODULE',[('name','ProcessController'),('resource','_RWCompactReactor'),('title','Integrated nuclear reactor'),('capacity','0'),('running','false'),('toggle','true'),('valve_i','0')]))
        patch.children.append(Node('MODULE',[('name','ModuleRWPowerVariant'),('batteryCapacity',str(ec)),('reactorCapacity',str(nuclear_ec)),('reactorScale',str(factor))]))
        tree.children.append(patch)
    tree.children.append(Node('@PART[RW_PWR_*_REACTOR]:NEEDS[Kerbalism,ProfileDefault]:AFTER[RoosterWorksStationModules]',[('%category','none'),('%TechHidden','true'),('%entryCost','0')]))
    (GD/'Compatibility/PowerVariants.cfg').write_text('// Stock swatches on existing cores; old reactor IDs retained for saves.\n'+dump(tree))
if __name__=='__main__':build()
