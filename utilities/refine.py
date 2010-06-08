from __future__ import division
import numpy as N
import rescalculator.lattice_calculator as lattice_calculator
pi=N.pi
from spinwaves.utilities.mpfit.mpfit import mpfit
import sys,os,copy
import pylab
from utilities.anneal import anneal
from numpy import sqrt
A=5.581
B=A
C=13.8757


h1=N.array([[1,0,0],
            [0,1,0],
            [0,0,1]
            ],'Float64')
h2=N.array([[0,-1,0],
            [1,0,0],
            [0,0,1]
            ],'Float64')
h3=N.array([[-1,0,0],
            [0,-1,0],
            [0,0,1]
            ],'Float64')
h4=N.array([[0,1,0],
            [-1,0,0],
            [0,0,1]
            ],'Float64')


ah=A; ch=C/2

B1=N.array([[sqrt(2)/3/ah,-4/3/ah/sqrt(2),sqrt(2)/3/ah],
            [4/3/ah/sqrt(2),-sqrt(2)/3/ah,-sqrt(2)/3/ah],
            [sqrt(3)/ch,sqrt(3)/ch,sqrt(3)/ch]
            ],'Float64')
B2=N.dot(h2,B1)
B3=N.dot(h3,B1)
B4=B.dot(h4,B1)
B1inv=N.linalg.inv(B1)
M2=N.dot(N.dot(B1inv,h2),B1) #could have done M2=N.dot(B1iv,B2)
M3=N.dot(N.dot(B1inv,h3),B1)
M4=N.dot(N.dot(B1inv,h4),B1) 
#so N.dot(M4,vec) takes vec from individual 4 into frame of individual 1
#vec is in hexagonal coordinates, so need to convert pc->hex for that individual


def calcstar():
    ar=N.sqrt(3*A**2+C**2)/3
    alphar=2*N.arcsin(3/2/N.sqrt(3+(C/A)**2))
    a=N.array([ar],'Float64')
    b=N.array([ar],'Float64')
    c=N.array([ar],'Float64')  
    alpha=N.array([alphar],'Float64')
    beta=N.array([alphar],'Float64')
    gamma=N.array([alphar],'Float64')
    orient1=N.array([[1,0,0]],'Float64')
    orient2=N.array([[0,0,1]],'Float64')
    orientation=lattice_calculator.Orientation(orient1,orient2)
    lattice = lattice_calculator.Lattice(a=a,b=b,c=c,alpha=alpha,beta=beta,gamma=gamma,\
                                 orientation=orientation)
    astar=lattice.astar
    alphastar=lattice.alphastar
    return astar[0],alphastar[0],lattice
    
    

def calcd(H,K,L):
    a=N.array([A],'Float64')
    b=N.array([B],'Float64')
    c=N.array([C],'Float64')
    
    
    alpha=N.radians(N.array([90],'Float64'))
    beta=N.radians(N.array([90],'Float64'))
    gamma=N.radians(N.array([120],'Float64'))
    orient1=N.array([[1,0,0]],'Float64')
    orient2=N.array([[0,0,1]],'Float64')
    orientation=lattice_calculator.Orientation(orient1,orient2)
    lattice = lattice_calculator.Lattice(a=a,b=b,c=c,alpha=alpha,beta=beta,gamma=gamma,\
                                 orientation=orientation)
    newinput=lattice_calculator.CleanArgs(a=lattice.a,b=lattice.b,c=lattice.c,alpha=lattice.alpha,beta=lattice.beta,\
                             gamma=lattice.gamma,orient1=lattice._orient1,orient2=lattice._orient2,H=H,K=K,L=L)
    orientation=lattice_calculator.Orientation(newinput['orient1'],newinput['orient2'])
    lattice.__init__(a=newinput['a'],b=newinput['b'],c=newinput['c'],alpha=newinput['alpha'],\
                        beta=newinput['beta'],gamma=newinput['gamma'],orientation=orientation\
                        )
    alphastar=lattice.alphastar
    print 'alphastar',alphastar
    EXP={}
    EXP['ana']={}
    EXP['ana']['tau']='pg(002)'
    EXP['mono']={}
    EXP['mono']['tau']='pg(002)';
    EXP['ana']['mosaic']=30
    EXP['mono']['mosaic']=30
    EXP['sample']={}
    EXP['sample']['mosaic']=10
    EXP['sample']['vmosaic']=10
    EXP['hcol']=N.array([40, 10, 20, 80],'Float64')
    EXP['vcol']=N.array([120, 120, 120, 120],'Float64')
    EXP['infix']=-1 #positive for fixed incident energy
    EXP['efixed']=14.7
    EXP['method']=0
    setup=[EXP]
    qx,qy,qz,Q=lattice.R2S(H,K,L)
    print 'Q',Q
    d=2*pi/Q
    print 'd',d
    return d
    
 
