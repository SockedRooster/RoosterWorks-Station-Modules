#!/usr/bin/env python3
"""Validate all HAB, LAB and CMD prototypes without launching KSP."""
from pathlib import Path
import subprocess,sys,hashlib
ROOT=Path(__file__).resolve().parents[1]
for f in ('validate_hab250.py','validate_lab250.py','validate_cmd250.py','validate_eva_airlock.py','validate_runtime_candidate.py','validate_hab_clearance.py','validate_eva_ladder.py','validate_hub250.py','validate_shared_endcaps.py','validate_cup250.py'):
    subprocess.run([sys.executable,str(ROOT/'Tools'/f)],check=True)
manifest=ROOT/'CHECKSUMS-SHA256.txt'
seen=set()
for line in manifest.read_text().splitlines():
    if not line.strip() or line.startswith('#'):continue
    digest,path=line.split('  ',1)
    assert path not in seen;seen.add(path)
    target=ROOT/path
    assert target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest()==digest,'Manifest mismatch '+path
actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'GameData').rglob('*') if p.is_file()}
assert actual==seen,(actual-seen,seen-actual)
print('PASS manifest: %d GameData files'%len(seen))
