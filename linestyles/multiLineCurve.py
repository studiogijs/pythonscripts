import rhinoscriptsyntax as rs
import scriptcontext as sc

def multiLineCurve():
    """
    --- --- --- --- --- --- --- --- --- --- ---
    -------------------------------------------
    --- --- --- --- --- --- --- --- --- --- --- 
    this script divides a curve by length and adds dashes to either side of the curve, grouped per curve / polyline
    limitation: does not accomodate at corners (to avoid ccx issues)
    www.studiogijs.nl
    """
    curves = rs.GetObjects("select curves to change into multiline-style",4, preselect=True)
    if not curves:
        return
    s=sc.sticky['scale'] if sc.sticky.has_key('scale') else 20
    scale = rs.GetReal("scale of the multiline curve", s, 5, 100)
     
    
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
                vec = rs.CurveTangent(curve, t)*scale/5
                line = rs.AddLine(pt-vec, pt+vec)
                trans = rs.VectorRotate(vec, 90, [0,0,1])
                trans/=2
                line_copy = rs.CopyObject(line, trans)
                trans = -trans
                lines.append(line_copy)
                rs.MoveObject(line, trans)
                lines.append(line)
            group = rs.AddGroup()
            rs.AddObjectsToGroup(lines, group)
            rs.AddObjectsToGroup(curve, group)
            rs.SelectObjects(lines)
            rs.SelectObjects(curves)
    rs.EnableRedraw(True)
                
multiLineCurve() 