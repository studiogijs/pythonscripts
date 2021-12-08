import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino
import System.Drawing.Color as Col

def main():
    """
    Creates a part list for all blocks in a document. Numbers will correspond with 
    balloons, but balloons don't need to be present for the table to be generated
    
    version 1.2
    www.studiogijs.nl
    
    version 1.1 adds table heading
    version 1.2 option for choosing between all or only top level blocks
   
    """
    t = sc.sticky['top_level_only'] if sc.sticky.has_key('top_level_only') else 0 #0 = top level only, 1= all blocks
    if t==None:
        t=0
    top_level_only = rs.GetBoolean("annotate top level blocks only?", ["top_level_only", "yes", "no"],t)
    if not top_level_only:
        return
    sc.sticky['top_level_only'] = top_level_only[0]
    
    
    previous_layer = rs.CurrentLayer()
    #check if layer 'annotation' exist, else create it
    if not rs.IsLayer("annotation"): rs.AddLayer("annotation")
    rs.LayerColor("annotation",Col.Black)
    
    rs.CurrentLayer("annotation")
    
    groups = sc.doc.ActiveDoc.Groups
    partlist = []
    
    blocknames=get_block_names()
    if not blocknames:
        print "This file does not contain block items (titleblock will be ignored)"
        return
    #add headings
    texts = ["ITEM", "PART NAME", "QTY"]
    partlist.append(texts)
    texts=[]
    for block_nr, blockname in enumerate(blocknames,1):
        texts.append(str(block_nr))
        texts.append(blockname)
        blockcount = get_block_count(blockname)
        texts.append(str(blockcount))

        partlist.append(texts)
        texts=[]
    create_table(partlist)
    #change back to previous layer
    rs.CurrentLayer(previous_layer)

def get_block_index(blockname):
    blocknames = get_block_names()
    if blocknames:
        return blocknames.index(blockname)
    return False
def get_block_count(blockname):
    #blockcount = sc.doc.ActiveDoc.InstanceDefinitions.ActiveCount
    blocks = sc.doc.ActiveDoc.InstanceDefinitions
    blocknames=[]
    for block in blocks:
        if block.Name==blockname:
            return block.UseCount()
    return False
    
def get_block_names():

    blocks = sc.doc.ActiveDoc.InstanceDefinitions
    blocknames=[]
    for block in blocks:
        if block.Name!= None and block.Name!="titleblock":
            if rs.IsBlockInUse(block.Name, where_to_look=sc.sticky['top_level_only']):
                blocknames.append(block.Name)
    
    if len(blocknames)>0:
       return blocknames
    return False

def create_table(partlist):
    g = rs.GroupNames()
    if not g or not "partlistgroup" in g:
        rs.AddGroup("partlistgroup")
    #clean the group
    group= sc.doc.Groups.FindName("partlistgroup")
    objs = sc.doc.ActiveDoc.Groups.GroupMembers(group.Index)
    rs.DeleteObjects(objs)
    
    twidth = 110
    def addTexts(texts, y):
        for i,text in enumerate(texts):
            if i==0:
                a=10
                just = Rhino.Geometry.TextJustification.BottomRight
                
            elif i==1:
                a=13.5
                just = Rhino.Geometry.TextJustification.BottomLeft
            else:
                a=20+twidth
                just = Rhino.Geometry.TextJustification.BottomRight
            plane = Rhino.Geometry.Plane.WorldXY
            plane.Origin = Rhino.Geometry.Point3d(a, y-4, 0)
            
            textobject = sc.doc.Objects.AddText(text, plane, 2.0 ,'Courier New', False, False, just)
            rs.AddObjectToGroup(textobject, "partlistgroup")

    def get_partlist_alignment():
    
        
        point = Rhino.Geometry.Point3d(0,0,0)
        listValues = "LowerLeft", "LowerRight", "UpperLeft", "UpperRight"
        listIndex = 1
        gp = Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Choose alignment and insertion point")
        opList = gp.AddOptionList("Alignment", listValues, listIndex)
        while True:
            get_rc = gp.Get()
            if gp.CommandResult()!=Rhino.Commands.Result.Success:
                return point, 0
            if get_rc==Rhino.Input.GetResult.Point:
                point = gp.Point()
                
            elif get_rc==Rhino.Input.GetResult.Option:
                if gp.OptionIndex()==opList:
                  listIndex = gp.Option().CurrentListOptionIndex
                continue
            break
        return point, listIndex
        
    def add_borders(i,y):
        
        start = Rhino.Geometry.Point3d(0,y-6,0)
        end = Rhino.Geometry.Point3d(22+twidth,y-6,0)
        line = sc.doc.Objects.AddLine(start, end) #bottom border
        rs.AddObjectToGroup(line, "partlistgroup")
        if i==0:
            #add top border
            trans = Rhino.Geometry.Transform.Translation(0,6,0)
            h_line = Rhino.Geometry.Line(start,end)
            h_line.Transform(trans)
            line = sc.doc.Objects.AddLine(h_line)
            rs.AddObjectToGroup(line, "partlistgroup")
        #add vertical lines
        v_start = Rhino.Geometry.Point3d(0,y,0)
        v_end = Rhino.Geometry.Point3d(0,y-6,0)
        
        v_line = Rhino.Geometry.Line(v_start,v_end)
        line = sc.doc.Objects.AddLine(v_line)
        rs.AddObjectToGroup(line, "partlistgroup")
        
        trans = Rhino.Geometry.Transform.Translation(12,0,0)
        v_line.Transform(trans)
        line = sc.doc.Objects.AddLine(v_line)
        rs.AddObjectToGroup(line, "partlistgroup")
        
        trans = Rhino.Geometry.Transform.Translation(twidth,0,0)
        v_line.Transform(trans)
        line = sc.doc.Objects.AddLine(v_line)
        rs.AddObjectToGroup(line, "partlistgroup")
        
        trans = Rhino.Geometry.Transform.Translation(10,0,0)
        v_line.Transform(trans)
        line = sc.doc.Objects.AddLine(v_line)
        rs.AddObjectToGroup(line, "partlistgroup")

    y = len(partlist)*6
    #get insertion point
    point, listIndex = get_partlist_alignment()
    if point:
        target = Rhino.Geometry.Point3d(0,0,0)
        if listIndex == 0: #lower left
            target[0] = point[0]
            target[1] = point[1]
        elif listIndex == 1: #lower right
            target[0] =point[0]-(16+twidth)
            target[1] = point[1]
        elif listIndex == 2: #upper left
            target[0] = point[0]
            target[1] = point[1]-len(partlist)*6
        else: #upper right
            target[0] =point[0]-(16+twidth)
            target[1] = point[1]-len(partlist)*6
            
    for i, texts in enumerate(partlist):
        addTexts(texts, y)
        add_borders(i, y)
        y-=6
    
    group= sc.doc.Groups.FindName("partlistgroup")
    objs = sc.doc.ActiveDoc.Groups.GroupMembers(group.Index)
    rs.MoveObjects(objs, (target))
    



if __name__ == '__main__':
    main()