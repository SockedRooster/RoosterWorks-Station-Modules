from pathlib import Path
import sys,json,hashlib,math
import numpy as np
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];W=R.parent;GD=R/'GameData/RoosterWorksStationModules';B=W/'rw-v075dev8/GameData/RoosterWorksStationModules'
sys.path[:0]=[str(R/'Source'),str(R/'Tools')]
from native_model import load,walk
from config_nodes import parse
added=set()
changed=set()
for f in GD.rglob('*'):
 if not f.is_file():continue
 rel=f.relative_to(GD).as_posix();old=B/rel
 if not old.exists():assert rel in added,rel
 elif f.read_bytes()!=old.read_bytes():changed.add(rel)
assert changed=={'RoosterWorksStationModules.version','Models/RW_GRAV_250.mu','Plugins/RoosterWorksGravityRing.dll'}
assert {p.relative_to(B) for p in B.rglob('*') if p.is_file()} <= {p.relative_to(GD) for p in GD.rglob('*') if p.is_file()}
model=load(GD/'Models/RW_GRAV_250.mu');nodes=dict(walk(model.root));byname={n['name']:n for n in nodes.values()}
for path,n in nodes.items():
 if 'mesh' in n:
  mesh=n['mesh'];v=np.array(mesh['vertices']);normal=np.array(mesh['normals']);assert np.isfinite(v).all() and np.isfinite(normal).all()
  assert len(v)<65535 and np.allclose(np.linalg.norm(normal,axis=1),1,atol=.001),path
  for sub in mesh['submeshes']:
   t=np.array(sub);cross=np.cross(v[t[:,1]]-v[t[:,0]],v[t[:,2]]-v[t[:,0]])
   assert (np.einsum('ij,ij->i',cross,normal[t].mean(axis=1))>=-1e-7).all(),path
  for index in n['materials']:
   assert 0<=index<len(model.materials)
   texture=model.textures[model.materials[index]['properties']['_MainTex']['index']]['name'];assert (GD/'Models'/(texture+'.png')).exists()
 if 'collider' in n:
  c=n['collider'];assert not c['trigger']
  if c['type']=='mesh':assert c['convex'] and sum(len(s) for s in c['mesh']['submeshes'])<=255
  else:assert all(a>0 for a in c['size'])
for i in range(8):assert all('RW_Gravity'+p+('%02d'%i) in byname for p in ('Hinge','Pod'))
assert len([n for n in byname if n.startswith('RW_GravityCabinCollision')])==32
# Evaluate exact controller poses through the complete native hierarchy.
def quat(q):
 x,y,z,w=q;return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],[2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def evaluate(model,d):
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

poses={}
for d in (0,.25,.5,.75,1):
 lo,hi,r=bounds(d);poses[str(d)]={'minimum':lo.tolist(),'maximum':hi.tolist(),'radial_diameter':float(r*2)}
assert poses['0']['radial_diameter']<5.0
assert max(abs(v) for key in ('minimum','maximum') for v in (poses['0'][key][1],))<=1.851
assert 9.8<poses['1']['radial_diameter']<10.1
part=parse((GD/'Parts/RW_GRAV_250.cfg').read_text()).children[0]
assert part.get('CrewCapacity')=='4' and part.get('TechRequired')=='specializedConstruction'
assert part.get('node_stack_top')=='0,1.85,0,0,1,0,2' and part.get('node_stack_bottom')=='0,-1.85,0,0,-1,0,2'
assert next(n for n in part.children if n.header=='INTERNAL').get('name')=='crewCabinInternals'
lights=next(n for n in part.children if n.get('name')=='ModuleColorChanger');renderers=[v for k,v in lights.values if k=='includedRenderer']
assert len(renderers)==8 and all(n in byname for n in renderers)
maps=parse((GD/'Compatibility/GravityRingGeometry.cfg').read_text()).children[0]
for spec in maps.children:
 n=nodes[spec.get('path')];assert len(n['mesh']['vertices'])==int(spec.get('vertices'));assert spec.get('ranges')=='0:'+str(len(n['mesh']['submeshes'][0]))
for color in ('steel','white','charcoal','blue','green','red','gold'):
 for tex in ('rwm_steel','rwm_bronze'):assert (GD/f'Models/rwm_ring_{tex}_{color}.png').exists()
compat=parse((GD/'Compatibility/GravityRing.cfg').read_text());hab=next(n for n in compat.children if 'FeatureHabitat' in n.header).children[0];assert hab.get('%volume')=='12'
assert 'PASS 2652 gravity-ring' in (R/'Reports/gravity-tests.log').read_text()
assert 'PASS gravity-ring controller compiled' in (R/'Reports/gravity-runtime-build.log').read_text()

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
 assert '/RW_GravityHinge%02d/RW_GravityTelescopic%02d/'%(i,i) in path
 assert np.isclose(np.array(byname[name]['mesh']['vertices'])[:,0].min(),-.1)
 assert np.isclose(np.array(byname[name]['mesh']['vertices'])[:,0].max(),2.75)
 assert 'RW_GravityAccessRotarySeal%02d'%i in byname
 assert 'RW_GravityAccessCollision%02d'%i in byname
# Deployed mesh geometry and proven lighting/color data must remain exact.
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
assert 'PASS 3690 actual-map color' in (R/'Reports/gravity-color-tests.log').read_text()

for line in (R/'CHECKSUMS-SHA256.txt').read_text().splitlines():
 digest,name=line.split('  ',1);assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
for name,digest in json.loads((R/'Reports/GRAVITY_PROTECTED_INPUTS.json').read_text()).items():assert hashlib.sha256((W/name).read_bytes()).hexdigest()==digest,name
(R/'Reports/GRAVITY_POSE_BOUNDS.json').write_text(json.dumps(poses,indent=2)+'\n')
print('PASS gravity dev.9: native geometry/materials/winding/collision; five finite folding poses; fixed size2 nodes; four-seat IVA; eight emissive window banks; stock tech with optional CTT; finish/ring maps; compact stow and telescopic arms; deployed geometry matches dev.8; accepted lights/maps and all other GameData preserved; protected inputs and hashes')
