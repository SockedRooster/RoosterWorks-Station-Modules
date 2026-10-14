"""Package the 23-part customization candidate; does not publish or install."""
from pathlib import Path
import hashlib,json,zipfile,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
VERSION='v0.7.5-dev.4'

def main():
    subprocess.run([sys.executable,str(ROOT/'Tools/validate.py')],check=True)
    package()

def package():
    """Archive an already validated kit; main() performs the complete validation."""
    files=sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
                 and p.suffix!='.pyc' and p.name!='LOG-collar-QA.png')
    tests=[p for p in files if p.relative_to(ROOT).parts[0]=='GameData']
    tests += [ROOT/f for f in ('README.md','INSTALLATION.md','RELEASE_NOTES.md','LICENSE','CHANGELOG.md',
                              'CHECKSUMS-SHA256.txt','TEST_CHECKLIST-v0.7.0.md','APPEARANCE_TEST_CHECKLIST.md','AIRLOCK_TEST_CHECKLIST.md','POWER_TEST_CHECKLIST.md','ADAPTER_TEST_CHECKLIST.md','GREENHOUSE_TEST_CHECKLIST.md','LARGE_FAMILY_TEST_CHECKLIST.md','ELECTRIC_CHARGE_BALANCE.md','FINISH_AND_REACTOR_OPTIONS.md','POWER_VARIANTS.md','CREW_TUBES_AND_BALANCE.md','ROADMAP.md','VAB_CATALOGUE.md','CUSTOMIZATION_065.md','STATION_EXPANSION_070_075.md','EDITOR_AND_STORAGE_075.md','RING_MENU_HOTFIX.md','COMMAND_STORAGE_075.md')]
    report={}
    for suffix,entries in [('Developer-Source',files),('TEST',tests)]:
        out=ROOT.parent/f'RoosterWorks-Station-Modules-{VERSION}-{suffix}.zip'
        with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
            for p in sorted(entries):
                info=zipfile.ZipInfo(p.relative_to(ROOT).as_posix(),(2026,10,13,12,0,0))
                info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
                archive.writestr(info,p.read_bytes(),compresslevel=9)
        with zipfile.ZipFile(out) as archive:assert archive.testzip() is None
        report[out.name]={'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'bytes':out.stat().st_size,'files':len(entries)}
    dev=ROOT.parent/f'RoosterWorks-Station-Modules-{VERSION}-Developer-Source.zip'
    test=ROOT.parent/f'RoosterWorks-Station-Modules-{VERSION}-TEST.zip'
    with zipfile.ZipFile(dev) as a,zipfile.ZipFile(test) as b:
        ad={n:a.read(n) for n in a.namelist() if n.startswith('GameData/')}
        bd={n:b.read(n) for n in b.namelist() if n.startswith('GameData/')}
        assert ad==bd
    sums=ROOT.parent/f'RoosterWorks-Station-Modules-{VERSION}-SHA256SUMS.txt'
    sums.write_text(''.join(v['sha256']+'  '+k+'\n' for k,v in report.items()))
    (ROOT.parent/f'RoosterWorks-{VERSION}-package-validation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
