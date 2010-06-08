import numpy as N
import math
import pylab
import unittest
from matplotlib.patches import Ellipse
eps=1e-3
pi=N.pi

def autovectorized(f):
     """Function decorator to do vectorization only as necessary.
     vectorized functions fail for scalar inputs."""
     def wrapper(input):
         if N.isscalar(input)==False:
             return N.vectorize(f)(input)
         return f(input)
     return wrapper



@autovectorized
def myradians(x):
    return math.radians(x)

#vecradians = N.vectorize(myradians, otypes=[double]) 

def sign(x):
    if x>0:
         ret=1
    if x<0:
        ret=-1
    if x==0:
        ret=0
    return ret

def blkdiag(g):
    "Returns a block diagonal matrix, given a list of square matrices, g"
    glen=len(g)
    n=0
    for i in range(glen):
   #     print g[i]
        n=n+g[i].shape[0]
   #     print n


    gout=N.zeros((n,n))
    offset=0
    for i in range(glen):
        currblock=g[i]
        lenx,leny=currblock.shape
    #    print i
    #    print lenx, leny
        for x in range(lenx):
            for y in range(leny):
                gout[x+offset,y+offset]=currblock[x,y]
     #           print gout
        offset=offset+lenx
    return gout


def similarity_transform(A,B):
    G=N.dot(B,A.transpose())
    G2=N.dot(A,G)
    return G2

class instrument:
    def __init__(self):
            self.tau_list={'pg(002)':1.87325, \
                            'pg(004)':3.74650, \
                            'ge(111)':1.92366, \
                            'ge(220)':3.14131, \
                            'ge(311)':3.68351, \
                            'be(002)':3.50702, \
                            'pg(110)':5.49806}
            #self.tau=self.tau_list[tau]
            return
    def get_tau(self,tau):
        return self.tau_list[tau]

class lattice:
    def __init__(self, a=N.array([2*N.pi, 2*N.pi], 'd'), \
                 b=N.array([2*N.pi, 2*N.pi], 'd'), \
                 c=N.array([2*N.pi, 2*N.pi], 'd'), \
                 alpha=N.array([90, 90], 'd'), \
                 beta=N.array([90, 90], 'd'), \
                 gamma=N.array([90, 90], 'd'), \
                 orient1=N.array([[1, 0, 0], [1, 0, 0]], 'd'), \
                 orient2=N.array([[0, 1, 0], [0, 1, 0]], 'd')):
        self.a=a
        self.b=b
        self.c=c
        self.alphad=alpha
        self.betad=beta
        self.gammad=gamma
        self.alpha=myradians(alpha)
        self.beta=myradians(beta)
        self.gamma=myradians(gamma)
        self.star()
        self.gtensor('lattice')
        self.gtensor('latticestar')
        self.npts=N.size(a)
        self.orient1=orient1.transpose()
        self.orient2=orient2.transpose()
        self.StandardSystem()
        return

    def scalar(self, x1, y1, z1, x2, y2, z2, lattice):
        "calculates scalar product of two vectors"
        if lattice=='lattice':
            a=self.a
            b=self.b
            c=self.c
            alpha=self.alpha
            beta=self.beta
            gamma=self.gamma
        if lattice=='latticestar':
            a=self.astar
            b=self.bstar
            c=self.cstar
            alpha=self.alphastar
            beta=self.betastar
            gamma=self.gammastar
        
        s=x1*x2*a**2+y1*y2*b**2+z1*z2*c**2+\
           (x1*y2+x2*y1)*a*b*N.cos(gamma)+\
           (x1*z2+x2*z1)*a*c*N.cos(beta)+\
           (z1*y2+z2*y1)*c*b*N.cos(alpha)
        return s

    def star(self):
        "Calculate unit cell volume, reciprocal cell volume, reciprocal lattice parameters"
        V=2*self.a*self.b*self.c*\
        N.sqrt(N.sin((self.alpha+self.beta+self.gamma)/2)*\
                N.sin((-self.alpha+self.beta+self.gamma)/2)*\
                N.sin((self.alpha-self.beta+self.gamma)/2)*\
                N.sin((self.alpha+self.beta-self.gamma)/2))
        self.Vstar=(2*N.pi)**3/V;
        self.astar=2*N.pi*self.b*self.c*N.sin(self.alpha)/V
        self.bstar=2*N.pi*self.a*self.c*N.sin(self.beta)/V
        self.cstar=2*N.pi*self.b*self.a*N.sin(self.gamma)/V
        self.alphastar=N.arccos((N.cos(self.beta)*N.cos(self.gamma)-\
                                 N.cos(self.alpha))/ \
                                (N.sin(self.beta)*N.sin(self.gamma)))
        self.betastar= N.arccos((N.cos(self.alpha)*N.cos(self.gamma)-\
                                 N.cos(self.beta))/ \
                                (N.sin(self.alpha)*N.sin(self.gamma)))
        self.gammastar=N.arccos((N.cos(self.alpha)*N.cos(self.beta)-\
                               N.cos(self.gamma))/ \
                              (N.sin(self.alpha)*N.sin(self.beta)))
        self.V=V
        return

    def angle2(self, x, y, z, h, k, l):
        "Calculate the angle between vectors in real and reciprocal space"
        "x,y,z are the fractional cell coordinates of the first vector,"
        "h,k,l are Miller indices of the second vector"
        phi=N.arccos(2*pi*(h*x+k*y+l*z)/self.modvec(x, y, z, 'lattice')/self.modvec(h, k, l, 'latticestar'))
        return phi


    def angle(self, x1, y1, z1, x2, y2, z2, lattice):
        "Calculate the angle between vectors in real and reciprocal space"
        "xi,yi,zi are the fractional cell coordinates of the vectors"
        phi=N.arccos(self.scalar(x1, y1, z1, x2, y2, z2, lattice)/self.modvec(x1, y1, z1, lattice)/self.modvec(x1, y1, z1, lattice))    
        return phi
    
    def modvec(self, x, y, z, lattice):
        "Calculates modulus of a vector defined by its fraction cell coordinates"
        "or Miller indexes"
        m=N.sqrt(self.scalar(x, y, z, x, y, z, lattice))
        return m

    def gtensor(self, lattice):
        "calculates the metric tensor of a lattice"
        g=N.zeros((3, 3, N.size(self.a)), 'd')
        #print 'shape ', g.shape
        if lattice=='lattice':
            a=self.a
            b=self.b
            c=self.c
            alpha=self.alpha
            beta=self.beta
            gamma=self.gamma
        if lattice=='latticestar':
            a=self.astar
            b=self.bstar
            c=self.cstar
            alpha=self.alphastar
            beta=self.betastar
            gamma=self.gammastar
        g[0, 0, :]=a**2;
        g[0, 1, :]=a*b*N.cos(gamma)
        g[0, 2, :]=a*c*N.cos(beta)

        g[1, 0, :]=g[0, 1, :]
        g[1, 1, :]=b**2
        g[1, 2, :]=c*b*N.cos(alpha)

        g[2, 0, :]=g[0, 2, :]
        g[2, 1, :]=g[1, 2, :]
        g[2, 2, :]=c**2
        if lattice=='lattice':
            self.g=g
