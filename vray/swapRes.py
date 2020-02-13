import rhinoscriptsyntax as rs

def swapRes():
    """
    This script script swaps x and y resolution.
    Typically useful for standard formats (together with changeRes.py) to switch between portrait and landscape
    script by Gijs de Zwart
    www.studiogijs.nl
    """
    vray = rs.GetPlugInObject("V-Ray for Rhino")
    
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_pixelAspect")
    param.Value=5
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_aspect_ratio")
    param.Value=5
    param = vray.Scene().Plugin("/SettingsOutput").Param("lock_resolution")
    param.Value = False
    
    param1 = vray.Scene().Plugin("/SettingsOutput").Param("img_width")
    width = param1.Value()
    
    param2 = vray.Scene().Plugin("/SettingsOutput").Param("img_height")
    height = param2.Value()
    param1.Value = height
    param2.Value = width
    vray.RefreshUI()
    print "x resolution is now %d and y %d" %(height, width)
swapRes()
