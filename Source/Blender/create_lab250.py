"""Run inside Blender 4.2+/5.x: import the procedural RW-LAB-250 geometry,
create editable meshes + material nodes, pack textures, and save .blend.
Use python Source/build_lab250.py to generate the native KSP .mu instead.
"""
import sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'Source'))
from build_lab250 import geometry,MODELS

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
coll=bpy.data.collections.new('RW-LAB-250 / Orbital Science')
bpy.context.scene.collection.children.link(coll)
root=bpy.data.objects.new('RW_LAB_250',None)
coll.objects.link(root)
for name,mesh in geometry().items():
    if not mesh.triangles:continue
    md=bpy.data.meshes.new('RW_LAB_'+name+'_mesh')
    md.from_pydata(mesh.vertices,[],mesh.triangles)
    md.update()
    uv=md.uv_layers.new(name='RW_UV')
    for polygon in md.polygons:
        for loop_id in polygon.loop_indices:
            uv.data[loop_id].uv=mesh.uvs[md.loops[loop_id].vertex_index]
    ob=bpy.data.objects.new('LAB_'+name,md)
    coll.objects.link(ob);ob.parent=root
    material=bpy.data.materials.new('RW_LAB_'+name)
    material.use_nodes=True
    shade=material.node_tree.nodes.get('Principled BSDF')
    img=material.node_tree.nodes.new('ShaderNodeTexImage')
    img.image=bpy.data.images.load(str(MODELS/f'rwm_{name}.png'),check_existing=True)
    material.node_tree.links.new(img.outputs['Color'],shade.inputs['Base Color'])
    shade.inputs['Metallic'].default_value=.55 if name in ('steel','bronze','rail') else .10
    shade.inputs['Roughness'].default_value=.3 if name=='glass' else .46
    md.materials.append(material)
    for f in md.polygons:f.use_smooth=(name not in ('lablabel',))
lightdata=bpy.data.lights.new('StudioSoftbox','AREA')
light=bpy.data.objects.new('StudioSoftbox',lightdata)
bpy.context.scene.collection.objects.link(light)
light.location=(6,-4,7);lightdata.energy=1700;lightdata.size=8
bpy.ops.object.camera_add(location=(7,-9,5.4))
cam=bpy.context.object
cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO';cam.data.ortho_scale=7.0
bpy.context.scene.camera=cam
bpy.context.scene.render.engine='BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x=1400
bpy.context.scene.render.resolution_y=1200
bpy.ops.file.pack_all()
out=HERE/'RW_LAB_250.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
print('Editable lab saved:',out)
