#!/usr/bin/env python3
"""RoosterWorks RW-CUP-250: original 2.5 m single-ended observation cupola.

Standalone procedurally authored 2.5m / 1.7m KSP .mu with a sloped eight-pane
panorama, top glass viewport, one bottom stack joint and watertight solid
collision geometry. No EVA, integrated docking port, or station command.

Run from any cwd: python Source/build_cup250.py
"""
from pathlib import Path
from collections import OrderedDict
import math
from PIL import Image, ImageDraw, ImageFont
import build_hab250 as h
from station_endcaps import add_endcap

ROOT=Path(__file__).resolve().parents[1]
PART='RW_CUP_250'
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
MAT=OrderedDict(list(h.TEXTURES.items())+[('cuplabel',(236,238,229))])
TAU=math.tau
BASE_Y=-.860
CROWN_Y=.625
R_SHELL=1.205

def meshes():return {name:h.Mesh() for name in MAT}
def radius(y):return 1.205+(.715-1.205)*(y+.23)/(.605+.23)
def norm(v):
    l=math.sqrt(sum(x*x for x in v));return tuple(x/l for x in v)
def point(y,t,extra=0):
    r=radius(y)+extra
    return (r*math.sin(t),y,r*math.cos(t))
def patch(mesh, ya,yb,ta,tb, offset=0,steps=4):
    """Conformal band. Recompute outward normals analytically for cone slope."""
    dr=(.715-1.205)/(.605+.23)
    for n in range(steps):
        a=ta+(tb-ta)*n/steps;b=ta+(tb-ta)*(n+1)/steps
        p=(point(ya,a,offset),point(ya,b,offset),point(yb,b,offset),point(yb,a,offset))
        ns=tuple(norm((math.sin(t),-dr,math.cos(t))) for t in (a,b,b,a))
        mesh.quad(p,ns,((n/steps,0),((n+1)/steps,0),((n+1)/steps,1),(n/steps,1)))
def label_texture():
    im=Image.new('RGB',(1024,512),(236,238,229));d=ImageDraw.Draw(im)
    d.rounded_rectangle((14,14,1010,498),radius=21,outline=(176,123,67),width=16)
    d.rectangle((39,41,985,472),outline=(42,57,69),width=5)
    try:
        title=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',76)
        subtitle=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',61)
    except OSError:title=subtitle=ImageFont.load_default()
    d.text((76,107),'ROOSTERWORKS',fill=(42,57,69),font=title)
    d.line((78,245,930,245),fill=(176,123,67),width=9)
    d.text((78,315),'CUP-250 / OBSERVE',fill=(90,70,58),font=subtitle)
    im.paste(h.rooster_crest_image(126),(856,104))
    return im

