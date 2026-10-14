"""Permit only the two explicitly rebuilt ring/menu DLLs in historical guards.

All historical expected binaries remain embedded. New source/binary hashes
are pinned to the reviewed dev3 hotfix; behavioural tests remain mandatory.
"""
import hashlib,json
from pathlib import Path
def check_digest(root,path,expected):
    root=Path(root);p=root/path
    if hashlib.sha256(p.read_bytes()).hexdigest()==expected:return True
    policy=json.loads((root/'Source/Balancing/ring_hotfix_policy.json').read_text())
    entry=policy.get(path)
    if entry is None:return False
    previous=root/'Source/Balancing/075dev2Runtime'/(p.name+'.bin')
    if hashlib.sha256(previous.read_bytes()).hexdigest()!=expected:return False
    if hashlib.sha256(p.read_bytes()).hexdigest()!=entry['after_binary']:return False
    return all(hashlib.sha256((root/n).read_bytes()).hexdigest()==h for n,h in entry['sources'].items())
