from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'Source'),str(R/'Tools')]
from native_model import load,walk
from config_nodes import parse
GD=R/'GameData/RoosterWorksStationModules'
m=load(GD/'Models/RW_GRAV_250.mu');nodes=dict(walk(m.root));maps=parse((GD/'Compatibility/GravityRingGeometry.cfg').read_text()).children[0]
fixture=[]
for spec in maps.children:
 n=nodes[spec.get('path')];fixture.append({'path':spec.get('path'),'texture':spec.get('texture'),'vertexCount':len(n['mesh']['vertices']),'triangles':[i for t in n['mesh']['submeshes'][0] for i in t],'ranges':spec.get('ranges')})
(R/'Reports/GRAVITY_COLOR_FIXTURE.json').write_text(json.dumps(fixture,indent=2)+'\n')
old=(R/'Tools/test-customization.ps1').read_text();doubles=old.split("$doubles = @'\n",1)[1].split('public static class CustomizationTest {',1)[0]
(R/'Tools/GravityColorDoubles.cs').write_text(doubles)
hashes=json.loads((R/'Reports/GRAVITY_PROTECTED_INPUTS.json').read_text())
for p in (R.parent/'rw-v075dev7').rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts:hashes[p.relative_to(R.parent).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'Reports/GRAVITY_PROTECTED_INPUTS.json').write_text(json.dumps(hashes,indent=2)+'\n')
(R/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in sorted((R/'GameData').rglob('*')) if p.is_file()))
print('Prepared actual native ring-map fixture, runtime doubles and protected hashes')
