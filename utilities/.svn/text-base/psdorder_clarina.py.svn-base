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
pi=N.pi

psd_a4_spacing=N.array([46.35,	  46.45,    46.54,     46.69,    46.84,     46.94,\
                        47.10,    47.23,    47.33,     47.46,    47.60,     47.71, \
                        47.85,    47.97,    48.14,     48.26,    48.33,     48.47, \
                        48.63,    48.72,    48.84,     48.95,    49.11,     49.21, \
                        49.38,    49.49,    49.61,     49.75,    49.90,     50.02, \
                        50.18,    50.28,    50.40,     50.53,    50.65,     50.81, \
                        50.91,    51.06,    51.19,     51.30,    51.46,     51.60, \
                        51.71,    51.83,    51.95,     52.09,    52.23,     52.14])
psd_a4_offset=-(psd_a4_spacing-psd_a4_spacing[23])
psd_a4_offset=N.reshape(psd_a4_offset,(psd_a4_offset.shape[0],1))
##psd_channel_efficiency=N.array([3.9918,	2.4668,	2.7027,	2.5016,	2.2414,	2.2440,	2.0113,	1.900,\
##                                1.7849,	1.7825,	1.6490,	1.4734,	1.3835,	1.3968,	1.3708,\
##                                1.1635,	1.1048,	1.1963,	1.1978,	1.0392,	1.0331,	1.0618,\
##                                1.0604,	1.0070,	0.9740,	1.0298,	1.0495,	0.9566,	0.9487,\
##                                1.0109,	1.0164,	0.9770,	0.9357,	1.0383,	1.0691,	0.9457,\
##                                0.9757,	0.9992,	1.0464,	0.9587,	0.9375,	0.9888,	0.9721,\
##                                0.9391,	0.9335,	0.9982,	0.8798,	0.9205])
psd_channel_efficiency=N.array([2.2372,		1.0000,		0.9487,		0.7647,		0.9304,		0.9620,\
                                1.1265,		0.0000,		0.9179,		1.0021,		0.9215,		0.8858,\
                                1.0105,		0.9737,		1.0434,		0.0000,		0.9358,		0.9897,\
                                1.0479,		0.9268,		0.8924,		0.9487,		1.0300,		0.9544,\
                                0.9127,		1.0000,		0.9918,		1.0021,		1.0063,		1.0105,\
                                1.0212,		0.9093,		1.0234,		1.0858,		1.0084,		0.9179,\
                                1.0000,		1.1032,		1.1480,		1.0000,		0.9959,		1.0084,\
                                0.9776,		1.1032,		0.9450,		1.0234,		1.0234,		1.1847])
psd_channel_efficiency=N.reshape(psd_channel_efficiency,(psd_channel_efficiency.shape[0],1))


def read_stitched(myfilestr):
    myfile = open(myfilestr, 'r')
    #get first line
    myFlag=True
    a4=[]
    I=[]
    Ierr=[]
    while myFlag:
        tokenized=readncnr.get_tokenized_line(myfile)
        #print tokenized
        if tokenized !=[]:
            a4.append(float(tokenized[0]))
            I.append(float(tokenized[1]))
            Ierr.append(float(tokenized[2]))
        if tokenized==[]:
            break
    myfile.close()
    I=N.array(I)
    Ierr=N.array(Ierr)
    a4=N.array(a4)
    return a4,I,Ierr




