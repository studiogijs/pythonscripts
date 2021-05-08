import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import page_scale_helpers as psh

def main():
    """
    Sets page scale and changes all details to the same scale. Adds 'page_scale'
    user text key and value to the page and detail_scale user text to details
    """
    
    pageview = sc.doc.Views.ActiveView
    if type(pageview) != Rhino.Display.RhinoPageView:
        print "This tool only works in layout space."
        return
    pagescale = psh.change_page_scale()#returns readable scale e.g. 1:5, 2:1
    
    if not pagescale:
        return
    scale = psh.get_scale(pagescale)#returns page scale ratio e.g 0.2, 2.0
    print scale
    details = pageview.GetDetailViews()
    if not details:
        return
    for detail in details:
        if not detail.DetailGeometry.IsParallelProjection:
            continue
        psh.set_detail_scale(detail, scale)

if __name__=="__main__":
    main()