#            print 'lattice'
        if lattice=='latticestar':
            self.gstar=g
#            print 'latticestar'
#        print g
        return

    def reciprocate(self, x, y, z, lattice):
        "calculate miller indexes of a vector defined by its fractional cell coords"
        if lattice=='lattice':
            g=self.g
        if lattice=='latticestar':
            g=self.gstar
        h=g[0, 0, :]*x+g[1, 0, :]*y+g[2, 0, :]*z;
        k=g[0, 1, :]*x+g[1, 1, :]*y+g[2, 1, :]*z;
        l=g[0, 2, :]*x+g[1, 2, :]*y+g[2, 2, :]*z;
        return h, k, l

    def vector(self, x1, y1, z1, x2, y2, z2, lattice):
        "calculates the fractional cell coordinates or Miller indexes of a vector"
        "product of two vectors, defined by their fractional cell coordinates or "
        "Miller idexes"
        if lattice=='lattice':
            g=self.gstar
            V=self.Vstar
        if lattice=='latticestar':
            g=self.g
            V=self.V
        g=g*V/(2*N.pi)**2
        x=y1*z2*g[0, 0, :]-z1*y2*g[0, 0, :]-x1*z2*g[1, 0, :]+z1*x2*g[1, 0, :]\
           +x1*y2*g[2, 0, :]-y1*x2*g[2, 0, :]
        y=y1*z2*g[0, 1, :]-z1*y2*g[0, 1, :]-x1*z2*g[1, 1, :]+z1*x2*g[1, 1, :]\
           +x1*y2*g[2, 1, :]-y1*x2*g[2, 1, :]
        z=y1*z2*g[0, 2, :]-z1*y2*g[0, 2, :]-x1*z2*g[1, 2, :]+z1*x2*g[1, 2, :]\
           +x1*y2*g[2, 2, :]-y1*x2*g[2, 2, :]
        return x,y,z

    def StandardSystem(self):
#        npts=self.npts
#        orient1=N.zeros((3,npts),'d')
#        orient2=N.zeros((3,npts),'d')
        orient1=self.orient1
        orient2=self.orient2
#        print 'orient1'
#        print orient1
#        print 'orient2 '
#        print orient2        
        modx=self.modvec(orient1[0, :], orient1[1, :], orient1[2, :], 'latticestar')
        x=N.copy(orient1)
        x[0, :]=x[0, :]/modx; # First unit basis vector
        x[1, :]=x[1, :]/modx;
        x[2, :]=x[2, :]/modx;
        
        proj=self.scalar(orient2[0, :], orient2[1, :], orient2[2, :], \
                    x[0, :], x[1, :], x[2, :], 'latticestar')
        
        y=N.copy(orient2)
        y[0, :]=y[0, :]-x[0, :]*proj; 
        y[1, :]=y[1, :]-x[1, :]*proj;
        y[2, :]=y[2, :]-x[2, :]*proj;

        mody=self.modvec(y[0, :], y[1, :], y[2, :], 'latticestar');

#    check for collinearity of orienting vectors
# implement later!!!
#        if ~isempty(find(mody<=0))
#        error('??? Fatal error: Orienting vectors are colinear!');
#        print 'where '+str((N.where(mody<=0)[0].size))
#        print 'mody '
#        print  mody
        try:
