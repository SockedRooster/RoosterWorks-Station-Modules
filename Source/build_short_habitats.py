"""0.75: one-course compact HABs; original window/hatch aspect ratios retained.

2.5 m diameter x 1.98 m, with true scaled 3.75 and 5 m versions. New IDs only.
Independent hatch groups, original shared caps, solid collision and warm lamps.
"""
from pathlib import Path
import sys,copy,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'Tools'))
from native_model import load,walk
from native_derivatives import write,derivative,export_obj
from config_nodes import parse,dump,Node
from station_endcaps import add_endcap
from appearance_textures import label
from surface_uv import finish
import build_hab250 as h
GD=ROOT/'GameData/RoosterWorksStationModules';MODELS=GD/'Models';HALF=.990
CENTRES=(math.pi/3,math.pi,5*math.pi/3)
CAPACITY={250:150,375:280,500:190}

def hull():
    m=h.Mesh();h.cylinder_surface(m,1.204,-HALF,HALF,segments=24)
    for sign in (-1,1):
        for j in range(24):
            a=math.tau*j/24;b=math.tau*(j+1)/24
            p=[(0,sign*HALF,0),h.point(1.204,a,sign*HALF),h.point(1.204,b,sign*HALF)]
            if sign<0:p.reverse()
            m.triangle(p,[(0,sign,0)]*3,[(0,0)]*3)
    return m

def geometry():
    groups={name:{key:h.Mesh() for key in h.TEXTURES} for name in ('Base','WindowBankStandard','SideHatch')}
    base=groups['Base'];standard=groups['WindowBankStandard'];hatch=groups['SideHatch']
    h.cylinder_surface(base['graphite'],1.187,-.91,.91,segments=96)
    saved=h.bay_openings
    h.bay_openings=lambda:iter((t-.732,t+.732,-.391,.391) for t in CENTRES)
    try:
        for col in range(12):
            theta=math.tau*(col+.5)/12
            for row in range(4):
                y0=-.74+row*1.48/4+.012;y1=-.74+(row+1)*1.48/4-.012
                h.clipped_hull_panel(base['cladding_white' if (row+col)%11==0 else 'cladding'],theta,y0,y1,math.tau/12-.022,1.204)
    finally:h.bay_openings=saved
    for centre in CENTRES:
        if centre==CENTRES[0]:
            h.panoramic_pressure_bay(standard,centre,0,.710)
            h.hatch_pressure_bay(hatch,centre,0,.710)
        else:h.panoramic_pressure_bay(base,centre,0,.710)
    for sign in (-1,1):
        h.cylinder_surface(base['ceramic'],1.200,sign*.740,sign*.990,segments=96) if sign>0 else h.cylinder_surface(base['ceramic'],1.200,-.990,-.740,segments=96)
        for y,r,material,width in ((.82,1.218,'graphite',.020),(.82,1.223,'bronze',.006),(.962,1.214,'steel',.030),(.962,1.222,'bronze',.007)):
            yy=sign*y;h.cylinder_surface(base[material],r,yy-width/2,yy+width/2,segments=96)
        add_endcap(base,sign,HALF)
    # Readable original branding lives in the gaps between window banks.
    for mat,lo,hi,width,r in (('graphite',.25,.60,.32,1.214),('bronze',.27,.58,.30,1.222),('crest',.285,.565,.27,1.229)):
        h.flat_panel(base[mat],0,lo,hi,width,r,segments=14)
    theta=2*math.pi/3
    for mat,lo,hi,width,r in (('graphite',-.245,.245,.59,1.221),('bronze',-.23,.23,.56,1.229),('label',-.21,.21,.52,1.237)):
        h.flat_panel(base[mat],theta,lo,hi,width,r,segments=14)
    h.equipment_bay(base,4*math.pi/3,0)
    def rail(group,theta,lo,hi):
        h.tube(group['rail'],h.point(1.258,theta,lo),h.point(1.258,theta,hi),r=.013,sides=8)
        for yy in (lo,hi):h.tube(group['steel'],h.point(1.213,theta,yy),h.point(1.258,theta,yy),r=.022,sides=8)
    for theta in (0,2*math.pi/3,4*math.pi/3):rail(base,theta,-.64,.64)
    rail(standard,CENTRES[0]+.1,-.64,.64)
    for offset in (-.40,.40):rail(hatch,CENTRES[0]+offset,-.66,.66)
    for y in (-.65,-.49):
        for j in range(8):h.tube(hatch['rail'],h.point(1.258,CENTRES[0]-.30+.60*j/8,y),h.point(1.258,CENTRES[0]-.30+.60*(j+1)/8,y),r=.013,sides=8)
    for group in groups.values():finish(group)
    return groups

