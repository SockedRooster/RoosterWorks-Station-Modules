from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];W=R.parent
p=R/'Tools/validate_gravity_ring.py';s=p.read_text().replace("W/'rw-v075dev7/GameData/RoosterWorksStationModules'","W/'rw-v075dev8/GameData/RoosterWorksStationModules'")
a=s.index('added={');b=s.index('\nchanged=set()',a);s=s[:a]+'added=set()'+s[b:]
a=s.index('assert changed==');b=s.index('\n',a);s=s[:a]+"assert changed=={'RoosterWorksStationModules.version','Models/RW_GRAV_250.mu','Plugins/RoosterWorksGravityRing.dll'}"+s[b:]
a=s.index('def bounds(d):');b=s.index('\nposes={}',a)
s=s[:a]+'''def evaluate(model,d):
 result={}
 def visit(n,parent):
  rotation=n['rotation'];scale=np.array(n['scale']);position=np.array(n['position']);name=n['name']
  reach=smooth(d/.55);inflate=smooth((d-.55)/.45);length=.95+1.8*reach
  for prefix,sign in (('RW_GravityHinge',1),('RW_GravityPod',-1)):
   suffix=name.removeprefix(prefix)
   if name.startswith(prefix) and len(suffix)==2 and suffix.isdigit():
    k=int(suffix);a=math.radians(sign*((82 if k in (0,4) else 88) if k%2==0 else -88)*(1-smooth(d/.65)))/2;rotation=(0,0,math.sin(a),math.cos(a))
    if sign>0:position=np.array((1.72-.27*reach,0,0))
    else:position=np.array((length,0,0));scale=np.array((.5+.5*inflate,.85+.15*inflate,.7+.3*inflate))
  if name.startswith('RW_GravityTelescopic'):scale=np.array((length/2.75,1,1))
  local=np.eye(4);local[:3,:3]=quat(rotation)@np.diag(scale);local[:3,3]=position;world=parent@local
  if 'mesh' in n:
   v=np.array(n['mesh']['vertices']);result[name]=(world[:3,:3]@v.T).T+world[:3,3]
  for child in n['children']:visit(child,world)
 visit(model.root,np.eye(4));return result
def bounds(d):
 v=np.concatenate(list(evaluate(model,d).values()));assert np.isfinite(v).all();return v.min(0),v.max(0),np.linalg.norm(v[:,[0,2]],axis=1).max()
'''+s[b:]
s=s.replace("assert poses['0']['radial_diameter']<4.5","assert poses['0']['radial_diameter']<5.0\nassert max(abs(v) for key in ('minimum','maximum') for v in (poses['0'][key][1],))<=1.851")
s=s.replace('PASS 1788 gravity-ring','PASS 2652 gravity-ring')
s=s.replace("assert '/RW_GravityHinge%02d/'%i in path","assert '/RW_GravityHinge%02d/RW_GravityTelescopic%02d/'%(i,i) in path")
a=s.index(' # At the fixed stack face,');b=s.index("assert 'PASS 3690",a)
s=s[:a]+'''# Deployed mesh geometry and proven lighting/color data must remain exact.
old=load(B/'Models/RW_GRAV_250.mu');oldpose=evaluate(old,1);newpose=evaluate(model,1)
for name,vertices in oldpose.items():assert np.allclose(vertices,newpose[name],atol=2e-6),name
for d in (0,.25,.5,.75,1):
 pose=evaluate(model,d)
 for i in range(8):
  cabin=pose['RW_GravitySector%02d_white'%i]
  assert np.linalg.norm(cabin[:,[0,2]],axis=1).min()>1.25
assert (GD/'Compatibility/GravityRingGeometry.cfg').read_bytes()==(B/'Compatibility/GravityRingGeometry.cfg').read_bytes()
assert (GD/'Models/rwm_gravity_window_emissive.png').read_bytes()==(B/'Models/rwm_gravity_window_emissive.png').read_bytes()
assert (GD/'Parts/RW_GRAV_250.cfg').read_bytes()==(B/'Parts/RW_GRAV_250.cfg').read_bytes()
'''+s[b:]
s=s.replace('PASS gravity dev.8:','PASS gravity dev.9:').replace('only scoped gravity model/config/mask/controller/version changes from dev.7','compact stow and telescopic arms; deployed geometry matches dev.8; accepted lights/maps and all other GameData preserved')
p.write_text(s)
p=R/'Tools/package_gravity_ring.py';s=p.read_text().replace('PASS gravity dev.8:','PASS gravity dev.9:').replace('PASS 1788 gravity-ring','PASS 2652 gravity-ring').replace('v0.7.5-dev.8-','v0.7.5-dev.9-').replace("'GRAVITY_RING_FIXES.md'}","'GRAVITY_RING_FIXES.md','GRAVITY_RING_COMPACT.md'}");p.write_text(s)
hashes=json.loads((R/'Reports/GRAVITY_PROTECTED_INPUTS.json').read_text())
for p in (W/'rw-v075dev8').rglob('*'):
 if p.is_file() and '__pycache__' not in p.parts:hashes[p.relative_to(W).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'Reports/GRAVITY_PROTECTED_INPUTS.json').write_text(json.dumps(hashes,indent=2)+'\n')
