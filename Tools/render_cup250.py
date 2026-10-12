"""Create true mesh + actual texture review renders (not AI concept images)."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'Source'))
import build_cup250 as c
from PIL import Image,ImageDraw,ImageFont
import vtk
from vtk.util.numpy_support import numpy_to_vtk
import numpy as np

meshes=c.geometry()
views=[('PANORAMA',(3.25,1.75,4.4)),('SERVICE SIDE',(-2.6,1.35,-4.65)),('OVERHEAD',(2.45,5.3,3.15))]
w,h=720,690
output=Image.new('RGB',(w*3,h+60),(19,27,34))
for k,(label,camera) in enumerate(views):
    ren=vtk.vtkRenderer();ren.SetBackground(.064,.095,.126);ren.SetBackground2(.105,.145,.18);ren.GradientBackgroundOn()
    for mat,mesh in meshes.items():
        if not mesh.triangles:continue
        pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(np.array(mesh.vertices,dtype=np.float32),deep=True))
        faces=vtk.vtkCellArray();faces.AllocateEstimate(len(mesh.triangles),3)
        for tri in mesh.triangles:
            faces.InsertNextCell(3)
            for i in tri:faces.InsertCellPoint(i)
        pd=vtk.vtkPolyData();pd.SetPoints(pts);pd.SetPolys(faces)
        uv=vtk.vtkFloatArray();uv.SetName('TCoords');uv.SetNumberOfComponents(2)
        for u,v in mesh.uvs:uv.InsertNextTuple2(u,v)
        pd.GetPointData().SetTCoords(uv)
        norms=vtk.vtkFloatArray();norms.SetName('Normals');norms.SetNumberOfComponents(3)
        for a,b,z in mesh.normals:norms.InsertNextTuple3(a,b,z)
        pd.GetPointData().SetNormals(norms)
        mapper=vtk.vtkPolyDataMapper();mapper.SetInputData(pd);mapper.ScalarVisibilityOff()
        actor=vtk.vtkActor();actor.SetMapper(mapper)
        reader=vtk.vtkPNGReader();reader.SetFileName(str(c.MODELS/('rwm_'+mat+'.png')));reader.Update()
        tex=vtk.vtkTexture();tex.SetInputConnection(reader.GetOutputPort());tex.InterpolateOn();tex.RepeatOn();actor.SetTexture(tex)
        prop=actor.GetProperty();prop.SetAmbient(.26);prop.SetDiffuse(.68);prop.SetSpecular(.3);prop.SetSpecularPower(28)
        if mat=='glass':prop.SetSpecular(.85);prop.SetSpecularPower(90)
        ren.AddActor(actor)
    light=vtk.vtkLight();light.SetPosition(4,6,8);light.SetFocalPoint(0,0,0);light.SetIntensity(.85);ren.AddLight(light)
    light2=vtk.vtkLight();light2.SetPosition(-5,0,-7);light2.SetFocalPoint(0,0,0);light2.SetIntensity(.5);ren.AddLight(light2)
    ren.SetAutomaticLightCreation(False)
    cam=ren.GetActiveCamera();cam.SetPosition(*camera);cam.SetFocalPoint(0,-.065,0);cam.SetViewUp(0,1,0);cam.ParallelProjectionOn();cam.SetParallelScale(1.28)
    rw=vtk.vtkRenderWindow();rw.OffScreenRenderingOn();rw.SetSize(w,h);rw.AddRenderer(ren);rw.SetMultiSamples(4);rw.Render()
    filt=vtk.vtkWindowToImageFilter();filt.SetInput(rw);filt.ReadFrontBufferOff();filt.Update()
    writer=vtk.vtkPNGWriter();writer.SetInputConnection(filt.GetOutputPort())
    path=ROOT/'Media'/f'RW-CUP-250-{k+1:02}-{label.replace(" ","-")}.png'
    writer.SetFileName(str(path));writer.Write()
    pane=Image.open(path).convert('RGB');output.paste(pane,(w*k,60))
    rw.Finalize()
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=ImageFont.truetype(fontpath,25)
d=ImageDraw.Draw(output)
for k,(label,_) in enumerate(views):
    d.text((w*k+20,15),f'RW-CUP-250   /   {label}',font=font,fill=(239,237,229))
path=ROOT/'Media/RW-CUP-250-v0.6.0-Review-Render.png'
output.save(path)
print(path)
