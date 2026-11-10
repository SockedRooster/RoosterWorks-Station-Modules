from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];W=R.parent;GD=R/'GameData/RoosterWorksStationModules';B=W/'rw-v075dev5/GameData/RoosterWorksStationModules'
sys.path.insert(0,str(R/'Source'))
from config_nodes import parse
allowed={'Compatibility/LogisticsLoadouts.cfg','Compatibility/ZZZZStationLogisticsBalance.cfg','Plugins/RoosterWorksStationLogistics.dll','RoosterWorksStationModules.version'}
changed=set()
for p in GD.rglob('*'):
 if p.is_file():
  rel=p.relative_to(GD).as_posix();old=B/rel
  if not old.exists() or p.read_bytes()!=old.read_bytes():changed.add(rel)
assert changed==allowed,changed
assert {p.relative_to(B) for p in B.rglob('*') if p.is_file()} <= {p.relative_to(GD) for p in GD.rglob('*') if p.is_file()}
roots=parse((GD/'Compatibility/LogisticsLoadouts.cfg').read_text());profiles={n.get('name'):n for n in roots.children if n.header=='RW_LOG_LOADOUTS'}
rules=parse((GD/'Compatibility/ZZZZStationLogisticsBalance.cfg').read_text());report=json.loads((R/'Reports/STATION_LOG_CAPACITIES.json').read_text())
base={'Food':1800,'Water':1700,'Oxygen':350000,'Nitrogen':200000,'Ammonia':40000,'CarbonDioxide':75000,'Hydrogen':750000}
for size,scale,slots,volume in ((250,1,12,1400),(375,3.375,24,4725),(500,8,36,11200)):
 ID=f'RW_LOG_{size}';profile=profiles[ID];choices={n.get('name'):n for n in profile.children};assert len(choices)==10
 assert report[ID]['loadouts']=={n.get('name'):[dict(r.values) for r in n.children] for n in profile.children}
 for name,cap in base.items():
  choice=choices['Carbon Dioxide' if name=='CarbonDioxide' else name];assert len(choice.children)==1
  r=choice.children[0];assert r.get('name')==name and float(r.get('amount'))==float(r.get('maxAmount'))==cap*scale
 mixed={n.get('name'):float(n.get('maxAmount')) for n in choices['Mixed supplies'].children}
 assert set(mixed)==set(base)
 assert abs(sum(mixed[n]/(base[n]*scale) for n in base)-1)<1e-8
 for n in base:assert abs(mixed[n]/(base[n]*scale)-(.2 if n in ('Food','Water','Oxygen') else .1))<1e-8
 for n in ('Waste','WasteWater'):assert float(choices[n].children[0].get('maxAmount'))==520*scale and choices[n].children[0].get('amount')=='0'
 part=parse((GD/f'Parts/{ID}.cfg').read_text()).children[0];inv=next(n for n in part.children if n.get('name')=='ModuleInventoryPart')
 assert int(inv.get('InventorySlots'))==slots and float(inv.get('packedVolumeLimit'))==volume
 late=next(n for n in rules.children if n.header==f'@PART[{ID}]:NEEDS[Kerbalism,ProfileDefault]:FINAL')
 for n in late.children:
  if n.header.startswith('%RESOURCE'):assert float(n.get('%amount'))==float(n.get('%maxAmount'))==mixed[n.get('%name')]
 for role in ('LOG','PWR'):
  rule=next(n for n in rules.children if n.header==f'@PART[RW_{role}_{size}]:NEEDS[Kerbalism]:FINAL')
  assert {n.header for n in rule.children}=={'!MODULE[Habitat],*','!MODULE[Sensor]:HAS[#type[habitat_radiation]]'}|{'!RESOURCE['+n+'],*' for n in ('Shielding','Atmosphere','WasteAtmosphere','MoistAtmosphere')}
 assert 'PASS 1884 station-logistics' in (R/f'Reports/logistics-tests-{size}.log').read_text()
assert all(n.header.split(']')[0][6:] in {f'RW_{r}_{s}' for r in ('LOG','PWR') for s in (250,375,500)} for n in rules.children)
for line in (R/'CHECKSUMS-SHA256.txt').read_text().splitlines():
 digest,name=line.split('  ',1);assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
for name,digest in json.loads((R/'Reports/PROTECTED_INPUTS.json').read_text()).items():assert hashlib.sha256((W/name).read_bytes()).hexdigest()==digest,name
assert json.loads((GD/'RoosterWorksStationModules.version').read_text())['VERSION']['BUILD']==6
print('PASS station dev.6: three exact volume-scaled LOG profiles; priority mixed allocation; CO2/H2; unchanged inventory; six scoped LOG/PWR habitat/shielding removals; all part configs, models, textures, five existing plugins and other compatibility files identical to dev.5; protected inputs and manifest')
