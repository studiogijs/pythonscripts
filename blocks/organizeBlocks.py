import rhinoscriptsyntax as rs
import Rhino

def organizeBlocks():
    """
    organize blocks onto layers with their blockname nested under layer Block_Definitions
    tested in Rhino 6.14
    www.studiogijs.nl
    """
    blocks = Rhino.RhinoDoc.ActiveDoc.Objects.FindByObjectType(Rhino.DocObjects.ObjectType.InstanceReference)
    if not blocks:
        print 'no blocks found in this document'
        return
    for block in blocks:
        block_name = block.InstanceDefinition.Name
        #check if layer Block_Definitions exist, else create it
        if not rs.IsLayer("Block_Definitions"): rs.AddLayer("Block_Definitions")
        
        #check if layer with block name exists, else create it
        layer_name = "Block_Definitions::"+block_name
        if not rs.IsLayer(layer_name):
            block_layer = rs.AddLayer(block_name, parent = "Block_Definitions")
        else:
            block_layer = layer_name
        rs.ObjectLayer(block.Id, block_layer)
        
if __name__ == '__main__':
    organizeBlocks()