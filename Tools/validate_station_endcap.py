from pathlib import Path
import sys,json,hashlib
import numpy as np
from PIL import Image
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];W=R.parent;sys.path[:0]=[str(R/'Tools'),str(R/'Source')]
from native_model import load,walk
from config_nodes import parse
GD=R/'GameData/RoosterWorksStationModules';BG=W/'rw-v075dev9/GameData/RoosterWorksStationModules';G=W/'ground-hotpatch-v23/GameData/RoosterWorksGroundModules';ID='RW_END_250_125'
checks=0
def check(v,message):
 global checks
 checks+=1
 assert v,message
added={p.relative_to(GD).as_posix() for p in GD.rglob('*') if p.is_file() and not (BG/p.relative_to(GD)).exists()}
check(added=={f'Parts/{ID}.cfg',f'Models/{ID}.mu','Models/rwm_station_endlabel.png','Models/rwm_endwindow.png','Models/rwm_endwindow_emissive.png','Compatibility/RoundedStationEndcap.cfg'},'Unexpected new GameData files '+str(added))
for old in BG.rglob('*'):
 if old.is_file():
  relative=old.relative_to(BG);check((GD/relative).exists(),'Removed old asset')
  if relative.as_posix()!='RoosterWorksStationModules.version':check(old.read_bytes()==(GD/relative).read_bytes(),'Changed existing asset '+str(relative))
check(json.loads((GD/'RoosterWorksStationModules.version').read_text())['VERSION']['BUILD']==10,'Version')
p=parse((GD/f'Parts/{ID}.cfg').read_text()).children[0];modules={n.get('name'):n for n in p.children if n.header=='MODULE'}
check(p.header=='PART' and p.get('name')==ID,'Part declaration')
check(p.get('node_stack_top')=='0, .45, 0, 0, 1, 0, 1' and p.get('node_stack_bottom')=='0, -.45, 0, 0, -1, 0, 2','Y-axial interfaces')
check(p.get('CrewCapacity')=='0' and p.get('vesselType')=='Station','Orbital crewless role')
check(p.get('mass')=='.30' and p.get('fuelCrossFeed')=='true','Mass/crossfeed')
check(not any(n.header in ('RESOURCE','INTERNAL') for n in p.children),'Unexpected resource/IVA')
check(set(modules)=={'ModuleRWStationFinish','ModuleRWRingColor','ModuleRWEditorMenu','ModuleDockingNode','ModuleColorChanger'},'Unexpected runtime dependency')
check(next(n for n in p.children if n.header=='MODEL').get('model')=='RoosterWorksStationModules/Models/'+ID,'Ground dependency')
port=modules['ModuleDockingNode'];check(port.get('referenceAttachNode')=='top' and port.get('nodeType')=='size1','Small end only docking')
check(port.get('stagingEnabled')==port.get('stagingToggleEnabledEditor')==port.get('stagingToggleEnabledFlight')=='false','Docking staging disabled')
check(modules['ModuleRWRingColor'].get('ringModel')==ID,'Ring model')
model=load(GD/f'Models/{ID}.mu');nodes=dict(walk(model.root));n=next(n for _,n in walk(model.root) if n['name']==port.get('nodeTransformName'))
x,y,z,w=n['rotation'];forward=np.array((2*(x*z+y*w),2*(y*z-x*w),1-2*(x*x+y*y)))
check(np.allclose(n['position'],(0,.45,0)) and np.allclose(forward,(0,1,0),atol=1e-6),'Nose port direction and position')
source=load(G/'Models/RW_GND_END_250_125.mu');oldnodes={n['name']:n for _,n in walk(source.root)};A=np.array([[0,0,-1],[-1,0,0],[0,1,0]])
triangles=0;colliders=0
for path,n in walk(model.root):
 check(not any(v in n['name'] for v in ('Leg','Stair','GroundContact','GroundPipe')),'Ground hardware')
 if 'mesh' in n:
  mesh=n['mesh'];v=np.array(mesh['vertices']);norm=np.array(mesh['normals']);check(np.isfinite(v).all() and np.isfinite(norm).all(),'Non-finite mesh')
  check(len(v)==len(norm)==len(mesh['uvs']) and len(v)<65535,'Mesh cardinality')
  check(np.allclose(np.linalg.norm(norm,axis=1),1,atol=.001),'Unit normals')
  for sub in mesh['submeshes']:
   tri=np.array(sub);triangles+=len(tri);cross=np.cross(v[tri[:,1]]-v[tri[:,0]],v[tri[:,2]]-v[tri[:,0]]);dot=(cross*norm[tri].mean(1)).sum(1);check(dot.min(initial=0)>-1e-7,'Winding '+path)
  original=oldnodes[n['name']]['mesh']
  if n['name']!='RW_Endcap_graphite':
   check(np.allclose(v,np.array(original['vertices'])@A.T,atol=1e-7),'Unexpected shape change '+path)
   check(mesh['uvs']==original['uvs'] and mesh['submeshes']==original['submeshes'],'UV/topology change '+path)
  else:check(len(original['submeshes'][0])-len(mesh['submeshes'][0])==2496,'Hose removal count')
 if 'collider' in n:
  c=n['collider'];check(c['type']=='mesh' and c['convex']==1 and c['trigger']==0,'Hull collision')
  check(sum(map(len,c['mesh']['submeshes']))<=255,'PhysX convex triangle limit')
  check(np.allclose(c['mesh']['vertices'],np.array(oldnodes[n['name']]['collider']['mesh']['vertices'])@A.T,atol=1e-7),'Collision shape changed')
  colliders+=1
