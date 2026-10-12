"""Run in Blender 4.2+/5.x; creates editable RW-CMD-250 .blend from source mesh."""
import sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'Source'))
from build_cmd250 import geometry,MODELS

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
coll=bpy.data.collections.new('RW-CMD-250 / Compact Station Command')
bpy.context.scene.collection.children.link(coll)
root=bpy.data.objects.new('RW_CMD_250',None)
coll.objects.link(root)
for name,mesh in geometry().items():
    if not mesh.triangles:continue
    md=bpy.data.meshes.new('RW_CMD_'+name+'_mesh')
    md.from_pydata(mesh.vertices,[],mesh.triangles)
    md.update()
    uv=md.uv_layers.new(name='RW_UV')
    for poly in md.polygons:
        for loop in poly.loop_indices:
            uv.data[loop].uv=mesh.uvs[md.loops[loop].vertex_index]
    obj=bpy.data.objects.new('CMD_'+name,md)
    coll.objects.link(obj);obj.parent=root
    material=bpy.data.materials.new('RW_CMD_'+name)
    material.use_nodes=True
    shader=material.node_tree.nodes.get('Principled BSDF')
    img=material.node_tree.nodes.new('ShaderNodeTexImage')
    img.image=bpy.data.images.load(str(MODELS/f'rwm_{name}.png'),check_existing=True)
    material.node_tree.links.new(img.outputs['Color'],shader.inputs['Base Color'])
    shader.inputs['Metallic'].default_value=.58 if name in ('steel','bronze','rail') else .12
    shader.inputs['Roughness'].default_value=.33 if name=='glass' else .45
    md.materials.append(material)
    for face in md.polygons:face.use_smooth=name not in ('cmdlabel',)
light_data=bpy.data.lights.new('StudioSoftbox','AREA')
light=bpy.data.objects.new('StudioSoftbox',light_data)
bpy.context.scene.collection.objects.link(light)
light.location=(6,-4,7);light_data.energy=1700;light_data.size=8
bpy.ops.object.camera_add(location=(7,-9,4.5))
cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=5.5
bpy.context.scene.camera=cam
bpy.context.scene.render.engine='BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x=1400
bpy.context.scene.render.resolution_y=1100
bpy.ops.file.pack_all()
out=HERE/'RW_CMD_250.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
print('RW-CMD-250 editable .blend saved:',out)
