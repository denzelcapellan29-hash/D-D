"""Read-only reusable polygon-face contact candidates for imported Blender assets.

Does not modify Blender geometry. Nearest face-center distance is not proof
of watertight mating, collision-free placement, or structural support.
"""
def sample_faces(obj, predicate, stride=700):
    if obj.type != "MESH" or stride < 1:
        raise ValueError("Mesh and positive stride required")
    normals=obj.matrix_world.to_3x3().inverted().transposed()
    items=[]
    for i in range(0,len(obj.data.polygons),stride):
        f=obj.data.polygons[i]
        center=obj.matrix_world@f.center
        if predicate(center):
            items.append((center,(normals@f.normal).normalized()))
    return items

def compare(a,b,filter_a,filter_b,bands,stride=700,max_gap=.2,opposing_dot=-.7):
    left=sample_faces(a,filter_a,stride)
    right=sample_faces(b,filter_b,stride)
    rows=[]
    for low,high in bands:
        x=[v for v in left if low<=v[0].z<high]
        y=[v for v in right if low<=v[0].z<high]
        if not x or not y:
            rows.append(dict(height=[low,high],status="UNVERIFIED"));continue
        gaps=[]
        for p,n in x:
            q,m=min(y,key=lambda v:(p-v[0]).length_squared)
            gaps.append(((p-q).length,n.dot(m)))
        gaps.sort()
        rows.append(dict(height=[low,high],samples=[len(x),len(y)],
            median=sorted(d for d,n in gaps)[len(gaps)//2],
            near=sum(d<max_gap for d,n in gaps),
            near_opposed=sum(d<max_gap and n<opposing_dot for d,n in gaps),
            status="CANDIDATE_ONLY"))
    return dict(pair=[a.name,b.name],bands=rows,status="NOT_CERTIFIED_CONTACT")
