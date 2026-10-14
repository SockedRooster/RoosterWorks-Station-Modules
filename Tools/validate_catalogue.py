from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from config_nodes import parse
from build_catalogue import MAPPING
from tube_material_regression import check as check_tube
GD=ROOT/'GameData/RoosterWorksStationModules'
tree=parse((GD/'Compatibility/StationCatalogue.cfg').read_text())
assert len(tree.children)==17
parts=set()
for role,(subcategory,category,label) in MAPPING.items():
    node=next(n for n in tree.children if n.header.startswith(f'@PART[RW_{role}_250,'))
    assert node.header.endswith(':NEEDS[VABOrganizer]:FINAL') and node.get('%category')==category
    assert [n.header for n in node.children]==['!VABORGANIZER,*','VABORGANIZER']
    assert node.children[1].get('organizerSubcategory')==subcategory
    for size in (250,375):
        name=f'RW_{role}_{size}';assert (GD/f'Parts/{name}.cfg').is_file();parts.add(name)
    print('PASS',role,'->',label)
adapter=next(n for n in tree.children if n.header.startswith('@PART[RW_ADP_250_375]'))
assert adapter.children[1].get('organizerSubcategory')=='crewAdapters';parts.add('RW_ADP_250_375')
assert len(parts)==23
fallbacks=[n for n in tree.children if n.header.startswith('ORGANIZERSUBCATEGORY')]
assert len(fallbacks)==5 and all(':NEEDS[VABOrganizer,!StationPartsExpansionRedux]' in n.header for n in fallbacks)
assert {n.get('name') for n in fallbacks}=={'crewUtility','cupolas','crewTubes','crewAdapters','crewHubs'}
baseline=json.loads((ROOT/'Tools/catalogue_baseline.json').read_text())
for path,digest in baseline.items():
    if path.endswith('.version'):continue
    if path.endswith('/RW_TUB_250.mu') or path.endswith('/RW_TUB_375.mu'):check_tube(ROOT,path,digest)
    else:assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('Unexpected prior asset change',path)
roadmap=(ROOT/'ROADMAP.md').read_text(encoding='utf-8')
assert all(term in roadmap for term in ('Selectable logistics contents','Food','Water','Oxygen','Ammonia','Waste','Selectable ring colors'))
print('PASS all 23 catalogue placements, unique final nodes, conditional SSPXr category fallbacks, tube loader material-table fix and exact geometry/collision/UV preservation; roadmap variants recorded')
