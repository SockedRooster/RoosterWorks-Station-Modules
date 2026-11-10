"""Self-contained orbital versions of four ground industrial roles."""
from pathlib import Path
import sys,copy,math,json,hashlib
import numpy as np
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];W=R.parent;B=W/'rw-v075dev10';G=W/'ground-hotpatch-v28';GD=R/'GameData/RoosterWorksStationModules'
sys.path[:0]=[str(R/'Source'),str(R/'Tools')]
from native_model import load,walk
from native_derivatives import write
from config_nodes import Node,parse,dump
from appearance_textures import label
import build_hab250 as h
A=np.array([[0,0,1],[1,0,0],[0,1,0]],dtype=float)
ROLES={'ISRU':'Orbital Ore Refinery','NST':'Nuclear Materials Vault','CEN':'Fuel Centrifuge','NSM':'Nuclear Smelter'}

def node(name,position=(0,0,0),rotation=(0,0,0,1)):
 return dict(name=name,position=position,rotation=rotation,scale=(1,1,1),children=[])

def saddle(model):
 # A sealed saddle for the original refinery skid, before axis conversion.
 mesh=h.Mesh()
 for a,b in zip(np.linspace(-.65,.65,25),np.linspace(-.65,.65,25)[1:]):
  za=-math.sqrt(1.204**2-a*a)+.035;zb=-math.sqrt(1.204**2-b*b)+.035
  points=np.array([(-.95,a,za),(.95,a,za),(.95,b,zb),(-.95,b,zb),(-.95,a,-1.31),(.95,a,-1.31),(.95,b,-1.31),(-.95,b,-1.31)])
  for face in ((0,1,2,3),(4,7,6,5),(0,4,5,1),(3,2,6,7),(0,3,7,4),(1,5,6,2)):
   v=points[list(face)];normal=np.cross(v[1]-v[0],v[2]-v[0]);normal/=np.linalg.norm(normal)
   if np.dot(normal,v.mean(0)-points.mean(0))<0:v=v[::-1];normal=-normal
   mesh.quad(v.tolist(),[normal.tolist()]*4)
 material=next(i for i,m in enumerate(model.materials) if model.textures[m['properties']['_MainTex']['index']]['name']=='rwm_graphite')
 out=node('RW_ISRU_HullSaddle');out.update(mesh=dict(vertices=mesh.vertices,normals=mesh.normals,uvs=mesh.uvs,submeshes=[mesh.triangles]),materials=[material],shadows=(1,1))
 return out