def read_order_files(flist):
#    myfilebaseglob=myfilebase+'*.'+myend
#    print myfilebaseglob
#    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readncnr.datareader()
    H=[]#N.array([])
    I=[]#N.array([])
    Ierr=[]#N.array([])
    monlist=[]
    count=0
    mon0=5.0e4
    a4list=[]
    for currfile in flist:
        #print currfile
        mydata=mydatareader.readbuffer(currfile)
        #if count==0:
        #    #mon0=mydata.header['count_info']['monitor']
        #    mon0=5.0e4
        mon=mydata.data['monitor'][0]
        if count==0:
            mon0=mon
        #print count, mon0,mon
        #temp=N.concatenate((temp,N.array(mydata.data['temp'])))
        H.append(N.array(mydata.data['temp'],'float64'))
        psd_detectors=mydata.metadata['count_info']['AnalyzerDetectorDevicesOfInterest'.lower()]
        psd_arr=[]
        a4_center=[]
        a4=N.array(mydata.data['a4'],'float64')
        for psd in psd_detectors:
            psd_arr.append(N.array(mydata.data[psd],'float64'))
            a4_center.append(a4)
        #print 'loop done'
        psd_arr=N.array(psd_arr,'float64')
        effs=N.tile(psd_channel_efficiency,(1,psd_arr.shape[1]))
        Ierr.append(N.sqrt(psd_arr)*effs*mon0/mon)
        #Ierr=N.concatenate((Ierr,N.sqrt(psd_arr)*effs))
        #print 'psdarr shape ',psd_arr.shape
        #print 'new shape ',N.tile(psd_channel_efficiency,(1,psd_arr.shape[1])).shape
        psd_arr=psd_arr*effs*mon0/mon
        a4_center_arr=N.array(a4_center)
        #print psd_arr.shape
        #print a4_center_arr.shape
        #print psd_a4_offset
        #print N.tile(psd_a4_offset,(1,a4.shape[0])).shape
        a4_corrected=a4_center_arr+N.tile(psd_a4_offset,(1,a4.shape[0]))
        #print a4_corrected
        a4list.append(a4_corrected)
        #It=N.array(N.array(mydata.data['detector']),'float64')
        #Iterr=N.sqrt(It)
        monlist.append(mon)
        I.append(psd_arr)
        #I=N.concatenate((I,psd_arr))
        #Ierr.append(N.sqrt(psd_arr))
        count=count+1
    #print H
    #print I
    #print Ierr
    #print I[0].shape
    #print 'I shape ',I[1].shape
    #for i in range(48):
    #    I[],Ierr=simple_combine.monitor_normalize(I[],Ierr,monlist)
    I=N.hstack(I)
    Ierr=N.hstack(Ierr)
    print I.shape
    print Ierr.shape
    H=N.hstack(H)
    monlist=N.hstack(monlist)
    a4list=N.hstack(a4list)
    #print N.array(I)
    #print a4list
    return N.array(H),N.array(I),N.array(Ierr),N.array(monlist),N.array(a4list)


def orderparameter(p,T):
    #p[0]=Intensity
    #I0,Tc,Beta,background=p
    Beta=0.5
    I0,Tc,background=p

    I=N.absolute(I0)*N.power(N.absolute(T/N.absolute(Tc)-1),2*N.absolute(Beta))
    I[T>Tc]=0.0
    I=I+background
    return I

def gaussian(p,x):
    #p[0]=Intensity
    area,xc,w,background,slope=p
    amp1=area/N.sqrt(2*pi)/w
    #[I Center Width Bak]
    peakshape=N.absolute(background)+N.absolute(amp1)*N.exp(-0.5*((x-N.absolute(xc))/N.absolute(w))**2)+slope*x
    return peakshape


def chisq_calc(p,x,I,Ierr):
    Icalc=gaussian(p,x)
    chisq=(I-Icalc)*(I-Icalc)/p.shape[0]/Ierr/Ierr
    return chisq

def residuals(p,x,I,Ierr):
    Icalc=gaussian(p,T)
    residual=(I-Icalc)/Ierr
    return residual



def get_background_file():
        myfilestr=mydirectory+'\\'+'LaOFeAs56416.stitched'
        flist=[myfilestr]
        print flist
        a4,I,Ierr=read_stitched(myfilestr)
        Tstitched=170
        mon_stitched=80000
        a4min=33.7
        a4max=35.8
        a4range=N.intersect1d(N.where(a4>a4min)[0],N.where(a4<a4max)[0])

        if 0:
            #Icalc=gaussian(pfit,a4[a4range])
            pylab.errorbar(a4[a4range],I[a4range],Ierr[a4range],marker='s',linestyle='None',mfc='blue',mec='blue',ecolor=None)
            #pylab.plot(a4[a4range],Icalc,'r')
            pylab.show()
        return a4,I,Ierr,Tstitched,mon_stitched

