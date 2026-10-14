"""Original cosmetic engineering details. No colliders or gameplay modules.

One shared atlas keeps small equipment panels economical. All UV islands have
an inset gutter; units are metres, +Y is the existing KSP stack axis.
"""
import math

def append(dst, src):
    off=len(dst.vertices)
    dst.vertices.extend(src.vertices); dst.normals.extend(src.normals)
    dst.uvs.extend(src.uvs)
    dst.triangles.extend(tuple(i+off for i in tri) for tri in src.triangles)

def atlas_uv(u,v,slot):
    # Atlas rows are specified top-down, mesh V is bottom-up.
    col=slot%4; row=slot//4
    top,height=(212,88) if slot in (4,5,6) else (12,488)
    return ((col*256+12+232*(1-u))/1024, 1-(row*512+top+height*(1-v))/1024)

def plate(m,theta,y,width=.24,height=.36,slot=0,radius=1.235):
    import build_hab250 as h
    # Layered gasket, metallic bevel and inset textured cover. All follow hull.
    angle=width/radius
    h.flat_panel(m['black'],theta,y-height/2-.018,y+height/2+.018,angle+.027,radius-.011,16)
    h.flat_panel(m['steel'],theta,y-height/2-.010,y+height/2+.010,angle+.013,radius-.006,16)
    src=h.Mesh()
    h.flat_panel(src,theta,y-height/2,y+height/2,angle,radius,16)
    src.uvs=[atlas_uv(u,v,slot) for u,v in src.uvs]
    append(m['detail'],src)
    for dt in (-angle*.43,angle*.43):
        for dy in (-height*.43,height*.43):
            h.radial_fastener(m['steel'],theta+dt,y+dy,radius=radius+.002,head=.0055)

def connector(m,theta,y,radius=1.235):
    import build_hab250 as h
    # Closed electrical/thermal quick-disconnect cover and hexagonal flange.
    a=h.point(radius,theta,y); b=h.point(radius+.016,theta,y)
    h.tube(m['graphite'],a,b,r=.039,sides=12)
    h.tube(m['steel'],h.point(radius+.011,theta,y),h.point(radius+.021,theta,y),r=.031,sides=6)
    # Solid outward caps: an uncapped tube alone reads as floating wire rings.
    normal=(math.sin(theta),0,math.cos(theta));tangent=(math.cos(theta),0,-math.sin(theta))
    for material,r,depth,sides in (('steel',.031,.021,6),('black',.017,.022,16)):
        center=h.point(radius+depth,theta,y)
        def vertex(a):
            return tuple(center[k]+r*math.cos(a)*tangent[k]+(r*math.sin(a) if k==1 else 0) for k in range(3))
        for j in range(sides):
            m[material].triangle((center,vertex(math.tau*j/sides),vertex(math.tau*(j+1)/sides)),
                                 (normal,)*3,((.5,.5),(0,0),(1,0)))

def conduit(m,theta,y0,y1,radius=1.230):
    import build_hab250 as h
    for da,material in ((-.023,'graphite'),(.023,'bronze')):
        h.tube(m[material],h.point(radius,theta+da,y0),h.point(radius,theta+da,y1),r=.007,sides=6)
    for yy in (y0,(y0+y1)*.5,y1):
        h.flat_panel(m['steel'],theta,yy-.010,yy+.010,.071,radius+.009,6)

def radiator(m,theta,y,width=.36,height=.48,radius=1.240):
    import build_hab250 as h
    plate(m,theta,y,width,height,slot=2,radius=radius)
    angle=width/radius*.88
    for k in range(10):
        yy=y-height*.38+k*height*.76/9
        h.flat_panel(m['graphite'],theta,yy-.008,yy+.008,angle,radius+.006,16)
        h.flat_panel(m['rail'],theta,yy+.004,yy+.009,angle,radius+.011,16)

def add_hab(m):
    import build_hab250 as h
    # Upper/lower service decks clear of every full window/hatch footprint.
    for theta in (.10,math.pi-.64,math.pi+.64):
        for y in (-1.30,1.26):
            placement=3.40 if theta>math.pi and y>0 else theta
            # Disallow details overlapping the accepted pressure-window bays.
            angle=.26/1.235
            assert not any(a<placement+angle/2 and b>placement-angle/2 and c<y+.16 and d>y-.16
                           for a,b,c,d in h.bay_openings())
            plate(m,placement,y,.26,.30,slot=0)
            connector(m,placement+.21,y)
    for theta in (math.pi-.64,math.pi+.64):
        conduit(m,theta,-.17,.17)
        plate(m,theta,1.62,.18,.15,slot=6,radius=1.237)

