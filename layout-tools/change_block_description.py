import rhinoscriptsyntax as rs

def change_block_description():
    
    """
    change or set a block description
    
    version 1.0
    www.studiogijs.nl
    """
    
    
    block = rs.GetObject("select block to add or change description", filter = 4096, preselect = True)
    if not block:
        return
    block = rs.coercerhinoobject(block).InstanceDefinition

    desc = rs.BlockDescription(block.Name)
    if desc == None:
        print "Current description not set"
    else:
        print "Current description: " + desc
    newdesc = rs.GetString("Set new description, to use spaces enter description between \" \"")
    if newdesc:
        rs.BlockDescription(block.Name, newdesc)

    

if __name__=="__main__":
    change_block_description()