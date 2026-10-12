from grid_connector_layout_v250 import *
def test_grid_and_intake():
    assert square_position(2,-1)==(3.048,-1.524,0.)
    assert len({cardinal_rotation(i) for i in range(4)})==4
    assert abs(radial_position(3,0,12)[0]-radial_position(3,12%12,12)[0])<1e-12
    required={(i,j) for i in range(3) for j in range(3)}
    assert missing_cells(required,required-{(1,1)})==[(1,1)]
    assert structural_intake(False,False,True)=="UNVERIFIED_MISSING_CONNECTORS"
    return {"passed":5,"geometry_authored":False}
if __name__=="__main__":print(test_grid_and_intake())
