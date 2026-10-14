"""Reconstruct the detailed greenhouse from its exact Python geometry in Blender.

Run Blender --background --python Source/Blender/create_grn250.py.
Outputs an editable, texture-packed .blend; does not export physics or MU.
"""
from pathlib import Path
import sys
import bpy
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'Source'))
from build_grn250 import geometry,MODELS
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
collection=bpy.data.collections.new('RoosterWorks / GRN-250');bpy.context.scene.collection.children.link(collection)
root=bpy.data.objects.new('RW_GRN_250',None);collection.objects.link(root)
for name,mesh in geometry().items():
    if not mesh.triangles:continue
    data=bpy.data.meshes.new('Greenhouse_'+name);data.from_pydata(mesh.vertices,[],mesh.triangles);data.update()
    uv=data.uv_layers.new(name='RW_UV')
    for poly in data.polygons:
        for li in poly.loop_indices:uv.data[li].uv=mesh.uvs[data.loops[li].vertex_index]
    obj=bpy.data.objects.new('RW_Greenhouse_'+name,data);collection.objects.link(obj);obj.parent=root
    mat=bpy.data.materials.new('RW_Greenhouse_'+name);mat.use_nodes=True
    tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(MODELS/f'rwm_{name}.png'),check_existing=True)
    shader=mat.node_tree.nodes.get('Principled BSDF');mat.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color'])
    shader.inputs['Metallic'].default_value=.50 if name in ('bronze','steel','rail') else .05
    shader.inputs['Roughness'].default_value=.48
    if name=='grnglass':
        shader.inputs['Alpha'].default_value=36/255
        shader.inputs['Roughness'].default_value=.18
        if hasattr(mat,'surface_render_method'):mat.surface_render_method='DITHERED'
        elif hasattr(mat,'blend_method'):mat.blend_method='BLEND'
    if name in ('grnlamp','grninspection'):
        emission=shader.inputs.get('Emission Color') or shader.inputs.get('Emission')
        if emission:mat.node_tree.links.new(tex.outputs['Color'],emission)
    data.materials.append(mat)
for y in (-.74,-.15,.44,1.03):
    data=bpy.data.lights.new('RW_GreenhouseInspectionLight','POINT');data.energy=70;data.color=(1,.91,.76)
    obj=bpy.data.objects.new('RW_GreenhouseInspectionLight',data);bpy.context.collection.objects.link(obj);obj.location=(0,y,0)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'Source/Blender/RW_GRN_250.blend'))