def get_highT_file():
        myfilestr=mydirectory+'\\'+'LaOFeAs56413.stitched'
        flist=[myfilestr]
        print flist
        a4,I,Ierr=read_stitched(myfilestr)
        I_int=[]
        I_err=[]
        Tstitched=8.7
        mon_stitched=80000
        a4min=33.7
        a4max=35.8
        a4range=N.intersect1d(N.where(a4>a4min)[0],N.where(a4<a4max)[0])

        p0=[copy.deepcopy(max(I[a4range]))*1.5,34.7,0.4,copy.deepcopy(I[-1]),0]
        #[Area xc width background slope]
        #print 'p0 ',p0

        #print 'a4range ',a4[a4range]
        oparam=scipy.odr.Model(gaussian)
        mydata=scipy.odr.RealData(a4[a4range],I[a4range],sx=None,sy=Ierr[a4range])
        myodr = scipy.odr.ODR(mydata, oparam, beta0=p0)
        myoutput=myodr.run()
        myoutput.pprint()
        pfit=myoutput.beta
        I_int.append(pfit[0])
        I_err.append(myoutput.sd_beta[0])
        #help(myoutput)
        #print 'pfit ',pfit
        if 0:
            Icalc=gaussian(pfit,a4[a4range])
            pylab.errorbar(a4[a4range],I[a4range],Ierr[a4range],marker='s',linestyle='None',mfc='blue',mec='blue',ecolor=None)
            pylab.plot(a4[a4range],Icalc,'r')
            pylab.show()
        return a4,I,Ierr,Tstitched,mon_stitched


def manyplots(peak1):
        if 1:
            n=0
            #pylab.errorbar(peak5.a4[n,:],peak5.I[n,:],peak5.Ierr[n,:],linestyle='None',marker='s',mfc='blue')
            for n in range(peak1.H.shape[0]/3):
                if n%12==0:
                    pylab.figure(n/12)
                pylab.subplot(4,3,n%12+1)
                pylab.errorbar(peak1.a4[:,n],peak1.I[:,n],peak1.Ierr[:,n],linestyle='None',marker='s',mfc='blue')
                pylab.xlim((33.7,35.8))
                pylab.ylim((30,150))
                pylab.title(peak1.H[n])
            pylab.show()
        return()

def output(a4,I,Ierr,outputfile=None):
        s=''
        if outputfile!=None:
            f=open(outputfile,'wt')
        for i in range(a4.size):
            s=s+'%2.3f %2.3f %2.3f'%(a4[i],I[i],Ierr[i])
            s=s+'\n'
        if outputfile==None:
            print s
        else:
            f.write(s)
        if outputfile!=None:
            f.close()
        return


