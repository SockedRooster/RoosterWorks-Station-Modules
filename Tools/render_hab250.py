#!/usr/bin/env python3
"""Generate offscreen visual previews of the actual RW-HAB-250 OBJ mesh."""
import vtk
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
OBJ=ROOT/'Source/Blender/RW_HAB_250.obj'
OUT=ROOT/'Media'
OUT.mkdir(exist_ok=True)

def render(pos,out,source_obj=OBJ):
    window=vtk.vtkEGLRenderWindow()
    window.SetOffScreenRendering(1)
    window.SetSize(900,950)
    window.SetMultiSamples(8)
    ren=vtk.vtkRenderer();window.AddRenderer(ren)
    ren.SetBackground(.033,.056,.084)
    ren.SetBackground2(.006,.012,.028)
    ren.GradientBackgroundOn()
    imp=vtk.vtkOBJImporter();imp.SetFileName(str(source_obj));imp.SetFileNameMTL(str(source_obj.with_suffix('.mtl')))
    imp.SetTexturePath(str(OBJ.parent));imp.SetRenderWindow(window);imp.Update()
    actors=ren.GetActors(); actors.InitTraversal()
    for i in range(actors.GetNumberOfItems()):
        actor=actors.GetNextActor()
        p=actor.GetProperty()
        p.SetAmbient(.39)
        p.SetDiffuse(.66)
        p.SetSpecular(.13)
        p.SetSpecularPower(36)
        p.SetInterpolationToPhong()
        if actor.GetTexture():actor.GetTexture().InterpolateOn()
    ren.AutomaticLightCreationOff()
    for position,color,intensity in [((7,8,9),(1,.96,.91),1.05),((-6,2,-8),(.65,.81,1),.65),((6,5,-9),(.94,1,1),.82),((-8,7,8),(.75,.85,1),.72)]:
        light=vtk.vtkLight();light.SetLightTypeToSceneLight();light.SetPosition(*position);light.SetFocalPoint(0,0,0)
        light.SetIntensity(intensity);light.SetColor(*color);ren.AddLight(light)
    camera=vtk.vtkCamera();camera.SetPosition(*pos);camera.SetFocalPoint(0,0,0)
    camera.SetViewUp(0,1,0);camera.SetViewAngle(35)
    ren.SetActiveCamera(camera);ren.ResetCameraClippingRange()
    window.Render()
    extract=vtk.vtkWindowToImageFilter();extract.SetInput(window);extract.SetInputBufferTypeToRGBA();extract.ReadFrontBufferOff();extract.Update()
    writer=vtk.vtkPNGWriter();writer.SetInputConnection(extract.GetOutputPort());writer.SetFileName(str(out));writer.Write()
    print('Rendered',out)

render((6.3,3.1,7.5),OUT/'RW-HAB-250_WindowSide.png')
render((6.3,3.1,7.5),OUT/'RW-HAB-250_SideHatch.png',ROOT/'Source/Blender/RW_HAB_250_SideHatch.obj')
render((3.6,2.8,-8.7),OUT/'RW-HAB-250_BrandSide.png')
render((4.1,9.8,-5.3),OUT/'RW-HAB-250_FlushEndcap.png')

# Build multi-angle design review sheet.
W,H=2250,1030
sheet=Image.new('RGB',(W,H),(7,12,23));d=ImageDraw.Draw(sheet)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
title=ImageFont.truetype(bold,53);sub=ImageFont.truetype(font,27)
section=ImageFont.truetype(bold,22);small=ImageFont.truetype(font,18)
d.text((65,27),'RW-HAB-250  |  ORBITAL HABITAT',font=title,fill=(237,242,245))
d.text((68,94),'RoosterWorks Station Modules · v0.2.7 | genuine cylinder-conforming frames (no floating side wings) | working warm-white cabin glow · actual generated OBJ mesh',font=sub,fill=(156,183,207))
for j,(filename,head,details) in enumerate([
    ('RW-HAB-250_WindowSide.png','01  LARGER PRESSURE WINDOWS','Full upper/lower curved bezel + larger square windows'),
    ('RW-HAB-250_SideHatch.png','02  OPTIONAL SIDE HATCH','All four hatch mounting edges conform to curved hull'),
    ('RW-HAB-250_FlushEndcap.png','03  THINNER END RIMS','Flush bulkheads + slim stack seams')]):
    x=34+j*738; y=158; w=714; h=806
    photo=Image.open(OUT/filename).convert('RGB').resize((w,h),Image.Resampling.LANCZOS)
    sheet.paste(photo,(x,y))
    d.rounded_rectangle((x,y,x+w,y+h),radius=13,outline=(56,75,94),width=2)
    d.rectangle((x+16,y+12,x+w-17,y+54),fill=(12,20,32))
    d.text((x+25,y+22),head,font=section,fill=(240,240,239))
    d.text((x+23,y+h-35),details,font=small,fill=(196,209,215))
sheet.save(OUT/'RW-HAB-250-v0.2.7-Review-Render.png',optimize=True)
print('Generated review sheet',OUT/'RW-HAB-250-v0.2.7-Review-Render.png')
