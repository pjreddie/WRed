import readncnr3 as readncnr
import numpy as N
import scriptutil as SU
import re
from simple_combine import simple_combine
import copy
import pylab
from findpeak3 import findpeak
from openopt import NLP
import scipy.optimize
import scipy.odr
from scipy.optimize import curve_fit
pi=N.pi
import sys
from mpfit import mpfit
import rescalculator.rescalc as rescalc

class data_item(object):
    def __init__(self,data,selected=True):
        self.data=data
        self.selected=selected

class Qnode(object):
    def __init__(self,q,th=None,th2th=None,qscans=None,other=None,data=None):
        self.q=q
        self.Q=0.0
        self.selected=True
        self.mon0=1.0
        self.th_correction=1.0
        self.tth_correction=1.0
        self.q_correction=1.0
        self.th_integrated_intensity=0.0
        self.tth_integrated_intensity=0.0
        self.q_integrated_intensity=0.0
        if th==None:
            self.th=[]
        else:
            self.th=th
        if th2th==None:
            self.th2th=[]
        else:
            self.th2th=th2th
        if other==None:
            self.other=[]
        else:
            self.other=other
        if qscans==None:
            self.qscans=[]
        else:
            self.qscans=qscans
        if data!=None:
            self.place_data(data)
        return

    def place_data(self,mydata,tol=1e-6):
        if mydata.metadata['file_info']['scantype']=='b':
            #print 'b'
            currfile=mydata.metadata['file_info']['filename']
            if N.abs(mydata.metadata['motor4']['step'])<tol and N.abs(mydata.metadata['motor3']['step'])>tol:
                #print currfile, 'a3 scan'
                self.th.append(data_item(mydata))
                #print 'self.th',self.th
            elif N.abs(mydata.metadata['motor4']['step']-2*mydata.metadata['motor3']['step'])<tol and N.abs(mydata.metadata['motor3']['step'])>tol:
                #print currfile, 'th-2th scan'
                self.th2th.append(data_item(mydata))
            else:
                #print currfile, 'strange scan'
                self.other.append(data_item(mydata))
        return

