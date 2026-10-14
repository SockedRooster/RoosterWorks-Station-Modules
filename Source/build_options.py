"""Grey shell textures and optional internally cooled nuclear PWR editions.

Build after the canonical family. All original native models remain identical.
Reactor editions have separate stable part IDs to protect existing passive cores.
"""
from pathlib import Path
import copy,json
import numpy as np
from PIL import Image
from config_nodes import parse,dump,Node
ROOT=Path(__file__).resolve().parents[1]
GD=ROOT/'GameData/RoosterWorksStationModules';MODELS=GD/'Models'
SURFACES=('ceramic','white','cladding','cladding_white')
RATE=6.5206e-9

def grey_textures():
    for surface in SURFACES:
        image=Image.open(MODELS/f'rwm_{surface}.png').convert('RGBA')
        a=np.array(image);rgb=a[:,:,:3].astype(float)
        # Preserve all existing panel seams, wear, stencil contrast and UV layout.
        # Recolour light neutral shell pixels only; keep warm trim and dark ink.
        neutral=(rgb.max(2)-rgb.min(2)<38)&(rgb.mean(2)>95)
        grey=rgb.mean(2)*.63+19
        for channel,offset in enumerate((-4,0,4)):
            a[:,:,channel]=np.where(neutral,np.clip(grey+offset,0,255),a[:,:,channel]).astype('uint8')
        Image.fromarray(a).save(MODELS/f'rwm_{surface}_grey.png')

def reactor(size,factor):
    tree=parse((GD/f'Parts/RW_PWR_{size}.cfg').read_text());part=tree.children[0]
    part.header='PART:NEEDS[CommunityResourcePack]'
    part.set('name',f'RW_PWR_{size}_REACTOR')
    part.set('title',f'RoosterWorks RW-PWR-{size} Nuclear Power and Service Core')
    part.set('description',f'Optional reactor-equipped power/service core with {3500 if size==250 else 6750} EC storage and {5*factor:g} EC/s nuclear generation. Integrated passive cooling requires no external radiators. EnrichedUranium is converted 1:1 to retained DepletedFuel; a full waste tank or empty fuel tank stops production. Select white or grey metal exterior independently. Reactor starts switched off. Kerbalism Default supports loaded and background operation; stock fallback requires Community Resource Pack. Exterior silhouette matches the passive core.')
    # Compact reactor plus integrated cooling hardware, independently of the
    # full station module's existing dry mass. Do not scale the entire PWR mass.
    part.set('mass',format(float(part.get('mass'))+.039*factor,'.10g'))
    part.set('cost',str(int(part.get('cost'))+round(10880*factor)))
    part.set('entryCost',str(int(part.get('entryCost'))+round(35500*factor)))
    # Same tier as the passive core: the optional edition remains discoverable
    # wherever the existing PWR part is available in the user's editor.
    part.set('TechRequired',part.get('TechRequired'))
    part.set('tags',part.get('tags')+' nuclear fission uranium reactor integrated cooling')
    for name,amount in (('EnrichedUranium',1.5*factor),('DepletedFuel',0)):
        part.children.append(Node('RESOURCE',[('name',name),('amount',format(amount,'.10g')),('maxAmount',format(1.5*factor,'.10g'))]))
    # Retain historical standalone definitions byte-for-byte for compatibility;
    # current capacities are supplied by the explicit late balance patch.
    for resource in part.children:
        if resource.header=='RESOURCE' and resource.get('name')=='ElectricCharge':
            resource.set('amount',3500 if size==250 else 6750);resource.set('maxAmount',3500 if size==250 else 6750)
    part.children.append(Node('MODULE:NEEDS[Kerbalism,ProfileDefault]',[
        ('name','ProcessController'),('resource','_RWCompactReactor'),('title','Integrated nuclear reactor'),
        ('capacity',str(factor)),('running','false'),('toggle','true'),('valve_i','0')]))
    converter=Node('MODULE:NEEDS[!Kerbalism]',[
        ('name','ModuleResourceConverter'),('ConverterName','Integrated nuclear reactor'),
        ('StartActionName','Start reactor'),('StopActionName','Stop reactor'),
        ('FillAmount','1'),('AutoShutdown','false'),('GeneratesHeat','false'),
        ('UseSpecialistBonus','false'),('IsActivated','false')])
    for header,name,rate,dump_excess in (('INPUT_RESOURCE','EnrichedUranium',RATE*factor,None),('OUTPUT_RESOURCE','DepletedFuel',RATE*factor,'false'),('OUTPUT_RESOURCE','ElectricCharge',5*factor,'true')):
        vals=[('ResourceName',name),('Ratio',format(rate,'.12g'))]
        if name!='ElectricCharge':vals.append(('FlowMode','NO_FLOW'))
        if dump_excess is not None:vals.append(('DumpExcess',dump_excess))
        converter.children.append(Node(header,vals))
    part.children.append(converter)
    (GD/f'Parts/RW_PWR_{size}_REACTOR.cfg').write_text(dump(tree))

