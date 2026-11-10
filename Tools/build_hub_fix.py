"""Surface-mounted service routes for the six-way hub; Blender background Python."""
from pathlib import Path
import sys,math,json,shutil
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'Tools'),str(R/'Source'),str(R/'.build-deps')]
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from build_uniformity import Edit,sweep,ranges
from build_attachment_fix import groups,pad,unit
from native_model import load,walk
from native_derivatives import write
from config_nodes import parse,dump
import build_hab250 as h
import build_hub250 as hub
GD=R/'GameData/RoosterWorksStationModules';M=GD/'Models';B=R/'Source/Study05Baseline'

def port_orient(p,axis):
    # Shortest rotation from a module's +Y to the radial port normal, with no roll.
    k=np.cross((0,1,0),axis);p=np.array(p)
    return np.cross(k,p)+k*np.dot(k,p)

def tree_for(model):
    vv=[];tt=[]
    for _,n in walk(model.root):
        if 'mesh' not in n or not n['name'].startswith('RW_Hub_'):continue
        tex=model.textures[model.materials[n['materials'][0]]['properties']['_MainTex']['index']]['name']
        if tex not in ('rwm_cladding','rwm_cladding_white','rwm_hubblanket','rwm_ceramic','rwm_white'):continue
        m=n['mesh'];off=len(vv);vv.extend(m['vertices']);tt.extend(tuple(i+off for i in t) for s in m['submeshes'] for t in s)
    return BVHTree.FromPolygons(vv,tt,all_triangles=True)

