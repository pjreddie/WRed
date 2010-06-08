import numpy as np
from numpy import pi,cos, sqrt, sin,exp,conj
from numpy.linalg import norm
I=np.complex(0,1)
import copy,sys,os
import readncnr3 as readncnr
import numpy as N
import scriptutil as SU
import re
from simple_combine import simple_combine
import scipy.optimize
import rescalculator.rescalc as rescalc
import utilities.findpeak4 as findpeak
from spinwaves.utilities.mpfit.mpfit import mpfit 
import pylab
from utilities.anneal import anneal


from enthought.mayavi import mlab


astar=2*pi/5.608;
bstar=2*pi/5.608
cstar=2*pi/8.58

#def readfiles():
 

#%scans=[12 16 18 37 39 41 43 45 47 49 51 53 55 57 59 61 63 65 67 69 71 73];

#fileszero='00';


#fileszero2='0';
#%scans2=10:17;
#%scans=[scans1 scans2];
#%scans=scans1;
#files=[];
#numfiles=[2,3,5,6,7];

#numfiles=[4:9];
#for i=1:length(numfiles)
#file=[filedir filehead fileszero num2str(numfiles(i)) fileend];
#files=[files;file];
#end

#numfiles=[10:17];
#for i=1:length(numfiles)
#file=[filedir filehead fileszero2 num2str(numfiles(i)) fileend];
#files=[files;file];
#end



def magstruct(pfit,Qm,Int,Interr,correction):
 Ifit=calcstructure(pfit,Qm,correction)
 chisq=(Ifit-Int)/Interr;
 #[th1 phi2 th2]; 
 return chisq

def chisq_an(pfit,Qm,Int,Interr,correction):
 chisq=magstruct(pfit,Qm,Int,Interr,correction)
 return (chisq**2).sum()

def myfunctlin(p, fjac=None, x=None, y=None, err=None,correction=None):
    # Parameter values are passed in "p"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    return [status, magstruct(p,x,y,err,correction)]

def readfiles(filestrlist):
 Ilist=[]
 Ierrlist=[]
 Qlist=[]
 hkllist=[]
 thlist=[]
 mydatalist=[]
 for myfilestr in filestrlist:
  mydatareader=readncnr.datareader()
  mydata=mydatareader.readbuffer(myfilestr)
  filename=mydata.metadata['file_info']['filename']
  h=mydata.metadata['q_center']['h_center']
  k=mydata.metadata['q_center']['k_center']
  l=mydata.metadata['q_center']['l_center']
  hkl='('+str(h)+' '+str(k)+' '+str(l)+')' 
  Q=np.array([h,k,l],'float64')
  print 'hkl',hkl
  print 'file', filename
  if len(Ilist)==0:
   mon0=mydata.metadata['count_info']['monitor']
   mon0=82500
        
  mon=mydata.metadata['count_info']['monitor']
  I_orig=np.array(mydata.data['counts'],'Float64')
            #node.measured_data.data['counts_err']=N.array(node.measured_data.data['counts_err'],'Float64')
  I_norm=I_orig*mon0/mon
  I_norm_err=np.sqrt(I_orig)*mon0/mon
  Ilist.append(I_norm)
  Ierrlist.append(I_norm_err)
  Qlist.append(Q)
  hkllist.append(hkl)
  th=np.array(mydata.data['a3'])
  thlist.append(th)
  mydatalist.append(mydata)
 return Qlist, thlist,Ilist, Ierrlist,hkllist,mydatalist
           


def gen_fe():
 #generate fe atoms in the unit cell
 r5=[0.2500,   0.0000,   0.5000];
 r6=[0.7500,   0.0000,   0.5000];
 r7=[0.2500,   0.5000,   0.5000]; 
 r8=[0.7500,   0.5000,   0.5000]; 
 r=np.vstack((r5,r6,r7,r8))
 return r

def gen_nd():
 r1=[0.0000,   0.2500,   0.6389];
 r2=[0.0000,   0.7500,   0.3611];
 r3=[0.5000,   0.7500,   0.6389];
 r4=[0.5000,   0.2500,   0.3611];
 r=np.vstack((r1,r2,r3,r4))
 return r

