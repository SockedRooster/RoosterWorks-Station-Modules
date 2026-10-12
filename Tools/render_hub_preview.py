"""Render actual hub mesh using the established textured software renderer."""
from pathlib import Path
import sys,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
import build_hub250 as hub
import render_window_comparison as renderer
hub.generate_geometry=lambda variant: hub.geometry()
hub.point=lambda radius,theta,y:(0,0,0)
renderer.load=lambda root,name:hub
out=renderer.render(ROOT,'hub',angle_offset=-.35,span=5.8)
out.save(ROOT/'Media/HUB-250-preview.png')
print(ROOT/'Media/HUB-250-preview.png')
