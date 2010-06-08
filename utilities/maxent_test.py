from __future__ import division
import numpy as N
import dct
import pylab
from openopt import NLP

A=1.0
xstep=0.05
zstep=0.05
pi=N.pi

def plotdensity(h,k,l,fq,xstep=0.01,zstep=0.01):
    x=N.arange(0.0,1.0,xstep)
    z=N.arange(0.0,1.0,zstep)
    xn=len(x)
    zn=len(z)
    X,Z=N.meshgrid(x,z)
    fsum=0.0
    P=N.zeros(X.shape)
    delta=.065;
    #%delta=.1;
    delta=.035;
    #outfile='c:\structfactors_density.dat'
    #fid=fopen([outfile],'w');
    for xia in range(xn):
        for zia in range(zn):
            fsum=0
            xi=x[xia]
            zi=z[zia]
            Aj=fq*N.sinc(2*delta*h)*N.sinc(2*delta*k)*N.sinc(2*delta*l)*pi**3
            cosqr=N.cos(2*pi*1*(h*xi+l*zi));
            #fsum=(Aj*cosqr).sum()
            fsum=(fq*cosqr).sum()
            #print xi,zi,'sum',fsum 
            #for i=1:n
            #    currf=fq(i);
            #    h=Qs(i,1);%/q(i);
            #    k=Qs(i,2);%/q(i);
            #    l=Qs(i,3);%/q(i);
            #    Aj=currf*N.sinc(2*pi*delta*h)*sinc(2*pi*delta*k)*sinc(2*pi*delta*l);   
            #    eiqr=cos(2*pi*1*(h*x(xi)/aa+l*z(zi)/cc));
            #    fsum=fsum+Aj*eiqr;
            #    %fprintf('h=%f k=%f l=%f currf=%f Aj%f
            #    %eiqr=%f\n',h*q(i),k*q(i),l*q(i),currf,Aj,eiqr)
            #end     
            #P[zi,xi]=fsum
            P[xia,zia]=fsum
                #fprintf(fid,'%3.5g  %3.5g  %3.5g  \n',xi,zi,P(zi,xi));
    #print P
    print P.shape
    P_fou=dct.dct2(P)
    if 0:
        pylab.pcolor(X,Z,P_fou)
        pylab.show()
    return X,Z,P


def pos_sum(p,h,k,l,fq,fqerr,x,z,cosmat_list):
    M=len(p)/2
    return p[0:M].sum()-A

def pos_sum_grad(p):
    M=len(p)/2
    return N.hstack((N.ones(M),N.zeros(M)))

def neg_sum(p,h,k,l,fq,fqerr,x,z,cosmat_list):
    M=len(p)/2
    return p[M::].sum()-A

def neg_sum_grad(p):
    M=len(p)/2
    return N.hstack((N.zeros(M),N.ones(M)))
 



def fourier_p(h,k,l,P,x,z,cosqr):
    #x=N.arange(0.0,1.0,xstep)
    #z=N.arange(0.0,1.0,zstep)
    xn=len(x)
    zn=len(z)
    #X,Z=N.meshgrid(x,z)
    fsum=0.0
    #delta=.065;
    #%delta=.1;
    #delta=.035;
    #outfile='c:\structfactors_density.dat'
    #fid=fopen([outfile],'w');
    fsum=0.0
    for xia in range(xn):
        for zia in range(zn):
            xi=x[xia]
            zi=z[zia]
            #Aj=fq*N.sinc(2*delta*h)*N.sinc(2*delta*k)*N.sinc(2*delta*l)*pi**3
            #cosqr=N.cos(2*pi*1*(h*xi+l*zi));
            fsum=fsum+P[xia,zia]*cosqr[xia,zia]  
            #print xi,zi,'sum',fsum,cosqr, P[xia,zia]
            #if abs(P[xia,zia])>0:
            #    print xi,zi,P[xia,zia]
    return 2*fsum/xn/zn


def transform_p(p,Mx,Mz,M):
    #pup_n=len(p)/2
    pup=p[0:M]
    pdown=p[M::]
    #print 'Mtrans',Mx,Mz,M
    #print 'pup',pup.shape
    #print 'pdown',pdown.shape
    #print 'p',p.shape
    p_up=pup.reshape(Mx,Mz)
    p_down=pdown.reshape(Mx,Mz)
    return p_up,p_down
     
     

