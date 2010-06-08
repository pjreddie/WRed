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

def read_order_files(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
#    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readncnr.datareader()
    temp=[]#N.array([])
    I=[]#N.array([])
    Ierr=[]#N.array([])
    monlist=[]
    count=0
    mon0=5.0e4
    for currfile in flist:
        #print currfile
        mydata=mydatareader.readbuffer(currfile)
        #if count==0:
        #    #mon0=mydata.header['count_info']['monitor']
        #    mon0=5.0e4
        mon=mydata.metadata['count_info']['monitor']
        #print count, mon0,mon
        #temp=N.concatenate((temp,N.array(mydata.data['temp'])))
        temp.append(N.array(mydata.data['temp'],'float64'))
        It=N.array(N.array(mydata.data['counts']),'float64')
        Iterr=N.sqrt(It)
        #It=It*mon0/mon
        monlist.append(mon)
        I.append(It)
        Ierr.append(Iterr)
        #Iterr=Iterr*mon0/mon
        #I=N.concatenate((I,It))
        #Ierr=N.concatenate((Ierr,Iterr))
        #print I
        #print Iterr
    #xa,ya,za=prep_data2(Qx,Qy,Counts);
        count=count+1
    return temp,I,Ierr,monlist


def orderparameter(p,T):
    #p[0]=Intensity
    I0,Tc,Beta,background=p
    I=I0*N.power(N.absolute(T/Tc-1),2*Beta)
    I[T>Tc]=0.0
    I=I+background
    return I

def chisq_calc(p,T,I,Ierr):
    Icalc=orderparameter(p,T)
    chisq=(I-Icalc)*(I-Icalc)/p.shape[0]/Ierr/Ierr
    return chisq

def residuals(p,T,I,Ierr):
    Icalc=orderparameter(p,T)
    residual=(I-Icalc)/Ierr
    return residual

if __name__=='__main__':
    mydirectory=r'C:\jasons\CoC3N2H5\Feb4_2008'
    myfilebase='order*'
    myend='bt9'
    temp,I,Ierr,monlist=read_order_files(mydirectory,myfilebase,myend)
##    print 'read '
##    print 'temp ',temp
##    print 'I',I
##    print Ierr 
##    print 'monlist ' ,monlist
##    print len(I),len(monlist)
    T,I,Ierr=simple_combine.simple_combine(temp,I,Ierr,monlist)
    #print temp.shape, I.shape, Ierr.shape
    #pylab.errorbar(temp,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None)
    p0=[copy.deepcopy(I[0]),20.0,.33333,copy.deepcopy(I[-1])]
    Trange=N.intersect1d(N.where(T>8)[0],N.where(T<27)[0])
    oparam=scipy.odr.Model(orderparameter)
    mydata=scipy.odr.RealData(T[Trange],I[Trange],sx=None,sy=Ierr)
    myodr = scipy.odr.ODR(mydata, oparam, beta0=p0)
    myoutput=myodr.run()
    myoutput.pprint()
    pfit=myoutput.beta
    #pfit = leastsq(residuals, p0, args=(T[Trange],I[Trange],Ierr[Trange]))  
    print 'pfit=',pfit
    print 'chisq=',chisq_calc(pfit,T[Trange],I[Trange],Ierr[Trange]).sum()
    Icalc=orderparameter(pfit,T)
    if 1:
        pylab.errorbar(T,I,Ierr,marker='s',linestyle='None',mfc='blue',mec='blue',ecolor=None)
        pylab.plot(T,Icalc)
        pylab.xlabel('T (K)')
        pylab.ylabel('Counts (arb. units)')
        #pylab.ylim((0,700))
        #pylab.arrow(90,200,0,50,fc='black',ec='black',width=.5)
        #pylab.arrow(60,200,0,50,fc='black',ec='black',width=.5)
        pylab.show()
