#!/usr/bin/env python3
"""RW-CMD-250: distinct compact station command module generated in Python.

Produces an original 1.72 m tall, 2.5 m diameter native KSP .mu,
matching Blender OBJ source, procedural textures, and 5 recessed windows.
No custom IVA, docking port, or functional RCS is implied by exterior details.
"""
from pathlib import Path
from collections import OrderedDict
import math
from PIL import Image,ImageDraw,ImageFont
import build_hab250 as h

ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData'/'RoosterWorksStationModules'/'Models'
PART='RW_CMD_250'
HEIGHT=1.72
HALF=HEIGHT/2
TAU=h.TAU
MAT=OrderedDict(list(h.TEXTURES.items())+[('cmdlabel',(233,237,232)),('display',(42,70,86))])

def blank():return {name:h.Mesh() for name in MAT}

def segment(m,key,r,a,b,y0,y1,n=15):
    h.cylinder_surface(m[key],r,y0,y1,segments=n,theta0=a,theta1=b)

def panel(m,key,theta,y0,y1,width,r=1.215,n=20):
    h.flat_panel(m[key],theta,y0,y1,width,r,segments=n)

def annulus(m,key,inner,outer,y,sgn=1):
    h.annulus(m[key],inner,outer,y,normal_sign=sgn,segments=96)

def fastener(m,theta,y,r=1.227):
    h.radial_fastener(m['steel'],theta,y,radius=r,head=.010)

def label_texture():
    im=Image.new('RGB',(1024,512),(228,232,230));d=ImageDraw.Draw(im)
    d.rectangle((15,18,1007,492),outline=(184,118,58),width=14)
    d.rectangle((39,39,982,475),outline=(48,64,74),width=5)
    try:
        p='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
        b='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
        title=ImageFont.truetype(b,80);small=ImageFont.truetype(p,59)
    except OSError:
        title=small=ImageFont.load_default()
    d.text((75,104),'ROOSTERWORKS',fill=(34,54,65),font=title)
    d.line((77,239,937,239),fill=(179,120,64),width=9)
    d.text((78,309),'RW-CMD-250 / CONTROL',fill=(94,69,49),font=small)
    im.paste(h.rooster_crest_image(118),(856,106))
    return im

def display_texture():
    im=Image.new('RGB',(512,512),(33,54,68));d=ImageDraw.Draw(im)
    for y in range(8,512,25):
        d.line((0,y,511,y),fill=(48,80,89),width=2)
    for x in (23,490):d.line((x,12,x,500),fill=(91,108,113),width=4)
    return im

def make_textures():
    MODELS.mkdir(parents=True,exist_ok=True)
    if not (MODELS/'rwm_ceramic.png').exists():h.make_textures(MODELS)
    label_texture().save(MODELS/'rwm_cmdlabel.png',optimize=True)
    display_texture().save(MODELS/'rwm_display.png',optimize=True)

def endcap(m,sign):
    from station_endcaps import add_endcap
    add_endcap(m,sign,.860)


def command_window(m,theta,y=.187,hw=.173):
    # Local 4-layer bevel; truly conformed to 2.5m cylindrical surface.
    shell=h.square_window_shape(theta,y,hw+.080,hw+.080,radius=1.22,chamfer=.10)
    edge=h.square_window_shape(theta,y,hw+.063,hw+.063,radius=1.22,chamfer=.09)
    outer=h.square_window_shape(theta,y,hw+.040,hw+.040,radius=1.22,chamfer=.07)
    inner=h.square_window_shape(theta,y,hw+.016,hw+.016,radius=1.22,chamfer=.04)
    glass=h.square_window_shape(theta,y,hw,hw,radius=1.22,chamfer=.03)
    # No full-width flat backing polygon or wing-like standoff.
    h.window_frame_ring(m['ceramic'],shell,edge,1.219,1.228)
    h.window_frame_ring(m['white'],edge,outer,1.228,1.242)
    h.window_frame_ring(m['steel'],outer,inner,1.242,1.230)
    h.window_frame_ring(m['black'],inner,glass,1.230,1.215)
    h.window_glass(m['glass'],glass,1.217)
    for dy in (-.230,.230):fastener(m,theta,y+dy,r=1.240)

