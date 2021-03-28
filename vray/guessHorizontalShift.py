import Rhino
import rhinoscriptsyntax as rs
import math
import System

def Main(option):
    if option == 0:
        guessHorizontalShift()
    if option == 1:
        resetHorizontalShift()
    if option == 2:
        printHorizontalShift()
    else:
        return

def guessHorizontalShift():
    
    """
    This script will correct the horizontal distortion and set it in the V-Ray Camera.
    It levels the camera for this correction to work well and resets
    lens shift (vertical shift) to 0
    Works with V-Ray 5.1
        
    version 0.4
        
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
        factor = math.tan(angle)
        
    if math.pi/4 <= angle < math.pi/2:
        factor = -math.tan(math.pi/2-angle)
        
    
    rv = rs.GetPlugInObject("V-Ray for Rhino").Scene().Plugin("/CameraPhysical")
    rv.Param("horizontal_shift").Value = factor
    print "Horizontal shift factor set to %r." %factor
    rv.Param("lens_shift").Value = 0
    rs.Redraw()
    
def resetHorizontalShift():
    rv = rs.GetPlugInObject("V-Ray for Rhino").Scene().Plugin("/CameraPhysical")
    rv.Param("horizontal_shift").Value = 0

def printHorizontalShift():
    rv = rs.GetPlugInObject("V-Ray for Rhino").Scene().Plugin("/CameraPhysical")
    print rv.Param("horizontal_shift").Value()
    
if __name__ == "__main__":
    option = rs.GetInteger("0 guessHorizontalShift | 1 resetHorizontalShift | 2:printHorizontalShift ",number=0)
    Main(option)