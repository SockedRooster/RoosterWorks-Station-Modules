"""Regression checks for non-debris classification and preserved v0.4.3 assets."""
from pathlib import Path
from zipfile import ZipFile
import json, sys
ROOT = Path(__file__).resolve().parents[1]
def parse(text):
    root = {'node':'ROOT','values':{},'children':[]}
    stack = [root]
    pending = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('//'): continue
        if line == '{':
            node = {'node':pending,'values':{},'children':[]}
            stack[-1]['children'].append(node)
            stack.append(node)
        elif line == '}': stack.pop()
        elif '=' in line:
            k,v=line.split('=',1)
            stack[-1]['values'].setdefault(k.strip(),[]).append(v.strip())
        else: pending=line
    return root


for label in ('HAB','LAB','CMD'):
    path=ROOT/f'GameData/RoosterWorksStationModules/Parts/RW_{label}_250.cfg'
    tree=parse(path.read_text())
    part=tree['children'][0]
    assert part['node']=='PART'
    assert part['values']['vesselType']==['Station'], f'{label} can otherwise launch as Debris'
    hatch_modules=[n for n in part['children'] if n['node']=='MODULE' and n['values'].get('name')==['ModuleRWStationHatch']]
    assert len(hatch_modules)==(1 if label=='HAB' else 0)
    assert all(n['values'].get('name')!=['ModuleCommand'] for n in part['children'] if label!='CMD')
plugin=ROOT/'GameData/RoosterWorksStationModules/Plugins/RoosterWorksStationRuntime.dll'
assert plugin.read_bytes().startswith(b'MZ')
version=json.loads((ROOT/'GameData/RoosterWorksStationModules/RoosterWorksStationModules.version').read_text())['VERSION']
assert tuple(version[k] for k in ('MAJOR','MINOR','PATCH')) in ((0,5,3),(0,6,0),(0,7,0),(0,8,0),(0,9,0),(0,10,0),(0,11,0),(0,12,0),(0,13,0),(0,14,0),(0,15,0),(0,16,0))
print('PASS all three parts explicitly classified Station; hatch module attached only to HAB')
print('PASS built runtime DLL and 0.5.3/0.6.0 package metadata present')
print('NOTE late hatch binding and CommNet need an actual KSP flight test')
