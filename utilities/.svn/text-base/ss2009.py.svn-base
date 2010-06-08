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
import matplotlib.ticker as ticker
import sys
from numpy import ma
from mpfit import mpfit
from scipy.optimize import curve_fit
from findpeak3 import findpeak
from openopt import NLP
import scipy.optimize
import scipy.odr



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
    xmesh_step=.1
    ymesh_step=.5
    #mxrange=N.linspace(x.min(),x.max(),100)
    #yrange=N.linspace(y.min(),y.max(),100)
    #print xrange
    #print yrange
    #print x
    xi,yi=N.mgrid[x.min():x.max():xmesh_step,y.min():y.max():ymesh_step]
    #blah
    # triangulate data
    #tri = D.Triangulation(N.copy(x),N.copy(y))
    #print 'before interpolator'
    ## interpolate data
    #interp = tri.nn_interpolator(z)
    #print 'interpolator reached'
    #zi = interp(xi,yi)
    print 'xi',xi.shape
    print yi.shape
    zm=ma.masked_where(z<3000,z)
    x=copy.deepcopy(x[:,z<500.0])
    y=copy.deepcopy(y[:,z<500.0])
    z=copy.deepcopy(z[:,z<500.0])
    zi = griddata(x,y,z,xi,yi)
    print 'zi',zi.shape
    print xi
    print yi
    return xi,yi,zi

    
    
def readfiles(flist,mon0=None):
    mydatareader=readncnr.datareader()
    #Qx=N.array([])
    #Qy=N.array([])
    #Qz=N.array([])
    #tth=N.array([])
    #Counts=N.array([])
    #T=N.array([])
    e=[]
    Counts=[]
    Counts_err=[]
    l=[]
    i=0
    for currfile in flist:
        #print currfile
        mydata=mydatareader.readbuffer(currfile)
        #print mydata.data.keys()
        if i==0:
            if mon0==None:
                mon0=mydata.data['monitor'][0]
                #mon0=mydata.metadata['count_info']['monitor']
        #a=mydata.metadata['lattice']['a']
        #b=mydata.metadata['lattice']['b']
        #c=mydata.metadata['lattice']['c']
        #mon=mydata.metadata['count_info']['monitor']
        mon=mydata.data['monitor'][0]
        e.append(N.array(mydata.data['e']))
        Counts.append(N.array(mydata.data['detector'])*mon0/mon)
        Counts_err.append(N.sqrt(N.array(mydata.data['detector']))*mon0/mon)
        l.append(N.array(mydata.data['qz']))
        #T.append(N.array(mydata.data['temp'])) #What we probably want
        #Tave=N.array(mydata.data['temp']).mean()
        #T.append(N.ones(tth[i].size)*Tave)
        #Qx=N.concatenate((Qx,N.array(mydata.data['qx'])*2*pi/a))
        #Qy=N.concatenate((Qy,N.array(mydata.data['qy'])*2*pi/b))
        #Qz=N.concatenate((Qz,N.array(mydata.data['qz'])*2*pi/c))
        #tth=N.concatenate((tth,N.array(mydata.data['a4'])))
        #Counts=N.concatenate((Counts,N.array(mydata.data['counts'])*mon0/mon))
        #T=N.concatenate((T,N.array(mydata.data['temp'])))
        
        i=i+1
    #xa,ya,za=prep_data2(Qx,Qy,Counts);
    #print 'xa',xa.min(),xa.max()
    #print 'qx',Qx.min(),Qx.max()
        #x,y,z=grid(Qx,Qz,Counts)
    return e,l,Counts,Counts_err,mon0



