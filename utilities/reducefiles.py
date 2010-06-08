import numpy as N
import pylab
from scipy import vectorize
import math
import mpfit
#import scipy.optimize.anneal as anneal

def readheader(myfile):
#get first line
    lineStr=myfile.readline()
    strippedLine=lineStr.rstrip()
    tokenized=strippedLine.split()
#    print tokenized
    header={'filetype':tokenized[5]}
    header['monitor_base']=float(tokenized[6])
    header['monitor_prefactor']=float(tokenized[7])
    header['monitor']=header['monitor_base']*header['monitor_prefactor']
    header['count_type']=tokenized[8]
    header['npts']=float(tokenized[9])
#skip over names of fields 
    lineStr=myfile.readline()
#comment and filename
    lineStr=myfile.readline()
#experiment info
    lineStr=myfile.readline()
#field names of experiment info
    lineStr=myfile.readline()
#motor1
    lineStr=myfile.readline()
    strippedLine=lineStr.rstrip()
    tokenized=strippedLine.split()
#    print tokenized
    motor1={'start':float(tokenized[1])}
    motor1['step']=float(tokenized[2])
    motor1['end']=float(tokenized[3])
    header['motor1']=motor1

#motor2
    lineStr=myfile.readline()
    strippedLine=lineStr.rstrip()
    tokenized=strippedLine.split()
#    print tokenized
    motor2={'start':float(tokenized[1])}
    motor2['step']=float(tokenized[2])
    motor2['end']=float(tokenized[3])
    header['motor2']=motor2
    
#motor3
    lineStr=myfile.readline()
    strippedLine=lineStr.rstrip()
    tokenized=strippedLine.split()
#    print tokenized
    motor3={'start':float(tokenized[1])}
    motor3['step']=float(tokenized[2])
    motor3['end']=float(tokenized[3])
    header['motor3']=motor3

#motor4
    lineStr=myfile.readline()
    strippedLine=lineStr.rstrip()
    tokenized=strippedLine.split()
#    print tokenized
    motor4={'start':float(tokenized[1])}
    motor4['step']=float(tokenized[2])
    motor4['end']=float(tokenized[3])
    header['motor4']=motor4

#motor5
    lineStr=myfile.readline()
    strippedLine=lineStr.rstrip()
    tokenized=strippedLine.split()
#    print tokenized
    motor5={'start':float(tokenized[1])}
    motor5['step']=float(tokenized[2])
    motor5['end']=float(tokenized[3])
    header['motor5']=motor5

#motor6
    lineStr=myfile.readline()
    strippedLine=lineStr.rstrip()
    tokenized=strippedLine.split()
#    print tokenized
    motor6={'start':float(tokenized[1])}
    motor6['step']=float(tokenized[2])
    motor6['end']=float(tokenized[3])
    header['motor6']=motor6


    return header


def readibuff(myfilestr):
    myfile = open(myfilestr, 'r')
    # Get the header information
    header=readheader(myfile)
    #skip over the comment
    lineStr = myfile.readline()
    # get the names of the fields
    lineStr=myfile.readline()
    strippedLine=lineStr.rstrip()
    tokenized=strippedLine.split()
    scan1=tokenized[0]
    scan2=tokenized[1]
#    print scan1
#    print scan2
#   prepare to read the data    
    count =  0
    scan1arr=[]
    scan2arr=[]
    intensity=[]
    intensityerr=[]
    while 1:
        lineStr = myfile.readline()
#        print lineStr
#        print 'Count ', count
        if not(lineStr):
            break
        count = count + 1
        if lineStr[0] != "#":
            #print "#:",count,lineStr.rstrip()
            strippedLine=lineStr.rstrip()
            tokenized=strippedLine.split()
            scan1arr.append(float(tokenized[0]))
            scan2arr.append(float(tokenized[1]))
            intensity.append(float(tokenized[3]))
            intensityerr.append(N.sqrt(float(tokenized[2])))
    myfile.close()
    data={scan1:N.array(scan1arr,'d')}
    data[scan2]=N.array(scan2arr,'d')
    data['intensity']=N.array(intensity,'d')
    data['intensity_err']=N.array(intensityerr,'d')
              
    return header,data

def modelfunction(p,x):
    #[amplitude center fwhm background slope]
    sigma=p[2]/N.sqrt(2*N.log(2))
    center=p[1]
    amp=p[0]/N.sqrt(2*N.pi)/sigma
    background=p[3]
    slope=p[4]
    model=background+slope*x+N.absolute(amp)*N.exp(-0.5*((x-center)/sigma)**2)    
    return model



def chisqrcalc(pfit,fjac=None,x=None,I=None,Ierr=None):
    model=modelfunction(pfit,x)
    chisq=(I-model)/(Ierr)
    chisq=chisq/(N.size(chisq)-N.size(pfit))