def geometry():
    m=blank()
    # Short command module silhouette: barrel with inset midsection and two
    # gentle 12 cm shoulders. All physical vertices fit the stack bounding box.
    h.cylinder_surface(m['graphite'],1.168,-.742,.742,segments=112)
    for j in range(14):
        t=TAU*(j+.5)/14;dw=TAU/14-.014
        for row in range(4):
            a=-.72+row*.36+.008;b=a+.344
            shade='cladding_white' if (j+row*2)%13==0 else 'cladding'
            panel(m,shade,t,a,b,dw,1.206,n=6)
            if row in (0,3) and j%2==0:fastener(m,t,a+.04)
    # Short reinforced pressure shell shoulders, slim and integrated.
    for sign in (-1,1):
        y0,y1=(.706,.859) if sign>0 else (-.859,-.706)
        h.cylinder_surface(m['white'],1.204,y0,y1,segments=96)
        for y,mat,rad,thick in ((.740,'graphite',1.213,.012),(.810,'steel',1.211,.012),(.811,'bronze',1.222,.0025)):
            mid=y*sign
            h.cylinder_surface(m[mat],rad,mid-thick,mid+thick,segments=96)
        endcap(m,sign)
    h.cylinder_surface(m['steel'],1.210,-.014,.014,segments=96)
    h.cylinder_surface(m['bronze'],1.217,-.003,.003,segments=96)
    # Command panoramic view: five windows around forward circumference.
    for theta in (-.90,-.45,0,.45,.90):
        command_window(m,theta,y=.171,hw=.143)
    # Side avionics box (visual surface detail, not solar/electrical equipment).
    for t in (-1.80,1.80):
        panel(m,'graphite',t,-.27,.41,.340,1.226,n=18)
        panel(m,'steel',t,-.23,.37,.298,1.232,n=18)
        panel(m,'display',t,-.19,.30,.250,1.238,n=18)
        for q in range(4):
            yy=-.14+.120*q
            panel(m,'graphite',t,yy-.009,yy+.009,.226,1.244,n=14)
        for y in (-.24,.38):
            for dt in (-.146,.146):fastener(m,t+dt,y,r=1.248)
    # Control bus dark panel with distinctive bronze label opposite windows.
    panel(m,'graphite',math.pi,-.430,.305,.832,1.223,n=38)
    panel(m,'bronze',math.pi,-.411,.287,.795,1.229,n=38)
    panel(m,'cmdlabel',math.pi,-.382,.260,.750,1.238,n=38)
    # Stand-alone crest on upper front structural deck.
    panel(m,'graphite',0,.576,.712,.225,1.218,n=16)
    panel(m,'bronze',0,.587,.700,.203,1.226,n=16)
    panel(m,'crest',0,.596,.694,.184,1.234,n=16)
    # Maintenance latches, single short rails, and small connection housings.
    for theta in (-2.38,2.38):
        h.tube(m['rail'],h.point(1.254,theta,-.48),h.point(1.254,theta,.51),r=.012,sides=8)
        for yy in (-.48,.51):
            h.tube(m['steel'],h.point(1.218,theta,yy),h.point(1.254,theta,yy),r=.018,sides=8)
    for theta in (-2.65,2.65):
        panel(m,'graphite',theta,-.55,-.38,.225,1.225,n=14)
        panel(m,'white',theta,-.52,-.408,.180,1.235,n=14)
    from exterior_detail import add_cmd
    add_cmd(m)
    from surface_uv import finish
    return finish(m)

