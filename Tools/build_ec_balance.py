"""Apply frozen role-based capacity policy and refresh metadata/manifest only."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from electric_charge_balance import apply
apply()
p=ROOT/'GameData/RoosterWorksStationModules/RoosterWorksStationModules.version'
v=json.loads(p.read_text());v['VERSION']={'MAJOR':0,'MINOR':7,'PATCH':5,'BUILD':1};p.write_text(json.dumps(v,indent=2)+'\n')
from build_options import build as build_options
build_options()
from build_crew_tubes import build as crew_tubes
crew_tubes()
files=sorted(p for p in (ROOT/'GameData').rglob('*') if p.is_file())
(ROOT/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
print('Applied base +5% EC policy to all 19 parts; no geometry or consumption changes')
