"""Rebuild only new 0.7/0.75 parts from retained native/procedural source.

For a full original family refresh run build_appearance.py first, then this.
Existing original part IDs/assets remain protected by expansion_baseline.json.
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from build_family500 import build as family500
from build_short_habitats import build as short_habs
from build_ring_options import build as rings
from build_logistics_options import build as logistics
from build_long_tubes import build as long_tubes
from build_editor_options import build as editor_options
from build_command_storage import build as command_storage
def main():
    family500()
    version=json.loads((ROOT/'GameData/RoosterWorksStationModules/RoosterWorksStationModules.version').read_text())['VERSION']
    if version['MINOR']==7 and version['PATCH']>=5:short_habs()
    if version['MINOR']==7 and version['PATCH']>=5 and version.get('BUILD',0)>=2:
        long_tubes();editor_options()
    if version.get("BUILD",0)>=4:command_storage()
    rings();logistics()
    files=sorted(p for p in (ROOT/'GameData').rglob('*') if p.is_file())
    (ROOT/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
if __name__=='__main__':main()