#            print N.where(mody<=eps)[0].size
            if N.where(mody<=eps)[0].size>0:
                print 'ValueError'
                raise ValueError
            y[0, :]=y[0, :]/mody; # Second unit basis vector
            y[1, :]=y[1, :]/mody;
            y[2, :]=y[2, :]/mody;
    
            z=N.copy(y);
    
            z[0, :]=x[1, :]*y[2, :]-y[1, :]*x[2, :];
            z[1, :]=x[2, :]*y[0, :]-y[2, :]*x[0, :];
            z[2, :]=-x[1, :]*y[0, :]+y[1, :]*x[0, :];
    
            proj=self.scalar(z[0, :], z[1, :], z[2, :], x[0, :], x[1, :], x[2, :], 'latticestar');
    
            z[0, :]=z[0, :]-x[0, :]*proj; 
            z[1, :]=z[1, :]-x[1, :]*proj;
            z[2, :]=z[2, :]-x[2, :]*proj;
    
            proj=self.scalar(z[0, :], z[1, :], z[2, :], y[0, :], y[1, :], y[2, :], 'latticestar');
    
            z[0, :]=z[0, :]-y[0, :]*proj; 
            z[1, :]=z[1, :]-y[1, :]*proj;
            z[2, :]=z[2, :]-y[2, :]*proj;
    
            modz=self.modvec(z[0, :], z[1, :], z[2, :], 'latticestar');
    
            z[0, :]=z[0, :]/modz; #% Third unit basis vector
            z[1, :]=z[1, :]/modz;
            z[2, :]=z[2, :]/modz;     
            
            self.x=x
            self.y=y
            self.z=z    
        except ValueError:
            print 'ORIENTATION VECTORS ARE COLLINEAR x,y,z not set'    
        return
    
    def S2R(self, qx, qy, qz):
        "Given cartesian coordinates of a vector in the S System, calculate its Miller indexes."
        x=self.x
        y=self.y
        z=self.z
        H=qx*x[0, :]+qy*y[0, :]+qz*z[0, :];
        K=qx*x[1, :]+qy*y[1, :]+qz*z[1, :];
        L=qx*x[2, :]+qy*y[2, :]+qz*z[2, :];
        q=N.sqrt(qx**2+qy**2+qz**2);
        return H, K, L, q
    
    def R2S(self, H, K, L):
        "Given reciprocal-space coordinates of a vecotre, calculate its coordinates in the Cartesian space."
        x=self.x
        y=self.y
        z=self.z
        qx=self.scalar(H, K, L, x[0, :], x[1, :], x[2, :], 'latticestar');
        qy=self.scalar(H, K, L, y[0, :], y[1, :], y[2, :], 'latticestar');
        qz=self.scalar(H, K, L, z[0, :], z[1, :], z[2, :], 'latticestar');
        q=self.modvec(H, K, L, 'latticestar');
        return qx, qy, qz, q
    
    def ResMat(self, Q, W,EXP):
        CONVERT1=0.4246609*N.pi/60/180;
        CONVERT2=2.072;
        npts=self.npts
        RM=N.zeros((4, 4, npts),'d');
        R0=N.zeros((1, npts),'d');
        RM_=N.zeros((4, 4),'d');
        D=N.zeros((8, 13),'d');
        d=N.zeros((4, 7),'d');
        T=N.zeros((4, 13),'d');
        t=N.zeros((2, 7),'d');
        A=N.zeros((6, 8),'d');
        C=N.zeros((4, 8),'d');
        B=N.zeros((4, 6),'d');

        for ind in range(npts):
#            %Assign default values and decode parameters
            moncor=1;
            if 'moncor' in EXP[ind]:
                moncor = EXP[ind]['moncor']
            alpha = EXP[ind]['hcol']*CONVERT1;
            beta =  EXP[ind]['vcol']*CONVERT1;
            mono=EXP[ind]['mono']
            etam = mono['mosaic']*CONVERT1;
            etamv=etam
            if 'vmosaic' in mono:
                etamv = mono['vmosaic']*CONVERT1;
            ana=EXP[ind]['ana'];
            etaa = ana['mosaic']*CONVERT1;
            etaav=etaa;
            if 'vmosaic' in ana:
                etaav = ana['vmosaic']*CONVERT1;
            sample=EXP[ind]['sample'];
            infin=-1;
            if 'infin' in EXP[ind]:
                infin = EXP[ind]['infin']
            efixed=EXP[ind]['efixed']
            epm=1
            if 'dir1' in EXP[ind]:
                epm= EXP[ind]['dir1'];
            ep=1;
            if 'dir2' in EXP[ind]:
                ep= EXP[ind]['dir2'];
            monitorw=1;
            monitorh=1;
            beamw=1;
            beamh=1;
            monow=1;
            monoh=1;
            monod=1;
            anaw=1;
            anah=1;
            anad=1;
            detectorw=1;
            detectorh=1;
            sshape=N.eye(3);
            L0=1;
            L1=1;
            L1mon=1;
            L2=1;
            L3=1;        
            monorv=1e6;
            monorh=1e6;
            anarv=1e6;
            anarh=1e6;
            if 'beam' in EXP[ind]:
                beam=EXP[ind]['beam'];
                if 'width' in beam:
                    beamw=beam['width']**2;
                if 'height' in beam:
                    beamh=beam['height']**2
            bshape=N.diag([beamw,beamh]);
            if 'monitor' in EXP[ind]:
                monitor=EXP[ind]['monitor'];
                if 'width' in monitor:
                    monitorw=monitor['width']**2
                monitorh=monitorw;
                if 'height' in monitor:
                    monitorh=monitor['height']**2;
            monitorshape=N.diag([monitorw,monitorh]);
            if 'detector' in EXP[ind]:
                detector=EXP[ind]['detector'];
                if 'width' in detector:
                    detectorw=detector['width']**2;
                if 'height' in detector:
                    detectorh=detector['height']**2;
            dshape=N.diag([detectorw,detectorh]);
            if 'width' in mono:
                monow=mono['width']**2;
            if 'height' in mono:
                monoh=mono['height']**2;
            if 'depth' in mono:
                monod=mono.depth**2;
            mshape=N.diag([monod,monow,monoh]);
            if 'width' in ana: 
                anaw=ana['width']**2;
            if 'height' in ana:
                anah=ana['height']**2;
            if 'depth' in ana:
                anad=ana['depth']**2;
            ashape=N.diag([anad,anaw,anah]);
            if 'shape' in sample:
                sshape=sample['shape'];
            if 'arms' in EXP[ind]:
                arms=EXP[ind]['arms'];
                L0=arms[0];
                L1=arms[2];
                L2=arms[3];
                L3=arms[4];
                L1mon=L1;
                if len(arms)>3:
                    L1mon=arms[4];
            if 'rv' in mono:
                monorv=mono['rv'];
            if 'rh' in mono:
                monorh=mono['rh'];
            if 'rv' in ana:
                anarv=ana['rv'];
            if 'rh' in ana:
                anarh=ana['rh'];
            method=0;
            if 'method' in EXP[ind]:
                method=EXP[ind]['method'];
            myinstrument=instrument()
            taum=myinstrument.get_tau(mono['tau']);
            taua=myinstrument.get_tau(ana['tau']);
        
            horifoc=-1;
            if 'horifoc' in EXP[ind]:
                horifoc=EXP[ind]['horifoc'];
            if horifoc==1: 
                alpha[2]=alpha[2]*N.sqrt(8*N.log(2)/12); 
