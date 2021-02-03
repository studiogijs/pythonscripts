import rhinoscriptsyntax as rs
import Rhino
import scriptcontext as sc

def annotationBalloon():
    """
    adds leader with text and dot and a table with block name and count.
    tested in Rhino 6 for Windows, won't work in Rhino 5
    works together with addPartList.py
    new in v0.3: annotation dot is now at the end of the leader rather than at the perimeter, bug fixes
    www.studiogijs.nl
    """
    
    name = getBlockName()
    if not name:
        return
    curve, v, size = getInput()
    if curve and v and size:
        aCircle, aText, aCurve = addAnnotationCircle(curve, v, size)
        aEndDot = addEndDot(curve, size)
    else:
        return
    #create annotation object
    groupname = 'annotation-object_'+str(v)
    rs.AddGroup(groupname)
    rs.AddObjectsToGroup([aCircle, aText, aCurve, aEndDot], groupname)
    
    groups = sc.doc.ActiveDoc.Groups
    for group in groups:
        if group.Name == groupname:
            group.SetUserString("group-nr", str(v))
            group.SetUserString("block-name", name)
    
    #count = getInstanceCount(name)
    #texts = [str(v),name,count]
    
    
    #pt_x = (v-1)*6+20 # increase leading
    #addTexts(texts, pt_x)
    #addBorders(v)

def getFreeSlot():
    
    groups = sc.doc.ActiveDoc.Groups
    free=0
    if groups==None:
        return 1
    for group in groups:
        #print group.Id
        
        if group.Name == None or group.GetUserString("group-nr")==None:
            continue
        else:
            free +=1
        if sc.doc.Groups.GroupObjectCount(group.Index) == 0:
            #print "slot ", group.GetUserString("group-nr") ,"is free"
            return free
        #else:
            #print "slot " , group.GetUserString("group-nr"), "is in use"
        
    free+=1
    return free

def addAnnotationCircle(curve, v, s):
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
    text = str(v)
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
    #v = sc.sticky["itemNr"] if sc.sticky.has_key("itemNr") else 1 #value to display
    v=getFreeSlot()
    #startvalue = rs.GetInteger("modify start value or press enter for next",v, 1 )
    curve = getPolyline()
    #v=startvalue
    
    if not curve:
        return False, False, False
    curve = curve.ToNurbsCurve()
    return curve, v, size

def getPolyline():
    points = rs.GetPoints(draw_lines = True, in_plane = True, max_points = 3)
    if points and len(points)>1:
        return Rhino.Geometry.Polyline(points)
    else:
        return False

def getBlockName():
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

if __name__ == '__main__':
    annotationBalloon()