"""Optional Blender import of shipped expansion MU, including colliders.

blender --background --python Source/Blender/create_expansion.py -- RW_HABS_500
Produces an editable, packed .blend alongside this script; no exporter needed.
"""
from pathlib import Path
import sys,bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tools'))
from native_model import load,walk
part=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'RW_HABS_500'
assert part.startswith(('RW_HABS_','RW_')) and ('_500' in part or 'RW_HABS_' in part or part=='RW_ADP_375_500')
model=load(ROOT/f'GameData/RoosterWorksStationModules/Models/{part}.mu')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
materials=[]
for original in model.materials:
    material=bpy.data.materials.new(original['name']);material.use_nodes=True
    texture=material.node_tree.nodes.new('ShaderNodeTexImage')
    name=model.textures[original['properties']['_MainTex']['index']]['name']
    texture.image=bpy.data.images.load(str(ROOT/f'GameData/RoosterWorksStationModules/Models/{name}.png'),check_existing=True)
    material.node_tree.links.new(texture.outputs['Color'],material.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
    materials.append(material)
for path,node in walk(model.root):
    if 'mesh' not in node and 'collider' not in node:continue
    collider=node.get('collider');collision=collider is not None
    if collision and collider['type']=='box':
        bpy.ops.mesh.primitive_cube_add(size=1);obj=bpy.context.object;obj.name=node['name'];obj.dimensions=collider['size'];obj.location=node['position'];obj.rotation_mode='QUATERNION';x,y,z,w=node['rotation'];obj.rotation_quaternion=(w,x,y,z)
    else:
        mesh=collider['mesh'] if collision else node['mesh'];tris=[tri for sub in mesh['submeshes'] for tri in sub]
        data=bpy.data.meshes.new(node['name']);data.from_pydata(mesh['vertices'],[],tris);data.update()
        obj=bpy.data.objects.new(node['name'],data);bpy.context.collection.objects.link(obj)
        if not collision:
            uv=data.uv_layers.new(name='RW_UV')
            for poly in data.polygons:
                for li in poly.loop_indices:uv.data[li].uv=mesh['uvs'][data.loops[li].vertex_index]
            for index in node['materials']:data.materials.append(materials[index])
    obj['KSPTag']=node.get('tag','Untagged');obj['KSPLayer']=node.get('layer',0)
    if collision:obj.hide_render=True;obj.display_type='WIRE'
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f'Source/Blender/{part}.blend'))
