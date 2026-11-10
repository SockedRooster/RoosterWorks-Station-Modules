"""Pack and preview exact native orbital endcap geometry."""
from pathlib import Path
import sys,math,bpy
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.dont_write_bytecode=True
source=(R/'Tools/create_gravity_blend.py').read_text().split("scene=bpy.context.scene;scene.name='RW_GRAV_250'")[0]
exec(compile(source,str(R/'Tools/create_gravity_blend.py'),'exec'))
scene=bpy.context.scene;scene.name='RW_END_250_125';scene.unit_settings.system='METRIC'
import_model(GD/'Models/RW_END_250_125.mu',scene)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/Blender/RW_END_250_125.blend'));print('PASS packed editable station endcap',flush=True)
def aim(obj,p):obj.rotation_euler=(Vector(p)-obj.location).to_track_quat('-Z','Y').to_euler()
scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=28;scene.cycles.use_denoising=True;scene.render.resolution_x=1100;scene.render.resolution_y=900;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
world=bpy.data.worlds.new('Preview orbital endcap');scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.17,.22,.28,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6
for pos,energy,size in [((-3,-4,5),950,4),((4,2,4),650,4)]:
 data=bpy.data.lights.new('Preview light','AREA');obj=bpy.data.objects.new('Preview light',data);scene.collection.objects.link(obj);obj.location=pos;data.energy=energy;data.shape='DISK';data.size=size;aim(obj,(0,0,0))
bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-.47));plane=bpy.context.object;plane.name='Preview floor';mat=bpy.data.materials.new('Preview concrete');mat.diffuse_color=(.18,.21,.24,1);plane.data.materials.append(mat)
data=bpy.data.cameras.new('Preview camera');cam=bpy.data.objects.new('Preview camera',data);scene.collection.objects.link(cam);scene.camera=cam;data.type='ORTHO';data.ortho_scale=3.65
out=R/'Media/StationEndcap';out.mkdir(exist_ok=True)
for label,pos in [('Nose',(3,-4.2,3.2)),('Base',(-3,4.2,2.8))]:
 cam.location=pos;aim(cam,(0,0,-.05));scene.view_settings.view_transform='AgX';scene.render.filepath=str(out/(label+'.png'));bpy.ops.render.render(write_still=True);print('PASS rendered station endcap '+label,flush=True)
