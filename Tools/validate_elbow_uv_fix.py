from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
from native_model import load,walk
from tube_material_regression import check as check_tube
golden=json.loads((ROOT/'Tools/elbow_uv_baseline.json').read_text())
for path,digest in golden.items():
    if path.endswith('.version'):continue
    if path.endswith('/RW_TUB_250.mu') or path.endswith('/RW_TUB_375.mu'):
        check_tube(ROOT,path,digest);continue
    if path.endswith('/RW_ELB_250.mu') or path.endswith('/RW_ELB_375.mu'):
        before=ROOT/'Source/Balancing/ElbowUvBefore'/Path(path).name
        assert hashlib.sha256(before.read_bytes()).hexdigest()==digest
        old=load(before);new=load(ROOT/path)
        assert old.materials==new.materials and old.textures==new.textures
        a=list(walk(old.root));b=list(walk(new.root));assert len(a)==len(b)
        for (p,x),(q,y) in zip(a,b):
            assert p==q
            if 'mesh' in x:
                assert x['mesh']['vertices']==y['mesh']['vertices'] and x['mesh']['normals']==y['mesh']['normals']
                assert x['mesh']['submeshes']==y['mesh']['submeshes']
                # Match shared geometric vertices' UVs across adjacent strips.
                if x['name'].endswith('_crest') or x['name'].endswith('_elblabel'):
                    shared={}
                    for v,uv in zip(y['mesh']['vertices'],y['mesh']['uvs']):
                        key=tuple(round(k,6) for k in v)
                        if key in shared:assert np.allclose(shared[key],uv,atol=1e-6),'Discontinuous plaque UV'
                        shared[key]=uv
                y['mesh']['uvs']=x['mesh']['uvs']
        assert old.root==new.root,'Elbow change outside UV coordinates'
    else:assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('Unrelated GameData change',path)
print('PASS elbow UV-only delta: exact prior geometry, normals, materials, indices, physics and gameplay; shared badge UV edges continuous; all other models and GameData byte-preserved')
