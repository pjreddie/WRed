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


from enthought.mayavi import mlab


astar=2*pi/5.511;
bstar=2*pi/5.511
cstar=2*pi/12.136

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
  if len(Ilist)==0:
   mon0=mydata.metadata['count_info']['monitor']
        
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
 #generate atoms in the unit cell
 r1=[.25, .25, .25]
 r2=[.25, .75, .25]
 r3=[.75, .25, .25]
 r4=[.75,  .75, .25]
 
 r5=[.25, .25, .75]
 r6=[.25, .75, .75]
 r7=[.75, .25, .75]
 r8=[.75,  .75, .75]
 r=np.vstack((r1,r2,r3,r4,r5,r6,r7,r8))
 return r

def gen_spins(th_in=41):
 th=np.radians(th_in)
 #define the spins of the atoms in the cell
 s1=np.array([cos(th), sin(th), 0],'float64'); s1=s1/norm(s1);
 s2=np.array([cos(th), sin(th), 0],'float64'); s2=s2/norm(s2);
 s3=-s1
 s4=-s1
 s5=-s1
 s6=-s1
 s7=s1
 s8=s1
 s=np.vstack((s1,s2,s3,s4,s5,s6,s7,s8))
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
    
def calcstructure(pfit,Qs,correction):
 #positions of magnetic atoms in unit cell
 Mn3pt=gen_fe()
 momentsKMn3p=gen_spins(th_in=pfit[1])
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
 magnfacMn3p=sqrt(mgnfacFesquared(modq/4/pi));
 #calculate structure factor
 F1Mn3p=np.zeros((n,3));
 expt=exp(I*2*pi*np.dot(Qs,Mn3pt.T))
 F1Mn3p=np.dot(expt,momentsKMn3p)
 F1Mn3p[:,0]=F1Mn3p[:,0]*magnfacMn3p;
 F1Mn3p[:,1]=F1Mn3p[:,1]*magnfacMn3p;
 F1Mn3p[:,2]=F1Mn3p[:,2]*magnfacMn3p;
 #fmt=np.zeros((n,1))
 F1=F1Mn3p;
 #find fperpendicular from F-F.q*q hat
 Fperp1=np.zeros(F1.shape,'float64')
 Fperp1[:,0]=F1[:,0]-(Qn[:,0]*F1[:,0]+Qn[:,1]*F1[:,1]+Qn[:,2]*F1[:,2])*Qn[:,0]
 Fperp1[:,1]=F1[:,1]-(Qn[:,0]*F1[:,0]+Qn[:,1]*F1[:,1]+Qn[:,2]*F1[:,2])*Qn[:,1]
 Fperp1[:,2]=F1[:,2]-(Qn[:,0]*F1[:,0]+Qn[:,1]*F1[:,1]+Qn[:,2]*F1[:,2])*Qn[:,2]
 fm1=np.zeros(F1.shape,'float64')
 fm1=(Fperp1[:,0]*conj(Fperp1[:,0])+Fperp1[:,1]*conj(Fperp1[:,1])+Fperp1[:,2]*conj(Fperp1[:,2]))      
 fmt=fm1;
 fm=fmt[0:n]*pfit[0]**2*correction
 return fm

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
 EXP['ana']['tau']='pg(002)'
 EXP['mono']={}
 EXP['mono']['tau']='pg(002)';
 EXP['ana']['mosaic']=60
 EXP['mono']['mosaic']=60
 EXP['sample']={}
 EXP['sample']['mosaic']=30
 EXP['sample']['vmosaic']=30
 coll1=mydata.metadata['collimations']['coll1']
 coll2=mydata.metadata['collimations']['coll2']
 coll3=mydata.metadata['collimations']['coll3']
 coll4=mydata.metadata['collimations']['coll4']	
 
 EXP['hcol']=N.array([coll1,coll2,coll3,coll4],dtype='float64')
 EXP['hcol']=N.array([40, 22.7, 40, 120],dtype='float64')
 
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
 A=Anuclear*Amagn
 if 1:
  mydirectory=r'c:\srfeas\20081212'
  myfilebase='mag35'
  myend='.bt9'
  filenums=range(4,18-3)
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
  pfit=np.array([0.8 ,  -0.0026],'float64')  
  #correction=np.ones(Qs.shape[0])
  corrections=np.array(corrections)
  Qlist=np.array(Qlist)
  fm=calcstructure(pfit,Qlist,corrections)
  print 'fm',fm
  #scale by nuclear factor
  y=y/A
  yerr=yerr/A
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
  print 'p',p1
  dof=len(y)-len(p1)
  fake_dof=len(y)
  chimin=(magstruct(p1,Qlist,y,yerr,corrections)**2).sum()
  #chimin=(findpeak.cost_func(p1,x,y,yerr)**2).sum()
  chimin=chimin/dof if dof>0 else chimin/fake_dof
  covariance=covariance*chimin #assume our model is good
  print 'chimin',chimin
  fm=calcstructure(p1,Qlist,corrections)
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
