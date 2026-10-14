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
from native_model import load,walk
model=load(b.MODELS/(b.PART+'.mu'))
exported={n['name']:n for _,n in walk(model.root) if 'collider' in n}
expected={'HubCentralCollider':b.collision_central()}
for name,axis in b.PORTS.items():
    expected['HubPortCollider_'+name]=b.collision_port(axis)
    expected['HubShoulderCollider_'+name]=b.collision_shoulder(axis)
assert set(exported)==set(expected) and len(expected)==13
for name,mesh in expected.items():
        node=exported[name];collider=node['collider']
        assert node['position']==(0,0,0) and node['rotation']==(0,0,0,1) and node['scale']==(1,1,1)
        assert collider['type']=='mesh' and collider['trigger']==0 and collider['convex']==1
        actual=collider['mesh']
        assert len(actual['vertices'])==len(mesh.vertices)
        assert actual['submeshes']==[mesh.triangles]
        assert max(abs(a-c) for p,q in zip(actual['vertices'],mesh.vertices) for a,c in zip(p,q))<2e-7
        verts=set(tuple(round(x,7) for x in v) for v in mesh.vertices);edges=Counter()
        assert len(mesh.triangles)<255
        for tri in mesh.triangles:
            a,c,d=[mesh.vertices[i] for i in tri]
            n=b.norm(b.cross(b.sub(c,a),b.sub(d,a)))
            assert max(sum(n[q]*(v[q]-a[q]) for q in range(3)) for v in verts)<2e-6, (name,'convexity/winding')
            # Sample the entire collider surface against the analytic visible
            # pressure body. Square invisible corners must not survive export.
            for weights in ((1,0,0),(0,1,0),(0,0,1),(.5,.5,0),(.5,0,.5),(0,.5,.5),(1/3,1/3,1/3)):
                p=tuple(sum(weights[i]*point[q] for i,point in enumerate((a,c,d))) for q in range(3))
                axis_index=max(range(3),key=lambda i:abs(p[i]));y=abs(p[axis_index])
                radius=math.sqrt(sum(p[i]**2 for i in range(3) if i!=axis_index))
                if y<=b.ROOT_Y:assert sum(x*x for x in p)<=b.BODY_RADIUS**2+1e-6
                elif y<1.60:assert radius<=b.neck_radius(y)+1e-6,(name,'collider outside curved neck',p)
                else:assert radius<=1.204001 and y<=2.000001
            keys=[tuple(round(x,6) for x in v) for v in (a,c,d)]
            for j in range(3):edges[tuple(sorted((keys[j],keys[(j+1)%3])))]+=1
        assert set(edges.values())=={2},(name,'watertightness')
# Shared spherical boundaries occupy the same points and carry radial normals.
for j in range(65):
    t=math.tau*j/64;p=b.shoulder(t,0)
    assert abs(sum(x*x for x in p)-b.BODY_RADIUS**2)<1e-9
    assert abs(max(abs(p[0]),abs(p[2]))-p[1])<1e-9
    n=b.shoulder_normal(t,0)
    assert sum(a*c for a,c in zip(n,b.norm(p)))>1-1e-9
    assert abs(b.shoulder(t,.5)[1]-b.ROOT_Y)<1e-9
    assert abs(math.hypot(b.shoulder(t,1)[0],b.shoulder(t,1)[2])-1.204)<1e-9
assert abs((b.neck_radius(b.ROOT_Y+1e-6)-b.neck_radius(b.ROOT_Y))/1e-6+b.ROOT_Y/b.ROOT_RADIUS)<2e-5
assert abs((b.neck_radius(1.60)-b.neck_radius(1.60-1e-6))/1e-6)<2e-5
for key,mesh in b.geometry().items():
    assert len(mesh.vertices)<65535
    assert all(abs(v)<=2.00001 for p in mesh.vertices for v in p)
    assert (b.MODELS/('rwm_'+key+'.png')).exists()
    for tri in mesh.triangles:
        a,c,d=[mesh.vertices[i] for i in tri];n=b.cross(b.sub(c,a),b.sub(d,a))
        assert sum(x*x for x in n)>1e-15
        assert sum(n[q]*mesh.normals[tri[0]][q] for q in range(3))>0, 'inverted face'
print('PASS HUB: six unchanged size-2 nodes; 4m envelope; spherical shared seams and tangent necks; 13 exported closed convex colliders fit rounded body')
print('NOTE flight assembly, crew transfer, radial fit and Kerbalism atmosphere require in-game testing')
