"""Blender previews imported from the shipped MU files; no render-only geometry."""
from pathlib import Path
import sys,math,bpy
from mathutils import Vector
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'.build-deps'))
helper=R/'Tools/create_gravity_blend.py'
source=helper.read_text().split("scene=bpy.context.scene;scene.name='RW_GRAV_250'")[0]
source=source.replace("key=(src['name'],src['shader'])","key=(src['name'],src['shader'],model.textures[src['properties']['_MainTex']['index']]['name'])")
exec(compile(source,str(helper),'exec'))
out=R/'Media/VisualUpgrade';out.mkdir(exist_ok=True)

def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()

def preview(role,baseline=False,close=False):
    global GD,materials,images
    materials={};images={}
    name=role+('_Before' if baseline else '_After')+('_Detail' if close else '')
    scene=bpy.data.scenes.new(name);bpy.context.window.scene=scene
    GD=R/'GameData/RoosterWorksStationModules'
    path=(R/'Source/VisualBaseline' if baseline else GD/'Models')/f'RW_{role}_250.mu'
    import_model(path,scene)
    if baseline:
        for tex,image in images.items():
            original=R/'Source/VisualBaseline'/(tex+'.png')
            if original.exists():
                # Substitute only baseline albedo; same importer and lighting.
                replacement=bpy.data.images.load(str(original));replacement.pack()
                for mat in materials.values():
                    for node in mat.node_tree.nodes:
                        if node.type=='TEX_IMAGE' and node.image==image:node.image=replacement
    # Show the Standard habitat option; preserve alternative in the editable file.
    for o in scene.objects:
        parent=o
        while parent:
            if parent.name.split('.')[0]=='SideHatch':o.hide_render=True
            parent=parent.parent
    scene.render.engine='CYCLES';scene.cycles.samples=24;scene.cycles.use_denoising=True
    scene.render.resolution_x=1000;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
    scene.render.image_settings.file_format='PNG'
    world=bpy.data.worlds.new(name);scene.world=world;world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.055,.075,.105,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
    for pos,energy,size in [((-4,-6,7),1500,5),((4,1,5),1900,4),((2,-4,-1),300,3)]:
        data=bpy.data.lights.new('Studio','AREA');o=bpy.data.objects.new('Studio',data);scene.collection.objects.link(o);o.location=pos;data.energy=energy;data.shape='DISK';data.size=size;aim(o,(0,0,0))
    data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);scene.camera=o;data.type='ORTHO'
    if close:
        t=math.pi-.64;focus=(1.24*math.sin(t),1.24*math.cos(t),1.26)
        o.location=(focus[0]+2*math.sin(t+.25),focus[1]+2*math.cos(t+.25),focus[2]+.5);data.ortho_scale=.78
        aim(o,focus)
    else:
        o.location=(5,-8,4);data.ortho_scale=5.4 if role=='HAB' else 4.3;aim(o,(0,0,0))
    scene.view_settings.view_transform='AgX';scene.render.filepath=str(out/(name+'.png'))
    bpy.ops.render.render(write_still=True)
    print('Rendered '+name,flush=True)

for role,baseline,close in [('HAB',True,False),('HAB',False,False),('HAB',True,True),('HAB',False,True),('LAB',False,False),('CMD',False,False),('CUP',False,False),('LOG',False,False)]:preview(role,baseline,close)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/Blender/RW_VisualUpgrade_Review.blend'))
from PIL import Image,ImageDraw,ImageFont
f=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',32)
small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',22)
sheet=Image.new('RGB',(2000,1410),(13,20,28));d=ImageDraw.Draw(sheet)
d.text((35,18),'ROOSTERWORKS / EXTERIOR DETAIL STUDY',font=f,fill=(235,235,220))
d.text((35,65),'Actual exported KSP meshes • matched lighting • Blender preview, in-game review pending',font=small,fill=(155,181,191))
for i,name in enumerate(('HAB_Before','HAB_After','HAB_Before_Detail','HAB_After_Detail')):
    x=i*500;photo=Image.open(out/(name+'.png')).convert('RGB').resize((500,550))
    sheet.paste(photo,(x,150));d.text((x+24,110),('ORIGINAL' if 'Before' in name else 'UPGRADED')+(' / DETAIL' if 'Detail' in name else ''),font=small,fill=(230,206,159))
for i,role in enumerate(('LAB','CMD','CUP','LOG')):
    photo=Image.open(out/(role+'_After.png')).convert('RGB').resize((500,550));sheet.paste(photo,(i*500,780));d.text((i*500+24,740),'RW-'+role+' / UPGRADED',font=small,fill=(230,206,159))
d.text((35,1360),'15 models • 13 shared surface maps • original collisions, variants, shaders and gameplay retained',font=small,fill=(155,181,191))
sheet.save(out/'Review.png')