def chisq(p,h,k,l,fq,fqerr,x,z,cosmat_list):
    global xstep
    global zstep
    M=len(p)/2
    Mx=1.0/xstep
    Mz=1.0/zstep
    #print M,Mx,Mz
    fsum_up=N.zeros(h.shape)
    fsum_down=N.zeros(h.shape)
    chi=N.zeros(h.shape)
    P_up,P_down=transform_p(p,Mx,Mz,M)
    for i in range(len(h)):
        fsum_up[i]=fourier_p(h[i],k[i],l[i],P_up,x,z,cosmat_list[i])
        fsum_down[i]=fourier_p(h[i],k[i],l[i],P_down,x,z,cosmat_list[i])
        fmodel=fsum_up[i]-fsum_down[i]
        chi[i]=(fmodel-fq[i])**2/fqerr[i]**2
        #print h[i],k[i],l[i],fq[i],chi[i]
    
    return chi.sum()-2*M
   


def chisq_grad(p,h,k,l,fq,fqerr,x,z,cosmat_list):
    global xstep
    global zstep
    M=len(p)/2
    Mx=1.0/xstep
    Mz=1.0/zstep
    #print M,Mx,Mz
    fsum_up=N.zeros(h.shape)
    fsum_down=N.zeros(h.shape)
    fmodel=N.zeros(h.shape)
    
    chi=N.zeros(h.shape)
    P_up,P_down=transform_p(p,Mx,Mz,M)

    x=N.arange(0.0,1.0,xstep)
    z=N.arange(0.0,1.0,zstep)
    xn=len(x)
    zn=len(z)
    grad=N.zeros(P_up.shape)
    for i in range(len(h)):
        fsum_up[i]=fourier_p(h[i],k[i],l[i],P_up,x,z,cosmat_list[i])
        fsum_down[i]=fourier_p(h[i],k[i],l[i],P_down,x,z,cosmat_list[i])
        fmodel[i]=fsum_up[i]-fsum_down[i]
    for xia in range(xn):
        for zia in range(zn):
            xi=x[xia]
            zi=z[zia]
            #Aj=fq*N.sinc(2*delta*h)*N.sinc(2*delta*k)*N.sinc(2*delta*l)*pi**3
            #cosqr=N.cos(2*pi*1*(h*xi+l*zi));
            #fsum=fsum+P[xia,zia]*cosqr  
            chi=0
            for i in range(len(h)):
                #fsum_up[i]=fourier_p(h[i],k[i],l[i],P_up)
                #fsum_down[i]=fourier_p(h[i],k[i],l[i],P_down)
                #fmodel=fsum_up[i]-fsum_down[i]
                cosqr=N.cos(2*pi*1*(h[i]*xi+l[i]*zi));
                chi=chi+2*(fmodel[i]-fq[i])/fqerr[i]**2*cosqr
                #print i
            grad[xia,zia]=chi.sum()
            
    grad_up=grad.flatten()
    grad_down=-grad_up
    grad=N.concatenate((grad_up,grad_down))
        #print h[i],k[i],l[i],fq[i],chi[i]
    
    return grad




def S_grad(p,h,k,l,fq,fqerr,x,z,cosmat_list):
    global xstep
    global zstep
    global A
    M=int(len(p)/2)
    Mx=1.0/xstep
    Mz=1.0/zstep
    #print M,Mx,Mz
    #print '2M',2*M
    #fsum_up=N.zeros(h.shape)
    #fsum_down=N.zeros(h.shape)
    #fmodel=N.zeros(h.shape)
    gradient=N.zeros(2*M)
    pos=range(M)
    posm=range(M,2*M)
    #print 'pos',pos
    #print 'posm',posm
    hrows=range(2*M)
    hcols=hrows
    gradient[pos]=N.log(A)-N.log(p[0:M])
    gradient[posm]=N.log(A)-N.log(p[M+1:2*M])
    #P_up,P_down=transform_p(p,Mx,Mz,M)    
    #print 'gradient'
    return -gradient


def S_hessian(p,h,k,l,fq,fqerr,x,z,cosmat_list):
    global xstep
    global zstep
    print 'hessian'
    M=int(len(p)/2)
    Mx=1.0/xstep
    Mz=1.0/zstep
    #print M,Mx,Mz
    #print '2M',2*M
    #fsum_up=N.zeros(h.shape)
    #fsum_down=N.zeros(h.shape)
    #fmodel=N.zeros(h.shape)
    hessian=N.zeros(2*M)
    pos=range(M)
    posm=range(M,2*M)
    #print 'pos',pos
    #print 'posm',posm
    hrows=range(2*M)
    hcols=hrows
    hessian[pos]=-1./p[0:M]
    hessian[posm]=-1/p[M+1:2*M]
    #P_up,P_down=transform_p(p,Mx,Mz,M)    
    
    return hrows,hcols,hessian


def precompute_r():
    global xstep
    global zstep
    x=N.arange(0.0,1.0,xstep)
    z=N.arange(0.0,1.0,zstep)
    xn=len(x)
    zn=len(z)
    #X,Z=N.meshgrid(x,z)
    return x,z

