import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc

def setDetailNamesToScale(addNames = True):
    """
    sets the name of the detail to its scale, so that you can use this
    property for page scale text and optianally add text with the scale
    of each detail to the lower left corner
    version 1.1
    www.studiogijs.nl
    ----
    changes:
    version 1.1 : fixed bug with adding text to wrong pages
    version 1.01 : removed typo
    
    """
    pageviews = sc.doc.Views.GetPageViews()
    for pageview in pageviews:
        #get all details
        details = pageview.GetDetailViews()
        for detail in details:
            print detail
            
            #skip perspective details
            if detail.DetailGeometry.IsParallelProjection:
                ratio = detail.DetailGeometry.PageToModelRatio
    
                if ratio >=1:
                    text = str(int(ratio)) + ":1"
                else:
                    text = "1:" + str(int(1/ratio))
                rs.ObjectName(detail.Id, text)
                if addNames:
                    
                    pt = [0,0,0]
                    pt[0] = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Min.X+3
                    pt[1] = detail.Geometry.GetBoundingBox(Rhino.Geometry.Plane.WorldXY).Min.Y+3
                    text = "detail (scale " +text+ ")"
                    
                    sc.doc.Views.ActiveView = pageview
                    rs.AddText(text, pt, height=2.0, font = 'Courier new', justification = 65537)#bottom left
                    
                
if __name__ == '__main__':
    setDetailNamesToScale() 