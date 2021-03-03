import Rhino
import rhinoscriptsyntax as rs
import math
import System

def guessHorizontalShift():
    
    """
    This script will correct the horizontal distortion and set it in the V-Ray Camera.
    It levels the camera for this correction to work well and resets
    lens shift (vertical shift) to 0
    Works with V-Ray 5.1
        
    version 0.2
        
    www.studiogijs.nl
    """
    viewport =  Rhino.RhinoDoc.ActiveDoc.Views.ActiveView.ActiveViewport
    if viewport.IsParallelProjection:
        print "Stupid, you should select a perspective view"
        return
    view =  Rhino.RhinoDoc.ActiveDoc.Views.ActiveView.ActiveViewport
    #set camera location to target height
    pt = view.CameraLocation
    pt[2] = view.CameraTarget.Z
    dir = rs.VectorSubtract(view.CameraTarget, pt)
    view.SetCameraLocation(pt, False)
    view.SetCameraDirection(dir, False)
    
    
    #calculate camera direction angle relative to WorldXY plane
    cam = view.CameraZ
    vec = Rhino.Geometry.Vector3d(1,0,0)
    plane = Rhino.Geometry.Plane.WorldXY
    angle = Rhino.Geometry.Vector3d.VectorAngle(cam, vec, plane)
    
    #calculate the correction factor
    for i in range(3):
        if angle>math.pi/2:
            angle-=math.pi/2
        else:
            break
    
    if 0 <= angle < math.pi/4:
        factor = math.sin(angle)
        
    if math.pi/4 <= angle < math.pi/2:
        factor = -math.cos(angle)
        
    
    rv = rs.GetPlugInObject("V-Ray for Rhino").Scene().Plugin("/CameraPhysical")
    rv.Param("horizontal_shift").Value = factor
    rv.Param("lens_shift").Value = 0
    rs.Redraw()
guessHorizontalShift()