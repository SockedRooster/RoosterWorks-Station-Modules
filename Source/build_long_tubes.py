"""Double-length straight passages with unchanged diameter, endcaps and badge UVs."""
from pathlib import Path
import sys,copy,math
import build_crew_tubes as tube
from appearance_textures import label
from config_nodes import Node,parse,dump
from native_derivatives import write,export_obj
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Tools'))
from native_model import load
GD=ROOT/'GameData/RoosterWorksStationModules';MODELS=GD/'Models'
def build():
    patches=Node('ROOT')
    for size,scale in ((250,1),(375,1.5),(500,2)):
        name=f'RW_TUBL_{size}';source=f'RW_TUB_{size}'
        mesh=tube.geometry(False,scale,half_override=2)
        tube.native(name,mesh,[tube.mapped(tube.cylinder(1.198,2),False,scale)],size)
        model=load(MODELS/(name+'.mu'))
        for t in model.textures:
            if t['name'].startswith('rwm_tublabel'):t['name']=f'rwm_tublabel_long_{size}'
        write(model,MODELS/(name+'.mu'))
        label(f'TUB-L-{size}','LONG / PRESSURIZED PASSAGE').save(MODELS/f'rwm_tublabel_long_{size}.png')
        export_obj(model,ROOT/f'Source/Blender/{name}.obj')
        p=copy.deepcopy(parse((GD/f'Parts/{source}.cfg').read_text()).children[0])
        p.set('name',name);p.set('title',f'RoosterWorks RW-TUBL-{size} Long Crew Tube')
        p.set('description',f'{size/100:g} m diameter, {4*scale:g} m long pressurized crew passage. Twice the standard straight tube length with retained interface detail and readable insignia. Crewless; conditional Kerbalism pressure and Connected Living Space passability. White/Grey finish and selectable ring colors.')
        p.set('tags',p.get('tags')+' long extended')
        for key in ('mass','cost','entryCost'):p.set(key,format(float(p.get(key))*2,'.10g'))
        for key in ('node_stack_top','node_stack_bottom'):
            v=p.get(key).split(',');v[1]=str(float(v[1])*2);p.set(key,','.join(v))
        for n in p.children:
            if n.header=='MODEL':n.set('model',f'RoosterWorksStationModules/Models/{name}')
            if n.header=='MODULE' and n.get('name')=='ModuleRWStationFinish':n.set('finish','White')
        (GD/f'Parts/{name}.cfg').write_text(dump(Node('ROOT',children=[p])),encoding='utf-8')
        inner=.92*scale;length=4*scale
        patches.children += [Node(f'@PART[{name}]:NEEDS[Kerbalism,FeatureHabitat]:AFTER[zzzKerbalismDefault]',children=[Node('%MODULE[Habitat]',[('%name','Habitat'),('%volume',format(math.pi*inner**2*length,'.10g')),('%surface',format(2*math.pi*inner*length+2*math.pi*inner**2,'.10g'))])]),Node(f'@PART[{name}]:HAS[!MODULE[ModuleConnectedLivingSpace]]:NEEDS[ConnectedLivingSpace]',children=[Node('MODULE',[('name','ModuleConnectedLivingSpace'),('passable','true')])]),Node(f'@PART[{name}]:NEEDS[VABOrganizer]:FINAL',[('%category','Structural')],[Node('!VABORGANIZER,*'),Node('VABORGANIZER',[('organizerSubcategory','crewTubes')])])]
        # Keep finish support standalone, even when no B9PartSwitch is installed.
        patches.children.append(Node(f'@PART[{name}]:HAS[!MODULE[ModuleRWStationFinish]]:FOR[RoosterWorksStationModules]',children=[Node('MODULE',[('name','ModuleRWStationFinish'),('finish','White')])]))
        print('Built',name,'length',length,'m')
    (GD/'Compatibility/LongCrewTubes.cfg').write_text(dump(patches),encoding='utf-8')
if __name__=='__main__':build()
