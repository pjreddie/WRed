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


    ax=fig.add_subplot(1,1,nfig)
    pc=ax.pcolormesh(xa,ya,zima,shading='interp',cmap=cmap)  # working good!
#    pc=ax.imshow(zima,interpolation='bilinear',cmap=cmap)
    
    pmin=zima.min()
    pmax=zima.max()
    #pmin=0
    #pmax=700
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
    #mon0=240000.0
    mon0=65000.0
    for currfile in flist:
        print currfile
        mydata=mydatareader.readbuffer(currfile)
        mon=mydata.header['count_info']['monitor']
        
        o1=N.array([mydata.header['orient1']['h'],mydata.header['orient1']['k'],mydata.header['orient1']['l']])
        o2=N.array([mydata.header['orient2']['h'],mydata.header['orient2']['k'],mydata.header['orient2']['l']])
        o3=N.cross(o1,o2)
        h=N.array(mydata.data['Qx'])
        k=N.array(mydata.data['Qy'])
        l=N.array(mydata.data['Qz'])
        A=N.array([o1,o2,o3]).T
        a_arr=[]
        b_arr=[]
        for i in range(len(h)):
            hkl=N.array([h[i],k[i],l[i]])
            sol=N.linalg.solve(A,hkl)
            a=sol[0]
            b=sol[1]
            a_arr.append(a)
            b_arr.append(b)
            
        
        if eflag=='weird':
            Qx=N.concatenate((Qx,a_arr))
            Qy=N.concatenate((Qy,b_arr))
        else:
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
    elif eflag=='weird':
        xa,ya,za=prep_data2(Qy,Qx,Counts)
        
    return xa,ya,za


if __name__ == '__main__':
    Nu = 10000
    aspect = 1.0
    mydirectory=r'C:\BiFeO3film\Feb25_2010'
    #myfilebase='cmesh'
    myend='bt9'
    xa,ya,za=readmeshfiles(mydirectory,'meshb',myend,eflag='weird') #Rm temp
    #xa,ya,za=readmeshfiles(mydirectory,'mesha',myend,eflag='hkk') #Rm temp
    #xc,yc,zc=readmeshfiles(mydirectory,'meshc',myend,eflag='hhl') #Rm temp
    #xf,yf,zf=readmeshfiles(mydirectory,'meshf',myend,eflag='hkk') #0
    #xg,yg,zg=readmeshfiles(mydirectory,'meshg',myend,eflag='hkh') #-1.3
    print 'matplotlib'
    
    if 1:

        fig=pylab.figure(figsize=(8,8))
        ylim=(.48,.52)
        xlim=(-.02,.02)
        #ylabel='E (meV)'
        #xlabel=r'Q$ \ \ (\AA^{-1}$)'
        fig.subplots_adjust(wspace=0.5)
        fig.subplots_adjust(hspace=0.3)
        


    if 1:
        xlabel='(0 1 -1)'
        ylabel='(1 1 1)'
        ax,g=plot_data(xa,ya,za,fig,1,colorflag=True)
        #ax.text(.98,.20,'E=0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        #ax.xaxis.set_major_formatter(NullFormatter())
        #ax.set_ylim(ylim); ax.set_xlim(xlim)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.text(.96,.90,'(a)',fontsize=18,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='grey')
        #g.ax.ticks=N.arange(0,100,20)
        
    if 1:
        pylab.show()
