"""Original six-way 2.5 m station connector. Units metres, Unity +Y up.

Six stack faces lie at +/-2 m. A spherical pressure body blends into six circular necks.
Thirteen convex solid colliders follow the rounded junction and its ports.
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
BODY_RADIUS=1.80
ROOT_Y=1.30
ROOT_RADIUS=math.sqrt(BODY_RADIUS**2-ROOT_Y**2)

def neck_radius(y):
    # Hermite blend: tangent to the spherical shell and cylindrical collar.
    v=(y-ROOT_Y)/(1.60-ROOT_Y)
    return ((2*v**3-3*v**2+1)*ROOT_RADIUS
            +(v**3-2*v**2+v)*(1.60-ROOT_Y)*(-ROOT_Y/ROOT_RADIUS)
            +(-2*v**3+3*v**2)*1.204)

def shoulder(t,u,lift=0):
    # Six spherical face patches meet exactly along their shared great circles.
    # The old cube-face roots have been removed entirely.
    if u<=.5:
        edge_phi=math.atan(1/max(abs(math.sin(t)),abs(math.cos(t))))
        root_phi=math.acos(ROOT_Y/BODY_RADIUS)
        phi=edge_phi+(root_phi-edge_phi)*(u*2)
        r=BODY_RADIUS*math.sin(phi);y=BODY_RADIUS*math.cos(phi)
    else:
        y=ROOT_Y+(u-.5)*2*(1.60-ROOT_Y);r=neck_radius(y)
    return h.point(r,t,y+lift)

def shoulder_normal(t,u):
    if u<=.5:return norm(shoulder(t,u))
    tangent=sub(shoulder(t+.00001,u),shoulder(t-.00001,u))
    slope=sub(shoulder(t,u+.00001),shoulder(t,u-.00001))
    return norm(cross(tangent,slope))

def shoulder_quad(mesh,a,b,u,v,lift,panel):
    samples=((a,u),(b,u),(b,v),(a,v))
    mesh.quad([shoulder(t,k,lift) for t,k in samples],
              [shoulder_normal(t,k) for t,k in samples],
              [(max(0,min(1,t/(math.tau/8)-panel)),k) for t,k in samples])

def geometry():
    meshes={k:h.Mesh() for k in MAT}
    for name,axis in PORTS.items():
        m={k:h.Mesh() for k in MAT}
        # Curved thermal petals subdivide the spherical core and necks.
        for j in range(64):
            a=math.tau*j/64;b=math.tau*(j+1)/64;panel=j//8
            left_gap=.002 if j%8==0 else 0
            right_gap=.002 if j%8==7 else 0
            for k in range(20):
                u=k/20;v=(k+1)/20
                shoulder_quad(m['graphite'],a,b,u,v,0,panel)
                # Narrow joints show the continuous pressure shell beneath.
                lo=.008 if k==0 else u;hi=.992 if k==19 else v
                shoulder_quad(m['cladding_white' if panel%3==0 else 'cladding'],
                              a+left_gap,b-right_gap,lo,hi,.002,panel)
        h.cylinder_surface(m['ceramic'],1.204,1.60,1.985,segments=64)
        for y0,y1,r,mat in [(1.60,1.625,1.211,'steel'),(1.67,1.685,1.216,'graphite'),
                            (1.88,1.90,1.214,'steel'),(1.91,1.918,1.220,'bronze'),
                            (1.96,2.0,1.225,'white')]:
            h.cylinder_surface(m[mat],r,y0,y1,segments=64)
        from station_endcaps import face_mesh
        for mat,mesh in face_mesh().items():
            if mesh.triangles:append(m[mat],mesh)
        from exterior_detail import add_hub_port
        add_hub_port(m)
        for mat in MAT:append(meshes[mat],rotate(m[mat],axis))
    from surface_uv import finish
    return finish(meshes)
def collision_port(axis):
    m=h.Mesh();h.cylinder_surface(m,1.204,1.60,2.0,segments=24)
    for y,sgn in [(1.60,-1),(2.0,1)]:
        for j in range(24):
            pts=[(0,y,0),h.point(1.204,math.tau*j/24,y),h.point(1.204,math.tau*(j+1)/24,y)]
            if sgn<0:pts.reverse()
            m.triangle(pts,[(0,sgn,0)]*3,[(.5,.5),(0,0),(1,0)])
    return rotate(m,axis)
def collision_shoulder(axis):
    # Conservative closed frustum, overlapping the spherical central collider.
    # Its sides stay inside the curved visible neck rather than retaining the
    # previous invisible square shoulders.
    mesh=h.Mesh();y0=1.24;y1=1.60;r0=1.10;r1=1.204
    for j in range(24):
        a=math.tau*j/24;b=math.tau*(j+1)/24
        quad(mesh,[h.point(r0,a,y0),h.point(r0,b,y0),h.point(r1,b,y1),h.point(r1,a,y1)])
        for y,r,sgn in ((y0,r0,-1),(y1,r1,1)):
            pts=[(0,y,0),h.point(r,a,y),h.point(r,b,y)]
            if sgn<0:pts.reverse()
            mesh.triangle(pts,[(0,sgn,0)]*3,[(.5,.5),(0,0),(1,0)])
    return rotate(mesh,axis)

def collision_central():
    # Inscribed sphere: 224 triangles, below Unity's convex cooking limit.
    mesh=h.Mesh();n=16;rows=8
    def p(j,k):
        phi=math.pi*k/rows
        return h.point(BODY_RADIUS*math.sin(phi),math.tau*j/n,BODY_RADIUS*math.cos(phi))
    def face(pts):
        center=tuple(sum(p[q] for p in pts)/3 for q in range(3))
        if sum(x*y for x,y in zip(cross(sub(pts[1],pts[0]),sub(pts[2],pts[0])),center))<0:pts.reverse()
        mesh.triangle(pts,[norm(p) for p in pts],[(0,0),(1,0),(1,1)])
    for j in range(n):
        face([p(j,0),p(j,1),p(j+1,1)])
        for k in range(1,rows-1):
            face([p(j,k),p(j,k+1),p(j+1,k+1)])
            face([p(j,k),p(j+1,k+1),p(j+1,k)])
        face([p(j,rows-1),p(j,rows),p(j+1,rows-1)])
    return mesh

def create_mu(meshes):
    w=h.Writer(MODELS/(PART+'.mu'));w.i(76543,5);w.s(PART);h.node(w,PART)
    for index,(mat,mesh) in enumerate(meshes.items()):
        if not mesh.triangles:continue
        w.i(0);h.node(w,'RW_Hub_'+mat)
        w.i(7);h.write_mesh(w,mesh)
        w.i(8);w.b(1);w.b(1);w.i(1,index);w.i(1)
    w.i(0);h.node(w,'HubCentralCollider')
    w.i(25);w.b(0);w.b(1);h.write_mesh(w,collision_central());w.i(1)
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
