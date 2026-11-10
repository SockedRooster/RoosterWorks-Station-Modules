"""Validate native geometry, protected gameplay, selector maps and DXT5nm mips."""
from pathlib import Path
import sys,json,zipfile,struct,math
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'.build-deps'),str(R/'Tools'),str(R/'Source')]
import numpy as np
from PIL import Image
from native_model import load,walk
from config_nodes import parse
M=R/'GameData/RoosterWorksStationModules/Models'
B=R/'Source/Study02Baseline'
counts={};protected=0;colliders=0;glass=0;ringmaps=0
for p in sorted(M.glob('*.mu')):
    old=load(B/p.name);new=load(p);oldnodes=dict(walk(old.root));nodes=dict(walk(new.root))
    habitat=p.stem.startswith(('RW_HAB_','RW_HABS_'))
    for path,n in oldnodes.items():
        after=nodes[path]
        for key,value in n.items():
            if key not in ('children','mesh'):assert after[key]==value,(p.name,path,key)
        if 'collider' in n:colliders+=1
        if 'mesh' not in n:continue
        before=n['mesh'];mesh=after['mesh']
        tex=old.textures[old.materials[n['materials'][0]]['properties']['_MainTex']['index']]['name']
        cladding=tex in ('rwm_cladding','rwm_cladding_white')
        if not (habitat and cladding):
            assert mesh['submeshes']==before['submeshes'] and mesh['uvs']==before['uvs'],(p.name,path)
            assert len(mesh['vertices'])==len(before['vertices'])
        if not habitat or 'Glass' in path:
            assert mesh['vertices']==before['vertices'],(p.name,path)
            if tex!='rwm_hubblanket':assert mesh['normals']==before['normals'],(p.name,path)
        if 'Glass' in path:assert mesh==before;glass+=1
    total=0
    for path,n in nodes.items():
        if 'mesh' not in n:continue
        mesh=n['mesh'];v=np.asarray(mesh['vertices']);normal=np.asarray(mesh['normals']);uv=np.asarray(mesh['uvs'])
        assert len(v)<65535 and len(v)==len(normal)==len(uv)
        assert np.isfinite(v).all() and np.isfinite(normal).all() and np.isfinite(uv).all()
        assert all(0<=i<len(v) for sub in mesh['submeshes'] for tri in sub for i in tri)
        total+=sum(len(sub) for sub in mesh['submeshes'])
        if 'tangents' in mesh:
            tangent=np.asarray(mesh['tangents']);assert len(tangent)==len(v) and np.isfinite(tangent).all()
            assert np.max(np.abs(np.linalg.norm(tangent[:,:3],axis=1)-1))<.001
            assert np.max(np.abs(np.sum(tangent[:,:3]*normal,axis=1)))<.003
            assert np.all(abs(tangent[:,3])==1)
    for tex in new.textures:
        assert any((M/(tex['name']+ext)).exists() for ext in ('.png','.dds'))
        if tex['name'].endswith('_NRM'):assert tex['type']==1
    counts[p.name]=total
    # Every configured selector still sees identical vertex counts and triangle indices.
    for cfg in (R/'GameData/RoosterWorksStationModules/Compatibility').glob('*Geometry.cfg'):
        for rule in parse(cfg.read_text()).children:
            if rule.header!='RW_RING_MAP' or rule.get('model')!=p.stem:continue
            for spec in rule.children:
                path=spec.get('path');assert path in nodes,(cfg.name,path)
                a=oldnodes[path]['mesh'];b=nodes[path]['mesh']
                assert a['submeshes']==b['submeshes'] and len(a['vertices'])==len(b['vertices'])
                assert len(b['vertices'])==int(spec.get('vertices'));ringmaps+=1
for kind in ('quilt','foil'):
    path=M/f'rwm_{kind}_NRM.dds';data=path.read_bytes();assert data[:4]==b'DDS ' and data[84:88]==b'DXT5'
    levels=struct.unpack_from('<I',data,28)[0];assert levels==11
    expected=128+sum(max(1,(max(1,1024>>i)+3)//4)**2*16 for i in range(levels));assert len(data)==expected
    rgba=np.asarray(Image.open(path));xy=rgba[:,:,[3,1]].astype(float)/127.5-1
    assert np.mean(np.sum(xy*xy,axis=-1))<.45
    assert rgba[:,:,0].min()>245 and rgba[:,:,2].min()>245
with zipfile.ZipFile(R.parent/'RoosterWorks-Visual-Development-01-Install.zip') as z:
    for name in z.namelist():
        if name.startswith('GameData/') and '/Models/' not in name:
            assert (R/name).read_bytes()==z.read(name),name;protected+=1
report=json.loads((R/'Reports/DETAIL_STUDY_02.json').read_text())
report.update(status='PASS offline; KSP runtime acceptance pending',native_models_validated=len(counts),colliders_preserved=colliders,glass_meshes_preserved=glass,ring_selector_meshes_preserved=ringmaps,gameplay_files_byte_identical=protected,dds_normals='2 DXT5nm maps, 11 mip levels each, normal texture flag + orthonormal tangents',triangle_counts=counts)
(R/'Reports/DETAIL_STUDY_02.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS',len(counts),'models;',colliders,'colliders;',glass,'glass meshes;',ringmaps,'ring-selector meshes;',protected,'gameplay files')
print('PASS normal map references, 11-level DXT5nm chains, tangents and 16-bit mesh limits')
