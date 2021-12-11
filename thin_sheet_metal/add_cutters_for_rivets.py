import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def add_cutters_for_rivets():
    
    """
    This script adds cylinder objects (as a group named 'rivet-hole-cutters')
    at rivet block positions to easily cut holes into
    the sheet metal objects. 
    
    www.studiogijs.nl
    """
    depth = 12
    origin = Rhino.Geometry.Point3d(0.0,0.0,-depth/2)
    direction = Rhino.Geometry.Vector3d(0.0, 0.0, 1.0)
    plane = Rhino.Geometry.Plane(origin, direction)
    
    
    blocks = sc.doc.ActiveDoc.InstanceDefinitions
    
    blocknames=[]
    
    for block in blocks:
        if block.Name!= None:
            if block.Name.__contains__("rivet"):
                blocknames.append(block.Name)
    if len(blocknames)==0:
        print "no rivet block items found in this document"
        return
    rivets = []
    for name in blocknames:
        instances = rs.BlockInstances(name, 0)
        for instance in instances:
            rivets.append(instance)
    cutters = []
    cutter_group = rs.AddGroup("rivet-hole-cutters")
    for rivet in rivets:
        radius = float(rs.coercerhinoobject(rivet).InstanceDefinition.Name[-5])/2+0.15
        circle = Rhino.Geometry.Circle(plane, radius).ToNurbsCurve()
        cyl = Rhino.Geometry.Extrusion.Create(circle, depth, True)
        xform = rs.BlockInstanceXform(rivet)
        trans = Rhino.Geometry.Transform(xform)
        cyl.Transform(trans)
        cutter = sc.doc.Objects.AddExtrusion(cyl)
        rs.AddObjectToGroup(cutter, "rivet-hole-cutters")
        
    sc.doc.Views.Redraw()

if __name__== "__main__":
    add_cutters_for_rivets()