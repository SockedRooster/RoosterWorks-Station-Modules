"""Run with Blender: exported geometry and surface contact regression checks."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_hub_fix import *
import hashlib
report=json.loads((R/'Reports/HUB_ROUTING_06.json').read_text());stats=dict(models=0,colliders=0,routes=0,mounts=0,interfaces=0,joins=0,unchanged_models=0,unchanged_other_files=0)
for entry in report['models']:
    file=M/entry['model'];old=load(B/file.name);new=load(file);a=dict(walk(old.root));b=dict(walk(new.root));tree=tree_for(new);scale=int(file.stem.split('_')[2])/250
    assert old.materials==new.materials and old.textures==new.textures
    for path,n in a.items():
        if 'collider' in n:
            assert n==b[path],(file.name,path,'collider changed');stats['colliders']+=1
        if 'mesh' in n and n['name'].startswith('RW_Hub_') and any(s in n['name'] for s in ('cladding','ceramic','white','hubblanket','detail','crest','black')):
            assert n==b[path],(file.name,path,'protected surface changed')
    for path,n in b.items():
        if 'mesh' not in n:continue
        m=n['mesh'];v=np.array(m['vertices']);tri=np.array([t for s in m['submeshes'] for t in s]);assert 0<len(v)<65535
        assert len(v)==len(m['normals'])==len(m['uvs']);assert all(np.isfinite(m[k]).all() for k in ('vertices','normals','uvs'));assert tri.min()>=0 and tri.max()<len(v)
        if n['name'].startswith('RW_05_'):
            areas=np.linalg.norm(np.cross(v[tri[:,1]]-v[tri[:,0]],v[tri[:,2]]-v[tri[:,0]]),axis=1)
            assert areas.min()>1e-12,(file.name,path,'degenerate triangles')
        for idx in n['materials']:
            if '_BumpMap' in new.materials[idx]['properties']:assert len(m['tangents'])==len(v)
    for route in entry['routes']:
        n=next(n for _,n in b.items() if n['name']==route['name']);v=np.array(n['mesh']['vertices']);points=np.array(route['centers']);assert np.linalg.norm(np.diff(points,axis=0),axis=1).min()>1e-7
        for endpoint in route['endpoints']:
            c=np.array(endpoint['center']);axis=np.array(endpoint['axis']);near=v[np.abs((v-c)@axis)<1e-5];near=near[np.linalg.norm(near-c,axis=1)<.04*scale]
            assert len(near)>=12 and np.linalg.norm(near.mean(0)-c)<1e-5,(file.name,route['name'],'cap center')
            assert abs(np.dot(c,axis)-2*scale)<1e-5
            radius=np.linalg.norm(c-axis*np.dot(c,axis));assert abs(radius-(1.30 if route['kind']=='rail' else 1.272)*scale)<1e-5
            lane=int(route['name'].split('_')[3]);theta=(2*math.pi/3,4*math.pi/3)[lane]+(1 if 'Axial' in route['name'] else -1)*dict(rail=0,service_blue=.065,service_yellow=.092)[route['kind']]
            x,z=radius*math.sin(theta),radius*math.cos(theta)
            expected=(2*scale*axis[0],-axis[0]*x,z) if axis[0] else ((x,-axis[2]*z,2*scale*axis[2]) if axis[2] else (x,2*scale*axis[1],z))
            assert np.allclose(c,expected,atol=1e-5),(file.name,route['name'],'port roll mismatch')
            stats['interfaces']+=1
        for p in points[13:-6]:
            loc,normal,_,distance=tree.find_nearest(Vector(p))
            assert distance<.10*scale,(file.name,route['name'],'unsupported gap',distance)
        stats['routes']+=1
        if 'join' in route:
            join=route['join'];target=next(r for r in entry['routes'] if r['name']==join['target']);assert target['kind']==route['kind']
            assert np.allclose(points[-1],target['centers'][join['index']],atol=1e-7)
            # Check the actual exported branch end ring reaches the target center.
            c=np.array(join['center']);assert np.linalg.norm(v-c,axis=1).min()<=route['radius']*1.001
            assert not any(n['name']==route['name']+'_Terminal' for _,n in b.items())
            stats['joins']+=1
    for mount in entry['mounts']:
        loc,_,_,distance=tree.find_nearest(Vector(mount['foot']));assert distance<1e-5
        assert np.linalg.norm(np.array(mount['foot'])-mount['top'])<.13*scale
        stats['mounts']+=1
    assert entry['removed_loom_components']>0;stats['models']+=1
for cfg in (GD/'Compatibility').glob('*Geometry.cfg'):
    for rule in parse(cfg.read_text()).children:
        if rule.header!='RW_RING_MAP' or not rule.get('model').startswith('RW_HUB_'):continue
        nodes=dict(walk(load(M/(rule.get('model')+'.mu')).root))
        for spec in rule.children:
            m=nodes[spec.get('path')]['mesh'];assert len(m['vertices'])==int(spec.get('vertices')) and len(m['submeshes'][0])==int(spec.get('triangles'))
            for token in spec.get('ranges').split(','):
                start,count=map(int,token.split(':'));assert start>=0 and count>0 and start+count<=len(m['submeshes'][0])
    before=parse((B/cfg.name).read_text());after=parse(cfg.read_text())
    assert [dump(n) for n in before.children if not (n.get('model') or '').startswith('RW_HUB_')]==[dump(n) for n in after.children if not (n.get('model') or '').startswith('RW_HUB_')]
for path,digest in json.loads((B/'runtime_sha256.json').read_text()).items():
    if Path(path).name.startswith('RW_HUB_') and path.endswith('.mu'):continue
    if path.endswith('Geometry.cfg'):continue
    if path.endswith('.version') and (R/'RELEASE_METADATA.json').exists():
        assert json.loads((GD/path).read_text())['VERSION']==json.loads((R/'RELEASE_METADATA.json').read_text())['version_tuple']
        continue
    assert hashlib.sha256((GD/path).read_bytes()).hexdigest()==digest,path
    stats['unchanged_models' if path.endswith('.mu') else 'unchanged_other_files']+=1
assert stats['models']==3 and stats['unchanged_models']==44 and stats['interfaces']==108 and stats['joins']==72
report.update(status='PASS offline; KSP in-game acceptance pending',validation=stats)
(R/'Reports/HUB_ROUTING_06.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status']);print(json.dumps(stats,indent=2))
