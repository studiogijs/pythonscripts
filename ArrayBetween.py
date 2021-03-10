"""
This script allows you array curves, surfaces and polysurfaces, from object
boundingbox center or corners to a picked point, where the new objects will get
distributed between center or corner and picked point. You will see a dynamic preview
and can change the amount while the preview updates.

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


def ArrayBetween():

    def OnDynamicDraw(sender, e):
        i=optBasePoint[0]
        pts=[]
        count=optInt.CurrentValue
        if i==0:#center
            basept.X = center.X
            basept.Y = center.Y
        if i==1:#lowerleft
            basept.X = center.X-width/2
            basept.Y = center.Y-depth/2
        if i==2:#upperleft
            basept.X = center.X-width/2
            basept.Y = center.Y+depth/2
        if i==3:#lowerright
            basept.X = center.X+width/2
            basept.Y = center.Y-depth/2
        if i==4:#upperright
            basept.X = center.X+width/2
            basept.Y = center.Y+depth/2
        vec = e.CurrentPoint - basept


        gp.SetBasePoint(basept, False)
        line = Rhino.Geometry.Line(basept, e.CurrentPoint)
        curve=line.ToNurbsCurve()
        params=curve.DivideByCount(count-1,True)
        for param in params:
            pts.append(line.PointAt(param))

        length = vec.Length
        dist=length/(count-1)
        vec.Unitize()

        for i in range(1,count):
            translate = vec * i * dist
            xf = Rhino.Geometry.Transform.Translation(translate)
            newobj=obj.Duplicate()
            newobj.Transform(xf)
            if obj.ObjectType==Rhino.DocObjects.ObjectType.Curve:
                e.Display.DrawCurve(newobj, Color.LightCyan, 2)
            if obj.ObjectType==Rhino.DocObjects.ObjectType.Brep:
                e.Display.DrawBrepWires(newobj, Color.LightCyan)
        e.Display.DrawLine(line, Color.Blue, 2)


    def getPoint():
        while True:
            result = gp.Get()
            if result == Rhino.Input.GetResult.Point:
                count=optInt.CurrentValue
                line = Rhino.Geometry.Line(center, gp.Point())
                curve=line.ToNurbsCurve()
                params=curve.DivideByCount(count-1,True)
                pts=[]
                for param in params:
                    pts.append(line.PointAt(param))
                vec = gp.Point() - basept
                length = vec.Length
                dist=length/(count-1)
                vec.Unitize()

                for i in range(1,count):
                    translate = vec * i * dist
                    xf = Rhino.Geometry.Transform.Translation(translate)
                    newobj=obj.Duplicate()
                    newobj.Transform(xf)
                    if obj.ObjectType==Rhino.DocObjects.ObjectType.Curve:
                        sc.doc.Objects.AddCurve(newobj)
                    if obj.ObjectType==Rhino.DocObjects.ObjectType.Brep:
                        sc.doc.Objects.AddBrep(newobj)
                sc.doc.Views.Redraw()
            elif result == Rhino.Input.GetResult.Option:
                optionindex = gp.Option().CurrentListOptionIndex
                optBasePoint[0]=optionindex

                getPoint()
            break


    docobj = rs.GetObject("select object to array", 28)
    if not docobj: return
    if rs.IsCurve(docobj):
        obj=rs.coercecurve(docobj)
    if rs.IsBrep(docobj):
        obj=rs.coercebrep(docobj)
    if not obj:
        return

    plane=Rhino.Geometry.Plane.WorldXY
    bb=obj.GetBoundingBox(plane)
    if bb==None:
        print "can't calculate boundingbox"
        return
    center = bb.Center

    basept = bb.Center

    minimum = bb.Min
    maximum = bb.Max

    center.Z=minimum.Z
    width = maximum.X-minimum.X
    depth = maximum.Y-minimum.Y


    gp=Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt("point to array to / distance")
    optInt=Rhino.Input.Custom.OptionInteger(3,3,999)
    gp.AddOptionInteger("Count",optInt)
    basepoints=["center", "lower_left","upper_left","lower_right","upper_right"]
    gp.AddOptionList("basepoint", basepoints, 0)
    optBasePoint=[0]#equal to index 0 of basepoints option

    gp.DynamicDraw += OnDynamicDraw
    getPoint()
if( __name__ == "__main__" ):
    ArrayBetween()
