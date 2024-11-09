import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
from System.Drawing import Color
from Rhino.Geometry import Point3d, Vector3d, Plane, Transform, Rectangle3d
from math import pi as pi



def create_projected_detail():
    """
    This script will create a projected view from a selected detail
    front/back from top view
    left/right from front view
    back from right or left view
    
    version 0.7
    
    new in 0.2:
        - locked details should now work better
    new in 0.3:
        - projected views now have their cplane set to the view, which should result in better behavior when editing the detail
        - projected views from top or bottom views to right or left are ignored with user message.
        - message when trying to add projected view from perspective
    new in 0.4:
        - new details now have their title correctly set to the actual view projection
    new in 0.5:
        - new detail preview now snaps to the selected detail, to make it more clear where it ends
        - temporarily disable osnaps during operation
    new in 0.6:
        - fixed a bug that prevented the projection to be altered when the selected detail was locked
    new in 0.7
        -cleaned up code, bug fixes
        
    www.studiogijs.nl
    """
    def restore_osnap():
        #restore osnapmode
        Rhino.ApplicationSettings.ModelAidSettings.Osnap = osnap
        
    def rotate_viewport(vect):
        angle = pi/2
        if Rhino.ApplicationSettings.ViewSettings.RotateReverseKeyboard: angle = -angle
        if abs(vect.X)>abs(vect.Y): #make horizontal view
            if VP==1 or VP==4:
                print ("Can't make a correct projection of this view on left or right")
                rs.DeleteObject(newdetail)
                restore_osnap()
                return
                pass
            if VP==2 or VP==6:
                newplane = Rhino.Geometry.Plane(Rhino.Geometry.Point3d.Origin, Rhino.Geometry.Plane.WorldXY.XAxis)
                view.ActiveViewport.SetConstructionPlane(newplane)
                if viewportname == "front":
                    if vect.X<0:
                        #left view from front
                        new_viewport_name = "Left"
                    else:
                        new_viewport_name = "Right"
                
                if viewportname == "back":
                    if vect.X<0:
                        #left view from back
                        new_viewport_name = "Right"
                    else:
                        new_viewport_name = "Left"
                
            elif VP==3 or VP==5:
                newplane = Rhino.Geometry.Plane(Rhino.Geometry.Point3d.Origin, Rhino.Geometry.Plane.WorldXY.YAxis)
                view.ActiveViewport.SetConstructionPlane(newplane)
                if viewportname == "left":
                    if vect.X<0:
                        #left view from left
                        new_viewport_name = "Back"
                    else:
                        new_viewport_name = "Front"
                if viewportname == "right":
                    if vect.X<0:
                        #left view from right
                        new_viewport_name = "Front"
                    else:
                        new_viewport_name = "Back"
        
            if vect.X<0:
                view.ActiveViewport.KeyboardRotate(True,angle)#rotate left
            else:
                view.ActiveViewport.KeyboardRotate(True,-angle)#rotate right
            
        else:
            if VP==1 or VP==4:
                newplane = Rhino.Geometry.Plane(Rhino.Geometry.Point3d.Origin, Rhino.Geometry.Plane.WorldXY.YAxis)
                view.ActiveViewport.SetConstructionPlane(newplane)
                if viewportname == "top":
                    if vect.Y<0:
                        #front view from top
                        new_viewport_name = "Front"
                    else:
                        new_viewport_name = "Back"
                if viewportname == "bottom":
                    if vect.Y<0:
                        #back view from bottom
                        new_viewport_name = "Back"
                    else:
                        new_viewport_name = "Front"
            elif VP==2 or VP==3 or VP==5 or VP==6:
                newplane = Rhino.Geometry.Plane(Rhino.Geometry.Point3d.Origin, Rhino.Geometry.Plane.WorldXY.ZAxis)
                view.ActiveViewport.SetConstructionPlane(newplane)
                if vect.Y<0:
                    #bottom view from front, right, left or back
                    new_viewport_name = "Bottom"
                else:
                    new_viewport_name = "Top"
            if vect.Y<0:
                view.ActiveViewport.KeyboardRotate(False,angle)#rotate down
            else:#Y>0
                view.ActiveViewport.KeyboardRotate(False,-angle)#rotate up
            return new_viewport_name

    def OnDynamicDraw(sender, e):
        
        
        rot=""
        plane = Plane(ptLL, Plane.WorldXY.ZAxis)
        sizeX = ptLR.X-ptLL.X #width of selected detail
        sizeY = ptUR.Y-ptLR.Y #height of selected detail
        vec = e.CurrentPoint-basept
        if abs(vec.X)>abs(vec.Y):
            if vec.X>0:
                translate = Vector3d(sizeX,0,0)
                if rot!="right":
                    rot="right"
            else:
                translate = Vector3d(-sizeX,0,0)
                if rot!="left":
                    rot="left"
        elif abs(vec.Y)>abs(vec.X):
            if vec.Y>0:
                translate = Vector3d(0,sizeY,0,)
                if rot!="up":
                    rot="up"
            else:
                translate = Vector3d(0,-sizeY,0)
                if rot!="down":
                    rot="down"
    
        else:
            translate = vec
        xf = Transform.Translation(translate)
        newobj = Rectangle3d(plane,sizeX,sizeY)
        crv  = newobj.ToNurbsCurve()
        preview=crv.Duplicate()
        preview.Transform(xf)
        e.Display.DrawCurve(preview, Color.LightCyan, 2)


    def get_point():
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
    rc, objref = Rhino.Input.RhinoGet.GetOneObject("Select detail to create projected drawing of", False, filter)
    if not objref or rc != Rhino.Commands.Result.Success: 
        return
    detail_obj = objref.Object()
    if not isinstance(detail_obj, Rhino.DocObjects.DetailViewObject):
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
    
    #temporarily disable osnaps if enabled
    osnap = Rhino.ApplicationSettings.ModelAidSettings.Osnap
    Rhino.ApplicationSettings.ModelAidSettings.Osnap = False
    line = get_point()
    if not line:
        restore_osnap()
        return
    vect = line.To - basept

    #determine which side the new detail should go
    if abs(vect.X)>abs(vect.Y): #add view to left or right of selected detail
        if vect.X<0: #add view left
            translation = rs.VectorSubtract(ptLL, ptLR) # to the left
        else:
            translation = rs.VectorSubtract(ptLR, ptLL) # to the right
    else: #add view on top or bottom of selected detail
        if vect.Y<0:  #add view down
            translation = rs.VectorSubtract(ptLR, ptUR) # down
        else:
            translation = rs.VectorSubtract(ptUR, ptLR) # up
    
    #create new detail
    rs.EnableRedraw = False
    newdetail = rs.CopyObject(detail_obj, translation)
    d = rs.coercerhinoobject(newdetail)
    lockedstate = d.DetailGeometry.IsProjectionLocked
    d.DetailGeometry.IsProjectionLocked = False
    d.CommitViewportChanges()
    d.CommitChanges()
    
    #set new detail as active detail
    view = sc.doc.Views.ActiveView
    view.SetActiveDetail(newdetail)
    
    #determine what the current viewport projection is
    VP = 0
    new_viewport_name = ""
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
        restore_osnap()
        return
    
    #make the rotation to the viewport
    new_view_name = rotate_viewport(vect)
    viewport = d.Viewport
    title = viewport.Name
    print (viewport.Name)
    viewport.Name = new_view_name
    
    d.DetailGeometry.IsProjectionLocked = lockedstate
    print (d.CommitViewportChanges())
    #d.CommitChanges()
    sc.doc.Views.ActiveView.SetPageAsActive()
    restore_osnap()
    sc.doc.Views.Redraw()
    rs.EnableRedraw = True
if __name__=="__main__":
    create_projected_detail()
    