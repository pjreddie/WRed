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
import sys
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

def get_highT_file():
        mydirectory=r'C:\12436\data'
        #myfilestr=mydirectory+'\\'+'LaOFeAs56416.stitched'
        myfilestr=mydirectory+'\\'+'170Kch4to44good.dat'
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

def get_lowT_file():
        mydirectory=r'C:\12436\data'
        #myfilestr=mydirectory+'\\'+'LaOFeAs56413.stitched'
        myfilestr=mydirectory+'\\'+'8Kch4to44good.dat'
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
        return a4,I,Ierr,Tstitched,mon_stitched

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

if __name__=='__main__':
    delta=.03
    mydirectory=r'C:\12436\data'
    if len(sys.argv)>1:
        delta=float(sys.argv[1])
    print 'delta= ',delta
    a4_high,I_high,Ierr_high,Tstiched_high,mon_stiched_high=get_highT_file()
    a4_low,I_low,Ierr_low,Tstiched_low,mon_stiched_low=get_lowT_file()
    a4_high_max=max(a4_high)
    a4_high_min=min(a4_high)
    a4_low_max=max(a4_low)
    a4_low_min=min(a4_low)
    a4min=max(a4_low_min,a4_high_min)
    a4max=min(a4_low_max,a4_high_max)
    a4range_high=N.intersect1d(N.where(a4_high>a4min)[0],N.where(a4_high<a4max)[0])
    a4range_low=N.intersect1d(N.where(a4_low>a4min)[0],N.where(a4_low<a4max)[0])
    a4list=[a4_low,a4_high+delta]
    Ilist=[I_low,-I_high]
    Ierrlist=[Ierr_low,Ierr_high]
    monlist=[mon_stiched_low,mon_stiched_high]
    a4out,Iout,Ierrout=simple_combine.simple_combine(a4list,Ilist,Ierrlist,monlist,method='interpolate',step=0.1)
    print 'done'
    background=300.0
    Iout=Iout+background
    myfilestr=mydirectory+'\\'+'subtracted.txt'
    output(a4out,Iout,Ierrout,outputfile=myfilestr)
    #exit()
    pylab.subplot(3,1,1)
    pylab.errorbar(a4_low,I_low,Ierr_low,linestyle='None',marker='s',mfc='blue',markersize=1.0)
    pylab.subplot(3,1,2)
    pylab.errorbar(a4_high,I_high,Ierr_high,linestyle='None',marker='s',mfc='red',markersize=2.0)
    pylab.subplot(3,1,3)
    #for delta in N.arange(-.1,.1,.01):
    #    print delta
    pylab.errorbar(a4out,Iout-background,Ierrout,linestyle='None',marker='s',mfc='green',markersize=1.0)
    pylab.ylim((-30,30))
    pylab.show()