#            %---------------------------------------------------------------------------------------------
#            %Calculate angles and energies
            w=W[ind];
            q=Q[ind];
            ei=efixed;
            ef=efixed;
            if infin>0:
                 ef=efixed-w
            else:
                 ei=efixed+w; 
            ki = N.sqrt(ei/CONVERT2);
            kf = N.sqrt(ef/CONVERT2);
            thetam=N.arcsin(taum/(2*ki))*sign(epm); 
            thetaa=N.arcsin(taua/(2*kf))*sign(ep); 
            s2theta=-N.arccos( (ki**2+kf**2-q**2)/(2*ki*kf));# %2theta sample
            thetas=s2theta/2;
            phi=N.arctan2(-kf*N.sin(s2theta), ki-kf*N.cos(s2theta)); #%Angle from ki to Q
        
 #           %---------------------------------------------------------------------------------------------
#            %Calculate beam divergences defined by neutron guides
            pi=N.pi
            if alpha[0]<0:
                  alpha[0]=-alpha[0]*2*0.427/ki*pi/180; 
            if alpha[1]<0:
                  alpha[1]=-alpha[1]*2*0.427/ki*pi/180; 
            if alpha[2]<0:
                  alpha[2]=-alpha[2]*2*0.427/ki*pi/180; 
            if alpha[3]<0:
                  alpha[3]=-alpha[3]*2*0.427/ki*pi/180; 
            
            if beta[0]<0:
                  beta[0]=-beta[0]*2*0.427/ki*pi/180; 
            if beta[1]<0:
                  beta[1]=-beta[1]*2*0.427/ki*pi/180; 
            if beta[2]<0:
                  beta[2]=-beta[2]*2*0.427/ki*pi/180; 
            if beta[3]<0:
                  beta[3]=-beta[3]*2*0.427/ki*pi/180; 
            
#            %---------------------------------------------------------------------------------------------
#            %Rededine sample geometry
            psi=thetas-phi;# %Angle from sample geometry X axis to Q
            rot=N.zeros((3,3));
            rot[0,0]=N.cos(psi);
            rot[1,1]=N.cos(psi);
            rot[0,1]=N.sin(psi);
            rot[1,0]=-N.sin(psi);
            rot[2,2]=1;
            sshape=N.dot(rot.transpose(),N.dot(sshape,rot)); #matrix multiplication?   
#            %---------------------------------------------------------------------------------------------
#            %Definition of matrix G    
            G=1.0/N.array([alpha[0],alpha[1],beta[0],beta[1],alpha[2],alpha[3],beta[2],beta[3]])**2;
            G=N.diag(G);
#            %---------------------------------------------------------------------------------------------
#            %Definition of matrix F    
            F=1.0/N.array([etam,etamv,etaa,etaav])**2;
            F=N.diag(F);
#            %---------------------------------------------------------------------------------------------
#            %Definition of matrix A
            A[0,0]=ki/2/N.tan(thetam);
            A[0,1]=-A[0,0];
            A[3,4]=kf/2/N.tan(thetaa);
            A[3,5]=-A[3,4];
            A[1,1]=ki;
            A[2,3]=ki;
            A[4,4]=kf;
            A[5,6]=kf;
#            %---------------------------------------------------------------------------------------------
#            %Definition of matrix C
            C[0,0]=1.0/2;
            C[0,1]=1.0/2;
            C[2,4]=1.0/2;
            C[2,5]=1.0/2;
            C[1,2]=1.0/(2*N.sin(thetam));
            C[1,3]=-C[1,2];# %mistake in paper
            C[3,6]=1.0/(2*N.sin(thetaa));
            C[3,7]=-C[3,6];
#            %---------------------------------------------------------------------------------------------
#            %Definition of matrix B
            B[0,0]=N.cos(phi);
            B[0,1]=N.sin(phi);
            B[0,3]=-N.cos(phi-s2theta);
            B[0,4]=-N.sin(phi-s2theta);
            B[1,0]=-B[0,1];
            B[1,1]=B[0,0];
            B[1,3]=-B[0,4];
            B[1,4]=B[0,3];
            B[2,2]=1.0;
            B[2,5]=-1.0;
            B[3,0]=2*CONVERT2*ki;
            B[3,3]=-2*CONVERT2*kf;
#            %---------------------------------------------------------------------------------------------
#            %Definition of matrix S
            Sinv=blkdiag([bshape,mshape,sshape,ashape,dshape]);# %S-1 matrix        
            S=N.linalg.inv(Sinv);
#            %---------------------------------------------------------------------------------------------
#            %Definition of matrix T
            T[0,0]=-1./(2*L0); # %mistake in paper
            T[0,2]=N.cos(thetam)*(1./L1-1./L0)/2;
            T[0,3]=N.sin(thetam)*(1./L0+1./L1-2./(monorh*N.sin(thetam)))/2;
            T[0,5]=N.sin(thetas)/(2*L1);
            T[0,6]=N.cos(thetas)/(2*L1);
            T[1,1]=-1./(2*L0*N.sin(thetam));
            T[1,4]=(1./L0+1./L1-2*N.sin(thetam)/monorv)/(2*N.sin(thetam));
            T[1,7]=-1./(2*L1*N.sin(thetam));
            T[2,5]=N.sin(thetas)/(2*L2);
            T[2,6]=-N.cos(thetas)/(2*L2);
            T[2,8]=N.cos(thetaa)*(1./L3-1./L2)/2;
            T[2,9]=N.sin(thetaa)*(1./L2+1./L3-2/(anarh*N.sin(thetaa)))/2;
            T[2,11]=1./(2*L3);
            T[3,7]=-1./(2*L2*N.sin(thetaa));
            T[3,10]=(1./L2+1./L3-2*N.sin(thetaa)/anarv)/(2*N.sin(thetaa));
            T[3,12]=-1./(2*L3*N.sin(thetaa));
