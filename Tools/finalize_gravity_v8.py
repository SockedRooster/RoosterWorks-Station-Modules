from pathlib import Path
R=Path(__file__).resolve().parents[1];W=R.parent
p=R/'GRAVITY_RING.md';s=p.read_text(encoding='utf-8')
if not s.startswith('Current corrections:'):
 p.write_text('Current corrections: v0.7.5-dev.8 — see GRAVITY_RING_FIXES.md. Includes two pressure-access tubes and their wider, slightly angled stow geometry (5 m fairing recommended), corrected color-map format and dedicated window emission mask. Previous design notes below.\n\n'+s,encoding='utf-8')
p=R/'ROADMAP.md';s=p.read_text(encoding='utf-8')
if '## GRAV-250 dev.8 corrections' not in s:p.write_text(s+'\n## GRAV-250 dev.8 corrections\n\nCorrected ring-map format and window emission; added opposed folding pressure-access passages. Advanced gravity and rotating IVA remain future work.\n',encoding='utf-8')
p=W/'WORKSPACE_INDEX.md';s=p.read_text(encoding='utf-8');start=s.index('Latest station build:');end=s.index('Latest ground build:',start)
s=s[:start]+'''Latest station build: **rw-v075dev8 / v0.7.5-dev.8 TEST**. GRAV-250 now has
two opposed folding access tubes, a dedicated window-emission mask/alpha curve
and corrected start:count ring-map ranges. The bad dev.7 hyphen ranges caused
the reported FormatException spam; an actual-runtime regression reproduces it
and verifies all corrected colors/reopens. 3,690 color + 1,788 controller checks
and scoped native tests pass. Other station parts/plugins are unchanged.
Current packed model and previews are in rw-v075dev8; ZIPs are in outputs/.

'''+s[end:]
s=s.replace('| Station Modules | 0.7.5-dev.7 | 0.7.5-dev.6 | rw-v075dev7 / rw-v075dev6 |','| Station Modules | 0.7.5-dev.8 | 0.7.5-dev.7 | rw-v075dev8 / rw-v075dev7 |');p.write_text(s,encoding='utf-8')
p=W/'ROOSTERWORKS_DEVELOPMENT_CONTEXT.md';s=p.read_text(encoding='utf-8')
if not s.startswith('Latest station build: rw-v075dev8'):
 p.write_text('''Latest station build: rw-v075dev8 / v0.7.5-dev.8 TEST. User reported console FormatException, ring lights not working and missing hub/perimeter access. Actual KSP.log attributes spam to ModuleRWRingColor.Bind Int32.Parse: our new map used 0-255 but established parser expects start:count. Fixed all four entries to0:256. Existing shared customization plugin untouched. New actual-map/actual-source test reproduces old FormatException, then3690 checks pass through all colors/reopens/native mesh resets. Glass inherited HAB UV-specific _Emissive map; dedicated full-white16x16 rwm_gravity_window_emissive plus explicit alphaCurve1 gives all eight ring windows full mask coverage. Stock ModuleColorChanger controls retained. Added opposed0.76m outer-diameter hollow access tubes under hinges00/04 with five reinforcing hoops, spherical pivot seals and moving box colliders. Access spokes fold82deg vs other88 to clear2.5m inline modules; source/runtime/render/pose tests agree. 1788 existing controller assertions still pass, native normals/collision/mask/target/range/5poses/inline clearance/preservation gates pass. Only GRAV model/config/map/controller andversionchangefrom7, plusone masktexture; all other GameData unchanged. Current source Source/build_gravity_ring.py, Source/GravityRing.cs, packed Source/Blender/RW_GRAV_250.blend. In-game confirmation pending. Earlier native crash report185152770 was in Parallax.CollisionManager.RemoveQueuedData, separate from this managed FormatException; optional collisionLevel=-1 diagnostic ZIP prepared in outputs but never installed; no Parallax edits bundled here. No installedgame/save/previousbuild/ground/Support changes. ZIPs outputsdev.8. Prior notes below.

'''+s,encoding='utf-8')
print('Finalized dev.8 correction notes')
