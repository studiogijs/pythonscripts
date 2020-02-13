
"""
This script does what the name says: it allows you make a curve from 2 views loosely.
This means the resulting curve has the same structure and degree, and same amount
of control points as the original curves. Points don't need to be aligned exactly,
the script will average points out it the flow direction of the curves.

***********************************
* script written by Gijs de Zwart *
* www.studiogijs.nl               *
* March, 2016                     *
***********************************

"""

import rhinoscriptsyntax as rs

def Crv2ViewLoose():
    curve1 = rs.GetObject("select first curve", rs.filter.curve)
    if curve1 !=None:
        rs.LockObject(curve1)
    curve2 = rs.GetObject("select second curve", rs.filter.curve)
    if curve1==None or curve2==None:
        return

    degree1=rs.CurveDegree(curve1)
    degree2=rs.CurveDegree(curve2)
    pts1 = rs.CurvePoints(curve1)
    pts2 = rs.CurvePoints(curve2)
    error=False
    errors=[]
    if rs.IsPolyCurve(curve1) or rs.IsPolyCurve(curve2):
        errors.append("Error: This script only works for single open curves")
        error=True
    if not rs.IsCurvePlanar(curve1) or not rs.IsCurvePlanar(curve2):
        errors.append("Error: One or more of the input curves is not planar.")
        error=True
    if rs.IsCurvePeriodic(curve1) or rs.IsCurvePeriodic(curve2):
        errors.append("Error: This script only works with open curves")
        error=True
    if len(pts1)!=len(pts2):
        errors.append("Error: Input curves need to have same amount of control points")
        error=True
    if rs.CurveDegree(curve1) != rs.CurveDegree(curve2):
        errors.append("Error: Input curves need to be of same degree")
        error=True
    if error:
        for err in errors:
            print err
        rs.UnlockObject(curve1)
        return

    top=0
    right=0
    front=0
    if rs.CurvePlane(curve1).ZAxis[2]!=0:#top view curve
        top=1

    if rs.CurvePlane(curve2).ZAxis[2]!=0:#top view curve
        top=2

    if rs.CurvePlane(curve1).ZAxis[0]!=0:#right view curve
        right=1

    if rs.CurvePlane(curve2).ZAxis[0]!=0:#right view curve
        right=2

    if rs.CurvePlane(curve1).ZAxis[1]!=0:#front view curve
        front=1

    if rs.CurvePlane(curve2).ZAxis[1]!=0:#front view curve
        front=2


    pts3=[]#array to store the points for the new curve
    if top==1 and right==2:
        for i in range(0,len(pts1)):
            pts1[i][2] = pts2[i][2]
            pts1[i][1] = (pts1[i][1]+pts2[i][1])/2 #average out y-coordinate of each point
            pts3.append(pts1[i])
    if top==2 and right==1:
        for i in range(0,len(pts1)):
            pts2[i][2] = pts1[i][2]
            pts2[i][1] = (pts1[i][1]+pts2[i][1])/2 #average out y-coordinate of each point
            pts3.append(pts2[i])
    if top==1 and front==2:
        for i in range(0,len(pts1)):
            pts1[i][2] = pts2[i][2]
            pts1[i][0] = (pts1[i][0]+pts2[i][0])/2 #average out x-coordinate of each point
            pts3.append(pts1[i])
    if top==2 and front==1:
        for i in range(0,len(pts1)):
            pts2[i][2] = pts1[i][2]
            pts2[i][0] = (pts1[i][0]+pts2[i][0])/2 #average out x-coordinate of each point
            pts3.append(pts2[i])
    rs.UnlockObject(curve1)

    if (right==0 and front==0) or (top==0 and right==0) or (top==0 and front==0):
        print "Error: Curves need to be placed on orthogonal views"
        return
    else:

        rs.AddCurve(pts3,degree1)

if __name__ == '__main__':
    Crv2ViewLoose()