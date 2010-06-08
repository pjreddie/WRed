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
import os
pi=N.pi



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

    #flist=flist[0:12]
    datalist=[]
    for currfile in flist:
        #print 'MAIN READ',currfile
        mydata=mydatareader.readbuffer(currfile)
        mydata.data['counts_err']=N.sqrt(mydata.data['counts'])*mon0/mydata.metadata['count_info']['monitor']
        mydata.data['counts']=N.array(mydata.data['counts'])*mon0/mydata.metadata['count_info']['monitor']
        datalist.append(mydata)
    
    #print qtree.qlist
    return datalist

if __name__=='__main__':
    #myfilestr=r'C:\Ce2RhIn8\Mar10_2009\magsc035.bt9'
    #myfilestr=r'c:\bifeo3xtal\jan8_2008\9175\fpx53418.bt7'
    #myfilestr=r'c:\13165\13165\data\MagHigh56784.bt7'
    #myfilestr=r'c:\13176\data\CeOFeAs57255.bt7.out'
    #mydatareader=readncnr.datareader()
    #mydata=mydatareader.readbuffer(myfilestr)
    #print mydata.data.keys()
    myfilebase='srfea0'
    myend='bt9'
    mydirectory=r'C:\srfeas\SrFeAsNi\Ni0p00'
    flist=[]
    for i in range(14,23):
        myfilebaseglob=myfilebase+str(i)+'.'+myend
        myfilestr=os.path.join(mydirectory,myfilebaseglob)
        flist.append(myfilestr)
    print flist
    mydatareader=readncnr.datareader()
    mydata=mydatareader.readbuffer(myfilestr)
    print mydata.data.keys()
    print int(mydata.metadata['file_info']['fileseq_number'])
    #print myfilebaseglob
    #flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    datalist=readfiles(flist)
