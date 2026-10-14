#!/usr/bin/env python3
"""RW-LAB-250 v0.3.0: original procedural science laboratory exterior.

Reuses Station Modules' tested shared primitives and materials from
build_hab250.py, without reusing its window-bank assemblies.  All lab window
frames are angularly subdivided directly on a cylinder; their curved faces
do not have wide-chord backing plates like the early HAB prototypes.
"""
from __future__ import annotations
from pathlib import Path
from collections import OrderedDict
import math, struct
from PIL import Image,ImageDraw,ImageFont
import build_hab250 as hb

ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData'/'RoosterWorksStationModules'/'Models'
PART='RW_LAB_250'
TAU=hb.TAU
MAT=OrderedDict(list(hb.TEXTURES.items())+[('lablabel',(235,237,230)),('instrument',(43,74,82))])

def blank():return {x:hb.Mesh() for x in MAT}

def cyl(mesh,r,y0,y1,steps=96,a0=0,a1=TAU):
    hb.cylinder_surface(mesh,r,y0,y1,segments=steps,theta0=a0,theta1=a1)

def panel(mesh,t,y0,y1,ang=.36,r=1.220,steps=16):
    hb.flat_panel(mesh,t,y0,y1,ang,r,segments=steps)

def stud(mesh,t,y,r=1.233,s=.010):
    hb.radial_fastener(mesh,t,y,radius=r,head=s)

def rail(mesh,theta,lo,hi):
    hb.tube(mesh,hb.point(1.266,theta,lo),hb.point(1.266,theta,hi),r=.013,sides=8)
    for yy in (lo,hi):
        hb.tube(mesh,hb.point(1.217,theta,yy),hb.point(1.266,theta,yy),r=.019,sides=8)

def lab_windows(m):
    """Three compact independent observation viewports; no HAB-wide backing."""
    center=0.0; y=.63
    # Curved ceramic local reinforcement, overlapping shield panels directly.
    panel(m['graphite'],center,y-.232,y+.230,1.06,1.209,steps=52)
    panel(m['ceramic'],center,y-.221,y+.222,1.02,1.214,steps=52)
    for dt in (-.326,0.0,.326):
        t=center+dt
        plate=hb.square_window_shape(t,y,.149,.149)
        white=hb.square_window_shape(t,y,.135,.135)
        steel=hb.square_window_shape(t,y,.113,.113)
        seal=hb.square_window_shape(t,y,.101,.101)
        glass=hb.square_window_shape(t,y,.088,.088)
        # All rings densely tessellated, not wide flat chords.
        hb.window_frame_ring(m['white'],plate,white,1.235,1.230)
        hb.window_frame_ring(m['steel'],white,steel,1.230,1.224)
        hb.window_frame_ring(m['graphite'],steel,seal,1.224,1.218)
        hb.window_frame_ring(m['black'],seal,glass,1.218,1.216)
        hb.window_glass(m['glass'],glass,1.220)
        for dy in (-.168,.168):stud(m['steel'],t, y+dy,r=1.241,s=.009)

def shield_rib(m,theta,center_y,length=.7):
    panel(m['graphite'],theta,center_y-length/2,center_y+length/2,.030,1.218,steps=3)
    panel(m['steel'],theta,center_y-length/2+.032,center_y+length/2-.032,.012,1.227,steps=3)

def sensor_bay(m,t,y,designation='Spectrometer'):
    """Distinctive high-tech instrument cassette: graphite bay, layered hatches,
    condenser/cooling ribs, and a recessed spectrometry target aperture."""
    panel(m['graphite'],t,y-.40,y+.40,.59,1.219,steps=30)
    panel(m['steel'],t,y-.36,y+.36,.53,1.229,steps=30)
    panel(m['white'],t,y-.335,y+.335,.484,1.237,steps=30)
    panel(m['instrument'],t,y-.29,y+.285,.426,1.245,steps=30)
    # Conformal instrument fins; like actual vacuum lab sensor hardware.
    for h in range(7):
        yy=y-.245+h*.079
        panel(m['graphite'],t,yy-.012,yy+.012,.396,1.255,steps=27)
        panel(m['rail'],t,yy+.009,yy+.013,.396,1.258,steps=27)
    for s in (-1,1):
        theta=t+s*.286
        hb.tube(m['steel'],hb.point(1.240,theta,y-.28),hb.point(1.240,theta,y+.28),r=.017,sides=8)
    for dy in (-.348,.348):
        for da in (-.235,.235):stud(m['bronze'],t+da,y+dy,r=1.244,s=.011)

