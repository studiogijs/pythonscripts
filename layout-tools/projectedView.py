import Rhino
import scriptcontext as sc
import rhinoscriptsyntax as rs
from System.Drawing import Color


def createProjectedDetail():
    """
    This script will create a projected view from a selected detail
    front/back from top view
    left/right from front view
    back from right or left view
    
    known bugs: creating left or right views from top won't work correctly
    projected view is now a parallel view but isn't converted to a named view. Activating the detail and 'panning' will result in rotation of the view
    version 0.2
    new in version 0.2: locked details should now work better
    www.studiogijs.nl
    """

    def OnDynamicDraw(sender, e):

        vec = e.CurrentPoint-basept
        translate = vec
        xf = Rhino.Geometry.Transform.Translation(translate)
        plane = Rhino.Geometry.Plane(ptLL, Rhino.Geometry.Plane.WorldXY.ZAxis)
        sizeX = ptLR.X-ptLL.X #width of selected detail
        sizeY = ptUR.Y-ptLR.Y #height of selected detail
        newobj = Rhino.Geometry.Rectangle3d(plane,sizeX,sizeY)
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
    detailview = rs.GetObject("select detail for projected view",32768, preselect=True)
    if not detailview:
        return
    
    
    detail = rs.coercerhinoobject(detailview)
    if not detail.DetailGeometry.IsParallelProjection:
        return
    #get lower left and lower right and upper right points of selected detail view
    ptLL = Rhino.Geometry.Point3d(0,0,0)
    ptLR = Rhino.Geometry.Point3d(0,0,0)
    ptUR = Rhino.Geometry.Point3d(0,0,0)
    
    ptLL = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Min
    
    ptLR.X = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Max.X
    ptLR.Y = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Min.Y
    
    ptUR = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Max
    
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

    newdetail = rs.CopyObject(detailview, vectY)
    d = rs.coercerhinoobject(newdetail)
    
    sc.doc.Views.ActiveView.SetActiveDetail(newdetail)
    
    d.DetailGeometry.IsProjectionLocked = False
    d.CommitChanges()
    if abs(vect.X)>abs(vect.Y): #make horizontal view
        if vect.X<0:
            
            rs.RotateView(direction = 0,angle = 90)#rotate left
        else:
            
            rs.RotateView(direction = 1,angle = 90)#rotate right
        
    else:
        if vect.Y<0:
            
            rs.RotateView(direction = 3,angle = 90)#rotate down
        else:
            
            rs.RotateView(direction = 2,angle = 90)#rotate up
    d.DetailGeometry.IsProjectionLocked = True
    d.CommitChanges()
    sc.doc.Views.ActiveView.SetPageAsActive()
    sc.doc.Views.Redraw()


if __name__=="__main__":
    createProjectedDetail()
    