def gen_nd_spins(s_in):
 #s1th=np.radians(s1th_in)
 #s2th=np.radians(s2th_in)
 #define the spins of the atoms in the cell
 #s1=np.array([cos(s1th), 0, sin(s1th)],'float64'); s1=s1/norm(s1);
 #s2=np.array([cos(s2th), 0, sin(s2th)],'float64'); s2=s2/norm(s2);
 #s4=np.array([-cos(s2th), 0, sin(s2th)],'float64'); s4=s4/norm(s4);
 #s=np.vstack((s1,-s1,s1,s1))  #s1th_in=90: ++=--; -+=0=+-; -90:+-=0=-+; --=++= same as +90 for s1th
 th1,th2,th3,th4,phi1,phi2,phi3,phi4=s_in
 s1=np.array([sin(th1)*cos(phi1), sin(th1)*sin(phi1), cos(th1)],'float64')
 s2=np.array([sin(th2)*cos(phi2), sin(th2)*sin(phi2), cos(th2)],'float64')
 s3=np.array([sin(th3)*cos(phi3), sin(th3)*sin(phi3), cos(th3)],'float64')
 s4=np.array([sin(th4)*cos(phi4), sin(th4)*sin(phi4), cos(th4)],'float64')
 s=np.vstack((s1,s2,s3,s4))
 
 
 return s

def gen_nd_spins_orig(s1th_in=-90,s2th_in=0):
 s1th=np.radians(s1th_in)
 s2th=np.radians(s2th_in)
 #define the spins of the atoms in the cell
 s1=np.array([cos(s1th), 0, sin(s1th)],'float64'); s1=s1/norm(s1);
 #s2=np.array([cos(s2th), 0, sin(s2th)],'float64'); s2=s2/norm(s2);
 #s4=np.array([-cos(s2th), 0, sin(s2th)],'float64'); s4=s4/norm(s4);
 s=np.vstack((s1,-s1,s1,s1))  #s1th_in=90: ++=--; -+=0=+-; -90:+-=0=-+; --=++= same as +90 for s1th
 
 return s

def gen_fe_spins(th_in=0.0):
 th=np.radians(th_in)
 #define the spins of the atoms in the cell
 s5=np.array([cos(th), 0, sin(th)],'float64'); s1=s5/norm(s5);
 s=np.vstack((s5,-s5,s5,-s5))
 return s
 



@mlab.show
def draw_struct():
    fig=mlab.figure()    
    r=gen_fe()
    s=gen_spins()
    #view along z-axis
    x=r[:,0]
    y=r[:,1]
    z=r[:,2]
    u=s[:,0]
    v=s[:,1]
    w=s[:,2]
    
    #print x.shape
    #print y.shape
    #print z.shape
    pts_as=mlab.points3d(x,y,z,color=(0,0,1),colormap='gist_rainbow',figure=fig,scale_factor=.1)
    mlab.quiver3d(x, y, z,u,v,w, line_width=3, scale_factor=.3,figure=fig)
    outline=mlab.outline(figure=fig,extent=[0,1,0,1,0,1])
    mlab.orientation_axes(figure=fig,xlabel='a',ylabel='b',zlabel='c')
    print 'done'

    
def mgnfacFesquared(x):

#x=s=sin(theta)/lambda=modq/4/pi
 y=( 0.0706*exp(-35.008*x**2)+0.3589*exp(-15.358*x**2)
   +0.5819*exp(-5.561*x**2)-0.0114)**2
 return y
    

def mgnfacNdsquared(s):
 #j0
 j0=( 0.0540*exp(-25.029*s**2)+0.3101*exp(-12.102*s**2)+0.6575*exp(-4.722*s**2)-0.0216);
 #j2
 vals=[.6751, 18.342, 1.6272 ,7.26, 0.9644, 2.602, 0.015];
 A=vals[0]; a=vals[1]; B=vals[2]; b=vals[3]; C=vals[4]; c=vals[5]; D=vals[6]; 
 j2=A*s**2.*exp(-a*s**2)+B*s**2*exp(-b*s**2)+C*s**2*exp(-c*s**2)+D*s**2;
 S=3.0/2;
 l=6.0;
 j=9.0/2;
 gs=(j*(j+1)-l*(l+1)+S*(S+1))/j/(j+1)/2;  #check factor of 2?  should it be /j/(j+1)/2??
 gl=(j*(j+1)+l*(l+1)-S*(S+1))/j/(j+1)/2;
 g=gs+gl;
 y=j0+gl/g*j2;
 y=y**2;
 return y


