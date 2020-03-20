from inspect import getsource, getmembers, isfunction
import rhinoscriptsyntax as rs

import Rhino
import scriptcontext as sc


""" script to search blockitems
"""

def get_source():
    
    search_term = rs.StringBox('Function name to search for', title = 'blockitems').lower()
    if not search_term:
        return
    table = sc.doc.InstanceDefinitions
    
    counts = [block.ObjectCount for block in table.GetList(True)]
    print counts
    blocknames = [block.Name for block in table.GetList(True)]
    match = [(name.lower(), rs.BlockInstanceCount(name)) for name in blocknames if search_term in name.lower()]
    print match
    selected = rs.ListBox(match)
    print 'you selected ', selected
   
    #print rs.BlockInstanceCount(selected)


if __name__ == '__main__':
    get_source()