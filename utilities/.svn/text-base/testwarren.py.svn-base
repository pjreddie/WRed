from __future__ import division
import numpy as N
import rescalculator.lattice_calculator as lattice_calculator
pi=N.pi
from spinwaves.utilities.mpfit.mpfit import mpfit
import sys,os,copy
import pylab
from utilities.anneal import anneal
from numpy import sqrt,sin,cos
import scipy.integrate

a=3.84; b=3.879; wavelength=2.35

def integrand(x,a):
    return N.exp(-(x**2-a)**2)

def f(x,a):
    return scipy.integrate.quad(integrand,0,scipy.integrate.inf,(a,))[0]

def integrand2(phi,th,L,th_hk):
    return N.exp(-4*pi*L**2/wavelength**2*(sin(th)*cos(phi)-sin(th_hk))**2)
 



def F(th,L,th_hk):
    def innerF(th):
        #return scipy.integrate.simps(integrand2,0,pi/2,(th,L,th_hk))[0]
        return scipy.integrate.quad(integrand2,0,pi/2,(th,L,th_hk))[0]
    Fvec=N.vectorize(innerF)
    return Fvec(th)

def Ihk(th,p):
    C,L,h,k=p
    th_rad=N.deg2rad(th)
    #L=1.0/sqrt((1/Nx/a)**2+(1/Ny/b)**2)
    th_hk=N.arcsin(sqrt((h/a)**2+(k/b)**2)*wavelength/2)
    FM=1.0
    y=C*FM**2*F(th_rad,L,th_hk)
    #print 'y',y
    y=y/sin(th_rad)
    #print 'y2',y
    return y

def readfiles(flist,mon0=None):
    mydatareader=readncnr.datareader()
    #Qx=N.array([])
    #Qy=N.array([])
    #Qz=N.array([])
    #tth=N.array([])
    #Counts=N.array([])
    #T=N.array([])
    tth=[]
    Counts=[]
    Counts_err=[]
    T=[]
    i=0
    for currfile in flist:
        #print currfile
        mydata=mydatareader.readbuffer(currfile)
        #print mydata.data.keys()
        if i==0:
            if mon0==None:
                mon0=mydata.metadata['count_info']['monitor']
        #a=mydata.metadata['lattice']['a']
        #b=mydata.metadata['lattice']['b']
        #c=mydata.metadata['lattice']['c']
        mon=mydata.metadata['count_info']['monitor']
        tth.append(N.array(mydata.data['a4']))
        Counts.append(N.array(mydata.data['counts'])*mon0/mon)
        Counts_err.append(N.sqrt(N.array(mydata.data['counts']))*mon0/mon)
        #T.append(N.array(mydata.data['temp'])) #What we probably want
        Tave=N.array(mydata.data['temp']).mean()
        T.append(N.ones(tth[i].size)*Tave)
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
    return tth,T,Counts,Counts_err,mon0

if __name__=="__main__":
    C=100
    #h=.526; k=1.0
    h=0.5; k=0.5; 
    L=50.0
    p=N.array([C,L,h,k],'Float64')
    th=N.arange(22,32,.2)/2
    y=Ihk(th,p)
    print 'yfinal',y
    if 1:
        pylab.plot(th*2,y,'s')
        pylab.show()
    file1=r'c:\ZnMn2O4\bt2\t90k.bt2';
    file2=r'c:\ZnMn2O4\bt2\t40k.bt2';