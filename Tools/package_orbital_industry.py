from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];OUT=R.parent/'outputs';OUT.mkdir(exist_ok=True)
assert 'PASS orbital industry dev.11: 2933 ' in (R/'Reports/orbital-industry-validation.log').read_text()
assert 'PASS 3708 docking/menu assertions' in (R/'Reports/orbital-docking-tests.log').read_text()
for role in ('ISRU','NST','CEN','NSM'):
 assert 'PASS 3728 actual-map color assertions' in (R/f'Reports/orbital-{role.lower()}-colors.log').read_text()
 assert 'PASS rendered orbital '+role in (R/'Reports/orbital-industry-render.log').read_text()
 assert (R/f'Media/OrbitalIndustry/{role}.png').stat().st_size>50000
assert 'PASS rendered orbital ISRU' in (R/'Reports/orbital-isru-refined-render.log').read_text()
assert (R/'Source/Blender/RW_OrbitalIndustry.blend').stat().st_size>1000000
assert (R/'Media/OrbitalIndustry/Family.png').exists()
files=sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.blend1') and p.name not in ('orbital-industry-package.log','ORBITAL_INDUSTRY_PACKAGE_VALIDATION.json'))
docs={'README.md','INSTALLATION.md','RELEASE_NOTES.md','LICENSE','CHANGELOG.md','ROADMAP.md','CHECKSUMS-SHA256.txt','STATION_LOGISTICS_BALANCE.md','GRAVITY_RING.md','GRAVITY_RING_FIXES.md','GRAVITY_RING_COMPACT.md','ROUNDED_STATION_ENDCAP.md','ORBITAL_INDUSTRY.md'}
install=[p for p in files if p.relative_to(R).parts[0]=='GameData' or p.relative_to(R).as_posix() in docs or p.relative_to(R).as_posix().startswith(('Media/GravityRing/','Media/StationEndcap/','Media/OrbitalIndustry/'))]
results={};payloads=[]
for suffix,entries in (('TEST',install),('Developer-Source',files)):
 out=OUT/f'RoosterWorks-Station-Modules-v0.7.5-dev.11-{suffix}.zip'
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in entries:
   i=zipfile.ZipInfo(p.relative_to(R).as_posix(),(2026,10,17,12,0,0));i.compress_type=zipfile.ZIP_DEFLATED;i.external_attr=0o644<<16;z.writestr(i,p.read_bytes(),compresslevel=9)
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  for name in z.namelist():
   assert z.read(name)==(R/name).read_bytes()
   if name.startswith('GameData/'):assert name.startswith('GameData/RoosterWorksStationModules/')
  assert len([n for n in z.namelist() if n.startswith('GameData/') and '/Parts/' in n and n.endswith('.cfg')])==49
  assert len([n for n in z.namelist() if n.startswith('GameData/') and n.endswith('.mu')])==47
  for line in z.read('CHECKSUMS-SHA256.txt').decode().splitlines():
   digest,name=line.split('  ',1);assert hashlib.sha256(z.read(name)).hexdigest()==digest
  payloads.append({n:hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('GameData/')})
 results[out.name]={'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'files':len(entries)}
 print('PASS orbital industry archive CRC, exact bytes, 49 parts / 47 models, manifest and scoped Station Modules install:',out.name,flush=True)
assert payloads[0]==payloads[1]
(OUT/'RoosterWorks-Station-Modules-v0.7.5-dev.11-SHA256SUMS.txt').write_text(''.join(v['sha256']+'  '+k+'\n' for k,v in results.items()))
(R/'Reports/ORBITAL_INDUSTRY_PACKAGE_VALIDATION.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
