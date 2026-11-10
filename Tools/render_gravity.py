from pathlib import Path
import bpy,math
from mathutils import Vector
R=Path(__file__).resolve().parents[1];out=R/'Media/GravityRing';out.mkdir(exist_ok=True)
scene=bpy.context.scene
def aim(obj,p):obj.rotation_euler=(Vector(p)-obj.location).to_track_quat('-Z','Y').to_euler()
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
for label,d in [('Stowed',0),('Unfolding',.5),('Deployed',1)]:
 for o in list(scene.objects):
  if o.name.startswith('Preview '):bpy.data.objects.remove(o,do_unlink=True)
 for i in range(8):
  folded=82 if i in (0,4) else 88
  angle=math.radians((folded if i%2==0 else -folded)*(1-smooth(d/.65)))
  scene.objects['RW_GravityHinge%02d'%i].rotation_euler=(0,-angle,0)
  reach=smooth(d/.55);inflate=smooth((d-.55)/.45);length=.95+1.8*reach
  scene.objects['RW_GravityHinge%02d'%i].location.x=1.72-.27*reach
  scene.objects['RW_GravityTelescopic%02d'%i].scale=(length/2.75,1,1)
  pod=scene.objects['RW_GravityPod%02d'%i];pod.rotation_euler=(0,angle,0);pod.location.x=length;pod.scale=(.5+.5*inflate,.85+.15*inflate,.7+.3*inflate)
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=32;scene.cycles.use_denoising=True;scene.render.resolution_x=1200;scene.render.resolution_y=1000;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
 world=bpy.data.worlds.new('Preview World '+label);scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.14,.19,.25,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
 for k,pos,energy,size in [('key',(4,-5,9),1400,7),('rim',(-6,1,6),1100,5)]:
  data=bpy.data.lights.new('Preview '+k,'AREA');o=bpy.data.objects.new('Preview '+k,data);scene.collection.objects.link(o);o.location=pos;aim(o,(0,0,0));data.energy=energy;data.shape='DISK';data.size=size
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-3.15 if d<.6 else -1.95));floor=bpy.context.object;floor.name='Preview Floor';mat=bpy.data.materials.new('Preview Floor Material');mat.diffuse_color=(.15,.18,.22,1);floor.data.materials.append(mat)
 data=bpy.data.cameras.new('Preview Camera');cam=bpy.data.objects.new('Preview Camera',data);scene.collection.objects.link(cam);cam.location=(10,-14,10);aim(cam,(0,0,0));data.type='ORTHO';data.ortho_scale=12.3 if d>.6 else 8.5;scene.camera=cam
 scene.view_settings.view_transform='AgX';scene.render.filepath=str(out/(label+'.png'));bpy.ops.render.render(write_still=True);print('PASS rendered gravity ring '+label,flush=True)
