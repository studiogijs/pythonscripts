import Rhino
import rhinoscriptsyntax as rs
def set_gumball_max():
    objs = rs.GetObjects("select objects", preselect=True, select=True)
    if not objs:
        return
    bb = rs.BoundingBox(objs)
    origin = bb[6]
    command = "GumballRelocate %f,%f,%f Enter" % (origin[0], origin[1], origin[2])
    rs.Command(command)
    command = "GumballRelocate SetScaleHandles %f %f %f Enter" % (bb[1][0]-bb[0][0], bb[3][1]-bb[0][1], bb[4][2]-bb[0][2])
    rs.Command(command)
set_gumball_max()