def build(file):
    model=load(B/file.name);e=Edit(model);scale=int(file.stem.split('_')[2])/250
    # The old axial runs and their supports are wholly replaced.
    model.root['children']=[n for n in model.root['children'] if not n['name'].startswith('RW_04_Stack_')]
    removed=0
    for path,n in list(walk(model.root)):
        if 'mesh' not in n or e.texture(n) not in ('rwm_steel','rwm_graphite','rwm_bronze'):continue
        drop=set()
        for g in groups(n['mesh']):
            p=np.array(n['mesh']['vertices'])[g['used']]/scale
            # Shoulder loom segments and clips: inside all collar roots, small disconnected components.
            if np.abs(p).max()<1.595 and np.ptp(p,axis=0).max()<.27:
                drop.update(g['triangles']);removed+=1
        e.trim(path,n,drop)
    tree=tree_for(model);audit=[];contacts=[]
    def project(p):
        # Closest hull point avoids selecting the far side of a neighboring port.
        loc,normal,_,_=tree.find_nearest(Vector(p))
        assert loc is not None,tuple(p)
        return np.array(loc),unit(normal)
    def add_route(name,raw,kind,endpoints=()):
        radius=(.014 if kind=='rail' else .007)*scale;clearance=(.043 if kind=='rail' else .020)*scale
        points=[];feet=[];normals=[]
        for i,p in enumerate(raw):
            foot,normal=project(p);points.append(foot+normal*clearance);feet.append(foot);normals.append(normal)
        # Average faceted skin normals through the path, avoiding zigzags at panel joints.
        points=np.array(points)
        for _ in range(12):points[1:-1]=.25*points[:-2]+.5*points[1:-1]+.25*points[2:]
        # Three terminal samples share the mating radius and axial tangent.
        for index,center,axis in endpoints:
            step=np.linalg.norm(np.array(raw[1])-raw[0])
            for j in range(3):
                k=index-j if index else j
                points[k]=np.array(center)-np.array(axis)*(step*j)
            for j in range(3,13):
                k=index-j if index else j;w=(j-2)/11;w=w*w*(3-2*w)
                straight=np.array(center)-np.array(axis)*(step*j)
                points[k]=straight*(1-w)+points[k]*w
        mesh=h.Mesh();mounts=h.Mesh();sweep(mesh,points,radius)
        for i in range(5,len(points)-4,8):
            foot=feet[i];normal=normals[i];tangent=unit(np.array(points[min(i+1,len(points)-1)])-points[max(0,i-1)])
            tangent=unit(tangent-normal*np.dot(tangent,normal))
            pad(mounts,foot-normal*.002*scale,tangent,normal,scale,depth=.008 if kind=='rail' else .004)
            h.tube(mounts,tuple(foot-normal*.002*scale),tuple(points[i]),r=(.012 if kind=='rail' else .006)*scale,sides=8)
            contacts.append(dict(route=name,foot=foot.tolist(),top=np.asarray(points[i]).tolist(),normal=normal.tolist()))
        e.add(model.root,name,kind,mesh);e.add(model.root,name+'_Mounts','steel',mounts)
        audit.append(dict(name=name,kind=kind,centers=[np.asarray(p).tolist() for p in points],feet=[p.tolist() for p in feet],radius=radius,endpoints=[dict(index=i,center=list(c),axis=list(a)) for i,c,a in endpoints]))
    # Full pole-to-pole runs keep the original top/bottom stack convention.
    for lane,theta in enumerate((2*math.pi/3,4*math.pi/3)):
        for kind,delta in (('rail',0),('service_blue',.065),('service_yellow',.092)):
            raw=[]
            for y in np.linspace(-2,2,129):
                blend=math.sin(math.pi*(y+2)/4)**2
                a=theta+(math.pi/12 if lane==0 else -math.pi/12)*blend+delta
                # A spherical guiding path, then exact projection onto the rendered skin.
                r=math.sqrt(max(1.204**2,1.80**2-y*y))
                raw.append(np.array(h.point(r,a,y))*scale)
            rr=(1.30 if kind=='rail' else 1.272)*scale
            ends=[(0,h.point(rr,theta+delta,-2*scale),(0,-1,0)),(128,h.point(rr,theta+delta,2*scale),(0,1,0))]
            add_route(f'RW_05_Axial_{lane}_{kind}',raw,kind,ends)
    # Side-port wires use the mating face's handedness. Every branch then wraps
    # around the upper/lower shoulder and joins the corresponding axial service.
    for port,axis in hub.PORTS.items():
        if port in ('top','bottom'):continue
        for lane,theta in enumerate((2*math.pi/3,4*math.pi/3)):
            for kind,delta in (('rail',0),('service_blue',.065),('service_yellow',.092)):
                raw=[]
                for t in np.linspace(0,1,65):
                    y=2-(2-1.28)*t;a=theta+(math.pi/12 if lane==0 else -math.pi/12)*(t*t*(3-2*t))-delta
                    rr=1.204 if y>=1.6 else (hub.neck_radius(y) if y>=1.3 else math.sqrt(1.8**2-y*y))
                    raw.append(port_orient(h.point(rr,a,y),axis)*scale)
                rr=(1.30 if kind=='rail' else 1.272)*scale
                center=port_orient(h.point(rr,theta-delta,2*scale),axis)
                start=np.array(raw[-1]);sign=1 if start[1]>=0 else -1
                angle=math.atan2(start[0],start[2]);height=sign*1.36*scale
                choices=[]
                for axial in [r for r in audit if 'Axial' in r['name'] and r['kind']==kind]:
                    pp=np.array(axial['centers']);idx=int(np.argmin(abs(pp[:,1]-height)));end=pp[idx];endangle=math.atan2(end[0],end[2]);turn=(endangle-angle+math.pi)%(2*math.pi)-math.pi
                    choices.append((abs(turn),turn,end,axial['name'],idx))
                _,turn,end,target,target_index=min(choices,key=lambda v:v[0])
                # Rise around the spherical shoulder first, then follow the neck
                # circumference to the existing stack lane. No path crosses a cap.
                target_direction=unit(h.point(math.sqrt(1.8**2-1.36**2)*scale,angle,height))
                start_direction=unit(start)
                for t in np.linspace(0,1,33)[1:]:
                    w=t*t*(3-2*t);direction=unit(start_direction*(1-w)+target_direction*w);raw.append(direction*1.8*scale)
                for t in np.linspace(0,1,max(17,int(abs(turn)*40)))[1:]:
                    a=angle+turn*t;raw.append(np.array(h.point(hub.neck_radius(1.36)*scale,a,height)))
                name=f'RW_05_{port}_{lane}_{kind}'
                add_route(name,raw,kind,[(0,center,axis)])
                n=next(n for _,n in walk(model.root) if n['name']==name)
                # A true geometric tee: exact same center as the matching axial tube.
                record=audit[-1];points=np.array(record['centers']);correction=end-points[-1]
                for j in range(12):
                    w=(j/11)**2*(3-2*j/11);points[-12+j]+=correction*w
                mesh=h.Mesh();sweep(mesh,points,record['radius']);n['mesh']=dict(vertices=mesh.vertices,normals=mesh.normals,uvs=mesh.uvs,submeshes=[mesh.triangles]);record['centers']=points.tolist()
                record['join']=dict(target=target,index=target_index,center=end.tolist())
    # Remap only hub selectors whose mesh triangles were trimmed.
    nodes=dict(walk(model.root))
    for cfg in (GD/'Compatibility').glob('*Geometry.cfg'):
        config=parse(cfg.read_text())
        for rule in config.children:
            if rule.header!='RW_RING_MAP' or rule.get('model')!=file.stem:continue
            kept=[]
            for spec in rule.children:
                path=spec.get('path');selected=set()
                for token in spec.get('ranges').split(','):
                    a,b=map(int,token.split(':'));selected.update(range(a,a+b))
                surviving=[j for j,old in enumerate(e.maps.get(path,[])) if old in selected]
                if surviving and path in nodes and 'mesh' in nodes[path]:
                    m=nodes[path]['mesh'];spec.set('vertices',len(m['vertices']));spec.set('triangles',len(m['submeshes'][0]));spec.set('ranges',ranges(surviving));kept.append(spec)
            rule.children=kept
        cfg.write_text(dump(config))
    write(model,file)
    return dict(model=file.name,removed_loom_components=removed,routes=audit,mounts=contacts)

if __name__=='__main__':
    for cfg in B.glob('*Geometry.cfg'):shutil.copyfile(cfg,GD/'Compatibility'/cfg.name)
    result=[]
    for file in sorted(M.glob('RW_HUB_*.mu')):
        result.append(build(file));print(file.name,'complete',flush=True)
    (R/'Reports/HUB_ROUTING_06.json').write_text(json.dumps(dict(status='Built; validation pending',models=result),indent=2))
