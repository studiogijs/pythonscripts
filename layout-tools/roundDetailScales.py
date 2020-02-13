import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc



def roundDetailScales():
    """
    this script changes the scale of all details on all pages to their nearest scale
    version 1.01
    www.studiogijs.nl
    """
    
    #get all pages
    pageviews = sc.doc.Views.GetPageViews()
    for pageview in pageviews:
        #get all details
        details = pageview.GetDetailViews()
        for detail in details:
            #skip perspective details
            if detail.DetailGeometry.IsParallelProjection:
                ratio = detail.DetailGeometry.PageToModelRatio
                #for each scale find the nearest scale
                if 0.007<ratio<=0.015: scale = 0.01 #1:100
                if 0.015<ratio<=0.035: scale = 0.02 #1:50
                if 0.035<ratio<=0.07: scale = 0.05  #1:20
                if 0.07<ratio<=0.15: scale = 0.1 #1:10
                if 0.15<ratio<=0.35: scale = 0.2 #1:5
                if 0.35<ratio<=0.7: scale = .5 #1:2
                if 0.7<ratio<=1.5: scale = 1.0 #1:1
                if 1.5<ratio<=3.5: scale = 2.0 #2:1
                if 3.5<ratio<=7.0: scale = 5.0 #5:1
                if 7.0<ratio<=15.0: scale = 10.0 #10:1
            #leave any other page ratio that doesn't fit the bill
            else: continue
            
            #modify the scale
            pageview.SetActiveDetail(detail.Id)
            detail.DetailGeometry.SetScale(1, sc.doc.ModelUnitSystem, scale, sc.doc.PageUnitSystem)
            #lock detail
            detail.DetailGeometry.IsProjectionLocked = True
            detail.CommitChanges()
            
            #set focus back to page
            pageview.SetPageAsActive()
    sc.doc.Views.Redraw()

if __name__ == '__main__':
    roundDetailScales()