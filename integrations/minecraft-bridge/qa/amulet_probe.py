from __future__ import annotations
import argparse, shutil, tempfile
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(description='Non-destructive Amulet world load/save compatibility probe')
    ap.add_argument('world')
    args=ap.parse_args()
    try:
        import amulet
    except ImportError as e:
        raise SystemExit('amulet-core is not installed. Validated target for this probe: amulet-core==1.9.49 on Python >=3.11.') from e

    src=Path(args.world).resolve()
    if not src.is_dir(): raise SystemExit('Probe expects an extracted Minecraft world directory.')
    with tempfile.TemporaryDirectory(prefix='acq_amulet_probe_') as td:
        copy=Path(td)/src.name
        shutil.copytree(src,copy)
        level=amulet.load_level(str(copy))
        try:
            print('dimensions:', list(level.dimensions))
            level.save()
        finally:
            level.close()
        level2=amulet.load_level(str(copy))
        try:
            print('reopen: ok')
        finally:
            level2.close()

if __name__=='__main__': main()