#            %---------------------------------------------------------------------------------------------
#            %Definition of matrix D
#            % Lots of index mistakes in paper for matix D
            D[0,0]=-1./L0;
            D[0,2]=-N.cos(thetam)/L0;
            D[0,3]=N.sin(thetam)/L0;
            D[2,1]=D[0,0];
            D[2,4]=-D[0,0];
            D[1,2]=N.cos(thetam)/L1;
            D[1,3]=N.sin(thetam)/L1;
            D[1,5]=N.sin(thetas)/L1;
            D[1,6]=N.cos(thetas)/L1;
            D[3,4]=-1./L1;
            D[3,7]=-D[3,4];
            D[4,5]=N.sin(thetas)/L2;
            D[4,6]=-N.cos(thetas)/L2;
            D[4,8]=-N.cos(thetaa)/L2;
            D[4,9]=N.sin(thetaa)/L2;
            D[6,7]=-1./L2;
            D[6,10]=-D[6,7];
            D[5,8]=N.cos(thetaa)/L3;
            D[5,9]=N.sin(thetaa)/L3;
            D[5,11]=1./L3;
            D[7,10]=-D[5,11];
            D[7,12]=D[5,11];
#            %---------------------------------------------------------------------------------------------
#            %Definition of resolution matrix M
            if method==1:
                Minv=N.dot(N.dot(B,A),N.dot(N.linalg.inv(D.linalg.inv(D*N.linalg.inv(S+T.transpose()*F*T)*D.transpose())+G),\
                N.dot(A.transpose(),B.transpose())))#; %Popovici
                #Minv=B*A*((D*(S+T'*F*T)^(-1)*D')^(-1)+G)^(-1)*A'*B'; %Popovici
            else:
                #%Horizontally focusing analyzer if needed
                #print 'intermediate C.T*F*C'
                #print N.dot(C.transpose(),N.dot(F,C))
                #print 'product'
                #print N.dot(F,C)
                HF_int=N.linalg.inv(G+N.dot(C.transpose(),N.dot(F,C)));
                HF=similarity_transform(A,HF_int)
                #print 'HF'
                #print HF
                if horifoc>0:
                    HF=N.linalg.inv(HF);
                    HF[4,4]=(1.0/(kf*alpha[2]))**2; 
                    HF[4,3]=0; 
                    HF[3,4]=0; 
                    HF[3,3]=(N.tan(thetaa)/(etaa*kf))**2;
                    HF=N.linalg.inv(HF);
                Minv=similarity_transform(B,HF)#; %Cooper-Nathans
            M=N.linalg.inv(Minv);
            #print 'A'
            #print A
            #print 'B'
            #print B
            #print 'C'
            #print C
            #print 'D'
            #print D
            #print 'T'
            #print T
            #print 'M'
            #print M
            #print 'Minv'
            #print Minv
            #print 'G'
            #print G
            #print 'F'
            #print F
            RM_[0,0]=M[0,0];
            RM_[1,0]=M[1,0];
            RM_[0,1]=M[0,1];
            RM_[1,1]=M[1,1];
            
            RM_[0,2]=M[0,3];
            RM_[2,0]=M[3,0];
            RM_[2,2]=M[3,3];
            RM_[2,1]=M[3,1];
            RM_[1,2]=M[1,3];
            
            RM_[0,3]=M[0,2];
            RM_[3,0]=M[2,0];
            RM_[3,3]=M[2,2];
            RM_[3,1]=M[2,1];
            RM_[1,3]=M[1,2];
 #           %---------------------------------------------------------------------------------------------
 #           %Calculation of prefactor, normalized to source
            #print 'RM_'
            #print RM_
            Rm=ki**3/N.tan(thetam); 
            Ra=kf**3/N.tan(thetaa);
            #print 'Rm'
            #print Rm
            #print 'Ra'
            #print Ra
            if method==1:
                R0_=Rm*Ra*(2*pi)**4/(64*pi**2*N.sin(thetam)*N.sin(thetaa))\
                *N.sqrt(N.linalg.det(F)/N.linalg.det\
                        (N.linalg.inv(N.dot(D,N.dot(N.linalg.inv(S+N.dot(T.T,N.dot(F,T))),D.T)))+G)); #%Popovici
            else:
                R0_=Rm*Ra*(2*pi)**4/(64*pi**2*N.sin(thetam)*N.sin(thetaa))\
                *N.sqrt( N.linalg.det(F)/N.linalg.det(G+N.dot(C.transpose(),N.dot(F,C)))); #%Cooper-Nathans
                #print 'RO_'
                #print R0_
#            %---------------------------------------------------------------------------------------------
#            %Normalization to flux on monitor
            if moncor==1:
                g=G[0:4][:,0:4];
                f=F[0:2][:,0:2];
                #print 'f'
                #print f
                #print 'g'
                #print g
                c=C[0:2][:,0:4];
                t[0,0]=-1./(2*L0);#  %mistake in paper
                t[0,2]=N.cos(thetam)*(1./L1mon-1./L0)/2;
                t[0,3]=N.sin(thetam)*(1./L0+1./L1mon-2./(monorh*N.sin(thetam)))/2;
                t[0,6]=1./(2*L1mon);
                t[1,1]=-1./(2*L0*N.sin(thetam));
                t[1,4]=(1./L0+1./L1mon-2*N.sin(thetam)/monorv)/(2*N.sin(thetam));
                sinv=blkdiag([bshape,mshape,monitorshape]);# %S-1 matrix        
                s=N.linalg.inv(sinv);
                d[0,0]=-1./L0;
                d[0,2]=-N.cos(thetam)/L0;
                d[0,3]=N.sin(thetam)/L0;
                d[2,1]=D[0,0];
                d[2,4]=-D[0,0];
                d[1,2]=N.cos(thetam)/L1mon;
                d[1,3]=N.sin(thetam)/L1mon;
                d[1,5]=0;
                d[1,6]=1./L1mon;
                d[3,4]=-1./L1mon;
                if method==1:
                    Rmon=Rm*(2*pi)**2/(8*pi*N.sin(thetam))*N.sqrt(N.linalg.det(f)/\
                                                                  N.linalg.det(N.linalg.inv(N.dot(d,N.dot(N.linalg.inv(s+t.transpose()*f*t),d.transpose())))+g)); #%Popovici
                else:
                    Rmon=Rm*(2*pi)**2/(8*pi*N.sin(thetam))*N.sqrt(N.linalg.det(f)/N.linalg.det(g+N.dot(c.transpose(),N.dot(f,c)))); #%Cooper-Nathans
                R0_=R0_/Rmon;
                R0_=R0_*ki; #%1/ki monitor efficiency
                #print 'R01', R0_
                #print 'Rmon', Rmon
                
