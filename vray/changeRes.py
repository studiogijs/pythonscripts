import rhinoscriptsyntax as rs

def changeRes():
    """
    This script scales the resolution by user specified factor.
    Typically use this in a toolbar, where you can pass the scale factor directly
    script by Gijs de Zwart
    www.studiogijs.nl
    """
    i=rs.GetReal(number=2, minimum=0.1)
    vray = rs.GetPlugInObject("V-Ray for Rhino")
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_width")
    param.Value = int(param.Value()*i)
    width = param.Value()
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_height")
    param.Value = int(param.Value()*i)
    height = param.Value()
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_aspect_ratio")
    param.Value = 5
    print "image resolution set to %d by %d" %(width, height)
changeRes()
