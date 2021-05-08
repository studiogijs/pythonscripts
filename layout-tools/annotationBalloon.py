import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc
def get_block_index(blockname):
    #blockcount = sc.doc.ActiveDoc.InstanceDefinitions.ActiveCount
    blocks = sc.doc.ActiveDoc.InstanceDefinitions
    blocknames=[]
    for block in blocks:
        if block.Name!= None and block.Name!="titleblock":
            blocknames.append(block.Name)
    return blocknames.index(blockname)
    

def annotationBalloon():
    """
    Adds a numbered balloon to the document based on the numbering in part list.
    Works only with block items, similar to how this works in 'solid modelers'
    on parts in assemblies
    www.studiogijs.nl
    """
    
    name = getBlockName()
    if not name:
        return
    block_nr = get_block_index(name)+1 
    
    curve, size = getInput()
    if curve and size:
        aCircle, aText, aCurve = addAnnotationCircle(curve, block_nr, size)
        aEndDot = addEndDot(curve, size)
    else:
        return
    #create annotation object
    groupname = 'annotation-object_'+str(block_nr)
    rs.AddGroup(groupname)
    rs.AddObjectsToGroup([aCircle, aText, aCurve, aEndDot], groupname)
    
    groups = sc.doc.ActiveDoc.Groups
    for group in groups:
        if group.Name == groupname:
            group.SetUserString("group-nr", str(block_nr))
            group.SetUserString("block-name", name)
    
   


def addAnnotationCircle(curve, block_nr, s):
    """
    adds a circle with text at user specified size to the end of a curve
    returns circle and number
    """
    vector = curve.TangentAtEnd
    vector*=s
    pt = curve.PointAtEnd
    pt+=vector
    circle = Rhino.Geometry.Circle(pt, s)
    hatchcurve = circle.ToNurbsCurve()
    circle = sc.doc.Objects.AddCircle(circle)
    curve = sc.doc.Objects.Add(curve)
    text = str(block_nr)
    plane = Rhino.Geometry.Plane.WorldXY
    plane.Origin = pt
    just = Rhino.Geometry.TextJustification.MiddleCenter
    text = sc.doc.Objects.AddText(text, plane, s*0.6 ,'Courier Std', False, False, just)
    return circle, text, curve

def addEndDot(curve, s):
    """
    creates a hatched circle at the start of a curve
    """
    d = s/5
    pt = curve.PointAtStart
    circle = Rhino.Geometry.Circle(pt, d)
    circle = circle.ToNurbsCurve()
    hatch = Rhino.Geometry.Hatch.Create(circle, 0, 0, 0)
    dot = sc.doc.Objects.AddHatch(hatch[0])
    return dot
    
    
def getInput():
    """
    returns the drawn curve, annotation size and value on success, or False on failure
    """
    s = sc.sticky['annSize'] if sc.sticky.has_key('annSize') else 5 #size of circle radius
    if s==None:
        s=5
    size = rs.GetInteger("size of annotation", s, 3)
    sc.sticky['annSize'] = size
    curve = getPolyline()
        
    if curve:
        curve = curve.ToNurbsCurve()
        return curve, size
    return False, False

def getPolyline():
    points = rs.GetPoints(draw_lines = True, in_plane = True, max_points = 3)
    if points and len(points)>1:
        return Rhino.Geometry.Polyline(points)
    return False

def getBlockName():
    """
    input: user input selected block
    returns block name on succes
    """
    go = Rhino.Input.Custom.GetObject()
    go.SetCommandPrompt("Select block instance to annotate")
    go.GeometryFilter = Rhino.DocObjects.ObjectType.InstanceReference
    go.EnablePreSelect(False, True)
    go.InactiveDetailPickEnabled = True
    rc = go.Get()
    if rc == Rhino.Input.GetResult.Object:
        
        objref = go.Object(0)
        obj = objref.Object()
        name = rs.BlockInstanceName(obj.Id)
        return name
    return False

if __name__ == '__main__':
    annotationBalloon()