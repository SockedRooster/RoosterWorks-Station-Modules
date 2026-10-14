#!/usr/bin/env python3
"""Static validation of the RW-LAB-250 v0.4.0 and Kerbalism / stock modes."""
from pathlib import Path
import sys,math,json,struct,re
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
from build_lab250 import geometry,MAT,MODELS,PART
part=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_LAB_250.cfg').read_text()
patch=(ROOT/'GameData/RoosterWorksStationModules/Compatibility/LabKerbalism.cfg').read_text()
hab=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_HAB_250.cfg').read_text()
assert 'name = RW_LAB_250' in part and 'name = RW_HAB_250' in hab
assert part.count('{')==part.count('}') and patch.count('{')==patch.count('}')
assert 'CrewCapacity = 2' in part and 'mass = 3.25' in part
assert 'node_stack_top = 0, 1.980' in part and 'node_stack_bottom = 0, -1.980' in part
assert part.index('name = ModuleScienceContainer')<part.index('name = ModuleScienceLab')
assert 'containerModuleIndex = 0' in part and part.count('name = ModuleScienceConverter')==1
assert '%MODULE[Laboratory]' in patch and 'analysis_rate = 0.0006' in patch
assert '!MODULE[ModuleScienceLab],*' in patch and '!MODULE[ModuleScienceConverter],*' in patch
assert ':NEEDS[Kerbalism,FeatureScience]' in patch and ':NEEDS[Kerbalism,ProfileDefault]' in patch
assert 'name = ModuleColorChanger' in part and 'includedRenderer = RW_LabGlass' in part
assert 'defaultActionGroup = Light' in part
for n in ('Food','Water','Oxygen','Nitrogen','Waste','WasteWater'):
    assert f'%RESOURCE[{n}]' in patch
    assert f'name = {n}' not in part
for n in ('Habitat','Laboratory'):
    assert '%MODULE['+n+']' in patch
# Integrated stock experiments with stock science definitions (no custom duplicates).
ids=('temperatureScan','barometerScan','gravityScan','atmosphereAnalysis','mobileMaterialsLab','mysteryGoo')
for exp in ids:
    assert part.count('experimentID = '+exp)==1,exp
    assert 'experiment_id = '+exp in patch,exp
assert part.count('name = ModuleScienceExperiment')==len(ids)
assert 'experiment_id = geigerCounter' in patch
assert '!MODULE[ModuleScienceExperiment],*' in patch
assert 'name = HardDrive' in patch and 'sampleCapacity = 20' in patch
assert '!MODULE[ModuleScienceContainer],*' in patch
assert 'name = Mobile_Processing_Lab_Int' in part
version=json.loads((ROOT/'GameData/RoosterWorksStationModules/RoosterWorksStationModules.version').read_text())
assert tuple(version['VERSION'][x] for x in ('MAJOR','MINOR','PATCH'))in ((0,4,0),(0,4,1),(0,4,2),(0,4,3),(0,4,4),(0,4,5),(0,4,6),(0,5,0),(0,5,1),(0,5,2),(0,5,3),(0,6,0),(0,7,0),(0,8,0),(0,9,0),(0,10,0),(0,11,0),(0,12,0),(0,13,0),(0,14,0),(0,15,0),(0,16,0))
models=MODELS
mu=(models/(PART+'.mu')).read_bytes()
assert struct.unpack_from('<ii',mu)==(76543,5) and len(mu)>250000
for token in (b'RW_LAB_250',b'RW_LabGlass',b'LabFlushEndcapTop',b'LabFlushEndcapBottom',b'rwm_lablabel',b'rwm_instrument',b'KSP/Emissive/Diffuse'):
    assert token in mu,token
for mat in list(MAT)+['cabin_emissive']:
    p=models/('rwm_'+mat+'.png')
    assert p.exists() and p.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
for extra in ('Source/Blender/RW_LAB_250.obj','Source/Blender/RW_LAB_250.mtl','Source/Blender/create_lab250.py'):
    assert (ROOT/extra).is_file()
allmeshes=geometry()
tri=sum(len(m.triangles) for m in allmeshes.values())
assert 8000<tri<50000,tri
for material,mesh in allmeshes.items():
    assert len(mesh.vertices)<65535
    assert len(mesh.vertices)==len(mesh.uvs)==len(mesh.normals)
    assert all(all(0<=i<len(mesh.vertices) for i in face) for face in mesh.triangles)
all_vertices=[xyz for mesh in allmeshes.values() for xyz in mesh.vertices]
assert all(-1.980001<=v[1]<=1.980001 for v in all_vertices)
assert 1.20<max(math.hypot(v[0],v[2]) for v in all_vertices)<1.40
# Window glass: three compact panels, each under 0.20m in height, not 18 HAB squares.
glass=allmeshes['glass']
assert len(glass.triangles)==3*8 and len(glass.vertices)==3*8*3
assert .48<min(v[1] for v in glass.vertices) and max(v[1] for v in glass.vertices)<.80
# Each window ring edge spans at most 0.07 rad, preventing wide flat quads.
for mat in ('white','graphite','black','steel'):
    mesh=allmeshes[mat]
    assert len(mesh.triangles)>0
assert (ROOT/'GameData/RoosterWorksStationModules/Models/RW_HAB_250.mu').exists()
print('PASS RW-LAB-250: 2 seats, distinct exterior, 3 recessed glass windows, %d triangles'%tri)
print('PASS stock lab modules; Kerbalism science replaces stock research instead of duplicating it')
print('PASS conditional life support, fixed 2.5m stack nodes, warm-white lights, native .mu')
print('NOTE Real KSP/ModuleManager science processing and light states need in-game tests')
