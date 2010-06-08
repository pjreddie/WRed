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


    ax=fig.add_subplot(4,2,nfig)
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







if __name__ == '__main__':
    Nu = 10000
    aspect = 1.0
    mydirectory=r'c:\bifeo3xtal\dec7_2007'
    myfilebase='cmesh'
    myend='bt9'
    xc,yc,zc=readmeshfiles(mydirectory,'cmesh',myend) #Rm temp
    xd,yd,zd=readmeshfiles(mydirectory,'dmesh',myend) #0
    xe,ye,ze=readmeshfiles(mydirectory,'emesh',myend) #-1.3
    xf,yf,zf=readmeshfiles(mydirectory,'fmesh',myend) #0
    xg,yg,zg=readmeshfiles(mydirectory,'gmesh',myend) #1.3
    xh,yh,zh=readmeshfiles(mydirectory,'hmesh',myend) #0
    xi,yi,zi=readmeshfiles(mydirectory,'imesh',myend) #-1.3
    xj,yj,zj=readmeshfiles(mydirectory,'jmesh',myend) #0
    print 'matplotlib'

    if 1:

        fig=pylab.figure(figsize=(8,8))
        ylim=(.485,.515)
        xlim=(.485,.515)
        #ylabel='E (meV)'
        #xlabel=r'Q$ \ \ (\AA^{-1}$)'
        xlabel='(1 1 0)'
        ylabel='(1 -1 -2)'


    if 1:
        ax,g=plot_data(xd,yd,zd,fig,1,colorflag=True)
        ax.text(.98,.20,'E=0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        #g.ax.ticks=N.arange(0,100,20)

    if 1:
        ax,g=plot_data(xe,ye,ze,fig,2,colorflag=True)
        ax.text(.98,.20,'E=-1.3 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)

    if 1:
        ax,g=plot_data(xf,yf,zf,fig,3,colorflag=True)
        ax.text(.98,.20,'0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
    if 1:
        ax,g=plot_data(xg,yg,zg,fig,4,colorflag=True)
        ax.text(.98,.20,'1.3 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
    if 1:
        ax,g=plot_data(xh,yh,zh,fig,5,colorflag=True)
        ax.text(.98,.20,'0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        fmt = FormatStrFormatter('%0.3g')  # or whatever
        ax.xaxis.set_major_formatter(fmt)
        ax.xaxis.set_major_locator(MaxNLocator(5))
    if 1:
        ax,g=plot_data(xi,yi,zi,fig,6,colorflag=True)
        ax.text(.98,.20,'-1.3 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_xlabel(xlabel)
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        fmt = FormatStrFormatter('%0.3g')  # or whatever
        ax.xaxis.set_major_formatter(fmt)
        ax.xaxis.set_major_locator(MaxNLocator(5))

    if 0:
        ax,g=plot_data(xf,yf,zf,fig,6,colorflag=True)
        ax.text(.98,.20,'0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_xlabel(xlabel)
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        #fmt = FormatStrFormatter('%1.4g')  # or whatever
        #ax.yaxis.set_major_formatter(fmt)


    if 1:
        print 'gca ', fig.gca()
        for im in fig.gca().get_images():
            print im
            im.set_clim(0.0,660.0)
        #pylab.show()
    if 0:
        print 'saving'
        pylab.savefig(r'c:\sqltest\fields.pdf',dpi=150)
        print 'saved'
    if 1:
        pylab.show()
