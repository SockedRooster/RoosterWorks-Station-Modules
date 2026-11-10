from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R.parent/'ground-hotpatch-v22/Tools/create_equipment_blend.py').read_text()
s=s.replace("CORE=R.parent/'rw-v075dev5'","CORE=R").replace("GD=R/'GameData/RoosterWorksGroundModules'","GD=R/'GameData/RoosterWorksStationModules'")
s=s[:s.index('for i,path in enumerate(sorted')]+'''scene=bpy.context.scene;scene.name='RW_GRAV_250'
scene.unit_settings.system='METRIC';import_model(GD/'Models/RW_GRAV_250.mu',scene)
folder=R/'Source/Blender';folder.mkdir(exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=str(folder/'RW_GRAV_250.blend'))
print('PASS packed native-equivalent editable gravity ring scene')
'''
(R/'Tools/create_gravity_blend.py').write_text(s)