def precompute_cos(h,k,l,x,z):
   # x=N.arange(0.0,1.0,xstep)
   # z=N.arange(0.0,1.0,zstep)
    xn=len(x)
    zn=len(z)
    #X,Z=N.meshgrid(x,z)
    #fsum=0.0
    #delta=.065;
    #%delta=.1;
    #delta=.035;
    #outfile='c:\structfactors_density.dat'
    #fid=fopen([outfile],'w');
    #fsum=0.0
    coslist=[]
    cosmat_list=[]
    for i in range(len(h)):
        hc=h[i]
        kc=k[i]
        lc=l[i]
        cosmat=[]#
        cosmat_2d=N.zeros((xn,zn))
        for xia in range(xn):
            for zia in range(zn):
                xi=x[xia]
                zi=z[zia]
                #Aj=fq*N.sinc(2*delta*h)*N.sinc(2*delta*k)*N.sinc(2*delta*l)*pi**3
                cosqr=N.cos(2*pi*1*(hc*xi+lc*zi))
                cosmat.append(cosqr)
                cosmat_2d[xia,zia]=cosqr
        coslist.append(N.hstack((cosmat,cosmat)))
        cosmat_list.append(cosmat_2d)  
    return coslist,cosmat_list

def chisq_hessian(p,fqerr,v,coslist,flist):
    global xstep
    global zstep
    #v is the vector we are muliplying by
    M=len(p)/2
    Mx=1.0/xstep
    Mz=1.0/zstep
    #print M,Mx,Mz
    vlen=len(v)
    plen=len(p)
    vout=N.zeros(vlen)
    
    xn=len(x)
    zn=len(z)
    print 'sizes'
    print 'cosk',len(coslist[0])
    print 'flist', len(flist)
    print 'fqerr', len(fqerr)
    print 'v',len(v)
    print 'p',len(p)
    for i in range(vlen):
        for j in range(vlen):
            tot=0
            al=0
            for cosk in coslist:
                tot=tot+cosk[i]*cosk[j]*flist[i]*flist[j]/fqerr[al]**2
                al=al+1;
            print 'tot',tot,v[j]
            vout[i]=vout[i]+v[j]*tot
            print 'vout',i,j,vout[i]
    vout=2*vout/M**2
    return vout

def Entropy(p2,h,k,l,fq,fqerr,x,z,cosmat_list):
    return (p2*(N.log(p2/A)-1)).sum()


def max_wrap(p,coslist,cosmat_list,x,z):
    l1,l2,l3=p[0:2]
    p2=p[3::]
    chisqr=chisq(p,h,k,l,fq,fqerr,x,z,cosmat_list,xstep=0.1,zstep=0.1)
    pos=pos_sum(p,A=1.0)
    neg=neg_sum(p,A=1.0)
    ent=Entropy(p2)
    f=ent+l1*chisqr+l2*pos+l3*neg    
    return f

if __name__=="__main__":
    global xstep
    global zstep
    myfilestr=r'c:\structfactors.dat'
    bob=N.loadtxt(myfilestr)
    #print bob
    #print bob.shape
    h,k,l,fq,fqerr=N.loadtxt(myfilestr).T
    #print h
    #X,Z,P=plotdensity(h,k,l,fq)
    #pu=P.flatten()
    #pd=N.zeros(len(pu))
    #p=N.concatenate((pu,pd))
    #xstep=.05
    #zstep=.05
    Mx=1.0/xstep
    Mz=1.0/zstep
    M=Mx*Mz
    print 'M', M,Mx,Mz
    p0=N.ones(M*2)
    #print 'len pu',len(pu)
    #print 'len pd',len(pd)
    #print 'len p',len(p)
    
    x,z=precompute_r()
    X,Z=N.meshgrid(x,z)
    coslist,cosmat_list=precompute_cos(h,k,l,x,z)
    #print 'coslist',coslist[0]
    flist=N.ones(len(p0))
    
    
    flist[M::]=-flist[M::]
    #vout=chisq_hessian(p,fqerr,p,coslist,flist)
    #print 'vout', vout
    
#    print 'pos',pos_sum(p0)
#    print 'neg',neg_sum(p0)
    p = NLP(Entropy, p0, maxIter = 1e3, maxFunEvals = 1e5)
    #p = NLP(chisq, p0, maxIter = 1e3, maxFunEvals = 1e5)
    # f(x) gradient (optional):
#    p.df = S_grad
#    p.d2f=S_hessian
#    p.userProvided.d2f=True
    
    
    # lb<= x <= ub:
    # x4 <= -2.5
    # 3.5 <= x5 <= 4.5
    # all other: lb = -5, ub = +15
    #p.lb =1e-7*N.ones(p.n)
    #p.ub = N.ones(p.n)
    p.lb =1e-7*N.ones(p0.shape)
    p.ub = N.ones(p0.shape)
    #p.ub[4] = -2.5
    #p.lb[5], p.ub[5] = 3.5, 4.5

