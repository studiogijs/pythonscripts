import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

def addDetailScale():
    """
    adds a scale caption to a selected detail to the lower left corner
    version 1.0
    www.studiogijs.nl
    """
    #set focus back to page
    pageview = sc.doc.Views.ActiveView
    pageview.SetPageAsActive()
    detail = rs.GetObject("select detail to change",32768, preselect=True)
    if not detail:
        return
    detail = rs.coercerhinoobject(detail)
    
    if detail.DetailGeometry.IsParallelProjection:
        ratio = detail.DetailGeometry.PageToModelRatio

        if ratio >=1:
            text = str(int(ratio)) + ":1"
        else:
            text = "1:" + str(int(1/ratio))

            pt = [0,0,0]
            pt[0] = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Min.X+3
            pt[1] = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Min.Y+3
            text = "detail (scale " +text+ ")"
            
            sc.doc.Views.ActiveView = pageview
            rs.AddText(text, pt, height=2.0, font = 'Courier new', justification = 65537)#bottom left
                    
                
if __name__ == '__main__':
    addDetailScale() 