"""Optional Blender script: reconstruct the editable RW-CUP-250 source from geometry."""
import sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'Source'))
from build_cup250 import geometry,MODELS
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
collection=bpy.data.collections.new('RoosterWorks Cupola / RW-CUP-250')
bpy.context.scene.collection.children.link(collection)
root=bpy.data.objects.new('RW_CUP_250',None);collection.objects.link(root)
for mat_name,mesh in geometry().items():
    if not mesh.triangles:continue
    data=bpy.data.meshes.new('Cup_'+mat_name)
    data.from_pydata(mesh.vertices,[],mesh.triangles);data.update()
    uv=data.uv_layers.new(name='RW_UV')
    for poly in data.polygons:
        for idx in poly.loop_indices:uv.data[idx].uv=mesh.uvs[data.loops[idx].vertex_index]
    ob=bpy.data.objects.new('RW_Cup_'+mat_name,data);collection.objects.link(ob);ob.parent=root
    mat=bpy.data.materials.new('RW_Cup_'+mat_name);mat.use_nodes=True
    shader=mat.node_tree.nodes.get('Principled BSDF')
    tex=mat.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image=bpy.data.images.load(str(MODELS/('rwm_'+mat_name+'.png')),check_existing=True)
    mat.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color'])
    shader.inputs['Metallic'].default_value=.52 if mat_name in ('steel','bronze','rail') else .07
    shader.inputs['Roughness'].default_value=.20 if mat_name=='glass' else .48
    data.materials.append(mat)
    for f in data.polygons:f.use_smooth=mat_name not in ('cuplabel',)
light_data=bpy.data.lights.new('Studio','AREA')
light=bpy.data.objects.new('Studio',light_data);bpy.context.scene.collection.objects.link(light)
light.location=(5,-4,6);light_data.energy=1600;light_data.size=7
bpy.ops.object.camera_add(location=(5,-7,3.4))
cam=bpy.context.object;cam.rotation_euler=(Vector((0,-.1,0))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=4.7;bpy.context.scene.camera=cam
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'RW_CUP_250.blend'))
print('Saved original RoosterWorks cupola source .blend')
