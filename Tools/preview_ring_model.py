"""Apply the shipped exact ring selection to an in-memory preview model."""
from pathlib import Path
import sys,copy
from native_model import walk
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Source'))
from config_nodes import parse
def apply(model,color):
    tree=parse((ROOT/'GameData/RoosterWorksStationModules/Compatibility/RingGeometry.cfg').read_text())
    mapping=next(n for n in tree.children if n.get('model')==model.name)
    nodes=dict(walk(model.root))
    for spec in mapping.children:
        node=nodes[spec.get('path')];triangles=node['mesh']['submeshes'][0];selected=set()
        for pair in spec.get('ranges').split(','):
            start,count=map(int,pair.split(':'));selected.update(range(start,start+count))
        node['mesh']['submeshes']=[[t for i,t in enumerate(triangles) if i not in selected],[t for i,t in enumerate(triangles) if i in selected]]
        mat=copy.deepcopy(model.materials[node['materials'][0]])
        mat['properties']['_MainTex']['index']=len(model.textures)
        model.textures.append({'name':f"rwm_ring_{spec.get('texture')}_{color.lower()}",'type':0})
        node['materials'].append(len(model.materials));model.materials.append(mat)
