"""Reusable read-only normal distribution screening for imported Blender assets.

This reports sampled face-normal diversity within caller-selected regions.
It NEVER defines an architectural connector or changes geometry.
"""
def normal_bins(obj, predicate, stride=900, bin_size=0.2):
    if obj.type != "MESH": raise ValueError("Expected mesh")
    if stride < 1 or not 0 < bin_size <= 1: raise ValueError("Invalid parameters")
    transform=obj.matrix_world.to_3x3().inverted().transposed()
    bins={}
    count=0
    for index in range(0,len(obj.data.polygons),stride):
        face=obj.data.polygons[index]
        center=obj.matrix_world@face.center
        if not predicate(center):continue
        normal=(transform@face.normal).normalized()
        key=(int(center.z),round(round(normal.y/bin_size)*bin_size,3))
        bins[key]=bins.get(key,0)+1
        count+=1
    return {'object':obj.name,'sampled':count,'bins':[
        {'height_bucket':k[0],'normal_y_bucket':k[1],'count':v}
        for k,v in sorted(bins.items(),key=lambda kv:kv[1],reverse=True)],
        'status':'NORMAL_SCREENING_NOT_INTERFACE_CERTIFICATION'}
