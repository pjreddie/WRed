import numpy as N
#import matplotlib
#matplotlib.use('WXAgg')
import pylab

#from matplotlib.figure import Figure
from sgolay import savitzky_golay as savitzky_golay
import sys,copy
import scipy.interpolate as interpolate
pi=N.pi
from numpy.random import randn
import scipy, scipy.optimize
from spinwaves.utilities.mpfit.mpfit import mpfit


def findpeak(x,y,npeaks,order=4,kernel=11):
    """This is a program that finds the positions and FWHMs in a set of
    data specified by x and y.  The user supplies the number of peaks and
    the program returns an array p, where the first entries are the positions of
    the peaks and the next set are the FWHMs of the corresponding peaks
    The program is adapted from a routine written by Rob Dimeo at NIST and
    relies on using a Savit-Golay filtering technique to obtain the derivative
    without losing narrow peaks.  The parameter F is the frame size for the smoothing
    and is set to 11 pts.  The order of the polynomial for making interpolations to better
    approximate the derivative is 4.  I have improved on Dimeo's program by also calculating second
    derivative information to better handle close peaks.  If peaks are too close together, there are
    still problems because the derivative may not turn over.  I have also added a refinement of going
    down both the left and right sides of the peak to determine the FWHMs because of the issue of peaks that
    are close together."""

#F=11;
#[b,g]=sgolay(4,F);   %original
#%g=sgolay(4,F);

#yd=zeros(1,length(x));
#yd2=zeros(1,length(x));
#for n=(F+1)/2:length(x)-(F+1)/2
#    yd(n)=g(:,2)'*y(n - (F+1)/2 + 1: n + (F+1)/2 - 1)';
#    yd2(n)=g(:,3)'*y(n - (F+1)/2 + 1: n + (F+1)/2 - 1)';
#end
    step=abs(x[0]-x[1]) #assume that x is monotonic and uniform step sizes
    #print 'step',step
    yd=savitzky_golay(y,kernel=kernel,order=order,deriv=1)/step
    yd2=savitzky_golay(y,kernel=kernel,order=order,deriv=2)/step**2
    n_crossings=0;
    ny = len(yd);
    #print 'y',y
    #print 'ny',ny, len(y)
    value_sign = 2*(yd > 0) - 1;
    indices = 0;



    # Determine the number of zero crossings
    #%diff_sign = value_sign(2:ny)-value_sign(1:ny-1);
    diff_sign=N.hstack(([0],N.diff(value_sign)))

#    wh_cross = find(((diff_sign==2) | (diff_sign==-2)) & yd2<0);
    wh_cross_table=N.abs(diff_sign)==2 
    yd_table=yd2<0

    #print wh_cross_table
    #print yd_table
    index_list=N.array(range(len(wh_cross_table)))
    #print N.array(wh_cross_table)*N.array(yd_table)
    wh_cross=index_list[N.array(wh_cross_table)*N.array(yd_table)]
    #print 'wh_cross',wh_cross, 'y[wh_cross]',y[wh_cross],'yd',yd[wh_cross],'yd2',yd_table[wh_cross]
    n_crossings=len(wh_cross);


#    
#    
#    
    indices = 0.5*(2*wh_cross-1);
    indices=wh_cross
#    print 'indices',indices
#    
    no_width = 0;
#    
    if n_crossings > 0:
#    #% Ok, now which ones of these are peaks?


        #ymax=interp1(ysupport,y,indices);
        ysupport=range(len(y))
        #print 'ysupport',ysupport
        yinterpolater=interpolate.interp1d(ysupport,y,fill_value=0.0,kind='linear',copy=True,bounds_error=False)
        ymax=yinterpolater(indices)
        #print 'y_interpolated',ymax
