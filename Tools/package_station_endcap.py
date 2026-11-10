from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];OUT=R.parent/'outputs';OUT.mkdir(exist_ok=True)
assert 'PASS station endcap dev.10: 2055 checks' in (R/'Reports/station-endcap-validation.log').read_text()
assert 'PASS 3728 actual-map color assertions' in (R/'Reports/endcap-color-tests.log').read_text()
log=(R/'Reports/station-endcap-render.log').read_text()
for text in ('PASS packed editable station endcap','PASS rendered station endcap Nose','PASS rendered station endcap Base'):assert text in log
assert (R/'Source/Blender/RW_END_250_125.blend').stat().st_size>100000
for name in ('Nose','Base'):assert (R/f'Media/StationEndcap/{name}.png').stat().st_size>50000
files=sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.blend1') and p.name not in ('station-endcap-package.log','STATION_ENDCAP_PACKAGE_VALIDATION.json'))
docs={'README.md','INSTALLATION.md','RELEASE_NOTES.md','LICENSE','CHANGELOG.md','ROADMAP.md','CHECKSUMS-SHA256.txt','STATION_LOGISTICS_BALANCE.md','GRAVITY_RING.md','GRAVITY_RING_FIXES.md','GRAVITY_RING_COMPACT.md','ROUNDED_STATION_ENDCAP.md'}
install=[p for p in files if p.relative_to(R).parts[0]=='GameData' or p.relative_to(R).as_posix() in docs or p.relative_to(R).as_posix().startswith(('Media/GravityRing/','Media/StationEndcap/'))]
results={};payloads=[]
for suffix,entries in (('TEST',install),('Developer-Source',files)):
 out=OUT/f'RoosterWorks-Station-Modules-v0.7.5-dev.10-{suffix}.zip'
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
  payloads.append({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('GameData/')})
 results[out.name]={'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'files':len(entries)}
 print('PASS station endcap archive CRC, source bytes, manifest and scoped Station Modules install:',out.name,flush=True)
assert payloads[0]==payloads[1]
(OUT/'RoosterWorks-Station-Modules-v0.7.5-dev.10-SHA256SUMS.txt').write_text(''.join(v['sha256']+'  '+k+'\n' for k,v in results.items()))
(R/'Reports/STATION_ENDCAP_PACKAGE_VALIDATION.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
