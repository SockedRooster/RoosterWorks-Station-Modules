"""RW-PWR-250 passive station battery/service core, native Unity metres.

2.5 m stack interfaces, 2.4 m long. Cabinets, cable trunks and cooling fins
are cosmetic. Stock ElectricCharge provides actual shared battery storage.
"""
from pathlib import Path
from collections import OrderedDict
import math
from PIL import Image,ImageDraw
import build_hab250 as h
from station_endcaps import add_endcap
from exterior_detail import plate,connector,conduit
from surface_uv import finish
ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
PART='RW_PWR_250';HALF=1.2;R=1.204;CAPACITY=12600
MAT=OrderedDict(h.TEXTURES) # Common endcap helper expects the complete palette.
MAT['pwrlabel']=(235,237,229);MAT['pwrpanel']=(42,57,65)

def textures():
    from appearance_textures import font,label
    im=label('PWR-250','POWER / SERVICE');d=ImageDraw.Draw(im)
    d.rectangle((47,47,976,86),fill=(48,64,70))
    d.text((65,49),'ELECTRICAL SYSTEMS   /   STATION BATTERY CORE',font=font(23,True),fill=(229,232,221))
    im.save(MODELS/'rwm_pwrlabel.png',optimize=True)
    im=Image.new('RGB',(512,1024),(39,53,61));d=ImageDraw.Draw(im)
    d.rounded_rectangle((10,10,501,1013),radius=18,outline=(115,126,128),width=8)
    d.text((35,34),'CELL BANK',font=font(47,True),fill=(228,233,222))
    d.text((37,104),'RW / ELECTRICAL',font=font(26),fill=(177,145,99))
    for row in range(6):
        y=174+row*124
        d.rounded_rectangle((28,y,482,y+97),radius=7,fill=(28,40,47),outline=(86,106,111),width=3)
        d.rectangle((49,y+20,79,y+76),fill=(175,128,71))
        d.text((100,y+11),f'BUS {row+1:02d}',font=font(26,True),fill=(202,215,208))
        d.text((100,y+51),'ISOLATED CELL ARRAY',font=font(18),fill=(136,157,159))
        for j in range(5):d.rectangle((387+j*13,y+22,392+j*13,y+69),fill=(82,112,116))
    d.text((38,954),'SERVICE WITH BUS ISOLATED',font=font(22,True),fill=(218,217,197))
    im.save(MODELS/'rwm_pwrpanel.png',optimize=True)

