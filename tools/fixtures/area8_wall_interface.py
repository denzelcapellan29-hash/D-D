"""Area 8 fixture configuration for reusable_asset_interface_diagnostics.py.

This file is a caller profile; the generic code knows nothing about Area 8.
Thresholds are diagnostic screening values, not approved structural tolerances.
"""
BANDS=[(0,1),(1,2),(2,3),(3,4),(4,5.5)]
STRIDE=700
NEAR_DISTANCE_M=.2
OPPOSING_NORMAL_DOT=-.7

def run_area8_wall_fixture():
    import bpy
    from reusable_asset_interface_diagnostics import compare
    return compare(bpy.data.objects["WALL_00"],
                   bpy.data.objects["WALL_01"],
                   lambda p:p.y>1.65,lambda p:p.y<4.15,
                   BANDS,stride=STRIDE,max_gap=NEAR_DISTANCE_M,
                   opposing_dot=OPPOSING_NORMAL_DOT)
