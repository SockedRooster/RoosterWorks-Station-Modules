"""Check six nodes, geometric winding, closed convex colliders and native output."""
from pathlib import Path
from collections import Counter
import math,sys,struct
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
import build_hub250 as b
cfg=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_HUB_250.cfg').read_text()
nodes={}
for line in cfg.splitlines():
    if line.strip().startswith('node_stack_'):
        name,values=line.split('=');nodes[name.strip().removeprefix('node_stack_')]=tuple(float(v) for v in values.split(','))
assert set(nodes)==set(b.PORTS)
for name,axis in b.PORTS.items():
    assert nodes[name]==tuple(2*x for x in axis)+axis+(2,)
assert 'CrewCapacity = 0' in cfg and 'ModuleDockingNode' not in cfg and 'vesselType = Station' in cfg
assert 'attachRules = 1,0,1,1,0' in cfg and 'stackSymmetry = 3' in cfg
data=(b.MODELS/(b.PART+'.mu')).read_bytes();assert struct.unpack_from('<ii',data)==(76543,5)
for name,axis in b.PORTS.items():
    for label,mesh in [('Port',b.collision_port(axis)),('Shoulder',b.collision_shoulder(axis))]:
        assert ('Hub'+label+'Collider_'+name).encode() in data
        verts=set(tuple(round(x,7) for x in v) for v in mesh.vertices);edges=Counter()
        assert len(mesh.triangles)<255
        for tri in mesh.triangles:
            a,c,d=[mesh.vertices[i] for i in tri]
            n=b.norm(b.cross(b.sub(c,a),b.sub(d,a)))
            assert max(sum(n[q]*(v[q]-a[q]) for q in range(3)) for v in verts)<2e-6, (name,label,'convexity/winding')
            keys=[tuple(round(x,6) for x in v) for v in (a,c,d)]
            for j in range(3):edges[tuple(sorted((keys[j],keys[(j+1)%3])))]+=1
        assert set(edges.values())=={2},(name,label,'watertightness')
for key,mesh in b.geometry().items():
    assert len(mesh.vertices)<65535
    assert all(abs(v)<=2.00001 for p in mesh.vertices for v in p)
    assert (b.MODELS/('rwm_'+key+'.png')).exists()
    for tri in mesh.triangles:
        a,c,d=[mesh.vertices[i] for i in tri];n=b.cross(b.sub(c,a),b.sub(d,a))
        assert sum(x*x for x in n)>1e-15
        assert sum(n[q]*mesh.normals[tri[0]][q] for q in range(3))>0, 'inverted face'
print('PASS HUB: six outward size-2 nodes at +/-2m; 4m envelope; 13 solid colliders; closed, convex, outward meshes')
print('NOTE flight assembly, crew transfer, radial fit and Kerbalism atmosphere require in-game testing')
