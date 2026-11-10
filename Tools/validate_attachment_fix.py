"""Study 03 regression checks against the exact Study 02 native models."""
from pathlib import Path
import sys,json,zipfile
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'.build-deps'),str(R/'Tools'),str(R/'Source')]
import numpy as np
from native_model import load,walk
from config_nodes import parse
M=R/'GameData/RoosterWorksStationModules/Models';B=R/'Source/Study03Baseline'
report=json.loads((R/'Reports/ATTACHMENT_FIX_03.json').read_text());colliders=glass=ringmaps=protected=0;counts={};largest=0
rules=[]
for cfg in (R/'GameData/RoosterWorksStationModules/Compatibility').glob('*Geometry.cfg'):
    rules.extend(n for n in parse(cfg.read_text()).children if n.header=='RW_RING_MAP')
for file in sorted(M.glob('*.mu')):
    old=load(B/file.name);new=load(file);a=dict(walk(old.root));b=dict(walk(new.root));assert old.materials==new.materials and old.textures==new.textures
    for path,n in a.items():
        after=b[path]
        for key,value in n.items():
            if key not in ('children','mesh'):assert after[key]==value,(file.name,path,key)
        if 'collider' in n:colliders+=1
        if 'mesh' not in n:continue
        tex=old.textures[old.materials[n['materials'][0]]['properties']['_MainTex']['index']]['name']
        if tex!='rwm_rail':
            assert n['mesh']['submeshes']==after['mesh']['submeshes']
            assert n['mesh']['uvs']==after['mesh']['uvs']
            assert len(n['mesh']['vertices'])==len(after['mesh']['vertices'])
        if 'Glass' in path or 'glass' in tex:
            assert n['mesh']==after['mesh'],path;glass+=1
    counts[file.name]=0
    for path,n in b.items():
        if 'mesh' not in n:continue
        m=n['mesh'];v=np.asarray(m['vertices']);normal=np.asarray(m['normals']);uv=np.asarray(m['uvs']);tri=np.asarray([t for sub in m['submeshes'] for t in sub])
        largest=max(largest,len(v));assert len(v)<65535
        assert len(v)==len(normal)==len(uv) and np.isfinite(v).all() and np.isfinite(normal).all() and np.isfinite(uv).all()
        assert tri.min()>=0 and tri.max()<len(v)
        if '/RW_Seated03_' in path:
            area=np.linalg.norm(np.cross(v[tri[:,1]]-v[tri[:,0]],v[tri[:,2]]-v[tri[:,0]]),axis=1)
            assert area.min()>1e-12,(file.name,path,'degenerate support')
        for idx in n['materials']:
            if '_BumpMap' in new.materials[idx]['properties']:assert len(m['tangents'])==len(v)
        counts[file.name]+=len(tri)
    for rule in rules:
        if rule.get('model')!=file.stem:continue
        for spec in rule.children:
            path=spec.get('path');assert len(a[path]['mesh']['vertices'])==len(b[path]['mesh']['vertices'])==int(spec.get('vertices'))
            assert a[path]['mesh']['submeshes']==b[path]['mesh']['submeshes'];ringmaps+=1
with zipfile.ZipFile(R.parent/'RoosterWorks-Detail-Study-02-Install.zip') as z:
    for name in z.namelist():
        if name.startswith('GameData/') and not name.endswith('.mu'):
            assert (R/name).read_bytes()==z.read(name),name;protected+=1
report.update(status='PASS offline; in-game grazing-angle acceptance pending',validation=dict(models=len(counts),colliders_preserved=colliders,glass_meshes_preserved=glass,ring_selector_meshes_preserved=ringmaps,unchanged_runtime_files=protected,largest_mesh_vertices=largest,triangle_counts=counts),totals=dict(handles=sum(e['handles'] for e in report['models']),seated_tubes=sum(e['seated_tubes'] for e in report['models']),closed_panel_edges=sum(e['closed_panel_edges'] for e in report['models'])))
(R/'Reports/ATTACHMENT_FIX_03.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(counts),'native models;',colliders,'colliders;',glass,'glass meshes;',ringmaps,'selector meshes;',protected,'unchanged files')
print(report['totals']);print('Largest mesh',largest,'vertices; all new supports non-degenerate')
