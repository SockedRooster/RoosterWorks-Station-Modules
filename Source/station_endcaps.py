"""Shared original RoosterWorks layered endcap, canonical mating plane Y=2.

Reuse one mesh for HUB/HAB/LAB/CMD. Lower caps rotate 180 degrees about X;
all decoration is recessed within the existing stack plane.
"""
import math
import build_hab250 as h
def cross(a,b):return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def quad(mesh,p,uv=((0,0),(1,0),(1,1),(0,1))):
    n=cross(sub(p[1],p[0]),sub(p[2],p[0]));length=math.sqrt(sum(v*v for v in n))
    mesh.quad(p,[tuple(v/length for v in n)]*4,uv)
def append(dest,src):
    offset=len(dest.vertices)
    dest.vertices.extend(src.vertices);dest.normals.extend(src.normals);dest.uvs.extend(src.uvs)
    dest.triangles.extend(tuple(i+offset for i in t) for t in src.triangles)
def face_mesh():
    MAT=h.TEXTURES
    m={key:h.Mesh() for key in MAT}
    # Layered interface: thin structural lip, recessed bronze thermal
    # blanket and a smaller central pressure bulkhead. Surface fittings
    # are original decorative geometry; no EVA or docking functionality.
    caps={k:h.Mesh() for k in MAT}
    h.annulus(caps['graphite'],1.145,1.225,1.997,segments=96)
    h.annulus(caps['steel'],1.127,1.145,1.993,segments=96)
    h.cylinder_surface(caps['graphite'],1.127,1.921,1.993,segments=96)
    # Actual shallow folds in the blanket catch light without increasing
    # the mating envelope. Radial/angular UVs map the unique blanket texture.
    def blanket(r,t):
        depth=1.934+.004*math.sin(t*37+r*9)+.002*math.sin(t*71-r*14)
        return h.point(r,t,depth)
    for ring in range(8):
        r0=.59+.537*ring/8;r1=.59+.537*(ring+1)/8
        for j in range(144):
            a=math.tau*j/144;b=math.tau*(j+1)/144
            quad(m['hubblanket'],[blanket(r0,a),blanket(r1,a),blanket(r1,b),blanket(r0,b)],
                 ((j/144,ring/8),(j/144,(ring+1)/8),((j+1)/144,(ring+1)/8),((j+1)/144,ring/8)))
    h.cylinder_surface(caps['steel'],.615,1.929,1.986,segments=64)
    h.annulus(caps['steel'],.51,.615,1.986,segments=64)
    h.annulus(caps['black'],.485,.51,1.982,segments=64)
    h.annulus(caps['ceramic'],.13,.485,1.970,segments=64)
    h.annulus(caps['steel'],.104,.13,1.981,segments=48)
    for j in range(48):
        a=math.tau*j/48;b=math.tau*(j+1)/48
        caps['black'].triangle([(0,1.977,0),h.point(.104,a,1.977),h.point(.104,b,1.977)],
                              [(0,1,0)]*3,[(.5,.5),(0,0),(1,0)])
    for mesh in caps.values():
        mesh.uvs=[(.5+x/2.5,.5+z/2.5) for x,y,z in mesh.vertices]
    for mat in MAT:append(m[mat],caps[mat])
    for j in range(24):
        t=math.tau*j/24
        h.tube(m['steel'],h.point(1.184,t,1.983),h.point(1.184,t,2.0),r=.011,sides=8)
    # Four recessed fasteners and a small pressure-door handle.
    for j in range(4):
        t=math.pi/4+math.pi*j/2
        h.tube(m['graphite'],h.point(.55,t,1.974),h.point(.55,t,1.993),r=.020,sides=8)
    h.tube(m['steel'],(-.31,1.980,-.13),(-.31,1.980,.13),r=.017,sides=8)
    # Stand-off rail arcs hug the blanket; no fictitious functional grab.
    for center in (math.pi/2,3*math.pi/2):
        for j in range(18):
            a=center-.50+j/18;b=center-.50+(j+1)/18
            h.tube(m['rail'],h.point(.86,a,1.978),h.point(.86,b,1.978),r=.018,sides=8)
        for t in (center-.50,center+.50):
            h.tube(m['steel'],h.point(.86,t,1.938),h.point(.86,t,1.978),r=.027,sides=8)
    # Twin routed service lines distinguish these from uniform flat caps.
    for offset,mat in ((0,'graphite'),(.032,'bronze')):
        for j in range(16):
            a=.30+j*.70/16;b=.30+(j+1)*.70/16
            h.tube(m[mat],h.point(.72+offset,a,1.961),h.point(.72+offset,b,1.961),r=.009,sides=6)
    # Small flat brand plate below the central closure.
    quad(m['crest'],[(-.09,1.977,.35),(.09,1.977,.35),
                     (.09,1.977,.17),(-.09,1.977,.17)])
    return m
def add_endcap(meshes,sign,plane):
    for mat,mesh in face_mesh().items():
        placed=h.Mesh([(x,sign*(plane+y-2),sign*z) for x,y,z in mesh.vertices],
                      [(x,sign*y,sign*z) for x,y,z in mesh.normals],
                      list(mesh.uvs),list(mesh.triangles))
        append(meshes[mat],placed)
