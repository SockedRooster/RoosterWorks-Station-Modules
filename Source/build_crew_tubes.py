"""Native 2.5/3.75 m pressurized straight passages and true 90-degree elbows.

Existing layered caps, readable UVs and four optional-grey shell materials.
Quarter-circle bend with straight tangent collars; independent convex solids.
"""
from pathlib import Path
from collections import OrderedDict
import math
import build_hab250 as h
from station_endcaps import add_endcap
from surface_uv import finish
from exterior_detail import plate,connector,conduit
from config_nodes import Node,dump
ROOT=Path(__file__).resolve().parents[1];GD=ROOT/'GameData/RoosterWorksStationModules';MODELS=GD/'Models'
MAT=OrderedDict(h.TEXTURES);MAT['tublabel']=(235,237,229);MAT['elblabel']=(235,237,229)
BEND=1.8;COLLAR=.3;ARCLENGTH=BEND*math.pi/2

def frame(y,elbow):
    if not elbow:return (0,y,0),(1,0,0),(0,1,0),0
    s=y+ARCLENGTH/2
    if s<0:return (-BEND/2,-BEND/2+s,0),(1,0,0),(0,1,0),0
    if s>ARCLENGTH:return (BEND/2+s-ARCLENGTH,BEND/2,0),(0,-1,0),(1,0,0),0
    a=s/BEND
    return (BEND*(1-math.cos(a))-BEND/2,BEND*math.sin(a)-BEND/2,0),(math.cos(a),-math.sin(a),0),(math.sin(a),math.cos(a),0),1/BEND

def mapped(mesh,elbow,scale):
    out=h.Mesh()
    for (x,y,z),(nx,ny,nz) in zip(mesh.vertices,mesh.normals):
        c,n,t,k=frame(y,elbow)
        out.vertices.append(tuple(scale*(c[i]+x*n[i]+(z if i==2 else 0)) for i in range(3)))
        v=tuple(nx*n[i]+ny*t[i]/(1-x*k)+(nz if i==2 else 0) for i in range(3));length=math.sqrt(sum(a*a for a in v))
        out.normals.append(tuple(a/length for a in v))
    out.uvs=list(mesh.uvs);out.triangles=list(mesh.triangles)
    return out

def geometry(elbow=False,scale=1):
    half=ARCLENGTH/2+COLLAR if elbow else 1.0
    m={name:h.Mesh() for name in MAT}
    rows=10 if elbow else 4
    # Sufficient axial sampling follows the bend rather than faceting into boxes.
    def panel(material,theta,y0,y1,width,r,around=8,along=1):
        for j in range(along):
            first=len(m[material].uvs)
            h.cylinder_surface(m[material],r,y0+(y1-y0)*j/along,y0+(y1-y0)*(j+1)/along,segments=around,theta0=theta-width/2,theta1=theta+width/2)
            # Curvature subdivisions are geometry only: cover the artwork once
            # over the whole panel, not once per strip. Keep U unchanged so the
            # established outward-readable finish() correction still applies.
            m[material].uvs[first:]=[(u,(j+v)/along) for u,v in m[material].uvs[first:]]
    panel('graphite',math.pi,-half,half,math.tau,1.198,96,64 if elbow else 1)
    for col in range(16):
        for row in range(rows):
            low=-half+.17+row*(2*half-.34)/rows+.006;high=-half+.17+(row+1)*(2*half-.34)/rows-.006
            panel('cladding_white' if col%4==0 else 'cladding',math.tau*(col+.5)/16,low,high,math.tau/16-.014,1.204,6,4 if elbow else 1)
    for sign in (-1,1):
        low,high=(half-.17,half) if sign>0 else (-half,-half+.17)
        h.cylinder_surface(m['white'],1.209,low,high,96)
        for offset,width,r,material in ((.14,.02,1.218,'steel'),(.095,.007,1.224,'bronze')):
            h.cylinder_surface(m[material],r,sign*(half-offset)-width/2,sign*(half-offset)+width/2,96)
        add_endcap(m,sign,half)
    for seam in (-.45,.45) if not elbow else (-1.0,0,1.0):
        panel('steel',math.pi,seam-.012,seam+.012,math.tau,1.218,96,1)
        panel('bronze',math.pi,seam+.015,seam+.021,math.tau,1.223,96,1)
    for theta in (0,math.pi):
        name='elblabel' if elbow else 'tublabel'
        for mat,lo,hi,width,r in (('graphite',-.21,.21,.53,1.214),('bronze',-.195,.195,.5,1.222),(name,-.177,.177,.465,1.230)):
            panel(mat,theta,lo,hi,width,r,28,6 if elbow else 1)
        for y in (-half+.39,half-.39):connector(m,theta+.40,y,1.234)
    for theta in (math.pi/2,3*math.pi/2):
        panel('crest',theta,-.13,.13,.22,1.229,18,6 if elbow else 1)
        for y in (-half+.27,half-.27):plate(m,theta,y,.18,.10,slot=6,radius=1.231)
    # Rails/cable guards broken into short segments before bending, preventing
    # straight chords from clipping into the body or floating over curved panels.
    for theta in (math.pi/4,3*math.pi/4,5*math.pi/4,7*math.pi/4):
        for j in range(28 if elbow else 8):
            low=-half+.26+(2*half-.52)*j/(28 if elbow else 8)
            high=-half+.26+(2*half-.52)*(j+1)/(28 if elbow else 8)
            h.tube(m['rail'],h.point(1.237,theta,low),h.point(1.237,theta,high),.010,8)
    finish(m)
    return {key:mapped(mesh,elbow,scale) for key,mesh in m.items()}

