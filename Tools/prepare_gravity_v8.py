from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'Tools/validate_gravity_ring.py';s=p.read_text().replace("W/'rw-v075dev6/GameData/RoosterWorksStationModules'","W/'rw-v075dev7/GameData/RoosterWorksStationModules'")
a=s.index('added={');b=s.index('\nchanged=set()',a);s=s[:a]+"added={'Models/rwm_gravity_window_emissive.png'}"+s[b:]
s=s.replace("assert changed=={'RoosterWorksStationModules.version'}","assert changed=={'RoosterWorksStationModules.version','Models/RW_GRAV_250.mu','Parts/RW_GRAV_250.cfg','Compatibility/GravityRingGeometry.cfg','Plugins/RoosterWorksGravityRing.dll'}")
s=s.replace("sign*(88 if k%2==0 else -88)","sign*((82 if k in (0,4) else 88) if k%2==0 else -88)")
s=s.replace("'0-'+str(len(n['mesh']['submeshes'][0])-1)","'0:'+str(len(n['mesh']['submeshes'][0]))")
s=s.replace("print('PASS gravity dev.7:","print('PASS gravity dev.8:").replace('all dev.6 GameData unchanged except version','only scoped gravity model/config/mask/controller/version changes from dev.7')
# Strong checks for the actual reported defects and pressure passages.
extra='''
from PIL import Image
glass=model.materials[next(n['materials'][0] for n in byname.values() if n['name']=='RW_GravitySector00_glass')]
assert glass['shader']=='KSP/Emissive/Diffuse'
mask=model.textures[glass['properties']['_Emissive']['index']]['name']
assert mask=='rwm_gravity_window_emissive'
assert Image.open(GD/'Models'/ (mask+'.png')).convert('RGB').getextrema()==((255,255),(255,255),(255,255))
assert next(n for n in lights.children if n.header=='alphaCurve').values==[('key','0 1'),('key','1 1')]
for i in (0,4):
 name='RW_GravityAccessTube%02d'%i
 path=next(p for p,n in nodes.items() if n['name']==name)
 assert '/RW_GravityHinge%02d/'%i in path
 assert np.isclose(np.array(byname[name]['mesh']['vertices'])[:,0].min(),-.1)
 assert np.isclose(np.array(byname[name]['mesh']['vertices'])[:,0].max(),2.75)
 assert 'RW_GravityAccessRotarySeal%02d'%i in byname
 assert 'RW_GravityAccessCollision%02d'%i in byname
 # At the fixed stack face, the folded box clears an attached 2.5 m module.
 angle=math.radians(82)
 points=np.array([(1.45+x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle),z) for x in np.linspace(-.1,2.75,150) for y in np.linspace(-.38,.38,20) for z in (-.38,0,.38)])
 outside=points[points[:,1]>=1.85]
 assert np.linalg.norm(outside[:,[0,2]],axis=1).min()>1.25
assert 'PASS 3690 actual-map color' in (R/'Reports/gravity-color-tests.log').read_text()
'''
marker="for line in (R/'CHECKSUMS-SHA256.txt').read_text().splitlines():"
if 'from PIL import Image' not in s:s=s.replace(marker,extra+'\n'+marker)
p.write_text(s)
p=R/'Tools/package_gravity_ring.py';s=p.read_text().replace('PASS gravity dev.7:','PASS gravity dev.8:').replace('v0.7.5-dev.7-','v0.7.5-dev.8-')
if "assert 'PASS 3690" not in s:s=s.replace("result={};payload=[]","assert 'PASS 3690 actual-map color' in (R/'Reports/gravity-color-tests.log').read_text()\nresult={};payload=[]")
p.write_text(s)
doc='''# GRAV-250 corrections — v0.7.5-dev.8 TEST

- Fixed the console FormatException in ModuleRWRingColor.Bind. The generated
  map used 0-255; the established runtime requires start:count, e.g. 0:256.
  All four new map entries now use that grammar. The existing shared color
  plugin remains byte-identical, protecting other station/ground ring controls.
- Gave all eight window banks a dedicated full-white emission mask. The old
  HAB mask depended on HAB UVs and did not match the ring's torus UVs. Added an
  explicit opaque alpha curve to the stock Ring Lights control. Existing
  On/Off and Lights action-group behavior remains; no new lighting plugin.
- Added two opposed enclosed pressure-access tubes from the rotary hub to
  the perimeter, with bands, pivot seals and colliders. They fold with their
  spokes and rotate with the ring. Their stow angles allow clearance around
  a 2.5 m inline module. The assembly still needs a 5 m launch fairing.

Replace only GameData/RoosterWorksStationModules while KSP is closed, then
restart. Test ring color changes/reopening, lights off/on, full folding and
rotation. Existing saved light-off states remain off until switched on.
No installation or saves were modified preparing this build.

The console spam was our map-generation bug. It is distinct from the earlier
native crash stack in Parallax.CollisionManager.RemoveQueuedData. This update
does not change Parallax or include the separate collision diagnostic.

3,690 source-aware color assertions reproduce the old FormatException, then
test the corrected actual maps with all colors/reopens/native resets. 1,788
rotation/folding assertions pass. Native validation checks emission-mask
coverage, light targets/curves, mesh normals/colliders, passage ownership and
fixed-node clearance in addition to five fold poses and preservation hashes.
Full in-game visual/physics confirmation remains pending.

Current source: Source/build_gravity_ring.py, Source/GravityRing.cs and
Source/Blender/RW_GRAV_250.blend. Helpers: Tools/prepare_gravity_fixes.py,
Tools/test-gravity-colors.ps1, Tools/test-gravity-ring.ps1,
Tools/validate_gravity_ring.py. Preview Media/GravityRing/Deployed.png.
The general gravity-ring limitations remain described in GRAVITY_RING.md:
visual rotation only; no physical gravity, rotating IVA or extra habitat bonus.
'''
(R/'GRAVITY_RING_FIXES.md').write_text(doc,encoding='utf-8')
for name in ('README.md','RELEASE_NOTES.md'):
 p=R/name;s=p.read_text(encoding='utf-8')
 if not s.startswith('# RoosterWorks Station Modules — v0.7.5-dev.8'):
  p.write_text('# RoosterWorks Station Modules — v0.7.5-dev.8 TEST\n\nCorrects the GRAV-250 color-map FormatException and window emission, and adds two folding pressure-access tubes from hub to ring. See GRAVITY_RING_FIXES.md. Station logistics, other models and shared appearance plugins are unchanged.\n\n## Previous development history\n\n'+s,encoding='utf-8')
p=R/'Tools/package_gravity_ring.py';s=p.read_text().replace("'GRAVITY_RING.md'}","'GRAVITY_RING.md','GRAVITY_RING_FIXES.md'}");p.write_text(s)
print('Prepared dev.8 documentation and stronger regression/package gates')