def geometry():
    m=meshes()
    # Continuous dark pressure/structural lower barrel. View panes have no
    # opaque backing: unlike surface decals they form the entire canopy wall.
    h.cylinder_surface(m['graphite'],1.18,BASE_Y+.037,-.225,segments=96)
    for j in range(16):
        a=TAU*j/16+.006;b=TAU*(j+1)/16-.006
        mat='white' if j%7==0 else 'ceramic'
        h.cylinder_surface(m[mat],1.208,-.789,-.300,segments=6,theta0=a,theta1=b)
        h.cylinder_surface(m['steel'],1.216,-.798,-.786,segments=6,theta0=a,theta1=b)
    # Reinforcing rings, scalloped separators and matching bronze trim.
    for y0,y1,r,mat in [(-.835,-.816,1.213,'white'),(-.305,-.263,1.228,'graphite'),
                        (-.260,-.250,1.237,'steel'),(-.239,-.231,1.238,'bronze')]:
        h.cylinder_surface(m[mat],r,y0,y1,segments=96)
    h.annulus(m['white'],1.163,1.227,-.230,segments=96)
    # 8 sloped panoramic panes; structural mullions replace the pressure shell
    # between glass panels. Pane strips follow the actual taper, not flat chords.
    for j in range(8):
        mid=TAU*(j+.5)/8
        a=TAU*j/8;b=TAU*(j+1)/8
        # 0.061 rad edge space (both sides): each pane spans ~0.78m near foot.
        # No opaque underlayer behind the panoramas: glass is the canopy wall.
        patch(m['glass'],-.155,.520,a+.071,b-.071,offset=.012,steps=13)
        # Thin inner graphite gasket and metallic window frame on the sloping face.
        for pa,pb in ((a+.038,a+.053),(b-.053,b-.038)):
            patch(m['steel'],-.164,.528,pa,pb,offset=.018,steps=2)
        for pa,pb in ((a+.053,a+.073),(b-.073,b-.053)):
            patch(m['black'],-.157,.522,pa,pb,offset=.023,steps=2)
        # Sloped mullions and champagne-bronze stripe between each glass panel.
        patch(m['ceramic'],-.224,.591,a+.003,a+.034,offset=.025,steps=2)
        patch(m['steel'],-.224,.591,a+.035,a+.043,offset=.032,steps=1)
        # Lower/top header strips and fasteners near frame corners.
        patch(m['white'],-.227,-.160,a+.045,b-.045,offset=.028,steps=10)
        patch(m['white'],.525,.590,a+.045,b-.045,offset=.028,steps=10)
        for t in (a+.050,b-.050):
            for y in (-.171,.541):
                h.tube(m['bronze'],point(y,t,.032),point(y,t,.053),r=.009,sides=7)
    # Crown rings and a genuine exterior top window with no hull backing.
    h.cylinder_surface(m['graphite'],.715,.584,.625,segments=96)
    h.annulus(m['ceramic'],.636,.715,.623,segments=96)
    h.annulus(m['steel'],.613,.636,.624,segments=96)
    h.annulus(m['bronze'],.597,.611,.624,segments=96)
    for j in range(96):
        a=TAU*j/96;b=TAU*(j+1)/96
        m['glass'].triangle(((0,.622,0),h.point(.595,a,.622),h.point(.595,b,.622)),
                            ((0,1,0),)*3,((.5,.5),(.5+.48*math.sin(a),.5+.48*math.cos(a)),(.5+.48*math.sin(b),.5+.48*math.cos(b))))
    for j in range(12):
        theta=TAU*j/12
        h.tube(m['steel'],h.point(.668,theta,.624),h.point(.668,theta,.640),r=.012,sides=6)
    # Lower side electronics & handholds, RoosterWorks brand on one panel.
    def flat(theta,y0,y1,angle,r,material,steps=14):
        h.flat_panel(m[material],theta,y0,y1,angle,r,segments=steps)
    flat(math.pi,-.727,-.416,.60,1.219,'graphite',30)
    flat(math.pi,-.713,-.430,.55,1.228,'bronze',30)
    flat(math.pi,-.690,-.455,.50,1.235,'cuplabel',30)
    flat(0,-.617,-.405,.30,1.220,'graphite',12)
    flat(0,-.606,-.417,.265,1.227,'crest',12)
    for theta in (-1.17,1.17):
        h.tube(m['rail'],h.point(1.247,theta,-.777),h.point(1.247,theta,-.320),r=.018,sides=8)
        for y in (-.777,-.320):
            h.tube(m['steel'],h.point(1.213,theta,y),h.point(1.247,theta,y),r=.019,sides=8)
    # Reuse canonical hub face on its single compatible bottom stack interface.
    add_endcap(m,-1,.860)
    return m

