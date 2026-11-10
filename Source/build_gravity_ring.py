"""Original folding/inflatable GRAV-250. Fixed 2.5 m hub; visual rotor."""
from pathlib import Path
import sys,math,json,copy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'Source'),str(R/'Tools')]
import build_hab250 as h
from native_model import load,walk
from native_derivatives import write
from station_endcaps import face_mesh
from build_adp250375 import collision_section
from config_nodes import Node,dump
GD=R/'GameData/RoosterWorksStationModules';ID='RW_GRAV_250'
m=copy.deepcopy(load(GD/'Models/RW_HAB_250.mu'));m.name=ID
def node(name,pos=(0,0,0),rot=(0,0,0,1)):
 return dict(name=name,position=pos,rotation=rot,scale=(1,1,1),children=[],tag='Untagged',layer=0)
m.root=node(ID)
indices={t['name'].removeprefix('RW_'):i for i,t in enumerate(m.materials)}
# The HAB mask is laid out for HAB window UVs; the ring uses tiled torus UVs.
# Give its glass a dedicated full-white mask so every window can emit.
Image.new('RGB',(16,16),(255,255,255)).save(GD/'Models/rwm_gravity_window_emissive.png')
m.materials[indices['glass']]['properties']['_Emissive']['index']=len(m.textures)
m.textures.append({'name':'rwm_gravity_window_emissive','type':0})
# A dedicated native label avoids reusing another part's nameplate.
im=Image.new('RGB',(1024,512),(222,226,219));draw=ImageDraw.Draw(im)
draw.rectangle((14,14,1010,498),outline=(46,59,66),width=14);draw.rectangle((38,38,986,474),outline=(166,120,64),width=8)
font='C:/Windows/Fonts/arialbd.ttf'
draw.text((70,90),'ROOSTERWORKS',font=ImageFont.truetype(font,80),fill=(35,48,57))
draw.text((70,230),'GRAV-250 / ORBITAL RING',font=ImageFont.truetype(font,47),fill=(35,48,57))
draw.text((70,330),'FOLD   /   DEPLOY   /   ROTATE',font=ImageFont.truetype(font,36),fill=(89,100,99))
im.save(GD/'Models/rwm_gravitylabel.png');mat=copy.deepcopy(m.materials[indices['label']]);mat['name']='RW_gravitylabel';mat['properties']['_MainTex']['index']=len(m.textures);m.textures.append({'name':'rwm_gravitylabel','type':0});indices['gravitylabel']=len(m.materials);m.materials.append(mat)
def mesh(parent,name,key,a):
 if not a.triangles:return
 v=np.array(a.vertices);n=np.array(a.normals)
 tris=[tuple(reversed(t)) if np.dot(np.cross(v[t[1]]-v[t[0]],v[t[2]]-v[t[0]]),n[list(t)].mean(0))<0 else t for t in a.triangles]
 parent['children'].append(dict(**node(name),mesh=dict(vertices=a.vertices,normals=a.normals,uvs=a.uvs,submeshes=[tris]),materials=[indices[key]],shadows=(1,1)))
def solid(parent,name,center,size):
 n=node(name);n['collider']=dict(type='box',trigger=0,center=center,size=size);parent['children'].append(n)
def cyl(parent,name,key,r,lo,hi):
 a=h.Mesh();h.cylinder_surface(a,r,lo,hi,64)
 for y,sign in ((lo,-1),(hi,1)):
  for j in range(64):a.triangle([(0,y,0),h.point(r,j*math.tau/64,y),h.point(r,(j+1)*math.tau/64,y)],[(0,sign,0)]*3,[(.5,.5),(0,0),(1,0)])
 mesh(parent,name,key,a)
def rail(parent,name,key,p0,p1,r=.035):
 a=h.Mesh();h.tube(a,p0,p1,r,12);mesh(parent,name,key,a)