def regrid(x,y,z):
    print len(x)
    currmax=x[0].max()
    currmin=x[0].min()
    for currx in x:
        currmax=max([currx.max(),currmax])
        currmin=min([currx.min(),currmin])
    
    step=N.abs(x[0][0]-x[0][1])
    print currmin, currmax,step
    proto_x=N.arange(currmin,currmax+step,step)
    print 'proto', proto_x
    for i in range(len(x)):
        currx=x[i]
        curry=y[i]
        currz=z[i]
        if len(currx)<len(proto_x):
            lendiff=len(proto_x)-len(currx)
            lenorig=len(x[i])
            x[i]=copy.deepcopy(proto_x)
            newy=N.array(proto_x[:])
            newy[:lenorig]=curry[:]
            newy[lenorig:]=N.ones(lendiff)*curry[-1] #set padded temps to the same value as the end of the actual array
            newz=ma.array(copy.deepcopy(proto_x[:]))
            newz[:lenorig]=currz[:]
            newz[lenorig:]=N.ones(lendiff)*N.nan #set padded counts to nan
            y[i]=copy.deepcopy(newy)
            z[i]=copy.deepcopy(newz)
            #print "min", x[i].min()
            
            
            
            
        
    #sys.exit()
    x=N.array(x).flatten()
    y=N.array(y).flatten()
    z=N.array(z).flatten()
    return x,y,z





def regrid2(x,y,z):
    print len(x)
    currmax=x[0].max()
    currmin=x[0].min()
    for currx in x:
        currmax=max([currx.max(),currmax])
        currmin=min([currx.min(),currmin])
    
    step=N.abs(x[0][0]-x[0][1])
    print currmin, currmax,step
    proto_x=N.arange(currmin,currmax+step,step)
    print 'proto', proto_x
    for i in range(len(x)):
        currx=x[i]
        curry=y[i]
        currz=z[i]
        if len(currx)<len(proto_x):
            lendiff=len(proto_x)-len(currx)
            lenorig=len(x[i])
            x[i]=copy.deepcopy(proto_x)
            newy=N.array(proto_x[:])
            newy[:lenorig]=curry[:]
            newy[lenorig:]=N.ones(lendiff)*curry[-1] #set padded temps to the same value as the end of the actual array
            newz=ma.array(copy.deepcopy(proto_x[:]))
            newz[:lenorig]=currz[:]
            newz_mask=N.zeros(newz.shape)
            newz[lenorig:]=N.ones(lendiff)*N.nan #set padded counts to nan
            newz_mask[lenorig:]=N.ones(lendiff)  #mask these values
            newz.mask=newz_mask
            y[i]=copy.deepcopy(newy)
            z[i]=copy.deepcopy(newz)
            #print "min", x[i].min()
        else:
            newz=ma.array(copy.deepcopy(proto_x[:]))
            newz[:]=currz[:]
            newz_mask=N.zeros(newz.shape)
            newz.mask=newz_mask
            z[i]=copy.deepcopy(newz)
            
            
            
            
        
    #sys.exit()
    #x=N.array(x).flatten()
    #y=N.array(y).flatten()
    #z=N.array(z).flatten()
    return x,y,z


def fitpeak(x,y,yerr):
    maxval=x.max()
    minval=x.min()
    diff=y.max()-y.min()-y.mean()
    sig=y.std()
    print 'diff',diff,'std',sig
    if diff-1*sig>0:
        #the difference between the high and low point and
        #the mean is greater than 3 sigma so we have a signal
        p0=findpeak(x,y,2)
        print 'p0',p0
        #Area center width Bak area2 center2 width2
        center1=p0[0]
        width1=p0[1]
        center2=p0[2]
        width2=p0[3]
        sigma=width/2/N.sqrt(2*N.log(2))
        ymax=maxval-minval
        area=ymax*(N.sqrt(2*pi)*sigma)
        print 'ymax',ymax
        pin=[area,center1,width1,0,area,center2,width2]





        if 1:
            p = NLP(chisq, pin, maxIter = 1e3, maxFunEvals = 1e5)
            #p.lb=lowerm
            #p.ub=upperm
            p.args.f=(x,y,yerr)
            p.plot = 0
            p.iprint = 1
            p.contol = 1e-5#3 # required constraints tolerance, default for NLP is 1e-6