def build():
    grey_textures()
    (GD/'Compatibility/ExteriorFinish.cfg').write_text('''// Independent selector preserves stock HAB Standard / SideHatch variants.
@PART[RW_*]:HAS[!MODULE[ModuleRWStationFinish]]:FOR[RoosterWorksStationModules]
{
    MODULE
    {
        name = ModuleRWStationFinish
        finish = White
    }
}
''')
    for size,factor in ((250,1.1),(375,1.2)):reactor(size,factor)
    (GD/'Compatibility/CompactReactor.cfg').write_text('''// Dedicated process avoids all NFE/SystemHeat global reactor patches.
// Fixed built-in cooling is part of the added dry mass. No external radiator.
RESOURCE_DEFINITION:NEEDS[Kerbalism,ProfileDefault,CommunityResourcePack]
{
    name = _RWCompactReactor
    density = 0
    isVisible = false
}
@Profile[default]:NEEDS[Kerbalism,ProfileDefault,CommunityResourcePack]:AFTER[KerbalismDefault]
{
    Process
    {
        name = rw compact fission
        title = Integrated RoosterWorks reactor
        modifier = _RWCompactReactor
        input = EnrichedUranium@0.0000000065206
        output = DepletedFuel@0.0000000065206
        output = ElectricCharge@5
        dump_valve = ElectricCharge
    }
}
// Unsupported Kerbalism profiles do not receive an inert or free-power reactor.
!PART[RW_PWR_*_REACTOR]:NEEDS[Kerbalism,!ProfileDefault] {}
@PART[RW_PWR_250,RW_PWR_375]:NEEDS[VABOrganizer]:AFTER[VABOrganizer]
{
    %VABORGANIZER
    {
        %organizerSubcategory = batteries
    }
}
@PART[RW_PWR_*_REACTOR]:NEEDS[VABOrganizer]:AFTER[VABOrganizer]
{
    %VABORGANIZER
    {
        %organizerSubcategory = nuclearReactors
    }
}
@PART[RW_PWR_250]:FOR[RoosterWorksStationModules]
{
    %description = Crewless 2.5 m power and service core with 3500 EC storage. Eight cell cabinets, protected cables and sealed endcaps. Stores vessel electricity; generation is supplied separately. Optional nuclear edition is a separate editor choice. Exterior cooling hardware is cosmetic on this passive edition.
}
@PART[RW_PWR_375]:FOR[RoosterWorksStationModules]
{
    %description = Crewless 3.75 m power and service core with 6750 EC storage. Eight cell cabinets, protected cables and sealed endcaps. Stores vessel electricity; generation is supplied separately. Optional nuclear edition is a separate editor choice. Exterior cooling hardware is cosmetic on this passive edition.
}
''')
    (ROOT/'Media/CompactReactor-stats.json').write_text(json.dumps([dict(size=size,output_ec_per_second=5*f,fuel_capacity=1.5*f,waste_capacity=1.5*f,fuel_units_per_second=RATE*f,added_dry_mass=.039*f,full_power_lifetime_seconds=1.5/RATE,battery_ec=3500 if size==250 else 6750) for size,f in ((250,1.1),(375,1.2))],indent=2)+'\n')
    from build_power_options import build as power_options
    power_options()
    from build_storage_balance import build as storage_balance
    storage_balance()
    from build_catalogue import build as catalogue
    catalogue()
    from build_ring_options import build as ring_options
    ring_options()
    from build_logistics_options import build as logistics_options
    logistics_options()

if __name__=='__main__':build()
