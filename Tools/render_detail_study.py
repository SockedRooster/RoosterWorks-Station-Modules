"""Compare exported MU geometry and decoded runtime DDS normal maps."""
from pathlib import Path
import sys,math,zipfile,bpy
R=Path(__file__).resolve().parents[1];sys.path[:0]=[str(R/'.build-deps'),str(R/'Tools')]
from PIL import Image,ImageDraw,ImageFont
import numpy as np
from mathutils import Vector
helper=R/'Tools/create_gravity_blend.py'
exec(compile(helper.read_text().split("scene=bpy.context.scene;scene.name='RW_GRAV_250'")[0],str(helper),'exec'))
OUT=R/'Media/DetailStudy02';OUT.mkdir(exist_ok=True)
BASE=R/'Source/Study02Baseline'
if (R.parent/'RoosterWorks-Visual-Development-01-Install.zip').exists():
    with zipfile.ZipFile(R.parent/'RoosterWorks-Visual-Development-01-Install.zip') as z:
        for name in z.namelist():
            if '/Models/' in name and name.endswith('.png'):(BASE/Path(name).name).write_bytes(z.read(name))
for kind in ('quilt','foil'):
    packed=np.asarray(Image.open(GD/f'Models/rwm_{kind}_NRM.dds').convert('RGBA'),dtype=float)[::-1]/255
    x=packed[:,:,3]*2-1;y=packed[:,:,1]*2-1;z=np.sqrt(np.maximum(0,1-x*x-y*y))
    rgb=np.uint8(np.stack((x,y,z),axis=-1)*127.5+127.5)
    Image.fromarray(rgb).save(OUT/f'{kind}_decoded.png')

baseline=False
def material(src,model):
    name=model.textures[src['properties']['_MainTex']['index']]['name'];key=(name,src['shader'])
    if key in materials:return materials[key]
    mat=bpy.data.materials.new(src['name']);mat.use_nodes=True
    nodes=mat.node_tree.nodes;links=mat.node_tree.links;p=nodes.get('Principled BSDF')
    path=(BASE if baseline else GD/'Models')/(name+'.png')
    tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(path),check_existing=False);tex.image.alpha_mode='CHANNEL_PACKED';tex.image.pack()
    links.new(tex.outputs['Color'],p.inputs['Base Color']);p.inputs['Roughness'].default_value=.55
    if '_BumpMap' in src['properties']:
        kind='quilt' if 'cladding' in name else 'foil'
        texn=nodes.new('ShaderNodeTexImage');texn.image=bpy.data.images.load(str(OUT/f'{kind}_decoded.png'),check_existing=True);texn.image.colorspace_settings.name='Non-Color';texn.image.pack()
        normal=nodes.new('ShaderNodeNormalMap');normal.inputs['Strength'].default_value=1.;links.new(texn.outputs['Color'],normal.inputs['Color']);links.new(normal.outputs['Normal'],p.inputs['Normal'])
        p.inputs['Roughness'].default_value=.62 if kind=='quilt' else .38
        p.inputs['Specular IOR Level'].default_value=.28 if kind=='quilt' else .55
    if name in ('rwm_steel','rwm_rail','rwm_bronze'):p.inputs['Roughness'].default_value=.42
    # Daylight view: don't invent emissive window glow or replace dark albedo.
    if 'glass' in name:p.inputs['Roughness'].default_value=.22
    materials[key]=mat;return mat

def aim(obj,target):obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()

for role,view in [('HABS','Overall'),('HAB','Overall'),('HABS','Surface'),('HABS','Endcap')]:
    for before in (True,False):
        baseline=before;materials={};images={}
        name=f'{role}_{view}_'+('Before' if before else 'After')
        scene=bpy.data.scenes.new(name);bpy.context.window.scene=scene
        import_model((BASE if before else GD/'Models')/f'RW_{role}_250.mu',scene)
        for ob in scene.objects:
            parent=ob
            while parent:
                if parent.name.split('.')[0]=='SideHatch':ob.hide_render=True
                parent=parent.parent
        scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
        scene.render.resolution_x=1100;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
        world=bpy.data.worlds.new(name);scene.world=world;world.use_nodes=True
        world.node_tree.nodes['Background'].inputs['Color'].default_value=(.07,.085,.105,1);world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
        for pos,power,size in [((1,5,6),1000,3),((-5,-3,4),850,4),((4,-1,1),400,3)]:
            light=bpy.data.lights.new('Studio','AREA');obj=bpy.data.objects.new('Studio',light);scene.collection.objects.link(obj);obj.location=pos;light.energy=power;light.size=size;aim(obj,(0,0,0))
        camera=bpy.data.cameras.new(name);obj=bpy.data.objects.new(name,camera);scene.collection.objects.link(obj);scene.camera=obj;camera.type='ORTHO'
        if view=='Overall':obj.location=(5,8,4);camera.ortho_scale=3.55 if role=='HABS' else 5.1;target=(0,0,0)
        elif view=='Endcap':obj.location=(3,3,7);camera.ortho_scale=2.9;target=(0,0,.75)
        else:
            theta=math.pi/3+.25;target=(1.19*math.sin(theta),1.19*math.cos(theta),.31);obj.location=(target[0]+3*math.sin(theta),target[1]+3*math.cos(theta),target[2]+1.1);camera.ortho_scale=1.32
        aim(obj,target);scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.filepath=str(OUT/(name+'.png'))
        bpy.ops.render.render(write_still=True);print('Rendered '+name,flush=True)
bpy.ops.wm.save_as_mainfile(filepath=str(R/'Source/Blender/RW_DetailStudy02.blend'))
bold=ImageFont.truetype('C:/Windows/Fonts/segoeuib.ttf',34);small=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',23)
sheet=Image.new('RGB',(2200,2380),(15,22,28));d=ImageDraw.Draw(sheet)
d.text((35,22),'ROOSTERWORKS / TACTILE EXTERIOR STUDY 02',font=bold,fill=(238,236,219))
d.text((35,73),'Matched light • exported MU geometry + runtime DDS normals • Blender preview; KSP testing pending',font=small,fill=(167,185,195))
for row,(role,view) in enumerate((('HABS','Overall'),('HAB','Overall'),('HABS','Surface'),('HABS','Endcap'))):
    for col,state in enumerate(('Before','After')):
        x=col*1100;y=120+row*550
        photo=Image.open(OUT/f'{role}_{view}_{state}.png').convert('RGB').resize((550,550))
        sheet.paste(photo,(x+225,y))
        d.text((x+30,y+20),('PASS 01' if col==0 else 'STUDY 02')+' / '+role+' / '+view.upper(),font=small,fill=(226,201,150))
sheet.save(OUT/'Comparison.png')
exec(compile((R/'Tools/compose_detail_review.py').read_text(),str(R/'Tools/compose_detail_review.py'),'exec'))
