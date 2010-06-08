import numpy as N
import pylab
import scriptutil as SU
import re
import readncnr

def read_order_files(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readncnr.datareader()
    temp=N.array([])
    I=N.array([])
    Ierr=N.array([])
    count=0
    mon0=5.0e4
    for currfile in flist:
        print currfile
        mydata=mydatareader.readbuffer(currfile)
        if count==0:
            #mon0=mydata.header['count_info']['monitor']
            mon0=5.0e4
        mon=mydata.header['count_info']['monitor']
        #print count, mon0,mon
        temp=N.concatenate((temp,N.array(mydata.data['temp'])))
        It=N.array(mydata.data['counts'])
        Iterr=N.sqrt(It)
        It=It*mon0/mon
        Iterr=Iterr*mon0/mon
        I=N.concatenate((I,It))
        Ierr=N.concatenate((Ierr,Iterr))
        #print I
        #print Iterr
    #xa,ya,za=prep_data2(Qx,Qy,Counts);
        count=count+1
    return temp,I,Ierr


if __name__=='__main__':
    mydirectory=r'c:\camn2sb2\Jan23_2008'
    myfilebase='p*a*'
    myend='bt9'
    temp,I,Ierr=read_order_files(mydirectory,myfilebase,myend)
    myfilebase2='p*b*'
    tempb,Ib,Ierrb=read_order_files(mydirectory,myfilebase2,myend)
 #   print temp
    #print temp.shape, I.shape, Ierr.shape
    #pylab.errorbar(temp,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None)
    pylab.errorbar(tempb,Ib,Ierrb,marker='s',linestyle='None',mfc='blue',mec='blue',ecolor=None)
    pylab.show()
    