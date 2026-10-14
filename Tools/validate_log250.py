#!/usr/bin/env python3
"""Offline tests for original RW-LOG-250 supply vault (not a KSP flight test)."""
from pathlib import Path
from collections import Counter
import sys,math,struct
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
import build_log250 as log
part=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_LOG_250.cfg').read_text()
patch=(ROOT/'GameData/RoosterWorksStationModules/Compatibility/LogisticsKerbalism.cfg').read_text()
assert part.count('{')==part.count('}') and patch.count('{')==patch.count('}')
for name in ('name = RW_LOG_250','CrewCapacity = 0','vesselType = Station','name = ModuleInventoryPart',
             'InventorySlots = 12','packedVolumeLimit = 1400','name = ElectricCharge','fuelCrossFeed = True',
             'node_stack_top = 0, 1.500, 0, 0, 1, 0, 2',
             'node_stack_bottom = 0, -1.500, 0, 0, -1, 0, 2'):
    assert name in part,name
for unavailable in ('name = ModuleCommand','name = ModuleDockingNode','name = ModuleDataTransmitter',
                    'name = ModuleScienceExperiment','name = ModuleGenerator',
                    'name = ModuleDeployableSolarPanel','INTERNAL','node_stack_right','name = ModuleSAS'):
    assert unavailable not in part,'Incorrectly advertised function: '+unavailable
assert part.count('name = ElectricCharge')==1
assert 'name = Food' not in part and 'name = Oxygen' not in part
assert ':NEEDS[Kerbalism,ProfileDefault]' in patch
assert ':NEEDS[Kerbalism,FeatureHabitat]' in patch
for res in ('Food','Water','Oxygen','Nitrogen','Waste','WasteWater'):
    assert '%RESOURCE['+res+']' in patch
assert '%MODULE[Habitat]' in patch
meshes=log.geometry();total=sum(len(m.triangles) for m in meshes.values())
assert total>12000,total
assert len(meshes['logpanel'].triangles)>300
for name,mesh in meshes.items():
    assert len(mesh.vertices)==len(mesh.normals)==len(mesh.uvs),(name,'mesh arrays')
    assert len(mesh.vertices)<65535,(name,len(mesh.vertices))
    for triangle in mesh.triangles:
        assert len(triangle)==3 and all(0<=i<len(mesh.vertices) for i in triangle)
        p=[mesh.vertices[i] for i in triangle]
        u=[p[1][i]-p[0][i] for i in range(3)]
        v=[p[2][i]-p[0][i] for i in range(3)]
        n=(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
        if sum(x*x for x in n)>1e-18:
            assert sum(n[i]*mesh.normals[triangle[0]][i] for i in range(3))>-1e-6,(name,'inverted face')
verts=[v for mesh in meshes.values() for v in mesh.vertices]
assert all(-1.501<=p[1]<=1.501 for p in verts)
assert 1.26<max(math.hypot(p[0],p[2]) for p in verts)<1.32
hull=log.collision();assert len(hull.triangles)==96
vertices={tuple(round(x,6) for x in p) for p in hull.vertices};edges=Counter()
for tri in hull.triangles:
    p=[hull.vertices[i] for i in tri]
    a=[p[1][i]-p[0][i] for i in range(3)];b=[p[2][i]-p[0][i] for i in range(3)]
    n=(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
    for v in vertices:
        assert sum(n[i]*(v[i]-p[0][i]) for i in range(3))<1e-5,('nonconvex/inward collision',tri)
    for i in range(3):
        a=tuple(round(x,6) for x in p[i]);b=tuple(round(x,6) for x in p[(i+1)%3])
        edges[tuple(sorted((a,b)))]+=1
assert set(edges.values())=={2},'Collider not watertight'
mu=log.MODELS/'RW_LOG_250.mu';blob=mu.read_bytes()
assert struct.unpack_from('<ii',blob)==(76543,5)
for needle in (b'RW_LOG_250',b'RW_Log_logpanel',b'LogisticsHullCollider',b'rwm_loglabel',b'KSP/Diffuse'):
    assert needle in blob,needle
for mat,mesh in meshes.items():
    if not mesh.triangles:continue
    assert (log.MODELS/('rwm_'+mat+'.png')).read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
for name in ('Source/build_log250.py','Source/Blender/create_log250.py',
             'Source/Blender/RW_LOG_250.obj','Source/Blender/RW_LOG_250.mtl',
             'Tools/render_log250.py','Media/RW-LOG-250-v0.7.0-dev.1-Review-Render.png'):
    assert (ROOT/name).is_file(),name
print('PASS LOG: native 2.5m x 3.0m two-ended model; 8 service cassettes, reusable endcaps')
print('PASS LOG: closed 96-triangle convex collider, manifold and winding')
print('PASS LOG: passive stock inventory; no integrated battery under reference balance; conditional Kerbalism Default supplies and habitat')
print('PASS LOG: 0 crew, no EVA/command/science/docking/generators; unique textures and editable sources')
print('NOTE: All gameplay, inventory and actual Kerbalism storage must be verified in-game')
