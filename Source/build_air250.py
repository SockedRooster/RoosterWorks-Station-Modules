"""RW-AIR-250: original compact EVA chamber, Unity metres, native MU.

2.5 m interfaces, 2.4 m long, two seats. Always-present stock Airlock/Ladder
triggers; no hatch animation or custom pressure-cycle simulation is implied.
"""
from pathlib import Path
from collections import OrderedDict
import math
import build_hab250 as h
from station_endcaps import add_endcap
from exterior_detail import plate,connector,conduit
from surface_uv import finish
ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
PART='RW_AIR_250';HALF=1.2;R=1.204;HATCH_Y=-.15
MAT=OrderedDict(h.TEXTURES);MAT['airlabel']=(235,237,229)

def geometry():
    m={name:h.Mesh() for name in MAT}
    h.cylinder_surface(m['graphite'],1.198,-HALF,HALF,segments=96)
    for col in range(16):
        a=math.tau*col/16+.009;b=math.tau*(col+1)/16-.009
        for row in range(5):
            y0=-1.06+row*2.12/5+.009;y1=-1.06+(row+1)*2.12/5-.009
            h.cylinder_surface(m['cladding_white' if col%5==0 else 'cladding'],1.204,y0,y1,segments=6,theta0=a,theta1=b)
    for sign in (-1,1):
        lo,hi=(1.025,HALF) if sign>0 else (-HALF,-1.025)
        h.cylinder_surface(m['white'],1.209,lo,hi,segments=96)
        for y,r,width,mat in ((1.045,1.217,.013,'steel'),(1.095,1.221,.005,'bronze')):
            h.cylinder_surface(m[mat],r,sign*y-width/2,sign*y+width/2,segments=96)
        add_endcap(m,sign,HALF)
    # Seated pressure hatch with inherited hinges, latch, porthole and gasket.
    h.hatch_pressure_bay(m,0,HATCH_Y,.92)
    # Twin boarding rails face the exit; local ladder +Y remains climb-up.
    for theta in (-.36,.36):
        h.tube(m['rail'],h.point(1.282,theta,-.90),h.point(1.282,theta,.55),r=.019,sides=10)
        for y in (-.88,-.43,.08,.53):
            h.tube(m['steel'],h.point(1.209,theta,y),h.point(1.282,theta,y),r=.024,sides=10)
    for y in (-.91,-.72,-.53):
        h.tube(m['steel'],h.point(1.284,-.28,y),h.point(1.284,.28,y),r=.019,sides=10)
    # Pressure-service manifold and suit connections, kept clear of EVA path.
    for theta in (1.35,-1.35):
        plate(m,theta,-.08,.29,.65,slot=1,radius=1.236)
        connector(m,theta-.23,.10);connector(m,theta-.23,-.25)
        conduit(m,theta+.24,-.67,.66)
        plate(m,theta,.82,.24,.17,slot=5,radius=1.237)
    # Distinct rear oxygen-service bank and readable family identifier.
    plate(m,math.pi,.60,.40,.26,slot=0,radius=1.237)
    for mat,width,rad,y0,y1 in (('graphite',.78,1.219,-.42,.13),('bronze',.74,1.227,-.40,.11),('airlabel',.70,1.237,-.37,.08)):
        h.flat_panel(m[mat],math.pi,y0,y1,width,rad,32)
    h.flat_panel(m['crest'],0,.63,.91,.26,1.231,16)
    return finish(m)

def collision():
    m=h.Mesh();h.cylinder_surface(m,R,-HALF,HALF,segments=24)
    for sign in (-1,1):
        y=sign*HALF
        for j in range(24):
            pts=[(0,y,0),h.point(R,math.tau*j/24,y),h.point(R,math.tau*(j+1)/24,y)]
            if sign<0:pts.reverse()
            m.triangle(pts,[(0,sign,0)]*3,[(0,0)]*3)
    return m

def create_mu(m):
    w=h.Writer(MODELS/(PART+'.mu'));w.i(76543,5);w.s(PART);h.node(w,PART)
    for index,(mat,mesh) in enumerate(m.items()):
        if not mesh.triangles:continue
        assert len(mesh.vertices)<65535
        w.i(0);h.node(w,'RW_AirGlass' if mat=='glass' else 'RW_Air'+mat.title())
        w.i(7);h.write_mesh(w,mesh);w.i(8);w.b(1);w.b(1);w.i(1,index);w.i(1)
    w.i(0);h.node(w,'RW_AIR250_EVA_Airlock',(0,HATCH_Y,1.43),collider=(.72,.78,.40),tag='Airlock',layer=21,trigger=True);w.i(1)
    w.i(0);h.node(w,'RW_AIR250_EVA_Ladder',(0,HATCH_Y,1.43),collider=(.86,1.64,.70),rot=(0,1,0,0),tag='Ladder',layer=21,trigger=True);w.i(1)
    w.i(0);h.node(w,'AirlockSolidHullCollider');w.i(25);w.b(0);w.b(1);h.write_mesh(w,collision());w.i(1)
    w.i(10,len(MAT))
    for index,mat in enumerate(MAT):
        w.s('RW_Air_'+mat);w.s('KSP/Emissive/Diffuse' if mat=='glass' else 'KSP/Diffuse');w.i(4 if mat=='glass' else 2)
        w.s('_Color');w.i(0);w.f(1,1,1,1);w.s('_MainTex');w.i(4,index);w.f(1,1);w.f(0,0)
        if mat=='glass':
            w.s('_EmissiveColor');w.i(0);w.f(0,0,0,1);w.s('_Emissive');w.i(4,len(MAT));w.f(1,1);w.f(0,0)
    w.i(12,len(MAT)+1)
    for mat in MAT:w.s('rwm_'+mat);w.i(0)
    w.s('rwm_cabin_emissive');w.i(0);w.close()

def build():
    from appearance_textures import label
    label('AIR-250','EVA / AIRLOCK').save(MODELS/'rwm_airlabel.png',optimize=True)
    m=geometry();create_mu(m)
    import build_cmd250 as obj
    previous=obj.MAT;obj.MAT=MAT
    obj.create_obj(m,ROOT/'Source/Blender/RW_AIR_250.obj');obj.MAT=previous
    print('Built RW-AIR-250:',sum(len(mesh.triangles) for mesh in m.values()),'render triangles')

if __name__=='__main__':build()
