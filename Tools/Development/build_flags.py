"""Prepare the first Station Modules test build from the accepted 0.7.6 payload."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

here = Path(__file__).resolve().parent
releases = here.parent / "Releases/2026-11-02"
sdk = releases / "RoosterWorks-Station-Modules-v0.7.6-Source"
sys.path[:0] = [str(sdk/"Tools"), str(sdk/"Source")]
from native_model import load, walk
from config_nodes import parse, dump, Node

prefix = "GameData/RoosterWorksStationModules/"
with zipfile.ZipFile(releases/"RoosterWorks-Station-Modules-v0.7.6.zip") as baseline:
    files = {p:baseline.read(p) for p in baseline.namelist() if p.startswith(prefix)}

targets = {}
for path in sorted((sdk/prefix/"Models").glob("*.mu")):
    assert path.read_bytes() == files[prefix+"Models/"+path.name]
    model = load(path)
    nodes = [n for _, n in walk(model.root)]
    names = []
    for node in nodes:
        materials = [model.materials[i]["name"] for i in node.get("materials", [])]
        if any(m.endswith("_crest") for m in materials):
            assert len(materials) == 1 and node["mesh"]["uvs"]
            assert sum(n["name"] == node["name"] for n in nodes) == 1
            names.append(node["name"])
    assert names, path.name
    targets[path.stem] = names

parts = []
for path, data in sorted(files.items()):
    if not path.startswith(prefix+"Parts/") or not path.endswith(".cfg"):
        continue
    part = parse(data.decode("cp1252")).children[0]
    models = [child.get("model").split("/")[-1] for child in part.children if child.header == "MODEL"]
    assert len(models) == 1, path
    patch = Node("@PART["+part.get("name")+"]")
    for target in targets[models[0]]:
        patch.children.append(Node("MODULE",[("name","FlagDecal"),("textureQuadName",target),("flagDisplayed","True")]))
    patch.children.append(Node("MODULE",[("name","ModuleRWStationFlags")]))
    parts.append(patch)
assert len(parts) == 49 and len(targets) == 47
patch = "\n".join(map(dump,parts))
assert len(parse(patch).children) == len(parts)
files[prefix+"Compatibility/StationFlags.cfg"] = patch.encode()
files[prefix+"Plugins/RoosterWorksStationFlags.dll"] = (here/"RoosterWorksStationFlags.dll").read_bytes()
version = prefix+"RoosterWorksStationModules.version"
meta = json.loads(files[version])
meta["VERSION"].update(PATCH=7,BUILD=1)
files[version] = (json.dumps(meta,indent=2)+"\n").encode()
output = here/"RoosterWorks-Station-Modules-v0.7.7-test.1.zip"
with zipfile.ZipFile(output.with_suffix(".partial"), "w", zipfile.ZIP_DEFLATED, compresslevel=1) as z:
    for name,data in sorted(files.items()):
        z.writestr(name,data)
with zipfile.ZipFile(output.with_suffix(".partial")) as z:
    assert len(z.namelist()) == len(files) and all(z.read(p) == v for p,v in files.items())
output.with_suffix(".partial").replace(output)
print(f"{len(parts)} parts, {len(targets)} models; verified {output.name}")
