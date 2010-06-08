import numpy as N
import  pylab
import scipy.sandbox.delaunay as D
#import numpy.core.ma as ma
import matplotlib.numerix.ma as ma
from matplotlib.ticker import NullFormatter, MultipleLocator,MaxNLocator
from scipy.signal.signaltools import convolve2d
import scriptutil as SU
import re
import readicp
from matplotlib.ticker import FormatStrFormatter




def plot_nodes(tri):
    for nodes in tri.triangle_nodes:
        D.fill(x[nodes],y[nodes],'b')
    pylab.show()

def plot_data(xa,ya,za,fig,nfig,colorflag=False,convolveflag=False):

    cmap = pylab.cm.jet
    cmap.set_bad('w', 1.0)
    myfilter=N.array([[0.1,0.2,0.1],[0.2,0.8,0.2],[0.1,0.2,0.1]],'d') /2.0
    if convolveflag:
        zout=convolve2d(za,myfilter,mode='same') #to convolve, or not to convolve...
    else:
        zout=za
    zima = ma.masked_where(N.isnan(zout),zout)


    ax=fig.add_subplot(2,2,nfig)
    pc=ax.pcolormesh(xa,ya,zima,shading='interp',cmap=cmap)  # working good!
#    pc=ax.imshow(zima,interpolation='bilinear',cmap=cmap)
    
    pmin=zima.min()
    pmax=zima.max()
    pmin=0
    pmax=700
    #pc.set_clim(0.0,660.0)
    pc.set_clim(pmin,pmax)



    if colorflag:
        #g=pylab.colorbar(pc,ticks=N.arange(0,675,100))
        g=pylab.colorbar(pc,ticks=N.arange(pmin,pmax,100))
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



def readmeshfiles(mydirectory,myfilebase,myend,eflag='hhl'):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readicp.datareader()
    Qx=N.array([])
    Qy=N.array([])
    Qz=N.array([])
    
    Counts=N.array([])
    mon0=240000.0
    for currfile in flist:
        print currfile
        mydata=mydatareader.readbuffer(currfile)
        mon=mydata.header['count_info']['monitor']
        Qx=N.concatenate((Qx,N.array(mydata.data['Qx'])))
        Qy=N.concatenate((Qy,N.array(mydata.data['Qy'])))
        Qz=N.concatenate((Qz,N.array(mydata.data['Qz'])))
        Counts=N.concatenate((Counts,N.array(mydata.data['Counts'])*mon0/mon))
    if eflag=='hhl':
        xa,ya,za=prep_data2(Qx,Qz,Counts)
    elif eflag=='hkk':
        xa,ya,za=prep_data2(Qy,Qx,Counts)
    elif eflag=='hkh':
        xa,ya,za=prep_data2(Qx,Qy,Counts)
    return xa,ya,za



def plotcartoon(fig):
    #ax=pylab.subplot(2,2,2)
    ax=fig.add_subplot(2,2,4)

    # 1 1 0
    x1=N.array([4])
    y1=N.array([0])
    ax.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
    s=r'$\delta \delta 0$'
    ax.text(4.8,0.0,s,fontsize=20)

    # -1 -1 0
    x1=N.array([-4])
    y1=N.array([0])
    ax.plot(x1,y1,'bo',markersize=20,markerfacecolor='blue',markeredgecolor='blue')
    s=r'$\bar{\delta} \bar{\delta} 0$'
    ax.text(-7.2,0.0,s,fontsize=20)

    # 1 0 1
    x1=N.array([2])
    y1=N.array([4])
    ax.plot(x1,y1,'bo',markersize=5,markerfacecolor='white')
    s=r'$\delta 0 \delta$'
    ax.text(0.5,4.4,s,fontsize=20)


    # 0 -1 1
    x1=N.array([-2])
    y1=N.array([4])
    ax.plot(x1,y1,'bo',markersize=10,markerfacecolor='white')
    s=r'$0 \bar{\delta} \delta$'
    ax.text(-3.0,4.4,s,fontsize=20)


    # 0 1 -1
    x1=N.array([2])
    y1=N.array([-4])
    ax.plot(x1,y1,'bo',markersize=10,markerfacecolor='gray')
    s=r'$0 \delta \bar{\delta}$'
    ax.text(0.5,-6.8,s,fontsize=20)


    # -1 0 -1
    x1=N.array([-2])
    y1=N.array([-4])
    ax.plot(x1,y1,'bo',markersize=5,markerfacecolor='gray')
    s=r'$\bar{\delta} 0 \bar{\delta}$'
    ax.text(-3.0,-6.8,s,fontsize=20)


    ax.axis([-8.0,8.0,-8,8])
    ax.yaxis.set_major_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.text(.96,.90,'(d)',fontsize=18,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes)

    ax.set_xlabel('[1 1 0]')
    ax.set_ylabel('[0 0 1]')