def calc_cos2n(phi,h,k,l,d,alphastar,astar):
    """These H,K,L,should be in rhombohedral"""
    n=h**2+k**2+l**2
    r=h*k+k*l+l*h
    cosn=(n-r)*(1-N.cos(alphastar))*N.sin(phi)**2+\
        (n+2*r)*(1+2*N.cos(alphastar))*N.cos(phi)**2
    
    cosn=cosn*astar**2*d**2/4/pi**2/3
    return cosn

def pseudocubic2hex(h,k,l):
    g=N.array([[1,-1,0],[0,1,-1],[2,2,2]],'Float64')
    hh=[]
    kh=[]
    lh=[]
    for i in range(len(l)):
        vec=N.array([h[i],k[i],l[i]],'Float64')
        vech=N.dot(g,vec)
        hh.append(vech[0])
        kh.append(vech[1])
        lh.append(vech[2])
        
    return N.array(hh),N.array(kh),N.array(lh)
    
    
def hex2rhomb(h,k,l):
    g=N.array([[2,1,1],[-1,1,1],[-1,-2,1]],'Float64')/3
    hr=[]
    kr=[]
    lr=[]
    for i in range(len(l)):
        vec=N.array([h[i],k[i],l[i]],'Float64')
        vecr=N.dot(g,vec)
        hr.append(vecr[0])
        kr.append(vecr[1])
        lr.append(vecr[2])
        
    return N.array(hr),N.array(kr),N.array(lr)




def setup(Hpc,Kpc,Lpc):
    Hh,Kh,Lh=pseudocubic2hex(Hpc,Kpc,Lpc)
    if 0:
        print 'hex'
        for i in range(len(Hh)):
            print Hh[i],Kh[i],Lh[i]
    Hr,Kr,Lr=hex2rhomb(Hh,Kh,Lh)    
    if 0:
        print 'rhomb'
        for i in range(len(Hr)):
            print Hr[i],Kr[i],Lr[i]
    d=calcd(Hh,Kh,Lh)
    astar,alphastar,lattice=calcstar()
    #print astar,N.degrees(alphastar)
    return Hr,Kr,Lr,d,astar,alphastar,lattice,Hh,Kh,Lh

def mgnfacFe3psquared(x):
    y=( 0.3972*N.exp(-13.244*x**2)+0.6295*N.exp(-4.903*x**2)\
   -0.0314*N.exp(+.35*x**2)-0.0044)**2
    return y

