
## PointRotate.py Version 1.02
## Copyright (c) 2006 Bruce Vaughan, BV Detailing & Design, Inc.
## All rights reserved.
## NOT FOR SALE. The software is provided "as is" without any warranty.
#############################################################################
"""
    Return a point rotated about an arbitrary axis in 3D.
    Positive angles are counter-clockwise looking down the axis toward the origin.
    The coordinate system is assumed to be right-hand.
    Arguments: 'axis point 1', 'axis point 2', 'point to be rotated', 'angle of rotation (in radians)' >> 'new point'
    Revision History:
        Version 1.01 (11/11/06) - Revised function code
        Version 1.02 (11/16/06) - Rewrote PointRotate3D function

    Reference 'Rotate A Point About An Arbitrary Axis (3D)' - Paul Bourke        
"""

import numpy as np
from numpy import cos,sin, sqrt
    

def PointRotate3D(p1, p2, p0, theta):


    # Translate so axis is at origin    
    p = p0 - p1
    # Initialize point q
    q = np.array([0.0,0.0,0.0],'Float64')
    N = (p2-p1)
    Nm = sqrt(N[0]**2 + N[1]**2 + N[2]**2)
    
    # Rotation axis unit vector
    n = np.array([N[0]/Nm, N[1]/Nm, N[2]/Nm],'Float64')

    # Matrix common factors     
    c = cos(theta)
    t = (1 - cos(theta))
    s = sin(theta)
    X = n[0]
    Y = n[1]
    Z = n[2]

    # Matrix 'M'
    d11 = t*X**2 + c
    d12 = t*X*Y - s*Z
    d13 = t*X*Z + s*Y
    d21 = t*X*Y + s*Z
    d22 = t*Y**2 + c
    d23 = t*Y*Z - s*X
    d31 = t*X*Z - s*Y
    d32 = t*Y*Z + s*X
    d33 = t*Z**2 + c

    #            |p.x|
    # Matrix 'M'*|p.y|
    #            |p.z|
    q[0] = d11*p[0] + d12*p[1] + d13*p[2]
    q[1] = d21*p[0] + d22*p[1] + d23*p[2]
    q[2] = d31*p[0] + d32*p[1] + d33*p[2]

    # Translate axis and rotated point back to original location    
    return q + p1
    
## END PointRotate3D() ##########################

if __name__ == '__main__':
    p1=np.array([0,0,0],'Float64')
    p2=np.array([1,1,1],'Float64')
    p0=np.array([1,1,-2],'Float64')
    theta=np.radians(120)
    pout=PointRotate3D(p1, p2, p0, theta)
    print pout
    theta=np.radians(120*2)
    pout=PointRotate3D(p1, p2, p0, theta)
    print pout
    #theta=np.radians(90)
    #pout=PointRotate3D(p1, p2, p0, theta)
    #print pout