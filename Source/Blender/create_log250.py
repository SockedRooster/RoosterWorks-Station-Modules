"""Blender rebuild of original RW-LOG-250 procedural model; save editable blend."""
import sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'Source'))
from build_log250 import geometry,MODELS
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
collection=bpy.data.collections.new('RoosterWorks / RW-LOG-250 Logistics')
bpy.context.scene.collection.children.link(collection)
root=bpy.data.objects.new('RW_LOG_250',None);collection.objects.link(root)
for mat_name,mesh in geometry().items():
    if not mesh.triangles:continue
    data=bpy.data.meshes.new('Logistics_'+mat_name)
    data.from_pydata(mesh.vertices,[],mesh.triangles);data.update()
    uv=data.uv_layers.new(name='RW_UV')
    for poly in data.polygons:
        for li in poly.loop_indices:uv.data[li].uv=mesh.uvs[data.loops[li].vertex_index]
    ob=bpy.data.objects.new('RW_Log_'+mat_name,data);collection.objects.link(ob);ob.parent=root
    material=bpy.data.materials.new('RW_Log_'+mat_name);material.use_nodes=True
    bsdf=material.node_tree.nodes.get('Principled BSDF')
    tex=material.node_tree.nodes.new('ShaderNodeTexImage')
    tex.image=bpy.data.images.load(str(MODELS/('rwm_'+mat_name+'.png')),check_existing=True)
    material.node_tree.links.new(tex.outputs['Color'],bsdf.inputs['Base Color'])
    bsdf.inputs['Metallic'].default_value=.52 if mat_name in ('bronze','steel','rail') else .07
    bsdf.inputs['Roughness'].default_value=.47
    data.materials.append(material)
    for face in data.polygons:face.use_smooth=mat_name not in ('loglabel',)
light_data=bpy.data.lights.new('Studio','AREA')
light=bpy.data.objects.new('Studio',light_data);bpy.context.scene.collection.objects.link(light)
light.location=(6,-4,6);light_data.energy=1800;light_data.size=7
bpy.ops.object.camera_add(location=(5,-7,4))
cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=5.4;bpy.context.scene.camera=cam
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'RW_LOG_250.blend'))
print('Saved original RoosterWorks logistics station .blend')
