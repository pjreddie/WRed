import numpy as N
import  pylab
import scipy.sandbox.delaunay as D
#import numpy.core.ma as ma
import matplotlib.numerix.ma as ma
from matplotlib.ticker import NullFormatter, MultipleLocator
from scipy.signal.signaltools import convolve2d

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


    ax=fig.add_subplot(3,2,nfig)
    pc=ax.pcolormesh(xa,ya,zima,shading='interp',cmap=cmap)  # working good!
#    pc=ax.imshow(zima,interpolation='bilinear',cmap=cmap)
    pc.set_clim(0.0,80.0)



    if colorflag:
        g=pylab.colorbar(pc,ticks=N.arange(0,100,20))
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

if __name__ == '__main__':
    Nu = 10000
    aspect = 1.0
    xa,ya,za=prep_data(r'c:\resolution_stuff\1p4K.iexy');
    xb,yb,zb=prep_data(r'c:\resolution_stuff\15K.iexy');
    xc,yc,zc=prep_data(r'c:\resolution_stuff\50K.iexy');
    xd,yd,zd=prep_data(r'c:\resolution_stuff\90K.iexy');
    xe,ye,ze=prep_data(r'c:\resolution_stuff\150K.iexy');
    xf,yf,zf=prep_data(r'c:\resolution_stuff\250K.iexy');
    
    print 'matplotlib'



    fig=pylab.figure(figsize=(8,8))

    ylabel='E (meV)'
    xlabel=r'Q$ \ \ (\AA^{-1}$)'
    
 
    
    
    ax,g=plot_data(xa,ya,za,fig,1,colorflag=True)   
    ax.text(.98,.85,'2 K',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_formatter(NullFormatter())    
    #g.ax.ticks=N.arange(0,100,20)
    
    
    ax,g=plot_data(xb,yb,zb,fig,2,colorflag=True)
    ax.text(.98,.85,'15 K',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)
    ax.yaxis.set_major_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(NullFormatter())    
    
    
    
    ax,g=plot_data(xc,yc,zc,fig,3,colorflag=True)
    ax.text(.98,.85,'50 K',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)
    ax.set_ylabel(ylabel)
    ax.xaxis.set_major_formatter(NullFormatter())    

    ax,g=plot_data(xd,yd,zd,fig,4,colorflag=True)
    ax.text(.98,.85,'90 K',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_major_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(NullFormatter())    
    
    ax,g=plot_data(xe,ye,ze,fig,5,colorflag=True)
    ax.text(.98,.85,'150 K',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    
    
    ax,g=plot_data(xf,yf,zf,fig,6,colorflag=True)
    ax.text(.98,.85,'250 K',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)
    ax.set_xlabel(xlabel)
    ax.yaxis.set_major_formatter(NullFormatter())
    
    
    print 'gca ', fig.gca()
    for im in fig.gca().get_images():
        print im
        im.set_clim(0.0,80.0)

    print 'saving'
    pylab.savefig(r'c:\fig3b.pdf',dpi=150)
    print 'saved'
