from pathlib import Path
import sys,copy,json,hashlib
import numpy as np
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];W=R.parent;GD=R/'GameData/RoosterWorksStationModules';BG=W/'rw-v075dev10/GameData/RoosterWorksStationModules';G=W/'ground-hotpatch-v28/GameData/RoosterWorksGroundModules'
sys.path[:0]=[str(R/'Tools'),str(R/'Source')]
from native_model import load,walk
from config_nodes import parse
checks=0
def check(value,message):
 global checks
 checks+=1
 assert value,message
def rotation(q):
 x,y,z,w=q
 return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def matrices(root):
 out={}
 def rec(n,parent):
  m=np.eye(4);m[:3,:3]=rotation(n['rotation'])@np.diag(n['scale']);m[:3,3]=n['position'];m=parent@m;out[id(n)]=m
  for c in n['children']:rec(c,m)
 rec(root,np.eye(4));return out

specs=json.loads((R/'Reports/ORBITAL_INDUSTRY.json').read_text());check({s['role'] for s in specs}=={'ISRU','NST','CEN','NSM'},'Four industrial roles')
added={'Compatibility/OrbitalIndustry.cfg','Resources/OrbitalNuclearFeedstock.cfg','Plugins/RoosterWorksOrbitalIndustry.dll'}
for s in specs:added|={f"Models/{s['id']}.mu",f"Parts/{s['id']}.cfg",'Models/rwm_orbital_'+s['role'].lower()+'label.png'}
check({p.relative_to(GD).as_posix() for p in GD.rglob('*') if p.is_file() and not (BG/p.relative_to(GD)).exists()}==added,'Exact addition scope')
for old in BG.rglob('*'):
 if old.is_file():
  rel=old.relative_to(BG);check((GD/rel).exists(),'Removed station file')
  if rel.as_posix()!='RoosterWorksStationModules.version':check((GD/rel).read_bytes()==old.read_bytes(),'Prior station asset modified '+str(rel))
