import rhinoscriptsyntax as rs
import scriptcontext as sc

def arrowCurve():
    """
    ---->---->---->---->---->---->---->----
    this script divides a curve by length and adds dashes to either side of the curve, grouped per curve / polyline
    limitation: does not accomodate at corners (to avoid ccx issues)
    www.studiogijs.nl
    """
    curves = rs.GetObjects("select curves to change into arrow-style",4, preselect=True)
    if not curves:
        return
    s=sc.sticky['scale'] if sc.sticky.has_key('scale') else 20
    scale = rs.GetReal("scale of the arrow curve", s, 5, 100)
     
    
    if not scale:
        return
    sc.sticky['scale']=scale
    
    rs.EnableRedraw(False)
    
    for curve in curves:
        lines=[]
        if rs.CurveLength(curve)>scale:
            pts = rs.DivideCurveLength(curve, scale)
            for pt in pts:
                t=rs.CurveClosestPoint(curve, pt)
                vec = rs.CurveTangent(curve, t)*scale/10
                line = rs.AddLine(pt, pt+vec)
                line_copy = rs.CopyObject(line, [0,0,0])
                rs.RotateObject(line, pt, 45)
                rs.RotateObject(line_copy, pt, -45)
                lines.append(line)
                lines.append(line_copy)
            group = rs.AddGroup()
            rs.AddObjectsToGroup(lines, group)
            rs.AddObjectsToGroup(curve, group)
            rs.SelectObjects(lines)
            rs.SelectObjects(curves)
    rs.EnableRedraw(True)
arrowCurve() 