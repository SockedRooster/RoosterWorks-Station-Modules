"""Shared stack interfaces, clean hatch geometry and ring art. Run inside Blender."""
from pathlib import Path
import sys,math,copy,json,shutil
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'.build-deps'),str(R/'Source'),str(R/'Tools')]
import numpy as np
from PIL import Image
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from native_model import load,walk
from native_derivatives import write
from config_nodes import parse,dump
from build_attachment_fix import groups,tube_info,face,cap,pad,unit
from build_detail_study import tangents
import build_hab250 as h
GD=R/'GameData/RoosterWorksStationModules';M=GD/'Models';BASE=R/'Source/Study04Baseline';BASE.mkdir(exist_ok=True)
LANES=(2*math.pi/3,4*math.pi/3)

def meshdata(m):return dict(vertices=m.vertices,normals=m.normals,uvs=m.uvs,submeshes=[m.triangles])

def sweep(mesh,points,radius):
    points=np.asarray(points);rings=[];normals=[];side=None
    for i,p in enumerate(points):
        t=unit(points[min(i+1,len(points)-1)]-points[max(0,i-1)])
        if side is None:side=unit(np.cross(t,(0,0,1) if abs(t[2])<.9 else (1,0,0)))
        side=unit(side-t*np.dot(side,t));other=unit(np.cross(t,side))
        nn=[side*math.cos(j*math.tau/12)+other*math.sin(j*math.tau/12) for j in range(12)]
        rings.append([p+radius*n for n in nn]);normals.append(nn)
    for i in range(len(points)-1):
        for j in range(12):
            k=(j+1)%12;p=[rings[i][j],rings[i][k],rings[i+1][k],rings[i+1][j]];n=[normals[i][j],normals[i][k],normals[i+1][k],normals[i+1][j]]
            if np.dot(np.cross(p[1]-p[0],p[2]-p[0]),n[0])<0:p.reverse();n.reverse()
            mesh.quad([tuple(x) for x in p],[tuple(x) for x in n])
    cap(mesh,rings[0],unit(points[0]-points[1]));cap(mesh,rings[-1],unit(points[-1]-points[-2]))

class Edit:
    def __init__(self,model):
        self.model=model;self.maps={};self.original={}
        for path,n in walk(model.root):
            if 'mesh' in n:self.maps[path]=list(range(len(n['mesh']['submeshes'][0])));self.original[path]=copy.deepcopy(n['mesh'])
    def trim(self,path,n,drop):
        if not drop or 'mesh' not in n:return
        m=n['mesh'];keep=[i for i in range(len(m['submeshes'][0])) if i not in drop]
        self.maps[path]=[self.maps[path][i] for i in keep]
        if not keep:
            for key in ('mesh','materials','shadows'):n.pop(key,None)
            return
        tris=[m['submeshes'][0][i] for i in keep];used=sorted({v for t in tris for v in t});remap={v:i for i,v in enumerate(used)}
        for key in ('vertices','normals','uvs','tangents','uv2','colors'):
            if key in m:m[key]=[m[key][i] for i in used]
        m['submeshes']=[[tuple(remap[v] for v in t) for t in tris]]
    def clear(self,path,n):
        if 'mesh' in n:self.trim(path,n,set(range(len(n['mesh']['submeshes'][0]))))
    def texture(self,n):return self.model.textures[self.model.materials[n['materials'][0]]['properties']['_MainTex']['index']]['name']
    def add(self,parent,name,key,mesh):
        if not mesh.vertices:return
        index=next(i for i,m in enumerate(self.model.materials) if self.model.textures[m['properties']['_MainTex']['index']]['name']=='rwm_'+key)
        data=meshdata(mesh)
        if '_BumpMap' in self.model.materials[index]['properties']:tangents(data)
        child=dict(name=name,position=(0,0,0),rotation=(0,0,0,1),scale=(1,1,1),children=[],materials=[index],shadows=(1,1),mesh=data)
        parent['children'].append(child);return child

def inside(points,box):return np.all(points>=box[0]) and np.all(points<=box[1])

