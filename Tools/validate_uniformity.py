"""Validate native exports, protected runtime data and shared attachment interfaces."""
from pathlib import Path
import sys,json,math,hashlib
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'.build-deps'),str(R/'Tools'),str(R/'Source')]
import numpy as np
from native_model import load,walk
from config_nodes import parse
GD=R/'GameData/RoosterWorksStationModules';M=GD/'Models';B=R/'Source/Study04Baseline'
report=json.loads((R/'Reports/UNIFORMITY_04.json').read_text())
rules=[]
for cfg in (GD/'Compatibility').glob('*Geometry.cfg'):
    rules.extend(n for n in parse(cfg.read_text()).children if n.header=='RW_RING_MAP')
stats=dict(models=0,colliders_preserved=0,glass_meshes=0,ring_selectors=0,interface_endpoints=0,ladder_joins=0,protected_files=0,largest_mesh_vertices=0)
for entry in report['models']:
    file=M/entry['model'];old=load(B/file.name);new=load(file);a=dict(walk(old.root));b=dict(walk(new.root));stats['models']+=1
    for path,n in a.items():
        if 'collider' in n or 'light' in n or ('Gravity' in path):
            assert path in b,(file.name,path,'missing protected node')
            for key in ('position','rotation','scale','tag','layer','collider','light'):
                assert n.get(key)==b[path].get(key),(file.name,path,key)
        if 'collider' in n:stats['colliders_preserved']+=1
        if 'mesh' in n and 'glass' in old.textures[old.materials[n['materials'][0]]['properties']['_MainTex']['index']]['name']:
            assert path in b and 'mesh' in b[path],(file.name,path,'missing glass')
            assert np.allclose(n['mesh']['vertices'],b[path]['mesh']['vertices'],atol=1e-6),(file.name,path,'glass moved')
            stats['glass_meshes']+=1
    for path,n in b.items():
        if 'mesh' not in n:continue
        m=n['mesh'];v=np.asarray(m['vertices']);tri=np.asarray([t for s in m['submeshes'] for t in s]);stats['largest_mesh_vertices']=max(stats['largest_mesh_vertices'],len(v))
        assert 0<len(v)<65535 and len(tri)>0,(file.name,path)
        assert len(v)==len(m['normals'])==len(m['uvs'])
        assert all(np.isfinite(m[k]).all() for k in ('vertices','normals','uvs'))
        assert tri.min()>=0 and tri.max()<len(v)
        for idx in n['materials']:
            mat=new.materials[idx];props=mat['properties'];tex=new.textures[props['_MainTex']['index']]['name']
            assert 'label' not in tex,(file.name,path,'placard remains')
            for key in ('_MainTex','_BumpMap'):
                if key in props:
                    texture=new.textures[props[key]['index']]['name'];assert any((M/(texture+ext)).exists() for ext in ('.png','.dds','.tga')),(file.name,texture)
            if '_BumpMap' in props:assert len(m['tangents'])==len(v) and np.isfinite(m['tangents']).all()
    for rule in rules:
        if rule.get('model')!=file.stem:continue
        for spec in rule.children:
            path=spec.get('path');m=b[path]['mesh'];assert len(m['vertices'])==int(spec.get('vertices'));assert len(m['submeshes'][0])==int(spec.get('triangles'))
            for token in spec.get('ranges').split(','):
                start,count=map(int,token.split(':'));assert count>0 and start>=0 and start+count<=len(m['submeshes'][0])
            stats['ring_selectors']+=1
    for route in entry['routes']:
        n=next(n for _,n in b.items() if n['name']==f"RW_04_Stack_{route['lane']}_{route['kind']}");v=np.array(n['mesh']['vertices'])
        for end in ('bottom','top'):
            if end not in route['ports']:continue
            port=route['ports'][end];center=np.array(route[end]);direction=np.array(port[3:6]);relative=center-np.array(port[:3]);size=port[6]/2
            assert abs(np.dot(relative,direction))<1e-5,(file.name,end,'off attachment plane')
            assert abs(np.linalg.norm(relative)-(1.30 if route['kind']=='rail' else 1.272)*size)<1e-5
            # Actual exported tube includes a closed end cap centered on this interface.
            near=v[np.abs((v-center)@direction)<1e-5];near=near[np.linalg.norm(near-center,axis=1)<.04*size]
            assert len(near)>=12 and np.linalg.norm(near.mean(0)-center)<1e-5,(file.name,end,'exported cap mismatch')
            if file.stem.split('_')[1]!='ELB':
                angle=math.radians((120,240)[route['lane']])+dict(rail=0,service_blue=.065,service_yellow=.092)[route['kind']]
                radius=(1.30 if route['kind']=='rail' else 1.272)*size
                assert np.allclose(relative,(radius*math.sin(angle),0,radius*math.cos(angle)),atol=1e-5)
            stats['interface_endpoints']+=1
    if entry['ladder_contacts']:
        rail=next(n['mesh'] for p,n in b.items() if n['name'] in ('RW_04_EVA_Rails','RW_04_Hatch_Rails'));rung=next(n['mesh'] for p,n in b.items() if n['name'] in ('RW_04_EVA_Rungs','RW_04_Hatch_Rungs'))
        rv=np.array(rail['vertices']);steps=np.array(rung['vertices']);size=int(file.stem.split('_')[2])/250
        for pair in entry['ladder_contacts']:
            for endpoint in pair:
                c=np.array(endpoint);assert rv[:,1].min()<=c[1]<=rv[:,1].max()
                d=np.linalg.norm(rv[:,[0,2]]-c[[0,2]],axis=1)
                assert d.min()<.015*size and np.linalg.norm(steps-c,axis=1).min()<.015*size
                stats['ladder_joins']+=1
    if file.stem=='RW_GRAV_250':
        assert entry['ring_material_meshes']==11
        sectors=[n for p,n in b.items() if 'GravitySector' in n['name'] and n['name'].endswith('_white')]
        assert len(sectors)==8 and all('_BumpMap' in new.materials[n['materials'][0]]['properties'] for n in sectors)
for path,digest in json.loads((B/'protected_sha256.json').read_text()).items():
    assert hashlib.sha256((GD/path).read_bytes()).hexdigest()==digest,path
    stats['protected_files']+=1
assert stats['models']==47
report.update(status='PASS offline; KSP in-game acceptance pending',validation=stats)
(R/'Reports/UNIFORMITY_04.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(stats,indent=2));print(report['status'])
