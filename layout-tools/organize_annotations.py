import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
from System.Drawing import Color as Col

def organize_annotations():
    """
    - puts all dimensions found in all pages on layer 'dim' and annotations on 'annotation'
    - creates layer called 'dim' + 'annotation' if it doesn't exist and changes its color to black
    version 1.0
    www.studiogijs.nl
    """

    #check if layer 'dim' exist, else create it
    if not rs.IsLayer("dim"): rs.AddLayer("dim")
    rs.LayerColor("dim",Col.Black)
    
    #check if layer 'annotation' exist, else create it
    if not rs.IsLayer("annotation"): rs.AddLayer("annotation")
    rs.LayerColor("annotation",Col.Black)
    
    objects = Rhino.RhinoDoc.ActiveDoc.Objects.FindByObjectType(Rhino.DocObjects.ObjectType.Annotation)
    
    for obj in objects:
        
        if type(obj)==Rhino.DocObjects.LeaderObject or type(obj)==Rhino.DocObjects.TextObject:
            rs.ObjectLayer(obj, "annotation")
        else:
            rs.ObjectLayer(obj, "dim")

if __name__ == '__main__':
    organize_annotations() 