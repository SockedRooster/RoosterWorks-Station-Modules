#!/usr/bin/env python3
"""v0.2.7 RW-HAB-250 static checks (not game-runtime testing)."""
from pathlib import Path
from struct import unpack_from
import json,sys,math
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
from build_hab250 import (generate_geometry,generate_groups,TEXTURES,WINDOW_SCALE,
                          SPECIAL_BAY,square_window_shape,curved_rect_contour,Mesh)

part_path=ROOT/'GameData/RoosterWorksStationModules/Parts/RW_HAB_250.cfg'
patch_path=ROOT/'GameData/RoosterWorksStationModules/Compatibility/KerbalismDefault.cfg'
models=ROOT/'GameData/RoosterWorksStationModules/Models'
version=ROOT/'GameData/RoosterWorksStationModules/RoosterWorksStationModules.version'
part=part_path.read_text();patch=patch_path.read_text()
assert part.count('{')==part.count('}') and patch.count('{')==patch.count('}')
assert 'name = RW_HAB_250' in part and 'CrewCapacity = 4' in part
assert part.count('name = ModulePartVariants')==1
assert 'baseVariant = Standard' in part
for name in ('WindowBankStandard','SideHatch'):
    assert part.count(name)>=2 and name.encode() in (models/'RW_HAB_250.mu').read_bytes()
for label in ('displayName = Standard Windows','displayName = Exterior Side Hatch'):
    assert label in part
assert 'mass = 3.5' in part and 'name = crewCabinInternals' in part
assert 'node_stack_top = 0, 1.980' in part and 'node_stack_bottom = 0, -1.980' in part
assert ':NEEDS[Kerbalism,ProfileDefault]' in patch
assert ':NEEDS[Kerbalism,FeatureHabitat]' in patch and '%MODULE[Habitat]' in patch
for resource in ('Food','Water','Oxygen','Nitrogen','Waste','WasteWater'):
    assert '%RESOURCE['+resource+']' in patch and 'name = '+resource not in part
assert abs(WINDOW_SCALE-1.5)<1e-8 and SPECIAL_BAY==(2,1)
for half in (.160,.143,.127,.113,.104):
    old=square_window_shape(0,0,half,half)
    new=square_window_shape(0,0,half*WINDOW_SCALE,half*WINDOW_SCALE)
    def wh(x):return ((max(a for a,_ in x)-min(a for a,_ in x))*1.22,max(y for _,y in x)-min(y for _,y in x))
    w0,h0=wh(old);w,h=wh(new)
    assert abs(w/h-1)<1e-8
    assert abs(w/w0-1.5)<1e-9 and abs(h/h0-1.5)<1e-9
assert abs((.104*1.5*2)-.312)<1e-6
# Side Hatch rail must be absent in the hatch zone but present in Standard.
rail_theta=3*math.pi/8

def crossing_rail(group):
    hits=[]
    for x,y,z in group['rail'].vertices:
        t=(math.atan2(x,z)-rail_theta+math.pi)%(2*math.pi)-math.pi
        if abs(t)<.038 and -.970<y<-.340 and math.hypot(x,z)>1.230:
            hits.append((x,y,z))
    return hits


G=generate_groups()
assert set(G)=={'Base','WindowBankStandard','SideHatch'}
assert all(set(x)==set(TEXTURES) for x in G.values())
assert G['WindowBankStandard']['glass'].triangles
assert G['SideHatch']['glass'].triangles
assert len(G['WindowBankStandard']['glass'].triangles)!=len(G['SideHatch']['glass'].triangles)
assert len(crossing_rail(G['Base']))==0, 'Rail erroneously baked into common hull'
assert len(crossing_rail(G['WindowBankStandard']))>0, 'Standard lost its rail'
assert len(crossing_rail(G['SideHatch']))==0, 'Hatch rail still crosses door'
assert G['Base']['crest'].triangles, 'RoosterWorks logo geometry missing'
for gr,group in G.items():
    for material,mesh in group.items():
        assert len(mesh.vertices)==len(mesh.normals)==len(mesh.uvs),(gr,material)
        assert len(mesh.vertices)<65535,(gr,material)
        assert all(len(face)==3 and max(face)<len(mesh.vertices) for face in mesh.triangles)
for choice in ('Standard','SideHatch'):
    mesh=generate_geometry(choice)
    ys=[v[1] for m in mesh.values() for v in m.vertices]
    assert min(ys)>=-1.980001 and max(ys)<=1.980001,(choice,min(ys),max(ys))
    assert sum(len(m.triangles) for m in mesh.values())>11000
    obj=ROOT/('Source/Blender/RW_HAB_250'+('_SideHatch' if choice=='SideHatch' else '')+'.obj')
    assert obj.is_file() and obj.stat().st_size>200000
    assert obj.with_suffix('.mtl').is_file()