#            %---------------------------------------------------------------------------------------------
#            %Transform prefactor to Chesser-Axe normalization
            R0_=R0_/(2*pi)**2*N.sqrt(N.linalg.det(RM_));
#            %---------------------------------------------------------------------------------------------
#            %Include kf/ki part of cross section
            R0_=R0_*kf/ki;
#            %---------------------------------------------------------------------------------------------
#            %Take care of sample mosaic if needed [S. A. Werner & R. Pynn, J. Appl. Phys. 42, 4736, (1971)]
            if 'mosaic' in sample:
                etas = sample['mosaic']*CONVERT1;
                etasv=etas;
                if 'vmosaic' in sample:
                    etasv = sample['vmosaic']*CONVERT1;
                R0_=R0_/N.sqrt((1.+(q*etas)**2*RM_[3,3])*(1.0+(q*etasv)**2*RM_[1,1]));
                Minv=N.linalg.inv(RM_)
                Minv[1,1]=Minv[1,1]+q**2*etas**2;
                Minv[3,3]=Minv[3,3]+q**2*etasv**2;
                RM_=N.linalg.inv(Minv);
#            %---------------------------------------------------------------------------------------------
#            %Take care of analyzer reflectivity if needed [I. Zaliznyak, BNL]
            if ('thickness' in ana) & ('Q' in ana):
                KQ = ana['Q'];
                KT = ana['thickness'];
                toa=(taua/2)/N.sqrt(kf**2-(taua/2)**2);
                smallest=alpha[3];
                if alpha[3]>alpha[2]:
                     smallest=alpha[2]
                Qdsint=KQ*toa;
                dth=(N.arange(201)/200)*N.sqrt(2*N.log(2))*smallest;
                wdth=N.exp(-dth**2/2./etaa**2);
                sdth=KT*Qdsint*wdth/etaa/N.sqrt(2.*pi);
                rdth=1./(1+1./sdth);
                reflec=rdth.sum()/wdth.sum();
                R0_=R0_*reflec;
#            %---------------------------------------------------------------------------------------------
            R0[ind]=R0_;
            RM[:,:,ind]=RM_[:,:];
        return R0, RM
    
    def ResMatS(self,H,K,L,W,EXP):
# [len,H,K,L,W,EXP]=CleanArgs(H,K,L,W,EXP);
        x=self.x
        y=self.y
        z=self.z
        Q=self.modvec(H,K,L,'latticestar')
        uq=N.zeros((3,self.npts),'d')
        uq[0,:]=H/Q;  #% Unit vector along Q
        uq[1,:]=K/Q;
        uq[2,:]=L/Q;        
        xq=self.scalar(x[0,:],x[1,:],x[2,:],uq[0,:],uq[1,:],uq[2,:],'latticestar');
        yq=self.scalar(y[0,:],y[1,:],y[2,:],uq[0,:],uq[1,:],uq[2,:],'latticestar');
        zq=0; # %scattering vector assumed to be in (self.orient1,self.orient2) plane;        
        tmat=N.zeros((4,4,self.npts)); #%Coordinate transformation matrix
        tmat[3,3,:]=1;
        tmat[2,2,:]=1;
        tmat[0,0,:]=xq;
        tmat[0,1,:]=yq;
        tmat[1,1,:]=xq;
        tmat[1,0,:]=-yq;
        
        RMS=N.zeros((4,4,self.npts));
        rot=N.zeros((3,3));
        EXProt=EXP;
        
