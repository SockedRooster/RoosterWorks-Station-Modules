"""Original RW-GRN-250 hydroponic greenhouse, 2.5 m interfaces / 3.6 m long.

Eight true transparent glazing bays, four crop tiers, no opaque pane backing.
Native Unity metres. Plants are static exterior-visible detail, not animated IVA.
"""
from pathlib import Path
from collections import OrderedDict
import math,random
from PIL import Image,ImageDraw
import build_hab250 as h
from station_endcaps import add_endcap
from exterior_detail import plate,connector,conduit,append
from surface_uv import finish
ROOT=Path(__file__).resolve().parents[1];MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
PART='RW_GRN_250';HALF=1.8;R=1.204
GLASS_Y=(-1.215,1.215);GLASS_EDGE=.062;FRAME_HALF=.075
TIERS=(-.99,-.40,.19,.78)
MAT=OrderedDict(h.TEXTURES)
MAT.update(grnlabel=(235,237,229),grnglass=(119,154,162),grnleaf=(68,124,47),grnleaflight=(119,162,68),grnroot=(65,53,37),grnlamp=(245,232,196),grninspection=(245,232,196))

def sector(mesh,inner,outer,y,a,b,sign=1,steps=16):
    for j in range(steps):
        ta=a+(b-a)*j/steps;tb=a+(b-a)*(j+1)/steps
        mesh.quad((h.point(inner,ta,y),h.point(outer,ta,y),h.point(outer,tb,y),h.point(inner,tb,y)),
                  [(0,sign,0)]*4,reverse=sign<0)

def inward(mesh,r,y0,y1,a,b,steps=12):
    q=h.Mesh();h.cylinder_surface(q,r,y0,y1,segments=steps,theta0=a,theta1=b)
    q.normals=[tuple(-v for v in n) for n in q.normals];q.triangles=[(a,c,b) for a,b,c in q.triangles]
    append(mesh,q)

def radial_wall(mesh,inner,outer,y0,y1,t,sign):
    n=(sign*math.cos(t),0,-sign*math.sin(t))
    mesh.quad((h.point(inner,t,y0),h.point(outer,t,y0),h.point(outer,t,y1),h.point(inner,t,y1)),[n]*4,reverse=sign>0)

def leaf(mesh,base,angle,length,width,height):
    # Closed faceted leaf with a raised vein. Both sides have real outward faces.
    d=(math.cos(angle),0,math.sin(angle));side=(-d[2],0,d[0])
    pts=[base,tuple(base[i]+d[i]*length*.47+side[i]*width/2+(height*.60 if i==1 else 0) for i in range(3)),
         tuple(base[i]+d[i]*length+(height if i==1 else 0) for i in range(3)),
         tuple(base[i]+d[i]*length*.47-side[i]*width/2+(height*.60 if i==1 else 0) for i in range(3))]
    ridge=tuple(base[i]+d[i]*length*.47+(height*.74+.010 if i==1 else 0) for i in range(3))
    low=tuple(base[i]+d[i]*length*.47+(height*.56-.004 if i==1 else 0) for i in range(3))
    def tri(p,q,r):
        a=tuple(q[i]-p[i] for i in range(3));b=tuple(r[i]-p[i] for i in range(3))
        n=(a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]);l=math.sqrt(sum(v*v for v in n));n=tuple(v/l for v in n)
        mesh.triangle((p,q,r),[n]*3,((0,0),(1,0),(.5,1)))
    for j in range(4):
        # Ensure upper triangles face +Y, lower triangles face -Y.
        p,q=pts[j],pts[(j+1)%4]
        tri(ridge,p,q);tri(low,q,p)

