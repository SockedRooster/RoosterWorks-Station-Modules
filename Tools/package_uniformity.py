"""Package and verify the complete runtime and editable source candidate."""
from pathlib import Path
import hashlib,zipfile,json
R=Path(__file__).resolve().parents[1]
assert json.loads((R/'Reports/UNIFORMITY_04.json').read_text())['status'].startswith('PASS')
paths=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ('.build-deps','__pycache__')) and p.suffix not in ('.pyc','.blend1') and p.name!='CHECKSUMS-SHA256.txt')
(R/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in paths))
for kind in ('Install','Developer-Source'):
    target=R.parent/f'RoosterWorks-Uniformity-04-{kind}.zip'
    selected=paths+[R/'CHECKSUMS-SHA256.txt'] if kind=='Developer-Source' else [p for p in paths if p.is_relative_to(R/'GameData') or p.name in ('UNIFORMITY_04.md','UNIFORMITY_04.json')]
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in selected:z.write(p,p.relative_to(R).as_posix())
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for p in selected:assert hashlib.sha256(z.read(p.relative_to(R).as_posix())).digest()==hashlib.sha256(p.read_bytes()).digest(),str(p)
    print(target.name,round(target.stat().st_size/1024**2,1),'MiB; all files verified',flush=True)