# non-linear inequality constraints c(x) <= 0
# 2*x0^4 <= 1/32
# x1^2+x2^2 <= 1/8
# x25^2 +x25*x35 + x35^2<= 2.5

#p.c = lambda x: [2* x[0] **4-1./32, x[1]**2+x[2]**2 - 1./8, x[25]**2 + x[35]**2 + x[25]*x[35] -2.5]
# other valid c:
# p.c = [lambda x: c1(x), lambda x : c2(x), lambda x : c3(x)]
# p.c = (lambda x: c1(x), lambda x : c2(x), lambda x : c3(x))
# p.c = lambda x: numpy.array(c1(x), c2(x), c3(x))
# def c(x):
#      return c1(x), c2(x), c3(x)
# p.c = c



# non-linear equality constraints h(x) = 0
# 1e6*(x[last]-1)**4 = 0
# (x[last-1]-1.5)**4 = 0
#h1 = lambda x: 1e4*(x[-1]-1)**4
#h2 = lambda x: (x[-2]-1.5)**4
#p.h = [h1, h2]
    h_args=(h,k,l,fq,fqerr,x,z,cosmat_list)
    p.h=[pos_sum,neg_sum,chisq]
#    p.h=[pos_sum,neg_sum]
    p.args.h=h_args
    p.args.f=(h,k,l,fq,fqerr,x,z,cosmat_list)
    #p.args.f=h_args
# dh(x)/dx: non-lin eq constraints gradients (optional):
#def DH(x):
#    r = zeros((2, p.n))
#    r[0, -1] = 1e4*4 * (x[-1]-1)**3
#    r[1, -2] = 4 * (x[-2]-1.5)**3
#    return r
#p.dh = DH
#    p.dh=[chisq_grad,pos_sum_grad,]
    p.contol = 1e-2#3 # required constraints tolerance, default for NLP is 1e-6

# for ALGENCAN solver gradtol is the only one stop criterium connected to openopt
# (except maxfun, maxiter)
# Note that in ALGENCAN gradtol means norm of projected gradient of  the Augmented Lagrangian
# so it should be something like 1e-3...1e-5
    p.gradtol = 1e-3#5 # gradient stop criterium (default for NLP is 1e-6)
    #print 'maxiter', p.maxiter
    #print 'maxfun', p.maxfun
    p.maxiter=10
#    p.maxfun=100
    
# see also: help(NLP) -> maxTime, maxCPUTime, ftol and xtol
# that are connected to / used in lincher and some other solvers

    # optional: check of user-supplied derivatives
    #p.checkdf()
    #p.checkdc()
    #p.checkdh()

# last but not least:
# please don't forget,
# Python indexing starts from ZERO!!

    p.plot = 0
    p.iprint = 1
    #p.df_iter = 50
    p.maxTime = 4000
    print 'solving'
    r = p.solve('algencan')
    print 'done'
    pout=r.xf
    print 'solution:', pout

    print len(pout)
    
    P_up,P_down=transform_p(pout,Mx,Mz,M)
    P=P_up-P_down
    
    
    
    
    
    if 0:
        chi=chisq(p,h,k,l,fq,fqerr,x,z,cosmat_list,xstep=0.1,zstep=0.1)
        print 'chi',chi
        grad=chisq_grad(p,h,k,l,fq,fqerr)
        print 'gradient',grad
        sgrad_rows,sgrad_cols,s_grad=S_grad(p,h,k,l,fq,fqerr,A=1)
        print 'S_grad', s_grad
        srows,scols,s_hess=S_hessian(p,h,k,l,fq,fqerr)
        print 'S_hessian',s_hess
    if 1:
        pylab.pcolor(X,Z,P)
        pylab.show()
    if 0:    
        fsum=fourier_p(h[0],k[0],l[0],P)
        fsum=N.zeros(h.shape)
    if 0:
        for i in range(len(h)):
            fsum[i]=fourier_p(h[i],k[i],l[i],P)
            print h[i],k[i],l[i],fq[i],fsum[i],fq[i]/fsum[i]
    
    if 0:
        q=N.sqrt(h**2+l**2)  #Note, 107 is off by a factor of 2!
        pylab.plot(q,fsum,'s')
        #pylab.twinx()
        pylab.plot(q,fq,'s')
        pylab.show()
    if 0:
        myfilestr=r'c:\structfactors_density.dat'
        x,y,z=N.loadtxt(myfilestr).T
        bob=N.loadtxt(myfilestr).T
        print bob.shape
        pylab.pcolormesh(x,y,z)
        pylab.show()