def cylinder(radius,half):
    m=h.Mesh();h.cylinder_surface(m,radius,-half,half,24)
    for sign in (-1,1):
        for j in range(24):
            pts=[(0,sign*half,0),h.point(radius,math.tau*j/24,sign*half),h.point(radius,math.tau*(j+1)/24,sign*half)]
            if sign<0:pts.reverse()
            m.triangle(pts,[(0,sign,0)]*3,[(0,0)]*3)
    return m

def collisions(elbow,scale):
    if not elbow:return [mapped(cylinder(1.198,1),False,scale)]
    # Ten short closed convex chord solids plus two tangent collar solids.
    samples=[-ARCLENGTH/2-COLLAR,-ARCLENGTH/2]+[-ARCLENGTH/2+ARCLENGTH*j/10 for j in range(1,11)]+[ARCLENGTH/2+COLLAR]
    out=[]
    for j,(a,b) in enumerate(zip(samples,samples[1:])):
        p,_,_,_=frame(a,True);q,_,_,_=frame(b,True)
        v=tuple(q[i]-p[i] for i in range(3));length=math.sqrt(sum(x*x for x in v));t=tuple(x/length for x in v);n=(t[1],-t[0],0)
        low=-length/2-(.045 if j>0 else 0);high=length/2+(.045 if j<len(samples)-2 else 0)
        local=cylinder(1.194,(high-low)/2);mid=tuple((p[i]+q[i])/2+t[i]*(high+low)/2 for i in range(3))
        for k,((x,y,z),(nx,ny,nz)) in enumerate(zip(local.vertices,local.normals)):
            local.vertices[k]=tuple(scale*(mid[i]+x*n[i]+y*t[i]+(z if i==2 else 0)) for i in range(3))
            local.normals[k]=tuple(nx*n[i]+ny*t[i]+(nz if i==2 else 0) for i in range(3))
        out.append(local)
    return out

def native(part,meshes,solids,size):
    # KSPCF's fast MU loader sizes renderer bindings to the highest used
    # material index. A trailing unused material makes its table read fail.
    materials=list(MAT)
    while materials and not meshes[materials[-1]].triangles:materials.pop()
    w=h.Writer(MODELS/(part+'.mu'));w.i(76543,5);w.s(part);h.node(w,part)
    for index,(name,m) in enumerate(meshes.items()):
        if not m.triangles:continue
        assert len(m.vertices)<65535
        w.i(0);h.node(w,'RW_Passage_'+name);w.i(7);h.write_mesh(w,m);w.i(8);w.b(1);w.b(1);w.i(1,index);w.i(1)
    for j,m in enumerate(solids):
        w.i(0);h.node(w,'PassageHullCollider_'+str(j));w.i(25);w.b(0);w.b(1);h.write_mesh(w,m);w.i(1)
    w.i(10,len(materials))
    for index,name in enumerate(materials):
        w.s('RW_Passage_'+name);w.s('KSP/Diffuse');w.i(2);w.s('_Color');w.i(0);w.f(1,1,1,1);w.s('_MainTex');w.i(4,index);w.f(1,1);w.f(0,0)
    w.i(12,len(materials))
    for name in materials:w.s('rwm_'+name+('_375' if size==375 and name in ('tublabel','elblabel') else ''));w.i(0)
    w.close()

