import rhinoscriptsyntax as rs
import System
def changeRes():
    """
    With this script you can change the resolution through the command line.
    Typically use this in a toolbar, where you can pass the x and y relolution directly
    script by Gijs de Zwart
    www.studiogijs.nl
    """
    width = rs.GetInteger(number = 1024)
    height = rs.GetInteger(number=768)
    vray = rs.GetPlugInObject("V-Ray for Rhino")
    
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_pixelAspect")
    param.Value=5
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_aspect_ratio")
    param.Value=5
    
    
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_width")
    
    param.Value = width
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_height")
    param.Value = height
    
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_aspect_ratio_height")
    param.Value = System.Single(1)
    param = vray.Scene().Plugin("/SettingsOutput").Param("img_aspect_ratio_width")
    param.Value = System.Single(width/height)
    param = vray.Scene().Plugin("/SettingsOutput").Param("lock_resolution")
    param.Value = True
    vray.RefreshUI()

changeRes()
