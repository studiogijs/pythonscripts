import Rhino
import rhinoscriptsyntax as rs

def bounding_points():
    """
    adds bounding points to one or more (pre)selected objects, which can help
    positioning gumball or aligning/positioning objects
    
    ***********************************
    * script written by Gijs de Zwart *
    * www.studiogijs.nl               *
    ***********************************
    
    """
    objects=rs.GetObjects("select objects to add boundingbox points", preselect=True)
    if not objects:
        return
    bb=rs.BoundingBox(objects)
    
    BB = Rhino.Geometry.BoundingBox(bb)
    
    mid1 = BB.Center
    mid1.Z = BB.Min.Z #bottom
    mid2 = BB.Center
    mid2.Z = BB.Max.Z #top
    mid3 = BB.Center 
    mid3.Y = BB.Min.Y #front
    mid4 = BB.Center 
    mid4.Y = BB.Max.Y #back
    mid5 = BB.Center 
    mid5.X = BB.Min.X #left
    mid6 = BB.Center 
    mid6.X = BB.Max.X #right
    bb.append(mid1)
    bb.append(mid2)
    bb.append(mid3)
    bb.append(mid4)
    bb.append(mid5)
    bb.append(mid6)
    bb=rs.CullDuplicatePoints(bb,0.01)
    cloud=rs.AddPointCloud(bb)
    objects.append(cloud)
    rs.AddGroup(cloud)
    rs.AddObjectsToGroup(objects, cloud)

if( __name__ == "__main__" ):
    bounding_points()