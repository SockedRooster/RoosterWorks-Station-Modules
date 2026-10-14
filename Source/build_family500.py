"""0.7: actual 5 m native station family and a 3.75-to-5 m adapter.

Old parts and models are never rewritten. Geometry/volume scale from 2.5 m
by 2 / 8; EC uses role references, not volume. Hardware and seats retain roles.
"""
from pathlib import Path
import sys,copy,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Tools'))
from native_model import load,walk
from native_derivatives import derivative,export_obj,write
from config_nodes import parse,dump,Node
from appearance_textures import label
GD=ROOT/'GameData/RoosterWorksStationModules';MODELS=GD/'Models'
ROLES=('HAB','LAB','CMD','HUB','CUP','LOG','AIR','PWR','GRN','TUB','ELB')
LABELS={'HAB':'label','LAB':'lablabel','CMD':'cmdlabel','HUB':'hublabel','CUP':'cuplabel','LOG':'loglabel','AIR':'airlabel','PWR':'pwrlabel','GRN':'grnlabel','TUB':'tublabel','ELB':'elblabel'}
EC={'HAB':370,'LAB':0,'CMD':630,'HUB':0,'CUP':525,'LOG':0,'AIR':0,'PWR':10200,'GRN':0,'TUB':0,'ELB':0}
num=lambda x:format(float(x),'.10g')

def part(source,target,role,scale=2):
    tree=parse((GD/f'Parts/{source}.cfg').read_text());p=tree.children[0];p.set('name',target)
    p.set('title',p.get('title').replace('-250','-500'));p.set('bulkheadProfiles','size4')
    details={
      'HAB':'7.92 m-long four-crew habitat. Full-size windows and Standard / Side Hatch options; warm-white cabin lighting. Supplies/internal volume scale with native size; 370 base EC.',
      'LAB':'7.92 m-long two-crew research bay. Stock lab equipment retained; Kerbalism drive capped at 2.5 GB and 100 sample slots; warm-white lighting.',
      'CMD':'3.44 m-long two-crew station command core. Retains SAS, communications, reaction wheel, IVA and cabin lights; 630 base EC; Kerbalism archive capped at 2.5 GB.',
      'HUB':'Six 5 m stack interfaces on a rounded pressure junction; 8 m assembly envelope. Crewless and passive, with Kerbalism pressure support.',
      'CUP':'One-seat panoramic observation cupola with single bottom stack node, sloped glass and warm-white lighting. No added command or exterior EVA; 525 base EC.',
      'LOG':'6 m-long crewless logistics vault. 36 stock inventory slots / 11200 L item volume, independent of Kerbalism supplies. Mixed or dedicated editor payloads; no generation.',
      'AIR':'4.8 m-long two-crew EVA airlock with retained exit/ladder functions, warm-white lighting, stock inventory and Kerbalism pressure support.',
      'PWR':'4.8 m-long crewless power/service core. 10200 EC battery; optional internally cooled 8410 EC / 6.5 EC/s nuclear variant with finite fuel under Kerbalism Default/CRP.',
      'GRN':'7.2 m-long greenhouse with visible crops, preserved warm-white inspection lights and separate growth controller; Kerbalism Default crop system scales with size.',
      'TUB':'4 m-long crewless straight pressure passage with two size-4 interfaces. No seats, EVA or supplies; conditional Kerbalism pressure and CLS passability.',
      'ELB':'90-degree crewless pressure elbow, 3.6 m centreline bend radius and 0.6 m tangent collars. Two perpendicular size-4 interfaces; conditional pressure and CLS passability.'}
    p.set('description','Native 5 m '+details[role]+' Original RoosterWorks styling, White/Grey exterior and independent ring colors.')
    for key in ('mass','cost','entryCost'):
        if p.get(key) is not None:p.set(key,num(float(p.get(key))*scale**3) if key=='mass' else str(round(float(p.get(key))*scale**3)))
    for key in ('breakingForce','breakingTorque'):
        if p.get(key):p.set(key,num(float(p.get(key))*scale**2))
    for key,value in list(p.values):
        if key.startswith('node_stack_') or key=='node_attach':
            fields=[v.strip() for v in value.split(',')];fields[:3]=[num(float(v)*scale) for v in fields[:3]]
            if key.startswith('node_stack_') and len(fields)>6:fields[6]='4'
            p.set(key,', '.join(fields))
    for c in p.children:
        if c.header=='MODEL':c.set('model',f'RoosterWorksStationModules/Models/{target}')
        if c.header=='RESOURCE':
            for key in ('amount','maxAmount'):c.set(key,num(EC[role] if c.get('name')=='ElectricCharge' else float(c.get(key))*scale**3))
        if c.header=='MODULE':
            if c.get('moduleID'):c.set('moduleID',c.get('moduleID').replace('_250','_500'))
            if c.get('name')=='ModuleInventoryPart':
                c.set('InventorySlots',str(int(c.get('InventorySlots'))*3));c.set('packedVolumeLimit',num(float(c.get('packedVolumeLimit'))*scale**3))
            if c.get('name')=='ModuleReactionWheel':
                for key in ('PitchTorque','YawTorque','RollTorque'):c.set(key,num(float(c.get(key))*scale**3))
                for r in c.children:
                    if r.header=='RESOURCE':r.set('rate',num(float(r.get('rate'))*scale**3))
    (GD/f'Parts/{target}.cfg').write_text(dump(tree),encoding='utf-8')

