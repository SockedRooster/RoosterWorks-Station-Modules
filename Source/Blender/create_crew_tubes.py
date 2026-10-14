"""Optional Blender rebuild of exact shipped passage MU, including colliders.

Blender --background --python Source/Blender/create_crew_tubes.py -- RW_ELB_375
Outputs a packed editable .blend. No runtime/physics exporter is required.
"""
from pathlib import Path
import sys
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tools'))
from native_model import load,walk
part=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'RW_TUB_250'
assert part in ('RW_TUB_250','RW_TUB_375','RW_ELB_250','RW_ELB_375')
model=load(ROOT/f'GameData/RoosterWorksStationModules/Models/{part}.mu')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
materials=[]
for src in model.materials:
    mat=bpy.data.materials.new(src['name']);mat.use_nodes=True
    tex=mat.node_tree.nodes.new('ShaderNodeTexImage');name=model.textures[src['properties']['_MainTex']['index']]['name']
    tex.image=bpy.data.images.load(str(ROOT/f'GameData/RoosterWorksStationModules/Models/{name}.png'),check_existing=True)
    shader=mat.node_tree.nodes.get('Principled BSDF');mat.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color']);materials.append(mat)
for path,node in walk(model.root):
    if 'mesh' not in node and 'collider' not in node:continue
    collision='collider' in node;mesh=node['collider']['mesh'] if collision else node['mesh']
    tris=[tri for sub in mesh['submeshes'] for tri in sub]
    data=bpy.data.meshes.new(node['name']);data.from_pydata(mesh['vertices'],[],tris);data.update()
    obj=bpy.data.objects.new(node['name'],data);bpy.context.collection.objects.link(obj)
    if collision:obj.hide_render=True;obj.display_type='WIRE';continue
    uv=data.uv_layers.new(name='RW_UV')
    for poly in data.polygons:
        for li in poly.loop_indices:uv.data[li].uv=mesh['uvs'][data.loops[li].vertex_index]
    for index in node['materials']:data.materials.append(materials[index])
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f'Source/Blender/{part}.blend'))
