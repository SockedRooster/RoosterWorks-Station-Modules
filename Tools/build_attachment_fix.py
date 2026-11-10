"""Seat native exterior attachments; run with Blender --background --python.

Reads Study 02, never an installed game. Raycasts against exported opaque geometry.
Original selector-indexed triangles are retained; only unindexed rail meshes rebuild.
"""
from pathlib import Path
import sys,math,json,zipfile,copy
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'.build-deps'),str(R/'Source'),str(R/'Tools')]
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from native_model import load,walk
from native_derivatives import write
import build_hab250 as h
from build_detail_study import recalc
M=R/'GameData/RoosterWorksStationModules/Models';B=R/'Source/Study03Baseline';B.mkdir(exist_ok=True)

def unit(v):
    v=np.asarray(v,dtype=float);return v/max(np.linalg.norm(v),1e-12)

def groups(mesh):
    verts=np.array(mesh['vertices']);tri=np.array(mesh['submeshes'][0]);uv=np.array(mesh['uvs'])
    unique,inv=np.unique(np.round(verts,6),axis=0,return_inverse=True);parent=list(range(len(unique)))
    def find(a):
        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
        return a
    for a,b,c in inv[tri]:
        root=find(int(a));parent[find(int(b))]=root;parent[find(int(c))]=root
    grouped={}
    for i,t in enumerate(tri):grouped.setdefault(find(int(inv[t[0]])),[]).append(i)
    for indices in grouped.values():
        tids=np.array(indices);used=np.unique(tri[tids]);edges={}
        for a,b,c in inv[tri[tids]]:
            for a,b in ((a,b),(b,c),(c,a)):
                key=tuple(sorted((int(a),int(b))))
                if key in edges:edges[key]=None
                else:edges[key]=(int(a),int(b))
        boundary=[e for e in edges.values() if e is not None]
        yield dict(triangles=tids,used=used,points=unique,inv=inv,boundary=boundary)

def loops(g):
    adjacent={}
    for a,b in g['boundary']:adjacent.setdefault(a,[]).append(b);adjacent.setdefault(b,[]).append(a)
    if not adjacent or any(len(v)!=2 for v in adjacent.values()):return []
    unseen=set(adjacent);out=[]
    while unseen:
        start=min(unseen);path=[start];prev=None;cur=start
        while True:
            nxt=next((v for v in adjacent[cur] if v!=prev),None)
            if nxt==start:break
            if nxt is None or nxt in path:return []
            path.append(nxt);prev,cur=cur,nxt
        unseen.difference_update(path);out.append(path)
    return out

def face(mesh,points):
    points=np.asarray(points,dtype=float);n=unit(np.cross(points[1]-points[0],points[2]-points[0]))
    if np.linalg.norm(n)<.5:return
    if len(points)==3:mesh.triangle(points.tolist(),[tuple(n)]*3,[(.5,.5)]*3)
    else:mesh.quad(points.tolist(),[tuple(n)]*4,[(.5,.5)]*4)

def cap(mesh,ring,normal):
    ring=np.asarray(ring);centre=ring.mean(axis=0)
    for i in range(len(ring)):
        a=ring[i];b=ring[(i+1)%len(ring)]
        if np.dot(np.cross(a-centre,b-centre),normal)<0:a,b=b,a
        face(mesh,(centre,a,b))

def pad(mesh,centre,axis,normal,scale,depth=.012):
    axis=unit(axis);normal=unit(normal);side=unit(np.cross(axis,normal))
    outline=[(-.018,-.041),(.018,-.041),(.025,-.032),(.025,.032),(.018,.041),(-.018,.041),(-.025,.032),(-.025,-.032)]
    bottom=[centre+scale*(side*u+axis*v-normal*.0015) for u,v in outline]
    top=[centre+scale*(side*u*.88+axis*v*.94+normal*depth) for u,v in outline]
    cap(mesh,top,normal);cap(mesh,bottom,-normal)
    for j in range(8):
        k=(j+1)%8;p=[bottom[j],bottom[k],top[k],top[j]]
        outward=(bottom[j]+bottom[k])/2-centre
        if np.dot(np.cross(p[1]-p[0],p[2]-p[0]),outward)<0:p.reverse()
        face(mesh,p)

