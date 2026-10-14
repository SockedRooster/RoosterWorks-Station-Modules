"""Identify complete structural ring components without changing any native mesh.

Only connected circular components of diffuse metal/shell surfaces qualify.
Runtime selectors partition the original triangle list; colliders never change.
"""
from pathlib import Path
import sys,json,math
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Tools'))
from native_model import load,walk
from config_nodes import Node,dump
GD=ROOT/'GameData/RoosterWorksStationModules';MODELS=GD/'Models'
PALETTE={'Steel':(151,166,171),'White':(218,221,213),'Charcoal':(55,65,72),'Blue':(53,101,158),'Green':(70,116,87),'Red':(151,64,54),'Gold':(191,150,67)}
SURFACES={'rwm_bronze','rwm_steel','rwm_white','rwm_ceramic','rwm_cladding','rwm_cladding_white'}

def components(mesh):
    triangles=mesh['submeshes'][0];parent=list(range(len(triangles)));owner={}
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i,tri in enumerate(triangles):
        for vertex in tri:
            key=tuple(round(v,5) for v in mesh['vertices'][vertex])
            if key in owner:parent[find(i)]=find(owner[key])
            else:owner[key]=i
    groups={}
    for i in range(len(triangles)):groups.setdefault(find(i),[]).append(i)
    return groups.values()

def circular(mesh,group,minimum=1.18,maximum=1.86):
    # Uniformly welded vertices avoid weighting the centre by duplicate UV seams.
    points=np.array(sorted({tuple(round(v,5) for v in mesh['vertices'][k]) for i in group for k in mesh['submeshes'][0][i]}))
    if len(points)<48:return False
    centred=points-points.mean(axis=0)
    _,_,basis=np.linalg.svd(centred,full_matrices=False)
    projected=centred@basis.T
    radius=np.sqrt((projected[:,:2]**2).sum(axis=1))
    r=float(np.median(radius))
    # Full exterior rings span a circular 2.4/3.6 m interface; small hardware,
    # rectangular plaques, endcap blankets and long hull skins are excluded.
    if not minimum<=r<=maximum:return False
    if np.ptp(projected[:,2])>.23*(r/1.2):return False
    if radius.min()<r*.94 or radius.max()>r*1.06:return False
    angles=np.sort(np.arctan2(projected[:,1],projected[:,0]))
    gaps=np.diff(np.r_[angles,angles[0]+math.tau])
    return float(gaps.max())<.18

def ranges(indices):
    out=[];first=last=indices[0]
    for i in indices[1:]:
        if i==last+1:last=i
        else:out.append(f'{first}:{last-first+1}');first=last=i
    out.append(f'{first}:{last-first+1}')
    return ','.join(out)

def build():
    tree=Node('ROOT');report={};used=set()
    for path in sorted(MODELS.glob('RW_*.mu')):
        model=load(path);maps=[];total=0
        for nodepath,node in walk(model.root):
            if 'mesh' not in node or len(node.get('materials',[]))!=1:continue
            mat=model.materials[node['materials'][0]]
            if mat['shader']!='KSP/Diffuse':continue
            texture=model.textures[mat['properties']['_MainTex']['index']]['name']
            if texture not in SURFACES:continue
            mesh=node['mesh'];selected=[]
            for group in components(mesh):
                limits=(2.30,2.52) if path.stem.endswith('_500') and not path.stem.startswith('RW_ADP') else (1.70,2.52) if path.stem=='RW_ADP_375_500' else (1.18,1.86)
                if circular(mesh,group,*limits):selected.extend(group)
            if not selected:continue
            selected.sort();used.add(texture);total+=len(selected)
            maps.append(Node('MESH',[('path',nodepath),('texture',texture),('vertices',str(len(mesh['vertices']))),('triangles',str(len(mesh['submeshes'][0]))),('ranges',ranges(selected))]))
        assert maps,('No selectable complete ring found',path.name)
        entry=Node('RW_RING_MAP',[('model',path.stem)],maps);tree.children.append(entry)
        report[path.stem]={'renderers':len(maps),'ring_triangles':total}
    assert len(report)==len(list(MODELS.glob('RW_*.mu')))
    (GD/'Compatibility/RingGeometry.cfg').write_text('// Generated exact native triangle selections; no collider or model replacement.\n'+dump(tree),encoding='utf-8')
    from config_nodes import parse
    patches=Node('ROOT')
    for path in sorted((GD/'Parts').glob('RW_*.cfg')):
        part=parse(path.read_text()).children[0]
        model=next(n.get('model') for n in part.children if n.header=='MODEL').rsplit('/',1)[-1]
        assert model in report
        patches.children.append(Node(f"@PART[{part.get('name')}]:HAS[!MODULE[ModuleRWRingColor]]:FOR[RoosterWorksStationModules]",[],[Node('MODULE',[('name','ModuleRWRingColor'),('ringModel',model),('ringColor','Original')])]))
    (GD/'Compatibility/RingColors.cfg').write_text('// Independent finish, HAB hatch and PWR hardware controls are retained.\n'+dump(patches),encoding='utf-8')
    for texture in used:
        src=Image.open(MODELS/(texture+'.png')).convert('RGBA');a=np.array(src)
        luminance=a[:,:,:3].mean(axis=2).astype(float)
        weather=np.clip((luminance-np.median(luminance))*.4,-30,30)
        for label,color in PALETTE.items():
            out=a.copy()
            for channel,value in enumerate(color):out[:,:,channel]=np.clip(value+weather,0,255).astype('uint8')
            Image.fromarray(out).save(MODELS/f'rwm_ring_{texture}_{label.lower()}.png')
    (ROOT/'Media/RingGeometry.json').write_text(json.dumps(report,indent=2)+'\n')
    (ROOT/'Source/Balancing/ring_palette.json').write_text(json.dumps(PALETTE,indent=2)+'\n')
    print('Built selectable ring maps on',len(report),'models; native meshes preserved:',sum(x['ring_triangles'] for x in report.values()),'triangles')
if __name__=='__main__':build()