def geometry():
    m={name:h.Mesh() for name in MAT}
    h.cylinder_surface(m['graphite'],1.198,-HALF,HALF,segments=96)
    for col in range(16):
        for row in range(5):
            y0=-1.07+row*2.14/5+.01;y1=-1.07+(row+1)*2.14/5-.01
            h.cylinder_surface(m['cladding_white' if col%4==0 else 'cladding'],R,y0,y1,segments=6,
                               theta0=math.tau*col/16+.01,theta1=math.tau*(col+1)/16-.01)
    for sign in (-1,1):
        lo,hi=(1.035,HALF) if sign>0 else (-HALF,-1.035)
        h.cylinder_surface(m['white'],1.209,lo,hi,segments=96)
        for y,width,r,mat in ((1.051,.018,1.216,'steel'),(1.098,.006,1.223,'bronze')):
            h.cylinder_surface(m[mat],r,sign*y-width/2,sign*y+width/2,segments=96)
        add_endcap(m,sign,HALF)
    # Eight electrical cabinets, with chamfered borders and deeply layered cells.
    for bank in range(4):
        theta=math.tau*bank/4
        for cy in (-.57,.57):
            outer=h.curved_rect_contour(theta,cy,.325,.376,arc_steps=28,side_steps=12)
            inner=h.curved_rect_contour(theta,cy,.283,.332,arc_steps=28,side_steps=12)
            h.window_frame_ring(m['steel'],outer,inner,1.207,1.243)
            h.flat_panel(m['white'],theta,cy-.325,cy+.325,.557,1.247,32)
            h.flat_panel(m['pwrpanel'],theta,cy-.284,cy+.284,.403,1.251,28)
            for dt in (-.295,.295):
                for dy in (-.327,.327):h.radial_fastener(m['steel'],theta+dt,cy+dy,radius=1.244,head=.008)
            # Thin real cooling fins alongside the cell bank, not deployable radiators.
            for k in range(9):
                y=cy-.26+k*.52/8
                h.flat_panel(m['graphite'],theta+.245,y-.010,y+.010,.045,1.251,4)
                h.flat_panel(m['rail'],theta+.245,y+.003,y+.010,.045,1.258,4)
            h.tube(m['bronze'],h.point(1.258,theta-.244,cy-.09),h.point(1.258,theta-.244,cy+.09),r=.011,sides=8)
        # Four clear radial mounting areas on the narrow central structural belt.
        h.flat_panel(m['graphite'],theta,-.145,.145,.49,1.208,24)
        h.flat_panel(m['steel'],theta,-.122,.122,.44,1.214,24)
        for dy in (-.089,.089):
            for dt in (-.17,.17):h.radial_fastener(m['bronze'],theta+dt,dy,radius=1.218,head=.007)
    for bank in range(4):
        theta=math.tau*(bank+.5)/4
        # Protected cable trunks and bus connectors flank, rather than cover, IDs.
        for y0,y1 in ((-.99,-.25),(.25,.99)):conduit(m,theta,y0,y1,radius=1.230)
        for y in (-.81,.81):connector(m,theta+.16,y,radius=1.231)
        if bank%2==0:
            for mat,y0,y1,w,r in (('graphite',-.188,.188,.58,1.213),('bronze',-.173,.173,.54,1.222),('pwrlabel',-.153,.153,.50,1.235)):
                h.flat_panel(m[mat],theta,y0,y1,w,r,30)
        else:h.flat_panel(m['crest'],theta,-.125,.125,.21,1.227,16)
        plate(m,theta,.995,.16,.08,slot=6,radius=1.232)
    finish(m)
    m['pwrpanel'].uvs=[(1-u,v) for u,v in m['pwrpanel'].uvs]
    return m

def collision():
    mesh=h.Mesh();h.cylinder_surface(mesh,R,-HALF,HALF,segments=24)
    for sign in (-1,1):
        y=sign*HALF
        for j in range(24):
            pts=[(0,y,0),h.point(R,math.tau*j/24,y),h.point(R,math.tau*(j+1)/24,y)]
            if sign<0:pts.reverse()
            mesh.triangle(pts,[(0,sign,0)]*3,[(0,0)]*3)
    return mesh

def create_mu(m):
    w=h.Writer(MODELS/(PART+'.mu'));w.i(76543,5);w.s(PART);h.node(w,PART)
    for index,(mat,mesh) in enumerate(m.items()):
        if not mesh.triangles:continue
        assert len(mesh.vertices)<65535
        w.i(0);h.node(w,'RW_Power_'+mat);w.i(7);h.write_mesh(w,mesh)
        w.i(8);w.b(1);w.b(1);w.i(1,index);w.i(1)
    w.i(0);h.node(w,'PowerCoreHullCollider');w.i(25);w.b(0);w.b(1);h.write_mesh(w,collision());w.i(1)
    w.i(10,len(MAT))
    for index,mat in enumerate(MAT):
        w.s('RW_Power_'+mat);w.s('KSP/Diffuse');w.i(2)
        w.s('_Color');w.i(0);w.f(1,1,1,1);w.s('_MainTex');w.i(4,index);w.f(1,1);w.f(0,0)
    w.i(12,len(MAT))
    for mat in MAT:w.s('rwm_'+mat);w.i(0)
    w.close()

def build():
    textures();m=geometry();create_mu(m)
    import build_cmd250 as obj
    previous=obj.MAT;obj.MAT=MAT
    obj.create_obj(m,ROOT/'Source/Blender/RW_PWR_250.obj');obj.MAT=previous
    print('Built RW-PWR-250:',sum(len(mesh.triangles) for mesh in m.values()),'render triangles')

if __name__=='__main__':build()
