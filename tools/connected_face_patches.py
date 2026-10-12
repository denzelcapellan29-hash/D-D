"""Topology-only connected candidate-face regions for imported Blender meshes.
No mesh creation, vertex edits, or transformations. Input face indices come from
a separate source-faithful connector candidate filter; no positional shortcuts.
"""
from collections import defaultdict, deque

def connected_face_components(face_vertex_ids):
    """Return vertex-edge-connected components of indexed candidate polygon faces.
    face_vertex_ids: {polygon_index: tuple(vertex_index,...)}.
    Only actual SHARED EDGES count, never a shared vertex alone.
    """
    edge_faces=defaultdict(list)
    for face_id,vertices in face_vertex_ids.items():
        if len(vertices)<3:raise ValueError("Polygon requires at least 3 vertices")
        for a,b in zip(vertices,vertices[1:]+vertices[:1]):
            edge_faces[tuple(sorted((a,b)))].append(face_id)
    neighbors=defaultdict(set)
    for face_ids in edge_faces.values():
        if len(face_ids)==2:
            a,b=face_ids
            neighbors[a].add(b);neighbors[b].add(a)
        elif len(face_ids)>2:
            raise ValueError("Non-manifold candidate edge: manual review required")
    unseen=set(face_vertex_ids)
    components=[]
    while unseen:
        root=min(unseen)
        queue=deque([root]);unseen.remove(root);component=[]
        while queue:
            cur=queue.popleft();component.append(cur)
            for nxt in sorted(neighbors[cur]):
                if nxt in unseen:
                    unseen.remove(nxt);queue.append(nxt)
        components.append(sorted(component))
    return sorted(components,key=lambda item:(-len(item),item[0]))

def extract_candidate_topology(mesh, selected_face_indices):
    """Read-only adapter for bpy.types.Mesh.polygons. Use bounded candidate sets."""
    chosen={}
    for i in sorted(set(selected_face_indices)):
        if i<0 or i>=len(mesh.polygons):raise IndexError(i)
        chosen[i]=tuple(mesh.polygons[i].vertices)
    return connected_face_components(chosen)
