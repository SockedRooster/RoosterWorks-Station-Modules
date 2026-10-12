#!/usr/bin/env python3
"""Renders the ACTUAL generated lab OBJ mesh, not AI imagery."""
from pathlib import Path
import vtk
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OBJ=ROOT/'Source/Blender/RW_LAB_250.obj'
OUT=ROOT/'Media';OUT.mkdir(exist_ok=True)

def view(camera,out):
    window=vtk.vtkEGLRenderWindow();window.SetOffScreenRendering(1)
    window.SetSize(740,770);window.SetMultiSamples(4)
    scene=vtk.vtkRenderer();window.AddRenderer(scene)
    scene.SetBackground(.03,.055,.083);scene.SetBackground2(.005,.012,.028);scene.GradientBackgroundOn()
    imp=vtk.vtkOBJImporter()
    imp.SetFileName(str(OBJ));imp.SetFileNameMTL(str(OBJ.with_suffix('.mtl')))
    imp.SetTexturePath(str(OBJ.parent));imp.SetRenderWindow(window);imp.Update()
    collection=scene.GetActors();collection.InitTraversal()
    for i in range(collection.GetNumberOfItems()):
        actor=collection.GetNextActor();pr=actor.GetProperty()
        pr.SetAmbient(.40);pr.SetDiffuse(.66);pr.SetSpecular(.10)
        pr.SetInterpolationToPhong()
        if actor.GetTexture():actor.GetTexture().InterpolateOn()
    scene.AutomaticLightCreationOff()
    for point,color,power in [((8,9,9),(1,.98,.95),1.0),((-6,3,-8),(.65,.83,1),.63),((-8,7,8),(.82,.90,1),.62)]:
        light=vtk.vtkLight();light.SetLightTypeToSceneLight();light.SetPosition(*point)
        light.SetFocalPoint(0,0,0);light.SetColor(*color);light.SetIntensity(power);scene.AddLight(light)
    cam=vtk.vtkCamera();cam.SetPosition(*camera);cam.SetFocalPoint(0,0,0)
    cam.SetViewUp(0,1,0);cam.SetViewAngle(35);scene.SetActiveCamera(cam)
    scene.ResetCameraClippingRange();window.Render()
    bitmap=vtk.vtkWindowToImageFilter();bitmap.SetInput(window)
    bitmap.SetInputBufferTypeToRGBA();bitmap.ReadFrontBufferOff();bitmap.Update()
    writer=vtk.vtkPNGWriter();writer.SetInputConnection(bitmap.GetOutputPort());writer.SetFileName(str(out));writer.Write()
    print('rendered',out)

positions=[((5.4,3.0,8.7),'01-Window-Research','RECESSED OBSERVATION WINDOWS'),
           ((8.7,3.6,0.6),'02-Instrument-Bays','SCIENCE EQUIPMENT + RADIATORS'),
           ((-5.8,7.2,-5.2),'03-Bulkheads','FLUSH 2.5 M STACK INTERFACE')]
for xyz,slug,label in positions:view(xyz,OUT/f'RW-LAB-250-{slug}.png')
canvas=Image.new('RGB',(2280,890),(7,13,24));d=ImageDraw.Draw(canvas)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
tit=ImageFont.truetype(bold,50);small=ImageFont.truetype(font,24);cap=ImageFont.truetype(bold,21)
d.text((54,25),'RW-LAB-250  |  ORBITAL SCIENCE LABORATORY',font=tit,fill=(239,242,245))
d.text((58,88),'RoosterWorks Station Modules  •  v0.3.0 test prototype  •  generated OBJ mesh / actual source geometry',font=small,fill=(156,182,205))
for j,(_,slug,label) in enumerate(positions):
    x=15+j*752;y=140;w=742;h=720
    p=Image.open(OUT/f'RW-LAB-250-{slug}.png').convert('RGB').resize((w,h),Image.Resampling.LANCZOS)
    canvas.paste(p,(x,y))
    d.rectangle((x+10,y+9,x+w-10,y+54),fill=(14,25,42))
    d.text((x+26,y+20),label,font=cap,fill=(238,241,242))
    d.rounded_rectangle((x,y,x+w,y+h),radius=12,outline=(48,73,98),width=2)
canvas.save(OUT/'RW-LAB-250-v0.3.0-Review-Render.png',optimize=True)
print('Generated lab review sheet')