def qz(deg):a=math.radians(deg)/2;return (0,0,math.sin(a),math.cos(a))
def qy(deg):a=math.radians(deg)/2;return (0,math.sin(a),0,math.cos(a))
# Fixed pressure tunnel and layered stock-family end faces.
cyl(m.root,'RW_GravityHub','white',1.204,-1.8,1.8)
for y in (-1.12,1.12):
 for side in (0,math.pi):
  a=h.Mesh()
  for j in range(8):
   lo=side-.35+.7*j/8;hi=side-.35+.7*(j+1)/8
   a.quad([h.point(1.216,lo,y-.21),h.point(1.216,hi,y-.21),h.point(1.216,hi,y+.21),h.point(1.216,lo,y+.21)],[(math.sin(lo),0,math.cos(lo)),(math.sin(hi),0,math.cos(hi)),(math.sin(hi),0,math.cos(hi)),(math.sin(lo),0,math.cos(lo))],[(1-j/8,0),(1-(j+1)/8,0),(1-(j+1)/8,1),(1-j/8,1)])
  mesh(m.root,'RW_GravityNameplate'+str(y)+'_'+str(side),'gravitylabel',a)
seams=h.Mesh()
for y in (-1.46,-.72,.72,1.46):h.cylinder_surface(seams,1.207,y-.009,y+.009,96)
for j in range(12):
 theta=j*math.tau/12
 for lo,hi in ((-1.76,-.5),(.5,1.76)):h.tube(seams,h.point(1.208,theta,lo),h.point(1.208,theta,hi),.007,6)
mesh(m.root,'RW_GravityHubPanelSeams','graphite',seams)
for sign in (-1,1):
 for key,a in face_mesh().items():
  a.vertices=[(x,sign*(y-2+1.85),sign*z) for x,y,z in a.vertices];a.normals=[(x,sign*y,sign*z) for x,y,z in a.normals]
  mesh(m.root,'RW_GravityEnd_'+str(sign)+'_'+key,key,a)
