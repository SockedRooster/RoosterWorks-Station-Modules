from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];OUT=R.parent/'outputs';OUT.mkdir(exist_ok=True)
assert 'PASS station dev.6:' in (R/'Reports/station-logistics-validation.log').read_text()
assert 'PASS station logistics compiled' in (R/'Reports/logistics-runtime-build.log').read_text()
for size in (250,375,500):assert 'PASS 1884 station-logistics' in (R/f'Reports/logistics-tests-{size}.log').read_text()
files=sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.blend1') and p.name not in ('logistics-package.log','LOGISTICS_PACKAGE_VALIDATION.json'))
docs={'README.md','INSTALLATION.md','RELEASE_NOTES.md','LICENSE','CHANGELOG.md','CHECKSUMS-SHA256.txt','STATION_LOGISTICS_BALANCE.md'}
install=[p for p in files if p.relative_to(R).parts[0]=='GameData' or p.relative_to(R).as_posix() in docs]
result={};payload=[]
for suffix,entries in (('TEST',install),('Developer-Source',files)):
 out=OUT/f'RoosterWorks-Station-Modules-v0.7.5-dev.6-{suffix}.zip'
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in entries:
   i=zipfile.ZipInfo(p.relative_to(R).as_posix(),(2026,10,16,12,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o644<<16;z.writestr(i,p.read_bytes(),compresslevel=9)
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  for name in z.namelist():
   assert z.read(name)==(R/name).read_bytes()
   if name.startswith('GameData/'):assert name.startswith('GameData/RoosterWorksStationModules/')
  for line in z.read('CHECKSUMS-SHA256.txt').decode().splitlines():
   digest,name=line.split('  ',1);assert hashlib.sha256(z.read(name)).hexdigest()==digest
  payload.append({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('GameData/')})
 result[out.name]={'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'files':len(entries)}
 print('PASS station archive CRC, exact files, manifest and scoped install folder:',out.name,flush=True)
assert payload[0]==payload[1]
(OUT/'RoosterWorks-Station-Modules-v0.7.5-dev.6-SHA256SUMS.txt').write_text(''.join(v['sha256']+'  '+k+'\n' for k,v in result.items()))
(R/'Reports/LOGISTICS_PACKAGE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