def geometry():
    m={name:h.Mesh() for name in MAT};rng=random.Random(250)
    # Pressure-wall collars and detailed equipment decks at both ends.
    for sign in (-1,1):
        lo,hi=(1.20,HALF) if sign>0 else (-HALF,-1.20)
        h.cylinder_surface(m['graphite'],1.197,lo,hi,segments=96)
        for col in range(16):
            a=math.tau*col/16+.008;b=math.tau*(col+1)/16-.008
            yl,yh=(1.26,1.69) if sign>0 else (-1.69,-1.26)
            h.cylinder_surface(m['cladding_white' if col%4==0 else 'cladding'],R,yl,yh,segments=6,theta0=a,theta1=b)
        for y,w,r,mat in ((1.215,.080,1.217,'graphite'),(1.247,.052,1.231,'ceramic'),(1.275,.014,1.241,'steel'),(1.303,.007,1.239,'bronze'),(1.7275,.145,1.209,'white'),(1.683,.016,1.218,'steel'),(1.745,.006,1.222,'bronze')):
            h.cylinder_surface(m[mat],r,sign*y-w/2,sign*y+w/2,segments=128)
        add_endcap(m,sign,HALF)
        # Inner end wall behind all foliage; stack endcap is closed pressure hardware.
        for j in range(96):
            pts=[(0,sign*1.27,0),h.point(1.197,math.tau*j/96,sign*1.27),h.point(1.197,math.tau*(j+1)/96,sign*1.27)]
            if sign>0:pts.reverse()
            m['white'].triangle(pts,[(0,-sign,0)]*3,[(.5,.5),(0,0),(1,0)])
        for t in (math.pi/2,3*math.pi/2):
            plate(m,t,sign*1.49,.33,.24,slot=1,radius=1.235)
            connector(m,t+.26,sign*1.49)
        for t in (0,math.pi):
            for mat,w,rad,dy in (('graphite',.67,1.218,.172),('bronze',.63,1.227,.158),('grnlabel',.58,1.238,.143)):
                h.flat_panel(m[mat],t,sign*1.49-dy,sign*1.49+dy,w,rad,28)
    # Pane endpoints overlap full headers, frame foundations overlap glass edges.
    for bay in range(8):
        a=math.tau*bay/8;b=math.tau*(bay+1)/8
        h.cylinder_surface(m['grnglass'],1.198,*GLASS_Y,segments=16,theta0=a+GLASS_EDGE,theta1=b-GLASS_EDGE)
        inward(m['grnglass'],1.197,*GLASS_Y,a+GLASS_EDGE,b-GLASS_EDGE,16)
        h.cylinder_surface(m['graphite'],1.203,-1.263,1.263,segments=8,theta0=a-FRAME_HALF,theta1=a+FRAME_HALF)
        h.cylinder_surface(m['ceramic'],1.219,-1.262,1.262,segments=6,theta0=a-.044,theta1=a+.044)
        h.cylinder_surface(m['steel'],1.228,-1.258,1.258,segments=2,theta0=a-.012,theta1=a+.012)
        # Separate inspection-light strips, controlled by stock ModuleLight.
        # Kerbalism still owns the horticultural strips and crop lamp EC draw.
        for dt in (-.032,.032):
            h.cylinder_surface(m['grninspection'],1.190,-1.17,1.17,segments=2,theta0=a+dt-.004,theta1=a+dt+.004)
        for dt in (-.047,.047):
            h.cylinder_surface(m['bronze'],1.229,-1.251,1.251,segments=2,theta0=a+dt-.004,theta1=a+dt+.004)
        for y in (-1.18,-.59,0,.59,1.18):h.radial_fastener(m['steel'],a,y,radius=1.231,head=.010)
        # Interior rack spine and supply riser, kept inside the glass.
        h.tube(m['steel'],h.point(.61,a,-1.19),h.point(.61,a,1.19),r=.025,sides=8)
        h.tube(m['bronze'],h.point(1.12,a,-1.19),h.point(1.12,a,1.19),r=.013,sides=8)
        for tier,y in enumerate(TIERS):
            ta=a+.10;tb=b-.10
            sector(m['steel'],.55,1.105,y-.07,ta,tb,1)
            sector(m['graphite'],.55,1.105,y-.105,ta,tb,-1)
            h.cylinder_surface(m['steel'],1.105,y-.105,y-.07,segments=14,theta0=ta,theta1=tb)
            inward(m['steel'],.55,y-.105,y-.07,ta,tb,14)
            radial_wall(m['steel'],.55,1.105,y-.105,y-.07,ta,-1)
            radial_wall(m['steel'],.55,1.105,y-.105,y-.07,tb,1)
            sector(m['grnroot'],.59,1.06,y-.065,ta+.02,tb-.02,1)
            # Slim warm-white lamp under each next rack / top header.
            ly=y+.32
            h.cylinder_surface(m['black'],1.086,ly-.014,ly+.014,segments=12,theta0=ta,theta1=tb)
            h.cylinder_surface(m['grnlamp'],1.091,ly-.006,ly+.006,segments=12,theta0=ta+.02,theta1=tb-.02)
            for row,rad in enumerate((.73,.93)):
                for pos in range(3):
                    theta=ta+(tb-ta)*(pos+.5)/3
                    base=h.point(rad,theta,y-.040)
                    h.tube(m['grnleaf'],base,(base[0],base[1]+.055,base[2]),r=.008,sides=5)
                    for j in range(7):
                        angle=math.tau*j/7+rng.uniform(-.12,.12)
                        leaf(m['grnleaflight' if (j+pos+tier)%3==0 else 'grnleaf'],(base[0],base[1]+.025,base[2]),angle,rng.uniform(.075,.135),rng.uniform(.042,.072),rng.uniform(.035,.115))
    # Continuous central brace ring, not an opaque barrel behind panes.
    for mat,r,w in (('graphite',1.208,.047),('steel',1.229,.018),('bronze',1.233,.004)):
        h.cylinder_surface(m[mat],r,-w/2,w/2,segments=128)
    for t in (math.pi/4,5*math.pi/4):
        h.flat_panel(m['graphite'],t,-.125,.125,.23,1.231,16)
        h.flat_panel(m['crest'],t,-.112,.112,.20,1.239,16)
    return finish(m)