def averagesum(peak1):
        a4min=34
        a4max=35.5
        a4=peak1.a4[:,0]
        monlist=peak1.monlist
        a4range=N.intersect1d(N.where(a4>a4min)[0],N.where(a4<a4max)[0])
        l=min(a4range)
        r=max(a4range)
        print a4range
        print 'l=',l,' r=',r
        #a4,I,Ierr,Tstitched,mon_stitched=get_highT_file()
        #a4range=N.intersect1d(N.where(a4>a4min)[0],N.where(a4<a4max)[0])
        #I=I*monlist[0]/mon_stitched
        #Ierr=Ierr*monlist[0]/mon_stitched
        #pylab.errorbar(a4[a4range],peak1.I[a4range,95],peak1.Ierr[a4range,95],linestyle='None',marker='s',mfc='blue')
        #pylab.show()
        #exit()
        #print 'a4range ',a4range
        #I_sum=0.0
        #Ierr_sum=0.0
        #for i in range(l,r):
        #    I_sum=I_sum+I[i]
        #    Ierr_sum=Ierr+Ierr[i]**2
        #Ierr_sum=N.sqrt(Ierr_sum)
        #print 'l=',l,' r=',r
        #print 'I_sum=',N.average(peak1.I[l:r])*0.5
        #print 'I_err=',N.sqrt(N.average(peak1.Ierr[l:r]**2))*0.5



        #exit()
        l=min(a4range)
        r=max(a4range)
        print 'a4range ',a4range
        I=N.zeros(peak1.I[l,:].shape)
        Ierr=N.zeros(peak1.I[l,:].shape)
        for i in range(l,r):
            I=I+peak1.I[i,:]
            Ierr=Ierr+peak1.Ierr[i,:]**2
        print 'a4size ',a4range.size
        I=I/(r-l-1)
        Ierr=N.sqrt(Ierr)/(r-l-1)
        print N.average(peak1.I[l:r,:],axis=0)
        print 'peak1'
        print peak1.I[l:r,95]
        print 'H',H[95]
        print H.size
        #exit()
        H_ave=[]
        I_ave=[]
        Ierr_ave=[]
        ave=1
        #print 'H ', H
        if ave >1:
            for i in range(0,H.size-ave,ave):
                print i
                Ierr_ave.append(N.sqrt((Ierr[i:i+ave-1]**2).sum())/ave)
                I_ave.append(N.average(I[i:i+ave-1]))
                H_ave.append(N.average(H[i:i+ave-1]))
        if ave==1:
            Ierr_ave=Ierr
            I_ave=I
            H_ave=H
        I=N.array(I_ave)
        Ierr=N.array(Ierr_ave)
        H_ave=N.concatenate((H_ave,N.array([8.5])))
        Imax=I_ave.max()
        I_ave=N.concatenate((I_ave,N.array([45.32])))/Imax
        Ierr_ave=N.concatenate((Ierr_ave,N.array([1.327])))/Imax
        if 1:
            pylab.errorbar(H_ave,I_ave,Ierr_ave,linestyle='None',marker='s',mfc='blue')
            #pylab.ylim((40,150))
            pylab.show()
        exit()
        T=N.array(H_ave)
        #print T
        #print 'I0 ',I[0]
        #p0=[copy.deepcopy(I[0]),117.0,.33333,copy.deepcopy(I[-1])]
        p0=[copy.deepcopy(I[0]),120.0,copy.deepcopy(I[-1])]
        print 'p0 ',p0
        tmin=75
        tmax=200.0

        #print N.where(T>20)
        #exit()
        Trange=N.intersect1d(N.where(T>tmin)[0],N.where(T<tmax)[0])

        #print 'Trange ',Trange
        oparam=scipy.odr.Model(orderparameter)
        mydata=scipy.odr.RealData(T[Trange],I[Trange],sx=None,sy=Ierr[Trange])
        #mydata=scipy.odr.RealData(T,I,sx=None,sy=Ierr)
        myodr = scipy.odr.ODR(mydata, oparam, beta0=p0)
        myoutput=myodr.run()
        #myoutput.pprint()
        pfit=myoutput.beta
        #pfit = leastsq(residuals, p0, args=(T[Trange],I[Trange],Ierr[Trange]))
        print 'pfit=',pfit
        print 'perror= ',myoutput.sd_beta
        #print 'chisq=',chisq_calc(pfit,T[Trange],I[Trange],Ierr[Trange]).sum()
        Icalc=orderparameter(pfit,T)
        if 1:
            pylab.errorbar(T,I,Ierr,marker='s',linestyle='None',mfc='blue',mec='blue',ecolor=None)
            pylab.plot(T,Icalc)
            pylab.xlabel('T (K)')
            pylab.ylabel('Counts (arb. units)')
            #pylab.ylim((3000*0,7000))
            #pylab.xlim((10,tmax))
            #pylab.arrow(tmax,2000,0,500,fc='black',ec='black',width=.5)
            #pylab.arrow(tmin,2000,0,500,fc='black',ec='black',width=.5)
            pylab.show()
        return()

