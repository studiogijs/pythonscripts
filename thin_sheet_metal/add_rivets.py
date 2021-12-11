from __future__ import division
import rhinoscriptsyntax as rs
from Rhino.ApplicationSettings import *
import Rhino
import math
import scriptcontext as sc
from System.Drawing import Color
import Rhino.RhinoMath as rm


"""
add_rivets version 1.0

this script will add a rivet (named block) in Metric size to the rhino document
The rivet must be oriented on a surface and can be aligned with a center point or point
needed user input : rivet diameter, length, (center)point on (poly)surface

use add_cutters_for_rivets.py to insert cutters at rivet positions

-based on addBolt v0.8 script

script written by Gijs de Zwart
www.studiogijs.nl

"""

class Rivet():
    def __init__(self, size, length):
        diameter         = {'3mm':3.0, '4mm':4.0, '5mm':5.0}
        self.diameter    = diameter[size]
        self.length      = length
        self.name        = "rivet_D"+size+"x"+str(length)
        self.breps       = []
        self.curves      = []
        self.size       = size
    def __repr__(self):
        cls = self.__class__.__name__
        return '{}({}x{})'.format(cls, self.size, self.length)
    def __str__(self):
        return self.name

class Countersunk(Rivet):
    def __init__(self, size, length):
        Rivet.__init__(self, size, length)
        self.name ="countersunk_"+self.name

class Blind(Rivet):
    def __init__(self, size, length):
        Rivet.__init__(self, size, length)
        self.name ="blind_"+self.name

def get_rivet_properties():
    
    
    #collect previous settings
    r_size = sc.sticky["r_size"] if sc.sticky.has_key("r_size") else 0
    r_length= sc.sticky["r_length"] if sc.sticky.has_key("r_length") else 0
    r_type= sc.sticky["r_type"] if sc.sticky.has_key("r_type") else 1


    get_o = Rhino.Input.Custom.GetOption()
    get_o.SetCommandPrompt("Set Rivet Parameters")

    r_sizes = ['3mm','4mm', '5mm']
    r_size_index = get_o.AddOptionList("Rivet_Diameter", r_sizes, r_size)

    r_lengths=['2mm','3mm','4mm','5mm','6mm']
    r_length_index = get_o.AddOptionList("Rivet_Length", r_lengths, r_length)

    r_types=['countersunk','blind']
    r_type_index = get_o.AddOptionList("Rivet_Type", r_types, r_type)

    #accept Enter as an option
    get_o.AcceptNothing(True)

    while True:
        # perform the get operation. This will prompt the user to
        # input a point, but also allow for command line options
        # defined above
        get_rc = get_o.Get()
        if get_o.CommandResult()!= Rhino.Commands.Result.Success:
            return None,None,None
            
        if get_rc==Rhino.Input.GetResult.Nothing:
            pass
            
            
            
        elif get_rc==Rhino.Input.GetResult.Option:
            
            if get_o.OptionIndex() == r_size_index:
              r_size = get_o.Option().CurrentListOptionIndex
              
            if get_o.OptionIndex() == r_length_index:
              r_length = get_o.Option().CurrentListOptionIndex
                            
            if get_o.OptionIndex() == r_type_index:
              r_type = get_o.Option().CurrentListOptionIndex

            continue
        
        break
        
    
    sc.sticky["r_size"] = r_size
    sc.sticky["r_length"] = r_length
    sc.sticky["r_type"] = r_type
    
    
    
    size = r_sizes[r_size]
    length = r_lengths[r_length]
    length = int(length[:-2])#remove mm
    rivet_type = r_types[r_type]
    
    
    return size, length, rivet_type


