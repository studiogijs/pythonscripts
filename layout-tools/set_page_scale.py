import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import page_scale_helpers as psh

def main():
    """
    set page scale by adding 'page_scale' user text key and value
    """
    psh.change_page_scale()

if __name__=="__main__":
    main()