def calc_struct(p,h,k,l,d,q,alphastar,astar,lattice,hh,kh,lh):
    """h,k,l are rhombohedral, hh,kh,lh are hexagonal"""
    #Fe1h=N.array([0.0000,  0.0000,  0.2200],'Float64')
    #Fe2h=N.array([0.0000,  0.0000,  0.7200],'Float64')
    Fe1r=N.array([0.2200,  0.2200,  0.2200],'Float64')
    Fe2r=N.array([0.7200,  0.7200,  0.7200],'Float64')
    scale,phi1=p
    
    cos2n1=calc_cos2n(phi1,h,k,l,d,alphastar,astar)
    #cos2n2=calc_cos2n(phi2,h,k,l,d,alphastar,astar)
    s1=(1-cos2n1)
    #s2=(1-cos2n2)
    flist=[]
    for i in range(len(h)):
        #print 'i',i
        f=0
        vec=[h[i],k[i],l[i]]
        dotp1=N.dot(vec,Fe1r)*2*pi
        dotp2=N.dot(vec,Fe2r)*2*pi
        f=N.exp(-1.0j*dotp1)-N.exp(-1.0j*dotp2)        
        f2=N.abs(f)**2
        #print 'f1',f,f2
        
        vec=[k[i],l[i],h[i]]
        dotp1=N.dot(vec,Fe1r)*2*pi
        dotp2=N.dot(vec,Fe2r)*2*pi
        f=N.exp(-1.0j*dotp1)-N.exp(-1.0j*dotp2)
        f2=f2+N.abs(f)**2
        #print 'f2',f,f2
        
        vec=[l[i],h[i],k[i]]
        dotp1=N.dot(vec,Fe1r)*2*pi
        dotp2=N.dot(vec,Fe2r)*2*pi
        f=N.exp(-1.0j*dotp1)-N.exp(-1.0j*dotp2)
        f2=f2+N.abs(f)**2
        #print 'f3',f,f2
        
        f2=f2/3
        #print 'f2inal',f2
        flist.append(f2)
    flist=N.array(flist)*s1*scale**2
    
    ff=mgnfacFe3psquared(q/4/pi)
    #print 'ff',ff
    Bf=.005
    flist=flist*ff*N.exp(-Bf*q**2/4/pi**2)
        
        
    return flist



def cost_func(p,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh,y,err):
    #ycalc=gen_function(p,x)
    ycalc=calc_struct(p,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh)
    dof=len(y)-len(p)
    fake_dof=len(y)
    #print 'chi',(y-ycalc)/err
    return (y-ycalc)/err#/N.sqrt(fake_dof)

def chisq_an(p,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh,y,err):
    chisq=cost_func(p,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh,y,err)
    return (chisq**2).sum()/len(y)

def myfunctlin(p, fjac=None,Hr=None,Kr=None,Lr=None\
               ,d=None,q=None,alphastar=None,astar=None\
               ,lattice=None,Hh=None,Kh=None,\
                Lh=None,y=None,err=None):
    # Parameter values are passed in "p"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    return [status, cost_func(p,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh,y,err)]


    
