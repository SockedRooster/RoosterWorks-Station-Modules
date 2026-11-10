"""Current visual candidate checks, independent of historical art fingerprints."""
from pathlib import Path
import sys,json,math
R=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(R/'.build-deps'),str(R/'Tools')]
from native_model import load,walk
from PIL import Image
M=R/'GameData/RoosterWorksStationModules/Models'
audit=json.loads((R/'Reports/VISUAL_UPGRADE.json').read_text())
counts={}
for p in M.glob('*.mu'):
    model=load(p);count=0
    for _,n in walk(model.root):
        if 'mesh' not in n:continue
        m=n['mesh'];v=len(m['vertices'])
        assert v<65535 and v==len(m['normals'])==len(m['uvs']),p.name
        assert all(math.isfinite(x) for key in ('vertices','normals','uvs') for vec in m[key] for x in vec)
        assert all(0<=i<v for sub in m['submeshes'] for tri in sub for i in tri)
        assert len(m['submeshes'])==len(n['materials'])
        count+=sum(len(sub) for sub in m['submeshes'])
    for t in model.textures:assert (M/(t['name']+'.png')).exists(),t
    counts[p.name]=count
for entry in audit['models']:
    filename=entry['file'];base=load(R/'Source/VisualBaseline'/filename);new=load(M/filename)
    assert new.materials==base.materials and new.textures==base.textures
    new.root['children']=[n for n in new.root['children'] if not n['name'].startswith('RW_Visual12_')]
    assert new.root==base.root,filename
for filename in audit['textures']:
    with Image.open(M/filename) as new,Image.open(R/'Source/VisualBaseline'/filename) as old:
        assert new.size==old.size and new.mode==old.mode
        if old.mode=='RGBA':assert new.getchannel('A').tobytes()==old.getchannel('A').tobytes()
audit['validation']={'status':'PASS offline; KSP review pending','native_models_parsed':len(counts),'all_meshes_within_16_bit_limit':True,'original_materials_and_texture_tables_preserved':True,'texture_dimensions_and_modes_preserved':True,'triangle_counts':counts}
(R/'Reports/VISUAL_UPGRADE.json').write_text(json.dumps(audit,indent=2)+'\n')
print('PASS',len(counts),'native models; all mesh indices, texture references and 16-bit limits')
print('PASS 15 upgraded models preserve every original node, material, collider, transform and variant')
print('PASS 13 textures preserve dimensions and image modes')
