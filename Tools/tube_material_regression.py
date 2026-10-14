from pathlib import Path
import hashlib
from native_model import load,walk
def check(root,path,expected):
    root=Path(root);oldpath=root/'Source/Balancing/TubeMaterialBefore'/Path(path).name
    assert hashlib.sha256(oldpath.read_bytes()).hexdigest()==expected
    old=load(oldpath);new=load(root/path)
    assert old.materials[-1]['name'].endswith('_elblabel')
    assert new.materials==old.materials[:-1] and new.textures==old.textures[:-1]
    assert new.root==old.root,'Tube loading fix changed geometry, indices, UVs or colliders'
    indices=[i for _,n in walk(new.root) for i in n.get('materials',[])]
    assert max(indices)+1==len(new.materials),'Trailing unused material would break KSPCF loading'
