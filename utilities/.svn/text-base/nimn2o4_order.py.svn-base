import numpy as N
import  pylab
#import scipy.sandbox.delaunay as D
#import numpy.core.ma as ma
#import matplotlib.numerix.ma as ma
#from matplotlib.ticker import NullFormatter, MultipleLocator
#from scipy.signal.signaltools import convolve2d
import scriptutil as SU
import re
import readncnr3 as readncnr
#from matplotlib.ticker import FormatStrFormatter
#from matplotlib.ticker import MaxNLocator
#import linegen
#import locator



def readmeshfiles(mydirectory,myfilebase,myend):
    myfilebaseglob=myfilebase+'*.'+myend
    print myfilebaseglob
    flist = SU.ffind(mydirectory, shellglobs=(myfilebaseglob,))
    #SU.printr(flist)
    mydatareader=readncnr.datareader()
    temp1=N.array([])
    temp2=N.array([])
    temp3=N.array([])
    Counts1=N.array([])
    Counts2=N.array([])
    Counts3=N.array([])
    errors1=N.array([])
    errors2=N.array([])
    errors3=N.array([])
    mydata=mydatareader.readbuffer(flist[0])
    mon0=mydata.metadata['count_info']['monitor']
    for currfile in flist:
        #print currfile
        mydata=mydatareader.readbuffer(currfile)
        #print mydata.data.keys()
        #print mydata.__dict__
        #print mydata.metadata.keys()
        qcenter=mydata.metadata['q_center']
        hc,kc,lc=qcenter['h_center'],qcenter['k_center'],qcenter['l_center']
        mon=mydata.metadata['count_info']['monitor']
        curr_counts=N.array(mydata.data['counts'])
        curr_error=N.sqrt(curr_counts)*mon0/mon
        curr_counts=curr_counts*mon0/mon
        curr_temp=N.array(mydata.data['temp'])
        if hc==1.004:
            Counts1=N.concatenate((Counts1,curr_counts))
            temp1=N.concatenate((temp1,curr_temp))
            errors1=N.concatenate((errors1,curr_error))
            
        elif hc==1.036:
            Counts2=N.concatenate((Counts2,curr_counts)) 
            temp2=N.concatenate((temp2,curr_temp))      
            errors2=N.concatenate((errors2,curr_error)) 
        elif hc==2.0:
            Counts3=N.concatenate((Counts3,curr_counts))
            temp3=N.concatenate((temp3,curr_temp))
            errors3=N.concatenate((errors3,curr_error))
        #print 
        #Qx=N.concatenate((Qx,N.array(mydata.data['qx'])))
        #Qy=N.concatenate((Qy,N.array(mydata.data['qy'])))
        #Qz=N.concatenate((Qz,N.array(mydata.data['qz'])))
        
        #Counts=N.concatenate((Counts,N.array(mydata.data['counts'])))
    #print Qx
    #print Qy
    #print Counts
    dataset={}
    dataset['Counts1']=Counts1
    dataset['Counts2']=Counts2
    dataset['Counts3']=Counts3
    dataset['temp1']=temp1
    dataset['temp2']=temp2
    dataset['temp3']=temp3
    dataset['errors1']=errors1
    dataset['errors2']=errors2
    dataset['errors3']=errors3
    
    return dataset

if __name__ == '__main__':
    Nu = 10000
    aspect = 1.0
    mydirectory=r'c:\NiMn2O4\Jan16_2009'
    myfilebase='t3*'
    myend='bt9'
    dataset=readmeshfiles(mydirectory,myfilebase,myend)
    if 1:
        ax1=pylab.errorbar(dataset['temp1'],dataset['Counts1'],dataset['errors1'],
                   marker='s',linestyle='None',mfc='black',mec='black',ecolor='black')
    if 1:    
        ax2=pylab.errorbar(dataset['temp3'],dataset['Counts3'],dataset['errors3'],
                   marker='s',linestyle='None',mfc='blue',mec='blue',ecolor='blue')

    ax3=pylab.twinx()
    if 1:
        pylab.errorbar(dataset['temp2'],dataset['Counts2'],dataset['errors2'],
                   marker='s',linestyle='None',mfc='red',mec='red',ecolor='black')
    
    #print ax2
    
    #ax2[0].get_axes().set_yscale('log')
    if 0:
        pylab.savefig(r'c:\nimn2o4_order2.pdf')
    if 1:
        pylab.show()