#     #%  ymax = interpolate(y,indices)
        ymin = N.min(ymax)
        #print 'ymin',ymin
        #print 'npeaks',npeaks
        #print 'yd2',yd2
        xsupport=range(len(x))
        xinterpolater=interpolate.interp1d(xsupport,x,fill_value=0.0,kind='linear',copy=True,bounds_error=False)        
        xpeaks=xinterpolater(indices)
        #print 'xpeaks',xpeaks
        #return xpeaks

        for i in range(npeaks):
            this_max=N.max(ymax)
            max_index=N.nonzero(ymax==this_max)
            #max_index = find(ymax==this_max);
            if i ==0:
                best_index = indices[max_index]
            else:    
                best_index =N.hstack((best_index, indices[max_index]));
            ymax[max_index] = ymin;
        indices = best_index;

        #print 'indices',indices
        xsupport=range(len(x))
        xinterpolater=interpolate.interp1d(xsupport,x,fill_value=0.0,kind='linear',copy=True,bounds_error=False)        
        xpeaks=xinterpolater(indices)
        #print 'xpeaks',xpeaks
        results={}
        results['xpeaks']=xpeaks
        results['indices']=indices
        results['heights']=y[indices]
        return results

        #xsupport=1:length(x);
        #xpeaks = interp1(xsupport,x,indices);
#        xpeaks=xpeaks(1:npeaks);
#    
#    
#   

def findwidths(x,y,npeaks,xpeaks,indices):
    ny=len(y)
    for i in range(npeaks):   
        full_height = y[N.floor(indices[i])]
        half_height = 0.5*full_height;
#          % Descend down the peak until you get lower than the half height
        elevation = full_height;
        incrementr = 1;
        #print 'elevation', elevation
        #print 'half height',half_height
        while elevation > half_height:
#             % go down the right side of the peak
            incrementr = incrementr+1;
            no_widthr = 0;
            #elevation = y[N.floor(indices[i])+incrementr];
            if (N.floor(indices[i])+incrementr >= ny):
                no_widthr = 1;
                #print 'nowidthr'
                break;
            elevation = y[N.floor(indices[i])+incrementr];


        incrementr=incrementr-1  #error on the side of making it too narrow!
        #print 'incrementr', incrementr
        #print 'elevationr',y[N.floor(indices[i])+incrementr]
        #print 'no_widthr',no_widthr
#               %goto, no_width_found
#          #%now go to the left side of the peak
#          #% Descend down the peak until you get lower than the half height
        elevation = full_height;
        incrementl = -1;
        while elevation > half_height:
#             % go down the right side of the peak
            incrementl = incrementl-1;
            no_widthl = 0;
            #elevation = y[N.floor(indices[i])+incrementl];
            if (N.floor(indices[i])+incrementl<= 0):
                no_widthl = 1;
                break;
            elevation = y[N.floor(indices[i])+incrementl];

#               %goto, no_width_found

        incrementl=incrementl+1
        #print 'incrementl', incrementl
        #print 'elevationl',y[N.floor(indices[i])+incrementl]
        #print 'no_widthl',no_widthl
        no_width=N.min([no_widthl,no_widthr]);
        increment=N.min([N.abs(incrementl),incrementr]);

        #print 'delta',x[N.floor(indices[i])+increment]
        #print 'increment', increment
        #print 'no_width', no_width
#            
#    
#     #%     no_width_found:
        if no_width==1:
            #print 'no width found'
            width = 2.0*(x[ny-1]-xpeaks[i]);
        else:
            width = 2.0*(x[N.floor(indices[i])+increment]-xpeaks[i]);             
        if i == 0:
            fwhm = [width]
        else:
            fwhm = N.hstack((fwhm,N.array([width])))

#      #     %plot([(xpeaks(i)-fwhm(i)/2) (xpeaks(i)+fwhm(i)/2)],[half_height half_height]); hold on;
#      end
#      #%hold off;
#    
#      #%b=length(fwhm);
#      #%fwhm=fwhm(b);

    #print 'xpeaks',xpeaks
    #p=N.hstack((xpeaks[0:npeaks],N.abs(fwhm)))
    #print p
#      return p

    return N.abs(fwhm)



