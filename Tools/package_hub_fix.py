from pathlib import Path
import hashlib,json,zipfile
R=Path(__file__).resolve().parents[1];GD=R/'GameData/RoosterWorksStationModules'
assert json.loads((R/'Reports/HUB_ROUTING_06.json').read_text())['status'].startswith('PASS')
baseline=json.loads((R/'Source/Study05Baseline/runtime_sha256.json').read_text())
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in p.parts for x in ('.build-deps','__pycache__')) and p.suffix not in ('.pyc','.blend1') and p.name!='CHECKSUMS-SHA256.txt')
(R/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in files))
runtime=[p for p in files if p.is_relative_to(GD)]
changed=[p for p in runtime if hashlib.sha256(p.read_bytes()).hexdigest()!=baseline.get(p.relative_to(GD).as_posix())]
for kind in ('Patch','Install','Developer-Source'):
    selected=(changed if kind=='Patch' else runtime)+[R/'HUB_ROUTING_06.md',R/'Reports/HUB_ROUTING_06.json'] if kind!='Developer-Source' else files+[R/'CHECKSUMS-SHA256.txt']
    target=R.parent/f'RoosterWorks-Hub-Routing-06-{kind}.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in selected:z.write(p,p.relative_to(R).as_posix())
    with zipfile.ZipFile(target) as z:
        assert z.testzip() is None
        for p in selected:assert hashlib.sha256(z.read(p.relative_to(R).as_posix())).digest()==hashlib.sha256(p.read_bytes()).digest()
    print(target.name,round(target.stat().st_size/1024**2,1),'MiB; all files verified',flush=True)
print('Changed runtime files:',*[p.relative_to(GD).as_posix() for p in changed],sep='\n')
