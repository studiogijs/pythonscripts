import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import page_scale_helpers as psh

def main():
    """
    sets a predefined scale from a list for selected detail(s), defaults to page scale
    
    version 0.1
    www.studiogijs.nl
    """
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
    