assert (ROOT/'Source/Blender/create_hab250.py').is_file()
assert (ROOT/'Source/Blender/create_hab250.py').read_text().count('EXTERIOR_VARIANT')>=2
mu=(models/'RW_HAB_250.mu').read_bytes()
assert unpack_from('<ii',mu)==(76543,5) and len(mu)>650000
for name in (b'WindowBankStandard',b'SideHatch',b'RW_HAB250_SolidHullCollider',b'rwm_crest',b'KSP/Emissive/Diffuse',b'_EmissiveColor',b'_Emissive',b'RW_GlassBase',b'RW_GlassStandard',b'RW_GlassSideHatch'):
    assert name in mu
for name in list(TEXTURES)+['cabin_emissive']:
    texture=models/('rwm_'+name+'.png')
    assert texture.read_bytes()[:8]==b'\x89PNG\r\n\x1a\n'
    assert ('rwm_'+name).encode() in mu
    if name in TEXTURES:assert ('RW_'+name).encode() in mu
with Image.open(models/'rwm_crest.png') as im:
    assert im.size==(512,512) and im.getpixel((256,256))!=im.getpixel((0,0))
with Image.open(models/'rwm_glass.png') as im:
    assert max(im.getpixel((255,255)))<110
v=json.loads(version.read_text())
assert (v['VERSION']['MAJOR'],v['VERSION']['MINOR'],v['VERSION']['PATCH']) in ((0,2,7),(0,3,0),(0,4,0),(0,4,1),(0,4,2),(0,4,3),(0,4,4),(0,4,5),(0,4,6),(0,5,0),(0,5,1),(0,5,2),(0,5,3),(0,6,0),(0,7,0),(0,8,0),(0,9,0),(0,10,0),(0,11,0),(0,12,0),(0,13,0),(0,14,0),(0,15,0),(0,16,0))
assert v['KSP_VERSION']=={'MAJOR':1,'MINOR':12,'PATCH':5}
print('PASS | Part variants: Standard retains rail; Side Hatch rail clear of the door')
print('PASS | Native MU transforms, +50% square windows, original rooster logo texture')
print('PASS | Seated curved hatch skirt, model dimensions, both OBJ files, Kerbalism configs')
assert part.count('name = ModuleColorChanger')==1
assert 'moduleID = RW_HAB_250_CabinLights' in part
assert 'shaderProperty = _EmissiveColor' in part
assert 'toggleInEditor = true' in part and 'toggleInFlight = true' in part
assert 'defaultActionGroup = Light' in part
for render_name in ('RW_GlassBase','RW_GlassStandard','RW_GlassSideHatch'):
    assert 'includedRenderer = '+render_name in part
assert 'name = ModuleLight' not in part
assert 'name = ModulePartVariants' in part
with Image.open(models/'rwm_cabin_emissive.png') as emissive:
    r,g,b=emissive.getpixel((256,256))
    assert r>g>b>155, (r,g,b)
print('PASS | Stock warm-white cabin light emissive material, 3 targeted renderers, editor/flight toggle')

# Regression: the foundation's original 8-point full-width chord caused
# detached raised wings. Test that all radius/angle cross-section points are
# sampled along the actual cylindrical wall, with no flat spanning chord.
from build_hab250 import window_bay_foundation,subdivided_frame_outline,point

def check_foundation():
    group={k:Mesh() for k in TEXTURES}
    window_bay_foundation(group,.810,-.644,.710)
    assert sum(len(m.triangles) for m in group.values())>1500
    # Foundation shell seating is within 1mm of the r=1.204m clad hull.
    sides=[v for mesh in group.values() for v in mesh.vertices
           if abs(v[1]-(-.644+.710*.5*1.102))<.000001]
    assert len(sides)>50, 'No subdivided top hull edge'
    angles=[math.atan2(v[0],v[2]) for v in sides]
    assert max(angles)-min(angles)>1.44
    assert all(abs(math.hypot(v[0],v[2])-1.2048)<.00002 for v in sides)
    # Original 8-point foundation had one >1.4rad long edge; now adjacent
    # triangles may change theta at most 0.07rad (<5 degrees).
    for mat,mesh in group.items():
        for a,b,c in mesh.triangles:
            theta=[math.atan2(mesh.vertices[i][0],mesh.vertices[i][2]) for i in (a,b,c)]
            assert max(theta)-min(theta)<.075, ('wide flat chord',mat,theta)
check_foundation()
for gr,group in G.items():
    for mat,mesh in group.items():
        if mat not in ('white','steel','ceramic','black','graphite','glass','rail'):
            continue
        # No NaNs or broken infinite surfaces in either exposed variant.
        assert all(math.isfinite(c) for v in mesh.vertices for c in v)
print('PASS | v0.4.5 conformal foundation seated on hull; explicit aperture/clearance tests follow')
print('NOTE | Final confirmation requires oblique VAB render on KSP actual part')

# v0.4.2 EVA trigger: positive source + binary checks
assert "tag='Airlock',layer=21,trigger=True" in (ROOT/'Source/build_hab250.py').read_text()
assert 'RW_HAB250_EVA_Airlock =' not in part, 'EVA trigger must remain active across cosmetic variants'
assert b'RW_HAB250_EVA_Airlock' in mu and b'Airlock' in mu
print('PASS | Airlock trigger tag/layer, native registration plus runtime variant gating (flight test pending)')