def build():
    from appearance_textures import label
    from build_cmd250 import create_obj
    import build_cmd250 as obj
    patches=Node('ROOT')
    for elbow,kind in ((False,'TUB'),(True,'ELB')):
        label(kind+'-250','PRESSURIZED PASSAGE' if not elbow else '90 DEGREE / CREW PASSAGE').save(MODELS/('rwm_'+('elblabel' if elbow else 'tublabel')+'.png'))
        label(kind+'-375','PRESSURIZED PASSAGE' if not elbow else '90 DEGREE / CREW PASSAGE').save(MODELS/('rwm_'+('elblabel' if elbow else 'tublabel')+'_375.png'))
        for size,scale in ((250,1),(375,1.5)):
            part=f'RW_{kind}_{size}';m=geometry(elbow,scale);solid=collisions(elbow,scale);native(part,m,solid,size)
            prev=obj.MAT;obj.MAT=MAT;create_obj(m,ROOT/f'Source/Blender/{part}.obj');obj.MAT=prev
            if size==375:
                mtl=ROOT/f'Source/Blender/{part}.mtl'
                mtl.write_text(mtl.read_text().replace('rwm_tublabel.png','rwm_tublabel_375.png').replace('rwm_elblabel.png','rwm_elblabel_375.png'))
            half=ARCLENGTH/2+COLLAR if elbow else 1.0
            p,_,t,_=frame(half,elbow);bottom,_,bt,_=frame(-half,elbow)
            num=lambda x:format(x,'.9g')
            node=lambda pos,d: ', '.join([num(v*scale) for v in pos]+[num(v) for v in d]+[str(2 if size==250 else 3)])
            values=[('name',part),('module','Part'),('author','SockedRooster'),('rescaleFactor','1'),('node_stack_top',node(p,t)),('node_stack_bottom',node(bottom,tuple(-v for v in bt))),('attachRules','1,0,1,1,0'),('bulkheadProfiles','size2' if size==250 else 'size3'),('TechRequired','advConstruction'),('entryCost',str(round((6600 if elbow else 3900)*scale**3))),('cost',str(round((4400 if elbow else 2600)*scale**3))),('category','Structural'),('subcategory','0'),('title',f'RoosterWorks RW-{kind}-{size} '+('90 Degree Crew Tube Elbow' if elbow else 'Straight Crew Tube')),('manufacturer','RoosterWorks'),('description',f'{size/100:g} m pressurized crew passage. '+('Smooth 90-degree bend with tangent collars and two perpendicular stack interfaces.' if elbow else f'{2*scale:g} m straight tube with two aligned stack interfaces.')+' Crewless: no seats, IVA, EVA or supplies. Kerbalism pressure volume and optional Connected Living Space passability. Existing readable insignia, sealed interface rings, metal trim and selectable white/grey exterior.'),('tags','roosterworks station tube tunnel passage crew pressure '+('elbow bend 90' if elbow else 'straight')),('mass',num((.85 if elbow else .55)*scale**3)),('vesselType','Station'),('CrewCapacity','0'),('dragModelType','default'),('maximum_drag','.2'),('minimum_drag','.2'),('angularDrag','2'),('crashTolerance','13'),('breakingForce',num(220*scale**2)),('breakingTorque',num(220*scale**2)),('maxTemp','2000'),('skinMaxTemp','2400'),('fuelCrossFeed','True')]
            tree=Node('ROOT',children=[Node('PART',values,[Node('MODEL',[('model',f'RoosterWorksStationModules/Models/{part}')])])]);(GD/f'Parts/{part}.cfg').write_text(dump(tree))
            length=(ARCLENGTH+2*COLLAR if elbow else 2)*scale;inner=.92*scale
            patches.children.append(Node(f'@PART[{part}]:NEEDS[Kerbalism,FeatureHabitat]:AFTER[zzzKerbalismDefault]',children=[Node('%MODULE[Habitat]',[('%name','Habitat'),('%volume',num(math.pi*inner**2*length)),('%surface',num(2*math.pi*inner*length+2*math.pi*inner**2))])]))
            patches.children.append(Node(f'@PART[{part}]:HAS[!MODULE[ModuleConnectedLivingSpace]]:NEEDS[ConnectedLivingSpace]',children=[Node('MODULE',[('name','ModuleConnectedLivingSpace'),('passable','true')])]))
            print('Built',part,sum(len(x.triangles) for x in m.values()),'visual triangles;',len(solid),'convex colliders',flush=True)
    (GD/'Compatibility/CrewTubes.cfg').write_text(dump(patches))

if __name__=='__main__':build()
