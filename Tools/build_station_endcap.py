"""Orbital derivative of the accepted ground endcap, without underside hoses.

All ground/current station inputs are read-only. The orbital model is Y-axial
and self-contained in Station Modules, with no Ground Modules dependency.
"""
from pathlib import Path
import sys,copy,json,hashlib,math
import numpy as np
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[1];W=R.parent;sys.path[:0]=[str(R/'Tools'),str(R/'Source')]
from native_model import load,walk
from native_derivatives import write
from config_nodes import Node,parse,dump
from build_ring_options import components
from appearance_textures import label,font
from PIL import ImageDraw
GD=R/'GameData/RoosterWorksStationModules';BG=W/'rw-v075dev9/GameData/RoosterWorksStationModules';GROUND=W/'ground-hotpatch-v23/GameData/RoosterWorksGroundModules'
ID='RW_END_250_125';A=np.array([[0,0,-1],[-1,0,0],[0,1,0]],dtype=float)

def compact(mesh,remove):
 triangles=[t for i,t in enumerate(mesh['submeshes'][0]) if i not in remove]
 used=sorted({v for t in triangles for v in t});remap={v:i for i,v in enumerate(used)}
 for key in ('vertices','normals','uvs','uv2','colors','tangents'):
  if key in mesh:mesh[key]=[mesh[key][v] for v in used]
 mesh['submeshes']=[[tuple(remap[v] for v in t) for t in triangles]]