def calcstructure(pfit,Qs,correction):
 #positions of magnetic atoms in unit cell
 #p=[momFe momNd s2th)
 Fe3pt=gen_fe()
 momentsKFe3p=gen_fe_spins(th_in=0)*pfit[0] #fix Fe spins along the a-axis
 #Nd3pt=gen_nd()
 #momentsKNd3p=gen_nd_spins(s1th_in=-90.0,s2th_in=pfit[2])*pfit[1] #fix Fe spins along the a-axis
 #momentsKNd3p=gen_nd_spins(s1th_in=pfit[2],s2th_in=pfit[3])*pfit[1] #fix Fe spins along the a-axis
 #momentsKNd3p=gen_nd_spins()*pfit[1]
 #momentsKNd3p=gen_nd_spins(pfit[2:])*pfit[1]
 n,m=Qs.shape
 QA=copy.deepcopy(Qs)
 QA[:,0]=QA[:,0]*astar
 QA[:,1]=QA[:,1]*bstar
 QA[:,2]=QA[:,2]*cstar
 modq=sqrt(QA[:,0]*QA[:,0]+QA[:,1]*QA[:,1]+QA[:,2]*QA[:,2])
 Qn=copy.deepcopy(QA)
 Qn[:,0]=QA[:,0]/modq;
 Qn[:,1]=QA[:,1]/modq;
 Qn[:,2]=QA[:,2]/modq;   
 #calculate form factor
 magnfacFe3p=sqrt(mgnfacFesquared(modq/4/pi));
 #magnfacNd3p=sqrt(mgnfacNdsquared(modq/4/pi));
 #calculate structure factor
 F1Fe3p=np.zeros((n,3),'complex64');
 expt=exp(I*2*pi*np.dot(Qs,Fe3pt.T))
 F1Fe3p=np.dot(expt,momentsKFe3p)
 F1Fe3p[:,0]=F1Fe3p[:,0]*magnfacFe3p;
 F1Fe3p[:,1]=F1Fe3p[:,1]*magnfacFe3p;
 F1Fe3p[:,2]=F1Fe3p[:,2]*magnfacFe3p;
 
 #F1Nd3p=np.zeros((n,3));
 #expt=exp(I*2*pi*np.dot(Qs,Nd3pt.T))
 #F1Nd3p=np.dot(expt,momentsKNd3p)
 #F1Nd3p[:,0]=F1Nd3p[:,0]*magnfacNd3p;
 #F1Nd3p[:,1]=F1Nd3p[:,1]*magnfacNd3p;
 #F1Nd3p[:,2]=F1Nd3p[:,2]*magnfacNd3p;
 #fmt=np.zeros((n,1))
 
 F1=F1Fe3p#+F1Nd3p;
 #find fperpendicular from F-F.q*q hat
 Fperp1=np.zeros(F1.shape,'complex64')
 Fperp1[:,0]=F1[:,0]-(Qn[:,0]*F1[:,0]+Qn[:,1]*F1[:,1]+Qn[:,2]*F1[:,2])*Qn[:,0]
 Fperp1[:,1]=F1[:,1]-(Qn[:,0]*F1[:,0]+Qn[:,1]*F1[:,1]+Qn[:,2]*F1[:,2])*Qn[:,1]
 Fperp1[:,2]=F1[:,2]-(Qn[:,0]*F1[:,0]+Qn[:,1]*F1[:,1]+Qn[:,2]*F1[:,2])*Qn[:,2]
 fm1=np.zeros(F1.shape,'complex64')
 fm1=(Fperp1[:,0]*conj(Fperp1[:,0])+Fperp1[:,1]*conj(Fperp1[:,1])+Fperp1[:,2]*conj(Fperp1[:,2]))      
 fmt=fm1;
 fm=fmt[0:n]*correction
 return np.real(fm)

def gen_flist(mydirectory,myfilebase,myend,filenums):
 files=[]
 for filenum in filenums:
  if filenum < 10:
   myfilestr=myfilebase+'00'+str(filenum)+myend
  elif filenum < 100:
   myfilestr=myfilebase+'0'+str(filenum)+myend
  else:
   myfilestr=myfilebase+str(filenum)+myend
   
  myfilestr=os.path.join(mydirectory,myfilestr)
  files.append(myfilestr)
 return files

