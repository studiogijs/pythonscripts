"""
This script does what the name says: it allows you to offset a curve loosely.
This means the offset curve has the same structure and degree, and same amount
of control points as the original curve.
Option to offset both sides.

***********************************
* script written by Gijs de Zwart *
* www.studiogijs.nl               *
* March, 2016                     *
***********************************

"""


import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def OffsetCrvLoose():

    crv=rs.GetObject("select curve to offset loosely",rs.filter.curve, True)
    if crv==None:
        return
    if not rs.IsCurvePlanar(crv):
        print "Sorry, but that curve is not planar."
        return
    if rs.IsPolyCurve(crv):
        print "This simple script works only for single open or closed curves"
        return
    offset=rs.GetReal("offset amount",5)

    if offset==None or offset==0:
        return
    both_sides=rs.GetBoolean("Offset both sides?",["both_sides","off","on"], False)[0]
    bPeriodic=False
    #rs.EnableRedraw(False)
    pts=rs.CurvePoints(crv)
    degree=rs.CurveDegree(crv)
    if rs.IsCurvePeriodic(crv):
        pts=rs.CullDuplicatePoints(pts,0.01)
        bPeriodic=True
    offset_pts=[]
    offset_pts2=[]#if both_sides=true
    plane=rs.CurvePlane(crv)
    axis=plane.ZAxis
    for pt in pts:
        cp=rs.CurveClosestPoint(crv,pt)
        v=rs.CurveTangent(crv,cp)
        v=rs.VectorUnitize(v)
        v*=offset
        v=rs.VectorRotate(v,90,axis)
        pt_=rs.AddPoint(pt)
        #create points for offset on one side of the curve
        movedpt=rs.MoveObject(pt_,v)
        newpt=rs.coerce3dpoint(movedpt)
        offset_pts.append(newpt)
        #create points for offset on other side of the curve
        movedpt=rs.MoveObject(pt_,-2*v)
        newpt=rs.coerce3dpoint(movedpt)
        offset_pts2.append(newpt)
        rs.DeleteObject(pt_)
    nc = Rhino.Geometry.NurbsCurve.Create(bPeriodic,degree,offset_pts)
    nc2 = Rhino.Geometry.NurbsCurve.Create(bPeriodic,degree,offset_pts2)

    if not both_sides:
        if nc.GetLength(0.1)>nc2.GetLength(0.1):#get the longest curve...
            if offset>0:#...and add it to the document for positive offsets...
                sc.doc.Objects.AddCurve(nc)
            else:#...or the shortest for negative offsets.
                sc.doc.Objects.AddCurve(nc2)
        else:
            if offset>0:
                sc.doc.Objects.AddCurve(nc2)
            else:
                sc.doc.Objects.AddCurve(nc)
    else:#add both curves to the document
        sc.doc.Objects.AddCurve(nc)
        sc.doc.Objects.AddCurve(nc2)

    rs.EnableRedraw(True)
    sc.doc.Views.Redraw()
if __name__ == '__main__':
    OffsetCrvLoose()
                