def collision():
    from build_adp250375 import collision_section
    return collision_section(-HALF,HALF,R,R)

def create_mu(m):
    w=h.Writer(MODELS/(PART+'.mu'));w.i(76543,5);w.s(PART);h.node(w,PART)
    for index,(mat,mesh) in enumerate(m.items()):
        if not mesh.triangles:continue
        assert len(mesh.vertices)<65535
        w.i(0);h.node(w,'RW_GreenhouseLamps' if mat=='grnlamp' else 'RW_GreenhouseInspectionLamps' if mat=='grninspection' else 'RW_Greenhouse_'+mat)
        w.i(7);h.write_mesh(w,mesh);w.i(8);w.b(1);w.b(1);w.i(1,index);w.i(1)
    w.i(0);h.node(w,'GreenhouseSolidHullCollider');w.i(25);w.b(0);w.b(1);h.write_mesh(w,collision());w.i(1)
    # Native MU point Light record: type, intensity, range, RGBA, mask, angle.
    for y in TIERS:
        w.i(0);h.node(w,'RW_GreenhouseInspectionLight',(0,y+.25,0))
        w.i(23,2);w.f(1.4,2.2,1,.91,.76,1);w.i(-1);w.f(0);w.i(1)
    w.i(10,len(MAT))
    for index,mat in enumerate(MAT):
        emissive=mat in ('grnlamp','grninspection')
        shader='KSP/Alpha/Translucent' if mat=='grnglass' else 'KSP/Emissive/Diffuse' if emissive else 'KSP/Diffuse'
        w.s('RW_Greenhouse_'+mat);w.s(shader);w.i(4 if emissive else 2)
        w.s('_Color');w.i(0);w.f(1,1,1,1);w.s('_MainTex');w.i(4,index);w.f(1,1);w.f(0,0)
        if emissive:
            w.s('_EmissiveColor');w.i(0);w.f(0,0,0,1);w.s('_Emissive');w.i(4,index);w.f(1,1);w.f(0,0)
    w.i(12,len(MAT))
    for mat in MAT:w.s('rwm_'+mat);w.i(0)
    w.close()

def textures():
    from appearance_textures import label
    label('GRN-250','GREENHOUSE / HYDROPONICS').save(MODELS/'rwm_grnlabel.png',optimize=True)
    for mat in ('grnleaf','grnleaflight','grnroot','grnlamp','grninspection'):
        im=Image.new('RGB',(256,256),MAT[mat]);d=ImageDraw.Draw(im)
        if 'leaf' in mat:
            for j in range(9):
                y=16+j*28;d.line((0,y,128,y+14,256,y),fill=tuple(min(255,v+12) for v in MAT[mat]),width=2)
            d.line((128,0,128,256),fill=tuple(min(255,v+23) for v in MAT[mat]),width=4)
        elif mat=='grnroot':
            rng=random.Random(251)
            for j in range(1000):
                x=rng.randrange(256);y=rng.randrange(256);c=rng.randrange(40,80)
                d.ellipse((x,y,x+2,y+2),fill=(c,int(c*.81),int(c*.55)))
        im.save(MODELS/('rwm_'+mat+'.png'),optimize=True)
    # Uniform low-opacity glass avoids fake crop imagery / opaque artwork.
    Image.new('RGBA',(256,256),(126,163,173,36)).save(MODELS/'rwm_grnglass.png',optimize=True)

def build():
    textures();m=geometry();create_mu(m)
    import build_cmd250 as obj
    previous=obj.MAT;obj.MAT=MAT;obj.create_obj(m,ROOT/'Source/Blender/RW_GRN_250.obj');obj.MAT=previous
    mtl=ROOT/'Source/Blender/RW_GRN_250.mtl'
    mtl.write_text(mtl.read_text().replace('newmtl RW_Cmd_grnglass\n','newmtl RW_Cmd_grnglass\nd 0.14117647\n'),encoding='utf-8')
    print('Built RW-GRN-250:',sum(len(q.triangles) for q in m.values()),'visual triangles')

if __name__=='__main__':build()
