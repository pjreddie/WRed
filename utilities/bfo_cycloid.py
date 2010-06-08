from __future__ import division
import numpy
from enthought.mayavi import mlab

def f(x,y,z):
    r = numpy.sqrt(x**2 + y**2 + z**4)
    u = y*numpy.sin(r)/(r+0.001)
    v = -x*numpy.sin(r)/(r+0.001)
    w = numpy.zeros_like(z)
    return (u,v,w)

def genvec(vec):
    vmag=numpy.sqrt(vec[0]**2+vec[1]**2+vec[2]**2); vec=vec/vmag
    return vec

def spiral(x,y,z):
    A=1
    bas1=genvec([1,1,-2])
    bas2=genvec([1,1,1])
    k=genvec([1,-1,0])
    r=numpy.array([x,y,z],'float64')
    u = A*(bas1[0]*numpy.cos(numpy.dot(k,r))+bas2[0]*numpy.sin(numpy.dot(k,r)))
    v = A*(bas1[1]*numpy.cos(numpy.dot(k,r))+bas2[1]*numpy.sin(numpy.dot(k,r)))
    w = A*(bas1[2]*numpy.cos(numpy.dot(k,r))+bas2[2]*numpy.sin(numpy.dot(k,r)))
    return (u,v,w)

def amplitude(x,y,z):
    A=1
    bas1=genvec([1,1,-2])
    bas2=genvec([1,1,1])
    k=genvec([1,-1,0])
    r=numpy.array([x,y,z],'float64')
    u = A*(bas1[0]*numpy.cos(numpy.dot(k,r))+bas2[0]*numpy.cos(numpy.dot(k,r)))
    v = A*(bas1[1]*numpy.cos(numpy.dot(k,r))+bas2[1]*numpy.cos(numpy.dot(k,r)))
    w = A*(bas1[2]*numpy.cos(numpy.dot(k,r))+bas2[2]*numpy.cos(numpy.dot(k,r)))
    return (u,v,w)


@mlab.show
def test_quiver3d():
    fig=mlab.figure(fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))
    x, y, z = numpy.mgrid[-2:3, -2:3, -2:3]  
    print 'almost'
    #mlab.quiver3d(x, y, z,f, line_width=3, scale_factor=1,figure=fig)
    
    d=0.2
    x=d*numpy.arange(0,25)
    y=-d*numpy.arange(0,25)
    z=numpy.zeros(len(x))
    if 0:
        func=spiral
    if 1:
        func=amplitude
    mlab.quiver3d(x, y, z,func, line_width=3, scale_factor=1,figure=fig)
    outline=mlab.outline(figure=fig,extent=[-1,1,-1,1,-1,1])
    mlab.orientation_axes(figure=fig,xlabel='a',ylabel='b',zlabel='c')
    print 'done'
    


if __name__=="__main__":   
    if 1:
        #pass
        test_quiver3d()
    if 0:
        d=0.2
        x=d*numpy.arange(0,100)
        y=-d*numpy.arange(0,100)
        z=numpy.zeros(len(x))
        u,v,w=spiral(x,y,z)
        print u,v,w
    