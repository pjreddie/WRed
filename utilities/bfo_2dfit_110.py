from __future__ import division
import numpy as N
import  pylab
import scipy.sandbox.delaunay as D
#import numpy.core.ma as ma
import matplotlib.numerix.ma as ma
from matplotlib.ticker import NullFormatter, MultipleLocator,MaxNLocator
from scipy.signal.signaltools import convolve2d
import scriptutil as SU
import re,sys, os,copy
import readicp
from matplotlib.ticker import FormatStrFormatter
from numpy import sqrt, exp
pi=N.pi
from spinwaves.utilities.mpfit.mpfit import mpfit
from utilities.anneal import anneal






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
    mon0=80000.0
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
        return xa,ya,za,Qx,Qz,Counts
    elif eflag=='hkk':
        xa,ya,za=prep_data2(Qy,Qx,Counts)
        return xa,ya,za,Qx,Qy,Counts
    elif eflag=='hkh':
        xa,ya,za=prep_data2(Qx,Qy,Counts)
    return xa,ya,za

def quadform(pmat,x):
    matprod=N.dot(N.dot(x.T,pmat),x)
    return matprod
    

def calc_struct2(p,qx,qy):
    #pfirst=p[0:4]
    pfirst=N.array([p[0],p[1],p[1],p[2]])
    #x1_center,y1_center,x2_center,y2_center,I1,I2,width1,width2
    x1_center,y1_center,x2_center,y2_center,I1,I2=p[3::]
    pmat=N.reshape(pfirst,(2,2))
    #pmat=pmat/N.linalg.det(pmat)
    deltax1=qx-x1_center
    deltay1=qy-y1_center
    delta1=N.array([deltax1,deltay1])
    deltax2=qx-x2_center
    deltay2=qy-y2_center
    delta2=N.array([deltax2,deltay2])
    matprod1=quadform(pmat,delta1)
    matprod2=quadform(pmat,delta2)  
    #print matprod1
    Icalc=I1*N.exp(-matprod1/2)+I2*N.exp(-matprod2/2)
    eigs=N.linalg.eigvals(pmat)
    area=N.pi*N.sqrt(N.absolute(1/eigs[0]/eigs[1]))
    Icalc=Icalc/area
    return N.diagonal(Icalc)

def calc_struct(p,qx,qy):
    #pfirst=p[0:4]
    pfirst=N.array([N.absolute(p[0]),p[1],p[1],N.absolute(p[2])])
    #x1_center,y1_center,x2_center,y2_center,I1,I2,width1,width2
    x1_center,y1_center,x2_center,y2_center,I1,I2=N.absolute(p[3::])
    pmat=N.reshape(pfirst,(2,2))
    Iout=[]
    #pmat=pmat/N.linalg.det(pmat)
    for i in range(len(qx)): 
        deltax1=qx[i]-x1_center
        deltay1=qy[i]-y1_center
        delta1=N.array([deltax1,deltay1])
        deltax2=qx[i]-x2_center
        deltay2=qy[i]-y2_center
        delta2=N.array([deltax2,deltay2])
        matprod1=quadform(pmat,delta1)
        matprod2=quadform(pmat,delta2)  
        Icalc=I1*N.exp(-matprod1/2)+I2*N.exp(-matprod2/2)
        eigs=N.linalg.eigvals(pmat)
        area=N.pi*N.sqrt(N.absolute(1/eigs[0]/eigs[1]))
        #if matprod1<-1e-3:
        #    print 'less'
        #Icalc=Icalc/area
        Iout.append(Icalc)
    #print len(Icalc)
    return N.array(Iout)
    

def cost_func(p,qx,qy,I,Ierr):
    #ycalc=gen_function(p,x)
    Icalc=calc_struct(p,qx,qy)
    dof=len(I)-len(p)
    fake_dof=len(I)
    #print 'chi',(y-ycalc)/err
    return (I-Icalc)/Ierr#/N.sqrt(fake_dof)

def myfunctlin(p, fjac=None,y=None,err=None,qx=None, qy=None):
    # Parameter values are passed in "p"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    return [status, cost_func(p,qx,qy,y,err)]


def max_wrap(p,y,err,qx,qy):
    chimin=(cost_func(p,qx,qy,y,err)).sum()
    dof=len(y)-len(p)
    chimin=chimin/dof if dof>0 else chimin/fake_dof
    return chimin

