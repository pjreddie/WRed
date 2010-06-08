import numpy as N
import pylab
g=2.0
k=8.617343e-2
muB=5.7883e-2

def susceptibility(p,T,n=10):
    J,C=p
    J=N.absolute(J)
    K=J/2/k/T
    #Beta=1.0/k/T
    Beta=muB
    chi_par=(g**2*Beta**2*n/4/k/T)*N.exp(-J/k/T)*(1-(-N.tanh(K)**n))/(1+(-N.tanh(K)**n))+C/T
    return chi_par

if __name__=="__main__":
    p=[1,.5]
    T=N.arange(1.0,200.0,.5)
    chi=susceptibility(p,T,n=8)
    chi2=susceptibility(p,T,n=3)
    chi3=susceptibility(p,T,n=20000)
    print chi
    print 'J', p[0]/k
    if 1:
        pylab.plot(T,chi,marker='s')
        pylab.plot(T,chi2,marker='s')
        #pylab.plot(T,chi3,marker='s')
        pylab.show()
    
    
    