co=collision_section(-1.79,1.79,1.20,1.20);n=node('RW_GravityHubCollision');n['collider']=dict(type='mesh',trigger=0,convex=1,mesh=dict(vertices=co.vertices,normals=co.normals,uvs=co.uvs,submeshes=[co.triangles]));m.root['children'].append(n)
for y in (-1.6,1.6):cyl(m.root,'RW_GravityFixedMount'+str(y),'steel',1.25,y-.055,y+.055)
for y in (-.43,.43):cyl(m.root,'RW_GravityBearing'+str(y),'graphite',1.40,y-.06,y+.06)
rotor=node('RW_GravityRotor');m.root['children'].append(rotor)
cyl(rotor,'RW_GravityMotor','steel',1.35,-.38,.38)
for y in (-.34,.34):cyl(rotor,'RW_GravityMotorBand'+str(y),'bronze',1.367,y-.025,y+.025)
window_names=[];radius=4.2;minor=.72
for k in range(8):
 frame=node('RW_GravityFrame%02d'%k,(0,0,0),qy(-45*k));rotor['children'].append(frame)
 foldAngle=82 if k in (0,4) else 88
 hinge=node('RW_GravityHinge%02d'%k,(1.72,0,0),qz((foldAngle if k%2==0 else -foldAngle)));frame['children'].append(hinge)
 rail(frame,'RW_GravitySlideSocket%02d'%k,'steel',(1.20,0,0),(1.73,0,0),.12)
 if k in (0,4):
  # Two opposed enclosed pressure passages share the spoke's folding pivot.
  access=h.Mesh()
  for radius0,inward in ((.38,False),(.32,True)):
   a=h.Mesh();h.cylinder_surface(a,radius0,-.1,2.75,48)
   a.vertices=[(y,z,x) for x,y,z in a.vertices];a.normals=[tuple((-1 if inward else 1)*v for v in (y,z,x)) for x,y,z in a.normals]
   from station_endcaps import append
   append(access,a)
  for depth,sign in ((-.1,-1),(2.75,1)):
   a=h.Mesh();h.annulus(a,.32,.38,depth,sign,48);a.vertices=[(y,z,x) for x,y,z in a.vertices];a.normals=[(y,z,x) for x,y,z in a.normals];append(access,a)
  mesh(hinge,'RW_GravityAccessTube%02d'%k,'white',access)
  bands=h.Mesh()
  for depth in (.08,.65,1.3,1.95,2.64):
   for j in range(48):
    a=j*math.tau/48;b=(j+1)*math.tau/48;h.tube(bands,(depth,.389*math.sin(a),.389*math.cos(a)),(depth,.389*math.sin(b),.389*math.cos(b)),.012,8)
  mesh(hinge,'RW_GravityAccessBands%02d'%k,'steel',bands)
  solid(hinge,'RW_GravityAccessCollision%02d'%k,(1.325,0,0),(2.85,.76,.76))
  knuckle=h.Mesh()
  def sphere(a,b):return (1.45+.42*math.cos(a)*math.cos(b),.42*math.sin(b),.42*math.sin(a)*math.cos(b))
  def sn(a,b):return (math.cos(a)*math.cos(b),math.sin(b),math.sin(a)*math.cos(b))
  for i in range(32):
   a=i*math.tau/32;b=(i+1)*math.tau/32
   for j in range(16):
    c=-math.pi/2+j*math.pi/16;d=-math.pi/2+(j+1)*math.pi/16
    knuckle.quad([sphere(a,c),sphere(b,c),sphere(b,d),sphere(a,d)],[sn(a,c),sn(b,c),sn(b,d),sn(a,d)])
  knuckle.vertices=[(x-1.45,y,z) for x,y,z in knuckle.vertices]
  mesh(hinge,'RW_GravityAccessRotarySeal%02d'%k,'graphite',knuckle)
 # Paired pressure-access trusses and contrasting mechanical hinges.
 for z in (-.13,.13):
  rail(hinge,'RW_GravitySpoke%02d_%s'%(k,z),'steel',(0,0,z),(2.75,0,z),.065)
 for i in range(7):
  rail(hinge,'RW_GravityBrace%02d_%02d'%(k,i),'bronze',(i*2.75/7,0,-.13),((i+1)*2.75/7,0,.13),.018)
 hub=node('RW_GravityHingePin%02d'%k,(0,0,0),qz(90));hinge['children'].append(hub);cyl(hub,'RW_GravityHingeHardware%02d'%k,'bronze',.14,-.24,.24)
 pod=node('RW_GravityPod%02d'%k,(.95,0,0),qz(-(foldAngle if k%2==0 else -foldAngle)));pod['scale']=(.5,.85,.7);hinge['children'].append(pod)
 skins={key:h.Mesh() for key in ('white','glass','graphite','steel','bronze')}
 def p(theta,phi,r=minor):return ((radius+r*math.cos(phi))*math.cos(theta)-radius,r*math.sin(phi),(radius+r*math.cos(phi))*math.sin(theta))
 def normal(theta,phi):return (math.cos(phi)*math.cos(theta),math.sin(phi),math.cos(phi)*math.sin(theta))
 lo=-math.pi/8+.001;hi=math.pi/8-.001
 for i in range(24):
  a=lo+(hi-lo)*i/24;b=lo+(hi-lo)*(i+1)/24
  for j in range(24):
   c=j*math.tau/24;d=(j+1)*math.tau/24
   window=(i in (5,6,7,15,16,17) and j in (0,1,22,23))
   key='glass' if window else 'steel' if i in (0,23) or j in (6,18) else 'white'
   skins[key].quad([p(a,c),p(b,c),p(b,d),p(a,d)],[normal(a,c),normal(b,c),normal(b,d),normal(a,d)],[(i/4,j/4),((i+1)/4,j/4),((i+1)/4,(j+1)/4),(i/4,(j+1)/4)])
 for theta,sign in ((lo,-1),(hi,1)):
  center=((radius)*math.cos(theta)-radius,0,radius*math.sin(theta));n=(-math.sin(theta)*sign,0,math.cos(theta)*sign)
  for j in range(24):skins['graphite'].triangle([center,p(theta,j*math.tau/24),p(theta,(j+1)*math.tau/24)],[n]*3,[(.5,.5),(0,0),(1,0)])
  for j in range(24):h.tube(skins['bronze'],p(theta,j*math.tau/24,minor+.008),p(theta,(j+1)*math.tau/24,minor+.008),.012,8)
 # Narrow pressure-panel seams and raised window framing.
 for i in (4,12,20):
  theta=lo+(hi-lo)*i/24
  for j in range(24):h.tube(skins['graphite'],p(theta,j*math.tau/24,minor+.004),p(theta,(j+1)*math.tau/24,minor+.004),.006,6)
 for start in (5,15):
  a=lo+(hi-lo)*start/24;b=lo+(hi-lo)*(start+3)/24
  for theta in (a,b):
   for j in range(8):h.tube(skins['steel'],p(theta,-math.pi/6+math.pi/3*j/8,minor+.012),p(theta,-math.pi/6+math.pi/3*(j+1)/8,minor+.012),.012,8)
  for phi in (-math.pi/6,math.pi/6):
   for j in range(8):h.tube(skins['steel'],p(a+(b-a)*j/8,phi,minor+.012),p(a+(b-a)*(j+1)/8,phi,minor+.012),.012,8)
 for key,a in skins.items():
  name='RW_GravitySector%02d_%s'%(k,key);mesh(pod,name,key,a)
  if key=='glass':window_names.append(name)
 # Four convex boxes approximate each curved pressure sector without a
 # concave mesh collider; they move with the pod's deployment transforms.
 for j in range(4):
  angle=lo+(hi-lo)*(j+.5)/4;n=node('RW_GravityCabinCollision%02d_%d'%(k,j),p(angle,0,0),qy(-math.degrees(angle)));n['collider']=dict(type='box',trigger=0,center=(0,0,0),size=(1.38,1.38,.83));pod['children'].append(n)
 # Shorten only the arm hardware, preserving full-size hinge pins and packs.
 telescopic=node('RW_GravityTelescopic%02d'%k);telescopic['scale']=(.95/2.75,1,1)
 for child in list(hinge['children']):
  if child['name'].startswith(('RW_GravitySpoke','RW_GravityBrace','RW_GravityAccessTube','RW_GravityAccessBands','RW_GravityAccessCollision')):
   hinge['children'].remove(child);telescopic['children'].append(child)
 hinge['children'].append(telescopic)
