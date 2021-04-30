import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import page_scale_helpers as psh



def set_details_scale_to_page_scale():
    """
    This script changes the scale of the details to the page scale and adds a page scale if not set
    
    version 0.1
    www.studiogijs.nl
    """

    #set focus to page
    pageview = sc.doc.Views.ActiveView
    pageview.SetPageAsActive()
    id = str(pageview.ActiveViewportID)
    #set page scale
    page_scale = psh.change_page_scale() 
    scale = psh.get_scale(page_scale)
    if not scale:
        return    
    #get all details on page, set scale to page scale
    details = pageview.GetDetailViews()
    for detail in details:
        psh.set_detail_scale(detail, scale)

    sc.doc.Views.Redraw()

if __name__ == '__main__':
    set_details_scale_to_page_scale()