def remove_old(e,scale):
    plaques=[];hardware=[];labels=rails=wires=0
    for path,n in list(walk(e.model.root)):
        if 'mesh' not in n:continue
        tex=e.texture(n)
        if 'label' in tex:
            pts=np.array(n['mesh']['vertices']);plaques.append((pts.min(0)-.075*scale,pts.max(0)+.075*scale))
            e.clear(path,n)
            for cp,child in list(walk(n,path.rsplit('/',1)[0])):
                if cp!=path:e.clear(cp,child)
            labels+=1
    for path,n in list(walk(e.model.root)):
        if 'mesh' not in n:continue
        tex=e.texture(n);drop=set()
        if tex.startswith(('rwm_cladding','rwm_hubblanket')) or 'glass' in tex:continue
        for g in groups(n['mesh']):
            p=np.asarray(n['mesh']['vertices'])[g['used']]
            if any(inside(p,b) for b in plaques):drop.update(g['triangles']);continue
            info=tube_info(g)
            dims=np.ptp(p,axis=0);r=np.hypot(p[:,0],p[:,2])
            # Retain the curved end-face grab arcs; replace longitudinal side rails.
            israil=tex=='rwm_rail' and dims[1]>.24*scale and r.min()>1.16*scale and np.linalg.norm(np.asarray(n['mesh']['normals'])[g['used']].mean(0))<.45
            if 'RW_ELB_' in path and tex=='rwm_rail' and max(dims)>1.0*scale:israil=True
            iswire=False
            if info and tex in ('rwm_bronze','rwm_graphite'):
                c,axis,length,radius,_=info
                iswire=abs(axis[1])>.98 and length>.12*scale and radius<.011*scale and np.linalg.norm(((c[0]+c[1])/2)[[0,2]])>1.20*scale
            if israil or iswire:
                drop.update(g['triangles']);rails+=int(israil);wires+=int(iswire)
                hardware.append((p.min(0)-np.array((.10,.07,.10))*scale,p.max(0)+np.array((.10,.07,.10))*scale))
        e.trim(path,n,drop)
    # Remove obsolete feet, stand-offs and cable clips without touching full equipment bays.
    for path,n in list(walk(e.model.root)):
        if 'mesh' not in n:continue
        tex=e.texture(n)
        if tex not in ('rwm_steel','rwm_graphite','rwm_bronze','rwm_black'):continue
        drop=set()
        for g in groups(n['mesh']):
            p=np.asarray(n['mesh']['vertices'])[g['used']]
            if max(np.ptp(p,axis=0))<.16*scale and any(inside(p,b) for b in hardware):drop.update(g['triangles'])
        e.trim(path,n,drop)
    return dict(placards_removed=labels,old_rail_components_removed=rails,old_wire_components_removed=wires)

def hatch_geometry(theta,y,scale,flanks):
    m={key:h.Mesh() for key in h.TEXTURES};saved=h.window_bay_foundation
    h.window_bay_foundation=lambda *args:None
    try:h.hatch_pressure_bay(m,theta,y,.710)
    finally:h.window_bay_foundation=saved
    h.window_frame_ring(m['graphite'],h.curved_rect_contour(theta,y,.438,.433),h.curved_rect_contour(theta,y,.410,.407),1.203,1.199)
    if flanks:
        for sign in (-1,1):
            a,b=sorted((theta+sign*.425,theta+sign*.734))
            h.cylinder_surface(m['cladding'],1.204,y-.392,y+.392,segments=16,theta0=a,theta1=b)
        m['cladding'].uvs=[(1-u,v) for u,v in m['cladding'].uvs]
    # Solid sidewalls behind the door's layered surround; no panoramic window foundation.
    returns=h.Mesh()
    for key,mesh in list(m.items()):
        if key in ('glass','rail') or not mesh.vertices:continue
        for g in groups(meshdata(mesh)):
            if np.linalg.norm(np.asarray(mesh.normals)[g['used']].mean(0))<.70:continue
            for a,b in g['boundary']:
                p0,p1=g['points'][a],g['points'][b]
                def back(p):return np.array(h.point(1.197,math.atan2(p[0],p[2]),p[1]))
                face(returns,(p1,p0,back(p0),back(p1)))
    offset=len(m['black'].vertices);m['black'].vertices.extend(returns.vertices);m['black'].normals.extend(returns.normals);m['black'].uvs.extend(returns.uvs);m['black'].triangles.extend(tuple(i+offset for i in t) for t in returns.triangles)
    for mesh in m.values():mesh.vertices=[tuple(v*scale for v in p) for p in mesh.vertices]
    return m

