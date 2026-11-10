"""Station-only equivalent of ground dev.22 logistics balance."""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];W=R.parent
sys.path.insert(0,str(R/'Source'))
from config_nodes import Node,dump
GD=R/'GameData/RoosterWorksStationModules';C=GD/'Compatibility'
CAP={'Food':1800,'Water':1700,'Oxygen':350000,'Nitrogen':200000,'Ammonia':40000,'CarbonDioxide':75000,'Hydrogen':750000}
profiles=[];patches=[];late=[];report={}
def num(v):return format(v,'.12g')
for size,scale in ((250,1),(375,3.375),(500,8)):
 ID=f'RW_LOG_{size}';mix={n:v*scale*(.2 if n in ('Food','Water','Oxygen') else .1) for n,v in CAP.items()}
 def res(n,a,c):return Node('RESOURCE',[('name',n),('amount',num(a)),('maxAmount',num(c))])
 choices=[Node('LOADOUT',[('name','Mixed supplies')],[res(n,v,v) for n,v in mix.items()])]
 for n,v in CAP.items():choices.append(Node('LOADOUT',[('name','Carbon Dioxide' if n=='CarbonDioxide' else n)],[res(n,v*scale,v*scale)]))
 for n in ('Waste','WasteWater'):choices.append(Node('LOADOUT',[('name',n)],[res(n,0,520*scale)]))
 profiles.append(Node('RW_LOG_LOADOUTS',[('name',ID)],choices))
 patches.append(Node('@PART['+ID+']:NEEDS[Kerbalism,ProfileDefault,CommunityResourcePack]:HAS[!MODULE[ModuleRWStationLogisticsContents]]:FOR[RoosterWorksStationModules]',children=[Node('MODULE',[('name','ModuleRWStationLogisticsContents'),('profileSet',ID),('contents','Mixed supplies')])]))
 fallback=[Node('%RESOURCE['+n+']',[('%name',n),('%amount',num(v)),('%maxAmount',num(v))]) for n,v in mix.items()]
 fallback += [Node('!RESOURCE['+n+'],*') for n in ('Waste','WasteWater')]
 late.append(Node('@PART['+ID+']:NEEDS[Kerbalism,ProfileDefault]:FINAL',children=fallback))
 late.append(Node('@PART['+ID+']:FINAL',children=[Node('!MODULE[ModuleRWLogisticsContents],*')]))
 for role in ('LOG','PWR'):
  late.append(Node(f'@PART[RW_{role}_{size}]:NEEDS[Kerbalism]:FINAL',children=[Node('!MODULE[Habitat],*')]+[Node('!RESOURCE['+n+'],*') for n in ('Shielding','Atmosphere','WasteAtmosphere','MoistAtmosphere')]+[Node('!MODULE[Sensor]:HAS[#type[habitat_radiation]]')]))
 report[ID]={'scale':scale,'dedicated':{n:v*scale for n,v in CAP.items()},'mixed':mix,'loadouts':{n.get('name'):[dict(r.values) for r in n.children] for n in choices}}
(C/'LogisticsLoadouts.cfg').write_text('// Station-only loadout selector, calibrated per-resource capacities and volume scaling.\n'+dump(Node('ROOT',children=patches+profiles)),encoding='utf-8')
(C/'ZZZZStationLogisticsBalance.cfg').write_text('// Final station-only balance; explicit IDs exclude ground and Station Support.\n'+dump(Node('ROOT',children=late)),encoding='utf-8')
(R/'Reports').mkdir(exist_ok=True);(R/'Reports/STATION_LOG_CAPACITIES.json').write_text(json.dumps(report,indent=2)+'\n')
p=GD/'RoosterWorksStationModules.version';v=json.loads(p.read_text());v['VERSION']['BUILD']=6;p.write_text(json.dumps(v,indent=2)+'\n')
assert (R/'Source/StationLogisticsContents.cs').exists()
print('Built station LOG250/375/500 capacities and exact LOG/PWR habitat cleanup; inventory preserved')
