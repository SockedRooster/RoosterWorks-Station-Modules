from pathlib import Path
from collections import Counter
import sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from native_model import load,walk
from config_nodes import parse
from build_crew_tubes import geometry,collisions,frame,ARCLENGTH,COLLAR
from station_endcaps import face_mesh
cap=face_mesh()['crest'];cap_uv=np.array(cap.uvs)[np.array(cap.triangles)]
ca=cap_uv[:,1]-cap_uv[:,0];cb=cap_uv[:,2]-cap_uv[:,0]
cap_crest_area=float(np.abs(ca[:,0]*cb[:,1]-ca[:,1]*cb[:,0]).sum()/2)
GD=ROOT/'GameData/RoosterWorksStationModules'
for kind,elbow in (('TUB',False),('ELB',True)):
    for size,scale in ((250,1),(375,1.5)):
        name=f'RW_{kind}_{size}';model=load(GD/f'Models/{name}.mu')
        used=[i for _,n in walk(model.root) for i in n.get('materials',[])]
        assert max(used)+1==len(model.materials) and all(0<=i<len(model.materials) for i in used),'KSPCF-incompatible material table'
        nodes=[n for _,n in walk(model.root)];solids=[n['collider'] for n in nodes if 'collider' in n]
        assert len(solids)==(12 if elbow else 1) and all(c['convex']==1 and c['trigger']==0 for c in solids)
        for c in solids:
            m=c['mesh'];assert len(m['submeshes'][0])==96
            edges=Counter();v=np.array(m['vertices'])
            for tri in m['submeshes'][0]:
                p,q,r=v[list(tri)];n=np.cross(q-p,r-p);assert np.linalg.norm(n)>1e-10
                assert np.max((v-p)@n)<2e-6,('Non-convex collider',name)
                points=[tuple(round(x,5) for x in a) for a in (p,q,r)]
                for i in range(3):edges[tuple(sorted((points[i],points[(i+1)%3])))]+=1
            assert set(edges.values())=={2},('Collider not watertight',name)
        count=0;areas={}
        for n in nodes:
            if 'mesh' not in n:continue
            m=n['mesh'];v=np.array(m['vertices']);normals=np.array(m['normals']);assert len(v)<65535
            assert np.isfinite(v).all() and np.isfinite(normals).all() and np.allclose(np.linalg.norm(normals,axis=1),1,atol=2e-6)
            for tris,index in zip(m['submeshes'],n['materials']):
                count+=len(tris);tri=np.array(tris);p=v[tri]
                normal=np.cross(p[:,1]-p[:,0],p[:,2]-p[:,0])
                dot=np.einsum('ij,ij->i',normal,normals[tri].mean(axis=1))
                assert np.min(dot)>0,('Inverted or degenerate face',name,n['name'],dot.min())
                material=model.materials[index];tex=model.textures[material['properties']['_MainTex']['index']]['name']
                assert material['shader']=='KSP/Diffuse'
                uv=np.array(m['uvs'])[tri];ua=uv[:,1]-uv[:,0];ub=uv[:,2]-uv[:,0]
                areas[tex]=areas.get(tex,0)+float(np.abs(ua[:,0]*ub[:,1]-ua[:,1]*ub[:,0]).sum()/2)
                if 'label' in tex:assert tex.endswith('_375') if size==375 else not tex.endswith('_375')
                if 'label' in tex or tex=='rwm_crest':
                    uv=np.array(m['uvs'])[tri];a=uv[:,1]-uv[:,0];b=uv[:,2]-uv[:,0]
                    assert np.all(a[:,0]*b[:,1]-a[:,1]*b[:,0]<0),('Mirrored badge',name)
        assert count==(40172 if elbow else 17460)
        # Each of the two plaques and two logos covers the artwork exactly once.
        label=f'rwm_{"elblabel" if elbow else "tublabel"}'+('_375' if size==375 else '')
        assert math.isclose(areas[label],2,abs_tol=1e-6) and math.isclose(areas['rwm_crest'],2+2*cap_crest_area,abs_tol=1e-6),'Repeating full artwork in curvature strips'
        assert math.isclose(areas['rwm_cladding']+areas['rwm_cladding_white'],160 if elbow else 64,abs_tol=1e-5),'Panel texture repeats along subdivisions'
        for t in model.textures:assert (GD/f'Models/{t["name"]}.png').is_file()
        part=parse((GD/f'Parts/{name}.cfg').read_text()).children[0]
        assert part.get('CrewCapacity')=='0' and part.get('rescaleFactor')=='1'
        assert not any(n.header in ('MODULE','RESOURCE','INTERNAL') for n in part.children)
        half=ARCLENGTH/2+COLLAR if elbow else 1
        dirs=[]
        for label,y,sign in (('top',half,1),('bottom',-half,-1)):
            values=[float(x.strip()) for x in part.get('node_stack_'+label).split(',')];p,_,t,_=frame(y,elbow)
            assert np.allclose(values[:3],np.array(p)*scale) and np.allclose(values[3:6],np.array(t)*sign) and values[6]==(3 if size==375 else 2)
            dirs.append(np.array(values[3:6]))
        assert math.isclose(float(dirs[0]@dirs[1]),0 if elbow else -1,abs_tol=1e-8)
        # Exact large source geometry is a 1.5x native export, not rescaleFactor.
        if size==375:
            small=load(GD/f'Models/RW_{kind}_250.mu')
            for a,b in zip([n for _,n in walk(small.root) if 'mesh' in n],[n for _,n in walk(model.root) if 'mesh' in n]):
                assert np.allclose(np.array(a['mesh']['vertices'])*1.5,b['mesh']['vertices'],atol=1e-6)
                assert np.allclose(a['mesh']['normals'],b['mesh']['normals'])
        assert (ROOT/f'Source/Blender/{name}.obj').is_file() and (ROOT/f'Source/Blender/{name}.mtl').is_file()
        print('PASS',name,count,'outward visual triangles;',len(solids),'closed convex colliders; readable labels, real stack coordinates, no phantom crew/EVA/supplies')
patch=parse((GD/'Compatibility/CrewTubes.cfg').read_text());assert len(patch.children)==8
assert len([n for n in patch.children if 'FeatureHabitat' in n.header])==4
assert len([n for n in patch.children if 'ConnectedLivingSpace' in n.header])==4
print('PASS straight and perpendicular 90-degree interfaces; both native sizes, pressure and conditional CLS passability; in-game collision/transfer/pressure tests pending')