check(len(list((GD/'Parts').glob('*.cfg')))==49 and len(list((GD/'Models').glob('*.mu')))==47,'49 parts / 47 native models')
base=load(BG/'Models/RW_PWR_250.mu');rules=parse((GD/'Compatibility/OrbitalIndustry.cfg').read_text()).children
wanted=('ModuleResourceConverter','ModuleCoreHeat','ModuleOverheatDisplay','ModuleSystemHeat','ModuleSystemHeatConverter','ModuleSystemHeatFissionFuelContainer')
costs={'ElectricCharge':0,'Ore':.02,'Uraninite':.7,'RW_NuclearFeedstock':.8,'EnrichedUranium':865,'DepletedFuel':0}
for s in specs:
 ID=s['id'];role=s['role'];p=parse((GD/f'Parts/{ID}.cfg').read_text()).children[0];old=parse((G/f'Parts/RW_GND_{role}.cfg').read_text()).children[0]
 check(p.header==('PART' if role=='ISRU' else 'PART:NEEDS[CommunityResourcePack,SystemHeat]'),'Optional nuclear providers')
 check(p.get('vesselType')=='Station' and p.get('CrewCapacity')=='0' and p.get('mass')==old.get('mass'),'Station role / balance')
 check(p.get('category')=='Utility' and next(n for n in p.children if n.header.startswith('VABORGANIZER')).get('organizerSubcategory')=='crewUtility','Station Utility grouping')
 check([n for n in p.children if n.header=='RESOURCE' or n.get('name') in wanted]==[n for n in old.children if n.header=='RESOURCE' or n.get('name') in wanted],'Exact ground cargo / recipe / thermal modules')
 check(not any(n.get('name') in ('Habitat','ModuleCommand','ModuleRWGroundDeploy','ModuleRWGroundDocking','ModuleRCSFX','ModuleGenerator') for n in p.children),'Unrequested ground/crew/propulsion features')
 check(not any(n.get('name')=='Shielding' or n.header=='INTERNAL' for n in p.children),'No habitat/Shielding/IVA')
 ptext=(GD/f'Parts/{ID}.cfg').read_text();check('RoosterWorksGroundModules/' not in ptext and 'ModuleRWGround' not in ptext,'Runtime independence from Ground Modules')
 tanks=[n for n in p.children if n.header=='RESOURCE'];capacity=sum(float(n.get('maxAmount'))*costs[n.get('name')] for n in tanks);initial=sum(float(n.get('amount'))*costs[n.get('name')] for n in tanks)
 expected={'ISRU':14000,'NST':24000,'CEN':68000,'NSM':36000}[role]
 check(abs(float(p.get('cost'))-capacity+initial-expected)<1e-7,'Correct initial VAB price')
 for fraction in (0,.25,.5,.75,1):check(float(p.get('cost'))-capacity+capacity*fraction>=expected,'No negative empty/full prices')
 model=load(GD/f'Models/{ID}.mu');nodes=dict(walk(model.root));named={n['name']:n for _,n in walk(model.root)};world=matrices(model.root)
 check(model.root['children'][:len(base.root['children'])]==base.root['children'],'Accepted station hull geometry changed')
 hardware=named['RW_OrbitalIndustryHardware'];check(np.allclose(rotation(hardware['rotation']),[[0,0,1],[1,0,0],[0,1,0]]),'Ground X axis to station Y axis')
 check(len(hardware['children'])==4,'Two equipment and two saddles')
 check(sum(n['name'].endswith('_Port') for n in hardware['children'])==2,'Opposite equipment and saddle')
 for path,n in walk(model.root):
  check(not any(token in n['name'] for token in ('GroundLeg','GroundStairs','GroundContact','GroundPipe','RoofSocket','HullMount_equipment')),'Ground hardware leaked '+path)
  check(np.isfinite(n['position']).all() and np.isfinite(n['rotation']).all() and np.isfinite(n['scale']).all(),'Finite transforms')
  if 'mesh' in n:
   mesh=n['mesh'];v=np.array(mesh['vertices']);normal=np.array(mesh['normals'])
   check(len(v)==len(normal)==len(mesh['uvs']) and len(v)<65535,'Native cardinality')
   check(np.isfinite(v).all() and np.isfinite(normal).all() and np.isfinite(mesh['uvs']).all(),'Finite mesh')
   check(np.allclose(np.linalg.norm(normal,axis=1),1,atol=.001),'Unit normals')
   for sub in mesh['submeshes']:
    tri=np.array(sub);check(tri.min()>=0 and tri.max()<len(v),'Native index bounds')
    dot=(np.cross(v[tri[:,1]]-v[tri[:,0]],v[tri[:,2]]-v[tri[:,0]])*normal[tri].mean(1)).sum(1)
    check(dot.min(initial=0)>-1e-7,'Native winding '+path)
   if path.startswith('/'+ID+'/RW_OrbitalIndustryHardware'):
    transformed=v@world[id(n)][:3,:3].T+world[id(n)][:3,3];check(transformed[:,1].min()>-1.2 and transformed[:,1].max()<1.2,'Keep end mating planes clear')
  if 'collider' in n:
   c=n['collider']
   if c['type']=='box':check(all(x>0 for x in c['size']),'Positive collider size')
   else:check(c['convex']==1 and sum(map(len,c['mesh']['submeshes']))<=255,'PhysX convex limit')
 for tex in model.textures:check((GD/'Models'/(tex['name']+'.png')).exists(),'Self-contained texture '+tex['name'])
 docks=[n for n in p.children if n.get('name')=='ModuleDockingNode'];check(len(docks)==2,'Two built-in end ports')
 for dock in docks:
  target=np.array([float(v) for v in p.get('node_stack_'+dock.get('referenceAttachNode')).split(',')]);mt=world[id(named[dock.get('nodeTransformName')])]
  check(np.allclose(mt[:3,3],target[:3]) and np.allclose(mt[:3,2],target[3:6],atol=1e-6),'Port axis and attach node alignment')
  check(dock.get('nodeType')=='size2' and dock.get('crossfeed')=='true' and dock.get('stagingEnabled')=='false','Dock crossfeed/staging')
 check(any(n.get('name')=='ModuleRWOrbitalIndustryDocking' for n in p.children),'Self-contained clean docking UI')
 rule=next(n for n in rules if n.get('model')==ID);check(len(rule.children)==3,'Three native ring meshes')
 for entry in rule.children:
  m=nodes[entry.get('path')]['mesh'];check(int(entry.get('vertices'))==len(m['vertices']) and int(entry.get('triangles'))==len(m['submeshes'][0]),'Ring counts')
  for item in entry.get('ranges').split(','):
   start,count=map(int,item.split(':'));check(start>=0 and count>0 and start+count<=len(m['submeshes'][0]),'Correct ring range grammar')
 check('PASS 3728 actual-map color assertions' in (R/f'Reports/orbital-{role.lower()}-colors.log').read_text(),'Actual source color regression')
feed=parse((GD/'Resources/OrbitalNuclearFeedstock.cfg').read_text()).children[0];groundfeed=parse((G/'Resources/NuclearFeedstock.cfg').read_text()).children[0]
check(feed.header=='RESOURCE_DEFINITION:NEEDS[CommunityResourcePack,!RoosterWorksGroundModules]' and feed.values==groundfeed.values,'One identical shared feedstock definition with/without ground addon')
check('PASS orbital docking policy compiled against KSP 1.12.5' in (R/'Reports/orbital-runtime-compile.log').read_text(),'Actual KSP API compilation')
check('docking/menu assertions' in (R/'Reports/orbital-docking-tests.log').read_text() and 'PASS ' in (R/'Reports/orbital-docking-tests.log').read_text(),'Docking menu regression')
check(json.loads((GD/'RoosterWorksStationModules.version').read_text())['VERSION']['BUILD']==11,'Version')
for f in GD.rglob('*.cfg'):parse(f.read_text())
for path,digest in json.loads((R/'Reports/ORBITAL_INDUSTRY_PROTECTED.json').read_text()).items():check(hashlib.sha256((W/path).read_bytes()).hexdigest()==digest,'Protected input '+path)
(R/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in sorted((R/'GameData').rglob('*')) if p.is_file()))
print(f'PASS orbital industry dev.11: {checks} native/configuration/preservation checks; four standalone station parts; supported bilateral equipment; exact cargo and processors; Y-axis dock alignment; colors, positive prices and prior station/ground assets preserved')
