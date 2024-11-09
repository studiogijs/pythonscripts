import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import page_scale_helpers as psh

def main():
    """
    - Sets page scale by adding 'page_scale' user text key and value
    version 1.0
    www.studiogijs.nl
    """
    
    pageview = sc.doc.Views.ActiveView
    if type(pageview) != Rhino.Display.RhinoPageView:
        print ("This tool only works in layout space.")
        return
    psh.change_page_scale()

if __name__=="__main__":
    main()
