import rhinoscriptsyntax as rs
import scriptcontext as sc
def fenceCurve():
    """
    ---x---x---x---x---x---x---
    this script divides a curve by length and adds 'crosses' to it, grouped per curve / polyline
    www.studiogijs.nl
    """
    curves = rs.GetObjects("select curves to change into fence-style",4, preselect=True)
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
                vec = rs.CurveTangent(curve, t)
                line = rs.AddLine(pt-vec*scale/10, pt+vec*scale/10)
                rs.RotateObject(line, pt, 45)
                lines.append(line)
                line_copy = rs.RotateObject(line, pt, 90, copy=True)
                lines.append(line_copy)
            group = rs.AddGroup()
            rs.AddObjectsToGroup(lines, group)
            rs.AddObjectsToGroup(curve, group)
            rs.SelectObjects(lines)
            rs.SelectObjects(curves)
    rs.EnableRedraw(True)
                
fenceCurve()        