for t in model.textures:check((GD/'Models'/(t['name']+'.png')).exists(),'Missing texture '+t['name'])
check(not any('gnd_' in t['name'] for t in model.textures),'Ground-branded texture')
rule,organizer=parse((GD/'Compatibility/RoundedStationEndcap.cfg').read_text()).children
check(rule.get('model')==ID and len(rule.children)==3,'Ring maps')
for entry in rule.children:
 mesh=nodes[entry.get('path')]['mesh'];count=len(mesh['submeshes'][0]);check(int(entry.get('vertices'))==len(mesh['vertices']) and int(entry.get('triangles'))==count,'Ring-map mesh count')
 for token in entry.get('ranges').split(','):
  start,length=map(int,token.split(':'));check(start>=0 and length>0 and start+length<=count,'Ring triangle ranges')
check(organizer.children[-1].get('organizerSubcategory')=='crewAdapters','Station Adapters menu')
light=modules['ModuleColorChanger'];check(light.get('includedRenderer')=='RW_EndWindows','Window light target')
mat=model.materials[nodes['/'+ID+'/RW_EndWindows']['materials'][0]]
check(mat['shader']=='KSP/Emissive/Diffuse','Window shader')
mask=model.textures[mat['properties']['_Emissive']['index']]['name'];check(np.asarray(Image.open(GD/'Models'/(mask+'.png')).convert('RGB')).min()==255,'Window mask')
check(next(c for c in light.children if c.header=='alphaCurve').values==[('key','0 1'),('key','1 1')],'Window alpha')
check('PASS 3728 actual-map color assertions' in (R/'Reports/endcap-color-tests.log').read_text(),'Actual-runtime color regression')
for file in (GD/'Compatibility').glob('*.cfg'):parse(file.read_text())
for path,digest in json.loads((R/'Reports/ENDCAP_PROTECTED_INPUTS.json').read_text()).items():check(hashlib.sha256((W/path).read_bytes()).hexdigest()==digest,'Protected input '+path)
for line in (R/'CHECKSUMS-SHA256.txt').read_text().splitlines():
 digest,path=line.split('  ',1);check(hashlib.sha256((R/path).read_bytes()).hexdigest()==digest,'Manifest '+path)
print(f'PASS station endcap dev.10: {checks} checks; {triangles} triangles; {colliders} convex hull sections; 104 hose segments removed; fixed Y-axis nodes and outward size1 docking; station-only dependencies; window lighting and ring maps; all dev.9 assets/plugins and ground build preserved')