#    chisqr=(chisq*chisq).sum()
    status=0
    return [status,chisq]

def fitdata(a4,I,Ierr):
    fa={'x':a4, 'I':I,'Ierr':Ierr}
    parinfo=[]
    lowerm=[]
    upperm=[]
    #[amplitude center fwhm background slope]
    mid=a4[I==I.max()]
    pfit=N.array([I.max(), mid, (a4[a4.size-1]-a4[0])/4, I.min(), 0],'d')
    lowerm=[0,        -2*a4[0],        0,0,0]
    upperm=[10*I.max(),2*a4[a4.size-1],(a4[a4.size-1]-a4[0]),2*I.min(0)+1,1]
    print lowerm
    print upperm
    print pfit
    for i in range(pfit.size):
##        parinfo.append({'value':0., 'fixed':0, 'limited':[1,1],\
##                        'limits':[lowerm[i], upperm[i]], 'step':0})
        parinfo.append({'value':0., 'fixed':0, 'limited':[1,1],\
                        'limits':[lowerm[i], upperm[i]], 'step':0})

    parinfo[4]['fixed']=1
    m = mpfit.mpfit(chisqrcalc, pfit, parinfo=parinfo,functkw=fa,quiet=1)
    print 'status = ', m.status
    if (m.status <= 0): print 'error message = ', m.errmsg    
    p=N.array(m.params,'d')
#    print 'p ', p
    dof=a4.size -p.size
#    print 'dof ',dof
    std=m.perror*N.sqrt(m.fnorm/dof)
    return p,std

def readfile(header,data):
    a4=N.array(data['A4'],'d')
    I=N.array(data['intensity'],'d')
    Ierr=N.array(data['intensity_err'],'d')
    return a4,I,Ierr

def plotdata(a4,I,Ierr,p):
    pylab.errorbar(a4,I,Ierr,marker='o',linestyle=None)
    model=modelfunction(p,a4)
    pylab.plot(a4,model,'r')
#    pylab.show()


def readfiles(mydirectory,myend,myfilehead,myfiles,reflections,ploton):
    summarydict={}
    summarylist=[]
    pylab.clf()
    cols=3
    rows=N.ceil(float(reflections.shape[0])/cols)
    pylab.hold(True)
    for i in range(reflections.shape[0]):
        hkl=reflections[i]
        hklstr=str(hkl[0])+str(hkl[1])+str(hkl[2])
        myfilestr=mydirectory+myfilehead+myfiles[i]+myend
        print myfilestr,i
        header,data=readibuff(myfilestr)        
        a4,I,Ierr=readfile(header,data)
        p,std=fitdata(a4,I,Ierr)        
        pylab.subplot(rows,cols,i+1)
        plotdata(a4,I,Ierr,p)
        datadict={'p':p,'std':std,'hkl':hkl}
        summarydict[hklstr]=datadict
        summarylist.append(datadict)
    pylab.hold(False)
    if ploton:
        pylab.show()
    return summarylist    

def outputresult(summarylist):
    for i in range(len(summarylist)):
        l=summarylist[i]
        lineStr=str(l['hkl'][0])+' '+str(l['hkl'][1])+' '+str(l['hkl'][2])
        lineStr=lineStr+' '+str(l['p'][1])+' '+str(l['p'][0])+' '+str(l['std'][0])
        print lineStr
    return

def saveresult(summarylist,outputfile):
    myfile = open(outputfile, 'w')
    lineStr='# h k l a4 I Ierr'
    myfile.write("%s\n" % lineStr)

    for i in range(len(summarylist)):
        l=summarylist[i]
        lineStr=str(l['hkl'][0])+' '+str(l['hkl'][1])+' '+str(l['hkl'][2])
        lineStr=lineStr+' '+str(l['p'][1])+' '+str(l['p'][0])+' '+str(l['std'][0])
        myfile.write("%s\n" % lineStr)
    myfile.close()
    return

def mergearrays(a):
    c=a[0]
    for i in range(len(a)):
        c=N.union1d(c,a[i])
    return c

def registerarrays(a,combined_arr):
    b=[]
    outputarray=[]
    for i in range(len(combined_arr)):
        b=[]
        for j in range(len(a)):
            curr_arr=a[j]
            listofindices=N.where(curr_arr==combined_arr[i])
            #where returns a tuple!
            b.append(listofindices[0])
        outputarray.append(b)
    return outputarray

def addarrays(d,outputarray,Iarray,monitorarray):
    L=len(d)
    I=[]
    Ierr=[]
#    print 'Iarr ', Iarray
    for i in range(L):
        ind=outputarray[i]
        Ival=0
        monval=0
        for j in range(len(Iarray)):
