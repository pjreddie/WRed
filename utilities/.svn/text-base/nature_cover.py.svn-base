import csv
import numpy as N
import array
import pylab
import copy
import scipy.interpolate as interpolate

pi=N.pi

def fwhm2sigma(fwhm):
    factor=2*N.sqrt(2*N.log(2.0))
    sigma=fwhm/factor
    return sigma

def area2I(A,fwhm):
    sigma=fwhm2sigma(fwhm)
    print 'sigma ',sigma
    I=A/(N.sqrt(2*pi)*sigma)
    return I

def readfile(myfilestr):
    reader = csv.reader(open(myfilestr))
    header = reader.next()
    data = array.array('f')
    for row in reader:
        data.extend(map(float, row))
    #print 'Data size', len(data)
    #myfile=open(myfilestr)
    #header = myfile.readline()
    #data = N.fromfile(myfile, sep=',')#.reshape(-1,3)
    #myfile.close()
    ndata=N.array(data).reshape(-1,3)
    return ndata

def calcrange(a4lim,data):
    """returns the range of the data array included in the a4lim tuple (a4min,a4max)"""
    a4range=N.intersect1d(N.where(data>a4lim[0])[0],N.where(data<a4lim[1])[0])
    return a4range

def spe_write(T,a4,I,outputfile=None):
    #print len(T)
    #nx ny
    myfile=open(outputfile,'wt')
    s='%5d %5d'%(len(T),a4.size)
    print s
    myfile.write(s+'\n')
    s='###T'
    print s
    myfile.write(s+'\n')
    s=''
    s='%10.4f'%(T[0],)
    count=1
    for i in range(1,len(T)):
        if count==7:
            s=s+'%10.4f\n'%(T[i],)
            count=0
        else:
            s=s+'%10.4f'%(T[i],)
        count=count+1
    print s
    if len(T)%8!=0:
        s=s+'\n'
    myfile.write(s)
    s='###a4'
    print s
    myfile.write(s+'\n')
    #a4 grid
    a4size=a4.size
    s='%10.4f'%(a4[0],)
    count=int(2)
    for i in range(1,a4size):
        if count==8:
            s=s+'%10.4f\n'%(a4[i],)
            #print i,a4[i]
            count=1
        else:
            s=s+'%10.4f'%(a4[i],)
        #print count
            count=count+1

    print s
    if a4size%8!=0:
        s=s+'\n'
    myfile.write(s)
    s=''
    count=2
    for l in range(len(T)):
        s='###Intensity (arb. units)'
        print s
        myfile.write(s+'\n')
        s=''
        I_curr=I[l]
        s='%10.4f'%(I_curr[0],)
        count=int(2)
        for i in range(1,a4size):
            if count==8:
                s=s+'%10.4f\n'%(I_curr[i],)
                #print i,a4[i]
                count=1
            else:
                s=s+'%10.4f'%(I_curr[i],)
            #print count
                count=count+1

        print s
        if a4size%8!=0:
            s=s+'\n'
        myfile.write(s)
        s='###Errors'
        print s
        myfile.write(s+'\n')
        s=''
        I_curr=I[l]
        s='%10.4f'%(I_curr[0],)
        count=int(2)
        for i in range(1,a4size):
            if count==8:
                s=s+'%10.4f\n'%(I_curr[i],)
                #print i,a4[i]
                count=1
            else:
                s=s+'%10.4f'%(I_curr[i],)
            #print count
                count=count+1

        print s
        if a4size%8!=0:
            s=s+'\n'
        myfile.write(s)

        print T





    myfile.close()
    return

if __name__=='__main__':

    print area2I(87.82,.4537)
    mydirectory=r'c:\\12436\superconductor'
    myend='csv'
    myfilebase='lafen015_220_'
    T=[4,60,134,138,141,143,148,153,155,157,175]
    T=[60,134,138,141,143,148,153,155,157,175]
    a4lim=(92.65,95.02)
    a4=N.array([],'float64')
    I=N.array([],'float64')
    Ierr=N.array([],'float64')
    Tlist=N.array([],'float64')
    a4_idl=[]
    I_idl=[]
    T_idl=T
    for currT in T:
        myfilestr=mydirectory+'\\'+str(currT)+'K.'+myend
        print myfilestr
        data=readfile(myfilestr)
        if currT==4:
            data[:,1]=data[:,1]/3
            data[:,2]=data[:,2]/3
            #print '4'
        if currT==60:
            data[:,1]=data[:,1]/6
            data[:,2]=data[:,2]/6
            print 60
        if currT==175:
            data[:,1]=data[:,1]*0.25
            data[:,2]=data[:,2]*0.25
            #print '175'
        #data[:,0]->a4, others go [a4,I,Ierr]
        a4range=calcrange(a4lim,data[:,0])
        if 1:
            if currT in[175,4]:
                pylab.errorbar(data[a4range,0],data[a4range,1],data[a4range,2],marker='s',linestyle='None',mfc='blue',mec='blue',ecolor=None)
        a4=N.concatenate((a4,data[a4range,0]))
        a4_idl.append(data[a4range,0])
        I=N.concatenate((I,data[a4range,1]))
        I_idl.append(data[a4range,1])
        Ierr=N.concatenate((Ierr,data[a4range,2]))
        Tlist=N.concatenate((Tlist,currT*N.ones(data[a4range,2].shape,'float64')))
    if 0:
        pylab.show()
    #print a4
    a4=N.array(a4).flatten()
    I=N.array(I).flatten()
    Ierr=N.array(Ierr).flatten()
    T=N.array(Tlist).flatten()
    print min(a4)
    print max(a4)
    step=.05

    #print T
    a4_out=N.arange(a4lim[0],a4lim[1],step,'float64')
    I_int=N.zeros(a4_out.shape,'float64')
    I_out=[]
    for i in range(len(T_idl)):
        yinterpolater=interpolate.interp1d(a4_idl[i],I_idl[i],fill_value=0.0,kind='linear',copy=True,bounds_error=False)
        I_int=yinterpolater(a4_out)
        I_out.append(I_int)
    outputfile=mydirectory+'\\test.spe'
    spe_write(T_idl,a4_out,I_out,outputfile=outputfile)
    if 0:
        pylab.errorbar(data[a4range,0],data[a4range,1],data[a4range,2],marker='s',linestyle='None',mfc='blue',mec='blue',ecolor=None)
        pylab.show()