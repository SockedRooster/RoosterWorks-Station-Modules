"""Check the actual MU collision volume, KSP exit ray and window surfaces."""
from pathlib import Path
import sys, math, struct
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
import build_hab250 as b

def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

data=(b.MODELS/'RW_HAB_250.mu').read_bytes()
name=b'RW_HAB250_SolidHullCollider'
offset=data.index(bytes([len(name)])+name)+1+len(name)+40
assert struct.unpack_from('<i',data,offset)[0]==24
offset+=4
length=data[offset];offset+=1
assert data[offset:offset+length]==b'Untagged';offset+=length
layer,kind=struct.unpack_from('<ii',data,offset);offset+=8
assert layer==0 and kind==25
trigger,convex=struct.unpack_from('<BB',data,offset);offset+=2
assert trigger==0 and convex==1
start,count,submeshes,verts=struct.unpack_from('<iiii',data,offset);offset+=16
assert start==13 and submeshes==1 and verts==14
vertices=[struct.unpack_from('<fff',data,offset+i*12) for i in range(count)];offset+=count*12
assert struct.unpack_from('<i',data,offset)[0]==15;offset+=4+count*8
assert struct.unpack_from('<i',data,offset)[0]==17;offset+=4+count*12
kind,indices=struct.unpack_from('<ii',data,offset);offset+=8
assert kind==19 and indices//3==96
triangles=[struct.unpack_from('<iii',data,offset+i*12) for i in range(indices//3)]
assert b'RadialFaceCollider_' not in data and b'FlushEndcapTop' not in data

angle=math.tau/6
hatch=b.point(1.43,angle,-.64875)
distance=math.sqrt(dot(hatch,hatch))
direction=tuple(x/distance for x in hatch)
origin=tuple(hatch[k]-.5*direction[k] for k in range(3))
edges=Counter()
minimum_margin=10
for tri in triangles:
    a,c,d=[vertices[i] for i in tri]
    n=cross(sub(c,a),sub(d,a));norm=math.sqrt(dot(n,n))
    assert norm>1e-7
    n=tuple(x/norm for x in n)
    assert dot(n,a)>0, 'Collider face wound inward'
    assert max(dot(n,sub(v,a)) for v in vertices)<1e-5, 'Non-convex collision mesh'
    margin=-dot(n,sub(origin,a));minimum_margin=min(minimum_margin,margin)
    assert margin>.15, 'Stock ray origin must be well inside the solid collider'
    keys=[tuple(round(x,5) for x in v) for v in (a,c,d)]
    for i in range(3):edges[tuple(sorted((keys[i],keys[(i+1)%3])))]+=1
assert set(edges.values())=={2}, 'Collider must be watertight'

# Reproduce the former thin-box self-hit, including its exported rotations.
hits=[]
for k in range(12):
    a=math.tau*(k+.5)/12;phi=math.pi/2-a
    center=b.point(1.162,a,0)
    def local(v):return (math.cos(phi)*v[0]-math.sin(phi)*v[2],v[1],math.sin(phi)*v[0]+math.cos(phi)*v[2])
    o=local(sub(origin,center));d=local(direction);half=(.305,1.775,.045)
    if all(abs(o[i])<half[i] for i in range(3)):continue
    lo,hi=0,2
    for i in range(3):
        if abs(d[i])<1e-10:
            if abs(o[i])>half[i]:hi=-1
        else:
            values=sorted(((-half[i]-o[i])/d[i],(half[i]-o[i])/d[i]))
            lo=max(lo,values[0]);hi=min(hi,values[1])
    if lo<=hi:hits.append((k,lo))
assert hits, 'Old obstruction reproduction unexpectedly missed'

# Every surviving hull triangle stays outside every complete bank footprint.
panel=b.Mesh()
for row in range(8):
    for col in range(12):
        b.clipped_hull_panel(panel,math.tau*(col+.5)/12,-1.730+row*.4325+.014,-1.730+(row+1)*.4325-.014,math.tau/12-.027,1.204)
for tri in panel.triangles:
    theta=sum(math.atan2(panel.vertices[i][0],panel.vertices[i][2])%(math.tau) for i in tri)/3
    y=sum(panel.vertices[i][1] for i in tri)/3
    assert not any(a+1e-6<theta<c-1e-6 and d+1e-6<y<e-1e-6 for a,c,d,e in b.bay_openings())
group={k:b.Mesh() for k in b.TEXTURES}
b.panoramic_pressure_bay(group,1.0,0,.710)
for mat in ('white','graphite','black','glass'):
    mesh=group[mat]
    for ia,ib,ic in mesh.triangles:
        a,c,d=[mesh.vertices[i] for i in (ia,ib,ic)]
        n=cross(sub(c,a),sub(d,a))
        center=tuple((a[i]+c[i]+d[i])/3 for i in range(3))
        assert dot(n,(center[0],0,center[2]))>-1e-10, (mat,'inward visible surface')
        if mat=='glass':assert math.hypot(center[0],center[2])>1.2012, 'Glazing chord sinks into backing'
    assert max(math.hypot(v[0],v[2]) for v in mesh.vertices)<=1.20701
print('PASS stock exit ray reproduces old self-hit:',hits)
print('PASS native convex hull: closed, outward, 96 triangles; exit-ray origin margin %.3f m'%minimum_margin)
print('PASS hull openings across all courses, outward window faces, curved glass, window trim <= 3 mm above hull')
print('NOTE external-part obstruction and EVA/boarding still require KSP flight confirmation')
