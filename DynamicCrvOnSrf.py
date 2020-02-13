
"""
This script allows you draw a controlpoint curve on a surface, where you can
dynamically change the amount of points and see a preview of the resulting
curve while drawing.

***********************************
* script written by Gijs de Zwart *
* www.studiogijs.nl               *
* April, 2016                     *
***********************************

"""

import Rhino
import rhinoscriptsyntax as rs
from System.Drawing import Color
import scriptcontext as sc

def DynamicCrvOnSrf():

    def drawMyCurve(sender,e):

        points[-1]=e.CurrentPoint#change last point to CurrentPoint
        pts = [points[i] for i in xrange(len(points))]
        curve=rhsrf.InterpolatedCurveOnSurface(points,0.01)
        if curve==None:
            del pts[-1]
            curve=rhsrf.InterpolatedCurveOnSurface(pts,0.01)
        if curve:
            nc = curve.ToNurbsCurve()
            ptCount=optInt.CurrentValue
            nc=nc.Rebuild(ptCount,3, True)
            ncpoints = [nc.Points[i].Location for i in xrange(nc.Points.Count)]
            e.Display.DrawCurve(nc, Color.LightCyan,2)
            e.Display.DrawPoints(ncpoints,Rhino.Display.PointStyle.Simple,5,Color.Cyan)
            e.Display.DrawPoints(points,Rhino.Display.PointStyle.X,1,Color.Blue)

    def getPoint():
        if points!=[] and len(points)==4:
            gp.AddOption("Close")
        while True:
            result = gp.Get()
            if result == Rhino.Input.GetResult.Point:
                gp.AcceptUndo(True)
                gp.SetCommandPrompt("Next point")
                pt=gp.Point()
                newpoint=rs.AddPoint(pt)
                snapPoints.append(newpoint)
                #append first picked point
                if points==[]:
                    points.append(pt)
                    gp.DynamicDraw+=drawMyCurve
                #check if next picked point is same as previous
                if len(points)>1:
                    a=round(points[-1].X,2)
                    b=round(points[-2].X,2)
                    if a==b:
                        del points[-1]
                #add empty point to list
                #will get assigned in drawMyCurve()
                points.append(Rhino.Geometry.Point3d)

                #recursion: getpoint calling itself if a point has been picked:
                getPoint()
            elif result == Rhino.Input.GetResult.Option:
                #go back to point selection mode
                if gp.OptionIndex()==1:
                    getPoint()
                elif gp.OptionIndex()==2:
                    #close the curve
                    del points[-1]
                    ptCount=optInt.CurrentValue
                    pt=points[0]
                    #check if the last point is already 'closing' the curve
                    a=round(points[-1].X,2)
                    b=round(points[0].X,2)
                    if a==b:
                        del points[-1]
                    points.append(pt)
                    rs.DeleteObjects(snapPoints)
                    newcrv=rs.AddInterpCrvOnSrf(srf, points)
                    rs.RebuildCurve(newcrv,3,ptCount)
                    sc.doc.Views.Redraw()

            elif result == Rhino.Input.GetResult.Undo:
                if len(points)>1:
                    del points[-2]
                    rs.DeleteObject(snapPoints[-1])
                    del snapPoints[-1]
                if len(points)<=1:
                    gp.AcceptUndo(False)
                getPoint()
            #pressing spacebar, enter
            elif result == Rhino.Input.GetResult.Nothing and len(points)>2:#2 picked points +1 temporary point
                #remove last added preview point
                del points[-1]
                ptCount=optInt.CurrentValue
                rs.DeleteObjects(snapPoints)
                newcrv=rs.AddInterpCrvOnSrf(srf, points)
                rs.RebuildCurve(newcrv,3,ptCount)
                sc.doc.Views.Redraw()
            #pressing esc
            else:
                rs.DeleteObjects(snapPoints)
            break

    srf=rs.GetObject("Select surface to draw curve on", rs.filter.surface)
    if srf==None:
        return
    rhsrf=rs.coercesurface(srf)
    gp=Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt("Start of Curve")
    gp.Constrain(rhsrf, False)
    gp.AcceptNothing(True)
    Rhino.ApplicationSettings.SmartTrackSettings.UseSmartTrack=False
    points=[]
    snapPoints=[]
    optInt=Rhino.Input.Custom.OptionInteger(20,4,100)
    gp.AddOptionInteger("ptCount",optInt)
    getPoint()

if( __name__ == "__main__" ):
    DynamicCrvOnSrf()