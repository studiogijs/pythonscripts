import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def align_dims():
    if not sc.doc.Views.ActiveView.ActiveViewport.CameraZ == Rhino.Geometry.Plane.WorldXY.ZAxis:
        print "this works only in top view (world XY)"
        return

    """
    align vertical dimensions horizontally or horizontal dimensions vertically
    version 1.0
    www.studiogijs.nl
    """

    dims = rs.GetObjects("select dims to align", preselect = True, filter = 512)
    if not dims:
        return
    p_ref = rs.GetPoint("set basepoint for the dimensions", in_plane = True)
    if not p_ref:
        return
    p_ref = rs.coerce3dpoint(p_ref)

    dims = [rs.coercerhinoobject(dim) for dim in dims]
    for dim in dims:

        vertical=False
        horizontal=False
        rc, e1, e2, a1, a2, dp, tp = dim.Geometry.Get3dPoints()
        if not rc:
            return
        #check arrow endpoints to see if dim is vertical or horizontal
        if a1.Y == a2.Y: horizontal=True
        if a1.X == a2.X: vertical=True

        if not (horizontal or vertical): continue #next dimension

        #make sure all points are set relative to e1
        #for SetLocations method we need positions of dimension
        #extension lines and text position
        tp-=e1
        p_r=p_ref-e1
        e2-=e1
        if horizontal:
            #make 2dpoints for setting the new location
            #sometimes dimension plane is inverted
            #depending on where the endpoints wer picked
            px = dim.Geometry.Plane.XAxis.X #plane x-axis is (1,0,0) or (-1,0,0)
            py = dim.Geometry.Plane.YAxis.Y #plane y-axis is (0,1,0) or (0,-1,0)
            dp_new = Rhino.Geometry.Point2d(tp.X*px, p_r.Y*py)
            e1_new = Rhino.Geometry.Point2d(0, 0)
            e2_new = Rhino.Geometry.Point2d(e2.X*px, e2.Y*py)
        elif vertical:
            #make 2dpoints for setting the new location
            #notice that vertical dimensions have their plane rotated 90 degrees
            #sometimes dimension plane is inverted 
            px = dim.Geometry.Plane.XAxis.Y #plane x-axis is (0,-1,0) or (0,1,0)
            py = dim.Geometry.Plane.YAxis.X #plane y-axis is (1,0,0) or (-1,0,0)
            dp_new = Rhino.Geometry.Point2d(tp.Y*px, p_r.X*py)
            e1_new = Rhino.Geometry.Point2d(0, 0)
            e2_new = Rhino.Geometry.Point2d(e2.Y*px, e2.X*py)
        #perform the move
        dim.Geometry.SetLocations(e1_new,e2_new,dp_new)
        dim.CommitChanges()
if __name__ == '__main__':
    align_dims()
