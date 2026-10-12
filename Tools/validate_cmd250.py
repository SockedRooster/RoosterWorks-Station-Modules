#!/usr/bin/env python3
"""Static geometry, native model and game-config tests for RW-CMD-250 v0.4.1."""
from pathlib import Path
import sys, math,struct
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
from build_cmd250 import geometry,MAT,MODELS,PART,HEIGHT
part=(ROOT/'GameData/RoosterWorksStationModules/Parts/RW_CMD_250.cfg').read_text()
patch=(ROOT/'GameData/RoosterWorksStationModules/Compatibility/CommandKerbalism.cfg').read_text()
for text in [part,patch]:assert text.count('{')==text.count('}')
for tok in ('name = RW_CMD_250','CrewCapacity = 2','mass = 2.2','node_stack_top = 0, 0.860',
            'node_stack_bottom = 0, -0.860','name = ModuleCommand','minimumCrew = 0',
            'name = ModuleSAS','SASServiceLevel = 2','name = ModuleReactionWheel',
            'name = ModuleDataTransmitter','antennaPower = 5000000',
            'name = ModuleColorChanger','includedRenderer = RW_CmdGlass',
            'defaultActionGroup = Light','name = ElectricCharge','maxAmount = 2400'):
    assert tok in part,tok
# v0.4.1: exercise the actual control/communications configuration.
# A DIRECT radio alone is not a substitute for a built-in INTERNAL
# telemetry antenna on a probe-capable command pod.
assert part.count('name = ModuleCommand') == 1, 'Expected exactly one primary command module'
assert part.count('name = ModuleDataTransmitter') == 2, 'Require internal and direct radio'
assert 'antennaType = INTERNAL' in part and 'antennaType = DIRECT' in part
assert 'antennaPower = 500000' in part and 'antennaPower = 5000000' in part
assert 'requiresPilot = false' in part
assert 'remoteControl = true' in part
assert 'requiresTelemetry = true' in part, 'Uncrewed operation must continue requiring a real comms link'
assert 'name = ModuleProbeControlPoint' in part and 'minimumCrew = 1' in part and 'multiHop = True' in part
assert 'hasHibernation = false' in part
assert 'hasHibernation = True' not in part

for res in ('Food','Water','Oxygen','Nitrogen','Waste','WasteWater'):
    assert '%RESOURCE['+res+']' in patch
    assert 'name = '+res not in part
assert ':NEEDS[Kerbalism,FeatureHabitat]' in patch
assert '%MODULE[Habitat]' in patch
assert 'name = mk2CockpitStandardInternals' in part
mu=(MODELS/f'{PART}.mu').read_bytes()
assert struct.unpack_from('<ii',mu)==(76543,5) and len(mu)>120000
for name in (b'RW_CMD_250',b'RW_CmdGlass',b'CmdFlushEndcapTop',b'CmdFlushEndcapBottom',
             b'rwm_cmdlabel',b'rwm_display',b'KSP/Emissive/Diffuse'):
    assert name in mu,name
for key in list(MAT)+['cabin_emissive']:
    im=MODELS/f'rwm_{key}.png'
    assert im.is_file() and im.read_bytes().startswith(b'\x89PNG\r\n\x1a\n')
meshes=geometry()
tri=sum(len(v.triangles) for v in meshes.values())
assert 4500<tri<26000,tri
for mat,m in meshes.items():
    assert len(m.vertices)==len(m.uvs)==len(m.normals)
    assert len(m.vertices)<65535
    assert all(all(0<=i<len(m.vertices) for i in t) for t in m.triangles)
verts=[p for m in meshes.values() for p in m.vertices]
assert all(-HEIGHT/2-1e-6 <= y <= HEIGHT/2+1e-6 for x,y,z in verts), (min(y for x,y,z in verts),max(y for x,y,z in verts))
maxr=max(math.hypot(x,z) for x,y,z in verts)
assert 1.20<maxr<1.33,maxr
assert len(meshes['glass'].triangles)==5*8
for rel in ('Source/Blender/RW_CMD_250.obj','Source/Blender/RW_CMD_250.mtl','Source/Blender/create_cmd250.py'):
    assert (ROOT/rel).is_file(),rel
print(f'PASS RW-CMD-250: 2.5m by {HEIGHT}m, {tri} triangles, five windows')
print('PASS command/no-hibernation, INTERNAL + DIRECT telemetry, station control point, SAS, reaction wheel and lights configured')
print('PASS Kerbalism supplies/habitat conditional and stock-friendly')
print('NOTE: Real flight controls, Kerbalism and 2-seat stock IVA need in-game verification')
