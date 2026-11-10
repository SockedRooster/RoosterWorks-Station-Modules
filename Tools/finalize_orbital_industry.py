from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1];W=R.parent;OUT=W/'outputs'
for version in (10,11):
 for line in (OUT/f'RoosterWorks-Station-Modules-v0.7.5-dev.{version}-SHA256SUMS.txt').read_text().splitlines():
  digest,name=line.split('  ',1);assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==digest
note='''Latest station build: **rw-v075dev11 / v0.7.5-dev.11 TEST**, superseding dev.10.
Adds 2.5 m / 2.4 m-long orbital ISRU, NST, CEN and NSM, with supported matching
equipment on both sides, Y-axis station hulls, two size2 docking ends and Station
Utility placement. Same ground cargo/processing/thermal modules and positive
default empty prices (ISRU 14,000; NST 24,000; CEN 68,000; NSM 36,000).
Ground Modules optional; standalone feedstock definition gated off with Ground
Modules dev.26+ present. New docking-menu policy compiled against KSP; all old
station assets and DLLs preserved. 2,933 native/configuration checks, 14,912
actual-source color assertions and 3,708 docking/menu assertions pass; archives
verified. Live full-mod acceptance pending. 49 parts / 47 native models.
Editable source: Source/Blender/RW_OrbitalIndustry.blend. Guide ORBITAL_INDUSTRY.md;
actual-model previews Media/OrbitalIndustry/Family.png. Install/source ZIPs in
outputs/. Replace only Station Modules; Ground dev.28 is unchanged.

'''
p=W/'WORKSPACE_INDEX.md';t=p.read_text(encoding='utf-8-sig');start=t.index('Latest station build:');end=t.index('Latest ground build:',start);t=t[:start]+note+t[end:]
t=t.replace('| Station Modules | 0.7.5-dev.10 | 0.7.5-dev.9 | rw-v075dev10 / rw-v075dev9 |','| Station Modules | 0.7.5-dev.11 | 0.7.5-dev.10 | rw-v075dev11 / rw-v075dev10 |');p.write_text(t,encoding='utf-8')
p=W/'ROOSTERWORKS_DEVELOPMENT_CONTEXT.md';t=p.read_text(encoding='utf-8-sig');heading='# Current station build — October 17, 2026: dev.11 orbital industry\n\n'
if not t.startswith(heading):p.write_text(heading+note+t,encoding='utf-8')
removed=[]
for suffix in ('TEST.zip','Developer-Source.zip','SHA256SUMS.txt'):
 p=(OUT/('RoosterWorks-Station-Modules-v0.7.5-dev.9-'+suffix)).resolve()
 assert p.parent==OUT.resolve() and p.is_relative_to(W.resolve())
 if p.exists():removed.append({'path':p.relative_to(W).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()});p.unlink()
(OUT/'Station-dev11-retention.json').write_text(json.dumps({'kept':[11,10],'historical_source_baselines_retained':True,'removed':removed},indent=2)+'\n')
print('PASS retained dev.11/dev.10 archive hashes, workspace index and two-version station distribution retention')
