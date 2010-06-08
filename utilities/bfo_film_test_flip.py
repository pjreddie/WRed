import matplotlib
import matplotlib.pyplot as plt
import numpy as N
import readncnr3 as readncnr
import os,sys
from matplotlib.ticker import NullFormatter, MultipleLocator,MaxNLocator


def read_data(myfilestr):
    mydatareader=readncnr.datareader()
    mydata=mydatareader.readbuffer(myfilestr)
    #qz=N.array(mydata.data['qx'])
    qz=N.array(mydata.data['qx'])
    I=N.array(mydata.data['detector'],'float64')
    Ierr=N.sqrt(I)
    mon=mydata.data['monitor'][0]
    return qz,I,Ierr,mon
  
def read_fpx(myfilestr,key='smplgfrot'):
    mydatareader=readncnr.datareader()
    mydata=mydatareader.readbuffer(myfilestr)
    qz=N.array(mydata.data[key])
    I=N.array(mydata.data['detector'],'float64')
    Ierr=N.sqrt(I)
    mon=mydata.data['monitor'][0]
    return qz,I,Ierr,mon


def film110():
    mydirectory=r'C:\BiFeO3film\bt7\15154\data'
    fig=plt.figure()
    
    #horizontal
    myfilestr=os.path.join(mydirectory,'flipperoffvuline_horizonal78500.bt7')
    qz,I,Ierr,mon0=read_data(myfilestr)
    ax=fig.add_subplot(1,3,1)
    ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
    
    myfilestr=os.path.join(mydirectory,'flipperonvuline_horizonal78499.bt7')
    qz,I,Ierr,mon=read_data(myfilestr)
    Ierr=Ierr*mon0/mon
    I=I*mon0/mon
    ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
    #ax.set_title('horizontal')
    ax.legend(numpoints=1)
    plt.xlabel('L')
    plt.ylabel('Intensity (arb. units)')
    ax.xaxis.set_major_locator(MaxNLocator(4))
    
    #vertical
    ax=fig.add_subplot(1,3,2)
    myfilestr=os.path.join(mydirectory,'flipperoffvuline_vertical78502.bt7')
    qz,I,Ierr,mon=read_data(myfilestr)
    Ierr=Ierr*mon0/mon
    I=I*mon0/mon
    ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
    
    myfilestr=os.path.join(mydirectory,'flipperonvuline_vertical78501.bt7')
    qz,I,Ierr,mon=read_data(myfilestr)
    Ierr=Ierr*mon0/mon
    I=I*mon0/mon
    ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
    #ax.set_title('vertical')
    ax.legend(numpoints=1)
    ax.xaxis.set_major_locator(MaxNLocator(4))
    plt.xlabel('L')
    #plt.ylabel('Intensity (arb. units)')
    
    
    
    
    #smplgfield rot
    
    if 1:
        #fig2=plt.figure()
        
        #Magnetic
        
        
        #ax=fig2.add_subplot(2,2,1)
        myfilestr=os.path.join(mydirectory,'fpx78503.bt7')
        qz,I,Ierr,mon0=read_fpx(myfilestr)
        #Ierr=Ierr*mon0/mon
        #I=I*mon0/mon
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
           
        myfilestr=os.path.join(mydirectory,'fpx78505.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.set_title('Magnetic')
        #ax.legend()
        #plt.xlabel(r'$ \theta$')
        #plt.ylabel('Intensity (arb. units)')
        
        
        
        
        #Nuclear
        #ax=fig2.add_subplot(2,2,2)
        
        myfilestr=os.path.join(mydirectory,'fpx78510.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        Inuc_sf=I
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
        #ax.set_title('Nuclear')
        #plt.xlabel(r'$ \theta $')
        #plt.ylabel('Intensity (arb. units)')
        
        myfilestr=os.path.join(mydirectory,'fpx78511.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        Inuc_nsf=I
        frnuc=Inuc_nsf/Inuc_sf
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.legend()
        #plt.xlabel(r'$ \theta $')
        #plt.ylabel('Intensity (arb. units)')
    
    
    #Corrected
    
    
    ax=fig.add_subplot(1,3,3)
    myfilestr=os.path.join(mydirectory,'fpx78503.bt7')
    qz,I,Ierr,mon=read_fpx(myfilestr)
    Ierr=Ierr*mon0/mon*frnuc
    I=I*mon0/mon*frnuc
    ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
       
    myfilestr=os.path.join(mydirectory,'fpx78505.bt7')
    qz,I,Ierr,mon=read_fpx(myfilestr)
    Ierr=Ierr*mon0/mon*frnuc
    I=I*mon0/mon*frnuc
    ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
    #ax.set_title('Corrected')
    ax.legend(numpoints=1)
    plt.xlabel(r'$ \theta $')
    ax.xaxis.set_major_locator(MaxNLocator(4))
    #plt.ylabel('Intensity (arb. units)')
    
    #fig3.subplots_adjust(hspace=0.3)
    
    
    
    
    plt.show()

    
    
def film111():
    mydirectory=r'C:\BiFeO3film\bt7\15154\data'
    
    
    if 1:
        fig5=plt.figure()
        
        #horizontal
        myfilestr=os.path.join(mydirectory,'hh0_sf_vu78635.bt7')
        qz,I,Ierr,mon0=read_data(myfilestr)
        ax=fig5.add_subplot(1,3,1)
        ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
        
        myfilestr=os.path.join(mydirectory,'hh0_nsf_vu78634.bt7')
        qz,I,Ierr,mon=read_data(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.set_title('horizontal')
        ax.legend(numpoints=1)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        plt.xlabel('L')
        plt.ylabel('Intensity (arb. units)')
        
        #vertical
        ax=fig5.add_subplot(1,3,2)
        #myfilestr=os.path.join(mydirectory,'hh0_sf_vu78632.bt7') # long time
        myfilestr=os.path.join(mydirectory,'hh0_sf_vu78631.bt7') # more points
        qz,I,Ierr,mon=read_data(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
        
        myfilestr=os.path.join(mydirectory,'hh0_nsf_vu78633.bt7')
        qz,I,Ierr,mon=read_data(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.set_title('vertical')
        ax.legend(numpoints=1)
        ax.xaxis.set_major_locator(MaxNLocator(4))
        plt.xlabel('L')
        #plt.ylabel('Intensity (arb. units)')
    
    
    
    
    #smplgfield rot
    
    if 1:
        #fig6=plt.figure()
        fig6=fig5
        #Magnetic
        
        
        #ax=fig6.add_subplot(2,2,1)
        myfilestr=os.path.join(mydirectory,'fpx78623.bt7')
        qz,I,Ierr,mon0=read_fpx(myfilestr)
        #Ierr=Ierr*mon0/mon
        #I=I*mon0/mon
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
           
        myfilestr=os.path.join(mydirectory,'fpx78624.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.set_title('Magnetic')
        #ax.legend(numpoints=1)
        #ax.xaxis.set_major_locator(MaxNLocator(4))
        #plt.xlabel(r'$ \theta$')
        #plt.xlim(95,140)
        #plt.ylabel('Intensity (arb. units)')
        
        
        
        
        #Nuclear
        #ax=fig6.add_subplot(2,2,2)
        
        myfilestr=os.path.join(mydirectory,'fpx78625.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        Inuc_sf=I
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
        #ax.set_title('Nuclear')
        #plt.xlabel(r'$ \theta $')
        #plt.ylabel('Intensity (arb. units)')
        
        myfilestr=os.path.join(mydirectory,'fpx78626.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        Inuc_nsf=I
        frnuc=Inuc_nsf/Inuc_sf
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.legend(numpoints=1)
        #plt.xlim(95,140)
        #plt.xlabel(r'$ \theta $')
        
        #plt.ylabel('Intensity (arb. units)')
        
        
        #Corrected
        
        
        ax=fig6.add_subplot(1,3,3)
        myfilestr=os.path.join(mydirectory,'fpx78623.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon*frnuc
        I=I*mon0/mon*frnuc
        ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
           
        myfilestr=os.path.join(mydirectory,'fpx78624.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon*frnuc
        I=I*mon0/mon*frnuc
        ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.set_title('Corrected')
        ax.legend(numpoints=1)
        plt.xlabel(r'$ \theta $')
        #plt.ylabel('Intensity (arb. units)')
        #ax.set_yscale('log')
        ax.xaxis.set_major_locator(MaxNLocator(4))
        plt.xlim(95,140)
        
        #fig6.subplots_adjust(hspace=0.3)
    
    
    
    
    plt.show()


    
    
def film110_1p5():
    mydirectory=r'C:\BiFeO3film\bt7\15537\data'
    fig=plt.figure()
    
    if 0:
        #horizontal
        myfilestr=os.path.join(mydirectory,'gfield80566.bt7')
        qz,I,Ierr,mon0=read_data(myfilestr)
        ax=fig.add_subplot(1,3,1)
        ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
        
        myfilestr=os.path.join(mydirectory,'gfield80567.bt7')
        qz,I,Ierr,mon=read_data(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.set_title('horizontal')
        ax.legend(numpoints=1)
        plt.xlabel('L')
        plt.ylabel('Intensity (arb. units)')
        ax.xaxis.set_major_locator(MaxNLocator(4))
    

    
    #smplgfield rot
    
    if 1:
        #fig2=plt.figure()
        
        #Magnetic
        
        
        #ax=fig2.add_subplot(2,2,1)
        myfilestr=os.path.join(mydirectory,'gfield80566.bt7')
        qz,I,Ierr,mon0=read_fpx(myfilestr)
        #Ierr=Ierr*mon0/mon
        #I=I*mon0/mon
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
           
        myfilestr=os.path.join(mydirectory,'gfield80567.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.set_title('Magnetic')
        #ax.legend()
        #plt.xlabel(r'$ \theta$')
        #plt.ylabel('Intensity (arb. units)')
        
        
        
        
        #Nuclear
        #ax=fig2.add_subplot(2,2,2)
        
        myfilestr=os.path.join(mydirectory,'gfield80568.bt7')
        qz,I,Ierr,mon=read_fpx(myfilestr)
        Ierr=Ierr*mon0/mon
        I=I*mon0/mon
        Inuc_sf=I
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
        #ax.set_title('Nuclear')
        #plt.xlabel(r'$ \theta $')
        #plt.ylabel('Intensity (arb. units)')
        if 1:
            myfilestr=os.path.join(mydirectory,'gfield80569.bt7')
            qz,I,Ierr,mon=read_fpx(myfilestr)
            Ierr=Ierr*mon0/mon
            I=I*mon0/mon
            Inuc_nsf=I
            frnuc=Inuc_nsf/Inuc_sf
        frnuc=Inuc_nsf
        #ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
        #ax.legend()
        #plt.xlabel(r'$ \theta $')
        #plt.ylabel('Intensity (arb. units)')
    
    
    #Corrected
    
    
    ax=fig.add_subplot(1,1,1)
    myfilestr=os.path.join(mydirectory,'gfield80566.bt7')
    qz,I,Ierr,mon=read_fpx(myfilestr)
    Ierr=Ierr*mon0/mon*frnuc
    I=I*mon0/mon*frnuc
    ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='red',mec='red',ecolor=None,label='sf')
       
    myfilestr=os.path.join(mydirectory,'gfield80567.bt7')
    qz,I,Ierr,mon=read_fpx(myfilestr)
    Ierr=Ierr*mon0/mon*frnuc
    I=I*mon0/mon*frnuc
    ax.errorbar(qz,I,Ierr,marker='s',linestyle='None',mfc='black',mec='black',ecolor=None,label='nsf')
    #ax.set_title('Corrected')
    ax.legend(numpoints=1)
    plt.xlabel(r'$ \theta $')
    ax.xaxis.set_major_locator(MaxNLocator(4))
    #plt.ylabel('Intensity (arb. units)')
    
    #fig3.subplots_adjust(hspace=0.3)
    
    
    
    
    plt.show()
    
    
    


if __name__=="__main__":
    myfilestr=r'c:\bifeo3xtal\jan8_2008\9175\mesh53439.bt7'
    if 0:
        film110()
    if 0:
        film111()
    if 1:
        film110_1p5()
    #myfilestr=r'c:\bifeo3xtal\jan8_2008\9175\fpx53418.bt7'
    #myfilestr=r'c:\13165\13165\data\MagHigh56784.bt7'
    #myfilestr=r'c:\13176\data\CeOFeAs57255.bt7.out'
    #mydatareader=datareader()
    #mydata=mydatareader.readbuffer(myfilestr,lines=91)
    #mydata=mydatareader.readbuffer(myfilestr)
    
    
    



