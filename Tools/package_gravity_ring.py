from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];OUT=R.parent/'outputs';OUT.mkdir(exist_ok=True)
assert 'PASS gravity dev.9:' in (R/'Reports/gravity-validation.log').read_text()
assert 'PASS 2652 gravity-ring' in (R/'Reports/gravity-tests.log').read_text()
assert 'PASS gravity-ring controller compiled' in (R/'Reports/gravity-runtime-build.log').read_text()
assert 'PASS rendered gravity ring Deployed' in (R/'Reports/gravity-render.log').read_text()
assert (R/'Source/Blender/RW_GRAV_250.blend').stat().st_size>100000
for label in ('Stowed','Unfolding','Deployed'):assert (R/f'Media/GravityRing/{label}.png').stat().st_size>50000
files=sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.blend1') and p.name not in ('gravity-package.log','GRAVITY_PACKAGE_VALIDATION.json'))
docs={'README.md','INSTALLATION.md','RELEASE_NOTES.md','LICENSE','CHANGELOG.md','CHECKSUMS-SHA256.txt','STATION_LOGISTICS_BALANCE.md','GRAVITY_RING.md','GRAVITY_RING_FIXES.md','GRAVITY_RING_COMPACT.md'}
install=[p for p in files if p.relative_to(R).parts[0]=='GameData' or p.relative_to(R).as_posix() in docs or p.relative_to(R).as_posix().startswith('Media/GravityRing/')]
assert 'PASS 3690 actual-map color' in (R/'Reports/gravity-color-tests.log').read_text()
result={};payload=[]
for suffix,entries in (('TEST',install),('Developer-Source',files)):
 out=OUT/f'RoosterWorks-Station-Modules-v0.7.5-dev.9-{suffix}.zip'
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
 print('PASS gravity archive CRC, native files, manifest and scoped install folder:',out.name,flush=True)
assert payload[0]==payload[1]
(OUT/'RoosterWorks-Station-Modules-v0.7.5-dev.9-SHA256SUMS.txt').write_text(''.join(v['sha256']+'  '+k+'\n' for k,v in result.items()))
(R/'Reports/GRAVITY_PACKAGE_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