class peak():
    def __init__(self):
        pass


if __name__=='__main__':
    if 0:
        x=N.arange(-2,2,.25)
        p=[1.,0.5,1.,10.]
        y=gaussian(p,x)
        pylab.plot(x,y,linewidth=0,marker='s')
        pylab.show()
    if 1:
        #mydirectory=r'C:\ca3comno6\Feb4_2008\Ca3CoMnO6\Feb4_2008\data'
        #mydirectory=r'C:\ca3comno6\Feb4_2008\data'
        mydirectory=r'C:\12436\data'
        myfilebase='LaOFeAsImpuritydown'
        myend='bt7'
        flist=[]
        rlist=[56421,56420,56419]
        for myfileseq in rlist:#range(56419,56421,1):
            print myfileseq
            myfilestr=mydirectory+'\\'+myfilebase+str(myfileseq)+'.'+myend
            flist.append(myfilestr)

        #myfilestr=mydirectory+'\\'+'LaOFeAs56413.bt7'
        #flist.append(myfilestr)
        #myfilestr=mydirectory+'\\'+'LaOFeAs56416.bt7'
        #flist.append(myfilestr)

        print flist
        H,I,Ierr,monlist,a4=read_order_files(flist)
        print H.shape
        #order is file, field
        peak1=peak()
        peak1.H=H
        peak1.I=I
        peak1.Ierr=Ierr
        peak1.a4=a4
        peak1.monlist=monlist
        #print peak1.Ierr[0:17,95]
        #print peak1.I[0:17,95]
        #exit()
        averagesum(peak1)
        exit()
        a4,I,Ierr,Tstitched,mon_stitched=get_highT_file()
        a4min=34
        a4max=35.5
        a4=peak1.a4[:,0]
        #fix the a4 range
        a4range=N.intersect1d(N.where(a4>a4min)[0],N.where(a4<a4max)[0])
        l=min(a4range)
        r=max(a4range)
        print 'a4range ',a4range
        I_sum=0.0
        Ierr_sum=0.0
        #for i in range(l,r):
        #    I_sum=I_sum+I[i]
        #    Ierr_sum=Ierr+Ierr[i]**2
        #Ierr_sum=N.sqrt(Ierr_sum)
        print 'l=',l,' r=',r
        print 'I_sum=',N.average(I[l:r])*monlist[0]/mon_stitched
        print 'I_err=',N.sqrt(N.average(Ierr[l:r]**2))*monlist[0]/mon_stitched
        print monlist[0]
        exit()
        I=I*monlist[0]/mon_stitched
        Ierr=Ierr*monlist[0]/mon_stitched
        pylab.errorbar(a4,I,Ierr,linestyle='None',marker='s',mfc='blue')
        pylab.show()
        print monlist
        print mon_stitched
        exit()
        l=17
        r=23
        a4min=34
        a4max=35.5
        a4min=33.7
        a4max=35.7
        a4=peak1.a4[:,0]
        #fix the a4 range
        a4range=N.intersect1d(N.where(a4>a4min)[0],N.where(a4<a4max)[0])
        l=min(a4range)
        r=max(a4range)
        #print a4.shape
        H_ave=[]
        I_ave=[]
        Ierr_ave=[]
        ave=5
        print 'H ',H.shape
        #print 'H ', H
        if ave >1:
            for i in range(0,H.size-ave,ave):
                #print i
                Ierr_ave.append(N.sqrt((Ierr[:,i:i+ave-1]**2).sum(axis=1)))
                I_ave.append(I[:,i:i+ave-1].sum(axis=1))
                H_ave.append(N.average(H[i:i+ave-1]))
        if ave==1:
            Ierr_ave=Ierr,
            I_ave=I
            H_ave=H
        I=N.array(I_ave)[:,a4range]
        Ierr=N.array(Ierr_ave)[:,a4range]
        a4=a4[a4range]
        H=N.array(H_ave)
        print I.shape
        if 1:
            for i in range(H.size/2,H.size):
                print 'T= ',H[i]
                pylab.errorbar(a4,I[i,:],Ierr[i,:],linestyle='None',marker='s',mfc='blue')
            #pylab.errorbar(a4,I[30,:],Ierr[0,:],linestyle='None',marker='s',mfc='blue')
            #pylab.ylim((40,150))
            pylab.show()
        exit()
        T=N.array(H_ave)
        #print T
        #print 'I0 ',I[0]
        #p0=[copy.deepcopy(I[0]),117.0,.33333,copy.deepcopy(I[-1])]
        p0=[copy.deepcopy(I[0]),127.0,copy.deepcopy(I[-1])]
        tmin=120
        tmax=200.0

        #print N.where(T>20)
        #exit()
        Trange=N.intersect1d(N.where(T>tmin)[0],N.where(T<tmax)[0])

        #print 'Trange ',Trange
        oparam=scipy.odr.Model(orderparameter)
        mydata=scipy.odr.RealData(T[Trange],I[Trange],sx=None,sy=Ierr[Trange])
        #mydata=scipy.odr.RealData(T,I,sx=None,sy=Ierr)
        myodr = scipy.odr.ODR(mydata, oparam, beta0=p0)
        myoutput=myodr.run()
        #myoutput.pprint()
        pfit=myoutput.beta
        #pfit = leastsq(residuals, p0, args=(T[Trange],I[Trange],Ierr[Trange]))
        print 'pfit=',pfit
        print 'perror= ',myoutput.sd_beta
        #print 'chisq=',chisq_calc(pfit,T[Trange],I[Trange],Ierr[Trange]).sum()
        Icalc=orderparameter(pfit,T)
        if 0:
            pylab.errorbar(T,I,Ierr,marker='s',linestyle='None',mfc='blue',mec='blue',ecolor=None)
            pylab.plot(T,Icalc)
            pylab.xlabel('T (K)')
            pylab.ylabel('Counts (arb. units)')
            #pylab.ylim((3000*0,7000))
            #pylab.xlim((10,tmax))
            #pylab.arrow(tmax,2000,0,500,fc='black',ec='black',width=.5)
            #pylab.arrow(tmin,2000,0,500,fc='black',ec='black',width=.5)
            pylab.show()