write(m,GD/f'Models/{ID}.mu')
part=Node('PART',[('name',ID),('module','Part'),('author','SockedRooster'),('rescaleFactor','1'),('node_stack_top','0,1.85,0,0,1,0,2'),('node_stack_bottom','0,-1.85,0,0,-1,0,2'),('attachRules','1,0,1,1,0'),('bulkheadProfiles','size2'),('TechRequired','longTermHabitation'),('entryCost','120000'),('cost','48000'),('category','Utility'),('subcategory','0'),('title','RoosterWorks RW-GRAV-250 Folding Gravity Habitat'),('manufacturer','RoosterWorks'),('description','Four-crew folding/inflatable ring on a fixed 2.5 m axial hub. Eight hinged spokes unfold the packed pressure sections to a 9.84 m outer diameter. Recommend a 5 m launch fairing. Deploy in orbit, then start the visual rotor; 6 rpm corresponds to 0.17 g at the 4.2 m ring center. This is a visual/habitation system, not a source of physical gravity for Kerbals or other parts. Transfer crew through the fixed hub; no exterior hatch. Stop before folding; folding is blocked with crew aboard. Original station end nodes remain stationary.'),('tags','roosterworks station gravity rotating ring centrifuge folding inflatable habitat'),('mass','8'),('CrewCapacity','4'),('vesselType','Station'),('dragModelType','default'),('maximum_drag','.2'),('minimum_drag','.2'),('angularDrag','2'),('crashTolerance','12'),('breakingForce','1000'),('breakingTorque','1000'),('maxTemp','2000'),('skinMaxTemp','2400'),('fuelCrossFeed','true')],[Node('MODEL',[('model','RoosterWorksStationModules/Models/'+ID)]),Node('INTERNAL',[('name','crewCabinInternals')]),Node('MODULE',[('name','ModuleRWGravityRing'),('deployment','0'),('targetDeployment','0'),('running','false'),('phase','0'),('rpm','6'),('deployDuration','30'),('powerRate','.75')]),Node('RESOURCE',[('name','ElectricCharge'),('amount','900'),('maxAmount','900')]),Node('MODULE',[('name','ModuleInventoryPart'),('InventorySlots','8'),('packedVolumeLimit','600')]),Node('VABORGANIZER:NEEDS[VABOrganizer]',[('organizerSubcategory','crewHabitation')]),Node('MODULE:NEEDS[ConnectedLivingSpace]',[('name','ModuleConnectedLivingSpace'),('passable','true')])])
changer=Node('MODULE',[('name','ModuleColorChanger'),('moduleID','RW_GRAV_250_CabinLights'),('shaderProperty','_EmissiveColor'),('animRate','.65'),('animState','false'),('useRate','true'),('toggleInEditor','true'),('toggleInFlight','true'),('toggleName','Toggle Ring Lights'),('eventOnName','Ring Lights On'),('eventOffName','Ring Lights Off'),('toggleAction','true'),('defaultActionGroup','Light')]+[('includedRenderer',n) for n in window_names])
for channel,value in (('redCurve','.93'),('greenCurve','.84'),('blueCurve','.67')):changer.children.append(Node(channel,[('key','0 0'),('key','1 '+value)]))
changer.children.append(Node('alphaCurve',[('key','0 1'),('key','1 1')]))
part.children.append(changer);part.children.append(Node('MODULE',[('name','ModuleRWRingColor'),('ringModel',ID),('ringColor','Original')]))
(GD/f'Parts/{ID}.cfg').write_text(dump(Node('ROOT',children=[part])),encoding='utf-8')
ringmaps=[]
for path,n in walk(m.root):
 if n['name'].startswith(('RW_GravityFixedMount','RW_GravityMotorBand')):
  tex=m.textures[m.materials[n['materials'][0]]['properties']['_MainTex']['index']]['name'];count=len(n['mesh']['submeshes'][0]);ringmaps.append(Node('MESH',[('path',path),('texture',tex),('vertices',str(len(n['mesh']['vertices']))),('triangles',str(count)),('ranges','0:'+str(count))]))
