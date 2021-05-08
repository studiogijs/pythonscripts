import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

def align_details():
    """
    This script will align a detail to another detail on page.
    It can match top <-> front both ways
    It can match front <-> right both ways
    The detail border will remain unaffected, in other words, it will be moved too.
    version 1.3
    update 1.1: bug fixes, page refresh Rhino 7
    update 1.2: added matching left to front
    update 1.3: added matching of other orthogonal views
    
    www.studiogijs.nl
    """
    #set focus back to page
    pageview = sc.doc.Views.ActiveView
    if type(pageview) != Rhino.Display.RhinoPageView:
        print "This tool only works in layout space."
        return
    pageview.SetPageAsActive()

    child = rs.GetObject("select detail to change")
    DC = rs.coercerhinoobject(child)
    if type(DC) !=Rhino.DocObjects.DetailViewObject:
        return
        
    parent = rs.GetObject("select detail to match to")
    DP = rs.coercerhinoobject(parent)
    if type(DP) !=Rhino.DocObjects.DetailViewObject:
        return
        
    def align(DP,DC):    
        if DP.DetailGeometry.IsParallelProjection:
            scale = DP.DetailGeometry.PageToModelRatio
            tP = DP.PageToWorldTransform
        else:
            return False
        if DC.DetailGeometry.IsParallelProjection:
            sc.doc.Views.ActiveView.SetActiveDetail(DC.Id)
            
            #check if right type of viewports are being attempted to match
            if (DP.Viewport.CameraZ.Z == 1 and DC.Viewport.CameraZ.Y == -1): #match front to top
                vertical = True
            elif (DC.Viewport.CameraZ.Z == 1 and DP.Viewport.CameraZ.Y == -1): #match top to front
                vertical = True
            elif (DP.Viewport.CameraZ.Y == -1 and DC.Viewport.CameraZ.X == 1): #match right to front
                vertical = False
            elif (DC.Viewport.CameraZ.Y == -1 and DP.Viewport.CameraZ.X == 1): #match front to right
                vertical = False
            elif (DP.Viewport.CameraZ.Y == -1 and DC.Viewport.CameraZ.X == -1): #match left to front
                vertical = False
            elif (DC.Viewport.CameraZ.Y == -1 and DP.Viewport.CameraZ.X == -1): #match front to left
                vertical = False
            elif (DP.Viewport.CameraZ.X == 1 and DC.Viewport.CameraZ.Y == 1): #match back to right
                vertical = False
            elif (DP.Viewport.CameraZ.Y == 1 and DC.Viewport.CameraZ.X == 1): #match right to back
                vertical = False
            elif (DP.Viewport.CameraZ.Y == 1 and DC.Viewport.CameraZ.X == -1): #match left to back
                vertical = False
            elif (DP.Viewport.CameraZ.X == -1 and DC.Viewport.CameraZ.Y == 1): #match back to left
                vertical = False
            else:
                return False
            #now it is safe to change the scale
            DC.DetailGeometry.SetScale(1, sc.doc.ModelUnitSystem, scale, sc.doc.PageUnitSystem)
            DC.CommitChanges()
            tC = DC.PageToWorldTransform
            vh = Rhino.Geometry.Vector3d(-(tP.M03*scale - tC.M03*scale),0,0)
            vv = Rhino.Geometry.Vector3d(0, -(tP.M23*scale - tC.M23*scale),0)
            
            if vertical:
                t = Rhino.Geometry.Transform.Translation(vh)#align horizontal
            else:
                t = Rhino.Geometry.Transform.Translation(vv)#align vertical
            DC.Geometry.Transform(t)
            DC.CommitChanges()
            
        else:
            return False
        return True
            
    rc = align(DP,DC)
    if not rc:
        print "These two viewports cannot be matched"
    sc.doc.Views.ActiveView.SetPageAsActive()
    sc.doc.Views.Redraw()

align_details()            