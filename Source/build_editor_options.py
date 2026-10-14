"""Cosmetic B9 swatches are optional; original persistent material controls remain authoritative."""
from pathlib import Path
from config_nodes import Node,dump
ROOT=Path(__file__).resolve().parents[1];GD=ROOT/'GameData/RoosterWorksStationModules'
PALETTE={'Original':'#BFA16A','Steel':'#97A6AB','White':'#DADDD5','Charcoal':'#374148','Blue':'#35659E','Green':'#467457','Red':'#974036','Gold':'#BF9643'}
def switch(identifier,title,choices):
    return Node('MODULE',[('name','ModuleB9PartSwitch'),('moduleID',identifier),('switcherDescription',title),('switcherDescriptionPlural',title+' options'),('affectDragCubes','false'),('affectFARVoxels','false'),('switchInFlight','false'),('uiGroupName','RWAppearance'),('uiGroupDisplayName','Appearance')],[Node('SUBTYPE',[('name',name.replace(' ','_')),('title',name),('primaryColor',color),('secondaryColor',color)]) for name,color in choices.items()])
def build():
    out=Node('ROOT')
    # FOR precedes the AFTER/FINAL Kerbalism additions. Cosmetics get a single early group.
    out.children.append(Node('@PART[RW_*]:HAS[~category[none],!MODULE[ModuleRWEditorMenu]]:FOR[RoosterWorksStationModules]',children=[Node('MODULE',[('name','ModuleRWEditorMenu')])]))
    out.children.append(Node('@PART[RW_*]:HAS[~category[none]]:NEEDS[B9PartSwitch]:FOR[RoosterWorksStationModules]',children=[switch('RWFinishSwatch','Surface',{'White':'#EBDDCC','Grey metal':'#747D83'}),switch('RWRingSwatch','Rings',PALETTE)]))
    (GD/'Compatibility/EditorAppearance.cfg').write_text('// Swatches manage no resources, transforms, materials or hardware variants.\n'+dump(out))
    out=Node('ROOT')
    for size,factor in ((250,1),(375,3.375),(500,8)):
        data=250*factor;sample=round(10*factor)
        drive=Node('%MODULE[HardDrive]',[('%name','HardDrive'),('%dataCapacity',str(data)),('%effectiveDataCapacity',str(data)),('%maxDataCapacityFactor','10'),('%sampleCapacity',str(sample)),('%effectiveSampleCapacity',str(sample)),('%maxSampleCapacityFactor','10')])
        bridge=Node('MODULE',[('name','ModuleRWScienceTiers'),('volumeFactor',str(factor))])
        out.children.append(Node(f'@PART[RW_LAB_{size}]:NEEDS[Kerbalism,FeatureScience]:FINAL',[('%description',f'RoosterWorks {size/100:g} m orbital science laboratory. Independent editor choices: {data:g} to {data*10:g} MB data and {sample} to {int(100*factor+.5)} sample slots in ten steps. Warm-white cabin lighting, White/Grey finish and independent ring colors. Kerbalism experiments, pressure and supplies retained.')],children=[drive,bridge]))
    # ZZZ filename runs after accepted StorageBalance and Family500 FINAL overrides.
    (GD/'Compatibility/ZZZScienceStorage075.cfg').write_text('// MB decimal; capacity scales with pressure volume; sample slots rounded per step.\n'+dump(out))
if __name__=='__main__':build()