def fit_peak(plotdict):
  x=plotdict['data']['x']
  y=plotdict['data']['y']
  yerr=plotdict['data']['yerr']
  kernel=findpeak.find_kernel(y)
  npeaks,nlist,plist=findpeak.find_npeaks(x,y,yerr,kernel,nmax=2)
  results=findpeak.findpeak(x,y,npeaks,kernel=kernel)
  fwhm=findpeak.findwidths(x,y,npeaks,results['xpeaks'],results['indices'])
  sigma=fwhm/2.354
  p0=[0,0]
  pb=N.concatenate((results['xpeaks'], fwhm, results['heights']*N.sqrt(2*pi*sigma**2)))
  pb=N.array(pb).flatten()
  p0=N.concatenate((p0,pb)).flatten()
  print 'p0',p0
  #
  fresults= scipy.optimize.leastsq(findpeak.cost_func, p0, args=(x,y,yerr),full_output=1)
  p1=fresults[0]
  covariance=fresults[1]

  parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
  parinfo=[]
  for i in range(len(p0)):
      parinfo.append(copy.deepcopy(parbase))
  for i in range(len(p0)): 
      parinfo[i]['value']=p0[i]
  parinfo[1]['fixed']=1 #fix slope
  fa = {'x':x, 'y':y, 'err':yerr}
  m = mpfit(findpeak.myfunctlin, p0, parinfo=parinfo,functkw=fa) 
  print 'status = ', m.status
  print 'params = ', m.params
  p1=m.params
  covariance=m.covar
  
  dof=len(y)-len(p1)
  fake_dof=len(y)
  chimin=(findpeak.cost_func(p1,x,y,yerr)**2).sum()
  chimin=chimin/dof if dof>0 else chimin/fake_dof
  covariance=covariance*chimin #assume our model is good
  
  
  
  area=N.array(N.abs(p1[2+2*npeaks::]))
  area_sig=covariance.diagonal()[2+2*npeaks::]
  fwhm=N.array(N.abs(p1[2+npeaks:2+2*npeaks]))
  
  
  
  ycalc=findpeak.gen_function(p1,x)
  fitdict={}
  fitdict['x']=x
  fitdict['y']=ycalc
  fitdict['area']=area.sum()
  fitdict['chi']=chimin
  fitdict['area_err']=N.sqrt(area_sig.sum())
  print 'area',fitdict['area']
  #next add the fit results
  print 'chi',chimin
  return fitdict


