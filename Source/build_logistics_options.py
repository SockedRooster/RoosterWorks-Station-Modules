"""Editor-only loadouts preserving the accepted mixed inventory and fixed volume.

Dedicated payload volume is conservatively 520 L (below the original mixed
522.222 L total); 3.75 m scales by 3.375. Stock KSP inventory is independent.
Gas pressure follows the installed Kerbalism Default tank definitions.
"""
from pathlib import Path
from config_nodes import Node,dump,parse
ROOT=Path(__file__).resolve().parents[1];GD=ROOT/'GameData/RoosterWorksStationModules'
OPTIONS=('Mixed supplies','Food','Water','Oxygen','Nitrogen','Ammonia','Waste','WasteWater')
PRESSURE={'Oxygen':200,'Nitrogen':180,'Ammonia':35}

def build():
    definitions=Node('ROOT');patches=Node('ROOT')
    for size,scale in ((250,1),(375,3.375),(500,8)):
        part=f'RW_LOG_{size}'
        if not (GD/f'Parts/{part}.cfg').exists():continue
        base=GD/'Compatibility/LogisticsKerbalism.cfg'
        tree=parse(base.read_text());legacy=[]
        for patch in tree.children:
            for child in patch.children:
                if child.header=='%RESOURCE['+str(child.get('%name'))+']':
                    legacy.append((child.get('%name'),format(float(child.get('%amount'))*scale,'.10g'),format(float(child.get('%maxAmount'))*scale,'.10g')))
        assert len(legacy)==6,base
        loadouts=Node('RW_LOG_LOADOUTS',[('name',part)])
        for label in OPTIONS:
            choice=Node('LOADOUT',[('name',label)])
            resources=legacy if label=='Mixed supplies' else [(label,'0' if label in ('Waste','WasteWater') else format(520*scale*PRESSURE.get(label,1),'.12g'),format(520*scale*PRESSURE.get(label,1),'.12g'))]
            for resource,amount,capacity in resources:
                choice.children.append(Node('RESOURCE',[('name',resource),('amount',amount),('maxAmount',capacity)]))
            loadouts.children.append(choice)
        definitions.children.append(loadouts)
        patches.children.append(Node(f'@PART[{part}]:NEEDS[Kerbalism,ProfileDefault,CommunityResourcePack]:HAS[!MODULE[ModuleRWLogisticsContents]]:FOR[RoosterWorksStationModules]',[],[
            Node('MODULE',[('name','ModuleRWLogisticsContents'),('profileSet',part),('contents','Mixed supplies')])]))
    (GD/'Compatibility/LogisticsLoadouts.cfg').write_text('// Editor-only custom selector; legacy mixed resources remain the default.\n'+dump(patches)+dump(definitions),encoding='utf-8')
    print('Built both LOG loadout sets; mixed inventories preserved; supplies full / waste empty.')
if __name__=='__main__':build()