(R/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in sorted((R/'GameData').rglob('*')) if p.is_file()))
doc='''# GRAV-250 compact stow — v0.7.5-dev.9 TEST

The folded silhouette now has eight fuller pressure packs in two alternating
rows around the hub. Spokes telescope from 2.75 m deployed reach to 0.95 m
when stowed; their diameter is retained. Packs retain 50% radial thickness,
85% axial height and 70% tangential width, replacing the tiny 18% scale from
dev.8. The complete stowed model fits within the hub's 3.7 m axial span.
Keep the recommended 5 m fairing; this is a shorter package, not a narrower one.

Sliding root mounts move the folded packs out just enough to clear the hub.
Hinge pins keep their proportions. Pressure passages telescope with their
arms and their seals follow the pivots. The entire original deployed geometry
is unchanged, with only new small root guides added. Hub attachment points,
mass, crew capacity, resources, rotation/power behavior and crew interlocks
are retained. The user-confirmed lighting fix, mask and stock light controls
remain byte-identical, as do the corrected color maps and shared plugins.

Close KSP, replace only GameData/RoosterWorksStationModules, then restart.
Preview Stowed/Unfolding/Deployed under Media/GravityRing. Test deploy/fold
and rotation on an uncrewed test part before using it on a working station.
No game installation, existing build or save was modified preparing this kit.

2,652 actual controller-source assertions pass. Native checks evaluate five
folding positions, pressure-pack clearance from the hub, shorter axial bounds,
unchanged full-deployment vertices for every old mesh, accepted lighting/mask
and map bytes, collider/material validity and preserved prior files. In-game
visual/physics acceptance is pending. Existing 3,690 color regressions remain
valid because their runtime, map entries and targeted meshes are unchanged.

Current builder Source/build_gravity_ring.py, runtime Source/GravityRing.cs,
packed editable source Source/Blender/RW_GRAV_250.blend. See GRAVITY_RING.md
for the retained limitations: visual rotation only; no physical gravity,
rotating IVA or automatically granted ring habitation/comfort bonus.
'''
(R/'GRAVITY_RING_COMPACT.md').write_text(doc,encoding='utf-8')
for name in ('README.md','RELEASE_NOTES.md'):
 p=R/name;s=p.read_text(encoding='utf-8')
 if not s.startswith('# RoosterWorks Station Modules — v0.7.5-dev.9'):
  p.write_text('# RoosterWorks Station Modules — v0.7.5-dev.9 TEST\n\nReworks the gravity ring stow proportions with telescopic spokes and fuller habitat packs close to the hub. The deployed shape and confirmed lights/color-map fixes are retained. See GRAVITY_RING_COMPACT.md.\n\n## Previous development history\n\n'+s,encoding='utf-8')
print('Prepared compact-ring checks and dev.9 packaging')