def add_lab(m):
    # Research instrumentation, thermal hardware and fluid manifold.
    for theta in (.72*math.pi,1.28*math.pi):
        plate(m,theta,1.30,.27,.36,slot=3)
        radiator(m,theta,-1.27,.30,.38)
        conduit(m,theta,-.86,.50)
    plate(m,math.pi,-.17,.46,.42,slot=1,radius=1.246)
    for theta in (math.pi-.26,math.pi+.26):
        for y in (-.34,.02):connector(m,theta,y)
    plate(m,.40,-1.35,.16,.18,slot=6)

def add_cmd(m):
    # Paired removable avionics units and a protected data-bus loom.
    for theta in (-1.32,1.32):
        plate(m,theta,-.36,.28,.32,slot=1,radius=1.243)
        connector(m,theta,.52,radius=1.235)
    for theta in (-2.08,2.08):
        plate(m,theta,.54,.21,.16,slot=3)
        conduit(m,theta,-.33,.35,radius=1.241)
    plate(m,0,-.46,.34,.20,slot=5)

def add_cup(m):
    # Observation frame is untouched; service instruments fit lower barrel.
    for theta in (-1.72,1.72):
        plate(m,theta,-.555,.31,.30,slot=3,radius=1.237)
        connector(m,theta+.23,-.535)
    for theta in (-.48,.48):
        plate(m,theta,-.690,.15,.13,slot=6,radius=1.232)

def add_log(m):
    for bank in range(4):
        theta=math.tau*bank/4
        for y in (-.655,.655):
            # Small cargo ID plaque sits above grille, below existing top strip.
            plate(m,theta,y+.253,.25,.047,slot=4,radius=1.258)
        angle=math.tau*(bank+.5)/4
        for y in (-.65,.65):
            # Offset from the original paired handrails; no rail through text.
            plate(m,angle+.235,y,.26,.35,slot=7,radius=1.246)
            connector(m,angle+.235,y-.27,radius=1.239)

def add_hub_port(m):
    # Short collar plates stay behind the common mating face; rotated per port.
    for theta in (0,math.pi/2,math.pi,3*math.pi/2):
        plate(m,theta,1.756,.24,.14,slot=5,radius=1.225)
    # Routed shoulder looms are repeated in each port's local frame.
    from build_hub250 import shoulder
    import build_hab250 as h
    for theta in (math.pi/4,3*math.pi/4,5*math.pi/4,7*math.pi/4):
        for dt,mat in ((-.025,'graphite'),(.025,'bronze')):
            for k in range(7):
                p=shoulder(theta+dt,.20+.60*k/7,.009)
                q=shoulder(theta+dt,.20+.60*(k+1)/7,.009)
                h.tube(m[mat],p,q,r=.008,sides=6)
        for u in (.24,.50,.76):
            p=shoulder(theta-.037,u,.012);q=shoulder(theta+.037,u,.012)
            h.tube(m['steel'],p,q,r=.009,sides=6)

def add_endcap(m):
    import build_hab250 as h
    # Continuous metal skirt eliminates an exposed floating lip. Inside plane.
    # Outer rim skirt is now closed to the lip in station_endcaps.face_mesh().
    for inner,outer,y,material in ((.627,.637,1.947,'bronze'),(1.086,1.094,1.948,'graphite')):
        h.annulus(m[material],inner,outer,y,segments=96)
    for j in range(12):
        theta=math.tau*(j+.5)/12
        h.tube(m['steel'],h.point(1.055,theta,1.938),h.point(1.055,theta,1.957),r=.008,sides=6)
    # Four recessed circuit/pressure ID plates with identical local geometry.
    for j in range(4):
        theta=math.tau*j/4+.30
        center=h.point(.95,theta,1.959)
        tangent=(math.cos(theta),0,-math.sin(theta));radial=(math.sin(theta),0,math.cos(theta))
        pts=[tuple(center[k]+u*tangent[k]+v*radial[k] for k in range(3))
             for u,v in ((-.075,.105),(.075,.105),(.075,-.105),(-.075,-.105))]
        m['detail'].quad(pts,((0,1,0),)*4,tuple(atlas_uv(u,v,5) for u,v in ((0,0),(1,0),(1,1),(0,1))))
