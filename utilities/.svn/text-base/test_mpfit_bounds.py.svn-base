from spinwaves.utilities.mpfit.mpfit import mpfit
import numpy as N
pi=N.pi
import copy


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
    return (y-ycalc)/err/N.sqrt(dof)

def myfunctlin(p, fjac=None, x=None, y=None, err=None):
    # Parameter values are passed in "p"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    return [status, cost_func(p,x,y,err)]

if __name__=="__main__":
    x=N.arange(-3,4,.005)
    #y=fp_gaussian(x,1,0,.5)
    p=[500,0.7,.2]
    y=matlab_gaussian(x,p)
    yerr=N.sqrt(y)+1
    p0=[0,0,0.7,.4,400] #center,fwhm,height
    if 1:
            parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
            parinfo=[]
            for i in range(len(p0)):
                parinfo.append(copy.deepcopy(parbase))
            for i in range(len(p0)): 
                parinfo[i]['value']=p0[i]
            fa = {'x':x, 'y':y, 'err':yerr}
            parinfo[4]['limited']=[1,1]
            parinfo[4]['limits']=[400,499]
            m = mpfit(myfunctlin, p0, parinfo=parinfo,functkw=fa) 
            print 'status = ', m.status
            print 'params = ', m.params
            p1=m.params
            covariance=m.covar