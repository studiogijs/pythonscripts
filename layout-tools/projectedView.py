import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
from System.Drawing import Color
from Rhino.Geometry import *


def createProjectedDetail():
    """
    This script will create a projected view from a selected detail
    front/back from top view
    left/right from front view
    back from right or left view
    
    version 0.4
    new in version 0.2:
        - locked details should now work better
    new in 0.3:
        - projected views now have their cplane set to the view, which should result in better behavior when editing the detail
        - projected views from top or bottom views to right or left are ignored with user message.
        - message when trying to add projected view from perspective
    new in 0.4:
        - new details now have their title correctly set to the actual view projection
    www.studiogijs.nl
    """

    def OnDynamicDraw(sender, e):

        vec = e.CurrentPoint-basept
        translate = vec
        xf = Transform.Translation(translate)
        plane = Plane(ptLL, Plane.WorldXY.ZAxis)
        sizeX = ptLR.X-ptLL.X #width of selected detail
        sizeY = ptUR.Y-ptLR.Y #height of selected detail
        newobj = Rectangle3d(plane,sizeX,sizeY)
        crv  = newobj.ToNurbsCurve()
        
        preview=crv.Duplicate()
        preview.Transform(xf)
        e.Display.DrawCurve(preview, Color.LightCyan, 2)


    def getPoint():
        while True:
            result = gp.Get()
            if result == Rhino.Input.GetResult.Point:
                #count=optInt.CurrentValue
                line = Rhino.Geometry.Line(basept, gp.Point())
                return line
            break

 
    #set focus page and select detail
    pageview = sc.doc.Views.ActiveView
    pageview.SetPageAsActive()
    filter = Rhino.DocObjects.ObjectType.Detail
    rc, objref = Rhino.Input.RhinoGet.GetOneObject("Select detail to rename", False, filter)
    if not objref or rc != Rhino.Commands.Result.Success: 
        return
    
    detail_obj = objref.Object()
    if not isinstance(detail_obj, Rhino.DocObjects.DetailViewObject):
        return
    viewport = detail_obj.Viewport
    
    if not viewport.IsParallelProjection:
        print "Can't make projected views from perspective views"
        return
    
    
    #get lower left and lower right and upper right points of selected detail view
    ptLL = Point3d(0,0,0)
    ptLR = Point3d(0,0,0)
    ptUR = Point3d(0,0,0)
    
    ptLL = detail_obj.Geometry.GetBoundingBox(Plane.WorldXY).Min
    
    ptLR.X = detail_obj.Geometry.GetBoundingBox(Plane.WorldXY).Max.X
    ptLR.Y = detail_obj.Geometry.GetBoundingBox(Plane.WorldXY).Min.Y
    
    ptUR = detail_obj.Geometry.GetBoundingBox(Plane.WorldXY).Max
    
    basept = (ptLL + ptUR)/2 #center of Detail view
    
    gp=Rhino.Input.Custom.GetPoint()
    gp.SetCommandPrompt("where to add projected view")

    gp.DynamicDraw += OnDynamicDraw
    line = getPoint()
    if not line:
        return
    vect = line.To - basept
    

    if abs(vect.X)>abs(vect.Y): #add view to left or right of selected detail
        if vect.X<0: #add view left
            vectY = rs.VectorSubtract(ptLL, ptLR) # to the left
        else:
            vectY = rs.VectorSubtract(ptLR, ptLL) # to the right
    else: #add view on top or bottom of selected detail
        if vect.Y<0:  #add view down
            vectY = rs.VectorSubtract(ptLR, ptUR) # down
        else:
            vectY = rs.VectorSubtract(ptUR, ptLR) # up

    newdetail = rs.CopyObject(detail_obj, vectY)
    d = rs.coercerhinoobject(newdetail)
    
    view = sc.doc.Views.ActiveView
    view.SetActiveDetail(newdetail)
    
    d.DetailGeometry.IsProjectionLocked = False
    
    VP = 0
    newViewportName = ""
    
    if d.Viewport.CameraZ==Rhino.Geometry.Vector3d(0,0,1):
        #top view
        viewportname = "top"
        VP=1
    elif d.Viewport.CameraZ==Rhino.Geometry.Vector3d(0,-1,0):
        #front view
        viewportname = "front"
        VP=2
    elif d.Viewport.CameraZ==Rhino.Geometry.Vector3d(1,0,0):
        #right view
        viewportname = "right"
        VP=3
    elif d.Viewport.CameraZ==Rhino.Geometry.Vector3d(0,0,-1):
        #bottom view
        viewportname = "bottom"
        VP=4
    elif d.Viewport.CameraZ==Rhino.Geometry.Vector3d(-1,0,0):
        #left view
        viewportname = "left"
        VP=5
    elif d.Viewport.CameraZ==Rhino.Geometry.Vector3d(0,1,0):
        #back view
        viewportname = "back"
        VP=6
    else:
        return
    
    if abs(vect.X)>abs(vect.Y): #make horizontal view
        if VP==1 or VP==4:
            print"Can't make a correct projection of this view, try to make them from front, right, left or back views"
            rs.DeleteObject(newdetail)
            return
        if VP==2 or VP==6:
            newplane = Rhino.Geometry.Plane(Rhino.Geometry.Point3d.Origin, Rhino.Geometry.Plane.WorldXY.XAxis)
            rs.ViewCPlane(plane = newplane)
            if viewportname == "front":
                if vect.X<0:
                    #left view from front
                    newViewportName = "Left"
                else:
                    newViewportName = "Right"
            
            if viewportname == "back":
                if vect.X<0:
                    #left view from back
                    newViewportName = "Right"
                else:
                    newViewportName = "Left"
            
        elif VP==3 or VP==5:
            newplane = Rhino.Geometry.Plane(Rhino.Geometry.Point3d.Origin, Rhino.Geometry.Plane.WorldXY.YAxis)
            rs.ViewCPlane(plane = newplane)
            if viewportname == "left":
                if vect.X<0:
                    #left view from left
                    newViewportName = "Back"
                else:
                    newViewportName = "Front"
            if viewportname == "right":
                if vect.X<0:
                    #left view from right
                    newViewportName = "Front"
                else:
                    newViewportName = "Back"
    
        if vect.X<0:
            
            rs.RotateView(direction = 0,angle = 90)#rotate left
        else:
            
            rs.RotateView(direction = 1,angle = 90)#rotate right
        
    else:
        if VP==1 or VP==4:
            newplane = Rhino.Geometry.Plane(Rhino.Geometry.Point3d.Origin, Rhino.Geometry.Plane.WorldXY.YAxis)
            rs.ViewCPlane(plane = newplane)
            if viewportname == "top":
                if vect.Y<0:
                    #front view from top
                    newViewportName = "Front"
                else:
                    newViewportName = "Back"
            if viewportname == "bottom":
                if vect.Y<0:
                    #back view from bottom
                    newViewportName = "Back"
                else:
                    newViewportName = "Front"
        elif VP==2 or VP==3 or VP==5 or VP==6:
            newplane = Rhino.Geometry.Plane(Rhino.Geometry.Point3d.Origin, Rhino.Geometry.Plane.WorldXY.ZAxis)
            rs.ViewCPlane(plane = newplane)
            if vect.Y<0:
                #bottom view from front, right, left or back
                newViewportName = "Bottom"
            else:
                newViewportName = "Top"
        if vect.Y<0:
            rs.RotateView(direction = 3,angle = 90)#rotate down
        else:#Y>0
            rs.RotateView(direction = 2,angle = 90)#rotate up
    #d.DetailGeometry.IsProjectionLocked = True
    viewport = d.Viewport
    title = viewport.Name
    viewport.Name = newViewportName
    d.CommitViewportChanges()
    sc.doc.Views.ActiveView.SetPageAsActive()
    sc.doc.Views.Redraw()


if __name__=="__main__":
    createProjectedDetail()
    