"""Portable role-based EC capacity policy: reference base + 5%, before MM."""
from pathlib import Path
import re,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
POLICY=ROOT/'Source/Balancing/electric_charge_policy.json'
def policy():return json.loads(POLICY.read_text())
def storage(text):
    matches=[]
    for match in re.finditer(r'\bRESOURCE\s*\{[^{}]*\}',text):
        block=match.group()
        if re.search(r'\bname\s*=\s*ElectricCharge\s*(?:\r?\n|$)',block) and 'maxAmount' in block:matches.append(match)
    assert len(matches)<=1,'Duplicate EC storage nodes'
    return matches[0] if matches else None
def set_capacity(text,amount,max_amount=None):
    match=storage(text)
    if match is None:
        assert float(amount)==0;return text
    block=match.group();max_amount=amount if max_amount is None else max_amount
    for key,value in (('amount',amount),('maxAmount',max_amount)):
        block,count=re.subn(r'(\b'+key+r'\s*=[ \t]*)[-+\d.eE]+',lambda m:m.group(1)+str(value),block)
        assert count==1
    return text[:match.start()]+block+text[match.end():]
def apply():
    report=[]
    for name,entry in policy()['parts'].items():
        p=ROOT/f'GameData/RoosterWorksStationModules/Parts/{name}.cfg'
        text=p.read_bytes().decode('utf-8');value=format(entry['target_base_ec'],'.10g')
        p.write_bytes(set_capacity(text,value).encode('utf-8'))
        report.append({'part':name,'base_ec':entry['target_base_ec'],'reference':entry['reference'],'expected_default_ec':entry['target_base_ec']*(2.8 if entry['crew']>0 else 1)})
    (ROOT/'Media/ElectricCharge-balance.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
def check_preserved(root,path,expected):
    """Require historical bytes, or exactly an authorized EC-only delta."""
    root=Path(root);p=root/path;current=p.read_bytes()
    if hashlib.sha256(current).hexdigest()==expected:return
    entries=json.loads((root/'Source/Balancing/electric_charge_policy.json').read_text())['parts']
    assert p.parent==root/'GameData/RoosterWorksStationModules/Parts' and p.stem in entries,('Unrelated change',path)
    candidates=[root/'Source/Balancing'/folder/p.name for folder in ('v012-before','v013-before','v015-before')]
    matches=[q.read_bytes() for q in candidates if q.is_file() and hashlib.sha256(q.read_bytes()).hexdigest()==expected]
    assert matches,('Historical fingerprint mismatch',path)
    old=matches[0]
    before=storage(old.decode('utf-8'));assert before is not None
    amount=re.search(r'\bamount\s*=\s*([-+\d.eE]+)',before.group()).group(1)
    capacity=re.search(r'\bmaxAmount\s*=\s*([-+\d.eE]+)',before.group()).group(1)
    restored=set_capacity(current.decode('utf-8'),amount,capacity).encode('utf-8')
    assert restored==old,('Change outside EC capacity',path)
if __name__=='__main__':apply()
