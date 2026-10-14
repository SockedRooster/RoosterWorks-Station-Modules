#!/usr/bin/env python3
"""RW-LOG-250 original two-ended station logistics/supply module.

2.5 m diameter, 3.0 m axial length. Procedural native KSP .mu plus OBJ/MTL.
Visual pressure-rated cargo door facades are sealed and non-animated; the real
interfaces are the two 2.5 m stack ends. No hatch, pilot seat or generator.
"""
from pathlib import Path
from collections import OrderedDict
import math
from PIL import Image, ImageDraw, ImageFont
import build_hab250 as h
from station_endcaps import add_endcap

ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
PART='RW_LOG_250'
TAU=h.TAU
HALF=1.50
R=1.204
MAT=OrderedDict(h.TEXTURES)  # Required by the shared canonical endcap meshes
MAT['loglabel']=(236,238,230)
MAT['logpanel']=(69,91,100)

def new_meshes():return {name:h.Mesh() for name in MAT}
def band(mesh,mat,r,y0,y1,segs=144):h.cylinder_surface(mesh[mat],r,y0,y1,segments=segs)
def panel(mesh,mat,theta,y0,y1,width,r=1.223,steps=22):
    h.flat_panel(mesh[mat],theta,y0,y1,width,r,segments=steps)
def rivet(mesh,theta,y,r=1.235,head=.009):h.radial_fastener(mesh['steel'],theta,y,radius=r,head=head)

def create_textures():
    MODELS.mkdir(parents=True,exist_ok=True)
    label=Image.new('RGB',(1024,512),(236,238,230));d=ImageDraw.Draw(label)
    d.rounded_rectangle((16,18,1008,494),radius=14,outline=(181,120,61),width=16)
    d.rectangle((38,40,986,472),outline=(50,65,73),width=5)
    def font(sz,bold=False):
        try:return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',sz)
        except OSError:return ImageFont.load_default()
    d.text((73,100),'ROOSTERWORKS',font=font(77,True),fill=(40,56,67))
    d.line((73,241,938,241),fill=(176,123,67),width=9)
    d.text((74,307),'LOG-250 / SUPPLY',font=font(68),fill=(80,70,61))
    label.paste(h.rooster_crest_image(115),(858,106))
    label.save(MODELS/'rwm_loglabel.png',optimize=True)
    vent=Image.new('RGB',(512,512),(57,76,84));d=ImageDraw.Draw(vent)
    for yy in range(20,508,20):
        d.rectangle((15,yy,497,yy+7),fill=(28,43,52))
        d.line((22,yy+8,491,yy+8),fill=(108,128,135),width=2)
    d.rectangle((9,9,503,503),outline=(132,147,146),width=9)
    for x in (22,490):
        for y in (24,488):d.ellipse((x-6,y-6,x+6,y+6),fill=(172,125,69))
    vent.save(MODELS/'rwm_logpanel.png',optimize=True)

def geometry():
    m=new_meshes()
    # Smooth opaque pressure hull, 18 longitudinal tile rows and clean dark
    # grooves. A split into small tiles is cosmetic, not separate collisions.
    # Recess opaque backing: the old R-radius backing was coplanar with the
    # white shoulder shell, causing dark/white z-fighting at both collars.
    band(m,'graphite',R-.006,-1.495,1.495)
    for col in range(16):
        t0=TAU*col/16+.012;t1=TAU*(col+1)/16-.012
        for row in range(7):
            y0=-1.36+row*2.72/7+.014;y1=-1.36+(row+1)*2.72/7-.010
            shade='cladding_white' if (col+row*3)%13==0 else 'cladding'
            h.cylinder_surface(m[shade],1.210,y0,y1,segments=5,theta0=t0,theta1=t1)
    # Constant-diameter, two-ended structural shoulders and reusable mates.
    for sign in (-1,1):
        y0,y1=(1.365,1.497) if sign>0 else (-1.497,-1.365)
        band(m,'white',R,y0,y1)
        for y,r,mat,thickness in [(1.370,1.219,'graphite',.011),
                                   (1.406,1.223,'bronze',.007),
                                   (1.457,1.217,'steel',.011)]:
            yy=sign*y
            band(m,mat,r,yy-thickness/2,yy+thickness/2)
        add_endcap(m,sign,HALF)
    # Cargo doors: 4 banks x 2 vertically spaced doors. Every tier uses an
    # opaque dark pocket, metal surround and visible latch/hinge hardware;
    # no experimental animated doors or KSP EVA triggers are claimed.
    for bank in range(4):
        theta=TAU*bank/4
        for row,cy in enumerate((-.655,.655)):
            y0=cy-.396;y1=cy+.396
            panel(m,'black',theta,y0-.069,y1+.069,.844,1.218,steps=36)
            panel(m,'graphite',theta,y0-.058,y1+.058,.806,1.228,steps=36)
            panel(m,'steel',theta,y0-.034,y1+.034,.758,1.237,steps=32)
            panel(m,'ceramic' if bank%2==0 else 'white',theta,y0-.017,y1+.017,.730,1.243,steps=32)
            # Recessed optical grille on middle of each sealed logistics cassette.
            panel(m,'logpanel',theta,cy-.250,cy+.245,.525,1.251,steps=30)
            for side in (-1,1):
                edge_t=theta+side*.344
                for dy in (-.300,.300):
                    # Four low-profile knuckle hinges, recessed to avoid
                    # colliding with another docked module at the ends.
                    h.tube(m['steel'],h.point(1.241,edge_t,cy+dy-.069),
                           h.point(1.241,edge_t,cy+dy+.069),r=.025,sides=8)
                    rivet(m,edge_t,cy+dy-.087,r=1.244)
            # Gold latch pin, dark handle and two safety label strips.
            latch_t=theta+.307
            h.tube(m['bronze'],h.point(1.248,latch_t,cy-.08),
                   h.point(1.248,latch_t,cy+.08),r=.022,sides=8)
            panel(m,'black',theta,cy+.288,cy+.320,.505,1.255,steps=27)
            panel(m,'bronze',theta,cy-.320,cy-.302,.505,1.255,steps=27)
            for dt in (-.350,.350):
                for yy in (y0-.042,y1+.044):rivet(m,theta+dt,yy,r=1.248)
    # Central continuous pressure ring makes the two stacked vault tiers read
    # as one station logistics module. Fine bronze seam provides family style.
    band(m,'graphite',1.254,-.127,.127)
    band(m,'ceramic',1.262,-.098,.098)
    band(m,'steel',1.266,-.016,.016)
    band(m,'bronze',1.274,-.004,.004)
    # Bulkhead/utility raceway conduits, guards, and real surface detail.
    for bank in range(4):
        angle=TAU*(bank+.5)/4
        for theta in (angle-.055,angle+.055):
            h.tube(m['rail'],h.point(1.245,theta,-1.10),
                   h.point(1.245,theta,1.10),r=.014,sides=8)
            for yy in (-1.10,0,1.10):
                h.tube(m['steel'],h.point(1.209,theta,yy),
                       h.point(1.245,theta,yy),r=.019,sides=7)
        panel(m,'graphite',angle,-.085,.085,.218,1.246,steps=10)
        panel(m,'bronze',angle,-.048,.048,.183,1.252,steps=10)
    # Both labels sit on structural girdle rather than covering the cargo bay.
    for theta in (TAU/8,TAU*5/8):
        panel(m,'graphite',theta,-.230,.228,.450,1.252,steps=24)
        panel(m,'bronze',theta,-.217,.215,.417,1.259,steps=24)
        panel(m,'loglabel',theta,-.207,.205,.397,1.268,steps=24)
    for theta in (TAU*3/8,TAU*7/8):
        panel(m,'graphite',theta,-.200,.200,.210,1.251,steps=14)
        panel(m,'crest',theta,-.178,.178,.186,1.258,steps=14)
    from exterior_detail import add_log
    add_log(m)
    from surface_uv import finish
    return finish(m)