if __name__ == '__main__':
    Nu = 10000
    aspect = 1.0
    mydirectory=r'C:\BiFeO3film\Oct16_2009'
    #myfilebase='cmesh'
    myend='bt9'
    xc,yc,zc=readmeshfiles(mydirectory,'meshc',myend,eflag='hhl') #Rm temp
    xf,yf,zf=readmeshfiles(mydirectory,'meshf',myend,eflag='hkk') #0
    xg,yg,zg=readmeshfiles(mydirectory,'meshg',myend,eflag='hkh') #-1.3
    print 'matplotlib'

    if 1:

        fig=pylab.figure(figsize=(8,8))
        ylim=(.47,.515)
        xlim=(.465,.500)
        #ylabel='E (meV)'
        #xlabel=r'Q$ \ \ (\AA^{-1}$)'
        fig.subplots_adjust(wspace=0.5)
        fig.subplots_adjust(hspace=0.3)
        


    if 1:
        ylabel='(0 0 1)'
        xlabel='(1 1 0)'
        ax,g=plot_data(xc,yc,zc,fig,1,colorflag=True)
        #ax.text(.98,.20,'E=0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        #ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.text(.96,.90,'(a)',fontsize=18,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        #g.ax.ticks=N.arange(0,100,20)
        
    if 1:
        ylabel='(1 0 0)'
        xlabel='(0 1 1)'
        ax,g=plot_data(xf,yf,zf,fig,2,colorflag=True)
        #ax.text(.98,.20,'E=0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        #ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.text(.96,.90,'(b)',fontsize=18,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        #g.ax.ticks=N.arange(0,100,20)
        
    if 1:
        ylabel='(0 1 0)'
        xlabel='(1 0 1)'
        ax,g=plot_data(xg,yg,zg,fig,3,colorflag=True)
        #ax.text(.98,.20,'E=0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        #ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.text(.96,.90,'(c)',fontsize=18,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        #g.ax.ticks=N.arange(0,100,20)
        
    if 1:
        plotcartoon(fig)
    

    if 0:
        ax,g=plot_data(xe,ye,ze,fig,2,colorflag=True)
        ax.text(.98,.20,'E=-1.3 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)

    if 0:
        ax,g=plot_data(xf,yf,zf,fig,3,colorflag=True)
        ax.text(.98,.20,'0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
    if 0:
        ax,g=plot_data(xg,yg,zg,fig,4,colorflag=True)
        ax.text(.98,.20,'1.3 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.yaxis.set_major_locator(MultipleLocator(1))
        ax.yaxis.set_major_formatter(NullFormatter())
        ax.xaxis.set_major_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
    if 0:
        ax,g=plot_data(xh,yh,zh,fig,5,colorflag=True)
        ax.text(.98,.20,'0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        ax.xaxis.set_minor_formatter(NullFormatter())
        ax.set_ylim(ylim); ax.set_xlim(xlim)
        fmt = FormatStrFormatter('%0.3g')  # or whatever
        ax.xaxis.set_major_formatter(fmt)
        ax.xaxis.set_major_locator(MaxNLocator(5))
    if 0:
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


    if 0:
        print 'gca ', fig.gca()
        for im in fig.gca().get_images():
            print im
            im.set_clim(0.0,660.0)
        #pylab.show()
    if 0:
        print 'saving'
        pylab.savefig(r'c:\sqltest\demo.pdf',dpi=150)
        print 'saved'
    if 1:
        pylab.show()