def compatibility():
    out=Node('ROOT');source_files=('KerbalismDefault.cfg','LabKerbalism.cfg','CommandKerbalism.cfg','HubKerbalism.cfg','CupolaKerbalism.cfg','LogisticsKerbalism.cfg','AirlockKerbalism.cfg','GreenhouseKerbalism.cfg','CrewTubes.cfg')
    for filename in source_files:
        for patch in parse((GD/'Compatibility'/filename).read_text()).children:
            if '_250]' not in patch.header:continue
            p=copy.deepcopy(patch);p.header=p.header.replace('_250','_500')
            def visit(n):
                for i,(key,value) in enumerate(n.values):
                    clean=key.lstrip('%@');factor=None
                    if (n.header.startswith('%RESOURCE[') or n.header.lstrip('%@')=='RESOURCE') and clean in ('amount','maxAmount'):factor=8
                    if clean=='volume':factor=8
                    if clean=='surface':factor=4
                    if n.get('name')=='ProcessController' and clean=='capacity':factor=4
                    if 'RW_GRN_500' in p.header and key in ('@crop_size *','@ec_rate *','@rate *'):factor=8
                    if factor is not None:n.values[i]=(key,num(float(value)*factor))
                for child in n.children:visit(child)
            visit(p);out.children.append(p)
    # Explicit science ceilings override the generic Kerbalism size-derived drive.
    storage=parse((GD/'Compatibility/StorageBalance.cfg').read_text())
    for p in storage.children[:2]:
        p=copy.deepcopy(p);role='CMD' if 'RW_CMD' in p.header else 'LAB';p.header=f'@PART[RW_{role}_500]:NEEDS[Kerbalism,FeatureScience]:FINAL';out.children.append(p)
    power=copy.deepcopy(parse((GD/'Compatibility/PowerVariants.cfg').read_text()).children[1]);power.header=power.header.replace('375','500')
    power.set('%description','5 m power/service core. Battery 10200 EC; Nuclear 8410 EC, 6.5 EC/s, 1.95 fuel/waste capacity. Built-in cooling. White/Grey and ring color independent.')
    for module in power.children:
        if module.get('name')=='ModulePartVariants':
            for variant in module.children:
                if variant.get('name')=='Nuclear':variant.set('mass',num(.039*1.3));variant.set('cost',str(round(10880*1.3)))
        if module.get('name')=='ModuleRWPowerVariant':
            module.set('batteryCapacity','10200');module.set('reactorCapacity','8410');module.set('reactorScale','1.3')
    out.children.append(power)
    from build_catalogue import MAPPING
    for role in ROLES:
        subcategory,category,_=MAPPING[role]
        out.children.append(Node(f'@PART[RW_{role}_500]:NEEDS[VABOrganizer]:FINAL',[('%category',category)],[Node('!VABORGANIZER,*'),Node('VABORGANIZER',[('organizerSubcategory',subcategory)])]))
    out.children.append(Node('@PART[RW_ADP_375_500]:NEEDS[VABOrganizer]:FINAL',[('%category','Structural')],[Node('!VABORGANIZER,*'),Node('VABORGANIZER',[('organizerSubcategory','crewAdapters')])]))
    (GD/'Compatibility/Family500.cfg').write_text('// Native 5 m family; new IDs only; existing patches unchanged.\n'+dump(out),encoding='utf-8')

