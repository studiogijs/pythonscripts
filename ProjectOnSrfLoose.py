"""
This script does what the name says: it allows you to loosly
project a curve on a surface. This means the projected curve has the same
structure and degree and same amount of control points as the original curve.

***********************************
* script written by Gijs de Zwart *
* www.studiogijs.nl               *
* March, 2016                     *
***********************************

"""

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def ProjectOnSrfLoose():
    crv=rs.GetObject("select curve to loosely project",rs.filter.curve)
    srf=rs.GetObject("Select surface to loosely project onto", rs.filter.surface)
    if crv==None or srf==None:
        return
    degree=rs.CurveDegree(crv)
    bPeriodic=False
    pts=rs.CurvePoints(crv)
    if rs.IsCurvePeriodic(crv):
        pts=rs.CullDuplicatePoints(pts,0.01)
        bPeriodic=True

    pts_projected=[]
    curveplane=rs.CurvePlane(crv)
    projection_dir=curveplane.ZAxis

    for pt in pts:

        pp=rs.ProjectPointToSurface(pt,srf,projection_dir)
        if len(pp)>0:
            pt_projected=pp[0]
            pts_projected.append(pt_projected)
    if len(pts_projected)<=2:
        return
    if len(pts_projected)<len(pts):
        bPeriodic=False
    nc = Rhino.Geometry.NurbsCurve.Create(bPeriodic,degree,pts_projected)
    sc.doc.Objects.AddCurve(nc)
    sc.doc.Views.Redraw()

    
if __name__ == '__main__':
        ProjectOnSrfLoose()
                