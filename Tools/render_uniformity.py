"""Native export review: default stack, seam, EVA ladder, hatch and ring poses."""
from pathlib import Path
import sys,math,bpy,re,copy,shutil
R=Path(__file__).resolve().parents[1]
helper=R/'Tools/render_detail_study.py'
exec(compile(helper.read_text().split('for role,view in')[0],str(helper),'exec'))
oldout=OUT;OUT=R/'Media/Uniformity04';OUT.mkdir(exist_ok=True)
for kind in ('quilt','foil'):shutil.copyfile(oldout/f'{kind}_decoded.png',OUT/f'{kind}_decoded.png')
sys.path.insert(0,str(R/'Source'))
from native_derivatives import write
from native_model import walk
baseline=False

def model(scene,role,offset=0,hatch=False,file=None):
    previous=set(scene.objects);import_model(file or GD/f'Models/RW_{role}_250.mu',scene)
    added=[o for o in scene.objects if o not in previous]
    for obj in added:
        if obj.parent is None:obj.location.z+=offset
        parent=obj
        while parent:
            hidden='WindowBankStandard' if hatch else 'SideHatch'
            if parent.name.split('.')[0]==hidden:obj.hide_render=True
            parent=parent.parent

ring=load(GD/'Models/RW_GRAV_250.mu')
for path,n in walk(ring.root):
    if re.fullmatch('RW_GravityHinge[0-9]{2}',n['name']):n['rotation']=(0,0,0,1);n['position']=(1.45,0,0)
    if re.fullmatch('RW_GravityPod[0-9]{2}',n['name']):n['rotation']=(0,0,0,1);n['position']=(2.75,0,0);n['scale']=(1,1,1)
    if re.fullmatch('RW_GravityTelescopic[0-9]{2}',n['name']):n['scale']=(1,1,1)
deployed=OUT/'Preview_Deployed.mu';write(ring,deployed)
for shot in ('Stack','Seam','EVA','Hatch','Ring_Stowed','Ring_Deployed'):
    materials={};images={};scene=bpy.data.scenes.new(shot);bpy.context.window.scene=scene
    if shot in ('Stack','Seam'):
        model(scene,'HABS');model(scene,'CMD',1.85);model(scene,'AIR',3.91)
        if shot=='Stack':target=(0,0,2.05);position=(4,-10,5.2);span=7.0
        else:
            t=2*math.pi/3;target=(1.3*math.sin(t),1.3*math.cos(t),.99);position=(target[0]+3*math.sin(t+.5),target[1]+3*math.cos(t+.5),1.22);span=1.65
    elif shot=='EVA':
        model(scene,'AIR');target=(0,0,-.05);position=(2.2,7,1.8);span=3.25
    elif shot=='Hatch':
        model(scene,'HABS',hatch=True);t=math.pi/3;target=(.9*math.sin(t),.9*math.cos(t),0);position=(5*math.sin(t+.25),5*math.cos(t+.25),1.1);span=2.3
    else:
        model(scene,'GRAV',file=deployed if shot=='Ring_Deployed' else None);target=(0,0,0)
        position=(7,-11,10) if shot=='Ring_Deployed' else (5,-8,4);span=11.4 if shot=='Ring_Deployed' else 5.8
    scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
    scene.render.resolution_x=1200;scene.render.resolution_y=1300;scene.render.resolution_percentage=100
    world=bpy.data.worlds.new(shot);scene.world=world;world.use_nodes=True;world.node_tree.nodes['Background'].inputs['Color'].default_value=(.07,.085,.105,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.5
    sizefactor=2 if 'Ring' in shot else 1
    for pos,energy,size in [((3,-5,8),1600,5),((-6,4,6),1500,5),((4,6,1),700,4)]:
        light=bpy.data.lights.new('Studio','AREA');obj=bpy.data.objects.new('Studio',light);scene.collection.objects.link(obj);obj.location=tuple(v*sizefactor for v in pos);light.energy=energy*sizefactor**2;light.size=size*sizefactor;aim(obj,target)
    camera=bpy.data.cameras.new(shot);obj=bpy.data.objects.new(shot,camera);scene.collection.objects.link(obj);scene.camera=obj;camera.type='ORTHO';camera.ortho_scale=span;obj.location=position;aim(obj,target)
    scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/(shot+'.png'));bpy.ops.render.render(write_still=True);print('Rendered '+shot,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/Blender/RW_Uniformity04.blend'))
bold=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',36);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',24)
sheet=Image.new('RGB',(2400,1530),(15,22,28));d=ImageDraw.Draw(sheet)
d.text((35,20),'ROOSTERWORKS / UNIFIED SERVICE LANES + CLEAN HATCHES',font=bold,fill=(238,236,219))
d.text((35,72),'Native models in default orientation • geometrically aligned interfaces • Blender preview; KSP verification pending',font=small,fill=(168,186,196))
for j,name in enumerate(('Stack','Seam','EVA','Hatch','Ring_Stowed','Ring_Deployed')):
    x=(j%3)*800;y=145+(j//3)*690;im=Image.open(OUT/(name+'.png')).convert('RGB').resize((600,650));sheet.paste(im,(x+100,y));d.text((x+24,y-36),name.replace('_',' ').upper(),font=small,fill=(229,202,154))
sheet.save(OUT/'Review.png')
