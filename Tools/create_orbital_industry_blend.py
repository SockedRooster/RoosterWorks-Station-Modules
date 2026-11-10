"""Editable scenes and honest previews of exact new native orbital geometry."""
from pathlib import Path
import sys,math,bpy
from mathutils import Vector
R=Path(__file__).resolve().parents[1];sys.dont_write_bytecode=True
helper=R/'Tools/create_gravity_blend.py';source=helper.read_text().split("scene=bpy.context.scene;scene.name='RW_GRAV_250'")[0]
source=source.replace("key=(src['name'],src['shader'])", "key=(src['name'],src['shader'],model.textures[src['properties']['_MainTex']['index']]['name'])")
exec(compile(source,str(helper),'exec'))
for i,role in enumerate(('ISRU','NST','CEN','NSM')):
 scene=bpy.context.scene if i==0 else bpy.data.scenes.new(role);scene.name='RW_'+role+'_250';scene.unit_settings.system='METRIC'
 import_model(GD/f'Models/RW_{role}_250.mu',scene)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/Blender/RW_OrbitalIndustry.blend'))
print('PASS packed four native-equivalent orbital industry scenes',flush=True)

def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
out=R/'Media/OrbitalIndustry';out.mkdir(exist_ok=True)
selected=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ('ISRU','NST','CEN','NSM')
for role in selected:
 scene=bpy.data.scenes['RW_'+role+'_250'];bpy.context.window.scene=scene
 scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=20;scene.cycles.use_denoising=True;scene.render.resolution_x=1000;scene.render.resolution_y=850;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
 world=bpy.data.worlds.new('Preview orbital '+role);scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.07,.11,.17,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.65
 for pos,energy,size in [((-5,-4,6),1400,4),((4,3,4),1100,4)]:
  data=bpy.data.lights.new('Preview light','AREA');o=bpy.data.objects.new('Preview light',data);scene.collection.objects.link(o);o.location=pos;data.energy=energy;data.shape='DISK';data.size=size;aim(o,(0,0,0))
 data=bpy.data.cameras.new('Preview camera');o=bpy.data.objects.new('Preview camera',data);scene.collection.objects.link(o);scene.camera=o;data.type='ORTHO';data.ortho_scale=5.4;o.location=(-5,-4,3.8);aim(o,(0,0,0))
 scene.view_settings.view_transform='AgX';scene.render.filepath=str(out/(role+'.png'));bpy.ops.render.render(write_still=True);print('PASS rendered orbital '+role,flush=True)
