import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import System.Drawing.Color as Col

def organizeDetails():
    """
    puts all details on layer 'details'
    creates layer called 'details' if it doesn't exist and changes its color to green
    version 1.0
    www.studiogijs.nl
    """

    #check if layer 'details' exist, else create it
    if not rs.IsLayer("details"): rs.AddLayer("details")
    rs.LayerColor("details",Col.Aquamarine)
    pageviews = sc.doc.Views.GetPageViews()
    for pageview in pageviews:
        #get all details
        details = pageview.GetDetailViews()
        for detail in details:
            rs.ObjectLayer(details, "details")

if __name__ == '__main__':
    organizeDetails() 