def main():
 protected={p.relative_to(W).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for base in (B,G) for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 (R/'Reports/ORBITAL_INDUSTRY_PROTECTED.json').write_text(json.dumps(protected,indent=2)+'\n')
 basepart=parse((B/'GameData/RoosterWorksStationModules/Parts/RW_PWR_250.cfg').read_text()).children[0]
 ringbase=next(n for n in parse((GD/'Compatibility/RingGeometry.cfg').read_text()).children if n.get('model')=='RW_PWR_250')
 ringrules=[];audit=[];fixtures={}
 for role,title in ROLES.items():
  ID='RW_'+role+'_250';model=load(B/'GameData/RoosterWorksStationModules/Models/RW_PWR_250.mu');model.name=ID;model.root['name']=ID
  tex='rwm_orbital_'+role.lower()+'label'
  for t in model.textures:
   if t['name']=='rwm_pwrlabel':t['name']=tex
  label(role+'-250',title.upper()).save(GD/f'Models/{tex}.png')
  gm=load(G/f'GameData/RoosterWorksGroundModules/Models/RW_GND_{role}.mu')
  if role=='ISRU':
   equipment=[copy.deepcopy(next(n for n in gm.root['children'] if n['name']=='RW_RefinerySkid')),saddle(gm)]
   for original in list(equipment):
    mirror=copy.deepcopy(original);mirror['name']+='_Port';mirror['rotation']=(0,1,0,0)
    def suffix(n):
     for child in n['children']:child['name']+='_Port';suffix(child)
    suffix(mirror);equipment.append(mirror)
  else:equipment=[copy.deepcopy(n) for n in gm.root['children'] if n['name'].startswith(('RW_'+role+'_Industry','RW_'+role+'_HullSaddle'))]
  wrapper=node('RW_OrbitalIndustryHardware',rotation=(.5,.5,.5,.5));wrapper['children']=equipment
  for _,n in walk(wrapper):
   if 'materials' not in n:continue
   indices=[]
   for i in n['materials']:
    src=gm.materials[i];texture=gm.textures[src['properties']['_MainTex']['index']]['name']
    found=next((j for j,m in enumerate(model.materials) if m['shader']==src['shader'] and model.textures[m['properties']['_MainTex']['index']]['name']==texture),None)
    assert found is not None,('New hardware material outside station palette',texture)
    indices.append(found)
   n['materials']=indices
  model.root['children'].append(wrapper)
  for end,sign in (('top',1),('bottom',-1)):
   model.root['children'].append(node('RW_IndustryDock_'+end,(0,sign*1.2,0),(-sign*math.sqrt(.5),0,0,math.sqrt(.5))))
  write(model,GD/f'Models/{ID}.mu')
  old=parse((G/f'GameData/RoosterWorksGroundModules/Parts/RW_GND_{role}.cfg').read_text()).children[0]
  p=copy.deepcopy(basepart);p.header='PART' if role=='ISRU' else 'PART:NEEDS[CommunityResourcePack,SystemHeat]'
  for k,v in [('name',ID),('title','RoosterWorks RW-'+role+'-250 '+title),('category','Utility'),('TechRequired',old.get('TechRequired')),('mass',old.get('mass')),('cost','14006' if role=='ISRU' else old.get('cost')),('entryCost',old.get('entryCost')),('CrewCapacity','0'),('breakingForce','2000'),('breakingTorque','2000'),('vesselType','Station'),('fuelCrossFeed','true'),('tags','roosterworks orbital station industry refinery nuclear uranium fuel processing storage '+role.lower())]:p.set(k,v)
  p.set('description','Orbital 2.5 m / 2.4 m inline '+title.lower()+'. Matching supported equipment on both sides, station hull and labels; two size2 docking ends with permanent crossfeed and manual undocking only. '+({'ISRU':'Four stock Ore recipes (LF+Ox, LiquidFuel, Oxidizer, Monopropellant); 300 Ore / 1000 EC. Fit external power, active radiators and separate fuel storage.',
   'NST':'Separate empty cargo bays: 1000 Uraninite, 500 RW Nuclear Feedstock, 200 EnrichedUranium and 200 DepletedFuel; 500 EC. Default empty price 24,000.',
   'NSM':'Uraninite to RW Nuclear Feedstock; 60 EC/s and 54 kW heat at nominal efficiency. Empty 250-unit input/output buffers; 1000 EC. Default empty price 36,000.',
   'CEN':'RW Nuclear Feedstock to EnrichedUranium and DepletedFuel; 120 EC/s and 108 kW heat at nominal efficiency. Empty feedstock 250 / fuel 40 / depleted 200 buffers; 1500 EC. Default empty price 68,000.'}[role])+' Crewless utility: no habitat, Shielding resource, reactor or generator. Nuclear processors require CRP and SystemHeat; use Engineer-enabled manual nuclear fuel transfer. No Ground Modules runtime dependency.')
  p.children=[n for n in p.children if n.header!='RESOURCE']
  next(n for n in p.children if n.header=='MODEL').set('model','RoosterWorksStationModules/Models/'+ID)
  wanted=('ModuleResourceConverter','ModuleCoreHeat','ModuleOverheatDisplay','ModuleSystemHeat','ModuleSystemHeatConverter','ModuleSystemHeatFissionFuelContainer')
  p.children += [copy.deepcopy(n) for n in old.children if n.header=='RESOURCE' or n.get('name') in wanted]
  p.children += [Node('MODULE',[('name','ModuleRWStationFinish'),('finish','White')]),Node('MODULE',[('name','ModuleRWRingColor'),('ringModel',ID),('ringColor','Original')]),Node('MODULE',[('name','ModuleRWEditorMenu')]),Node('MODULE',[('name','ModuleRWOrbitalIndustryDocking')]),Node('VABORGANIZER:NEEDS[VABOrganizer]',[('organizerSubcategory','crewUtility')])]
  for dock in [n for n in old.children if n.get('name')=='ModuleDockingNode']:
   d=copy.deepcopy(dock);end=d.get('referenceAttachNode')
   d.set('nodeTransformName','RW_IndustryDock_'+end);d.set('controlTransformName','RW_IndustryDock_'+end);p.children.append(d)
  (GD/f'Parts/{ID}.cfg').write_text(dump(Node('ROOT',children=[p])))
  rule=copy.deepcopy(ringbase);rule.set('model',ID)
  for n in rule.children:n.set('path',n.get('path').replace('/RW_PWR_250/','/'+ID+'/'))
  ringrules.append(rule);nodes=dict(walk(model.root))
  fixtures[ID]=[dict(path=n.get('path'),texture=n.get('texture'),vertexCount=int(n.get('vertices')),triangles=[i for t in nodes[n.get('path')]['mesh']['submeshes'][0] for i in t],ranges=n.get('ranges')) for n in rule.children]
  audit.append({'id':ID,'role':role,'ground_source':'RW_GND_'+role,'dry_mass_t':float(p.get('mass')),'configured_cost':float(p.get('cost')),'docking_ports':2,'side_assemblies':2,'axis':'Y','length_m':2.4})
 ids=','.join(s['id'] for s in audit)
 ringrules.append(Node('@PART['+ids+']:NEEDS[Kerbalism]:FINAL',children=[Node('!MODULE[Habitat],*')]+[Node('!RESOURCE['+v+'],*') for v in ('Shielding','Atmosphere','WasteAtmosphere','MoistAtmosphere')]))
 ringrules.append(Node('@PART['+ids+']:NEEDS[VABOrganizer]:FINAL',[('%category','Utility')],[Node('!VABORGANIZER,*'),Node('VABORGANIZER',[('organizerSubcategory','crewUtility')])]))
 (GD/'Compatibility/OrbitalIndustry.cfg').write_text(dump(Node('ROOT',children=ringrules)))
 feed=parse((G/'GameData/RoosterWorksGroundModules/Resources/NuclearFeedstock.cfg').read_text()).children[0];feed.header='RESOURCE_DEFINITION:NEEDS[CommunityResourcePack,!RoosterWorksGroundModules]'
 (GD/'Resources').mkdir(exist_ok=True)
 (GD/'Resources/OrbitalNuclearFeedstock.cfg').write_text('// Standalone definition; Ground Modules dev.26+ owns the identical resource when installed.\n'+dump(Node('ROOT',children=[feed])))
 (R/'Reports/ORBITAL_INDUSTRY.json').write_text(json.dumps(audit,indent=2)+'\n');(R/'Reports/ORBITAL_INDUSTRY_COLOR_FIXTURE.json').write_text(json.dumps(fixtures,separators=(',',':'))+'\n')
 source=(G/'Source/GroundDocking.cs').read_text().replace('ModuleRWGroundDocking','ModuleRWOrbitalIndustryDocking').replace('id.StartsWith("RW.GND.", StringComparison.Ordinal)','(id == "RW.ISRU.250" || id == "RW.NST.250" || id == "RW.CEN.250" || id == "RW.NSM.250")')
 (R/'Source/OrbitalIndustryDocking.cs').write_text(source)
 v=GD/'RoosterWorksStationModules.version';data=json.loads(v.read_text());data['VERSION']['BUILD']=11;v.write_text(json.dumps(data,indent=2)+'\n')
 for path,digest in protected.items():assert hashlib.sha256((W/path).read_bytes()).hexdigest()==digest,path
 print('PASS built four standalone 2.5 m Y-axial orbital industrial models/configs; original processing and cargo preserved; two supported side assemblies; two docking ends')

if __name__=='__main__':main()
