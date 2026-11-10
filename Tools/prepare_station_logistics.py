from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1];W=R.parent
hashes={}
for folder in ('rw-v075dev5','ground-hotpatch-v22'):
 for p in (W/folder).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:hashes[p.relative_to(W).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'Reports/PROTECTED_INPUTS.json').write_text(json.dumps(hashes,indent=2)+'\n')
doc='''# Station logistics balance — v0.7.5-dev.6 TEST

Applies the ground LOG balance to all three orbital station LOG sizes. The
2.5 m dedicated capacities are Food 1,800; Water 1,700; Oxygen 350,000;
Nitrogen 200,000; Ammonia 40,000; CarbonDioxide 75,000; Hydrogen 750,000.
The 3.75 m and 5 m versions multiply every capacity by 3.375 and 8 respectively.
Fractional units are retained to preserve exact proportional scaling.

Mixed supplies allocates 20% of each Food/Water/Oxygen dedicated capacity and
10% of each of the other four: 60% of the budget goes to priority supplies.
At 2.5 m this is 360 Food, 340 Water, 70,000 Oxygen, 20,000 Nitrogen,
4,000 Ammonia, 7,500 CarbonDioxide and 75,000 Hydrogen. Larger mixed loadouts
use the same volume multipliers. Dedicated Waste/WasteWater choices retain
520/1755/4160 units, initially empty; mixed now carries the seven supplies.

Station LOG/PWR at 2.5/3.75/5 m have no Kerbalism Habitat or Shielding, and no
internal pressure Atmosphere/WasteAtmosphere/MoistAtmosphere. Cargo Nitrogen,
electrical capacities, reactor fuel/variants and crewless status are preserved.

Item inventories remain unchanged: 12 slots/1,400 L; 24 slots/4,725 L;
36 slots/11,200 L. Resource tanks and item inventory are separate.

The new station-only selector adds Carbon Dioxide/Hydrogen choices without
rebuilding the five existing plugins or changing ground profiles. Storage
switching runs only in the editor, with no flight refills or save migration.
All native models, textures, part configs, appearance scope/ring controls and
other compatibility files match dev.5 exactly.

Close KSP and replace only GameData/RoosterWorksStationModules. Keep the ground
addon installed separately. Test newly placed LOG/PWR parts first to avoid old
craft resource persistence. In-game confirmation remains pending. No installed
game, save, previous build or publication was modified.

Current config builder: Source/build_station_logistics076.py. New runtime:
Source/StationLogisticsContents.cs; Tools/build-station-logistics-runtime.ps1.
Tools/test-station-logistics.ps1 -Size 250 (also 375 and 500) tests the actual
selector source with doubles: 1,884 checks per size, 5,652 total. These cover
all choice pairs, stale-resource cleanup, editor refresh, depletion, missing
definitions and flight preservation. Runtime compiles against KSP 1.12.5.
Tools/validate_station_logistics.py checks exact profiles, inventory, cleanup
scope, asset preservation and checksums. This does not run full game physics
or the ModuleManager load. Old validation reports/builders document history.
'''
(R/'STATION_LOGISTICS_BALANCE.md').write_text(doc,encoding='utf-8')
for name in ('README.md','RELEASE_NOTES.md'):
 p=R/name;s=p.read_text(encoding='utf-8')
 if not s.startswith('# RoosterWorks Station Modules — v0.7.5-dev.6'):
  p.write_text('# RoosterWorks Station Modules — v0.7.5-dev.6 TEST\n\nStation LOG storage now matches the ground balance with volume scaling, CO2/Hydrogen choices and priority mixed supplies. Station LOG/PWR have no habitat/shielding. Existing item inventories, appearance plugins and all models are preserved. See STATION_LOGISTICS_BALANCE.md.\n\n## Previous development history\n\n'+s,encoding='utf-8')
p=R/'ROADMAP.md';s=p.read_text(encoding='utf-8')
if 'Station dev.6 logistics balance' not in s:p.write_text(s+'\n## Station dev.6 logistics balance\n\nVolume-scaled LOG resource assignments and LOG/PWR habitat/shielding cleanup; no new asset scope.\n',encoding='utf-8')
(R/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in sorted((R/'GameData').rglob('*')) if p.is_file()))
print('Prepared station dev.6 documentation, protected hashes and checksums')
