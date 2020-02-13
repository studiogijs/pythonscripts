import rhinoscriptsyntax as rs

def moveLight():
    """
    Use this script to move a light in the direction it is aimed.
    Positive values are in the direction it aimed at.
    Typically use this in a toolbar, where you can pass the distance directly.
    script by Gijs de Zwart
    www.studiogijs.nl
    """
    distance = rs.GetInteger(number=10)
    object = rs.GetObject("select light to move in normal direction", preselect=True, filter=256)
    if not object:
        return
    light = rs.coercerhinoobject(object)
    dir = light.LightGeometry.Direction
    dir.Unitize()
    trans=dir*distance
    rs.MoveObject(object, trans)
    rs.SelectObject(object)
if __name__ == "__main__":
    moveLight()