def calc_DW(y,kernel=11,order=4):
    """Calculated the DW statistic for y, y must have more than 1 point"""
    ysmd=savitzky_golay(y,kernel=kernel,order=order,deriv=0)
    n=len(y)
    DW=0
    #for i in range(1,n):
    #    DW=((y[i]-ysmd[i])-(y[i-1]-ysmd[i-1]))**2+DW
    DW=((N.diff(y)-N.diff(ysmd))**2).sum()
    DW=DW*n/(n-1)    
    DW=DW/((y-ysmd)**2).sum()
    return DW

def make_odd(x):
    if x%2==0:
        return x-1
    else:
        return x

def optimize_DW(y,order=4):
    DW=[]
    #need to check that there are at least order+2 points and check range is valid
    if order%2==0:
        minkern=1
    else:
        minkern=0
    odd_len=make_odd(len(y))    
    kernel_range=range(order+2+minkern,min(len(y)/1,odd_len),2) #The 3 here is arbitrary and this line needs to be more robust!
    print kernel_range
    for kernel in kernel_range:
        print 'kernel',kernel
        DW.append(calc_DW(y,kernel=kernel,order=order))
        
    return kernel_range,DW
        

def calc_prob(npeaks,amax,covariance,chimin,rangex):
    prob=N.log(scipy.factorial(npeaks))+npeaks*N.log(4*pi)-npeaks*N.log(N.abs(amax)*N.abs(rangex))
    prob=prob+0.5*N.log(N.linalg.det(covariance/2))-chimin/2
    return prob

#def calc_prob(


def fp_gaussian(x,area,center,fwhm):
    sig = fwhm/2.354;
    y = (area/N.sqrt(2.0*pi*sig**2))*N.exp(-0.5*((x-center)/sig)**2);
    return y

def matlab_gaussian(x,p):
    area,center,fwhm=p
    sig = fwhm/2.354;
    #print 'area,center,fwhm',area,center,fwhm
    #y= N.abs(I)*N.exp(-0.5*((x-center)/w)**2)
    y = (N.abs(area)/N.sqrt(2.0*pi*sig**2))*N.exp(-0.5*((x-center)/sig)**2);
    return y

def matlab_gaussian2(x,p):
    height,center,fwhm=p
    sig = fwhm/2.354;
    #y= N.abs(I)*N.exp(-0.5*((x-center)/w)**2)
    y = height*N.exp(-0.5*((x-center)/sig)**2);
    return y

def gen_function(p,x):
    npeaks=(len(p)-2)/3
    y=p[0]+p[1]*x
    for i in range(npeaks):
        #print 'i',i
        center=p[2+i]
        fwhm=p[2+npeaks+i]
        #sigma=fwhm/2.354
        area=p[2+2*npeaks+i]#
        y=y+matlab_gaussian(x,[area,center,fwhm])
    return y

def cost_func(p,x,y,err):
    ycalc=gen_function(p,x)
    dof=len(y)-len(p)
    fake_dof=len(y)
    return (y-ycalc)/(err+1)#/N.sqrt(fake_dof)

def myfunctlin(p, fjac=None, x=None, y=None, err=None):
    # Parameter values are passed in "p"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    return [status, cost_func(p,x,y,err)]

def find_kernel(y):
    kern,DW=optimize_DW(y)
    DW=N.array(DW)
    DW_min=min(N.abs(DW-2))
    ind=N.where(N.abs(DW-2)==DW_min)[0]
    print 'ind',ind
    print 'DW_min',DW[ind]
    kernel=kern[ind]
    if 0:
        pylab.plot(kern,N.abs(DW-2),'s')
        pylab.show()
        sys.exit()
    return kernel