def optical_scanner(m,t,y):
    """Circular sensor pod embedded in hull with original annular baffles."""
    def circle(width,steps=48):
        return [(t+width/1.22*math.sin(TAU*k/steps),y+width*math.cos(TAU*k/steps)) for k in range(steps)]
    outer=circle(.275);rim=circle(.248);inner=circle(.218);aperture=circle(.184)
    hb.window_frame_ring(m['ceramic'],outer,rim,1.220,1.241)
    hb.window_frame_ring(m['steel'],rim,inner,1.241,1.248)
    hb.window_frame_ring(m['bronze'],inner,aperture,1.248,1.252)
    hb.window_glass(m['instrument'],aperture,1.251)
    for j in range(8):
        a=TAU*j/8
        stud(m['steel'],t+.280/1.22*math.sin(a),y+.280*math.cos(a),r=1.252,s=.010)

def science_label_image():
    im=Image.new('RGB',(1024,512),(224,229,225));d=ImageDraw.Draw(im)
    d.rectangle((12,14,1011,497),outline=(163,109,50),width=17)
    d.rectangle((36,38,984,473),outline=(37,54,69),width=5)
    try:
        bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',78)
        small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',56)
    except OSError:
        bold=small=ImageFont.load_default()
    d.text((78,101),'ROOSTERWORKS',fill=(28,48,57),font=bold)
    d.line((82,235,936,235),fill=(180,118,57),width=8)
    d.text((81,302),'RW-LAB-250 / RESEARCH',fill=(92,66,47),font=small)
    im.paste(hb.rooster_crest_image(120),(866,102))
    return im

def instrument_texture():
    im=Image.new('RGB',(512,512),(35,60,70));d=ImageDraw.Draw(im)
    for v in range(0,512,19):
        d.line((0,v,511,v),fill=(49+(v%3),78,86),width=3)
    for v in (9,502):d.line((v,0,v,511),fill=(111,127,128),width=3)
    return im

def make_textures():
    MODELS.mkdir(parents=True,exist_ok=True)
    if not (MODELS/'rwm_ceramic.png').exists():hb.make_textures(MODELS)
    science_label_image().save(MODELS/'rwm_lablabel.png',optimize=True)
    instrument_texture().save(MODELS/'rwm_instrument.png',optimize=True)

def geometry():
    m=blank()
    # Thin graphite pressure hull + 14 longitudinal ceramic segments.
    cyl(m['graphite'],1.183,-1.82,1.82)
    cols=14; rows=8
    for row in range(rows):
        y0=-1.73+3.46*row/rows+.010
        y1=-1.73+3.46*(row+1)/rows-.010
        for col in range(cols):
            tc=TAU*(col+.5)/cols
            width=TAU/cols-.019
            mat='cladding_white' if (row*3+col)%15==0 else 'cladding'
            panel(m[mat],tc,y0,y1,width,1.205,steps=5)
            if (row in (0,3,7)) and col%2==0:
                stud(m['steel'],tc+width*.35,y0+.037,r=1.223,s=.009)
    # Structural ribs and broad service zone below viewport row.
    for t in (TAU*.12,TAU*.38,TAU*.62,TAU*.88):
        shield_rib(m,t,0,2.80)
    lab_windows(m)
    # Unique research silhouette: asymmetric two instrument bays and scanners.
    sensor_bay(m,TAU*.25,-.21)
    sensor_bay(m,TAU*.75,-.21)
    optical_scanner(m,TAU*.50,.82)
    # Thin gold metallic pressure spine / condenser connection details.
    for theta in (TAU*.20, TAU*.30,TAU*.70, TAU*.80):
        rail(m['rail'],theta,-1.25,.97)
    # Dual passive radiator cassettes, flush to the cylinder, no big fins.
    for theta in (TAU*.39,TAU*.61):
        panel(m['graphite'],theta,-.98,-.45,.24,1.224,steps=12)
        panel(m['white'],theta,-.94,-.49,.20,1.231,steps=12)
        for j in range(6):
            y=-.90+.07*j
            panel(m['steel'],theta,y-.012,y+.012,.18,1.240,steps=12)
    # Narrow integrated axial end banding, matching the HAB support style.
    cyl(m['steel'],1.215,-.014,.014)
    cyl(m['bronze'],1.221,-.0025,.0025)
    for sign in (-1,1):
        y0,y1=(1.73,1.98) if sign>0 else (-1.98,-1.73)
        cyl(m['ceramic'],1.200,y0,y1)
        for center,half,mat,radius in ((1.815,.010,'graphite',1.217),
                                       (1.948,.012,'steel',1.214),
                                       (1.948,.003,'bronze',1.221)):
            lo,hi=(center-half,center+half) if sign>0 else (-center-half,-center+half)
            cyl(m[mat],radius,lo,hi)
        hb.recessed_bulkhead(m,sign)
    # Original emblem + scientific shield plaque, no 3D text handedness issues.
    panel(m['graphite'],0,1.18,1.55,.31,1.222,steps=14)
    panel(m['bronze'],0,1.195,1.54,.285,1.233,steps=14)
    panel(m['crest'],0,1.209,1.526,.266,1.240,steps=14)
    panel(m['graphite'],0,-1.19,-.77,.90,1.224,steps=24)
    panel(m['bronze'],0,-1.17,-.79,.86,1.229,steps=24)
    panel(m['lablabel'],0,-1.145,-.815,.82,1.237,steps=24)
    for t in (-.405,.405):
        for yy in (-1.115,-.835):stud(m['steel'],t,yy,r=1.246,s=.013)
    from exterior_detail import add_lab
    add_lab(m)
    from surface_uv import finish
    return finish(m)