def native():
    groups=geometry();oldpart=h.PART;oldhull=h.hull_collision_mesh
    try:
        h.PART='RW_HABS_250';h.hull_collision_mesh=hull
        h.create_mu(groups,MODELS/'RW_HABS_250.mu')
    finally:h.PART=oldpart;h.hull_collision_mesh=oldhull
    model=load(MODELS/'RW_HABS_250.mu')
    for _,n in walk(model.root):
        if n['tag'] in ('Airlock','Ladder'):n['position']=(n['position'][0],0,n['position'][2])
    for t in model.textures:
        if t['name']=='rwm_label':t['name']='rwm_habslabel_250'
    write(model,MODELS/'RW_HABS_250.mu');export_obj(model,'RW_HABS_250.obj');export_obj(model,'RW_HABS_250_SideHatch.obj','SideHatch')
    for size,scale in ((375,1.5),(500,2)):
        model=derivative('RW_HABS_250',f'RW_HABS_{size}',scale,{'rwm_habslabel_250':f'rwm_habslabel_{size}'})
        export_obj(model,f'RW_HABS_{size}.obj');export_obj(model,f'RW_HABS_{size}_SideHatch.obj','SideHatch')

def build():
    for size in (250,375,500):label(f'HAB-S-{size}','COMPACT / TWO CREW').save(MODELS/f'rwm_habslabel_{size}.png')
    native();patches=Node('ROOT')
    for size,scale in ((250,1),(375,1.5),(500,2)):
        tree=parse((GD/f'Parts/RW_HAB_{size}.cfg').read_text());part=tree.children[0];name=f'RW_HABS_{size}'
        part.set('name',name);part.set('title',f'RoosterWorks RW-HAB-S-{size} Compact Habitat');part.set('CrewCapacity','2')
        part.set('description',f'Compact {size/100:g} m, {1.98*scale:g} m-long two-crew habitat. One full-proportion window course with Standard / Side Hatch variants, original sealed ends, warm-white lighting and independent shell/ring colors. Half the matching full HAB dry mass, supply capacity and internal volume; base battery rounded to tens. Temporary two-seat stock IVA. No new recycler or comfort claims.')
        for key in ('mass','cost','entryCost'):part.set(key,format(float(part.get(key))*.5,'.10g'))
        part.set('node_stack_top',f'0, {HALF*scale:g}, 0, 0, 1, 0, {2 if size==250 else 3 if size==375 else 4}')
        part.set('node_stack_bottom',f'0, {-HALF*scale:g}, 0, 0, -1, 0, {2 if size==250 else 3 if size==375 else 4}')
        for child in part.children:
            if child.header=='MODEL':child.set('model',f'RoosterWorksStationModules/Models/{name}')
            if child.header=='INTERNAL':child.set('name','mk1CabinInternal')
            if child.header=='RESOURCE' and child.get('name')=='ElectricCharge':child.set('amount',str(CAPACITY[size]));child.set('maxAmount',str(CAPACITY[size]))
            if child.get('moduleID'):child.set('moduleID',child.get('moduleID').replace('RW_HAB_', 'RW_HABS_'))
        (GD/f'Parts/{name}.cfg').write_text(dump(tree),encoding='utf-8')
        for source in parse((GD/'Compatibility/KerbalismDefault.cfg').read_text()).children:
            patch=copy.deepcopy(source);patch.header=patch.header.replace('RW_HAB_250',name)
            def visit(n):
                for i,(key,value) in enumerate(n.values):
                    clean=key.lstrip('%@');factor=None
                    if n.header.startswith('%RESOURCE[') and clean in ('amount','maxAmount'):factor=scale**3*.5
                    if clean=='volume':factor=scale**3*.5
                    if clean=='surface':factor=scale**2*2/3 # same endcaps, half-length cylindrical wall
                    if factor is not None:n.values[i]=(key,format(float(value)*factor,'.10g'))
                for c in n.children:visit(c)
            visit(patch);patches.children.append(patch)
        patches.children.append(Node(f'@PART[{name}]:NEEDS[VABOrganizer]:FINAL',[('%category','Utility')],[Node('!VABORGANIZER,*'),Node('VABORGANIZER',[('organizerSubcategory','crewHabitation')])]))
        print('Built compact',name,'length',1.98*scale,'crew 2',flush=True)
    (GD/'Compatibility/ShortHabitats.cfg').write_text('// True compact geometry; two seats; balanced storage and usable hatch.\n'+dump(patches),encoding='utf-8')
if __name__=='__main__':build()