#        %Sample shape matrix in coordinate system defined by scattering vector
        for i in range(self.npts):
            sample=EXP[i]['sample'];
            if 'shape' in sample:
                rot[0,0]=tmat[0,0,i];
                rot[1,0]=tmat[1,0,i];
                rot[0,1]=tmat[0,1,i];
                rot[1,1]=tmat[1,1,i];
                rot[2,2]=tmat[2,2,i];
                EXProt[i]['sample']['shape']=N.dot(rot,N.dot(sample['shape'],rot.T));
        
        R0,RM= self.ResMat(Q,W,EXProt)
        
        for i in range(self.npts):
           RMS[:,:,i]=N.dot((tmat[:,:,i]).transpose(),N.dot(RM[:,:,i],tmat[:,:,i]));
        
        mul=N.zeros((4,4));
        e=N.eye(4,4);
        for i in range(self.npts):
            if 'Smooth' in EXP[i]:
                if 'X' in (EXP[i]['Smooth']):
                    mul[0,0]=1./(EXP[i]['Smooth']['X']**2/8/N.log(2));
                    mul[1,1]=1./(EXP[i]['Smooth']['Y']**2/8/N.log(2));
                    mul[2,2]=1./(EXP[i]['Smooth']['E']**2/8/N.log(2));
                    mul[3,3]=1./(EXP[i]['Smooth']['Z']**2/8/N.log(2));
                    R0[i]=R0[i]/N.sqrt(N.linalg.det(e/RMS[:,:,i]))*N.sqrt(N.linalg.det(e/mul+e/RMS[:,:,i]));
                    RMS[:,:,i]=e/(e/mul+e/RMS[:,:,i]);
        return R0, RMS

    def ResPlot(self,H,K,L,W,EXP):
        """Plot resolution ellipse for a given scan"""
        center=N.round(H.shape[0]/2)
        if center<1:
             center=0
        if center>H.shape[0]:
             center=H.shape[0]
        EXP=[EXP[center]]
        Style1=''
        Style2='--'
        
        XYAxesPosition=[0.1, 0.6, 0.3, 0.3]
        XEAxesPosition=[0.1, 0.1, 0.3, 0.3]
        YEAxesPosition=[0.6, 0.6, 0.3, 0.3]
        TextAxesPosition=[0.45, 0.0, 0.5, 0.5]
        GridPoints=101                
        
        [R0,RMS]=self.ResMatS(H,K,L,W,EXP)
        #[xvec,yvec,zvec,sample,rsample]=self.StandardSystem(EXP);
        self.StandardSystem()
        qx=self.scalar(self.x[0,:],self.x[1,:],self.x[2,:],H,K,L,'latticestar')
        qy=self.scalar(self.y[0,:],self.y[1,:],self.y[2,:],H,K,L,'latticestar')
        qw=W;
        
        #========================================================================================================
        #find reciprocal-space directions of X and Y axes
        
        o1=self.orient1 #EXP['orient1']
        o2=self.orient2 #EXP['orient2']
        pr=self.scalar(o2[0],o2[1],o2[2],self.y[0],self.y[1],self.y[2],'latticestar')
        o2[0]=self.y[0]*pr 
        o2[1]=self.y[1]*pr 
        o2[2]=self.y[2]*pr
        
        if N.abs(o2[0])<1e-5:
             o2[0]=0.0
        if N.absolute(o2[1])<1e-5:
             o2[1]=0.0
        if N.absolute(o2[2])<1e-5:
             o2[2]=0.0
        
        if N.abs(o1[0])<1e-5:
             o1[0]=0.0
        if N.absolute(o2[1])<1e-5:
             o1[1]=0.0
        if N.absolute(o2[2])<1e-5:
             o1[2]=0.0
        
        #%========================================================================================================
        #%determine the plot range
        XWidth=max(self.fproject(RMS,0))
        YWidth=max(self.fproject(RMS,1))
        WWidth=max(self.fproject(RMS,2))
        XMax=(max(qx)+XWidth*1.5)
        XMin=(min(qx)-XWidth*1.5)
        YMax=(max(qy)+YWidth*1.5)
        YMin=(min(qy)-YWidth*1.5)
        WMax=(max(qw)+WWidth*1.5)
        WMin=(min(qw)-WWidth*1.5)
           
        
        #%========================================================================================================
        #% plot XE projection
        
#        XEAxes=axes('position',XEAxesPosition); axis([XMin XMax WMin WMax]); box on; hold on;
#        XEAxis2=axes('position',XEAxesPosition,'XAxisLocation','top','Ytickmode','manual','TickDir','out');
#        omax=XMax/modvec(o1(1),o1(2),o1(3),rsample);
#        omin=XMin/modvec(o1(1),o1(2),o1(3),rsample);
#        olab=['Qx ( units of [' num2str(o1(1)) ' ' num2str(o1(2)) ' ' num2str(o1(3)) '] )'];
#        axis([omin omax WMin WMax]); xlabel(olab);
#        axes(XEAxes); xlabel('Qx (\AA-1)'); ylabel('E (meV)');
        proj,sec=self.project(RMS,1);   
        (a,b,c)=N.shape(proj)
        mat=N.copy(proj)
        for i in range(c):
            matm=N.matrix(mat[:,:,i])
            w,v=N.linalg.eig(matm)
            vm=N.matrix(v)
            vmt=vm.T
            mat_diag=vmt*matm*vm
        a1=1.0/N.sqrt(mat_diag[0,0])
        b1=1.0/N.sqrt(mat_diag[1,1])
        thetar=N.arccos(vm[0,0])
        theta=math.degrees(thetar)
        print a1
        print b1
        print theta
        print mat_diag
        x0y0=N.array([1.0,0.0])
        e=Ellipse(x0y0,width=2*a1,height=2*b1,angle=theta)
        fig=pylab.figure()
        ax = fig.add_subplot(111)
        ax.add_artist(e)
        e.set_clip_box(ax.bbox)
        e.set_alpha(0.5)
        e.set_facecolor('red')
        ax.set_xlim(x0y0[0]-.01, x0y0[0]+.01)
        ax.set_ylim(x0y0[1]-.5, x0y0[1]+.5)
        pylab.show()
        
        
        #self.PlotEllipse(proj,qx,qw,Style1);
        #self.PlotEllipse(sec,qx,qw,Style2);
        #pylab.show()
        return
        
        
        
    def fproject(self,mat_in,i):
        """return hwhm of projection"""
        if (i==0):
            v=2
            j=1
        if (i==1):
            v=0
            j=2
        if (i==2):
            v=0
            j=1
        mat=N.array(mat_in)
        (a,b,c)=N.shape(mat)
        proj=N.zeros((2,2,c),'d')        
        proj[0,0,:]=mat[i,i,:]-mat[i,v,:]*mat[i,v,:]/mat[v,v,:]
        proj[0,1,:]=mat[i,j,:]-mat[i,v,:]*mat[j,v,:]/mat[v,v,:]
        proj[1,0,:]=mat[j,i,:]-mat[j,v,:]*mat[i,v,:]/mat[v,v,:]
        proj[1,1,:]=mat[j,j,:]-mat[j,v,:]*mat[j,v,:]/mat[v,v,:]
        hwhm=proj[0,0,:]-proj[0,1,:]*proj[0,1,:]/proj[1,1,:]
        hwhm=N.sqrt(2*N.log(2))/N.sqrt(hwhm)
        return hwhm
           
    
    def PlotEllipse(self,mat_in,x0,y0,style):
        """plot ellipse"""
        mat=N.array(mat_in)
        (a,b,c)=N.shape(mat)
            #phi=0:2*pi/3000:2*pi;
        phi=N.arange(0,2*pi,2*pi/3000)
        for i in range(c):
            r=N.sqrt(2*N.log(2)/(mat[0,0,i]*N.cos(phi)*N.cos(phi)+mat[1,1,i]*N.sin(phi)*N.sin(phi)\
                                    +2*mat[0,1,i]*N.cos(phi)*N.sin(phi)))
            x=r*N.cos(phi)+x0[i];
            y=r*N.sin(phi)+y0[i];
            pylab.plot(x,y,style);
        return
    
    def project(self,mat_in,v):
        """return projection and cross section matrices"""
        if v == 2:
            i=0;j=1
        if v == 0:
            i=1;j=2
        if v == 1:
            i=0;j=2
        mat=N.array(mat_in)
        (a,b,c)=N.shape(mat)
        proj=N.zeros((2,2,c),'d')
        sec=N.zeros((2,2,c),'d')
        proj[0,0,:]=mat[i,i,:]-mat[i,v,:]*mat[i,v,:]/mat[v,v,:]
        proj[0,1,:]=mat[i,j,:]-mat[i,v,:]*mat[j,v,:]/mat[v,v,:]
        proj[1,0,:]=mat[j,i,:]-mat[j,v,:]*mat[i,v,:]/mat[v,v,:]
        proj[1,1,:]=mat[j,j,:]-mat[j,v,:]*mat[j,v,:]/mat[v,v,:]
        sec[0,0,:]=mat[i,i,:]
        sec[0,1,:]=mat[i,j,:]
        sec[1,0,:]=mat[j,i,:]
        sec[1,1,:]=mat[j,j,:]
        return proj,sec
            

       
