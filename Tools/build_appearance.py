"""Build v0.6.0 native models and editable OBJ assets, preserving gameplay; rounded HUB colliders match its revised body.

Run this family entry point instead of old individual texture generators.
Pillow and NumPy are the only extra dependencies; no Unity or VTK needed.
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
import build_hab250 as h
import build_lab250 as lab
import build_cmd250 as cmd
import build_hub250 as hub
import build_cup250 as cup
import build_log250 as log
from appearance_textures import finish

def main():
    groups=h.generate_groups()
    h.create_mu(groups,h.MODELS/'RW_HAB_250.mu')
    for variant,filename in [('WindowBankStandard','RW_HAB_250'),('SideHatch','RW_HAB_250_SideHatch')]:
        h.create_obj(h.combine_meshes(groups['Base'],groups[variant]),ROOT/f'Source/Blender/{filename}.obj')
    for b in (lab,cmd):
        m=b.geometry();b.create_native_mu(m,b.MODELS/f'{b.PART}.mu')
        b.create_obj(m,ROOT/f'Source/Blender/{b.PART}.obj')
    m=hub.geometry();hub.create_mu(m)
    previous=cmd.MAT
    cmd.MAT=hub.MAT
    cmd.create_obj(m,ROOT/'Source/Blender/RW_HUB_250.obj')
    cmd.MAT=previous
    m=cup.geometry();cup.write_mu(m);cup.write_obj(m)
    m=log.geometry();log.create_mu(m);log.create_obj(m)
    finish()
    from build_air250 import build as build_air
    build_air()
    from build_pwr250 import build as build_power
    build_power()
    from build_adp250375 import build as build_adapter
    build_adapter()
    from build_grn250 import build as build_greenhouse
    build_greenhouse()
    from build_family375 import build as build_large_family
    build_large_family()
    from electric_charge_balance import apply as apply_ec_balance
    apply_ec_balance()
    from build_crew_tubes import build as crew_tubes
    crew_tubes()
    from build_options import build as build_options
    build_options()
    version_path=ROOT/'GameData/RoosterWorksStationModules/RoosterWorksStationModules.version'
    version=json.loads(version_path.read_text());version['VERSION']={'MAJOR':0,'MINOR':6,'PATCH':0,'BUILD':0}
    version_path.write_text(json.dumps(version,indent=2)+'\n')
    files=sorted(p for p in (ROOT/'GameData').rglob('*') if p.is_file())
    (ROOT/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(ROOT).as_posix()+'\n' for p in files))
    print('Built nineteen native models, both HAB variants, OBJ/MTL and GameData manifest')

if __name__=='__main__':main()