def create_rivet():
    # *************************************************
    # *********** CREATE THE RIVET GEOMETRY ************
    # *************************************************
    size, length, type = get_rivet_properties()
    if type=='blind':
        #create a rivet object
        rivet     = Blind(size, length)
        z = -rivet.length
        r = rivet.diameter/2
        pts=[]
        pts.append(Rhino.Geometry.Point3d(-r-1.5,0.0,0.0))
        pts.append(Rhino.Geometry.Point3d(-r-1.5,0.0,0.5))
        pts.append(Rhino.Geometry.Point3d(-r,0.0,1.0))
        pts.append(Rhino.Geometry.Point3d(-r+0.5,0.0,1.0))
        pts.append(Rhino.Geometry.Point3d(-r+0.5,0.0,z-0.5))
        pts.append(Rhino.Geometry.Point3d(-r-0.5,0.0,z-0.5))
        pts.append(Rhino.Geometry.Point3d(-r-0.5,0.0,z))
        pts.append(Rhino.Geometry.Point3d(-r,0.0,z))
        pts.append(Rhino.Geometry.Point3d(-r,0.0,0.0))
        pts.append(Rhino.Geometry.Point3d(-r-1.5,0.0,0.0)) #repeat first point
        polyline = Rhino.Geometry.Polyline(pts)
        line = Rhino.Geometry.Line(Rhino.Geometry.Point3d(0.0,0.0,0.0), Rhino.Geometry.Point3d(0.0,0.0,1.0))
        
        revolve = Rhino.Geometry.RevSurface.Create(polyline, line, 0.0, 2*math.pi)
        revolve = Rhino.Geometry.Brep.CreateFromRevSurface(revolve, False, False)
        
        
        #add objects to rivet
        rivet.breps.append(revolve)
               
        #scale objects
        rivet = set_scale(rivet)
              
        add_rivet(rivet)

    if type=='countersunk':
        #create a rivet object
        rivet     = Countersunk(size, length)
        z = -rivet.length
        r = rivet.diameter/2
        pts=[]
        pts.append(Rhino.Geometry.Point3d(-r-1.5,0.0,0.0))
        pts.append(Rhino.Geometry.Point3d(-r-1.45,0.0,0.05))
        pts.append(Rhino.Geometry.Point3d(-r+0.45,0.0,0.05))
        pts.append(Rhino.Geometry.Point3d(-r+0.5,0.0,0.0))
        pts.append(Rhino.Geometry.Point3d(-r+0.5,0.0,z-0.5))
        pts.append(Rhino.Geometry.Point3d(-r-0.5,0.0,z-0.5))
        pts.append(Rhino.Geometry.Point3d(-r-0.5,0.0,z))
        pts.append(Rhino.Geometry.Point3d(-r,0.0,z))
        pts.append(Rhino.Geometry.Point3d(-r,0.0,-0.866))
        pts.append(Rhino.Geometry.Point3d(-r-1.5,0.0,0.0)) #repeat first point
        polyline = Rhino.Geometry.Polyline(pts)
        line = Rhino.Geometry.Line(Rhino.Geometry.Point3d(0.0,0.0,0.0), Rhino.Geometry.Point3d(0.0,0.0,1.0))
        
        revolve = Rhino.Geometry.RevSurface.Create(polyline, line, 0.0, 2*math.pi)
        revolve = Rhino.Geometry.Brep.CreateFromRevSurface(revolve, False, False)
        
        
        #add objects to rivet
        rivet.breps.append(revolve)
               
        #scale objects
        rivet = set_scale(rivet)
              
        add_rivet(rivet)

