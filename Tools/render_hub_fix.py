from pathlib import Path
import bpy,math
R=Path(__file__).resolve().parents[1]
helper=R/'Tools/render_detail_study.py'
exec(compile(helper.read_text().split('for role,view in')[0],str(helper),'exec'))
OUT=R/'Media/HubRouting06';OUT.mkdir(exist_ok=True)
import shutil
for kind in ('quilt','foil'):shutil.copyfile(R/f'Media/DetailStudy02/{kind}_decoded.png',OUT/f'{kind}_decoded.png')
baseline=False
for shot in ('Before','After','Back','Stack','Close'):
    materials={};images={};scene=bpy.data.scenes.new(shot);bpy.context.window.scene=scene
    import_model((R/'Source/Study05Baseline' if shot=='Before' else GD/'Models')/'RW_HUB_250.mu',scene)
    if shot=='Stack':
        for role,offset,rotation in [('CMD',(0,0,2.86),0),('HABS',(0,0,-2.99),0),('CMD',(2.86,0,0),-math.pi/2)]:
            prev=set(scene.objects);import_model(GD/f'Models/RW_{role}_250.mu',scene)
            for obj in set(scene.objects)-prev:
                if obj.parent is None:obj.location=offset;obj.rotation_euler[1]=rotation
                parent=obj
                while parent:
                    if parent.name.split('.')[0]=='SideHatch':obj.hide_render=True
                    parent=parent.parent
    scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
    scene.render.resolution_x=1300;scene.render.resolution_y=1400;scene.render.resolution_percentage=100
    world=bpy.data.worlds.new(shot);scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.07,.085,.105,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
    for pos,energy,size in [((3,-5,8),1600,5),((-6,4,6),1500,5),((4,6,1),700,4)]:
        light=bpy.data.lights.new('Studio','AREA');obj=bpy.data.objects.new('Studio',light);scene.collection.objects.link(obj);obj.location=pos;light.energy=energy;light.size=size;aim(obj,(0,0,0))
    camera=bpy.data.cameras.new(shot);obj=bpy.data.objects.new(shot,camera);scene.collection.objects.link(obj);scene.camera=obj;camera.type='ORTHO';camera.ortho_scale=9 if shot=='Stack' else 5.6;obj.location=(6,-8,4);aim(obj,(0,0,0))
    if shot=='Back':obj.location=(-6,8,4);aim(obj,(0,0,0))
    if shot=='Close':camera.ortho_scale=2.7;aim(obj,(.8,-.8,1.2))
    scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/(shot+'.png'));bpy.ops.render.render(write_still=True);print('Rendered',shot,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/Blender/RW_HubRouting06.blend'))
sheet=Image.new('RGB',(2100,850),(15,22,28));d=ImageDraw.Draw(sheet);font=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',26)
for j,name in enumerate(('After','Back','Stack')):
    im=Image.open(OUT/(name+'.png')).convert('RGB');im.thumbnail((700,754));sheet.paste(im,(j*700,65));d.text((j*700+24,18),name.upper()+' / HUB SERVICE ROUTING',font=font,fill=(230,222,199))
sheet.save(OUT/'Review.png')
