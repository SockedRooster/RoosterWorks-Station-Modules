"""RW-ADP-250-375: original crewless 2.5-to-3.75 m station transition.

Small +Y face, large -Y face, 1.8 m axial length. Shared sealed endcap
geometry is enlarged radially at the large face, with correct normal scaling.
"""
from pathlib import Path
from collections import OrderedDict
import math
import build_hab250 as h
from station_endcaps import face_mesh,append
from surface_uv import finish
ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
PART='RW_ADP_250_375';HALF=.9;SHOULDER=.72;SMALL=1.204;LARGE=SMALL*1.5
MAT=OrderedDict(h.TEXTURES);MAT['adplabel']=(235,237,229)

def radius(y):
    t=max(0,min(1,(y+SHOULDER)/(2*SHOULDER)))
    return LARGE+(SMALL-LARGE)*t

def normal(t,y):
    slope=(SMALL-LARGE)/(2*SHOULDER) if -SHOULDER<y<SHOULDER else 0
    v=(math.sin(t),-slope,math.cos(t));length=math.sqrt(sum(x*x for x in v))
    return tuple(x/length for x in v)

def panel(mesh,theta,y0,y1,width,lift=0,steps=12):
    for j in range(steps):
        a=theta-width/2+width*j/steps;b=theta-width/2+width*(j+1)/steps
        samples=((a,y0),(b,y0),(b,y1),(a,y1))
        mesh.quad([h.point(radius(y)+lift,t,y) for t,y in samples],
                  [normal(t,y) for t,y in samples],
                  ((j/steps,0),((j+1)/steps,0),((j+1)/steps,1),(j/steps,1)))

def add_cap(m,sign,scale):
    for mat,src in face_mesh().items():
        verts=[(x*scale,sign*(HALF+y-2),sign*z*scale) for x,y,z in src.vertices]
        normals=[]
        for x,y,z in src.normals:
            n=(x/scale,sign*y,sign*z/scale);length=math.sqrt(sum(v*v for v in n))
            normals.append(tuple(v/length for v in n))
        append(m[mat],h.Mesh(verts,normals,list(src.uvs),list(src.triangles)))

def geometry():
    m={name:h.Mesh() for name in MAT}
    # Continuous underlying cone, covered by individual curved shield tiles.
    panel(m['graphite'],math.pi,-SHOULDER,SHOULDER,math.tau,steps=96)
    for col in range(16):
        theta=math.tau*(col+.5)/16
        for row in range(4):
            y0=-SHOULDER+row*(2*SHOULDER)/4+.007
            y1=-SHOULDER+(row+1)*(2*SHOULDER)/4-.007
            panel(m['cladding_white' if col%4==0 else 'cladding'],theta,y0,y1,math.tau/16-.016,.002,6)
    for sign,r,scale in ((1,SMALL,1),(-1,LARGE,1.5)):
        y0,y1=(SHOULDER,HALF) if sign>0 else (-HALF,-SHOULDER)
        h.cylinder_surface(m['white'],r+.003,y0,y1,segments=96)
        for y,width,extra,mat in ((.752,.016,.010,'steel'),(.805,.006,.017,'bronze')):
            h.cylinder_surface(m[mat],r+extra*scale,sign*y-width/2,sign*y+width/2,segments=96)
        add_cap(m,sign,scale)
    # Conformal service plaques; no flat floating backing over the taper.
    for theta in (0,math.pi):
        for mat,y0,y1,width,lift in (('graphite',-.235,.205,.51,.010),('bronze',-.221,.191,.48,.015),('adplabel',-.201,.171,.44,.020)):
            panel(m[mat],theta,y0,y1,width,lift,28)
    for theta in (math.pi/2,3*math.pi/2):
        panel(m['graphite'],theta,-.125,.135,.23,.009,16)
        panel(m['crest'],theta,-.112,.122,.205,.014,16)
    # Small reinforcing spines and protected service lines follow the slope.
    for j in range(4):
        theta=math.tau*(j+.5)/4
        panel(m['steel'],theta,-.66,.66,.028,.010,4)
        for dt,mat in ((-.045,'graphite'),(.045,'bronze')):
            for k in range(8):
                y0=-.64+1.28*k/8;y1=-.64+1.28*(k+1)/8
                h.tube(m[mat],h.point(radius(y0)+.019,theta+dt,y0),h.point(radius(y1)+.019,theta+dt,y1),r=.007,sides=6)
        for y in (-.59,0,.59):panel(m['steel'],theta,y-.014,y+.014,.12,.026,8)
    return finish(m)

def collision_section(y0,y1,r0,r1):
    mesh=h.Mesh();N=24
    for j in range(N):
        a=math.tau*j/N;b=math.tau*(j+1)/N
        pts=[h.point(r0,a,y0),h.point(r0,b,y0),h.point(r1,b,y1),h.point(r1,a,y1)]
        v=(math.sin(a),(r0-r1)/(y1-y0),math.cos(a));length=math.sqrt(sum(x*x for x in v))
        n=tuple(x/length for x in v);mesh.quad(pts,[n]*4)
        for y,r,sign in ((y0,r0,-1),(y1,r1,1)):
            pts=[(0,y,0),h.point(r,a,y),h.point(r,b,y)]
            if sign<0:pts.reverse()
            mesh.triangle(pts,[(0,sign,0)]*3,[(0,0)]*3)
    return mesh

def colliders():
    return {'AdapterLargeCollar':collision_section(-HALF,-SHOULDER,LARGE,LARGE),
            'AdapterTaper':collision_section(-SHOULDER,SHOULDER,LARGE,SMALL),
            'AdapterSmallCollar':collision_section(SHOULDER,HALF,SMALL,SMALL)}

def create_mu(m):
    w=h.Writer(MODELS/(PART+'.mu'));w.i(76543,5);w.s(PART);h.node(w,PART)
    for index,(mat,mesh) in enumerate(m.items()):
        if not mesh.triangles:continue
        assert len(mesh.vertices)<65535
        w.i(0);h.node(w,'RW_Adapter_'+mat);w.i(7);h.write_mesh(w,mesh)
        w.i(8);w.b(1);w.b(1);w.i(1,index);w.i(1)
    for name,mesh in colliders().items():
        w.i(0);h.node(w,name);w.i(25);w.b(0);w.b(1);h.write_mesh(w,mesh);w.i(1)
    w.i(10,len(MAT))
    for index,mat in enumerate(MAT):
        w.s('RW_Adapter_'+mat);w.s('KSP/Diffuse');w.i(2)
        w.s('_Color');w.i(0);w.f(1,1,1,1);w.s('_MainTex');w.i(4,index);w.f(1,1);w.f(0,0)
    w.i(12,len(MAT))
    for mat in MAT:w.s('rwm_'+mat);w.i(0)
    w.close()

def build():
    from appearance_textures import label,font
    from PIL import ImageDraw
    im=label('ADP-250/375','ADAPTER');d=ImageDraw.Draw(im)
    d.rectangle((47,47,976,86),fill=(48,64,70))
    d.text((65,49),'STRUCTURAL SYSTEMS   /   2.5 M TO 3.75 M',font=font(23,True),fill=(229,232,221))
    im.save(MODELS/'rwm_adplabel.png',optimize=True)
    m=geometry();create_mu(m)
    import build_cmd250 as obj
    previous=obj.MAT;obj.MAT=MAT
    obj.create_obj(m,ROOT/'Source/Blender/RW_ADP_250_375.obj');obj.MAT=previous
    print('Built RW-ADP-250-375:',sum(len(mesh.triangles) for mesh in m.values()),'visual triangles')

if __name__=='__main__':build()
