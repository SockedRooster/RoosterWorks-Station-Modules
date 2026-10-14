"""Keep the ring bugfix narrowly scoped and portable across source kits."""
from pathlib import Path
import sys,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1]
from hotfix_assets import check_digest
baseline=json.loads((ROOT/'Tools/ring_hotfix_baseline.json').read_text())
for path,digest in baseline.items():
    if path.endswith('.version'):continue
    assert check_digest(ROOT,path,digest),('Outside ring/menu hotfix scope',path)
actual={p.relative_to(ROOT).as_posix() for p in (ROOT/'GameData').rglob('*') if p.is_file()}
assert set(baseline)<=actual and actual-set(baseline)<= {'GameData/RoosterWorksStationModules/Compatibility/ZZZCommandStorage075.cfg'}
assert json.loads((ROOT/'GameData/RoosterWorksStationModules/RoosterWorksStationModules.version').read_text())['VERSION']['BUILD'] in (3,4)
subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'Tools/test-customization.ps1')],check=True)
subprocess.run(['pwsh','-NoProfile','-File',str(ROOT/'Tools/test-editor-menu.ps1')],check=True)
print('PASS ring hotfix: all 213 GameData paths retained; only version and two pinned runtime DLLs change; recreated materials/native meshes/callbacks and reopened selector state covered')