def collision():
    """96 triangle watertight convex vessel collider, one per part."""
    mesh=h.Mesh();N=24
    h.cylinder_surface(mesh,R,-HALF,HALF,segments=N)
    for sign in (-1,1):
        for j in range(N):
            a=TAU*j/N;b=TAU*(j+1)/N
            pts=((0,sign*HALF,0),h.point(R,a,sign*HALF),h.point(R,b,sign*HALF))
            if sign<0:pts=(pts[0],pts[2],pts[1])
            mesh.triangle(pts,((0,sign,0),)*3,((0,0),)*3)
    return mesh

def create_mu(meshes):
    w=h.Writer(MODELS/(PART+'.mu'))
    w.i(76543,5);w.s(PART);h.node(w,PART)
    for i,(mat,mesh) in enumerate(meshes.items()):
        if not mesh.triangles:continue
        assert len(mesh.vertices)<65535,(mat,len(mesh.vertices))
        w.i(0);h.node(w,'RW_Log_'+mat)
        w.i(7);h.write_mesh(w,mesh)
        w.i(8);w.b(1);w.b(1);w.i(1,i);w.i(1)
    w.i(0);h.node(w,'LogisticsHullCollider')
    w.i(25);w.b(0);w.b(1);h.write_mesh(w,collision());w.i(1)
    w.i(10,len(MAT))
    for i,mat in enumerate(MAT):
        w.s('RW_Log_'+mat);w.s('KSP/Diffuse');w.i(2)
        w.s('_Color');w.i(0);w.f(1,1,1,1)
        w.s('_MainTex');w.i(4,i);w.f(1,1);w.f(0,0)
    w.i(12,len(MAT))
    for mat in MAT:w.s('rwm_'+mat);w.i(0)
    w.close()

def create_obj(meshes):
    f=ROOT/'Source/Blender/RW_LOG_250.obj';f.parent.mkdir(parents=True,exist_ok=True)
    mtl=f.with_suffix('.mtl')
    mtl.write_text(''.join('newmtl RW_Log_'+mat+'\nKa 0.3 0.3 0.3\nKd 1 1 1\nKs 0.2 0.2 0.2\nmap_Kd ../../GameData/RoosterWorksStationModules/Models/rwm_'+mat+'.png\n\n' for mat in MAT))
    with f.open('w') as out:
        out.write('# RoosterWorks original RW-LOG-250 geometry\nmtllib RW_LOG_250.mtl\n')
        off=0
        for mat,mesh in meshes.items():
            out.write('o RW_Log_'+mat+'\nusemtl RW_Log_'+mat+'\n')
            for p in mesh.vertices:out.write('v %.7f %.7f %.7f\n'%p)
            for p in mesh.uvs:out.write('vt %.7f %.7f\n'%p)
            for p in mesh.normals:out.write('vn %.7f %.7f %.7f\n'%p)
            for tri in mesh.triangles:
                out.write('f '+' '.join(f'{idx+off+1}/{idx+off+1}/{idx+off+1}' for idx in tri)+'\n')
            off+=len(mesh.vertices)

def main():
    create_textures();meshes=geometry();create_mu(meshes);create_obj(meshes)
    print(PART,'meshes',len(meshes),'tris',sum(len(x.triangles) for x in meshes.values()),
          'maxverts',max(len(x.vertices) for x in meshes.values()))
if __name__=='__main__':main()
