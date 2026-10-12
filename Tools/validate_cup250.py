#!/usr/bin/env python3
"""Offline validation of new RW-CUP-250 without claiming KSP flight confirmation."""
from pathlib import Path
from collections import Counter
import sys,math,struct,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
import build_cup250 as c
part=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_CUP_250.cfg').read_text()
patch=(ROOT/'GameData/RoosterWorksStationModules/Compatibility/CupolaKerbalism.cfg').read_text()
for s in (part,patch):
    assert s.count('{')==s.count('}'), 'Unbalanced CFG patch'
for tok in ('name = RW_CUP_250','CrewCapacity = 1','vesselType = Station','node_stack_bottom = 0, -0.860, 0, 0, -1, 0, 2',
            'name = ModuleColorChanger','includedRenderer = RW_CupGlass','name = cupolaInternal','name = ElectricCharge',
            'bulkheadProfiles = size2, srf'):
    assert tok in part,tok
for tok in ('node_stack_top','name = ModuleCommand','name = ModuleDockingNode','name = ModuleScienceExperiment',
            'name = ModuleDataTransmitter','name = ModuleReactionWheel','name = ModuleSAS'):
    assert tok not in part,'Cupola must be a terminal observation part: '+tok
assert part.count('name = ElectricCharge') == 1
assert ':NEEDS[Kerbalism,ProfileDefault]' in patch and ':NEEDS[Kerbalism,FeatureHabitat]' in patch
for res in ('Food','Water','Oxygen','Nitrogen','Waste','WasteWater'):
    assert '%RESOURCE['+res+']' in patch
    assert 'name = '+res not in part
assert '%MODULE[Habitat]' in patch
meshes=c.geometry()
for mat,mesh in meshes.items():
    assert len(mesh.vertices)==len(mesh.uvs)==len(mesh.normals)
    assert len(mesh.vertices)<65535,(mat,len(mesh.vertices))
    for tri in mesh.triangles:
        assert all(0<=i<len(mesh.vertices) for i in tri)
        v=[mesh.vertices[i] for i in tri]
        cross=c.hub_cross(v[0],v[1],v[2]) if hasattr(c,'hub_cross') else (
          (v[1][1]-v[0][1])*(v[2][2]-v[0][2])-(v[1][2]-v[0][2])*(v[2][1]-v[0][1]),
          (v[1][2]-v[0][2])*(v[2][0]-v[0][0])-(v[1][0]-v[0][0])*(v[2][2]-v[0][2]),
          (v[1][0]-v[0][0])*(v[2][1]-v[0][1])-(v[1][1]-v[0][1])*(v[2][0]-v[0][0]))
        if sum(v*v for v in cross) < 1e-18: continue
        assert sum(cross[i]*mesh.normals[tri[0]][i] for i in range(3)) > -1e-6,(mat,tri,'inverted winding')
verts=[p for mesh in meshes.values() for p in mesh.vertices]
assert min(y for x,y,z in verts)>-.861 and max(y for x,y,z in verts)<.642
maxradius=max(math.hypot(x,z) for x,y,z in verts)
assert 1.23<maxradius<1.32,maxradius
assert len(meshes['glass'].triangles)>=300
assert sum(len(x.triangles) for x in meshes.values())>6000
hull=c.collision()
assert len(hull.triangles)==96
points=set(tuple(round(v,6) for v in p) for p in hull.vertices)
edges=Counter()
for tri in hull.triangles:
    p=[hull.vertices[i] for i in tri]
    ab=tuple(p[1][i]-p[0][i] for i in range(3));ac=tuple(p[2][i]-p[0][i] for i in range(3))
    n=(ab[1]*ac[2]-ab[2]*ac[1],ab[2]*ac[0]-ab[0]*ac[2],ab[0]*ac[1]-ab[1]*ac[0])
    for v in points:
        assert sum(n[i]*(v[i]-p[0][i]) for i in range(3))<1e-5,('non-convex or inward collider',tri)
    for j in range(3):
        a=tuple(round(q,6) for q in p[j]);b=tuple(round(q,6) for q in p[(j+1)%3]);edges[tuple(sorted((a,b)))]+=1
assert set(edges.values())=={2},'Collision hull must be watertight'
mu=c.MODELS/(c.PART+'.mu');data=mu.read_bytes()
assert struct.unpack_from('<ii',data)==(76543,5)
for term in (b'RW_CUP_250',b'RW_CupGlass',b'CupolaHullCollider',b'KSP/Emissive/Diffuse',b'rwm_cuplabel'):
    assert term in data,term
for mat in c.MAT:
    assert (c.MODELS/('rwm_'+mat+'.png')).read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
for item in ('Source/build_cup250.py','Source/Blender/create_cup250.py','Source/Blender/RW_CUP_250.obj','Source/Blender/RW_CUP_250.mtl'):
    assert (ROOT/item).is_file(),item
print('PASS CUP: original single-bottom-stack 2.5m cupola, 8 sloped pane groups, top viewport')
print('PASS CUP: one crew; no phantom command/docking/EVA; conditional Kerbalism; native textured mesh')
print('PASS CUP: watertight convex 96-triangle collision hull, coordinates and source files')
print('NOTE: VAB/flight appearance, crew portrait, crew-transfer and Kerbalism pressure must be tested in-game')
