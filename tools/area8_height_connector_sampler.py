"""Read-only Blender wall-interface diagnostic, not physical contact certification."""
def inspect(a,b,bands,step=700):
    def points(o):
        inv=o.matrix_world.to_3x3().inverted().transposed()
        for i in range(0,len(o.data.polygons),step):
            f=o.data.polygons[i]
            yield o.matrix_world@f.center,(inv@f.normal).normalized()
    A=[x for x in points(a) if x[0].y>1.65]
    B=[x for x in points(b) if x[0].y<4.15]
    rows=[]
    for lo,hi in bands:
        left=[x for x in A if lo<=x[0].z<hi]
        right=[x for x in B if lo<=x[0].z<hi]
        if not left or not right:rows.append({'band':[lo,hi],'status':'UNVERIFIED'});continue
        near=[]
        for p,n in left:
            q,m=min(right,key=lambda x:(p-x[0]).length_squared)
            near.append(((p-q).length,n.dot(m)))
        near.sort(key=lambda x:x[0])
        rows.append({'band':[lo,hi],'count':[len(left),len(right)],
          'median_m':near[len(near)//2][0],
          'near_20cm':sum(d<.2 for d,n in near),
          'near_opposed':sum(d<.2 and n<-.7 for d,n in near),
          'status':'CANDIDATE_ONLY'})
    return {'pair':[a.name,b.name],'bands':rows,
            'status':'NOT_VALIDATED_CONTACT'}
