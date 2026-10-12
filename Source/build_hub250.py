"""Original six-way 2.5 m station connector. Units metres, Unity +Y up.

Six stack faces lie at +/-2 m. Smooth square-to-round shoulders enclose a
central pressure volume. Seven solid colliders preserve the concave outline.
No seats, exterior EVA hatch, command electronics or built-in docking ports.
"""
from pathlib import Path
from collections import OrderedDict
import math
from PIL import Image,ImageDraw,ImageFont
import build_hab250 as h

ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
PART='RW_HUB_250'
MAT=OrderedDict((k,v) for k,v in h.TEXTURES.items() if k not in ('glass','label','hubblanket'))
MAT['hublabel']=(235,237,229)
MAT['hubblanket']=(151,113,66)
PORTS={'top':(0,1,0),'bottom':(0,-1,0),'right':(1,0,0),
       'left':(-1,0,0),'front':(0,0,1),'back':(0,0,-1)}
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def norm(v):
    size=math.sqrt(sum(x*x for x in v))
    return tuple(x/size for x in v)
def orient(p,axis):
    # Proper rotation: local Y becomes port's outward normal.
    right=(1,0,0) if axis[1] else (axis[2],0,-axis[0])
    forward=cross(right,axis)
    return tuple(p[0]*right[i]+p[1]*axis[i]+p[2]*forward[i] for i in range(3))
def rotate(mesh,axis):
    return h.Mesh([orient(p,axis) for p in mesh.vertices],
                  [orient(n,axis) for n in mesh.normals],list(mesh.uvs),list(mesh.triangles))
def append(dest,src):
    offset=len(dest.vertices)
    dest.vertices.extend(src.vertices);dest.normals.extend(src.normals);dest.uvs.extend(src.uvs)
    dest.triangles.extend(tuple(i+offset for i in t) for t in src.triangles)
def quad(mesh,p,uv=((0,0),(1,0),(1,1),(0,1))):
    n=norm(cross(sub(p[1],p[0]),sub(p[2],p[0])))
    mesh.quad(p,(n,)*4,uv)
def shoulder(t,u,lift=0):
    r0=1.25/max(abs(math.sin(t)),abs(math.cos(t)))
    r=r0*(1-u)+1.204*u
    return h.point(r,t,1.25+.35*u+lift)
