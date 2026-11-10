"""Only the two reviewed selector headers may differ in historical guards."""
from pathlib import Path
import hashlib,copy
from config_nodes import parse,dump
FINISH='@PART[RW_*]:HAS[@MODEL:HAS[#model[RoosterWorksStationModules/Models/*]],!MODULE[ModuleRWStationFinish]]:FOR[RoosterWorksStationModules]'
MENU='@PART[RW_*]:HAS[@MODULE[ModuleRWRingColor],~category[none],!MODULE[ModuleRWEditorMenu]]:AFTER[RoosterWorksStationModules]'
SWATCH='@PART[RW_*]:HAS[@MODULE[ModuleRWRingColor],@MODULE[ModuleRWStationFinish],~category[none]]:NEEDS[B9PartSwitch]:AFTER[RoosterWorksStationModules]'
def check_selector_delta(root,path,expected):
    root=Path(root);p=root/path
    if p.parent!=root/'GameData/RoosterWorksStationModules/Compatibility':return False
    allowed={'ExteriorFinish.cfg':[FINISH],'EditorAppearance.cfg':[MENU,SWATCH]}
    if p.name not in allowed:return False
    reference=root/'Source/Balancing/075dev4Selectors'/p.name
    if hashlib.sha256(reference.read_bytes()).hexdigest()!=expected:return False
    before=parse(reference.read_text());after=parse(p.read_text())
    if [n.header for n in after.children]!=allowed[p.name]:return False
    restored=copy.deepcopy(after)
    for n,old in zip(restored.children,before.children):n.header=old.header
    return dump(restored)==dump(before)