def ladder(e,parent,theta,ys,lo,hi,scale,prefix):
    rails=h.Mesh();steps=h.Mesh();mounts=h.Mesh()
    angle=.36 if prefix=='EVA' else .45
    for side in (-1,1):
        t=theta+side*angle
        sweep(rails,[h.point(1.30*scale,t,lo*scale),h.point(1.30*scale,t,hi*scale)],.014*scale)
        normal=np.array((math.sin(t),0,math.cos(t)))
        for yy in (lo+.07,hi-.07):
            base=np.array(h.point(1.203*scale,t,yy*scale));pad(mounts,base,np.array((0,1,0)),normal,scale)
            h.tube(mounts,tuple(base),h.point(1.30*scale,t,yy*scale),r=.014*scale,sides=10)
    contacts=[]
    for yy in ys:
        path=[h.point(1.30*scale,theta-angle+2*angle*j/24,yy*scale) for j in range(25)]
        sweep(steps,path,.014*scale);contacts.append([list(path[0]),list(path[-1])])
    e.add(parent,'RW_04_'+prefix+'_Rails','rail',rails);e.add(parent,'RW_04_'+prefix+'_Rungs','rail',steps);e.add(parent,'RW_04_'+prefix+'_Mounts','steel',mounts)
    return contacts

def fix_hatches(e,role,scale):
    results=[]
    if role in ('HAB','HABS'):
        parent=next(n for p,n in walk(e.model.root) if n['name']=='SideHatch');parentpath=next(p for p,n in walk(e.model.root) if n is parent)
        # Preserve the exact glass renderer name used by cabin-light modules.
        glassname=next(n['name'] for p,n in walk(parent) if 'mesh' in n and 'glass' in e.texture(n))
        for path,n in list(walk(parent,parentpath.rsplit('/',1)[0])):e.clear(path,n)
        parent['children']=[]
        y=0 if role=='HABS' else -1.730+2.5*3.460/8
        for key,mesh in hatch_geometry(math.pi/3,y,scale,True).items():
            e.add(parent,glassname if key=='glass' else 'RW_04_Hatch_'+key,key,mesh)
        results=ladder(e,parent,math.pi/3,(y-.65,y-.43),y-.72,y+.56,scale,'Hatch')
    elif role=='AIR':
        glassname=next(n['name'] for p,n in walk(e.model.root) if 'mesh' in n and 'glass' in e.texture(n))
        for path,n in list(walk(e.model.root)):
            if 'mesh' not in n or e.texture(n).startswith('rwm_cladding'):continue
            drop=set()
            for g in groups(n['mesh']):
                p=np.asarray(n['mesh']['vertices'])[g['used']]/scale;theta=np.arctan2(p[:,0],p[:,2]);rad=np.hypot(p[:,0],p[:,2]);dims=np.ptp(p,axis=0)
                in_hatch=np.all(abs(theta)<.75) and rad.min()>1.19 and p[:,1].min()>-.665 and p[:,1].max()<.365
                rung=np.all(abs(theta)<.43) and rad.min()>1.18 and dims[1]<.06 and dims[0]>.4 and -.96<p[:,1].mean()<-.48
                if in_hatch or rung:drop.update(g['triangles'])
            e.trim(path,n,drop)
        for key,mesh in hatch_geometry(0,-.15,scale,False).items():
            # Reuse the original renderer instead of creating two equally named transforms.
            if key=='glass':
                n=next(n for _,n in walk(e.model.root) if n['name']==glassname);index=next(i for i,m in enumerate(e.model.materials) if e.model.textures[m['properties']['_MainTex']['index']]['name']=='rwm_glass')
                n.update(mesh=meshdata(mesh),materials=[index],shadows=(1,1));n['children']=[]
            else:e.add(e.model.root,'RW_04_AirHatch_'+key,key,mesh)
        results=ladder(e,e.model.root,0,(-.91,-.72,-.53),-1.2,1.2,scale,'EVA')
    return results

