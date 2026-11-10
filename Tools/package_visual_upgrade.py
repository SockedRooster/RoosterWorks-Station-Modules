"""Package current visual source and ready-to-install GameData with checksums."""
from pathlib import Path
import hashlib,zipfile
R=Path(__file__).resolve().parents[1]
def eligible(p):return p.is_file() and not any(x in p.parts for x in ('.build-deps','__pycache__')) and p.suffix not in ('.pyc','.blend1')
paths=sorted(p for p in R.rglob('*') if eligible(p) and p.name!='CHECKSUMS-SHA256.txt')
(R/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in paths))
for kind in ('Install','Developer-Source'):
    target=R.parent/f'RoosterWorks-Visual-Development-01-{kind}.zip'
    selected=paths+[R/'CHECKSUMS-SHA256.txt'] if kind=='Developer-Source' else [p for p in paths if p.is_relative_to(R/'GameData') or p.name=='VISUAL_UPGRADE.md']
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in selected:z.write(p,p.relative_to(R).as_posix())
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        assert 'GameData/RoosterWorksStationModules/Models/RW_HAB_250.mu' in z.namelist()
    print(target.name,round(target.stat().st_size/1024**2,1),'MiB; archive integrity PASS',flush=True)
