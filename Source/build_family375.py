"""Native 3.75 m family derived from the maintained 2.5 m source-kit exports.

Geometry/positions scale 1.5, volume/storage/dry mass 3.375, surface 2.25.
Keep original seats, IVA, variants, renderer/trigger names and equipment roles.
No rescaleFactor trick: new native meshes and colliders use real Unity metres.
"""
from pathlib import Path
import sys,copy,math,json
ROOT=Path(__file__).resolve().parents[1];MODELS=ROOT/'GameData/RoosterWorksStationModules/Models'
sys.path.insert(0,str(ROOT/'Tools'))
from native_model import load,walk
import build_hab250 as h
from config_nodes import parse,dump
from electric_charge_balance import policy
SCALE=1.5;VOLUME=SCALE**3;AREA=SCALE**2
ROLES={'HAB':'ORBITAL HABITAT','LAB':'RESEARCH LABORATORY','CMD':'STATION COMMAND','HUB':'PRESSURE JUNCTION','CUP':'PANORAMIC OBSERVATION','LOG':'LOGISTICS / STORAGE','AIR':'EVA / AIRLOCK','PWR':'POWER / SERVICE','GRN':'GREENHOUSE / HYDROPONICS'}
LABELS={'label':'HAB','lablabel':'LAB','cmdlabel':'CMD','hublabel':'HUB','cuplabel':'CUP','loglabel':'LOG','airlabel':'AIR','pwrlabel':'PWR','grnlabel':'GRN'}
def number(value,factor=1):return format(float(value)*factor,'.10g')
def mesh(w,m):
    w.i(13,len(m['vertices']),len(m['submeshes']));w.i(14)
    for p in m['vertices']:w.f(*(x*SCALE for x in p))
    for tag,key in ((15,'uvs'),(16,'uv2'),(17,'normals'),(18,'tangents'),(32,'colors')):
        if key in m:
            w.i(tag)
            for v in m[key]:w.f(*v)
    for tris in m['submeshes']:
        w.i(19,3*len(tris))
        for tri in tris:w.i(*tri)
    w.i(22)
def node(w,n):
    w.s(n['name']);w.f(*(x*SCALE for x in n['position']));w.f(*n['rotation']);w.f(*n['scale'])
    w.i(24);w.s(n['tag']);w.i(n['layer'])
    if 'mesh' in n:
        w.i(7);mesh(w,n['mesh']);w.i(8)
        for v in n['shadows']:w.b(v)
        w.i(len(n['materials']),*n['materials'])
    if 'collider' in n:
        c=n['collider']
        if c['type']=='mesh':w.i(25);w.b(c['trigger']);w.b(c['convex']);mesh(w,c['mesh'])
        elif c['type']=='box':
            w.i(28);w.b(c['trigger']);w.f(*(v*SCALE for v in c['size']));w.f(*(v*SCALE for v in c['center']))
        else:raise ValueError(c['type'])
    if 'light' in n:
        l=n['light'];w.i(23,l['type']);w.f(l['intensity'],l['range']*SCALE,*l['color']);w.i(l['cullingMask'] if l['cullingMask']<2**31 else l['cullingMask']-2**32);w.f(l['spotAngle'])
    for child in n['children']:w.i(0);node(w,child);w.i(1)
def native(role):
    old=load(MODELS/f'RW_{role}_250.mu');old.root['name']=f'RW_{role}_375'
    w=h.Writer(MODELS/f'RW_{role}_375.mu');w.i(76543,5);w.s(f'RW_{role}_375');node(w,old.root)
    w.i(10,len(old.materials))
    for mat in old.materials:
        w.s(mat['name']);w.s(mat['shader']);w.i(len(mat['properties']))
        for name,value in mat['properties'].items():
            w.s(name)
            if isinstance(value,dict):w.i(4,value['index']);w.f(*value['scale']);w.f(*value['offset'])
            elif isinstance(value,tuple):w.i(0);w.f(*value)
            else:w.i(2);w.f(value)
    w.i(12,len(old.textures))
    for t in old.textures:
        name=t['name'];name=name+'_375' if name.removeprefix('rwm_') in LABELS else name
        w.s(name);w.i(t['type'])
    w.close()
def obj(role,suffix=''):
    source=ROOT/f'Source/Blender/RW_{role}_250{suffix}.obj';target=source.with_name(f'RW_{role}_375{suffix}.obj')
    lines=[]
    for line in source.read_text().splitlines():
        if line.startswith('v '):line='v '+' '.join(number(v,SCALE) for v in line.split()[1:])
        elif line.startswith('mtllib '):line=line.replace('_250','_375')
        lines.append(line)
    target.write_text('\n'.join(lines)+'\n')
    source=source.with_suffix('.mtl');text=source.read_text()
    for name in LABELS:text=text.replace(f'rwm_{name}.png',f'rwm_{name}_375.png')
    target.with_suffix('.mtl').write_text(text)