def add_rivet(rivet):
    # ***********************************************
    # ******** ADDING THE RIVET TO THE SCENE *********
    # ***********************************************
    old_osnap_state = ModelAidSettings.OsnapModes #record Osnap state to reset later
    
    rivets=0
    rs.OsnapMode(32+134217728)
    while True:
        Rhino.UI.MouseCursor.SetToolTip("select surface or face")
        # this function ask the user to select a point on a surface to insert the bolt on
        # Surface to orient on
        gs = Rhino.Input.Custom.GetObject()
        gs.SetCommandPrompt("Surface to orient on")
        gs.GeometryFilter = Rhino.DocObjects.ObjectType.Surface
        gs.Get()
        if gs.CommandResult()!=Rhino.Commands.Result.Success:
            ModelAidSettings.OsnapModes = old_osnap_state #reset to previous Osnap state
            print str(rivets) + " "+rivet.__repr__() + " rivet(s) added to the document"
            Rhino.UI.MouseCursor.SetToolTip("")
            
            return

        objref = gs.Object(0)
        # get selected surface object
        obj = objref.Object()
        if not obj: 
            ModelAidSettings.OsnapModes = old_osnap_state #reset to previous Osnap state
            
            print str(rivets) + " "+rivet.__repr__() + " bolt(s) added to the document"
            return

        # get selected surface (face)
        global surface
        surface = objref.Surface()
        if not surface: return Rhino.Commands.Result.Failure
        # Unselect surface
        obj.Select(False)
    
        # Point on surface to orient to / activate center Osnap
        
        gp=Rhino.Input.Custom.GetPoint()
        gp.SetCommandPrompt("Point on surface to orient to")
        gp.Constrain(surface, False)
        #display the geometry to be created
        gp.DynamicDraw+=drawbreps
        gp.Get()
        
        if gp.CommandResult()!=Rhino.Commands.Result.Success:
            ModelAidSettings.OsnapModes = old_osnap_state #reset to previous Osnap state
            print str(rivets) + " "+rivet.__repr__() + " bolt(s) added to the document"
            return 

        getrc, u, v = surface.ClosestPoint(gp.Point())
        if getrc:
            getrc, target_plane = surface.FrameAt(u,v)
            if getrc:
                # Build transformation
                source_plane = Rhino.Geometry.Plane.WorldXY
                xform = Rhino.Geometry.Transform.PlaneToPlane(source_plane, target_plane)
                
                
                #check if layer Block_Definitions exist, else create it
                if not rs.IsLayer("Block_Definitions"): rs.AddLayer("Block_Definitions")
        
                #check if layer with block name exists, else create it
                if not rs.IsLayer("Block_Definitions::"+rivet.name):
                    
                    block_layer = rs.AddLayer("Block_Definitions::"+rivet.name, color = (120,210,210))
                    
                    
                    
                
                block_layer = "Block_Definitions::"+rivet.name
                
                layer_id = rs.LayerId(block_layer)
                
                layer_index = sc.doc.Layers.Find(layer_id, True)
                # Do the transformation
                
                
                
                rs.EnableRedraw(False)
                temp_layer = rs.CurrentLayer()
                
                rs.CurrentLayer(block_layer)
                
                objs=rivet.breps
                rhobj=[]
                for brep in objs :
                    
                    attribs = Rhino.DocObjects.ObjectAttributes()
                    attribs.WireDensity = -1
                    attribs.LayerIndex = layer_index
                    rhobj.append(sc.doc.Objects.AddBrep(brep, attribs)) 
                
                rs.AddBlock(rhobj,[0,0,0],rivet.name, True)
                
                newrivet = rs.InsertBlock2(rivet.name, xform)
                rs.CurrentLayer(temp_layer)
                rs.EnableRedraw(True)
                rivets +=1


def set_scale(rivet):
    
    scale = rm.UnitScale(sc.doc.ModelUnitSystem.Millimeters, sc.doc.ModelUnitSystem)
    xf=Rhino.Geometry.Transform.Scale(Rhino.Geometry.Plane.WorldXY, scale,scale,scale)
    for brep in rivet.breps:
        brep.Transform(xf)
    #copy to displaybreps for preview
    global displaybreps
    displaybreps = rivet.breps
     
    return rivet
                
def drawbreps(gp, args ):
    getrc, u, v = surface.ClosestPoint(args.CurrentPoint)
    if getrc:
        getrc, target_plane = surface.FrameAt(u,v)
    xf = Rhino.Geometry.Transform.PlaneToPlane(Rhino.Geometry.Plane.WorldXY,target_plane)
    
    for brep in displaybreps:
        new = brep.Duplicate()
        
        new.Transform(xf)
        args.Display.DrawBrepWires(new, Color.FromArgb(255, 120, 210, 210), 0)



if __name__ == "__main__":
    create_rivet()
