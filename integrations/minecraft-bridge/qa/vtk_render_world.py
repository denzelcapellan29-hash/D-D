from __future__ import annotations
import argparse, json, tempfile, zipfile, shutil
from pathlib import Path
import vtk
from world_reader import WorldReader

COLORS={
'minecraft:stone_bricks':(135,135,132),'minecraft:water':(55,105,170),
'minecraft:dark_oak_log':(58,42,29),'minecraft:dark_oak_planks':(78,51,30),
'minecraft:cobblestone':(105,105,102),'minecraft:spruce_planks':(128,92,52),
'minecraft:bricks':(155,80,65),'minecraft:white_terracotta':(205,190,180),
'minecraft:light_gray_terracotta':(145,128,120),'minecraft:yellow_terracotta':(185,140,65),
'minecraft:deepslate_tiles':(48,48,54),'minecraft:glass':(180,220,230),
'minecraft:light_blue_stained_glass_pane':(120,185,205),
'minecraft:stripped_spruce_log':(145,105,62),'minecraft:stripped_dark_oak_log':(88,67,43),
'minecraft:iron_chain':(75,75,80),'minecraft:white_wool':(230,230,225),
'minecraft:red_wool':(170,50,50),'minecraft:packed_mud':(120,95,78),
'minecraft:gravel':(125,120,116),'minecraft:smooth_stone':(160,160,160),
'minecraft:polished_andesite':(145,145,145),'minecraft:barrel':(125,85,45),
'minecraft:hay_block':(190,165,55),'minecraft:composter':(105,75,40)
}
FACES=[
((-1,0,0),[(0,0,0),(0,0,1),(0,1,1),(0,1,0)]),
((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),
((0,-1,0),[(0,0,0),(1,0,0),(1,0,1),(0,0,1)]),
((0,1,0),[(0,1,0),(0,1,1),(1,1,1),(1,1,0)]),
((0,0,-1),[(0,0,0),(0,1,0),(1,1,0),(1,0,0)]),
((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)])
]

def unpack_world(path:Path):
    if path.is_dir(): return path,None
    td=Path(tempfile.mkdtemp(prefix='acq_world_'))
    with zipfile.ZipFile(path) as z: z.extractall(td)
    dirs=[p for p in td.iterdir() if p.is_dir()]
    return (dirs[0] if len(dirs)==1 else td),td

def build_surface_mesh(w,bounds):
    x1,y1,z1,x2,y2,z2=bounds
    points=vtk.vtkPoints(); polys=vtk.vtkCellArray()
    colors=vtk.vtkUnsignedCharArray(); colors.SetNumberOfComponents(3); colors.SetName('rgb')
    pmap={}; cache={}; face_count=0; block_count=0
    def get(x,y,z):
        key=(x,y,z)
        if key not in cache:
            try: cache[key]=w.block(x,y,z)
            except Exception: cache[key]='minecraft:air'
        return cache[key]
    for y in range(y1,y2+1):
      for z in range(z1,z2+1):
       for x in range(x1,x2+1):
        block=get(x,y,z)
        if block=='minecraft:air': continue
        block_count+=1; col=COLORS.get(block,(190,0,190))
        for (dx,dy,dz),verts in FACES:
            nb=get(x+dx,y+dy,z+dz)
            if nb!='minecraft:air' and not (block!='minecraft:water' and nb=='minecraft:water'): continue
            ids=vtk.vtkIdList()
            for vx,vy,vz in verts:
                pt=(float(x+vx),float(y+vy),float(z+vz)); pid=pmap.get(pt)
                if pid is None: pid=points.InsertNextPoint(*pt); pmap[pt]=pid
                ids.InsertNextId(pid)
            polys.InsertNextCell(ids); colors.InsertNextTuple3(*col); face_count+=1
    pd=vtk.vtkPolyData(); pd.SetPoints(points); pd.SetPolys(polys); pd.GetCellData().SetScalars(colors)
    return pd,block_count,face_count

def render(poly,out,camera,size=(1600,1000)):
    mapper=vtk.vtkPolyDataMapper(); mapper.SetInputData(poly); mapper.SetScalarModeToUseCellData(); mapper.ScalarVisibilityOn()
    actor=vtk.vtkActor(); actor.SetMapper(mapper)
    ren=vtk.vtkRenderer(); ren.SetBackground(0.88,0.92,0.97); ren.AddActor(actor)
    rw=vtk.vtkRenderWindow(); rw.SetOffScreenRendering(1); rw.SetSize(*size); rw.AddRenderer(ren)
    ren.ResetCamera(); cam=ren.GetActiveCamera()
    if camera=='top': cam.SetPosition(0,1,0); cam.SetViewUp(0,0,-1); ren.ResetCamera()
    else: cam.Azimuth(45); cam.Elevation(32); cam.Zoom(1.15)
    rw.Render()
    w2i=vtk.vtkWindowToImageFilter(); w2i.SetInput(rw); w2i.SetInputBufferTypeToRGB(); w2i.ReadFrontBufferOff(); w2i.Update()
    writer=vtk.vtkPNGWriter(); writer.SetFileName(str(out)); writer.SetInputConnection(w2i.GetOutputPort()); writer.Write()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('world'); ap.add_argument('--bounds',nargs=6,type=int,required=True); ap.add_argument('--out-dir',default='qa_render')
    args=ap.parse_args()
    wd,tmp=unpack_world(Path(args.world)); out=Path(args.out_dir); out.mkdir(parents=True,exist_ok=True)
    try:
        poly,blocks,faces=build_surface_mesh(WorldReader(wd),args.bounds)
        render(poly,out/'iso.png','iso'); render(poly,out/'top.png','top')
        metrics={'bounds':args.bounds,'blocks':blocks,'visible_faces':faces,'points':poly.GetNumberOfPoints()}
        (out/'metrics.json').write_text(json.dumps(metrics,indent=2)+'\n'); print(json.dumps(metrics))
    finally:
        if tmp: shutil.rmtree(tmp,ignore_errors=True)

if __name__=='__main__': main()