def adapter():
    target='RW_ADP_375_500';model=load(MODELS/'RW_ADP_250_375.mu');model.name=target;model.root['name']=target
    # Different endpoint ratio: 3.75/5, not a uniformly scaled 2.5/3.75 cone.
    def mesh(m):
        old=m['vertices'];slope=(1.5-4/3)/1.8
        def factor(y):return 4/3+(y+.9)*slope
        normals=[]
        for (x,y,z),(nx,ny,nz) in zip(old,m['normals']):
            f=factor(y);v=(nx/f,(ny-slope*(x*nx+z*nz)/f)/(7/6),nz/f);length=math.sqrt(sum(a*a for a in v));normals.append(tuple(a/length for a in v))
        m['vertices']=[(x*factor(y),y*7/6,z*factor(y)) for x,y,z in old];m['normals']=normals
    for _,n in walk(model.root):
        assert n['position']==(0.,0.,0.)
        if 'mesh' in n:mesh(n['mesh'])
        if 'collider' in n:mesh(n['collider']['mesh'])
    for t in model.textures:
        if t['name']=='rwm_adplabel':t['name']='rwm_adplabel_375_500'
    label('ADP-375/500','3.75 m / 5 m TRANSITION').save(MODELS/'rwm_adplabel_375_500.png')
    write(model,MODELS/(target+'.mu'));export_obj(model,target+'.obj')
    p=parse((GD/'Parts/RW_ADP_250_375.cfg').read_text());part=p.children[0]
    part.set('name',target);part.set('title','RoosterWorks RW-ADP-375-500 Station Adapter');part.set('bulkheadProfiles','size3, size4')
    part.set('description','Native 2.1 m-long passive structural adapter from the 3.75 m top interface to the 5 m bottom interface. Reused sealed endcap details, original textures, White/Grey finish and independent ring colors. No crew, battery, command or EVA.')
    part.set('node_stack_top','0, 1.05, 0, 0, 1, 0, 3');part.set('node_stack_bottom','0, -1.05, 0, 0, -1, 0, 4')
    part.set('mass','2.6');part.set('cost','9800');part.set('entryCost','19000');part.set('breakingForce','600');part.set('breakingTorque','600')
    for child in part.children:
        if child.header=='MODEL':child.set('model',f'RoosterWorksStationModules/Models/{target}')
    (GD/f'Parts/{target}.cfg').write_text(dump(p),encoding='utf-8')

def build():
    for role in ROLES:
        texture=LABELS[role];newtexture='rwm_'+texture+'_500'
        label(role+'-500',{'HAB':'ORBITAL HABITAT','LAB':'RESEARCH LABORATORY','CMD':'STATION COMMAND','HUB':'PRESSURE JUNCTION','CUP':'PANORAMIC OBSERVATION','LOG':'LOGISTICS / STORAGE','AIR':'EVA / AIRLOCK','PWR':'POWER / SERVICE','GRN':'GREENHOUSE / HYDROPONICS','TUB':'PRESSURIZED PASSAGE','ELB':'90 DEGREE / CREW PASSAGE'}[role]).save(MODELS/(newtexture+'.png'))
        source=f'RW_{role}_250';target=f'RW_{role}_500';model=derivative(source,target,2,{'rwm_'+texture:newtexture})
        export_obj(model,target+'.obj')
        if role=='HAB':export_obj(model,target+'_SideHatch.obj','SideHatch')
        part(source,target,role);print('Built native',target,flush=True)
    adapter();compatibility()
    (ROOT/'Source/Balancing/family500_policy.json').write_text(json.dumps({'base_ec':EC,'source':'5 m SSPX core 600 +5%; cupola 500 +5%; HAB 500 +5%, -30%, round ten. PWR area proxy from accepted 3.75 m balances, rounded ten. Other passive roles retain zero.','power':{'battery':10200,'nuclear':8410,'scale':1.3},'scale':2,'volume':8,'area':4},indent=2)+'\n')
if __name__=='__main__':build()
