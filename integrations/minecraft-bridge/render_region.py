#!/usr/bin/env python3
"""
Headless renderer for Acq Minecraft Bridge /region results.

Input: bridge result JSON containing bounds, palette, runs, and order=y,z,x.
Output:
  - colored point-cloud PLY (portable 3D QA artifact)
  - optional orthographic/isometric PNG views when Pillow is installed

This renderer is intentionally independent of the Minecraft client camera.
"""

import argparse
import json
import math
from pathlib import Path

BLOCK_COLORS = {
    "minecraft:stone_bricks": (130,130,130),
    "minecraft:deepslate_bricks": (55,55,60),
    "minecraft:water": (55,110,170),
    "minecraft:dark_oak_log": (65,45,30),
    "minecraft:dirt": (115,80,55),
    "minecraft:dark_oak_planks": (75,50,32),
    "minecraft:gravel": (130,125,120),
    "minecraft:cobblestone": (110,110,108),
    "minecraft:packed_mud": (125,100,80),
    "minecraft:smooth_stone": (160,160,160),
    "minecraft:polished_andesite": (145,145,145),
    "minecraft:spruce_planks": (130,95,55),
    "minecraft:barrel": (125,85,45),
    "minecraft:chest": (160,110,45),
    "minecraft:lantern": (235,180,70),
    "minecraft:bricks": (155,80,65),
    "minecraft:light_gray_terracotta": (145,125,118),
    "minecraft:yellow_terracotta": (185,140,70),
    "minecraft:white_terracotta": (210,195,185),
    "minecraft:composter": (105,75,40),
    "minecraft:hay_block": (190,165,55),
    "minecraft:stripped_dark_oak_log": (90,70,45),
    "minecraft:stripped_spruce_log": (150,110,65),
    "minecraft:light_blue_stained_glass_pane": (120,185,205),
    "minecraft:glass": (190,220,225),
    "minecraft:red_wool": (170,50,50),
    "minecraft:white_wool": (225,225,220),
    "minecraft:iron_chain": (85,85,90),
    "minecraft:deepslate_tiles": (50,50,55),
}

def color_for(block_id):
    return BLOCK_COLORS.get(block_id, (180,0,180))

def unwrap_result(doc):
    if "result" in doc and isinstance(doc["result"], dict):
        return doc["result"]
    if "results" in doc and doc["results"]:
        return doc["results"][0].get("result", doc["results"][0])
    return doc

def expand_voxels(result):
    dims=result["dimensions"]
    dx,dy,dz=dims["x"],dims["y"],dims["z"]
    total=dx*dy*dz
    values=[0]*total
    pos=0
    for idx,count in result["runs"]:
        values[pos:pos+count]=[idx]*count
        pos+=count
    if pos != total:
        raise ValueError(f"RLE expands to {pos}, expected {total}")

    b=result["bounds"]
    palette=result["palette"]
    air=palette.index("minecraft:air") if "minecraft:air" in palette else None
    voxels=[]
    p=0
    for iy in range(dy):
        y=b["y1"]+iy
        for iz in range(dz):
            z=b["z1"]+iz
            for ix in range(dx):
                idx=values[p]
                p+=1
                if air is not None and idx == air:
                    continue
                block=palette[idx]
                voxels.append((b["x1"]+ix,y,z,block))
    return voxels

def write_ply(voxels,path):
    path=Path(path)
    with path.open("w",encoding="utf-8") as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(voxels)}\n")
        f.write("property float x\nproperty float y\nproperty float z\n")
        f.write("property uchar red\nproperty uchar green\nproperty uchar blue\n")
        f.write("end_header\n")
        for x,y,z,block in voxels:
            r,g,b=color_for(block)
            f.write(f"{x} {y} {z} {r} {g} {b}\n")

def write_png(voxels,path,yaw_deg=45,elev_deg=28,min_y=100):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return False

    pts=[v for v in voxels if v[1] >= min_y]
    if not pts:
        return False

    xs=[v[0] for v in pts]; ys=[v[1] for v in pts]; zs=[v[2] for v in pts]
    cx=(min(xs)+max(xs))/2
    cz=(min(zs)+max(zs))/2
    cy=min_y
    yaw=math.radians(yaw_deg)
    elev=math.radians(elev_deg)
    proj=[]
    for x,y,z,block in pts:
        X=x-cx; Y=y-cy; Z=z-cz
        xr=X*math.cos(yaw)-Z*math.sin(yaw)
        zr=X*math.sin(yaw)+Z*math.cos(yaw)
        sy=Y*math.cos(elev)-zr*math.sin(elev)
        depth=Y*math.sin(elev)+zr*math.cos(elev)
        proj.append((xr,sy,depth,block))

    W,H=1600,1050
    margin=60
    minx=min(p[0] for p in proj); maxx=max(p[0] for p in proj)
    miny=min(p[1] for p in proj); maxy=max(p[1] for p in proj)
    scale=min((W-2*margin)/(maxx-minx+1),(H-2*margin)/(maxy-miny+1))*0.92
    ox=W/2-(minx+maxx)/2*scale
    oy=H/2+(miny+maxy)/2*scale

    img=Image.new("RGB",(W,H),(235,238,240))
    draw=ImageDraw.Draw(img,"RGBA")
    size=max(2,int(scale*0.72))
    for sx,sy,depth,block in sorted(proj,key=lambda p:p[2]):
        r,g,b=color_for(block)
        a=80 if block=="minecraft:water" else 245
        px=int(ox+sx*scale); py=int(oy-sy*scale)
        draw.rectangle((px-size//2,py-size//2,px+size//2,py+size//2),fill=(r,g,b,a))

    img.save(path)
    return True

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--out-dir",default=".")
    ap.add_argument("--min-y",type=int,default=100)
    ap.add_argument("--views",default="45,135,225,315")
    args=ap.parse_args()

    doc=json.loads(Path(args.input).read_text(encoding="utf-8"))
    result=unwrap_result(doc)
    voxels=expand_voxels(result)
    out=Path(args.out_dir)
    out.mkdir(parents=True,exist_ok=True)
    write_ply(voxels,out/"region.ply")
    for yaw in [int(v) for v in args.views.split(",") if v.strip()]:
        write_png(voxels,out/f"region_{yaw}.png",yaw_deg=yaw,min_y=args.min_y)

if __name__=="__main__":
    main()
