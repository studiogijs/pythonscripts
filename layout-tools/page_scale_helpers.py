import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

def select_scale():
    
    """
    returns selected scale (e.g. 1:5, 1:1, etc.) from list box (predefined scales)
    """
    pageview = sc.doc.Views.ActiveView
    pageview.SetPageAsActive()
    id = str(pageview.ActiveViewportID)
    page_scale = Rhino.Runtime.TextFields.LayoutUserText(id, "page_scale")
    scales = ["1:100","1:50","1:20","1:10","1:5","1:2","1:1","2:1","5:1","10:1"]
    if (not page_scale) or (page_scale not in scales):
        value = rs.ListBox(scales, "Select scale", "Scale", "1:5")
    else:
        value = rs.ListBox(scales, "Select scale", "Scale", page_scale)
    if not value:
        return
    else:
        return value

def change_page_scale():
    
    """
    returns the selected page scale (e.g. 1:5, 1:1 etc.) or none if canceled
    """
    
    #set focus to page
    pageview = sc.doc.Views.ActiveView
    pageview.SetPageAsActive()
    id = str(pageview.ActiveViewportID)
    view_port = pageview.MainViewport
    value = select_scale()
    if not value:
        return
    view_port.SetUserString("page_scale",value)
    page_scale = Rhino.Runtime.TextFields.LayoutUserText(id, "page_scale")
    return page_scale


def get_scale(readable_scale):
    
    """
    input values:
        readable_scale
    returns readable_scale to scale (e.g. 1:50 --> 0.02)
    """
    
    scale = None
    if readable_scale =="1:100": scale = 0.01 
    if readable_scale =="1:50": scale = 0.02
    if readable_scale =="1:20": scale = 0.05
    if readable_scale =="1:10": scale = 0.1
    if readable_scale =="1:5": scale = 0.2
    if readable_scale =="1:2": scale = .5
    if readable_scale =="1:1": scale = 1.0
    if readable_scale =="2:1": scale = 2.0
    if readable_scale =="5:1": scale = 5.0
    if readable_scale =="10:1": scale = 10.0
    #leave any other readable ratio that doesn't fit the bill
    if not scale:
        return
    else:
        return scale
        
def set_detail_scale(detail, scale):
    """
    input values:
        detail (DetailViewObject, the detail to change)
        scale (float, the scale to set the detail to)
    changes detail's scale
    void function
    """
    
    #modify the scale
    pageview = sc.doc.Views.ActiveView
    pageview.SetActiveDetail(detail.Id)
    if scale<=1.0:
        readable_scale = "1:" + str(int(1/scale))
    else:
        readable_scale = str(int(scale)) + ":1"
    attribs = detail.Attributes.Duplicate()
    attribs.SetUserString("detail_scale", readable_scale)
    sc.doc.Objects.ModifyAttributes(detail.Id, attribs, True)
    
    #detail.SetUserString("detail_scale", readable_scale)
    
    
    detail.DetailGeometry.SetScale(1, sc.doc.ModelUnitSystem, scale, sc.doc.PageUnitSystem)
    #lock detail
    detail.DetailGeometry.IsProjectionLocked = True
    detail.CommitChanges()
    
    #set focus back to page
    pageview.SetPageAsActive()
    sc.doc.Views.Redraw()
    