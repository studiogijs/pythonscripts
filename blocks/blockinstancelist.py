import Rhino

def main():
 # get references and store in dictionary
  robs = list( Rhino.RhinoDoc.ActiveDoc.Objects.FindByObjectType(Rhino.DocObjects.ObjectType.InstanceReference ) )
  blocks = dict( [] )
  for rob in robs:
    obref = Rhino.DocObjects.ObjRef( rob )
    refer = obref.Geometry()
    definid = refer.ParentIdefId
    if definid in blocks:
      count = blocks[ definid ]
      blocks[ definid ] = count + 1
    else:
      blocks[ definid ] = 1
 # get definitions and read instance count from dictionary
  table = Rhino.RhinoDoc.ActiveDoc.InstanceDefinitions
  for defin in table:
    name = defin.Name
    guid = defin.Id
    if guid in blocks:
      count = blocks[ guid ]
    else:
      count = 0
    print '%s(block instance) : %2d pieces' % ( name, count )

main()

