"""Regression checks against recorded authentic v0.7.0-dev.3 native assets.

Golden fingerprints are captured from the supplied baseline, never from the
appearance candidate. This test also parses every exported native mesh.
"""
from pathlib import Path

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Source'))
from electric_charge_balance import check_preserved
import hashlib,json,math
from native_model import load,walk
ROOT=Path(__file__).resolve().parents[1]
MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def snapshot(path):
    model=load(path);colliders={};glass={};variants={};shaders={}
    count=0;maximum=0
    for address,node in walk(model.root):
        transform={key:node[key] for key in ('name','position','rotation','scale','tag','layer')}
        if 'collider' in node:colliders[address]=digest([transform,node['collider']])
        if 'mesh' in node:
            mesh=node['mesh'];n=len(mesh['vertices']);count+=sum(len(t) for t in mesh['submeshes']);maximum=max(n,maximum)
            assert n<65535 and n==len(mesh['normals'])==len(mesh['uvs'])
            assert all(math.isfinite(x) for p in mesh['vertices']+mesh['normals']+mesh['uvs'] for x in p)
            assert all(0<=i<n for sub in mesh['submeshes'] for tri in sub for i in tri)
            if 'Glass' in node['name']:glass[address]=digest([transform,mesh])
            if '/WindowBankStandard/' in address or '/SideHatch/' in address:variants[address]=digest([transform,mesh])
    for mat in model.materials:
        props=dict(mat['properties'])
        for key,val in props.items():
            if isinstance(val,dict) and 'index' in val:
                props[key]={**val,'index':model.textures[val['index']]['name']}
        shaders[mat['name']]=digest([mat['shader'],props])
    return {'colliders':colliders,'glazing':glass,'variants':variants,'materials':shaders,'triangles':count,'max_vertices':maximum}

def main():
    golden=json.loads((ROOT/'Tools/seam_revision_baseline.json').read_text())
    report={'baseline':'v0.7.0-dev.3','candidate':'v0.13.0-dev.1','parts':{}}
    for label,old in golden['parts'].items():
        current=snapshot(MODELS/f'RW_{label}_250.mu')
        for key in ('colliders','glazing','variants'):
            assert current[key]==old[key],(label,key,'regression')
        for name,value in old['materials'].items():assert current['materials'][name]==value,(label,name,'shader changed')
        model=load(MODELS/f'RW_{label}_250.mu')
        for tex in model.textures:assert (MODELS/(tex['name']+'.png')).exists(),tex['name']
        report['parts'][label]={'triangles_before':old['triangles'],'triangles_after':current['triangles'],
                                'largest_mesh_vertices':current['max_vertices'],'colliders_preserved':len(current['colliders']),
                                'glass_meshes_preserved':len(current['glazing'])}
        print('PASS native appearance regression:',label,'colliders preserved', 'glass, variants, shaders and textures preserved')
    for path,expected in golden['preserved_files'].items():
        check_preserved(ROOT,path,expected)
    report['preserved_files']=len(golden['preserved_files']);report['status']='PASS offline; KSP runtime pending'
    (ROOT/'Media/APPEARANCE_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PASS gameplay CFGs, runtime binary, original rooster, glass texture and warm-white emissive mask')

if __name__=='__main__':main()
