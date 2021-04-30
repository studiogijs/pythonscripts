import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
def change_page_scale():
    
    #set focus to page
    pageview = sc.doc.Views.ActiveView
    pageview.SetPageAsActive()
    id = str(pageview.ActiveViewportID)
    view_port = pageview.MainViewport
    page_scales = ["1:100","1:50","1:20","1:10","1:5","1:2","1:1","2:1","5:1","10:1"]
    value = rs.ListBox(page_scales, "Set page scale", "Page scale", "1:5")
    if not value:
        return
    view_port.SetUserString("page_scale",value)
    page_scale = Rhino.Runtime.TextFields.LayoutUserText(id, "page_scale")
    return page_scale
if __name__ == '__main__':
    change_page_scale() 