if __name__=="__main__":
    p0=N.array([100,N.radians(30)],'Float64')
    if 0:
        Hpc=N.array([1,1,2,1,.5],'float64')
        Kpc=N.array([1,1,-1,0,.5],'float64')
        Lpc=N.array([1,-2,-1,0,.5],'float64')
    if 1:
        data=N.array([[.5,-.5,1.5,55+6,5],            #192630
                     [.5,1.5,-.5,43+20,4],             #192638
                     [0.50,-1.50,-0.50,47+8,4],     #192635
                     [0.50,0.50,1.50,32+5,4],       #192629
                     [0.50,-1.50,-0.50,49+8,4],     #192662
                     [2.50,-0.50,-0.50,16+2,3],     #192661
                     [0.50,0.50, 2.50,18+1,3],      #192632
                     #[2.50,-0.50,-0.50,1,3], #why? #192631
                     [2.50,0.50,1.50,43,3],         #192634
                     [0.50, -1.50,0.50,36+17, 2],   #192628
                     [1.50, -1.50 ,-0.50,31+9,2],   #192624
                     [0.50, -1.50,  1.50,49, 2],    #192626
                     [0.50,1.50,  0.50,33+9, 3],    #192627
                     [0.5,2.50,1.50,30,3],          #192633
                     #[1.50,-1.50,0.50,33+0,2],     #192621 #th-2th
                     [2.50,0.50,1.50,30+0,1],     #192637
                     #[0.50,-1.50,-1.50,13+0,1],     #192660 #why
                     [0.50,1.50,-0.50,43+21,6]     #192636
                     #[0.50,1.50,1.50,10+5,2]     #192625
                     #[0.50,-0.50,0.50,29,2],  #th-2th
                     #[0.50,0.50,-0.50,36,2],   #th-2th
                     #[0.50,0.50,0.50,29,1]   #th-2th
                     ],'float64')
        Hpc=data[:,0]
        Kpc=data[:,1]
        Lpc=data[:,2]
        y=data[:,3]
        yerr=data[:,4]
    Hr,Kr,Lr,d,astar,alphastar,lattice,Hh,Kh,Lh=setup(Hpc,Kpc,Lpc)
    q=2*pi/d
    lam=2.35916
    y=y*(2*d/lam) #these are pure omega scans, so no lorenz factor? yes
    yerr=yerr*(2*d/lam)
    #y[-3:]=y[-3:]/(2*d[-3:]/lam) #these were w-2th scans, so they need the factor
    #yerr[-3:]=yerr[-3:]/(2*d[-3:]/lam)
    if 1:
        print 'data'
        for i in range(len(Hpc)):
            print Hpc[i],Kpc[i],Lpc[i],q[i],y[i],yerr[i]
        
        #Hpc=N.array([.5,.5,.5,.5,.5],'float64')
        #Kpc=N.array([.5,-1.5,2.5,-1.5,1.5],'float64')
        #Lpc=N.array([2.5,.5,1.5,-1.5,-.5],'float64')
        #y=N.array([18.4,55,30,13,63],'float64')
        #yerr=N.array([2.0,5.0,1.0,1,4],'float64')
        
    
    
    
    
    if 0:
        y=calc_struct(p0,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh)
        yerr=N.ones(y.shape,'Float64')
        
    
    parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
    parinfo=[]
    for i in range(len(p0)):
        parinfo.append(copy.deepcopy(parbase))
    for i in range(len(p0)): 
        parinfo[i]['value']=p0[i]
    parinfo[1]['fixed']=0 #fix slope
    parinfo[1]['limited']=[1,1]
    parinfo[1]['limits']=[0,pi/2]
    fa = {'y':y, 'err':yerr,
          'Hr':Hr
          ,'Kr':Kr
          ,'Lr':Lr
          ,'d':d
          ,'q':q
          ,'alphastar':alphastar,
          'astar':astar,
          'lattice':lattice,
          'Hh':Hh,
          'Kh':Kh,
          'Lh':Lh}
    
    lowerm=[0,0]
    upperm=[100,pi/2]
    p0,jmin=anneal(chisq_an,p0,args=(Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh,y,yerr),\
                      schedule='simple',lower=lowerm,upper=upperm,\
                      maxeval=None, maxaccept=None,dwell=500,maxiter=6000,T0=None)
    dof=len(y)-len(p0)
    fake_dof=len(y)
    chimin=(cost_func(p0,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh,y,yerr)**2).sum()
    chimin=chimin/dof if dof>0 else chimin/fake_dof 
    print 'p0_anneal',p0[0],N.degrees(p0[1])
    print 'chi_anneal', chimin
    
    
    
    
    m = mpfit(myfunctlin, p0, parinfo=parinfo,functkw=fa) 
    print 'status = ', m.status
    print 'params = ', m.params
    p1=m.params
    covariance=m.covar
    
    dof=len(y)-len(p1)
    fake_dof=len(y)
    chimin=(cost_func(p1,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh,y,yerr)**2).sum()
    chimin=chimin/dof if dof>0 else chimin/fake_dof
    ycalc=calc_struct(p1,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh)
    print 'chimin',chimin
    print 'p1',p1
    covariance=covariance*chimin #assume our model is good       
    scale=N.abs(p1[0])
    scale_sig=N.sqrt(covariance.diagonal()[0])
    angle=p1[1]
    angle_sig=N.sqrt(covariance.diagonal()[1])
    print 'scale',scale,'scale_sig',scale_sig
    print 'angle',N.degrees(angle),'angle_sig',angle_sig,N.degrees(angle_sig)%360
    
    if 1:
        print 'data'
        for i in range(len(Hpc)):
            print Hpc[i],Kpc[i],Lpc[i],q[i],y[i],yerr[i],ycalc[i]
    
    pylab.errorbar(q,y,yerr,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
    pylab.plot(q,ycalc,marker='s',linestyle='None',mfc='red')       
    pylab.show()    


    #f=calc_struct(p0,Hr,Kr,Lr,d,q,alphastar,astar,lattice,Hh,Kh,Lh)
    #print f
    #Hh=N.array([0,1,1,2],'float64')
    #Kh=N.array([1,1,1,-1],'float64')
    #Lh=N.array([2,1,-2,-1],'float64')

    
    
    
    