def create_native_mu(meshes,dest):
    w=h.Writer(dest);w.i(76543,5);w.s(PART);h.node(w,PART)
    for mat_id,(mat,mesh) in enumerate(meshes.items()):
        if not mesh.triangles:continue
        assert len(mesh.vertices)<65535,(mat,len(mesh.vertices))
        name='RW_CmdGlass' if mat=='glass' else 'RW_Cmd'+mat.title().replace('_','')
        w.i(0);h.node(w,name)
        w.i(7);w.i(13,len(mesh.vertices),1);w.i(14)
        for p in mesh.vertices:w.xyz(p)
        w.i(15)
        for u,v in mesh.uvs:w.f(u,v)
        w.i(17)
        for n in mesh.normals:w.xyz(n)
        w.i(19,len(mesh.triangles)*3)
        for tri in mesh.triangles:w.i(*tri)
        w.i(22);w.i(8);w.b(1);w.b(1);w.i(1,mat_id);w.i(1)
    # Tangential cylindrical colliders, all centered inside 2.5m shell.
    for i in range(12):
        theta=TAU*(i+.5)/12;phi=math.pi/2-theta
        rot=(0,math.sin(phi/2),0,math.cos(phi/2))
        w.i(0);h.node(w,f'CmdRadialFace_{i:02}',h.point(1.154,theta,0),collider=(.59,1.49,.06),rot=rot);w.i(1)
    for sg,name in ((-1,'Bottom'),(1,'Top')):
        w.i(0);h.node(w,'CmdFlushEndcap'+name,(0,sg*.801,0),collider=(1.45,.10,1.45));w.i(1)
    w.i(10,len(MAT))
    for mat_id,mat in enumerate(MAT):
        w.s('RW_Cmd_'+mat);w.s('KSP/Emissive/Diffuse' if mat=='glass' else 'KSP/Diffuse')
        w.i(4 if mat=='glass' else 2)
        w.s('_Color');w.i(0);w.f(1,1,1,1)
        w.s('_MainTex');w.i(4,mat_id);w.f(1,1);w.f(0,0)
        if mat=='glass':
            w.s('_EmissiveColor');w.i(0);w.f(0,0,0,1)
            w.s('_Emissive');w.i(4,len(MAT));w.f(1,1);w.f(0,0)
    w.i(12,len(MAT)+1)
    for mat in MAT:w.s('rwm_'+mat);w.i(0)
    w.s('rwm_cabin_emissive');w.i(0)
    w.close()

def create_obj(meshes,dest):
    dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
    dest.with_suffix('.mtl').write_text(''.join(
        f'newmtl RW_Cmd_{mat}\nKa 0.3 0.3 0.3\nKd 1 1 1\nKs 0.2 0.2 0.2\nmap_Kd ../../GameData/RoosterWorksStationModules/Models/rwm_{mat}.png\n\n'
        for mat in MAT),encoding='utf-8')
    with dest.open('w') as out:
        out.write('# RW-CMD-250 original compact command pod\nmtllib '+dest.with_suffix('.mtl').name+'\n')
        offset=0
        for mat,mesh in meshes.items():
            out.write('o '+mat+'\nusemtl RW_Cmd_'+mat+'\n')
            for vert in mesh.vertices:out.write('v %.6f %.6f %.6f\n'%vert)
            for uv in mesh.uvs:out.write('vt %.6f %.6f\n'%uv)
            for normal in mesh.normals:out.write('vn %.6f %.6f %.6f\n'%normal)
            for face in mesh.triangles:
                out.write('f '+' '.join(f'{offset+i+1}/{offset+i+1}/{offset+i+1}' for i in face)+'\n')
            offset+=len(mesh.vertices)

def main():
    make_textures()
    meshes=geometry()
    create_native_mu(meshes,MODELS/(PART+'.mu'))
    create_obj(meshes,ROOT/'Source/Blender/RW_CMD_250.obj')
    print('RW-CMD-250 triangles:',sum(len(x.triangles) for x in meshes.values()),'vertices:',sum(len(x.vertices) for x in meshes.values()))

if __name__=='__main__':main()