##        if 1:
##            for n in range(H.size/4):
##                print 'T=',H[n]
##                a4=peak1.a4[:,n]
##                I=peak1.I[:,n]
##                Ierr=peak1.Ierr[:,n]
##                a4min=30
##                a4max=34
##                a4range=N.intersect1d(N.where(a4>a4min)[0],N.where(a4<a4max)[0])
##                a4find=N.where(a4==34.4)[0]
##                #print 'max ', max(I[a4range])
##                p0=[copy.deepcopy(max(I[a4range]))*1.5,32.5,0.4,copy.deepcopy(I[-1]),0]
##                #[Area xc width background slope]
##                #print 'p0 ',p0
##
##                #print 'a4range ',a4[a4range]
##                oparam=scipy.odr.Model(gaussian)
##                mydata=scipy.odr.RealData(a4[a4range],I[a4range],sx=None,sy=Ierr[a4range])
##                myodr = scipy.odr.ODR(mydata, oparam, beta0=p0)
##                myoutput=myodr.run()
##                myoutput.pprint()
##                pfit=myoutput.beta
##                I_int.append(pfit[0])
##                I_err.append(myoutput.sd_beta[0])
##                #help(myoutput)
##                #print 'pfit ',pfit
##                if 0:
##                    Icalc=gaussian(pfit,a4[a4range])
##                    pylab.errorbar(a4[a4range],I[a4range],Ierr[a4range],linestyle='None',marker='s',mfc='blue')
##                    pylab.plot(a4[a4range],Icalc,'r')
##                    pylab.show()
##            if 0:
##                pylab.errorbar(H,I_int,I_err,linestyle='None',marker='s',mfc='blue')
##                #pylab.ylim((0,1400))
##                pylab.show()
##            #print a4find







        exit()

