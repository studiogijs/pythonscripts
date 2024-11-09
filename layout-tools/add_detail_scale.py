import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import page_scale_helpers as psh

def main():
    """
    adds a scale caption to a selected detail to the lower left corner if it's different
    from the page scale
    version 1.1
    www.studiogijs.nl
    
    new in version 1.1:
    -solved a bug that prevented text being added
    -added a check if page scale was set
    """
    pageview = sc.doc.Views.ActiveView
    
    if type(pageview) != Rhino.Display.RhinoPageView:
        print ("This tool works only in layout space.")
        return
    
    details = rs.GetObjects("select detail(s) to add detail info to",32768, preselect=True)
    if not details:
        return
    for detail in details:
        add_detail_scale(detail)

def add_detail_scale(detail):
    #set focus back to page
    pageview = sc.doc.Views.ActiveView
    pageview.SetPageAsActive()
    detail = rs.coercerhinoobject(detail)
    
    page_scale = pageview.ActiveViewport.GetUserString("page_scale")
    if page_scale==None:
        psh.change_page_scale()
    if detail.DetailGeometry.IsParallelProjection:
        ratio = detail.DetailGeometry.PageToModelRatio

        if ratio >=1.0:
            text = str(int(ratio)) + ":1"
        else:
            text = "1:" + str(int(1/ratio))
        if page_scale == text:
            print ("At least one detail has the same scale as the page scale, no scale info to this detail was added.")
            return
        else:
            pt = [0,0,0]
            pt[0] = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Min.X+3
            pt[1] = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Min.Y+3
            psh.set_detail_scale(detail, ratio)
            id = str(detail.Id)
            p="%"
            scale = '%s<UserText("%s","detail_scale")>%s' % (p, id, p)
            
            text = "detail (scale " +scale+ ")"
            
            sc.doc.Views.ActiveView = pageview
            rs.AddText(text, pt, height=2.0, font = 'Courier new', justification = 65537)#bottom left
                    
                
if __name__ == '__main__':
    main() 