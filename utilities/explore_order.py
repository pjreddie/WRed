import numpy as N
import pylab
import scriptutil as SU
import re
import readncnr2 as readncnr
import simple_combine
#import scipy
from scipy.optimize import leastsq
import copy
import scipy.odr
#import scipy.optimize.anneal as anneal
import anneal
pi=N.pi

def coth(x):
    return 1.0/N.tanh(x)

def orderparameter_spinwave(p,T):
    I0,c,Tc,background=p
    x=N.absolute(T/Tc)
    M=1-N.absolute(c)*T**1.5
    I=N.absolute(I0)*M**2
    I[T>N.absolute(Tc)]=0.0
    I=I+N.absolute(background)
    return I

def orderparameter_brillouin(p,T):
    I0,J,h,background=p
    x=-h/T
    B=(2*J+1)/2/J/N.tanh((2*J+1)/(2*J)*x)-1/N.tanh(x/2/J)/2/J
#    print N.tanh((2*J+1)/(2*J)*x)
#    print x
    I=background+I0*B**2
    return I


if __name__=='__main__':
    p0=[1.0,5.0e-3,50.0,0]
    #p0=[100.0,0.5,5.0e-4,0]
    T=N.arange(10.0,100.0,1.0)
    I=orderparameter_spinwave(p0,T)
    #I=orderparameter_brillouin(p0,T)
    pylab.plot(T,I,'r')
    pylab.show()