def correct_data(mydata,qscan=None):
 mya=mydata.metadata['lattice']['a']
 myb=mydata.metadata['lattice']['b']
 myc=mydata.metadata['lattice']['c']
 myalpha=N.radians(mydata.metadata['lattice']['alpha'])
 mybeta=N.radians(mydata.metadata['lattice']['beta'])
 mygamma=N.radians(mydata.metadata['lattice']['gamma'])
 a=N.array([mya],dtype='float64') #for now, the code is broken if only one element in the array for indexing
 b=N.array([myb],dtype='float64')
 c=N.array([myc],dtype='float64')
 alpha=N.array([myalpha],dtype='float64')
 beta=N.array([mybeta],dtype='float64')
 gamma=N.array([mygamma],dtype='float64')
 #print mydata.metadata
 h=mydata.metadata['orient1']['h']
 k=mydata.metadata['orient1']['k']
 l=mydata.metadata['orient1']['l']
 orient1=N.array([[h,k,l]],dtype='float64')
 h=mydata.metadata['orient2']['h']
 k=mydata.metadata['orient2']['k']
 l=mydata.metadata['orient2']['l']
 orient2=N.array([[h,k,l]],dtype='float64')
 orientation=rescalc.lattice_calculator.Orientation(orient1,orient2)
 mylattice=rescalc.lattice_calculator.Lattice(a=a,b=b,c=c,alpha=alpha,beta=beta,gamma=gamma,orientation=orientation)
 #h=q['h_center'] #perhaps just take this from the file in the future
 #k=q['k_center']
 #l=q['l_center']
 h=mydata.metadata['q_center']['h_center']
 k=mydata.metadata['q_center']['k_center']
 l=mydata.metadata['q_center']['l_center']
 H=N.array([h,h],dtype='float64');
 K=N.array([k,k],dtype='float64');
 L=N.array([l,l],dtype='float64');
 W=N.array([0.0,0.0],dtype='float64')
 EXP={}
 EXP['ana']={}
 EXP['ana']['tau']='2axis'#'pg(002)'
 #EXP['ana']['tau']='pg(002)'
 EXP['mono']={}
 EXP['mono']['tau']='pg(002)';
 EXP['ana']['mosaic']=600.0#60
 EXP['mono']['mosaic']=60
 EXP['sample']={}
 EXP['sample']['mosaic']=30
 EXP['sample']['vmosaic']=30
 coll1=mydata.metadata['collimations']['coll1']
 coll2=mydata.metadata['collimations']['coll2']
 coll3=mydata.metadata['collimations']['coll3']
 coll4=mydata.metadata['collimations']['coll4']	
 
 EXP['hcol']=N.array([coll1,coll2,coll3,coll4],dtype='float64')
 #EXP['hcol']=N.array([40, 47, 40, 200],dtype='float64')
 EXP['hcol']=N.array([40, 47, 40, 200],dtype='float64')
 
 EXP['vcol']=N.array([120, 120, 120, 240],dtype='float64')

 EXP['infix']=-1 #positive for fixed incident energy
 EXP['efixed']=mydata.metadata['energy_info']['ef']
 EXP['method']=0
 setup=[EXP]
 myrescal=rescalc.rescalculator(mylattice)
 newinput=rescalc.lattice_calculator.CleanArgs(a=a,b=b,c=c,alpha=alpha,beta=beta,gamma=gamma,orient1=orient1,orient2=orient2,\
                                               H=H,K=K,L=L,W=W,setup=setup)
 neworientation=rescalc.lattice_calculator.Orientation(newinput['orient1'],newinput['orient2'])
 mylattice=rescalc.lattice_calculator.Lattice(a=newinput['a'],b=newinput['b'],c=newinput['c'],alpha=newinput['alpha'],
                                              beta=newinput['beta'],gamma=newinput['gamma'],orientation=neworientation)
 myrescal.__init__(mylattice)
 Q=myrescal.lattice_calculator.modvec(H,K,L,'latticestar')
 #print 'Q', Q
 R0,RM=myrescal.ResMat(Q,W,setup)
 #print 'RM '
 #print RM.transpose()
 #print 'R0 ',R0
 #exit()
 R0,RMS=myrescal.ResMatS(H,K,L,W,setup)
 #myrescal.ResPlot(H, K, L, W, setup)
 #print 'RMS'
 #print RMS.transpose()[0]
 #corrections=myrescal.calc_correction(H,K,L,W,setup,qscan=[[1,0,1],[1,0,1]])
 corrections=myrescal.calc_correction(H,K,L,W,setup,qscan=qscan)
 #print corrections
 return corrections,Q[0]
 
 
