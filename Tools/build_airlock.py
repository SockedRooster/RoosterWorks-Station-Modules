"""Add AIR to the accepted six-module package without rebuilding old assets."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from build_air250 import build
build()
from electric_charge_balance import apply as apply_ec_balance
apply_ec_balance()
p=ROOT/'GameData/RoosterWorksStationModules/RoosterWorksStationModules.version'
v=json.loads(p.read_text());v['VERSION']={'MAJOR':0,'MINOR':6,'PATCH':0,'BUILD':0};p.write_text(json.dumps(v,indent=2)+'\n')
from build_options import build as build_options
build_options()
files=sorted(p for p in (ROOT/'GameData').rglob('*') if p.is_file())
(ROOT/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