# for ALGENCAN solver gradtol is the only one stop criterium connected to openopt
# (except maxfun, maxiter)
# Note that in ALGENCAN gradtol means norm of projected gradient of  the Augmented Lagrangian
# so it should be something like 1e-3...1e-5
            p.gradtol = 1e-5#5 # gradient stop criterium (default for NLP is 1e-6)
    #print 'maxiter', p.maxiter
    #print 'maxfun', p.maxfun
            p.maxIter=50
#    p.maxfun=100

    #p.df_iter = 50
            p.maxTime = 4000
    #r=p.solve('scipy_cobyla')
        #r=p.solve('scipy_lbfgsb')
            #r = p.solve('algencan')
            print 'ralg'
            r = p.solve('ralg')
            print 'done'
            pfit=r.xf
            print 'pfit openopt',pfit
            print 'r dict', r.__dict__
        if 1: 
            print 'mpfit'
            p0=pfit
            parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
            parinfo=[]
            for i in range(len(p0)):
                parinfo.append(copy.deepcopy(parbase))
            for i in range(len(p0)): 
                parinfo[i]['value']=p0[i]
            fa = {'x':x, 'y':y, 'err':yerr}
            #parinfo[1]['fixed']=1
            #parinfo[2]['fixed']=1
            m = mpfit(myfunct_res, p0, parinfo=parinfo,functkw=fa)
            if (m.status <= 0): 
                print 'error message = ', m.errmsg
            params=m.params
            pfit=params
            perror=m.perror
            #chisqr=(myfunct_res(m.params, x=th, y=counts, err=counts_err)[1]**2).sum()
            chisqr=chisq(pfit,x,y,yerr)
            dof=m.dof
            #Icalc=gauss(pfit,th)
            #print 'mpfit chisqr', chisqr
        ycalc=gauss(pfit,x)

        if 1:
            width_x=N.linspace(p0[0]-p0[1],p0[0]+p0[1],100)
            width_y=N.ones(width_x.shape)*(maxval-minval)/2
            pos_y=N.linspace(minval,maxval,100)
            pos_x=N.ones(pos_y.shape)*p0[0]
            if 0:
                
                pylab.errorbar(th,counts,counts_err,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
                pylab.plot(width_x,width_y)
                pylab.plot(pos_x,pos_y)
                pylab.plot(x,ycalc)
                pylab.show()

    else:
        #fix center
        #fix width
        print 'no peak'
        #Area center width Bak
        area=0
        center=x[len(x)/2]
        width=(x.max()-x.min())/5.0  #rather arbitrary, but we don't know if it's the first.... #better to use resolution
        Bak=y.mean()
        p0=N.array([area,center,width,Bak],dtype='float64')  #initial conditions
        parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
        parinfo=[]
        for i in range(len(p0)):
            parinfo.append(copy.deepcopy(parbase))
        for i in range(len(p0)): 
            parinfo[i]['value']=p0[i]
        fa = {'x':x, 'y':y, 'err':yerr}
        parinfo[1]['fixed']=1
        parinfo[2]['fixed']=1
        m = mpfit(myfunct_res, p0, parinfo=parinfo,functkw=fa)
        if (m.status <= 0): 
            print 'error message = ', m.errmsg
        params=m.params
        pfit=params
        perror=m.perror
        #chisqr=(myfunct_res(m.params, x=th, y=counts, err=counts_err)[1]**2).sum()
        chisqr=chisq(pfit,x,y,yerr)
        dof=m.dof
        ycalc=gauss(pfit,x)
        #print 'perror',perror
        if 0:
            pylab.errorbar(x,y,yerr,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
            pylab.plot(x,ycalc)
            pylab.show()

    print 'final answer'
    print 'perror', 'perror'
    #If the fit is unweighted (i.e. no errors were given, or the weights
    #	were uniformly set to unity), then .perror will probably not represent
    #the true parameter uncertainties.

    #	*If* you can assume that the true reduced chi-squared value is unity --
    #	meaning that the fit is implicitly assumed to be of good quality --
    #	then the estimated parameter uncertainties can be computed by scaling
    #	.perror by the measured chi-squared value.

    #	   dof = len(x) - len(mpfit.params) # deg of freedom
    #	   # scaled uncertainties
    #	   pcerror = mpfit.perror * sqrt(mpfit.fnorm / dof)

    print 'params', pfit
    print 'chisqr', chisqr  #note that chisqr already is scaled by dof
    pcerror=perror*N.sqrt(m.fnorm / m.dof)#chisqr
    print 'pcerror', pcerror

    integrated_intensity=N.abs(pfit[0])
    integrated_intensity_err=N.abs(pcerror[0])    
    ycalc=gauss(pfit,x)
    print 'perror',perror
    if 1:
        pylab.figure()
        pylab.errorbar(x,y,yerr,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
        pylab.plot(x,ycalc)
        #qstr=str(qnode.q['h_center'])+','+str(qnode.q['k_center'])+','+str(qnode.q['l_center'])
        #pylab.title(qstr)
        pylab.show()

    return pfit,perror,pcerror,chisq



def gauss(p,x):
    #Area center width Bak area2 center2 width2

    #p=[p0,p1,p2,p3]


    x0=p[1]
    width=p[2]
    sigma=width/2/N.sqrt(2*N.log(2))
    area=N.abs(p[0])/N.sqrt(2*pi)/sigma
    background=N.abs(p[3])
    center2=p[5]
    width2=p[6]
    sigma2=width2/2/N.sqrt(2*N.log(2))
    area2=N.abs(p[3])/N.sqrt(2*pi)/sigma2
    y=background+area*N.exp(-(0.5*(x-x0)*(x-x0)/sigma/sigma))
    y=y+area2*N.exp(-(0.5*(x-center2)*(x-center2)/sigma2/sigma2))
    return y



def chisq(p,a3,I,Ierr):
    Icalc=gauss(p,a3)
    #print I.shape
    #print Ierr.shape
    #print a3.shape
    #print Icalc.shape
    Ierr_temp=copy.deepcopy(Ierr)
    zero_loc=N.where(Ierr==0)[0]
    if len(zero_loc)!=0:
        Ierr_temp[zero_loc]=1.0
    chi=((I-Icalc)/Ierr_temp)**2    
    return chi.sum()/(len(I)-len(p))


def myfunct_res(p, fjac=None, x=None, y=None, err=None):
    # Parameter values are passed in "p"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    model = gauss(p, x)
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    Ierr_temp=copy.deepcopy(err)
    zero_loc=N.where(err==0)[0]
    if len(zero_loc)!=0:
        Ierr_temp[zero_loc]=1.0
    return [status, (y-model)/Ierr_temp]




if __name__=='__main__':
    

    if 1:
        myfilebase='eLsmo740'
        mydirectory=r'C:\ss2009\14470\data'
        myend='bt7'
        myfilebaseglob=myfilebase+'*.'+myend
        #filerange1=range(1,10)
        #filerange1.append(7)
        #filerange1.append(8)
        #filerange1.append(9)
        filerange1=range(12,21)
        #mydirectory=r'C:\srfeas\SrFeAsNi\Ni0p08\2009-04-diffraction'
        #file_range=(35,51)
        #myfilebase='SrFeA0'
        flist=[]
        
        for i in filerange1:
            currfile=os.path.join(mydirectory,myfilebase+str(i)+r"."+myend)
            print 'currfile',currfile
            flist.append(currfile)
        #for i in filerange2:
        #    currfile=os.path.join(mydirectory,myfilebase+str(i)+r"."+myend)
        #    print 'currfile',currfile
        #    flist.append(currfile) 
            
    
        #flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
        #SU.printr(flist)
        E,l,counts,counts_err,mon0=readfiles(flist)
        
        #p,perror,pcerror,chisq=fitpeak(tth[0],counts[0],counts_err[0])
        #print 'p',p,perror,pcerror, chisq
        #sys.exit()
        new_tth,new_T,new_counts=regrid2(E,l,counts)
        #x,y,z=grid(new_tth,new_T,new_counts)
        x=N.array(new_tth)
        y=N.array(new_T)
        z=ma.array(new_counts)

        #QX,QZ=N.meshgrid(qx,qz)
        cmap=pylab.cm.jet
        #import matplotlib.ticker as ticker
        zmin, zmax = 0, 5000
        locator = ticker.MaxNLocator(10) # if you want no more than 10 contours
        locator.create_dummy_axis()
        #locator.set_bounds(zmin, zmax)
        levs = locator()
        #levs=N.linspace(zmin,zmax,10)
        #levs=N.concatenate((levs,[3000]))
        pylab.subplot(1,2,1)
        mycontour=pylab.contourf(x,y,z,levs)#,
        #levs.set_bounds(zmin, zmax)
        #mycontour=pylab.contourf(x,y,z,35,extent=(17,19.6,y.min(),y.max()))#,cmap=pylab.cm.jet)
        #pylab.axis('equal')
    
        #pylab.pcolor(qx,qz,counts)
        #mycontour.set_clim(vmin=160, vmax=500)
        #mycbar=pylab.colorbar()
        
        #mycbar.set_clim(vmin=160, vmax=500)
        #pylab.xlim((17,19.6))
        #pylab.ylim((0,110))
        pylab.show()
        sys.exit()
    

    if 1:
        myfilebase='eLsmo740'
        mydirectory=r'C:\ss2009\14470\data'
        myend='bt7'
        myfilebaseglob=myfilebase+'*.'+myend
        filerange1=range(1,5)
        filerange1.append(7)
        filerange1.append(8)
        filerange1.append(9)
        filerange2=range(10,32)
        #mydirectory=r'C:\srfeas\SrFeAsNi\Ni0p08\2009-04-diffraction'
        #file_range=(35,51)
        #myfilebase='SrFeA0'
        flist=[]
        
        for i in filerange1:
            currfile=os.path.join(mydirectory,myfilebase+str(0)+str(i)+r"."+myend)
            print 'currfile',currfile
            flist.append(currfile)
        for i in filerange2:
            currfile=os.path.join(mydirectory,myfilebase+str(i)+r"."+myend)
            print 'currfile',currfile
            flist.append(currfile) 
            
    
        #flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
        #SU.printr(flist)
        tth,T,counts,counts_err,mon0=readfiles(flist,mon0=mon0)
        new_tth,new_T,new_counts=regrid2(tth,T,counts)
        #x,y,z=grid(new_tth,new_T,new_counts)
        x=N.array(new_tth)
        y=N.array(new_T)
        z=ma.array(new_counts)

        #QX,QZ=N.meshgrid(qx,qz)
        cmap=pylab.cm.jet
        #import matplotlib.ticker as ticker
        if 0:
            zmin, zmax = 160, 500
            locator = ticker.MaxNLocator(10) # if you want no more than 10 contours
            locator.create_dummy_axis()
            locator.set_bounds(zmin, zmax)
            levs = locator()
        #levs=10
        #levs=N.linspace(zmin,zmax,10)
        #levs=N.concatenate((levs,[3000]))
        ax2=pylab.subplot(1,2,2)
        #print 'hi'
        mycontour=pylab.contourf(x,y,z,levs)#,
        #levs.set_bounds(zmin, zmax)
        #mycontour=pylab.contourf(x,y,z,35,extent=(17,19.6,y.min(),y.max()))#,cmap=pylab.cm.jet)
        #pylab.axis('equal')
    
        #pylab.pcolor(qx,qz,counts)
        #mycontour.set_clim(vmin=160, vmax=500)
        mycbar=pylab.colorbar()
        
        #mycbar.set_clim(vmin=160, vmax=500)
        pylab.xlim((17,19.6))
        pylab.ylim((0,110))
        ax2.yaxis.set_major_formatter(pylab.NullFormatter())
        ax2.yaxis.set_major_locator(pylab.NullLocator())
        pylab.show()
    

