import numpy as N
import  pylab
import scipy.sandbox.delaunay as D
#import numpy.core.ma as ma
import matplotlib.numerix.ma as ma
from matplotlib.ticker import NullFormatter, MultipleLocator
from scipy.signal.signaltools import convolve2d
import scriptutil as SU
import re
import readncnr2 as readncnr
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator
import linegen
import locator
ctop=350.0
cstep=50
xmesh_step=2e-3
ymesh_step=1e-3
smooth=False
interpolate_on=True

def plot_nodes(tri):
    for nodes in tri.triangle_nodes:
        D.fill(x[nodes],y[nodes],'b')
    pylab.show()

def plot_data(xa,ya,za,fig,nfig,colorflag=False):

    cmap = pylab.cm.jet
    cmap.set_bad('w', 1.0)   
    myfilter=N.array([[0.1,0.2,0.1],[0.2,0.8,0.2],[0.1,0.2,0.1]],'d') /2.0
    if smooth:
        zout=convolve2d(za,myfilter,mode='same')
    else:
        zout=za
    zima = ma.masked_where(N.isnan(zout),zout)


    ax=fig.add_subplot(1,1,nfig)
    pc=ax.pcolormesh(xa,ya,zima,shading='interp',cmap=cmap)  # working good!
#    pc=ax.imshow(zima,interpolation='bilinear',cmap=cmap)
    pc.set_clim(0.0,ctop)



    if colorflag:
        g=pylab.colorbar(pc,ticks=N.arange(0,ctop,cstep))
        print g
        #g.ticks=None
        #gax.yaxis.set_major_locator(MultipleLocator(40))
        #g.ticks(N.array([0,20,40,60,80]))

    return ax,g

def prep_data(filename):
#    Data=pylab.load(r'c:\resolution_stuff\1p4K.iexy')
    Data=pylab.load(filename)
    xt=Data[:,2]
    yt=Data[:,3]
    zorigt=Data[:,0]
    x=xt[:,zorigt>0.0]
    y=yt[:,zorigt>0.0]
    z=zorigt[:,zorigt>0.0]
#    zorig=ma.array(zorigt)
    print 'reached'
    threshold=0.0;
#    print zorigt < threshold
#    print N.isnan(zorigt)
#    z = ma.masked_where(zorigt < threshold , zorigt)
    print 'where masked ', z.shape
#should be commented out--just for testing
##    x = pylab.randn(Nu)/aspect
##    y = pylab.randn(Nu)
##    z = pylab.rand(Nu)
##    print x.shape
##    print y.shape
    # Grid
    xi, yi = N.mgrid[-5:5:100j,-5:5:100j]
    xi,yi=N.mgrid[x.min():x.max():.05,y.min():y.max():.05]
    # triangulate data
    tri = D.Triangulation(x,y)
    print 'before interpolator'
    # interpolate data
    interp = tri.nn_interpolator(z)
    print 'interpolator reached'
    zi = interp(xi,yi)
    # or, all in one line
    #    zi = Triangulation(x,y).nn_interpolator(z)(xi,yi)
#    return x,y,z
    if interpolate_on==False:
        xi=x
        yi=y
        zi=z
        
    return xi,yi,zi    





def prep_data2(xt,yt,zorigt):
#    Data=pylab.load(r'c:\resolution_stuff\1p4K.iexy')
    #Data=pylab.load(filename)
    #xt=Data[:,2]
    #yt=Data[:,3]
    #zorigt=Data[:,0]
    x=xt[:,zorigt>0.0]
    y=yt[:,zorigt>0.0]
    z=zorigt[:,zorigt>0.0]
#    zorig=ma.array(zorigt)
    print 'reached'
    threshold=0.0;
#    print zorigt < threshold
#    print N.isnan(zorigt)
#    z = ma.masked_where(zorigt < threshold , zorigt)
    print 'where masked ', z.shape
#should be commented out--just for testing
##    x = pylab.randn(Nu)/aspect
##    y = pylab.randn(Nu)
##    z = pylab.rand(Nu)
##    print x.shape
##    print y.shape
    # Grid
    print x.min()
    print x.max()
    print y.min()
    print y.max()
    print x.shape
    xi,yi=N.mgrid[x.min():x.max():xmesh_step,y.min():y.max():ymesh_step]
    #blah
    # triangulate data
    tri = D.Triangulation(N.copy(x),N.copy(y))
    print 'before interpolator'
    # interpolate data
    interp = tri.nn_interpolator(z)
    print 'interpolator reached'
    zi = interp(xi,yi)
    # or, all in one line
    #    zi = Triangulation(x,y).nn_interpolator(z)(xi,yi)