def surface_tree(e):
    vv=[];tt=[]
    for path,n in walk(e.model.root):
        if 'mesh' not in n or '/SideHatch/' in path or 'GravityRotor' in path:continue
        if 'glass' in e.texture(n):continue
        # Main families bake their static geometry in root coordinates.
        if n['position']!=(0.,0.,0.) or n['rotation']!=(0.,0.,0.,1.):continue
        m=n['mesh'];off=len(vv);vv.extend(m['vertices']);tt.extend(tuple(v+off for v in t) for s in m['submeshes'] for t in s)
    return BVHTree.FromPolygons(vv,tt,all_triangles=True)

def ports(part):
    out={}
    for name in ('bottom','top'):
        val=part.get('node_stack_'+name)
        if val:out[name]=[float(v.strip()) for v in val.split(',')]
    return out

def uniform_routes(e,role,scale,port):
    if 'bottom' not in port:return []
    bottom=port['bottom'];top=port.get('top',[0,-.26*scale,0,0,1,0,bottom[6]])
    tree=surface_tree(e);records=[]
    if role=='ELB':
        from build_crew_tubes import frame,ARCLENGTH,COLLAR
        half=ARCLENGTH/2+COLLAR
        def centre(f):
            c,n,t,_=frame(-half+2*half*f,True);return np.array(c)*scale,np.array(n),np.array(t)
    else:
        def centre(f):return np.array(bottom[:3])*(1-f)+np.array(top[:3])*f,np.array((1,0,0)),np.array((0,1,0))
    def sample(f,theta,kind):
        c,n,t=centre(f);z=unit(np.cross(n,t));s=(bottom[6]*(1-f)+top[6]*f)/2
        shift=(math.pi/12 if theta<math.pi else -math.pi/12)*math.sin(math.pi*f)**2 if role=='HUB' else 0
        a=theta+shift;out=n*math.sin(a)+z*math.cos(a)
        loc,_,_,_=tree.ray_cast(Vector(c+out*4*scale),Vector(-out),4*scale)
        skin=float(np.dot(np.array(loc)-c,out)) if loc is not None else 1.204*s
        skin=max(.1,min(skin,2.6*scale))
        radius=max(1.30*s,skin+.045*s)
        # Terminal collars use an exact shared radius and tangent, not sampled fitting height.
        if f<.035 or f>.965:radius=1.30*s
        if kind!='rail':radius-=.028*s
        if role=='GRAV' and kind!='rail' and abs(c[1])<.55:radius=1.245
        return c+out*radius,c+out*skin,out,t,s
    for lane,theta in enumerate(LANES):
        for kind,da,r in (('rail',0,.014),('service_blue',.065,.007),('service_yellow',.092,.007)):
            mesh=h.Mesh();mounts=h.Mesh();ranges=[(0,1)]
            if role=='GRAV' and kind=='rail':ranges=[(0,.35),(.65,1)]
            for lo,hi in ranges:
                samples=[sample(f,theta+da,kind) for f in np.linspace(lo,hi,65)]
                points=[v[0] for v in samples];sweep(mesh,points,r*scale)
                for j in range(4,61,14):
                    target,foot,out,t,s=samples[j]
                    if role=='GRAV' and abs(target[1])<.60:continue
                    pad(mounts,foot,t,out,s,depth=.009 if kind=='rail' else .005)
                    h.tube(mounts,tuple(foot),tuple(target),r=(.012 if kind=='rail' else .009)*s,sides=8)
            e.add(e.model.root,f'RW_04_Stack_{lane}_{kind}',kind,mesh);e.add(e.model.root,f'RW_04_Stack_{lane}_{kind}_Mounts','steel',mounts)
            records.append(dict(lane=lane,kind=kind,bottom=sample(0,theta+da,kind)[0].tolist(),top=sample(1,theta+da,kind)[0].tolist(),ports=port))
    return records