def main():
 protected={p.relative_to(W).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for base in (W/'rw-v075dev9',W/'ground-hotpatch-v23') for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 (R/'Reports/ENDCAP_PROTECTED_INPUTS.json').write_text(json.dumps(protected,indent=2)+'\n')
 model=load(GROUND/'Models/RW_GND_END_250_125.mu');model.name=ID;model.root['name']=ID
 removed_groups=0;removed_triangles=0
 for _,n in walk(model.root):
  if n['name']=='RW_Endcap_graphite':
   mesh=n['mesh'];v=np.array(mesh['vertices']);tri=mesh['submeshes'][0];remove=set()
   for group in components(mesh):
    indices=sorted({i for t in group for i in tri[t]});points=v[indices]
    # All 104 twelve-sided hose segments, without selecting the two nearby
    # twenty-triangle captive bolts or the connected rounded shell.
    if len(group)==24 and points[:,1].max()<-.40 and np.abs(points[:,2]).min()>.20 and np.abs(points[:,2]).max()<.75:
     remove.update(group);removed_groups+=1
   removed_triangles=len(remove);compact(mesh,remove)
 assert removed_groups==104 and removed_triangles==2496,(removed_groups,removed_triangles)
 for _,n in walk(model.root):
  n['position']=tuple(A@np.array(n['position']))
  if n['name'].startswith('RW_Dock_'):
   n['name']='RW_StationEndDock';n['position']=(0,.45,0);n['rotation']=(-math.sin(math.pi/4),0,0,math.cos(math.pi/4))
  else:assert np.allclose(n['rotation'],(0,0,0,1)),n['name']
  for mesh in ([n['mesh']] if 'mesh' in n else [])+([n['collider']['mesh']] if n.get('collider',{}).get('type')=='mesh' else []):
   mesh['vertices']=[tuple(A@np.array(v)) for v in mesh['vertices']];mesh['normals']=[tuple(A@np.array(v)) for v in mesh['normals']]
 for material in model.materials:material['name']=material['name'].replace('GroundEndcap','StationEndcap')
 for texture in model.textures:
  old=texture['name']
  if old=='rwm_gnd_endlabel':texture['name']='rwm_station_endlabel'
  elif not (GD/'Models'/(old+'.png')).exists():(GD/'Models'/(old+'.png')).write_bytes((GROUND/'Models'/(old+'.png')).read_bytes())
 im=label('END-250/125','ORBITAL ENDCAP');draw=ImageDraw.Draw(im);draw.rectangle((47,47,976,86),fill=(48,64,70));draw.text((65,49),'STATION SYSTEMS   /   2.5 M TO 1.25 M',font=font(23,True),fill=(229,232,221));im.save(GD/'Models/rwm_station_endlabel.png',optimize=True)
 write(model,GD/f'Models/{ID}.mu')
 old=parse((GROUND/'Parts/RW_GND_END_250_125.cfg').read_text()).children[0];p=copy.deepcopy(old);p.header='PART';p.set('name',ID);p.set('title','RoosterWorks RW-END-250/125 Rounded Station Endcap');p.set('vesselType','Station');p.set('node_stack_top','0, .45, 0, 0, 1, 0, 1');p.set('node_stack_bottom','0, -.45, 0, 0, -1, 0, 2');p.set('mass','.30');p.set('cost','1250');p.set('breakingForce','350');p.set('breakingTorque','350')
 p.set('description','Rounded orbital 2.5 m to 1.25 m endcap, 0.9 m long. Clean insulated shoulder, recessed pressure faces, grab rails and matching station labels; no ground hoses, legs or stairs. Large end is a structural size2 attachment; small end has one stock-compatible size1 docking port. White/Grey metal surface and independent ring colors. Illuminated end windows follow Module Lights. Resource crossfeed enabled, docking staging disabled. No crew capacity, habitat or exterior EVA hatch.')
 p.set('tags','roosterworks station orbital rounded endcap adapter reducer dome docking 2.5 1.25 size1 size2')
 p.children=[n for n in p.children if n.get('name')!='ModuleRWGroundDocking']
 for n in p.children:
  if n.header=='MODEL':n.set('model','RoosterWorksStationModules/Models/'+ID)
  if n.get('name')=='ModuleRWRingColor':n.set('ringModel',ID)
  if n.get('name')=='ModuleDockingNode':n.set('nodeTransformName','RW_StationEndDock');n.set('controlTransformName','RW_StationEndDock')
  if n.get('name')=='ModuleColorChanger':n.set('moduleID',ID+'_EndLights')
 (GD/f'Parts/{ID}.cfg').write_text(dump(Node('ROOT',children=[p])))
 maps=parse((GROUND/'Compatibility/EndcapRingGeometry.cfg').read_text());rule=maps.children[0];rule.set('model',ID)
 for entry in rule.children:entry.set('path',entry.get('path').replace('/RW_GND_END_250_125/','/'+ID+'/'))
 organizer=Node('@PART['+ID+']:NEEDS[VABOrganizer]:FINAL',children=[Node('!VABORGANIZER,*'),Node('VABORGANIZER',[('organizerSubcategory','crewAdapters')])])
 (GD/'Compatibility/RoundedStationEndcap.cfg').write_text(dump(Node('ROOT',children=[rule,organizer])))
 fixture=[];nodes=dict(walk(model.root))
 for entry in rule.children:
  mesh=nodes[entry.get('path')]['mesh'];fixture.append({'path':entry.get('path'),'texture':entry.get('texture'),'vertexCount':len(mesh['vertices']),'triangles':[i for tri in mesh['submeshes'][0] for i in tri],'ranges':entry.get('ranges')})
 (R/'Reports/ENDCAP_COLOR_FIXTURE.json').write_text(json.dumps(fixture,separators=(',',':'))+'\n')
 v=GD/'RoosterWorksStationModules.version';data=json.loads(v.read_text());data['VERSION']['BUILD']=10;v.write_text(json.dumps(data,indent=2)+'\n')
 (R/'Reports/STATION_ENDCAP.json').write_text(json.dumps({'id':ID,'source':'ground-hotpatch-v23','removed_hose_segments':removed_groups,'removed_hose_triangles':removed_triangles,'axis':'Y','length_m':.9,'large_m':2.5,'small_m':1.25,'mass_t':.30,'small_end_docking_only':True,'source_to_station_rotation':A.tolist()},indent=2)+'\n')
 for path,digest in protected.items():assert hashlib.sha256((W/path).read_bytes()).hexdigest()==digest,path
 (R/'CHECKSUMS-SHA256.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(R).as_posix()+'\n' for p in sorted((R/'GameData').rglob('*')) if p.is_file()))
 print('PASS built Y-axial rounded station endcap; removed 104 hose segments; size2 structural base / size1 docking nose; standalone core assets')

if __name__=='__main__':main()