class Qtree(object):
    def __init__(self,qlist=None,mon0=1.0):
        if qlist==None:
            self.qlist=[]
        else:
            self.qlist=qlist
        self.mon0=mon0
        return
    def addnode(self,mydata):
        mydata=copy.deepcopy(mydata)
        qcenter=mydata.metadata['q_center']
        qlist=copy.deepcopy(self.qlist)
        if len(qlist)==0:
            #print '0 case'
            newnode=Qnode(qcenter,data=mydata)
            self.mon0=mydata.metadata['count_info']['monitor']
            self.qlist.append(newnode)
            #print '0000000000000'
            #print 'qlist len',len(self.qlist)
            #print 'before qlist q',self.qlist[0].q
            #print
        else:
            #print 'else'
            #print 'qlist len',len(self.qlist)
            #print 'before qlist q',self.qlist[0].q
            inlist=False
            for qnode in self.qlist:
                q=qnode.q
                #print 'qcenter',qcenter
                #print 'q',q
                if check_q(q,qcenter):
                    #print qcenter,'in list'
                    mon=mydata.metadata['count_info']['monitor']
                    counts_new=mydata.data['counts']*self.mon0/mon
                    counts_new_err=N.sqrt(mydata.data['counts'])*self.mon0/mon
                    mydata.data['counts']=counts_new
                    mydata.data['counts_err']=counts_new_err
                    mydata.metadata['count_info']['monitor']=self.mon0
                    qnode.place_data(mydata)
                    #print 'placed'
                    #print qnode.th
                    inlist=True 
            if inlist==False:
                #print 'NOT in list'
                newnode=Qnode(qcenter,data=mydata)
                self.qlist.append(newnode)
        return

    def find_node(self,qcenter):

        i=0
        index=False
        for qnode in self.qlist:
            q=qnode.q
            #print 'qcenter',qcenter
            #print 'q',q
            if check_q(q,qcenter):
                index=i
                break
            i=i+1
        return index

    def correct_data(self,mydata,q):
        mya=mydata.metadata['lattice']['a']
        myb=mydata.metadata['lattice']['b']
        myc=mydata.metadata['lattice']['c']
        myalpha=N.radians(mydata.metadata['lattice']['alpha'])
        mybeta=N.radians(mydata.metadata['lattice']['beta'])
        mygamma=N.radians(mydata.metadata['lattice']['gamma'])
        a=N.array([mya,mya],dtype='float64') #for now, the code is broken if only one element in the array for indexing
        b=N.array([myb,myb],dtype='float64')
        c=N.array([myc,myc],dtype='float64')
        alpha=N.array([myalpha,myalpha],dtype='float64')
        beta=N.array([mybeta,mybeta],dtype='float64')
        gamma=N.array([mygamma,mygamma],dtype='float64')
        #print mydata.metadata
        h=mydata.metadata['orient1']['h']
        k=mydata.metadata['orient1']['k']
        l=mydata.metadata['orient1']['l']
        orient1=N.array([[h,k,l],[h,k,l]],dtype='float64')
        h=mydata.metadata['orient2']['h']
        k=mydata.metadata['orient2']['k']
        l=mydata.metadata['orient2']['l']
        orient2=N.array([[h,k,l],[h,k,l]],dtype='float64')
        orientation=rescalc.lattice_calculator.Orientation(orient1,orient2)
        mylattice=rescalc.lattice_calculator.Lattice(a=a,b=b,c=c,alpha=alpha,beta=beta,gamma=gamma,orientation=orientation)
        h=q['h_center'] #perhaps just take this from the file in the future
        k=q['k_center']
        l=q['l_center']
        H=N.array([h,h],dtype='float64');
        K=N.array([k,k],dtype='float64');
        L=N.array([l,l],dtype='float64');
        W=N.array([0.0,0.0],dtype='float64')
        EXP={}
        EXP['ana']={}
        EXP['ana']['tau']='pg(002)'
        EXP['mono']={}
        EXP['mono']['tau']='pg(002)';
        EXP['ana']['mosaic']=25
        EXP['mono']['mosaic']=25
        EXP['sample']={}
        EXP['sample']['mosaic']=25
        EXP['sample']['vmosaic']=25
        coll1=mydata.metadata['collimations']['coll1']
        coll2=mydata.metadata['collimations']['coll2']
        coll3=mydata.metadata['collimations']['coll3']
        coll4=mydata.metadata['collimations']['coll4']	
        EXP['hcol']=N.array([coll1,coll2,coll3,coll4],dtype='float64')
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
        corrections=myrescal.calc_correction(H,K,L,W,setup,qscan=[[1,0,1],[1,0,1]])
        #print corrections
        return corrections,Q[0]


    def correct_node(self,index):
        qnode=self.qlist[index]
        q=qnode.q
        #I will assume that all data in a node will have the same instrument configuration
        #for now, handle th, 2th corrections, otherwise, need to access correctionsp'q_correction']
        if len(qnode.th)>0:
            mydata=qnode.th[0].data
            corrections,Q=self.correct_data(mydata,qnode.q)
            th_correction=corrections['th_correction'][0]
            qnode.th_correction=th_correction.flatten()[0]
            qnode.Q=Q
            #print 'corrected', qnode.th_correction
        if len(qnode.th2th)>0:
            mydata=qnode.tth[0].data
            corrections,Q=self.correct_data(mydata,qnode.q)
            tth_correction=corrections['tth_correction'][0]
            qnode.tth_correction=tth_correction.flatten()[0]
            qnode.Q=Q

        return

    def correct_nodes(self):
        for index in range(len(self.qlist)):
            self.correct_node(index)
        return

    def condense_node(self,index):
        qnode=self.qlist[index]
        print qnode.q
        #print qnode.th

        a3=[]
        counts=[]
        counts_err=[]
        monlist=[]
        for mydataitem in qnode.th:
            mydata=mydataitem.data
            monlist.append(mydata.metadata['count_info']['monitor'])
            counts_err.append(N.array(mydata.data['counts_err']))
            counts.append(N.array(mydata.data['counts']))
            a3.append(N.array(mydata.data['a3']))
        a3_out,counts_out,counts_err_out=simple_combine(a3,counts,counts_err,monlist)

        #print a3_out.shape
        #print counts_out.shape
        #print counts_err_out.shape
        qnode.th_condensed={}
        qnode.th_condensed['a3']=a3_out
        qnode.th_condensed['counts']=counts_out
        qnode.th_condensed['counts_err']=counts_err_out

        print qnode.th_condensed['counts'].std()
        print qnode.th_condensed['counts'].mean()
        print qnode.th_condensed['counts'].max()
        print qnode.th_condensed['counts'].min()
        if 0:
            pylab.errorbar(a3_out,counts_out,counts_err_out,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
            pylab.show()       
        return 

    def condense_nodes(self):
        for index in range(len(self.qlist)):
            self.condense_node(index)
        return

    def fit_node(self,index):
        qnode=self.qlist[index]
        print qnode.q
        th=qnode.th_condensed['a3']
        counts=qnode.th_condensed['counts']
        counts_err=qnode.th_condensed['counts_err']
        print qnode.th_condensed['counts'].std()
        print qnode.th_condensed['counts'].mean()
        maxval=qnode.th_condensed['counts'].max()
        minval=qnode.th_condensed['counts'].min()
        diff=qnode.th_condensed['counts'].max()-qnode.th_condensed['counts'].min()\
            -qnode.th_condensed['counts'].mean()
        sig=qnode.th_condensed['counts'].std()

        if diff-2*sig>0:
            #the difference between the high and low point and
            #the mean is greater than 3 sigma so we have a signal
            p0=findpeak(th,counts,1)
            print 'p0',p0
            #Area center width Bak
            center=p0[0]
            width=p0[1]
            sigma=width/2/N.sqrt(2*N.log(2))
            Imax=maxval-minval
            area=Imax*(N.sqrt(2*pi)*sigma)
            print 'Imax',Imax
            pin=[area,center,width,0]





            if 1:
                p = NLP(chisq, pin, maxIter = 1e3, maxFunEvals = 1e5)
                #p.lb=lowerm
                #p.ub=upperm
                p.args.f=(th,counts,counts_err)
                p.plot = 0
                p.iprint = 1
                p.contol = 1e-5#3 # required constraints tolerance, default for NLP is 1e-6

    # for ALGENCAN solver gradtol is the only one stop criterium connected to openopt
    # (except maxfun, maxiter)
    # Note that in ALGENCAN gradtol means norm of projected gradient of  the Augmented Lagrangian
    # so it should be something like 1e-3...1e-5
                p.gradtol = 1e-5#5 # gradient stop criterium (default for NLP is 1e-6)
        #print 'maxiter', p.maxiter
        #print 'maxfun', p.maxfun
                p.maxIter=50
    #    p.maxfun=100

        #p.df_iter = 50
                p.maxTime = 4000
        #r=p.solve('scipy_cobyla')
            #r=p.solve('scipy_lbfgsb')
                #r = p.solve('algencan')
                print 'ralg'
                r = p.solve('ralg')
                print 'done'
                pfit=r.xf
                print 'pfit openopt',pfit
                print 'r dict', r.__dict__

            if 0:
                print 'curvefit'
                print sys.executable
                pfit,popt=curve_fit(gauss2, th, counts, p0=pfit, sigma=counts_err)
                print 'p,popt', pfit,popt
                perror=N.sqrt(N.diag(popt))
                print 'perror',perror
                chisqr=chisq(pfit,th,counts,counts_err)
                dof=len(th)-len(pfit)
                print 'chisq',chisqr
            if 0:
                oparam=scipy.odr.Model(gauss)
                mydatao=scipy.odr.RealData(th,counts,sx=None,sy=counts_err)
                myodr = scipy.odr.ODR(mydatao, oparam, beta0=pfit)
                myoutput=myodr.run()
                myoutput.pprint()
                pfit=myoutput.beta
            if 1: 
                print 'mpfit'
                p0=pfit
                parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
                parinfo=[]
                for i in range(len(p0)):
                    parinfo.append(copy.deepcopy(parbase))
                for i in range(len(p0)): 
                    parinfo[i]['value']=p0[i]
                fa = {'x':th, 'y':counts, 'err':counts_err}
                #parinfo[1]['fixed']=1
                #parinfo[2]['fixed']=1
                m = mpfit(myfunct_res, p0, parinfo=parinfo,functkw=fa)
                if (m.status <= 0): 
                    print 'error message = ', m.errmsg
                params=m.params
                pfit=params
                perror=m.perror
                #chisqr=(myfunct_res(m.params, x=th, y=counts, err=counts_err)[1]**2).sum()
                chisqr=chisq(pfit,th,counts,counts_err)
                dof=m.dof
                #Icalc=gauss(pfit,th)
                #print 'mpfit chisqr', chisqr


            if 0:
                width_x=N.linspace(p0[0]-p0[1],p0[0]+p0[1],100)
                width_y=N.ones(width_x.shape)*(maxval-minval)/2
                pos_y=N.linspace(minval,maxval,100)
                pos_x=N.ones(pos_y.shape)*p0[0]
                if 1:
                    pylab.errorbar(th,counts,counts_err,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
                    pylab.plot(width_x,width_y)
                    pylab.plot(pos_x,pos_y)
                    pylab.plot(th,Icalc)
                    pylab.show()

        else:
            #fix center
            #fix width
            print 'no peak'
            #Area center width Bak
            area=0
            center=th[len(th)/2]
            width=(th.max()-th.min())/5.0  #rather arbitrary, but we don't know if it's the first....
            Bak=qnode.th_condensed['counts'].mean()
            p0=N.array([area,center,width,Bak],dtype='float64')  #initial conditions
            parbase={'value':0., 'fixed':0, 'limited':[0,0], 'limits':[0.,0.]}
            parinfo=[]
            for i in range(len(p0)):
                parinfo.append(copy.deepcopy(parbase))
            for i in range(len(p0)): 
                parinfo[i]['value']=p0[i]
            fa = {'x':th, 'y':counts, 'err':counts_err}
            parinfo[1]['fixed']=1
            parinfo[2]['fixed']=1
            m = mpfit(myfunct_res, p0, parinfo=parinfo,functkw=fa)
            if (m.status <= 0): 
                print 'error message = ', m.errmsg
            params=m.params
            pfit=params
            perror=m.perror
            #chisqr=(myfunct_res(m.params, x=th, y=counts, err=counts_err)[1]**2).sum()
            chisqr=chisq(pfit,th,counts,counts_err)
            dof=m.dof
            Icalc=gauss(pfit,th)
            #print 'perror',perror
            if 0:
                pylab.errorbar(th,counts,counts_err,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
                pylab.plot(th,Icalc)
                pylab.show()

        print 'final answer'
        print 'perror', 'perror'
        #If the fit is unweighted (i.e. no errors were given, or the weights
        #	were uniformly set to unity), then .perror will probably not represent
        #the true parameter uncertainties.

        #	*If* you can assume that the true reduced chi-squared value is unity --
        #	meaning that the fit is implicitly assumed to be of good quality --
        #	then the estimated parameter uncertainties can be computed by scaling
        #	.perror by the measured chi-squared value.

        #	   dof = len(x) - len(mpfit.params) # deg of freedom
        #	   # scaled uncertainties
        #	   pcerror = mpfit.perror * sqrt(mpfit.fnorm / dof)

        print 'params', pfit
        print 'chisqr', chisqr  #note that chisqr already is scaled by dof
        pcerror=perror*N.sqrt(m.fnorm / m.dof)#chisqr
        print 'pcerror', pcerror

        self.qlist[index].th_integrated_intensity=N.abs(pfit[0])
        self.qlist[index].th_integrated_intensity_err=N.abs(pcerror[0])    
        Icalc=gauss(pfit,th)
        print 'perror',perror
        if 0:
            pylab.figure()
            pylab.errorbar(th,counts,counts_err,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
            pylab.plot(th,Icalc)
            qstr=str(qnode.q['h_center'])+','+str(qnode.q['k_center'])+','+str(qnode.q['l_center'])
            pylab.title(qstr)
            #pylab.show()

        return

    def fit_nodes(self):
        for index in range(len(self.qlist)):

            self.fit_node(index)
        return

def gauss(p,x):
    #Area center width Bak

    #p=[p0,p1,p2,p3]


    x0=p[1]
    width=p[2]
    sigma=width/2/N.sqrt(2*N.log(2))
    area=N.abs(p[0])/N.sqrt(2*pi)/sigma
    background=N.abs(p[3])
    y=background+area*N.exp(-(0.5*(x-x0)*(x-x0)/sigma/sigma))
    return y

def gauss2(x,p0,p1,p2,p3):
    #Area center width Bak

    p=[p0,p1,p2,p3]


    x0=p[1]
    width=p[2]
    sigma=width/2/N.sqrt(2*N.log(2))
    area=N.abs(p[0])/N.sqrt(2*pi)/sigma
    background=N.abs(p[3])
    y=background+area*N.exp(-(0.5*(x-x0)*(x-x0)/sigma/sigma))
    return y

def chisq(p,a3,I,Ierr):
    Icalc=gauss(p,a3)
    #print I.shape
    #print Ierr.shape
    #print a3.shape
    #print Icalc.shape
    Ierr_temp=copy.deepcopy(Ierr)
    zero_loc=N.where(Ierr==0)[0]
    if len(zero_loc)!=0:
        Ierr_temp[zero_loc]=1.0
    chi=((I-Icalc)/Ierr_temp)**2    
    return chi.sum()/(len(I)-len(p))


def myfunct_res(p, fjac=None, x=None, y=None, err=None):
    # Parameter values are passed in "p"
    # If fjac==None then partial derivatives should not be
    # computed.  It will always be None if MPFIT is called with default
    # flag.
    model = gauss(p, x)
    # Non-negative status value means MPFIT should continue, negative means
    # stop the calculation.
    status = 0
    Ierr_temp=copy.deepcopy(err)
    zero_loc=N.where(err==0)[0]
    if len(zero_loc)!=0:
        Ierr_temp[zero_loc]=1.0
    return [status, (y-model)/Ierr_temp]



def check_q(q1,q2,tol=1e-6):
    heq=False
    keq=False
    leq=False
    #print 'q1,q2',q1,q2
    if N.abs(q2['h_center']-q1['h_center'])< tol:
        heq=True
    if N.abs(q2['k_center']-q1['k_center'])< tol:
        keq=True
    if N.abs(q2['l_center']-q1['l_center'])< tol:
        leq=True
    #print 'heq',heq,'keq',keq,'leq',leq

    return (heq and keq and leq)



def readfiles(flist,tol=1e-4):
    mydatareader=readncnr.datareader()
    H=[]#N.array([])
    I=[]#N.array([])
    Ierr=[]#N.array([])
    monlist=[]
    count=0
    myfirstdata=mydatareader.readbuffer(flist[0])
    mon0=myfirstdata.metadata['count_info']['monitor']
    print 'mon0',mon0
    qtree=Qtree()
    Qtree.mon0=mon0
    #flist=flist[0:12]
    for currfile in flist:
        #print 'MAIN READ',currfile
        mydata=mydatareader.readbuffer(currfile)
        mydata.data['counts_err']=N.sqrt(mydata.data['counts'])*mon0/mydata.metadata['count_info']['monitor']
        mydata.data['counts']=N.array(mydata.data['counts'])*mon0/mydata.metadata['count_info']['monitor']
        mydata.metadata['count_info']['monitor']=mon0
        qtree.addnode(copy.deepcopy(mydata))
        #print 'readloop'
        #print 'q in loop', qtree.qlist[0].q

    for qnode in qtree.qlist:
        print qnode.q['h_center'],qnode.q['k_center'],qnode.q['l_center'],len(qnode.th),qnode.th

    #print qtree.qlist
    return qtree

if __name__=='__main__':
    myfilestr=r'C:\Ce2RhIn8\Mar10_2009\magsc035.bt9'
    #myfilestr=r'c:\bifeo3xtal\jan8_2008\9175\fpx53418.bt7'
    #myfilestr=r'c:\13165\13165\data\MagHigh56784.bt7'
    #myfilestr=r'c:\13176\data\CeOFeAs57255.bt7.out'
    mydatareader=readncnr.datareader()
    mydata=mydatareader.readbuffer(myfilestr)
#    print mydata.__dict__
#    print mydata.additional_metadata
#    print mydata.metadata
#    print mydata.metadata['file_info']['scantype']
#    print mydata.metadata['collimations']
#    print mydata.metadata['dspacing']['monochromator_dspacing']
#    print mydata.metadata['dspacing']['analyzer_dspacing']
#    print mydata.metadata['lattice']['a']
#    print mydata.metadata['lattice']['b']
#    print mydata.metadata['lattice']['c']
#    print mydata.metadata['lattice']['alpha']
#    print mydata.metadata['lattice']['beta']
#    print mydata.metadata['lattice']['gamma']
#    print mydata.metadata['motor3']['step']
#    print mydata.metadata['motor4']['step']
#    print mydata.metadata['count_info']['monitor']
#    print mydata.metadata['energy_info']
#    print mydata.metadata['q_center']['h_center']
#    print mydata.metadata['q_center']['k_center']
#    print mydata.metadata['q_center']['l_center']
#    print mydata.metadata['file_info']['filebase']
#    print mydata.metadata['file_info']['filename']
#    print mydata.metadata['file_info']['fileseq_number']
    print mydata.data.keys()
    myfilebase='magsc'
    myend='bt9'
    mydirectory=r'c:\ce2rhin8\mar10_2009'
    myfilebaseglob=myfilebase+'*.'+myend
    #print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)

    qtree=readfiles(flist)
    qtree.condense_nodes()
    qtree.correct_nodes()
    qtree.fit_nodes()
    qlist=qtree.qlist
    I=[]
    Ierr=[]
    Q=[]
    correction=[]
    for qnode in qlist:
        print qnode.q['h_center'], qnode.q['k_center'],qnode.q['l_center'],qnode.th_integrated_intensity, qnode.th_integrated_intensity_err,qnode.th_correction
        correction.append(qnode.th_correction)
        I.append(qnode.th_integrated_intensity/qnode.th_correction)
        Ierr.append(qnode.th_integrated_intensity_err/qnode.th_correction)
        Q.append(qnode.Q)
    print 'Q',Q
    print 'Correction',correction
    if 1:
        pylab.errorbar(Q,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')

    if 1:
        pylab.show()

    #qtree.condense_node(0)
    #qtree.condense_node(1)
    #qtree.fit_node(0)
    #qtree.fit_node(1)
    #qtree.fit_node(2)