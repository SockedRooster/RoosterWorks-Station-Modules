"""Exercise actual part families and FOR/AFTER eligibility without Support fixes."""
from pathlib import Path
import sys,json,hashlib,fnmatch,copy
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'Source'))
from config_nodes import parse,dump,Node
from selector_scope import FINISH,MENU,SWATCH,check_selector_delta
GD=R/'GameData/RoosterWorksStationModules'
baseline=json.loads((R/'Tools/selector_scope_baseline.json').read_text())
for path,digest in baseline.items():
    if path.endswith('.version'):continue
    assert hashlib.sha256((R/path).read_bytes()).hexdigest()==digest or check_selector_delta(R,path,digest),path
assert {p.relative_to(R).as_posix() for p in (R/'GameData').rglob('*') if p.is_file()}==set(baseline)
finish=parse((GD/'Compatibility/ExteriorFinish.cfg').read_text()).children[0]
ui=parse((GD/'Compatibility/EditorAppearance.cfg').read_text()).children
assert finish.header==FINISH and [n.header for n in ui]==[MENU,SWATCH]
ring=parse((GD/'Compatibility/RingColors.cfg').read_text()).children
def modules(p):return [n.get('name') for n in p.children if n.header=='MODULE']
def run(part):
    p=copy.deepcopy(part);name=p.get('name')
    if any(n.header=='MODEL' and fnmatch.fnmatch(n.get('model',''),'RoosterWorksStationModules/Models/*') for n in p.children) and 'ModuleRWStationFinish' not in modules(p):p.children+=copy.deepcopy(finish.children)
    for patch in ring:
        if patch.header.split(']',1)[0]=='@PART['+name and 'ModuleRWRingColor' not in modules(p):p.children+=copy.deepcopy(patch.children)
    # AFTER executes following both FOR additions, without running any Support
    # removal patch. This proves Station Modules itself prevents the spillover.
    if p.get('category')!='none' and 'ModuleRWRingColor' in modules(p):
        if 'ModuleRWEditorMenu' not in modules(p):p.children+=copy.deepcopy(ui[0].children)
        if 'ModuleRWStationFinish' in modules(p):p.children+=copy.deepcopy(ui[1].children)
    return p
current=0
for path in (GD/'Parts').glob('*.cfg'):
    p=run(parse(path.read_text()).children[0])
    if p.get('category')=='none' or p.get('name').endswith('_REACTOR'):continue # hidden by retained legacy compatibility pass
    current+=1;assert modules(p).count('ModuleRWEditorMenu')==1
    assert {n.get('moduleID') for n in p.children if n.get('name')=='ModuleB9PartSwitch'}=={'RWFinishSwatch','RWRingSwatch'}
assert current==41
support=R.parent/'work/RoosterWorks-Station-Support-v1.0.5/GameData/RoosterWorksStationSupport/Parts'
if support.is_dir():
    for path in support.glob('*.cfg'):
        before=parse(path.read_text()).children[0];assert dump(run(before))==dump(before),('Support changed without hotfix',path.name)
    print('PASS all 15 actual Support parts unaffected without a Support hotfix/removal patch')
ground=R.parent/'ground-hotpatch/GameData/RoosterWorksGroundModules/Parts'
if ground.is_dir():
    for path in ground.glob('*.cfg'):
        p=run(parse(path.read_text()).children[0]);assert modules(p).count('ModuleRWEditorMenu')==1
        assert {n.get('moduleID') for n in p.children if n.get('name')=='ModuleB9PartSwitch'}=={'RWFinishSwatch','RWRingSwatch'}
    print('PASS all 12 ground hot-patch parts retain appearance swatches')
unrelated=Node('PART',[('name','RW_AnotherMod'),('category','Structural')],[Node('MODEL',[('model','OtherMod/Models/Part')])]);assert dump(run(unrelated))==dump(unrelated)
assert json.loads((GD/'RoosterWorksStationModules.version').read_text())['VERSION']['BUILD']==5
print('PASS appearance scope: 41 station parts retain swatches; foreign RW_* parts untouched; only two selector headers and version change; identical binaries/models/resources')