(GD/'Compatibility/GravityRingGeometry.cfg').write_text(dump(Node('ROOT',children=[Node('RW_RING_MAP',[('model',ID)],ringmaps)])),encoding='utf-8')
compat=Node('ROOT',children=[Node('@PART[RW_GRAV_250]:NEEDS[Kerbalism,ProfileDefault]:AFTER[zzzKerbalismDefault]',children=[Node('%RESOURCE['+n+']',[('%name',n),('%amount',a),('%maxAmount',c)]) for n,a,c in [('Food','60.8','60.8'),('Water','30.4','30.4'),('Oxygen','8437.5','8437.5'),('Nitrogen','5725.1','5725.1'),('Waste','0','67.5'),('WasteWater','0','40.5')]]),Node('@PART[RW_GRAV_250]:NEEDS[Kerbalism,FeatureHabitat]:AFTER[zzzKerbalismDefault]',children=[Node('%MODULE[Habitat]',[('%name','Habitat'),('%volume','12'),('%surface','37')])])])
# Conservative fixed-hub habitat only: do not grant always-on deployed volume
# or an artificial-gravity comfort bonus when the ring is stopped/stowed.
part.set('TechRequired','specializedConstruction')
part.set('description',part.get('description')+' Two opposed enclosed pressure-access tubes fold with their spokes and connect the rotary hub to the perimeter.')
(GD/f'Parts/{ID}.cfg').write_text(dump(Node('ROOT',children=[part])),encoding='utf-8')
compat.children.append(Node('@PART[RW_GRAV_250]:NEEDS[CommunityTechTree]:AFTER[CommunityTechTree]',[('@TechRequired','longTermHabitation')]))
(GD/'Compatibility/GravityRing.cfg').write_text('// Fixed-hub life support; visual rotation grants no automatic comfort bonus.\n'+dump(compat),encoding='utf-8')
(R/'Reports').mkdir(exist_ok=True)
(R/'Reports/GRAVITY_RING.json').write_text(json.dumps({'part':ID,'major_radius':4.2,'minor_radius':.72,'diameter':9.84,'crew':4,'stock_IVA':'crewCabinInternals','default_rpm':6,'equivalent_g':(math.tau*6/60)**2*4.2/9.80665,'habitat_model':'fixed hub only, 12 m3; no automatic gravity bonus','triangles':sum(len(s) for _,n in walk(m.root) if 'mesh' in n for s in n['mesh']['submeshes'])},indent=2)+'\n')
p=GD/'RoosterWorksStationModules.version';v=json.loads(p.read_text());v['VERSION']['BUILD']=9;p.write_text(json.dumps(v,indent=2)+'\n')
print('PASS built GRAV-250: fixed hub, eight folded spokes/packed ring sections, pressure windows and convex collision')