#           print 'ind', ind
           if (len(ind) != 0):
               currI=Iarray[j]
#               print 'CurrI ', currI
               selectI=currI[ind[j]]
               # sum over the values of a4
               monval=monval+monitorarray[j]*len(selectI)
               Isum=N.sum(selectI)
               Ival=Ival+Isum
        I.append(float(Ival)/monval)
        Ierr.append(N.sqrt(float(Ival))/monval)
    return N.array(I),N.array(Ierr)

def addarraysbasic(inputx,inputy,inputmon):
    combined_array=mergearrays(inputx)
#    print 'combined ', combined_array
#    print 'inputmon ',inputmon
#    print 'norm ', inputmon[0]
    indice_list=registerarrays(inputx,combined_array)
    I,Ierr=addarrays(combined_array,indice_list,inputy,inputmon)
    I=I*inputmon[0]
    Ierr=Ierr*inputmon[0]
    return N.array(combined_array),I,Ierr




def addfiles(headers,data,hkl):
    norm_monitor=headers[0]['monitor']
    monitorarr=[]
    a4arr=[]
    Iarr=[]
    for i in range(len(headers)-0):
        monitorarr.append(headers[i]['monitor'])
        a4curr,Icurr,Ierrcurr=readfile(headers[i],data[i])
        a4arr.append(a4curr)
        Iarr.append(Icurr)
#    print a4arr
#    print Iarr
#    print monitorarr
    a4out,Iout,Ierrout=addarraysbasic(a4arr,Iarr,monitorarr)
#    pylab.hold(True)
#    pylab.errorbar(a4out,Iout,Ierrout,marker='o',linestyle=None)
#    pylab.errorbar(a4arr[0],Iarr[0],N.sqrt(Iarr[0]),mfc='red',marker='o',linestyle=None)
#    pylab.errorbar(a4arr[1],Iarr[1],N.sqrt(Iarr[1]),mfc='green',marker='o',linestyle=None)
#    pylab.show()

    p,std=fitdata(a4out,Iout,Ierrout)        
    plotdata(a4out,Iout,Ierrout,p)
#    pylab.show()
    hklstr=str(hkl[0])+str(hkl[1])+str(hkl[2])
    datadict={'p':p,'std':std,'hkl':hkl}
    summarylist=datadict


    return summarylist
        


if __name__=="__main__":
#    myfilestr=r'c:\bifeo3xtal\nu024001.bt9'
    #single files
#    summarydict={}
    #files to be added
#    myfiles006=['006001','006003']
# note:110 and 104 are very close in theta and twotheta!!!
    if 1:
#        myfiles006=['006001','006003']
        mydirectory=r'c:\bifeo3\data\bifeo3xtal\\'
        
        myfiles116=['116001','116002']
        myend='.bt9'
        myfilehead='nu'
        headers=[]
        data=[]
        for i in range(len(myfiles116)-0):
            myfilestr=mydirectory+myfilehead+myfiles116[i]+myend
            header,datum=readibuff(myfilestr)
            headers.append(header)
            data.append(datum)
        #summarylist=addfiles(headers,data)
        #print summarylist
#        print headers
#        print data
#        a4out,Iout,Ierrout=addfiles(headers,data,[1,1,6])
        summarylist116=addfiles(headers,data,[1,1,6])
        print summarylist116
#        print a4out
#        print Iout
#        print Ierrout
    

#nuclear
    if 1:
#        mydirectory=r'c:\bifeo3\data\bifeo3xtal\\'
        myend='.bt9'
        myfilehead='nu'
        reflections=N.array([[0,2,4],[1,1,3],[1,2,2],[2,0,2],[2,1,1],[1,0,4],[1,1,0]\
                             ,[0,0,6]])
        myfiles=['024001','113001','122001','202001','211001','104004','110002'\
                ,'006003']
        ploton=0
        summarylist=readfiles(mydirectory,myend,myfilehead,myfiles,reflections,ploton)
        summarylist.append(summarylist116)
#        print fullsummarylist
#        print summarylist116

        outputresult(summarylist)
        saveresult(summarylist,mydirectory+'nuclear.dat')
        

    if 0:
        myfiles116=['116001','116002']
        myend='.bt9'
        myfilehead='m'
        reflections=N.array([[0,0,3],[0,0,3],[1,0,7],[1,1,3],[2,0,5]\
                             ,[1,0,1],[1,0,1],[1,0,1]])
        myfiles=['003l001','003r001','a107001','a113001','a205001'\
                 ,'101l001','101c001','101r001']

        ploton=1
        summarylist=readfiles(mydirectory,myend,myfilehead,myfiles,reflections,ploton) 
        outputresult(summarylist)
        #saveresult(summarylist,mydirectory+'mag.dat')
     



