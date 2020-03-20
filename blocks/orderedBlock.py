import rhinoscriptsyntax as rs
import Rhino


def organizedBlock():
    """
    create a block from selection and add it to a layer with the block's name
    nested under layer Block_Definitions
    tested in Rhino 6.14
    www.studiogijs.nl
    """
    
    #get objects to create block from
    objs = rs.GetObjects("select objects to creat block from")
    if not objs: return
    
    base_point = rs.GetPoint("block base point")
    if not base_point: return
    
    
    
    
    def checkName():    
        block_name = rs.GetString("enter block name")
        #check if layer Block_Definitions exist, else create it
        if not rs.IsLayer("Block_Definitions"): rs.AddLayer("Block_Definitions")
        
        #check if layer with block name exists, else create it
        if not rs.IsLayer("Block_Definitions::"+block_name):
            block_layer = rs.AddLayer(block_name, parent = "Block_Definitions")
            return block_layer, block_name
        else:
             print "block definition with this name already exists"
             checkName()
        
            
    block_layer, block_name = checkName()
    
    #create the block
    
    block = rs.AddBlock(objs, base_point, block_name, True)
    if not block:
        return
    temp_layer = rs.CurrentLayer()
    
    rs.CurrentLayer(block_layer)
    rs.InsertBlock(block, base_point)
    rs.CurrentLayer(temp_layer)

if __name__ == '__main__':
    organizedBlock()