if __name__ == '__main__':
    Nu = 10000
    aspect = 1.0
    mydirectory=r'C:\BiFeO3film\Jan18_2010'
    #myfilebase='cmesh'
    myend='bt9'
    xc,yc,zc,X,Y,Z=readmeshfiles(mydirectory,'meshd',myend,eflag='hkk') #Rm temp
    #xf,yf,zf=readmeshfiles(mydirectory,'meshf',myend,eflag='hkk') #0
    #xg,yg,zg=readmeshfiles(mydirectory,'meshg',myend,eflag='hkh') #-1.3
    print 'matplotlib'

    #p0=N.array([1,N.radians(60)],'Float64')
    I1=234; I2=270; x1_center=.5; y1_center=.475; x2_center=x1_center; y2_center=.4835
    wid2=1e5
    wid1=2e3
    area=1#pi*N.sqrt(1.0/wid1/wid2)
    area=N.pi*N.sqrt(N.absolute(1/wid1/wid2))
    #I1=I1/area
    #I2=I2/area
    p0=N.array([wid1,0,wid2,x1_center,y1_center,x2_center,y2_center,I1,I2],'Float64')
    ycalc=calc_struct(p0,X,Y)
    if 0:
        xa,ya,za=prep_data2(Y,X,ycalc)
        fig=pylab.figure(figsize=(8,8))
        ax,g=plot_data(xa,ya,za,fig,1,colorflag=True)
        ax,g=plot_data(xc,yc,zc,fig,2,colorflag=True)
        pylab.show()
        sys.exit()
    
    y=Z
    yerr=N.sqrt(Z)
    
    
    parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
    parinfo=[]
    for i in range(len(p0)):
        parinfo.append(copy.deepcopy(parbase))
    for i in range(len(p0)): 
        parinfo[i]['value']=p0[i]
    #parinfo[1]['fixed']=0 #fix slope
    if 0:
        parinfo[3]['fixed']=1 #fix slope
        parinfo[4]['fixed']=1 #fix slope
        parinfo[4]['fixed']=1 #fix slope
        parinfo[6]['fixed']=1 #fix slope
    #parinfo[3]['fixed']=1
    #parinfo[5]['fixed']=1
    if 0:
        parinfo[1]['limited']=[1,1]
        parinfo[1]['limits']=[0,pi*2]
    if 1:
        #for i in range(5,8,2):
        for i in range(3,9,1):
            parinfo[i]['limited']=[1,1]
        #parinfo[3]['limits']=[.49,.51]
        #parinfo[5]['limits']=[.49,.51]
        parinfo[4]['limits']=[.475,.485]
        parinfo[6]['limits']=[.475,.485]
        parinfo[3]['limits']=[.49,.51]
        parinfo[5]['limits']=[.49,.51]
        parinfo[7]['limits']=[100,300]
        parinfo[8]['limits']=[100,300]
    fa = {'y':y, 'err':yerr,
          'qx':X,
          'qy':Y}
    

    
    if 1:
        print 'annealing'
        myschedule='fast'
        #myschedule='simple'
        lowerm=[1e3,-1e5,1e3,   .49,.475,.49,.475,100,100]
        upperm=[1e5,1e5,1e5,.51,.485,.51,.485,300,300]
        h_args=(y,yerr,X,Y)
        p1,jmin=anneal(max_wrap,p0,args=h_args,\
                      schedule=myschedule,lower=lowerm,upper=upperm,\
                      maxeval=1000, maxaccept=None,dwell=200,maxiter=200,feps=1e-2,full_output = 0)
    
    dof=len(y)-len(p1)
    fake_dof=len(y)
    chimin=(cost_func(p1,X,Y,y,yerr)**2).sum()
    chimin=chimin/dof if dof>0 else chimin/fake_dof
    ycalc=calc_struct(p1,X,Y)
    print 'chimin',chimin
    print 'p1',p1    
    
    if 1:
        print 'linearizing'
        m = mpfit(myfunctlin, p1, parinfo=parinfo,functkw=fa) 
        print 'status = ', m.status
        print 'params = ', m.params
        p1=m.params
        covariance=m.covar
    if 0:
        covariance=covariance*chimin #assume our model is good    
        scale=N.abs(p1[0])
        scale_sig=N.sqrt(covariance.diagonal()[0])
        angle=p1[1]
        angle_sig=N.sqrt(covariance.diagonal()[1])
        print 'scale',scale,'scale_sig',scale_sig
        print 'angle',N.degrees(angle),'angle_sig',angle_sig,N.degrees(angle_sig)%360
        
    
    
    #sys.exit()
    if 1:

        fig=pylab.figure(figsize=(8,8))
        ylim=(.47,.515)
        xlim=(.465,.500)
        #ylabel='E (meV)'
        #xlabel=r'Q$ \ \ (\AA^{-1}$)'
        fig.subplots_adjust(wspace=0.5)
        fig.subplots_adjust(hspace=0.3)
        


    if 1:
        ylabel='(1 0 0)'
        xlabel='(0 1 -1)'
        ax,g=plot_data(xc,yc,zc,fig,1,colorflag=True)
        #ax.text(.98,.20,'E=0 KV',fontsize=14,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        #ax.xaxis.set_major_formatter(NullFormatter())
        #ax.set_ylim(ylim); ax.set_xlim(xlim)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.text(.96,.90,'(a)',fontsize=18,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')
        #g.ax.ticks=N.arange(0,100,20)
    if 1:
        xa,ya,za=prep_data2(Y,X,ycalc)
        ax,g=plot_data(xa,ya,za,fig,2,colorflag=True)
        ax.set_ylabel(ylabel)
        ax.set_xlabel(xlabel)
        #ax.xaxis.set_major_formatter(NullFormatter())
        #ax.set_ylim(ylim); ax.set_xlim(xlim)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.text(.96,.90,'(b)',fontsize=18,horizontalalignment='right',verticalalignment='top',transform=ax.transAxes,color='white')

    if 1:
        pylab.show()