def part(role):
    path=ROOT/f'GameData/RoosterWorksStationModules/Parts/RW_{role}_250.cfg';root=parse(path.read_text());p=root.children[0]
    p.set('name',f'RW_{role}_375');p.set('title',p.get('title').replace('-250','-375'))
    p.set('bulkheadProfiles',p.get('bulkheadProfiles').replace('size2','size3'))
    p.set('description','Large 3.75 m edition with the established crew capacity and equipment functions. '+p.get('description').replace('2.5 m','3.75 m').replace('2.5m','3.75m').replace('-250','-375'))
    for key in ('mass','cost','entryCost'):
        if p.get(key) is not None:p.set(key,number(p.get(key),VOLUME) if key=='mass' else str(round(float(p.get(key))*VOLUME)))
    for key in ('breakingForce','breakingTorque'):p.set(key,number(p.get(key),AREA))
    for key,value in list(p.values):
        if key.startswith('node_stack_') or key=='node_attach':
            values=[v.strip() for v in value.split(',')]
            values[:3]=[number(v,SCALE) for v in values[:3]]
            if key.startswith('node_stack_') and len(values)>6:values[6]='3'
            p.set(key,', '.join(values))
    for c in p.children:
        if c.header=='MODEL':c.set('model',c.get('model').replace('_250','_375'))
        if c.header=='RESOURCE':
            for key in ('amount','maxAmount'):
                value=policy()['parts'][f'RW_{role}_375']['target_base_ec'] if c.get('name')=='ElectricCharge' else float(c.get(key))*VOLUME
                c.set(key,number(value))
        if c.header=='MODULE':
            if c.get('moduleID'):c.set('moduleID',c.get('moduleID').replace('_250','_375'))
            if c.get('name')=='ModuleInventoryPart':
                c.set('InventorySlots',str(int(c.get('InventorySlots'))*2));c.set('packedVolumeLimit',number(c.get('packedVolumeLimit'),VOLUME))
            if c.get('name')=='ModuleReactionWheel':
                for key in ('PitchTorque','YawTorque','RollTorque'):c.set(key,number(c.get(key),VOLUME))
                for r in c.children:
                    if r.header=='RESOURCE':r.set('rate',number(r.get('rate'),VOLUME))
    # Physical lengths in descriptive prose must match the larger native geometry.
    for text,length in (('1.8 m',2.7),('2.4 m',3.6),('3.6 m',5.4)):
        if role=='GRN' and text=='3.6 m' or role in ('AIR','PWR') and text=='2.4 m':p.set('description',p.get('description').replace(text,f'{length:g} m'))
    (path.parent/f'RW_{role}_375.cfg').write_text(dump(root),encoding='utf-8')
def patches():
    root=parse('');organizer=parse('')
    for path in sorted((ROOT/'GameData/RoosterWorksStationModules/Compatibility').glob('*.cfg')):
        if path.name.startswith('LargeFamily') or path.name in ('ExteriorFinish.cfg','CompactReactor.cfg','PowerVariants.cfg','StorageBalance.cfg','CrewTubes.cfg','StationCatalogue.cfg'):continue
        tree=parse(path.read_text())
        for p in tree.children:
            if not any(f'RW_{r}_250' in p.header for r in ROLES):continue
            p=copy.deepcopy(p);p.header=p.header.replace('_250','_375')
            def scale(n):
                for i,(key,value) in enumerate(n.values):
                    clean=key.lstrip('%@')
                    factor=None
                    if n.header.lstrip('%@') in ('RESOURCE','RESOURCE[Food]','RESOURCE[Water]','RESOURCE[Oxygen]','RESOURCE[Nitrogen]','RESOURCE[Waste]','RESOURCE[WasteWater]') and clean in ('amount','maxAmount'):factor=VOLUME
                    if n.header.startswith('%RESOURCE[') and clean in ('amount','maxAmount'):factor=VOLUME
                    if clean=='volume':factor=VOLUME
                    if clean=='surface':factor=AREA
                    if n.get('name')=='ProcessController' and clean=='capacity':factor=AREA
                    if 'RW_GRN_375' in p.header and key in ('@crop_size *','@ec_rate *','@rate *'):factor=VOLUME
                    if factor is not None:n.values[i]=(key,number(value,factor))
                for c in n.children:scale(c)
            scale(p)
            (organizer if 'VABOrganizer' in p.header else root).children.append(p)
    (ROOT/'GameData/RoosterWorksStationModules/Compatibility/LargeFamilyKerbalism.cfg').write_text('// Independent 3.75 m family; storage/volume x3.375, surface x2.25.\n'+dump(root),encoding='utf-8')
    (ROOT/'GameData/RoosterWorksStationModules/Compatibility/LargeFamilyVABOrganizer.cfg').write_text(dump(organizer),encoding='utf-8')
def build():
    from appearance_textures import label
    for name,role in LABELS.items():label(role+'-375',ROLES[role]).save(MODELS/f'rwm_{name}_375.png',optimize=True)
    report={}
    for role in ROLES:
        native(role);obj(role);part(role)
        if role=='HAB':obj(role,'_SideHatch')
        model=load(MODELS/f'RW_{role}_375.mu')
        report[role]={'scale':SCALE,'volume_factor':VOLUME,'visual_triangles':sum(sum(len(t) for t in n['mesh']['submeshes']) for _,n in walk(model.root) if 'mesh' in n)}
        print('Built native RW-'+role+'-375',flush=True)
    patches();(ROOT/'Media/LargeFamily-build.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':build()