def find_npeaks(x,y,yerr,kernel,nmax=6):
    nlist=[]
    plist=[]
    #if 1:
    for npeaks in range(1,nmax): 
        print 'npeaks',npeaks
        results=findpeak(x,y,npeaks,kernel=kernel)
        fwhm=findwidths(x,y,npeaks,results['xpeaks'],results['indices'])
        print 'res',results['xpeaks']
        print 'fwhm',fwhm
        print 'heights',results['heights']       
        p0=[0,0]
        
        #results['heights']=[1000,500,1000]
        #fwhm=[.1,.2,.4]
        sigma=fwhm/2.354
        pb=N.concatenate((results['xpeaks'], fwhm, results['heights']*N.sqrt(2*pi*sigma**2)))
        pb=N.array(pb).flatten()
        p0=N.concatenate((p0,pb)).flatten()
        print 'p0',p0
        ycalc=gen_function(p0,x)
        if 1:
            fresults= scipy.optimize.leastsq(cost_func, p0, args=(x,y,yerr),full_output=1)
            p1=fresults[0]
            covariance=fresults[1]
            print 'p1',p1
            
            
    
        if 0:
            parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
            parinfo=[]
            for i in range(len(p0)):
                parinfo.append(copy.deepcopy(parbase))
            for i in range(len(p0)): 
                parinfo[i]['value']=p0[i]
            fa = {'x':x, 'y':y, 'err':yerr}
            m = mpfit(myfunctlin, p0, parinfo=parinfo,functkw=fa) 
            print 'status = ', m.status
            print 'params = ', m.params
            p1=m.params
            covariance=m.covar
         
        if 1:
            #area=max(N.abs(p1[-3::]))
            #area=N.array((N.abs(p1[-3::])))
            area=N.array(N.abs(p1[2+2*npeaks::]))
            fwhm=N.array(N.abs(p1[2+npeaks:2+2*npeaks]))
            sigma=fwhm/2.354
            amax=max(area/N.sqrt(2*pi*sigma**2))
            #amax=max(y)/N.sqrt(2*pi*sigma**2)
            dof=len(y)-len(p1)
            fake_dof=len(y)
            chimin=(cost_func(p1,x,y,yerr)**2).sum()
            chimin=chimin#/fake_dof
            
            rangex=max(x)-min(x)
            #prob=calc_prob(npeaks,amax,covariance,chimin,rangex)
            #print 'det_covariance',N.linalg.det(covariance)
            
            prob=len(y)*N.log(chimin/len(y)) +len(p1)*N.log(len(y))
            print 'prob',prob,'chimin',chimin,'amax',amax
            nlist.append(npeaks)
            plist.append(prob)
            #sys.exit()
    nmin=nlist[N.where(N.array(plist)==min(plist))[0]]        
    print 'nmin', nmin
    return nmin,nlist,plist

if __name__=="__main__":
    x=N.arange(-3,4,.005)
    #y=fp_gaussian(x,1,0,.5)
    p=[500,0.7,.2]
    y=matlab_gaussian(x,p)
    p=[1000,1,.4]
    y=y+matlab_gaussian(x,p)
    p=[1000,1.2,.1]
    y=y+matlab_gaussian(x,p)
    yerr=N.sqrt(y)+2
    y += randn(len(y)) * yerr
    y=N.abs(y)
    
    if 0:
        pylab.plot(x,y,'s')
        pylab.show()
        sys.exit()
    #yerr=N.sqrt(y)+1
    #fig=Figure()
    #fig=pylab.Figure()
    #canvas = FigureCanvas(fig)
    #axes = fig.add_subplot(111)
    

    kernel=31
    npeaks=2 
    nmin,nlist,plist=find_npeaks(x,y,yerr,kernel)
    if 0:
        pylab.semilogy(nlist,plist,'s')
        
    if 1:
        pylab.plot(nlist,plist,'s') 
    if 1:
        pylab.show()
    if 0:
        pylab.plot(x,y,'s')
        pylab.axis([0,2,0,1.4e4])
            
        for i in range(npeaks):
            pylab.axvline(x=results['xpeaks'][i])
            xcen=results['xpeaks'][i]
            half_height=y[results['indices'][i]]/2
            pylab.plot([(xcen-fwhm[i]/2),(xcen+fwhm[i]/2)],[half_height,half_height])
            ycalc=gen_function(p1,x)
            pylab.plot(x,ycalc)
        
        pylab.axis([0,2,0,1.4e4])
        pylab.show()
    