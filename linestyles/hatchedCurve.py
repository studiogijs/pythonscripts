from __future__ import division
import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
#from System.Drawing import Color

def hatchedCurve():
    """
    this script divides a curve by length and makes a hatch-dashed version of it'
    works only in world top
    version 1.1
    www.studiogijs.nl
    """
    
    projection  = Rhino.Geometry.Vector3d(0,0,1)
    viewprojection  = sc.doc.Views.ActiveView.ActiveViewport.CameraZ
    if not viewprojection == projection:
        print " this script only works in top view"
        return
    getcurves = rs.GetObjects("select curves to change into hatch-dashed-style",4, preselect=True)
    rs.UnselectAllObjects()
    if not getcurves:
        return

    s=sc.sticky['scale'] if sc.sticky.has_key('scale') else 1
    scale = rs.GetReal("line-width of the hatch-dashed curve", s, .5, 5)
     
    if not scale:
        return
    sc.sticky['scale']=scale
    
    f=sc.sticky['factor'] if sc.sticky.has_key('factor') else 5
    factor = rs.GetReal("line-length factor of the hatch-dashed curve", f, 1, 10)
     
    if not factor:
        return
    sc.sticky['factor']=factor
    
    #turn of the lights, magic should be done in darkness
    rs.EnableRedraw(False)    
    
    style = Rhino.Geometry.CurveOffsetCornerStyle.Sharp
    tol = sc.doc.ModelAbsoluteTolerance
    plane = Rhino.Geometry.Plane.WorldXY
    
    subcurvelist=[]
    offset_curves=[]
    for curve in getcurves:
        # ------------------------------------------------------
        # offset curves inward and outward to create the borders 
        # ------------------------------------------------------
        c = rs.coercecurve(curve)
        if not rs.IsCurvePlanar(curve):
            continue
        #else:
            #rs.HideObject(curve)
        
        offsets =c.Offset(plane, scale/2, tol, style)
        if offsets:
            offset = sc.doc.Objects.Add(offsets[0])
            offset_curves.append(offset)
        offsets =c.Offset(plane, -scale/2, tol, style)
        if offsets:
            offset = sc.doc.Objects.Add(offsets[0])
            offset_curves.append(offset)
        # -----------------------------------
        # explode c into segments if possible
        # -----------------------------------
        exploded = rs.ExplodeCurves(c)
        if exploded :
            for segment in exploded:
                subcurvelist.append(segment)
        else:
            #it appears this is for single lines only
            subcurvelist.append(rs.CopyObject(curve))
    
    segments=[]
    # -------------------------------------------------------
    # divide subcurves into shorter segments (dashed pattern)
    # -------------------------------------------------------
    for curve in subcurvelist:
        closed=False
        if rs.coercecurve(curve).IsClosed:
            closed=True 
        if rs.CurveLength(curve)>(scale*factor):
            segment_count = int(rs.CurveLength(curve)/(scale*factor/2))
            while True:
                #we need to start with 1/2 segment, then full space, then half segment
                #so #of segments needs to be a multiple of 4
                if segment_count%4==0: break
                else: segment_count+=1
            
            pts = rs.DivideCurve(curve, segment_count)
            
            if closed:
                pts = pts[1:] #remove only first point, since last point == first    
            pts = pts[1:-1] #remove first and last point
            
            pts = pts[::2] #remove every other point
            # --------------
            # dash the curve 
            # --------------
            for i, pt in enumerate(pts):
                t = rs.CurveClosestPoint(curve, pt)
                curves = rs.SplitCurve(curve, t)
                curve = curves[1]
                segment = curves[0]
                if closed:
                    #delete every odd segment
                    if i%2==0:
                        rs.DeleteObject(segment)
                    else: segments.append(segment)
                else:
                    #delete every even segment
                    if i%2==1:
                        rs.DeleteObject(segment)
                    else:
                        segments.append(segment)
                        
            #append the remaining part
            segments.append(curve)
    
    def hatchthis(s):
        
        #offset all segments
        s=rs.coercecurve(s)
        offsets = s.Offset(plane, scale/2, tol, style)
        if offsets:
            p1,p2, curve1 = getPointsAndLines(offsets)
        offsets = s.Offset(plane, -scale/2, tol, style)
        if offsets:
            p3,p4, curve2 = getPointsAndLines(offsets)     
        if not (p1 and p2 and p3 and p4):
            return
        
        #create end lines between the two offset curves
        line1 = rs.AddLine(p1, p3)
        line2 = rs.AddLine(p2, p4)
        polyline = rs.JoinCurves([line1, line2, curve1, curve2], True, tol)
        
        # FINALLY: hatch the bloody thing
        hatch = rs.AddHatch(polyline, 'Solid')
        
        #clean up
        rs.DeleteObject(polyline)
        
        return hatch
    
    if segments:
        segments = rs.JoinCurves(segments, True)
        layer = "hatched_curves"
        if not rs.IsLayer(layer):
            rs.AddLayer(layer)
        
        hatches =[]
        #create the hatches
        for s in segments:
            rs.ObjectLayer(hatchthis(s), layer)
        for offset in offset_curves:
            rs.ObjectLayer(offset, layer)

    #clean up    
    rs.DeleteObjects(segments)
    rs.HideObjects(getcurves)
    rs.DeleteObjects(curves)
    #put on the lights, it's the result that counts
    rs.EnableRedraw(True)

def getPointsAndLines(offsets):
    """
    function to get the end points and underlying curve geometry of the offsets
    """
    if type(offsets[0])==Rhino.Geometry.PolylineCurve:
        curve = sc.doc.Objects.AddPolyline(offsets[0].ToPolyline())
        c1 = offsets[0].ToPolyline()
        p1 = c1.First
        p2 = c1.Last
    elif type(offsets[0])==Rhino.Geometry.LineCurve:
        curve = sc.doc.Objects.AddLine(offsets[0].Line)
        c1 = offsets[0].Line
        p1 = c1.From
        p2 = c1.To
    else:
        curve = offsets[0]
        p1 = curve.PointAtStart
        p2 = curve.PointAtEnd
        curve = sc.doc.Objects.AddCurve(curve)
    return p1, p2, curve


if __name__ == "__main__":            
    hatchedCurve()        
