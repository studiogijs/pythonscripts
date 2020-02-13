import Rhino
import math
import scriptcontext as sc
import rhinoscriptsyntax as rs



def reflectLight():
    
    """
    
    This script will place a (pre)selected light on a surface or polysurface by reflection
    After the script has run, it will select the modified light, so you can quickly repeat
    the placement with this light
    script by Gijs de Zwart
    www.studiogijs.nl
    
    """
    
    object = rs.GetObject("select light", preselect=True, filter=256)
    if not object:
        return
    light = rs.coercerhinoobject(object)
    loc=light.LightGeometry.Location
    dir=light.LightGeometry.Direction
     
    
    
    #rs.AddPoint(camLoc)
    #rs.AddPoint(camTar)
    #rs.AddLine([0,0,0],camDir)
    
    srf = rs.GetObject("select surface to reflect light on", filter=8, subobjects=True)
    #rs.GetObjects(
    if not srf:
        return
    pt = rs.GetPointOnSurface(srf)
    if not pt:
        return
    #if not sc.doc.Views.ActiveView.ActiveViewport.IsPerspectiveProjection:
    #    print "this script needs a perspective view to start"
    #    return
    camLoc = sc.doc.Views.ActiveView.ActiveViewport.CameraLocation
    camTar = sc.doc.Views.ActiveView.ActiveViewport.CameraTarget
    camDir = sc.doc.Views.ActiveView.ActiveViewport.CameraDirection
    pt_srf = rs.SurfaceClosestPoint(srf, pt)
    if not pt_srf:
        print "could not find surface point"
        return
    normal = rs.SurfaceNormal(srf, pt_srf)
    if not normal:
        print "could not calculate surface normal"
        return
    plane = Rhino.Geometry.Plane(pt, normal, -camDir)
    #sc.doc.Views.ActiveView.ActiveViewport.SetConstructionPlane(plane)
    #line = Rhino.Geometry.Line(camLoc, pt)
    #trans = Rhino.Geometry.Transform(angleRadians,rotationAxis, rotationCenter)
    trans = Rhino.Geometry.Transform.Rotation(math.pi, normal, pt)
    #rs.RotateObject(line, pt, 180, plane.XAxis, copy=True)
    
    #line.Transform(trans)
    camLoc.Transform(trans)
    
    
    newdir = rs.VectorCreate(pt, camLoc)
    newdir.Unitize()
    newplane = rs.PlaneFromNormal(camLoc, newdir)
    if light.LightGeometry.IsRectangularLight:
        
        lightX=light.LightGeometry.Width
        lightWidth = lightX.Length
        lightY=light.LightGeometry.Length
        lightHeight = lightY.Length
        lightO=light.LightGeometry.Location
        
       
        lightX = lightWidth * newplane.XAxis
        lightY = lightHeight * newplane.YAxis
        light.LightGeometry.Width = lightX
        light.LightGeometry.Length = lightY
        
        camLoc-=lightX/2
        camLoc-=lightY/2
        light.LightGeometry.Location = camLoc
        
        #mid = Rhino.Geometry.Vector3d(lightWidth/2, lightHeight/2, 0)
        #trans = Rhino.Geometry.Transform.ChangeBasis(Rhino.Geometry.Plane.WorldXY, lightPlane)
        #mid.Transform(trans)
        #light.LightGeometry.Location -=mid
    if light.LightGeometry.IsSpotLight:
        light.LightGeometry.Location = camLoc
        newdir*= rs.VectorLength(dir)
    light.LightGeometry.Direction = newdir
    
    #sc.doc.Objects.AddLine(line)
    
    sc.doc.Lights.Modify(object, light.LightGeometry)
    rs.SelectObject(object)
    
reflectLight()