def geometry():
    meshes={k:h.Mesh() for k in MAT}
    for name,axis in PORTS.items():
        m={k:h.Mesh() for k in MAT}
        # Eight thermal panels per shoulder; dark joints remain narrow.
        for j in range(64):
            a=math.tau*j/64;b=math.tau*(j+1)/64
            quad(m['graphite'],[shoulder(a,0),shoulder(b,0),shoulder(b,1),shoulder(a,1)])
            left_gap=.002 if j%8==0 else 0
            right_gap=.002 if j%8==7 else 0
            quad(m['white' if j//8%3==0 else 'ceramic'],
                 [shoulder(a+left_gap,.015,.002),shoulder(b-right_gap,.015,.002),
                  shoulder(b-right_gap,.985,.002),shoulder(a+left_gap,.985,.002)])
        for material in ('graphite','ceramic','white'):
            mesh=m[material]
            mesh.uvs=[(math.atan2(x,z)/math.tau+.5,y*.5) for x,y,z in mesh.vertices]
            # Keep each octant's deliberate crease, smooth subdivisions within it.
            for i,(x,y,z) in enumerate(mesh.vertices):
                t=math.atan2(x,z);u=max(0,min(1,(y-1.25)/.35))
                tangent=sub(shoulder(t+.00001,u),shoulder(t-.00001,u))
                slope=sub(shoulder(t,1),shoulder(t,0))
                mesh.normals[i]=norm(cross(tangent,slope))
        h.cylinder_surface(m['ceramic'],1.204,1.60,1.985,segments=64)
        for y0,y1,r,mat in [(1.60,1.625,1.211,'steel'),(1.67,1.685,1.216,'graphite'),
                            (1.88,1.90,1.214,'steel'),(1.91,1.918,1.220,'bronze'),
                            (1.96,2.0,1.225,'white')]:
            h.cylinder_surface(m[mat],r,y0,y1,segments=64)
        from station_endcaps import face_mesh
        for mat,mesh in face_mesh().items():
            if mesh.triangles:append(m[mat],mesh)
        for mat in MAT:append(meshes[mat],rotate(m[mat],axis))
    return meshes
def collision_port(axis):
    m=h.Mesh();h.cylinder_surface(m,1.204,1.24,2.0,segments=24)
    for y,sgn in [(1.24,-1),(2.0,1)]:
        for j in range(24):
            pts=[(0,y,0),h.point(1.204,math.tau*j/24,y),h.point(1.204,math.tau*(j+1)/24,y)]
            if sgn<0:pts.reverse()
            m.triangle(pts,[(0,sgn,0)]*3,[(.5,.5),(0,0),(1,0)])
    return rotate(m,axis)
def collision_shoulder(axis):
    # Convex hull of the square root and circular collar. Compute supporting
    # planes rather than relying on Unity to repair a nonconvex input mesh.
    from itertools import combinations
    pts=[(x,1.25,z) for x in (-1.25,1.25) for z in (-1.25,1.25)]
    pts += [h.point(1.204,math.tau*j/24,1.60) for j in range(24)]
    planes={}
    for i,j,k in combinations(range(len(pts)),3):
        raw=cross(sub(pts[j],pts[i]),sub(pts[k],pts[i]))
        if sum(x*x for x in raw)<1e-12:continue
        n=norm(raw);ds=[sum(n[q]*(p[q]-pts[i][q]) for q in range(3)) for p in pts]
        if max(ds)>1e-7 and min(ds)<-1e-7:continue
        if max(ds)>1e-7:n=tuple(-x for x in n)
        face=tuple(p for p,d in enumerate(ds) if abs(d)<1e-7)
        planes[face]=n
    mesh=h.Mesh()
    for ids,n in planes.items():
        center=tuple(sum(pts[i][q] for i in ids)/len(ids) for q in range(3))
        u=norm(sub(pts[ids[0]],center));v=cross(n,u)
        def angle(i):
            p=sub(pts[i],center)
            return math.atan2(sum(p[q]*v[q] for q in range(3)),sum(p[q]*u[q] for q in range(3)))
        ordered=sorted(ids,key=angle)
        for i in range(1,len(ordered)-1):
            mesh.triangle([pts[ordered[0]],pts[ordered[i]],pts[ordered[i+1]]],[n]*3,[(0,0),(1,0),(1,1)])
    return rotate(mesh,axis)
def create_mu(meshes):
    w=h.Writer(MODELS/(PART+'.mu'));w.i(76543,5);w.s(PART);h.node(w,PART)
    for index,(mat,mesh) in enumerate(meshes.items()):
        if not mesh.triangles:continue
        w.i(0);h.node(w,'RW_Hub_'+mat)
        w.i(7);h.write_mesh(w,mesh)
        w.i(8);w.b(1);w.b(1);w.i(1,index);w.i(1)
    w.i(0);h.node(w,'HubCentralCollider',collider=(2.5,2.5,2.5));w.i(1)
    for name,axis in PORTS.items():
        w.i(0);h.node(w,'HubPortCollider_'+name)
        w.i(25);w.b(0);w.b(1);h.write_mesh(w,collision_port(axis));w.i(1)
        w.i(0);h.node(w,'HubShoulderCollider_'+name)
        w.i(25);w.b(0);w.b(1);h.write_mesh(w,collision_shoulder(axis));w.i(1)
    w.i(10,len(MAT))
    for index,mat in enumerate(MAT):
        w.s('RW_Hub_'+mat);w.s('KSP/Diffuse');w.i(2)
        w.s('_Color');w.i(0);w.f(1,1,1,1)
        w.s('_MainTex');w.i(4,index);w.f(1,1);w.f(0,0)
    w.i(12,len(MAT))
    for mat in MAT:w.s('rwm_'+mat);w.i(0)
    w.close()
def main():
    im=Image.new('RGB',(1024,512),(235,237,229));d=ImageDraw.Draw(im)
    d.rectangle((12,12,1012,500),outline=(176,123,67),width=18)
    font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',100)
    d.text((65,75),'ROOSTERWORKS',font=font,fill=(42,57,69))
    d.text((65,265),'HUB-250 / 6-WAY',font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',86),fill=(80,70,58))
    im.save(MODELS/'rwm_hublabel.png')
    # Original low-contrast bronze insulation texture; deterministic and
    # independently authored, using no pixels from the reference add-on.
    import random
    rng=random.Random(25052)
    blanket=Image.new('RGB',(512,256))
    pixels=[]
    for yy in range(256):
        for xx in range(512):
            wave=5*math.sin(xx*.17+math.sin(yy*.053)*2)+3*math.sin(xx*.61+yy*.033)
            noise=rng.uniform(-2,2)
            pixels.append(tuple(max(0,min(255,int(c+wave+noise))) for c in (151,113,66)))
    blanket.putdata(pixels);blanket.save(MODELS/'rwm_hubblanket.png')

    meshes=geometry();create_mu(meshes)
    # The established OBJ exporter supports arbitrary material dictionaries.
    import build_cmd250 as obj
    obj.MAT=MAT;obj.create_obj(meshes,ROOT/'Source/Blender/RW_HUB_250.obj')
    print(PART,sum(len(m.triangles) for m in meshes.values()),'triangles')
if __name__=='__main__':main()