class TestLattice(unittest.TestCase):

    def setUp(self):
        a=N.array([2*pi],'d')
        b=N.array([2*pi],'d')
        c=N.array([2*pi],'d')
        alpha=N.array([90],'d')
        beta=N.array([90],'d')
        gamma=N.array([90],'d')
        orient1=N.array([[1,0,0]],'d')
        orient2=N.array([[0,1,1]],'d')
        self.fixture = lattice(a=a,b=b,c=c,alpha=alpha,beta=beta,gamma=gamma,\
                               orient1=orient1,orient2=orient2)
    
    def test_astar(self):
        self.assertAlmostEqual(self.fixture.astar[0],1.0,2,'astar Not equal to '+str(1.0))
    def test_bstar(self):
        self.assertAlmostEqual(self.fixture.bstar[0],1.0,2,'bstar Not equal to '+str(1.0))
    def test_cstar(self):
        self.assertAlmostEqual(self.fixture.cstar[0],1.0,2,'cstar '+str(self.fixture.cstar[0])+' Not equal to '+str(1.0))
    def test_alphastar(self):
        self.assertAlmostEqual(self.fixture.alphastar[0],pi/2,2,'alphastar Not equal to '+str(pi/2))
    def test_betastar(self):
        self.assertAlmostEqual(self.fixture.betastar[0],pi/2,2,'betastar Not equal to '+str(pi/2))
    def test_gammastar(self):
        self.assertAlmostEqual(self.fixture.gammastar[0],pi/2,2,'gammastar Not equal to '+str(pi/2))
    def test_V(self):
        self.assertAlmostEqual(self.fixture.V[0],248.0502,2,'V Not equal to '+str(248.0502))
    def test_Vstar(self):
        self.assertAlmostEqual(self.fixture.Vstar[0],1.0,2,'Vstar Not equal to '+str(1.0))
    def test_g(self):
        #print self.fixture.g
        self.assertAlmostEqual((self.fixture.g[:,:,0][0,0]),39.4784*(N.eye(3)[0,0]) ,2,'g Not equal to '+str(39.4784 ))
    def test_gstar(self):
        #print self.fixture.gstar
        self.assertAlmostEqual(self.fixture.gstar[:,:,0][0,0],1.0*N.eye(3)[0,0] ,2,'gstar Not equal to '+str(1.0 ))
 
    def test_StandardSystem_x(self):
 #       #print self.fixture.gstar
        self.assertAlmostEqual(self.fixture.x[0],1.0 ,2,'Standard System x Not equal to '+str(1.0 ))
 
    
      
                               
#    def test_zeroes(self):
#        self.assertEqual(0 + 0, 0)
#        self.assertEqual(5 + 0, 5)
#        self.assertEqual(0 + 13.2, 13.2)
#
#    def test_positive(self):
#        self.assertEqual(123 + 456, 579)
#        self.assertEqual(1.2e20 + 3.4e20, 3.5e20)
#
#    def test_mixed(self):
#        self.assertEqual(-19 + 20, 1)
#        self.assertEqual(999 + -1, 998)
#        self.assertEqual(-300.1 + -400.2, -700.3)
#        

if __name__=="__main__":
    if 1:
        a=N.array([2*pi],'d')
        b=N.array([2*pi],'d')
        c=N.array([2*pi],'d')
        alpha=N.array([90],'d')
        beta=N.array([90],'d')
        gamma=N.array([90],'d')
 #       orient1=N.array([[0,1,1]],'d')
        orient1=N.array([[1,0,0]],'d')
        orient2=N.array([[0,1,1]],'d')
        mylattice=lattice(a=a,b=b,c=c,alpha=alpha,beta=beta,gamma=gamma,\
                               orient1=orient1,orient2=orient2)
        H=N.array([1],'d');K=N.array([0],'d');L=N.array([0],'d');W=N.array([0],'d')
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
        EXP['hcol']=N.array([40, 10, 20, 80],'d')
        EXP['vcol']=N.array([120, 120, 120, 120],'d')
        EXP['infix']=-1 #positive for fixed incident energy
        EXP['efixed']=14.7
        EXP['method']=0
        setup=[EXP]  
        R0,RMS=mylattice.ResMatS(H,K,L,W,setup)
        mylattice.ResPlot(H, K, L, W, setup)
        print 'RMS'
        print RMS.transpose()[0]
#        mylattice.StandardSystem()
##    x1=N.array([1.0, 1.0], 'd'); y1=N.array([1.0, 1.0], 'd'); z1=N.array([1.0, 1.0], 'd'); x2=x1; y2=y1; z2=z1;
##    print 'scalar ', mylattice.scalar(x1,y1,z1,x2,y2,z2,'lattice')
##    print 'me ',mylattice.gtensor('lattice')
##    myinstrument=instrument();
##    print myinstrument.get_tau('pg(004)')
#    unittest.main()