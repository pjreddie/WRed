import numpy as N
import  pylab
import scipy.sandbox.delaunay as D
#import numpy.core.ma as ma
import matplotlib.numerix.ma as ma
from matplotlib.ticker import NullFormatter, MultipleLocator
from scipy.signal.signaltools import convolve2d
import scriptutil as SU
import re
import readicp
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import MaxNLocator
import linegen
import locator

def plot_nodes(tri):
    for nodes in tri.triangle_nodes:
        D.fill(x[nodes],y[nodes],'b')
    pylab.show()

def plot_data(xa,ya,za,fig,nfig,colorflag=False):

    cmap = pylab.cm.jet
    cmap.set_bad('w', 1.0)   
    myfilter=N.array([[0.1,0.2,0.1],[0.2,0.8,0.2],[0.1,0.2,0.1]],'d') /2.0
    zout=convolve2d(za,myfilter,mode='same')
    zima = ma.masked_where(N.isnan(zout),zout)


    ax=fig.add_subplot(1,1,nfig)
    pc=ax.pcolormesh(xa,ya,zima,shading='interp',cmap=cmap)  # working good!
#    pc=ax.imshow(zima,interpolation='bilinear',cmap=cmap)
    pc.set_clim(0.0,660.0)



    if colorflag:
        g=pylab.colorbar(pc,ticks=N.arange(0,675,100))
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
    xi, yi = N.mgrid[-5:5:100j,-5:5:100j]
    xi,yi=N.mgrid[x.min():x.max():.001,y.min():y.max():.001]
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
    return xi,yi,zi    



def readmeshfiles(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readicp.datareader()
    Qx=N.array([])
    Qy=N.array([])
    Qz=N.array([])
    Counts=N.array([])
    for currfile in flist:
        print currfile
        mydata=mydatareader.readbuffer(currfile)
        Qx=N.concatenate((Qx,N.array(mydata.data['Qx'])))
        Qy=N.concatenate((Qy,N.array(mydata.data['Qy'])))
        Qz=N.concatenate((Qz,N.array(mydata.data['Qz'])))
        Counts=N.concatenate((Counts,N.array(mydata.data['Counts'])))
    xa,ya,za=prep_data2(Qx,Qy,Counts);
    return xa,ya,za



def readmeshfiles_direct(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readicp.datareader()
    Qx=N.array([])
    Qy=N.array([])
    Qz=N.array([])
    Counts=N.array([])
    for currfile in flist:
        print currfile
        mydata=mydatareader.readbuffer(currfile)
        Qx=N.concatenate((Qx,N.array(mydata.data['Qx'])))
        Qy=N.concatenate((Qy,N.array(mydata.data['Qy'])))
        Qz=N.concatenate((Qz,N.array(mydata.data['Qz'])))
        Counts=N.concatenate((Counts,N.array(mydata.data['Counts'])))
    #xa,ya,za=prep_data2(Qx,Qy,Counts);
    return Qx,Qy,Counts





if __name__ == '__main__':
    Nu = 10000
    aspect = 1.0
    mydirectory=r'c:\bifeo3xtal\dec7_2007'
    myfilebase='cmesh'
    myend='bt9'
    xd,yd,zd=readmeshfiles(mydirectory,'dmesh',myend) #0

    if 1:

        fig=pylab.figure(figsize=(8,8))
        ylim=(.485,.515)
        xlim=(.485,.515)
        xlabel='(1 1 0)'
        ylabel='(1 -1 -2)'
     
        
    if 1:    
        ax,g=plot_data(xd,yd,zd,fig,1,colorflag=True)   
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.set_ylim(ylim); ax.set_xlim(xlim)  
        

    
    if 1:
        point1=(.514,.494)
        point2=(.492,.51)
        xt,yt,zorigt=readmeshfiles(mydirectory,'dmesh',myend) #0        
        myline=linegen.line_interp(point1,point2,divisions=50)
        xout,yout,zout=myline.interp(xt,yt,zorigt)
        line_x=myline.line_x; line_y=myline.line_y 
        pylab.plot(line_x,line_y,'red',linewidth=3.0)
        ax.set_ylim(ylim); ax.set_xlim(xlim)  
    

    
    if 0:
        xt,yt,zorigt=readmeshfiles(mydirectory,'dmesh',myend) #0
        xout,yout,zout=myline.interp(xt,yt,zorigt)
        
    if 1:    
        print 'gca ', fig.gca()
        for im in fig.gca().get_images():
            print im
            im.set_clim(0.0,660.0)
        #pylab.show()
        
    if 1:
        fig2=pylab.figure(figsize=(8,8))
        pylab.plot(xout,zout,'s')
        #pylab.plot(xi,zi,'red',linewidth=3.0)
        #ax.set_ylim(ylim); ax.set_xlim(xlim)
        pylab.show()  
    if 0:
        print 'saving'
        pylab.savefig(r'c:\sqltest\demo.pdf',dpi=150)
        print 'saved'
