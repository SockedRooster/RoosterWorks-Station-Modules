"""Reconstruct a native large model in Blender: -- --part HAB --variant Standard.

Optional source tool, not required to build MU. Lamp energy is a Blender preview
setting; the native MU range/intensity and stock runtime remain authoritative.
"""
from pathlib import Path
import sys,argparse
import bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'Tools'))
from native_model import load,walk
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
p=argparse.ArgumentParser();p.add_argument('--part',default='HAB',choices=('HAB','LAB','CMD','HUB','CUP','LOG','AIR','PWR','GRN'));p.add_argument('--variant',default='Standard',choices=('Standard','SideHatch'));args=p.parse_args(args)
model=load(ROOT/f'GameData/RoosterWorksStationModules/Models/RW_{args.part}_375.mu')
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for path,node in walk(model.root):
    if args.part=='HAB' and (args.variant=='Standard' and '/SideHatch/' in path or args.variant=='SideHatch' and '/WindowBankStandard/' in path):continue
    if 'light' in node:
        data=bpy.data.lights.new(node['name'],'POINT');data.color=node['light']['color'][:3];data.energy=50*node['light']['intensity']
        obj=bpy.data.objects.new(node['name'],data);bpy.context.collection.objects.link(obj);obj.location=node['position']
    if 'mesh' not in node:continue
    m=node['mesh'];data=bpy.data.meshes.new(node['name']);data.from_pydata(m['vertices'],[],[tri for sub in m['submeshes'] for tri in sub]);data.update()
    uv=data.uv_layers.new(name='RW_UV')
    for poly in data.polygons:
        for li in poly.loop_indices:uv.data[li].uv=m['uvs'][data.loops[li].vertex_index]
    obj=bpy.data.objects.new(node['name'],data);bpy.context.collection.objects.link(obj)
    start=0
    for tris,index in zip(m['submeshes'],node['materials']):
        source=model.materials[index];texname=model.textures[source['properties']['_MainTex']['index']]['name']
        mat=bpy.data.materials.new(source['name']);mat.use_nodes=True;shader=mat.node_tree.nodes.get('Principled BSDF')
        tex=mat.node_tree.nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(ROOT/f'GameData/RoosterWorksStationModules/Models/{texname}.png'),check_existing=True)
        mat.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color'])
        if source['shader']=='KSP/Alpha/Translucent':
            mat.node_tree.links.new(tex.outputs['Alpha'],shader.inputs['Alpha'])
            if hasattr(mat,'surface_render_method'):mat.surface_render_method='DITHERED'
            elif hasattr(mat,'blend_method'):mat.blend_method='BLEND'
        if texname=='rwm_grninspection':
            emission=shader.inputs.get('Emission Color') or shader.inputs.get('Emission')
            if emission:mat.node_tree.links.new(tex.outputs['Color'],emission)
        slot=len(data.materials);data.materials.append(mat)
        for poly in data.polygons[start:start+len(tris)]:poly.material_index=slot
        start+=len(tris)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/f'Source/Blender/RW_{args.part}_375.blend'))