#    return x,y,z
    if interpolate_on==False:
        #print "off"
        #print xi.shape
        #print N.reshape(x,(15,31))
        xi=N.reshape(x,(15,31))
        yi=N.reshape(y,(15,31))
        zi=N.reshape(z,(15,31))
        #print zi2-zi
        #blah
        print "interpolation off"
    return xi,yi,zi    



def readmeshfiles(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readncnr.datareader()
    Qx=N.array([])
    Qy=N.array([])
    Qz=N.array([])
    Counts=N.array([])
    for currfile in flist:
        print currfile
        mydata=mydatareader.readbuffer(currfile)
        Qx=N.concatenate((Qx,N.array(mydata.data['qx'])))
        Qy=N.concatenate((Qy,N.array(mydata.data['qy'])))
        Qz=N.concatenate((Qz,N.array(mydata.data['qz'])))
        Counts=N.concatenate((Counts,N.array(mydata.data['counts'])))
        
    #print Qx
    #print Qy
    #print Counts
    xa,ya,za=prep_data2(Qx,Qz,Counts)
    return xa,ya,za



def readmeshfiles_direct(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readncnr.datareader()
    Qx=N.array([])
    Qy=N.array([])
    Qz=N.array([])
    Counts=N.array([])
    for currfile in flist:
        print currfile
        mydata=mydatareader.readbuffer(currfile)
        Qx=N.concatenate((Qx,N.array(mydata.data['qx'])))
        Qy=N.concatenate((Qy,N.array(mydata.data['qy'])))
        Qz=N.concatenate((Qz,N.array(mydata.data['qz'])))
        Counts=N.concatenate((Counts,N.array(mydata.data['counts'])))
    #xa,ya,za=prep_data2(Qx,Qy,Counts);
    return Qx,Qz,Counts





if __name__ == '__main__':
    Nu = 10000
    aspect = 1.0
    mydirectory=r'c:\ca3comno6\Feb1_2008'
    myfilebase='nmesh*'
    myfilebase1='nmesh*'
    myend='bt9'
    xd,yd,zd=readmeshfiles(mydirectory,myfilebase,myend)
    #xa,ya,za=readmeshfiles(mydirectory,myfilebase2,myend)
    #zd=zd+za
#    xd,yd,zd=readmeshfiles(mydirectory,myfilebase,myend) #0

    if 1:

        fig=pylab.figure(figsize=(8,8))
        ylim=(yd.min(),yd.max())
        xlim=(xd.min(),xd.max())
        xlabel='(1 0 0)'
        ylabel='(0 0 1)'
        
    if 1:    
        ax,g=plot_data(xd,yd,zd,fig,1,colorflag=True)   
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.set_ylim(ylim); ax.set_xlim(xlim)  
        

    
    if 1:
        #point1=(1.0,1.0)
        #point2=(1.025,1.025)
        point1=(.955,.97)
        point2=(1.045,1.03)
        xt2,yt2,zorigt2=readmeshfiles(mydirectory,myfilebase,myend) #0        
        #xa2,ya2,za2=readmeshfiles(mydirectory,myfilebase2,myend)
        zorigt2=zorigt2#+za2

        myline=linegen.line_interp(point1,point2,divisions=50)
        xout,yout,zout=myline.interp(xt2,yt2,zorigt2)
        print 'slope=',myline.slope
        print 'intercept=',myline.intercept
        line_x=myline.line_x; line_y=myline.line_y 
        pylab.plot(line_x,line_y,'red',linewidth=3.0)
        ax.set_ylim(ylim); ax.set_xlim(xlim)  
        #ax.square()
        ax.set_aspect('equal', 'datalim')
    
    if 0:
        xt,yt,zorigt=readmeshfiles(mydirectory,'dmesh',myend) #0
        xout,yout,zout=myline.interp(xt,yt,zorigt)
        
    if 1:    
        print 'gca ', fig.gca()
        for im in fig.gca().get_images():
            print im
            im.set_clim(0.0,400.0)
        #pylab.show()
        
    if 0:
        fig2=pylab.figure(figsize=(8,8))
        pylab.plot(xout,zout,'s')
        #pylab.plot(xi,zi,'red',linewidth=3.0)
        #ax.set_ylim(ylim); ax.set_xlim(xlim)
        pylab.show()
    
    if 1:
        pylab.show()  
    if 0:
        print 'saving'
        pylab.savefig(r'c:\ca3comno6\feb1_2008\demo.pdf',dpi=150)
        print 'saved'