def curved_tube(mesh,path,radius):
    path=np.asarray(path);tangent=[]
    for i in range(len(path)):tangent.append(unit(path[min(i+1,len(path)-1)]-path[max(0,i-1)]))
    side=unit(np.cross(tangent[len(tangent)//2],path[0]-path[2]))
    if np.linalg.norm(side)<.5:side=unit(np.cross(tangent[0],(1,0,0)))
    rings=[];norms=[]
    for p,t in zip(path,tangent):
        b=unit(np.cross(t,side));nn=[side*math.cos(j*math.tau/12)+b*math.sin(j*math.tau/12) for j in range(12)]
        rings.append([p+radius*n for n in nn]);norms.append(nn)
    for i in range(len(path)-1):
        for j in range(12):
            k=(j+1)%12;pts=[rings[i][j],rings[i][k],rings[i+1][k],rings[i+1][j]];ns=[norms[i][j],norms[i][k],norms[i+1][k],norms[i+1][j]]
            if np.dot(np.cross(pts[1]-pts[0],pts[2]-pts[0]),ns[0])<0:pts.reverse();ns.reverse()
            mesh.quad([tuple(p) for p in pts],[tuple(n) for n in ns])
    cap(mesh,rings[0],-tangent[0]);cap(mesh,rings[-1],tangent[-1])

def tube_info(g):
    ll=loops(g)
    if len(ll)!=2 or not 5<=len(ll[0])<=32 or len(ll[0])!=len(ll[1]):return None
    rings=[g['points'][a] for a in ll];centres=[a.mean(axis=0) for a in rings];axis=unit(centres[1]-centres[0]);length=np.linalg.norm(centres[1]-centres[0])
    radius=np.mean(np.linalg.norm(rings[0]-centres[0],axis=1))
    if radius<1e-6 or length<1e-6:return None
    if max(abs((r-centres[i])@axis).max() for i,r in enumerate(rings))>radius*.03:return None
    if max(np.std(np.linalg.norm(r-centres[i],axis=1)) for i,r in enumerate(rings))>radius*.03:return None
    return centres,axis,length,radius,rings

def variant(path):
    return 'hatch' if '/SideHatch/' in path else 'window' if '/WindowBankStandard/' in path else 'base'

def identity(n):return n['position']==(0.,0.,0.) and n['rotation']==(0.,0.,0.,1.) and n['scale']==(1.,1.,1.)

def build_one(filename):
    model=load(filename);original=copy.deepcopy(model);snapshot=list(walk(model.root));nodes=dict(snapshot)
    eligible=[];skipped=[]
    for path,n in snapshot:
        if 'mesh' not in n:continue
        ancestors=[v for p,v in snapshot if path==p or path.startswith(p+'/')]
        if not all(identity(v) for v in ancestors):skipped.append(path);continue
        if len(n['materials'])!=1:continue
        mat=model.materials[n['materials'][0]];tex=model.textures[mat['properties']['_MainTex']['index']]['name']
        if 'Emissive' in mat['shader'] or 'Alpha' in mat['shader'] or 'glass' in tex.lower():continue
        if tex.startswith(('rwm_grnleaf','rwm_grnroot')):continue
        eligible.append((path,n,tex))
    # Unit scale inferred from model family, including size-pair adapters.
    bits=filename.stem.split('_');size=int(bits[2]) if bits[2].isdigit() else 250;scale=size/250
    trees={}
    for mode in ('base','hatch','window'):
        vv=[];tt=[]
        for path,n,tex in eligible:
            if variant(path) not in ('base',mode):continue
            m=n['mesh'];offset=len(vv);vv.extend(m['vertices']);tt.extend(tuple(i+offset for i in t) for s in m['submeshes'] for t in s)
        trees[mode]=BVHTree.FromPolygons(vv,tt,all_triangles=True)
    audit=dict(model=filename.name,handles=0,seated_tubes=0,closed_panel_edges=0,skipped_transformed_meshes=len(skipped),max_return_m=0.,mounts=[])
    additions={};handle_mounts=[]
    def add(path,material):
        key=(path,material)
        if key not in additions:additions[key]=h.Mesh()
        return additions[key]
    def support(point,direction,mode,limit=.14):
        direction=unit(direction);origin=np.asarray(point)-direction*.0007*scale
        loc,no,_,dist=trees[mode].ray_cast(Vector(origin),Vector(-direction),limit*scale)
        if loc is None:return None
        return np.asarray(loc)-direction*.001*scale
    # Replace long straight rail tubes with continuous round-return handles.
    for path,n,tex in eligible:
        if tex!='rwm_rail':continue
        m=n['mesh'];remove=set();new=h.Mesh()
        for g in groups(m):
            info=tube_info(g)
            if info is None:continue
            centres,axis,length,radius,rings=info
            if length<.26*scale or radius>.032*scale or abs(axis[1])<.98:continue
            a,b=sorted(centres,key=lambda p:p[1]);normal=unit((a[0]+b[0],0,a[2]+b[2]))
            if np.linalg.norm((a+b)[[0,2]]/2)<1.15*scale:continue
            split=[(a,b)]
            if length>1.7*scale:
                mid=(a+b)/2;split=[(a,mid-np.array((0,.27*scale,0))),(mid+np.array((0,.27*scale,0)),b)]
            accepted=[]
            for aa,bb in split:
                # Start below the old grip's back surface, so it cannot support itself.
                foot0=support(aa-normal*(radius+.001*scale),normal,variant(path));foot1=support(bb-normal*(radius+.001*scale),normal,variant(path))
                if foot0 is None or foot1 is None:continue
                # Maintain the existing maximum grip envelope and functional ladder route.
                depth=min(float(np.dot(aa-foot0,normal)),float(np.dot(bb-foot1,normal)))
                if depth<.025*scale:continue
                direction=unit(foot1-foot0);bend=min(.027*scale,depth*.55);start=foot0+normal*(depth-bend)
                route=[foot0+normal*.012*scale,start]
                for phi in np.linspace(math.pi,math.pi/2,7)[1:]:route.append(foot0+direction*bend+normal*(depth-bend)+direction*bend*math.cos(phi)+normal*bend*math.sin(phi))
                for phi in np.linspace(math.pi/2,0,7):route.append(foot1-direction*bend+normal*(depth-bend)+direction*bend*math.cos(phi)+normal*bend*math.sin(phi))
                route.append(foot1+normal*.012*scale)
                curved_tube(new,route,min(radius,.013*scale))
                for foot in (foot0,foot1):
                    pad(add(path,'graphite'),foot,direction,normal,scale,depth=.003)
                    pad(add(path,'steel'),foot+normal*.002*scale,direction,normal,scale,depth=.012)
                    # Two small captive heads stay clear of the grip's returned end.
                    side=unit(np.cross(direction,normal))
                    for sign in (-1,1):
                        centre=foot+direction*(sign*.028*scale)+normal*.014*scale
                        top=centre+normal*.0025*scale
                        h.tube(add(path,'graphite'),tuple(centre),tuple(top),r=.0045*scale,sides=8)
                        ring=[top+.0045*scale*(side*math.cos(j*math.tau/8)+direction*math.sin(j*math.tau/8)) for j in range(8)]
                        cap(add(path,'graphite'),ring,normal)
                    handle_mounts.append((variant(path),foot,normal))
                    audit['mounts'].append(dict(path=path,point=foot.tolist(),normal=normal.tolist(),embedded_m=.001*scale))
                accepted.append((aa,bb));audit['handles']+=1
            assert not accepted or len(accepted)==len(split),'Partial handle rebuild would overlap its source'
            if len(accepted)==len(split):remove.update(g['triangles'].tolist())
        if remove:
            oldtris=m['submeshes'][0];kept=[t for i,t in enumerate(oldtris) if i not in remove];used=sorted({i for t in kept for i in t});mapping={v:i for i,v in enumerate(used)}
            for key in ('vertices','normals','uvs'):
                m[key]=[m[key][i] for i in used]+getattr(new,key)
            m['submeshes']=[[(mapping[a],mapping[b],mapping[c]) for a,b,c in kept]+[tuple(i+len(used) for i in t) for t in new.triangles]]
            for key in ('tangents','uv2','colors'):m.pop(key,None)
    # Ground open fastener/stand-off roots, and give their tips real end caps.
    for path,n,tex in eligible:
        if tex not in ('rwm_steel','rwm_bronze','rwm_graphite','rwm_rail'):continue
        m=n['mesh'];verts=np.array(m['vertices']);changed=False
        for g in groups(m):
            info=tube_info(g)
            if info is None:continue
            centres,axis,length,radius,rings=info;mid=sum(centres)/2;radial=unit((mid[0],0,mid[2]))
            if radius>.041*scale or length>.16*scale or abs(np.dot(axis,radial))<.94:continue
            order=sorted(range(2),key=lambda i:np.linalg.norm(centres[i][[0,2]]));lo,hi=order
            normal=unit(centres[hi]-centres[lo]);foot=support(centres[lo],normal,variant(path),.09)
            if foot is None:continue
            delta=foot-centres[lo]
            if np.linalg.norm(delta)>.09*scale:continue
            shortened=next((f for mode,f,nn in handle_mounts if mode==variant(path) and np.linalg.norm((f-centres[lo])-normal*np.dot(f-centres[lo],normal))<.008*scale),None)
            if shortened is not None:topdelta=shortened+normal*.012*scale-centres[hi]
            elif radius<=.012*scale:
                # A bolt needs a low head above its backing, not a long exposed peg.
                topdelta=foot+normal*max(.0025*scale,min(.006*scale,radius*.6))-centres[hi]
            else:topdelta=np.zeros(3)
            ids0=set(loops(g)[lo]);ids1=set(loops(g)[hi])
            for index in g['used']:
                if g['inv'][index] in ids0:verts[index]+=delta
                elif g['inv'][index] in ids1:verts[index]+=topdelta
            cap(add(path,tex[4:]),rings[hi]+topdelta,normal)
            cap(add(path,tex[4:]),rings[lo]+delta,-normal)
            changed=True;audit['seated_tubes']+=1
        if changed:m['vertices']=verts.tolist()
    # Shell every open patch perimeter down to the next opaque surface.
    for path,n,tex in eligible:
        if tex in ('rwm_rail','rwm_hubblanket') or any(s in tex for s in ('grnleaf','grnroot')):continue
        m=n['mesh'];normals=np.asarray(m['normals'])
        for g in groups(m):
            if not g['boundary']:continue
            mean=normals[g['used']].mean(axis=0)
            if np.linalg.norm(mean)<.70:continue
            normal=unit(mean);centre=np.asarray(m['vertices'])[g['used']].mean(axis=0)
            radial=unit((centre[0],0,centre[2]));radial_mode=abs(normal[1])<.30 and np.dot(normal,radial)>.75
            mat=tex[4:] if tex in ('rwm_white','rwm_ceramic','rwm_steel','rwm_bronze','rwm_graphite','rwm_black') else 'ceramic' if 'cladding' in tex else 'graphite'
            backing=add(path,mat);cache={}
            for a,b in g['boundary']:
                endpoints=[]
                for index in (a,b):
                    if index not in cache:
                        p=g['points'][index];direction=unit((p[0],0,p[2])) if radial_mode else normal
                        foot=support(p,direction,variant(path),.12)
                        cache[index]=foot
                    endpoints.append(cache[index])
                if any(p is None for p in endpoints):continue
                p0,p1=g['points'][a],g['points'][b];q0,q1=endpoints
                depth=max(np.linalg.norm(p0-q0),np.linalg.norm(p1-q1))
                if depth<.0012*scale:continue
                face(backing,(p1,p0,q0,q1));audit['closed_panel_edges']+=1;audit['max_return_m']=max(audit['max_return_m'],depth)
    for (path,material),mesh in additions.items():
        if not mesh.vertices:continue
        index=next((i for i,m in enumerate(model.materials) if model.textures[m['properties']['_MainTex']['index']]['name']=='rwm_'+material),None)
        if index is None:index=nodes[path]['materials'][0]
        # Small fixed-color support meshes inherit their parent variant visibility.
        for chunk,start in enumerate(range(0,len(mesh.triangles),14000)):
            tris=mesh.triangles[start:start+14000];used=sorted({i for t in tris for i in t});remap={v:i for i,v in enumerate(used)}
            newmesh=dict(vertices=[mesh.vertices[i] for i in used],normals=[mesh.normals[i] for i in used],uvs=[mesh.uvs[i] for i in used],submeshes=[[tuple(remap[i] for i in t) for t in tris]])
            nodes[path]['children'].append(dict(name=f'RW_Seated03_{material}_{chunk}',position=(0,0,0),rotation=(0,0,0,1),scale=(1,1,1),children=[],shadows=(1,1),materials=[index],mesh=newmesh))
    write(model,filename);return audit

def main():
    with zipfile.ZipFile(R.parent/'RoosterWorks-Detail-Study-02-Install.zip') as z:
        for name in z.namelist():
            if name.startswith('GameData/') and not name.endswith('/'):(R/name).write_bytes(z.read(name))
    audit=[]
    for file in sorted(M.glob('*.mu')):
        (B/file.name).write_bytes(file.read_bytes());entry=build_one(file);audit.append(entry)
        print(file.name,'handles',entry['handles'],'seated tubes',entry['seated_tubes'],'closed edges',entry['closed_panel_edges'],flush=True)
    (R/'Reports/ATTACHMENT_FIX_03.json').write_text(json.dumps(dict(status='Built; validation pending',models=audit),indent=2)+'\n')

if __name__=='__main__':main()
