import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino


def addPartList():
    """
    create a partlist from blockitems that are numbered with annotationBalloon_v02.py
    Run the script to update the list at any time, for example after adding
    new balloons or removing balloons
    
    version 0.2
    changes in 0.2: added quotes around block names to make it work in v7 wip
    www.studiogijs.nl
    """
    
    groups = sc.doc.ActiveDoc.Groups
    partlist = []
    for group in groups:
        texts=[]
        if group.Name == None or group.GetUserString("group-nr")==None:
            continue
        elif sc.doc.ActiveDoc.Groups.GroupObjectCount(group.Index) == 0:
            continue
        else:
            texts.append(group.GetUserString("group-nr"))
            blockname = group.GetUserString("block-name")
            texts.append(blockname)
            blockcount = getInstanceCount(blockname)
            texts.append(blockcount)
        partlist.append(texts)
    createTable(partlist)

def getInstanceCount(name):
    version = getRhinoVersion()
    if version ==5:
        count = str(rs.BlockInstanceCount(name))
    else:
        count = "%<BlockInstanceCount(\""+name+"\")>%"
    return count

def createTable(partlist):
    if not "partlistgroup" in rs.GroupNames():
        rs.AddGroup("partlistgroup")
    #clean the group
    group= sc.doc.Groups.FindName("partlistgroup")
    objs = sc.doc.ActiveDoc.Groups.GroupMembers(group.Index)
    rs.DeleteObjects(objs)
    
    #rs.DeleteObjects
    twidth = 100
    def addTexts(texts, y):
        for i,text in enumerate(texts):
            if i==0:
                a=6
                just = Rhino.Geometry.TextJustification.BottomRight
                
            elif i==1:
                a=9.5
                just = Rhino.Geometry.TextJustification.BottomLeft
            else:
                a=14+twidth
                just = Rhino.Geometry.TextJustification.BottomRight
            plane = Rhino.Geometry.Plane.WorldXY
            plane.Origin = Rhino.Geometry.Point3d(a, y-4, 0)
            
            textobject = sc.doc.Objects.AddText(text, plane, 2.0 ,'Courier New', False, False, just)
            rs.AddObjectToGroup(textobject, "partlistgroup")
        
    def addBorders(i,y):
        
        start = Rhino.Geometry.Point3d(0,y-6,0)
        end = Rhino.Geometry.Point3d(16+twidth,y-6,0)
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
        
        trans = Rhino.Geometry.Transform.Translation(8,0,0)
        v_line.Transform(trans)
        line = sc.doc.Objects.AddLine(v_line)
        rs.AddObjectToGroup(line, "partlistgroup")
        
        trans = Rhino.Geometry.Transform.Translation(twidth,0,0)
        v_line.Transform(trans)
        line = sc.doc.Objects.AddLine(v_line)
        rs.AddObjectToGroup(line, "partlistgroup")
        
        trans = Rhino.Geometry.Transform.Translation(8,0,0)
        v_line.Transform(trans)
        line = sc.doc.Objects.AddLine(v_line)
        rs.AddObjectToGroup(line, "partlistgroup")

    y = len(partlist)*6
    for i, texts in enumerate(partlist):
        addTexts(texts, y)
        addBorders(i, y)
        y-=6
    #sc.doc.Views.Redraw()
    group= sc.doc.Groups.FindName("partlistgroup")
    objs = sc.doc.ActiveDoc.Groups.GroupMembers(group.Index)
    
    rs.MoveObjects(objs, (10,10,0))

def getRhinoVersion():
    version = str(Rhino.RhinoApp.ExeVersion)

    if version=='5':
        version = 5
    elif version=='6':
        version = 6
    elif version=='7':
        version = 7
    else:
        return False
    return version

if __name__ == '__main__':
    addPartList()