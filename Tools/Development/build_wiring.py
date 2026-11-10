"""Build the wiring toggle on top of the flag test release, without rendering."""
from pathlib import Path
import json
import math
import re
import sys

import zipfile

here = Path(__file__).resolve().parent
sdk = here.parent / "Releases/2026-11-02/RoosterWorks-Station-Modules-v0.7.6-Source"
sys.path[:0] = [str(sdk/"Source"), str(sdk/"Tools")]
from config_nodes import Node, dump, parse
from native_derivatives import write
from native_model import load, walk

prefix = "GameData/RoosterWorksStationModules/"
with zipfile.ZipFile(here/"RoosterWorks-Station-Modules-v0.7.7-test.1.zip") as previous:
    files = {name: previous.read(name) for name in previous.namelist()}

def mirror_elbow_mesh(mesh, radius, angle):
    # Straight collars meet a circular bend at the two tangent points.
    co, si = math.cos(angle), math.sin(angle)
    for i, (x,y,z) in enumerate(mesh["vertices"]):
        dx, dy = radius/2-x, y+radius/2
        curved = dy >= 0 and dx >= 0
        if curved:
            distance = math.hypot(dx,dy)
            nx, ny = dx/distance, -dy/distance
            u = radius-distance
        elif dy < 0:
            nx, ny, u = 1, 0, x+radius/2
        else:
            nx, ny, u = 0, -1, radius/2-y
        v = u*co+z*si
        mesh["vertices"][i] = (x+(v-u)*nx, y+(v-u)*ny, z*co-u*si)
        stretch = (radius-v)/(radius-u) if curved else 1
        for key in ("normals","tangents"):
            if key not in mesh:
                continue
            a,b,c,*extra = mesh[key][i]
            radial = a*nx+b*ny
            along = -a*ny+b*nx
            along *= 1/stretch if key == "normals" else stretch
            radial_out = radial*co+c*si
            vec = (radial_out*nx-along*ny,radial_out*ny+along*nx,c*co-radial*si)
            length = math.hypot(*vec)
            mesh[key][i] = tuple(axis/length for axis in vec)+tuple(extra)

patches = []
tested = set()
for cfg, data in list(files.items()):
    if not cfg.startswith(prefix+"Parts/") or not cfg.endswith(".cfg"):
        continue
    part = parse(data.decode("cp1252")).children[0]
    model_url = next(c for c in part.children if c.header == "MODEL").get("model")
    stem = model_url.split("/")[-1]
    hub = stem.startswith("RW_HUB_")
    elbow = stem.startswith("RW_ELB_")
    if stem not in tested:
        path = sdk/"GameData"/(model_url+".mu")
        assert path.read_bytes() == files["GameData/"+model_url+".mu"]
        model = load(path)
        wires = [n for n in model.root["children"] if re.fullmatch(
            r"RW_(04_Stack|05_\w+)_[01]_service_(blue|yellow)(_Mounts)?", n["name"])]
        assert len(wires) == (40 if hub else 8), (stem,len(wires))
        for n in wires:
            assert n["position"] == (0,0,0) and n["rotation"] == (0,0,0,1) and n["scale"] == (1,1,1)
            assert not n["children"] and "collider" not in n
            if elbow:
                angle = -.13 if "_blue" in n["name"] else -.184
                mirror_elbow_mesh(n["mesh"],1.8*int(stem.split("_")[-1])/250,angle)
        if elbow:
            model.name = model.root["name"] = stem+"_MirroredWiring"
            model.root["children"] = wires
            # These prefabs supply meshes only. Reuse one valid metal material on disk.
            material = model.materials[wires[-1]["materials"][0]]
            tex = material["properties"]["_MainTex"]
            model.textures = [model.textures[tex["index"]]]
            tex["index"] = 0
            model.materials = [material]
            for n in wires:
                n["materials"] = [0]
            temp = here/"ElbowMeshes"
            temp.mkdir(exist_ok=True)
            target = Path(temp)/(model.name+".mu")
            write(model,target)
            checked = load(target)
            assert [n["name"] for n in checked.root["children"]] == [n["name"] for n in wires]
            files[prefix+"Models/"+target.name] = target.read_bytes()
        tested.add(stem)
    values = [("name","ModuleRWStationWiring")]
    if hub:
        values.append(("hub","True"))
    if elbow:
        values.append(("elbowModel",model_url))
    patches.append(Node("@PART["+part.get("name")+"]",children=[Node("MODULE",values)]))

assert len(tested) == 47 and len(patches) == 49
files[prefix+"Compatibility/StationWiring.cfg"] = "\n".join(map(dump,patches)).encode()
files[prefix+"Plugins/RoosterWorksStationWiring.dll"] = (here/"RoosterWorksStationWiring.dll").read_bytes()
version = prefix+"RoosterWorksStationModules.version"
meta = json.loads(files[version])
meta["VERSION"]["BUILD"] = 2
files[version] = (json.dumps(meta,indent=2)+"\n").encode()
target = here/"RoosterWorks-Station-Modules-v0.7.7-test.2.zip"
tmp = target.with_suffix(".partial")
with zipfile.ZipFile(tmp,"w",zipfile.ZIP_DEFLATED,compresslevel=1) as z:
    for name,data in sorted(files.items()):
        z.writestr(name,data)
with zipfile.ZipFile(tmp) as z:
    assert len(z.namelist()) == len(files) and all(z.read(p) == v for p,v in files.items())
tmp.replace(target)
print("Verified wiring targets on 47 models and configuration for 49 parts.")

