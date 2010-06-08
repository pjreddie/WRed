import numpy as N
import  pylab
#import scipy.sandbox.delaunay as D
#import numpy.core.ma as ma
#import matplotlib.numerix.ma as ma
#from matplotlib.ticker import NullFormatter, MultipleLocator
#from scipy.signal.signaltools import convolve2d
import scriptutil as SU
import re
import readncnr2 as readncnr
#from matplotlib.ticker import FormatStrFormatter
#from matplotlib.ticker import MaxNLocator
import scipy.optimize as optimize

#define TnNum 1
#define JtNum 2
#define NfNum 3
#define BkNum 4
#define Tn (p[TnNum])
#define Jt (p[JtNum])
#define Nf (p[NfNum])
#define Bk (p[BkNum])
##float bsol(float temp, float * p){
##  float t=4.0*(Jt/(Jt+1))*Tn/temp;
##  return (((Tn<=0) || (Jt<=0) || (temp >= Tn)) ?
##              0.0 :
##              pklzbrent(bfun,0,t,1e-6,temp,p));
##}float bfun(float x, float t, float * p){
##        if(x==0) return -1.0;   /* so that it wont find solution at zero */
##        /* let's do it for a change the straight way */
##        return (x-3*brill(Jt,x)*(Jt/(Jt+1))*(Tn/t));
##}float brill(float j, float x)
##{
##        float temp;
##        temp=(2*j+1)/2/j;
##        return (x==0? 0 :temp/tanh((double)temp*x)-1/tanh((double)x/2/j)/2/j);
##}
##void
##
##float fnc(float t, float * p){
##  if (Intensity)
##     return Bk+Nf*SQR(brill(Jt,bsol(t,p)));
##  else
##     return Bk+Nf*brill(Jt,bsol(t,p));
##}


def bsol(temp,p):
    Tn,Jt,Nf,Bk=p
    t=4.0*(Jt/(Jt+1.0))*Tn/temp
    #print t
    if (Tn<=0) or (Jt<=0) or temp>=Tn:
        xout=0.0#N.zeros(temp.shape,'float64')
    else:
        #xout=optimize.brent(bfun,args=(temp,p),brack=(0.0,t/2,t),tol=1.0e-6)
        #print 'before optim'
        xout=optimize.brentq(bfun,0.0,t,args=(temp,p),xtol=1e-6)# (bfun,args=(temp,p),brack=(0.0,t/2,t),tol=1.0e-6)
        #print 'after optim'

    return xout

def bfun(x,T,p):
    Tn,Jt,Nf,Bk=p
    if x==0.0:
        B=-1.0#   /* so that it wont find solution at zero */
        #/* let's do it for a change the straight way */
        #print 'bfun x=0'
    else:
        B=(x-3*brill(Jt,x)*(Jt/(Jt+1))*(Tn/T))
    return B

def brill(j,x):
    #Tn,Jt,Nf,Bk=p
    #print 'Tn=',Tn,' Jt=',Jt,' Nf=',Nf,' Bk=',Bk
    temp=(2*j+1.0)/2/j
    #print x
    if x==0:
        Br=0.0
        #print 'brill x=0'
    else:
        Br=temp/N.tanh(temp*x)-1.0/N.tanh(x/2/j)/2/j
    #Br[x==0]=0
    return Br

def Intensity(T,p):
    Tn,Jt,Nf,Bk=p
    #print 'before brill'
    br=brill(Jt,bsol(T,p))
    #print 'after brill'
    bout=Bk+Nf*br**2
    return bout

def orderparameter(p,T):
    I=[]
    for t in T:
        I.append(Intensity(t,p))
    return N.array(I)

if __name__=='__main__':
    #p=[Tn Jt Nf Bk]
    p=[50.0,0.5,100.0,0.0]
    T=N.arange(70.0)
    I=[]
    M=[]
    #for t in T:
    #    M.append(brill(0.5,t))
    #print M
    #if 1:
    #    pylab.plot(T,M,'bo')
    #    pylab.show()
    #exit()
    #print Intensity(20.0,p)
    #exit()
    I=orderparameter(p,T)
    #for t in T:
    #    print 'T=',t
    #    I.append(Intensity(t,p))
    #print I
    if 1:
        pylab.plot(T,I,'bo')
        pylab.show()
