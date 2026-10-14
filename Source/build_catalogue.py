"""Explicit final editor placement; no flight/gameplay or storage changes."""
from pathlib import Path
from config_nodes import Node,dump
ROOT=Path(__file__).resolve().parents[1];GD=ROOT/'GameData/RoosterWorksStationModules'
MAPPING={
    'HAB':('crewHabitation','Utility','Habitation'),
    'LAB':('labs','Science','Labs'),
    'CMD':('station','Pods','Station Cores'),
    'CUP':('cupolas','Pods','Cupolas'),
    'LOG':('crewUtility','Utility','Station Utility'),
    'HUB':('crewHubs','Structural','Station Hubs'),
    'AIR':('airlocks','Utility','Airlocks'),
    'GRN':('greenhouses','Science','Greenhouses'),
    'TUB':('crewTubes','Structural','Station Connectors'),
    'ELB':('crewTubes','Structural','Station Connectors'),
    'PWR':('batteries','Electrical','Batteries')}
def build():
    tree=Node('ROOT')
    for role,(subcategory,category,label) in MAPPING.items():
        node=Node(f'@PART[RW_{role}_250,RW_{role}_375]:NEEDS[VABOrganizer]:FINAL',[('%category',category)])
        node.children=[Node('!VABORGANIZER,*'),Node('VABORGANIZER',[('organizerSubcategory',subcategory)])];tree.children.append(node)
    tree.children.append(Node('@PART[RW_ADP_250_375]:NEEDS[VABOrganizer]:FINAL',[('%category','Structural')],[Node('!VABORGANIZER,*'),Node('VABORGANIZER',[('organizerSubcategory','crewAdapters')])]))
    # Keep the requested labels if VABOrganizer is used without SSPXr.
    for name,label,priority,categorypriority in (('cupolas','Cupolas',22,0),('crewUtility','Station Utility',88,70),('crewTubes','Station Connectors',88,50),('crewAdapters','Station Adapters',15,20),('crewHubs','Station Hubs',110,20)):
        tree.children.append(Node('ORGANIZERSUBCATEGORY:NEEDS[VABOrganizer,!StationPartsExpansionRedux]',[('name',name),('Label',label),('Priority',str(priority)),('CategoryPriority',str(categorypriority))]))
    (GD/'Compatibility/StationCatalogue.cfg').write_text('// User-defined placement; LOG Station Utility confirmed over Supply Containers.\n'+dump(tree))
if __name__=='__main__':build()
