"""Pure connectivity fixtures for connected_face_patches.py."""
from connected_face_patches import connected_face_components

def run():
    square={0:(0,1,2),1:(2,1,3),2:(9,10,11)}
    groups=connected_face_components(square)
    assert groups==[[0,1],[2]],groups
    # Sharing only a vertex must not connect a face.
    only_vertex=connected_face_components({0:(0,1,2),1:(2,3,4)})
    assert only_vertex==[[0],[1]]
    # Non-manifold edge fails safely.
    try:
        connected_face_components({0:(0,1,2),1:(1,0,3),2:(0,1,4)})
    except ValueError: pass
    else: raise AssertionError("Non-manifold candidate edge not rejected")
    return {"tests_passed":3,"status":"SYNTHETIC_ONLY"}
if __name__=="__main__":print(run())
