import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import page_scale_helpers as psh

def main():
    """
    - sets a predefined scale from a list for selected detail(s), defaults to page scale
    
    version 0.2
    www.studiogijs.nl
    """
    pageview = sc.doc.Views.ActiveView
    if type(pageview) != Rhino.Display.RhinoPageView:
        print "This tool only works in layout space."
        return
    details = rs.GetObjects("select detail(s) to change scale",32768, preselect=True)
    if not details:
        return
    value = psh.select_scale()
    if not value:
        return
    scale = psh.get_scale(value)
    for detail in details:
        
        detail = rs.coercerhinoobject(detail)
        if not detail.DetailGeometry.IsParallelProjection:
            continue
        psh.set_detail_scale(detail, scale)


 
if __name__ == '__main__':
    main()
    