if __name__=="__main__":
 print "main"
 gamma=1.913;r0=2.818;Amagn=(gamma*r0/2)**2;   # in fm (to account that nuclear scattering lenghts are also given in fm)
 Anuclear=.0978;
 Anuclear=7.2663e-004;
 Anuclear=.0032;
 Anuclear=0.4568;
 A=Anuclear*Amagn*2
 if 1:
  mydirectory=r'C:\Ndfeas\jeff\Nd1111\Apr15_2010'
  myfilebase='magfb'
  myend='.bt9'
  filenums=[14,15]
  #filenums=[14]
  flist=gen_flist(mydirectory,myfilebase,myend,filenums)
  print flist
  Qlist, thlist,Ilist, Ierrlist,hkllist,mydatalist=readfiles(flist)
  print Qlist
  fig=pylab.figure(figsize=(8,8))
  modqlist=[]
  corrections=[]
  y=[]
  yerr=[]
  for i in range(len(Qlist)):
   print hkllist[i]
   plotdict={}
   print 'file',flist[i]
   plotdict['data']={}
   plotdict['data']['x']=thlist[i]
   plotdict['data']['y']=Ilist[i]
   plotdict['data']['yerr']=Ierrlist[i]
   fitdict=fit_peak(plotdict)
   y.append(fitdict['area'])
   yerr.append(fitdict['area_err'])
   if 0:
    ax=fig.add_subplot(3,4,i+1)
    ax.errorbar(plotdict['data']['x'],plotdict['data']['y'],plotdict['data']['yerr'],marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
    ax.plot(fitdict['x'],fitdict['y'])
   correction,modq=correct_data(mydatalist[i])
   corrections.append(correction['th_correction'][0])
   modqlist.append(modq)
  if 0:
   pylab.show() 
  print corrections
  print modqlist
  y=np.array(y,'float64')
  yerr=np.array(yerr,'float64')
  pfit=np.array([0.56 ,1.52, -90,-42.0],'float64') 
  pfit=np.array([0.56 ,1.52],'float64')
  s_in=[0,90,40,40,90,90,90,90]
  th1,th2,th3,th4,phi1,phi2,phi3,phi4=s_in
  pfit=np.array([5.5],'float64')
  
  #correction=np.ones(Qs.shape[0])
  corrections=np.array(corrections)
  Qlist=np.array(Qlist)
  fm=calcstructure(pfit,Qlist,corrections)
  print 'fm',fm
  #scale by nuclear factor
  y=y/A
  yerr=yerr/A
  
  if 0:
   print 'annealing'
   #myschedule='fast'
   myschedule='simple'
   lowerm=1e-4*N.ones(len(pfit))
        #lowerm[0:3]=[-1,-1,-1]
   #upperm=N.ones(len(pfit))
   myargs=(Qlist,y,yerr,corrections)
   upperm=np.array([1000.0])
   pout,jmin=anneal(chisq_an,pfit,args=myargs,\
                 schedule=myschedule,lower=lowerm,upper=upperm,\
                 maxeval=1000, maxaccept=None,dwell=2000,maxiter=120,feps=1e-2,full_output = 0)
  
   print 'annealed',pout
   pfit=pout
  
  
  
  parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
  parinfo=[]
  for i in range(len(pfit)):
      parinfo.append(copy.deepcopy(parbase))
  for i in range(len(pfit)): 
      parinfo[i]['value']=pfit[i]
  fa = {'x':Qlist, 'y':y, 'err':yerr, 'correction':corrections}
  m = mpfit(myfunctlin, pfit, parinfo=parinfo,functkw=fa) 
  
  
  
  
  print 'status = ', m.status
  print 'params = ', m.params
  p1=m.params
  covariance=m.covar
  if 0:
   print 'p',p1[0],p1[1],np.degrees(p1[2:])
   th1,th2,th3,th4,phi1,phi2,phi3,phi4=p1[2:]
   s1=np.array([sin(th1)*cos(phi1), sin(th1)*sin(phi1), cos(th1)],'float64')
   s2=np.array([sin(th2)*cos(phi2), sin(th2)*sin(phi2), cos(th2)],'float64')
   s3=np.array([sin(th3)*cos(phi3), sin(th3)*sin(phi3), cos(th3)],'float64')
   s4=np.array([sin(th4)*cos(phi4), sin(th4)*sin(phi4), cos(th4)],'float64')
   print 'spins'
   print s1
   print s2
   print s3
   print s4
  dof=len(y)-len(p1)
  fake_dof=len(y)
  chimin=(magstruct(p1,Qlist,y,yerr,corrections)**2).sum()
  #chimin=(findpeak.cost_func(p1,x,y,yerr)**2).sum()
  chimin=chimin/dof if dof>0 else chimin/fake_dof
  covariance=covariance*chimin #assume our model is good
  print 'chimin',chimin
  fm=calcstructure(p1,Qlist,corrections)
  print 'fm',fm
  if 1:
    ax=fig.add_subplot(1,1,1)
    ax.errorbar(modqlist,y,yerr,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
    ax.plot(modqlist,fm,marker='o',linestyle='None',mfc='red')
    pylab.show()
  
  #area=N.array(N.abs(p1[2+2*npeaks::]))
  #area_sig=covariance.diagonal()[2+2*npeaks::]
  #fwhm=N.array(N.abs(p1[2+npeaks:2+2*npeaks]))
  

 if 0:
  Qs=np.array([[  1,     0,     7],
               [  3,     0,     1],
               [  3,     0,     3],
               [  3,     0,     5],
               [  1,     0,     1],
               [  1,     0,     3],
               [  1,     0,     5],
               [  1,     0,     7],
               [  1,     0,     9],
               [  1,     0,    11],
               [  3,     0,     7],
               [  3,     0,     9],
               [  5,     0,     1],
               [  5,     0,     3]],
               'float64')
  pfit=np.array([1.0],'float64')  
  correction=np.ones(Qs.shape[0])
  fm=calcstructure(pfit,Qs,correction)
  print 'fm',fm
 if 0:
  r=gen_fe()
  draw_struct()