def ring_art(e):
    model=e.model;idx=next(i for i,m in enumerate(model.materials) if model.textures[m['properties']['_MainTex']['index']]['name']=='rwm_cladding_white');count=0
    for path,n in walk(model.root):
        if 'mesh' not in n:continue
        name=n['name'];sector='GravitySector' in name and name.endswith('_white')
        hub=name=='RW_GravityHub';access='GravityAccessTube' in name
        if not (sector or hub or access):continue
        n['materials']=[idx];m=n['mesh']
        if hub:m['uvs']=[(u*12,v*8) for u,v in m['uvs']]
        if sector:
            v=np.array(m['vertices']);normal=np.array(m['normals']);uv=np.array(m['uvs']);amount=.005*np.maximum(0,np.sin(math.pi*(uv[:,0]%1))*np.sin(math.pi*(uv[:,1]%1)))
            m['vertices']=(v+normal*amount[:,None]).tolist()
        tangents(m);count+=1
    return count

def ranges(values):
    out=[]
    for i in sorted(values):
        if out and i==out[-1][0]+out[-1][1]:out[-1][1]+=1
        else:out.append([i,1])
    return ','.join(f'{a}:{b}' for a,b in out)

def main():
    source=R.parent/'RoosterWorks-Attachment-Fix-03/GameData/RoosterWorksStationModules'
    if not source.exists():
        for path in BASE.glob('*.mu'):shutil.copyfile(path,M/path.name)
        for path in BASE.glob('*Geometry.cfg'):shutil.copyfile(path,GD/'Compatibility'/path.name)
    for path in source.rglob('*'):
        if path.is_file():target=GD/path.relative_to(source);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(path,target)
    for name,color in (('service_blue',(53,104,164)),('service_yellow',(212,173,49))):Image.new('RGB',(32,32),color).save(M/f'rwm_{name}.png')
    configs={p.name:parse(p.read_text()) for p in (GD/'Compatibility').glob('*Geometry.cfg')}
    audit=[]
    for path in sorted(M.glob('*.mu')):
        shutil.copyfile(path,BASE/path.name);model=load(path);e=Edit(model);role=path.stem.split('_')[1];scale=int(path.stem.split('_')[2])/250
        for key in ('service_blue','service_yellow'):
            index=len(model.textures);model.textures.append(dict(name='rwm_'+key,type=0));model.materials.append(dict(name='RW_04_'+key,shader='KSP/Specular',properties={'_MainTex':dict(index=index,scale=(1.,1.),offset=(0.,0.)),'_Color':(1.,1.,1.,1.),'_SpecColor':(.3,.3,.3,1.),'_Shininess':.3}))
        entry=dict(model=path.name,**remove_old(e,scale));entry['ladder_contacts']=fix_hatches(e,role,scale)
        cfg=GD/'Parts'/(path.stem+'.cfg');part=parse(cfg.read_text()).children[0] if cfg.exists() else None
        entry['routes']=uniform_routes(e,role,scale,ports(part)) if part else []
        entry['ring_material_meshes']=ring_art(e) if role=='GRAV' else 0
        nodes=dict(walk(model.root));updated=0
        for config in configs.values():
            for rule in config.children:
                if rule.header!='RW_RING_MAP' or rule.get('model')!=path.stem:continue
                kept=[]
                for spec in rule.children:
                    address=spec.get('path');selected=set()
                    for token in spec.get('ranges').split(','):
                        a,b=map(int,token.split(':'));selected.update(range(a,a+b))
                    surviving=[j for j,old in enumerate(e.maps.get(address,[])) if old in selected]
                    if not surviving or address not in nodes or 'mesh' not in nodes[address]:continue
                    mesh=nodes[address]['mesh'];spec.set('vertices',len(mesh['vertices']));spec.set('triangles',len(mesh['submeshes'][0]));spec.set('ranges',ranges(surviving));kept.append(spec);updated+=1
                rule.children=kept
        entry['ring_map_meshes']=updated;write(model,path);audit.append(entry)
        print(path.name,'placards',entry['placards_removed'],'service routes',len(entry['routes']),'hatch rungs',len(entry['ladder_contacts']),'ring art',entry['ring_material_meshes'],flush=True)
    for name,config in configs.items():(GD/'Compatibility'/name).write_text(dump(config))
    (R/'Reports/UNIFORMITY_04.json').write_text(json.dumps(dict(status='Built; validation pending',lanes_degrees=[120,240],models=audit),indent=2)+'\n')

if __name__=='__main__':main()
