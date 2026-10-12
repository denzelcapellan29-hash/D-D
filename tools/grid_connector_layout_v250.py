"""Grid + connector construction checks (nonrendered metadata only).
Use in Blender Python; never creates visible primitives or modifies GLB vertices.
"""
import math
FEET_PER_GRID=5
GRID_METERS=1.524

def square_position(i,j,level=0):
    if not all(isinstance(v,int) for v in (i,j,level)):
        raise TypeError("Grid indices must be integers")
    return (i*GRID_METERS,j*GRID_METERS,level*GRID_METERS)

def cardinal_rotation(quarter_turn):
    if not isinstance(quarter_turn,int): raise TypeError("Rotation must be integer quarter turns")
    return (quarter_turn%4)*(math.pi/2)

def radial_position(ring,sector,sector_count,radial_pitch=GRID_METERS):
    if not all(isinstance(v,int) for v in (ring,sector,sector_count)): raise TypeError("Indices must be integers")
    if ring<0 or sector_count<3 or not (0<=sector<sector_count):
        raise ValueError("Invalid radial cell")
    a=2*math.pi*sector/sector_count
    return (ring*radial_pitch*math.cos(a),ring*radial_pitch*math.sin(a),a)

def missing_cells(required,occupied,permitted_openings=()):
    required=set(required);occupied=set(occupied)
    return sorted(required-occupied-set(permitted_openings))

def structural_intake(has_connectors,measured_patch_valid,provenance_ok):
    if not provenance_ok: return "FAIL_ASSET_PROVENANCE"
    if not has_connectors: return "UNVERIFIED_MISSING_CONNECTORS"
    if not measured_patch_valid: return "UNVERIFIED_CONTACT_PATCH"
    return "ELIGIBLE_FOR_ASSEMBLY_FIXTURE_NOT_STRUCTURALLY_PASSED"