def collision():
    """96-triangle closed convex canopy prism, no hollow self-colliding walls."""
    mesh=h.Mesh();N=24
    bottom=-.86;top=.625
    for j in range(N):
        a=TAU*j/N;b=TAU*(j+1)/N
        def cone(y,t,r):return h.point(r,t,y)
        p=(cone(bottom,a,1.205),cone(bottom,b,1.205),cone(top,b,.714),cone(top,a,.714))
        mesh.quad(p,((math.sin(a),0,math.cos(a)),(math.sin(b),0,math.cos(b)),(math.sin(b),0,math.cos(b)),(math.sin(a),0,math.cos(a))))
        mesh.triangle(((0,top,0),p[3],p[2]),((0,1,0),)*3,((0,0),(0,0),(0,0)))
        mesh.triangle(((0,bottom,0),p[1],p[0]),((0,-1,0),)*3,((0,0),(0,0),(0,0)))
    return mesh

def write_mu(m):
    dest=MODELS/(PART+'.mu')
    w=h.Writer(dest);w.i(76543,5);w.s(PART);h.node(w,PART)
    for i,(mat,mesh) in enumerate(m.items()):
        if not mesh.triangles:continue
        assert len(mesh.vertices)<65535,(mat,len(mesh.vertices))
        w.i(0);h.node(w,'RW_CupGlass' if mat=='glass' else 'RW_Cup'+mat.title())
        w.i(7);h.write_mesh(w,mesh)
        w.i(8);w.b(1);w.b(1);w.i(1,i);w.i(1)
    w.i(0);h.node(w,'CupolaHullCollider')
    w.i(25);w.b(0);w.b(1);h.write_mesh(w,collision());w.i(1)
    w.i(10,len(MAT))
    for i,mat in enumerate(MAT):
        w.s('RW_Cup_'+mat);w.s('KSP/Emissive/Diffuse' if mat=='glass' else 'KSP/Diffuse')
        w.i(4 if mat=='glass' else 2)
        w.s('_Color');w.i(0);w.f(1,1,1,1)
        w.s('_MainTex');w.i(4,i);w.f(1,1);w.f(0,0)
        if mat=='glass':
            w.s('_EmissiveColor');w.i(0);w.f(0,0,0,1)
            w.s('_Emissive');w.i(4,len(MAT));w.f(1,1);w.f(0,0)
    w.i(12,len(MAT)+1)
    for mat in MAT:w.s('rwm_'+mat);w.i(0)
    w.s('rwm_cabin_emissive');w.i(0)
    w.close()

def write_obj(m):
    out=ROOT/'Source/Blender/RW_CUP_250.obj';out.parent.mkdir(parents=True,exist_ok=True)
    mtl=out.with_suffix('.mtl')
    mtl.write_text(''.join('newmtl RW_Cup_'+mat+'\nKa 0.3 0.3 0.3\nKd 1 1 1\nKs 0.2 0.2 0.2\nmap_Kd ../../GameData/RoosterWorksStationModules/Models/rwm_'+mat+'.png\n\n' for mat in MAT))
    with out.open('w') as f:
        f.write('# Original RoosterWorks panoramic observation cupola\nmtllib RW_CUP_250.mtl\n')
        off=0
        for mat,mesh in m.items():
            f.write('o '+mat+'\nusemtl RW_Cup_'+mat+'\n')
            for x,y,z in mesh.vertices:f.write(f'v {x:.7f} {y:.7f} {z:.7f}\n')
            for u,v in mesh.uvs:f.write(f'vt {u:.7f} {v:.7f}\n')
            for x,y,z in mesh.normals:f.write(f'vn {x:.7f} {y:.7f} {z:.7f}\n')
            for a,b,c in mesh.triangles:
                f.write('f '+' '.join(f'{i+off+1}/{i+off+1}/{i+off+1}' for i in (a,b,c))+'\n')
            off+=len(mesh.vertices)

def main():
    MODELS.mkdir(parents=True,exist_ok=True)
    label_texture().save(MODELS/'rwm_cuplabel.png')
    m=geometry();write_mu(m);write_obj(m)
    print(PART,'triangles',sum(len(mesh.triangles) for mesh in m.values()),'vertices',sum(len(mesh.vertices) for mesh in m.values()))

if __name__=='__main__':main()
