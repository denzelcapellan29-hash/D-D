"""Area 8 read-only structural wall silhouette profile for Blender 5.x.

Uses world-coordinate polygon centers; metadata only. A polygon-center envelope
is not a certified contact patch. Does not create meshes or change objects.
"""
def silhouette_profile(obj, height_bands, stride=1400, axis=1):
    if obj.type != "MESH" or stride < 1:
        raise ValueError("Expected mesh object and positive sampling stride")
    rows=[]
    for low,high in height_bands:
        values=[]
        for i in range(0,len(obj.data.polygons),stride):
            point=obj.matrix_world @ obj.data.polygons[i].center
            if low <= point.z < high:
                values.append(float(point[axis]))
        values.sort()
        if not values:
            rows.append(dict(z_m=[low,high],status="UNVERIFIED_NO_SAMPLES"))
            continue
        rows.append(dict(z_m=[low,high],count=len(values),
                         minimum=values[0],maximum=values[-1],
                         p05=values[int((len(values)-1)*.05)],
                         p95=values[int((len(values)-1)*.95)],
                         status="SAMPLED_ENVELOPE_NOT_CONTACT_PATCH"))
    return dict(object=obj.name,axis=axis,stride=stride,bands=rows,
                status="DIAGNOSTIC_ONLY")

if __name__ == "__main__":
    import bpy,json
    bands=[(0,1),(1,2),(2,3),(3,4),(4,5.5)]
    print(json.dumps(silhouette_profile(bpy.data.objects["WALL_00"],bands),indent=2))
