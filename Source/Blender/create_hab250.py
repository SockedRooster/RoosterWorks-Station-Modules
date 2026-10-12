"""Run inside Blender 4.x/5.x to create editable RW-HAB-250 model.

Command-line:
    blender --background --python Source/Blender/create_hab250.py
Or load this file in the Blender Scripting workspace and press Run Script.
Blender is not required for the direct-source KSP .mu builder.
"""
import sys
import math
from pathlib import Path
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent
ROOT=SOURCE.parent
sys.path.insert(0,str(SOURCE))
from build_hab250 import generate_geometry, TEXTURES, MODELS
# Set to 'SideHatch' to generate the alternate exterior in Blender.
EXTERIOR_VARIANT = 'Standard'  # Standard, SideHatch
CABIN_LIGHTS_PREVIEW = False  # True shows soft warm-white glass in Blender

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for material in list(bpy.data.materials):
    if material.users==0:bpy.data.materials.remove(material)

collection=bpy.data.collections.new('RW-HAB-250 | Exterior')
bpy.context.scene.collection.children.link(collection)
main=bpy.data.objects.new('RW_HAB_250',None)
collection.objects.link(main)

for name,mesh in generate_geometry(EXTERIOR_VARIANT).items():
    data=bpy.data.meshes.new('Hab250_'+name+'_mesh')
    data.from_pydata(mesh.vertices,[],mesh.triangles)
    data.update()
    uv=data.uv_layers.new(name='RW_UV')
    for polygon in data.polygons:
        for loop in polygon.loop_indices:
            uv.data[loop].uv=mesh.uvs[data.loops[loop].vertex_index]
    obj=bpy.data.objects.new('RW_'+name.title(),data)
    collection.objects.link(obj)
    obj.parent=main
    material=bpy.data.materials.new('RW_'+name)
    material.use_nodes=True
    nodes=material.node_tree.nodes
    shader=nodes.get('Principled BSDF')
    image=nodes.new('ShaderNodeTexImage')
    image.image=bpy.data.images.load(str(MODELS/f'rwm_{name}.png'),check_existing=True)
    material.node_tree.links.new(image.outputs['Color'],shader.inputs['Base Color'])
    shader.inputs['Metallic'].default_value=.7 if name in ('steel','bronze','rail') else .08
    shader.inputs['Roughness'].default_value=.27 if name=='glass' else .48
    if name=='glass':
        shader.inputs['Metallic'].default_value=.45
        if 'Emission Color' in shader.inputs:
            shader.inputs['Emission Color'].default_value=(1.0,.90,.72,1.0)
        if 'Emission Strength' in shader.inputs:
            shader.inputs['Emission Strength'].default_value=(.55 if CABIN_LIGHTS_PREVIEW else 0.0)
    data.materials.append(material)
    for p in data.polygons:p.use_smooth=name not in ('label',)

# Recessed, flush 2.5m circular end bulkheads are model geometry, not
# separate protruding docking-port parts.
# Model-pipeline guides: hidden in final renders (the .mu builder generates
# actual KSP collision nodes, these helpers are artist-only).
coll=bpy.data.collections.new('RW | Collider Guides (not exported)')
bpy.context.scene.collection.children.link(coll)
for sign, label in ((1,'Top'),(-1,'Bottom')):
    bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.59,depth=.18,location=(0,sign*1.88,0))
    obj=bpy.context.object
    obj.name='Guide_Docking_'+label
    for c in list(obj.users_collection):c.objects.unlink(obj)
    coll.objects.link(obj)
    obj.display_type='WIRE'
    obj.hide_render=True

# v0.4.3 always-active EVA trigger GUIDE. The native model writer generates the
# working KSP tagged Airlock collider; Blender object is a non-exported guide.
# Side hatch replaces the lower/front bank (row=2, col=1); local +Z faces
# outward from its 60 degree centre. All measurements in metres.
if True:  # EVA Airlock is always active; Standard Windows is visual-only.
    from mathutils import Quaternion
    angle=math.tau/6
    y=-1.730+(2.5)*(3.460/8)
    marker=bpy.data.objects.new('RW_HAB250_EVA_Airlock_GUIDE',None)
    coll.objects.link(marker)
    marker.location=(1.43*math.sin(angle), y, 1.43*math.cos(angle))
    marker.rotation_mode='QUATERNION'
    marker.rotation_quaternion=Quaternion((math.cos(angle/2),0,math.sin(angle/2),0))
    marker.empty_display_type='CUBE'
    marker.empty_display_size=.35
    marker['KSP_UnityTag']='Airlock'
    marker['KSP_UnityLayer']=21
    marker['KSP_TriggerCollider']=True
    marker.hide_render=True

# Perspective rendering studio for inspection only. All meshes stay editable.
light_data=bpy.data.lights.new('StudioSoftbox','AREA')
light=bpy.data.objects.new('StudioSoftbox',light_data)
bpy.context.scene.collection.objects.link(light)
light.location=(5,-5,7)
light_data.energy=1700
light_data.shape='DISK'
light_data.size=8

bpy.ops.object.camera_add(location=(7,-9,5.4))
cam=bpy.context.object
cam.name='Preview_Camera'
vec=Vector((0,0,0))-cam.location
cam.rotation_euler=vec.to_track_quat('-Z','Y').to_euler()
cam.data.type='ORTHO'
cam.data.ortho_scale=7.0
bpy.context.scene.camera=cam
bpy.context.scene.render.engine='BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x=1400
bpy.context.scene.render.resolution_y=1200
bpy.context.scene.render.resolution_percentage=100
bpy.context.scene.render.image_settings.file_format='PNG'
bpy.context.scene.world.color=(.13,.17,.21)

for obj in bpy.context.selected_objects:obj.select_set(False)
main.select_set(True)
bpy.context.view_layer.objects.active=main
# Embed source textures in .blend so it remains usable when moved.
bpy.ops.file.pack_all()
out=HERE/'RW_HAB_250.blend'
bpy.ops.wm.save_as_mainfile(filepath=str(out))
print('Blender source saved:',out)
print('NOTE: Native KSP .mu is generated by python Source/build_hab250.py')