def create_native_mu(m,path):
    w=hb.Writer(path);w.i(76543,5);w.s(PART);hb.node(w,PART)
    for mat_id,(mat,mesh) in enumerate(m.items()):
        if not mesh.triangles:continue
        assert len(mesh.vertices)<65535,(mat,len(mesh.vertices))
        name='RW_LabGlass' if mat=='glass' else 'RW_Lab'+mat.title()
        w.i(0);hb.node(w,name)
        w.i(7);w.i(13,len(mesh.vertices),1);w.i(14)
        for xyz in mesh.vertices:w.xyz(xyz)
        w.i(15)
        for u,v in mesh.uvs:w.f(u,v)
        w.i(17)
        for norm in mesh.normals:w.xyz(norm)
        w.i(19,len(mesh.triangles)*3)
        for tri in mesh.triangles:w.i(*tri)
        w.i(22);w.i(8);w.b(1);w.b(1);w.i(1,mat_id)
        w.i(1)
    # Solid body colliders; no editable/painted per-window hit boxes.
    for i in range(12):
        t=TAU*(i+.5)/12
        phi=math.pi/2-t
        q=(0,math.sin(phi/2),0,math.cos(phi/2))
        w.i(0);hb.node(w,f'LabRadialFace_{i:02}',hb.point(1.154,t,0),collider=(.59,3.52,.08),rot=q);w.i(1)
    for sign,label in ((-1,'Bottom'),(1,'Top')):
        w.i(0);hb.node(w,'LabFlushEndcap'+label,(0,sign*1.895,0),collider=(1.36,.14,1.36));w.i(1)
    w.i(10,len(MAT))
    for mat in MAT:
        w.s('RW_Lab_'+mat);w.s('KSP/Emissive/Diffuse' if mat=='glass' else 'KSP/Diffuse')
        w.i(4 if mat=='glass' else 2)
        w.s('_Color');w.i(0);w.f(1,1,1,1)
        w.s('_MainTex');w.i(4,list(MAT).index(mat));w.f(1,1);w.f(0,0)
        if mat=='glass':
            w.s('_EmissiveColor');w.i(0);w.f(0,0,0,1)
            w.s('_Emissive');w.i(4,len(MAT));w.f(1,1);w.f(0,0)
    w.i(12,len(MAT)+1)
    for mat in MAT:w.s('rwm_'+mat);w.i(0)
    w.s('rwm_cabin_emissive');w.i(0)
    w.close()

def create_obj(m,dest):
    dest=Path(dest);dest.parent.mkdir(exist_ok=True,parents=True)
    dest.with_suffix('.mtl').write_text(''.join(
        f'newmtl RW_Lab_{mat}\nKa 0.3 0.3 0.3\nKd 1.0 1.0 1.0\nKs 0.2 0.2 0.2\nmap_Kd ../../GameData/RoosterWorksStationModules/Models/rwm_{mat}.png\n\n'
        for mat in MAT),encoding='utf-8')
    with dest.open('w') as f:
        f.write('# RW-LAB-250 procedural laboratory\nmtllib '+dest.with_suffix('.mtl').name+'\n')
        offset=0
        for mat,mesh in m.items():
            f.write('o '+mat+'\nusemtl RW_Lab_'+mat+'\n')
            for xyz in mesh.vertices:f.write('v %0.6f %0.6f %0.6f\n'%xyz)
            for uv in mesh.uvs:f.write('vt %0.6f %0.6f\n'%uv)
            for xyz in mesh.normals:f.write('vn %0.6f %0.6f %0.6f\n'%xyz)
            for tri in mesh.triangles:
                f.write('f '+' '.join(f'{offset+i+1}/{offset+i+1}/{offset+i+1}' for i in tri)+'\n')
            offset+=len(mesh.vertices)

def main():
    make_textures()
    m=geometry()
    create_native_mu(m,MODELS/f'{PART}.mu')
    create_obj(m,ROOT/f'Source/Blender/{PART}.obj')
    print('RW-LAB-250 native model built:',sum(len(mesh.triangles) for mesh in m.values()),'triangles;',sum(len(mesh.vertices) for mesh in m.values()),'vertices')
    print('Model:',MODELS/f'{PART}.mu')

if __name__=='__main__':main()
