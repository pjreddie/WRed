import readncnr3 as readncnr
import numpy as N
import scriptutil as SU
import re
import simple_combine
import copy
import os
import pylab
pi=N.pi
from matplotlib.mlab import griddata



from math import fmod
import numpy

import matplotlib.cbook as cbook
import matplotlib.transforms as transforms
import matplotlib.artist as artist
import matplotlib.patches as patches
from matplotlib.path import Path


class Ring(patches.Patch):
    """
    Ring patch.
    """
    def __str__(self):
        return "Ring(%g,%g,%g,%g)"%(self.r1,self.r2,self.theta1,self.theta2)

    def __init__(self,
                 center=(0,0),
                 r1=0,
                 r2=None,
                 theta1=0,
                 theta2=360,
                 **kwargs
                 ):
        """
        Draw a ring centered at *x*, *y* center with inner radius *r1* and
        outer radius *r2* that sweeps *theta1* to *theta2* (in degrees).

        Valid kwargs are:

        %(Patch)s
        """
        patches.Patch.__init__(self, **kwargs)
        self.center = center
        self.r1, self.r2 = r1,r2
        self.theta1, self.theta2 = theta1,theta2

        # Inner and outer rings are connected unless the annulus is complete
        delta=abs(theta2-theta1)
        if fmod(delta,360)<=1e-12*delta:
            theta1,theta2 = 0,360
            connector = Path.MOVETO
        else:
            connector = Path.LINETO

        # Form the outer ring
        arc = Path.arc(theta1,theta2)

        if r1 > 0:
            # Partial annulus needs to draw the outter ring
            # followed by a reversed and scaled inner ring
            v1 = arc.vertices
            v2 = arc.vertices[::-1]*float(r1)/r2
            v = numpy.vstack([v1,v2,v1[0,:],(0,0)])
            c = numpy.hstack([arc.codes,arc.codes,connector,Path.CLOSEPOLY])
            c[len(arc.codes)]=connector
        else:
            # Wedge doesn't need an inner ring
            v = numpy.vstack([arc.vertices,[(0,0),arc.vertices[0,:],(0,0)]])
            c = numpy.hstack([arc.codes,[connector,connector,Path.CLOSEPOLY]])

        v *= r2
        v += numpy.array(center)
        self._path = Path(v,c)
        self._patch_transform = transforms.IdentityTransform()
    __init__.__doc__ = cbook.dedent(__init__.__doc__) % artist.kwdocd

    def get_path(self):
        return self._path



















def grid(x,y,z):
    xmesh_step=.02
    ymesh_step=.02
    xrange=N.linspace(x.min(),x.max(),37)
    yrange=N.linspace(y.min(),y.max(),68-43)
    print xrange
    print yrange
    print x
    xi,yi=N.mgrid[x.min():x.max():xmesh_step,y.min():y.max():ymesh_step]
    #blah
    # triangulate data
    #tri = D.Triangulation(N.copy(x),N.copy(y))
    #print 'before interpolator'
    ## interpolate data
    #interp = tri.nn_interpolator(z)
    #print 'interpolator reached'
    #zi = interp(xi,yi)
    print xi.shape
    print yi.shape
    zi = griddata(x,y,z,xi,yi)
    return xi,yi,zi

    
    
def readfiles(flist):
    mydatareader=readncnr.datareader()
    Qx=N.array([])
    Qy=N.array([])
    Qz=N.array([])
    Counts=N.array([])
    for currfile in flist:
        #print currfile
        mydata=mydatareader.readbuffer(currfile)
        #print mydata.data.keys()
        a=mydata.metadata['lattice']['a']
        b=mydata.metadata['lattice']['b']
        c=mydata.metadata['lattice']['c']
        Qx=N.concatenate((Qx,N.array(mydata.data['qx'])*2*pi/a))
        Qy=N.concatenate((Qy,N.array(mydata.data['qy'])*2*pi/b))
        Qz=N.concatenate((Qz,N.array(mydata.data['qz'])*2*pi/c))
        Counts=N.concatenate((Counts,N.array(mydata.data['counts'])))
    #xa,ya,za=prep_data2(Qx,Qy,Counts);
    #print 'xa',xa.min(),xa.max()
    #print 'qx',Qx.min(),Qx.max()
        #x,y,z=grid(Qx,Qz,Counts)
    return Qx,Qz,Counts


def findpeaks(qx,qz,q,counts):
    
    qlist=N.linspace(q.min(),q.max(),100)
    counts_out=[]
    for l in range(len(qlist)):
        qsum=0
        q_spaced=qlist[l]
        num_counted=0
        for i in range(len(q)):
                if l>0:
                    if q[i]<=q_spaced and q[i]>qlist[l-1]:
                        qsum=qsum+counts[i]
                        num_counted=num_counted+1
                else:
                    if q[i]<=q_spaced and q[i]>0:
                        qsum=qsum+counts[i]
                        num_counted=num_counted+1
        if num_counted>0:
            counts_out.append(qsum/num_counted)
        else:
            print 'qsum',qsum
            counts_out.append(0)
            
    return qlist,counts_out


