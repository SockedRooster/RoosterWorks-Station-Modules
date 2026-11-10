from pathlib import Path
R=Path(__file__).resolve().parents[1];W=R.parent
p=W/'WORKSPACE_INDEX.md';s=p.read_text(encoding='utf-8');start=s.index('Latest station build:');end=s.index('Latest ground build:',start)
s=s[:start]+'''Latest station build: **rw-v075dev7 / v0.7.5-dev.7 TEST**. New GRAV-250
folding/inflatable four-crew ring: stationary 2.5 m hub, eight folding spokes,
9.84 m deployed ring, powered visual rotation and 1–8 rpm controls. No physical
gravity/comfort bonus; conservative Kerbalism counts the fixed hub only.
All dev.6 assets and LOG/PWR balance remain unchanged. Native geometry/pose
checks, KSP compilation and 1,788 controller assertions pass. In-game testing
pending. Preview/source/install archives are in rw-v075dev7 and outputs/.

'''+s[end:]
s=s.replace('| Station Modules | 0.7.5-dev.6 | 0.7.5-dev.5 | rw-v075dev6 / rw-v075dev5 |','| Station Modules | 0.7.5-dev.7 | 0.7.5-dev.6 | rw-v075dev7 / rw-v075dev6 |');p.write_text(s,encoding='utf-8')
p=W/'ROOSTERWORKS_DEVELOPMENT_CONTEXT.md';s=p.read_text(encoding='utf-8')
if not s.startswith('Latest station build: rw-v075dev7'):
 p.write_text('''Latest station build: rw-v075dev7 / v0.7.5-dev.7 TEST. User asked for a rotating gravity ring compatible with 2.5 m station parts and chose folding orbital deployment. Built RW_GRAV_250 with fixed 2.5 m hub, two ±1.85 m size2 stack nodes, eight alternately folding spokes and packed/inflatable torus sectors. Ring major radius4.2 m/minor.72, nominal OD9.84m; folded visual OD3.356 m, length5.763m; recommend5m fairing. Four crew stock crewCabinInternals, no exterior hatch, transfer through hub. 8t/48000funds/900EC, 8slots600L. ModuleRWGravityRing separate DLL: deploy30s/.25ECs; powered visual spin1–8RPM default6, .75ECs; ramp/coast, persisted phase/deployment/RPM, crewed/spinning fold gates, orbital/editor controls, packed/warp pause. Does NOT create physical gravity, torque or rotating IVA; equivalent g informational (~.17g at6RPM). No automatic comfort bonus. Conservative Kerbalism uses fixed hub12m3/surface37 only; ring deployed habitation accounting and real gravity integration future. White/Grey via existing path scope, new hub ring map and eight emissive window banks. All dev.6 GameData byte-identical exceptversion, adds six assets/configs only; existing 6 plugins preserved. Build Source/build_gravity_ring.py; Source/GravityRing.cs; Tools/build-gravity-runtime.ps1; packed native-equivalent Source/Blender/RW_GRAV_250.blend. Previews Media/GravityRing Stowed/Unfolding/Deployed. KSP1.12.5 compilation, 1788 actual-source controller assertions, native/collider/material/ring maps/5poses/preservation/hash validation passed. Install/source ZIPs outputs dev.7. In-game confirmation pending. No game/save/ground/dev6/artist/Support/skycrane modifications or publication. All dev6 LOG scaling/PWR-LOG no-hab balance retained. Prior notes below.

'''+s,encoding='utf-8')
print('Updated station gravity-ring workspace notes')