if __name__=='__main__':
    myfilebase='SrFeA0'
    mydirectory=r'C:\srfeas\SrFeAsNi\Ni0p08\2009-03-diffraction'
    myend='bt9'
    myfilebaseglob=myfilebase+'*.'+myend
    file_range=(43,69)
    
    #mydirectory=r'C:\srfeas\SrFeAsNi\Ni0p08\2009-04-diffraction'
    #file_range=(35,51)
    #myfilebase='SrFeA0'
    flist=[]
    for i in range(file_range[0],file_range[1]):
        currfile=os.path.join(mydirectory,myfilebase+str(i)+r"."+myend)
        #print 'currfile',currfile
        flist.append(currfile)
    #flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    qx,qz,counts=readfiles(flist)
    x,y,z=grid(qx,qz,counts)
    print qx.shape, qz.shape, counts.shape
    q=N.sqrt(qx**2+qz**2)
    qout,counts_out=findpeaks(qx,qz,q,counts)
    if 0:
        pylab.plot(qout,counts_out,'s')
        pylab.show()
    if 1:
        #QX,QZ=N.meshgrid(qx,qz)
        pylab.contourf(x,y,z,35)#,cmap=pylab.cm.jet)
        pylab.axis('equal')
    
        #pylab.pcolor(qx,qz,counts)
        pylab.colorbar()
        #pylab.show()
    
    if 1:
        axes = pylab.gca()
        # Full ring
        
        #103
        if 0:
            a=5.542
            c=12.231
            h=1.0
            l=3.0
        #Fe2as
        if 1:
            a=3.6379; c=5.9834
            h=1;k=0;l=0
            
        r=N.sqrt((2*pi/a*h)**2+(2*pi/c*l)**2)
        print 'r',r
        delta=.02
        axes.add_patch(Ring(center=(0,0),r1=r-delta, r2=r+delta,theta1=40,theta2=65,
                        fill=True,fc='pink',ec='darkblue',alpha=0.3))
        
        h=1.0;k=0.0;l=1.0
            
        r=N.sqrt((2*pi/a*h)**2+(2*pi/c*l)**2)
        print 'r',r
        delta=.02
        axes.add_patch(Ring(center=(0,0),r1=r-delta, r2=r+delta,theta1=40,theta2=65,
                        fill=True,fc='pink',ec='darkblue',alpha=0.3))
        
        
  #Feas
        if 0:
            a=5.4420; b=6.0278; c=3.3727
            h=2;k=0;l=0
            h=1;k=0;l=1
            h=0;k=1;l=1
            
            r=N.sqrt((2*pi/a*h)**2+(2*pi/b*k)**2+(2*pi/c*l)**2)
            print 'r',r
            delta=.02
            axes.add_patch(Ring(center=(0,0),r1=r-delta, r2=r+delta,theta1=40,theta2=65,
                        fill=True,fc='grey',ec='darkblue',alpha=0.3))      
        
 #Al
        if 1:
            a=4.0592; b=a; c=a
            h=1.0/2;k=1./2;l=1./2
            h=1;k=0;l=0
            #h=2;k=0;l=0
            #h=1.0/2;k=1.0/2;l=1.0/2
            #h=2;k=2;l=2
            
            r=N.sqrt((2*pi/a*h)**2+(2*pi/b*k)**2+(2*pi/c*l)**2)
            print 'r',r
            delta=.02
            axes.add_patch(Ring(center=(0,0),r1=r-delta, r2=r+delta,theta1=40,theta2=65,
                        fill=True,fc='grey',ec='darkblue',alpha=0.3))      

 #FeAs2
        if 1:
            a=5.2684; b=5.9631; c=2.9007
            h=1.0/2;k=1./2;l=1./2
            h=1.0;k=1.0;l=0
            #h=2;k=2;l=2
            
            r=N.sqrt((2*pi/a*h)**2+(2*pi/b*k)**2+(2*pi/c*l)**2)
            print 'r',r
            delta=.02
            axes.add_patch(Ring(center=(0,0),r1=r-delta, r2=r+delta,theta1=40,theta2=65,
                        fill=True,fc='orange',ec='darkblue',alpha=0.5))      

 #SrFe2As2 Ni
        if 1:
            a=5.542; b=5.495; c=12.231
            h=0.0;k=.0;l=3.1 #about right
            #h=0.0;k=.0;l=3.4 #good 
            #h=0.0;k=.0;l=3.6 #good
            #h=0.0;k=.0;l=3.9 # good
            
            #h=1./2;k=1.0/2;l=1.0/2
            #h=2;k=2;l=2
            h=0.0; k=0.0; l=4.0
            r=N.sqrt((2*pi/a*h)**2+(2*pi/b*k)**2+(2*pi/c*l)**2)
            print 'r',r
            delta=.02
            axes.add_patch(Ring(center=(0,0),r1=r-delta, r2=r+delta,theta1=40,theta2=65,
                        fill=True,fc='purple',ec='darkblue',alpha=0.3))      
        
        
        
        pylab.xlim((0.7,1.8))
        pylab.ylim((0.7,1.8))
        #pylab.axis('equal')
        
    if 1:
        pylab.show()

        
