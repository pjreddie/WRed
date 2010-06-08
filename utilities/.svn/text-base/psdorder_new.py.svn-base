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

class psd:
    def __init__(self,left=0,center=21,right=48):
        self.left=left
        self.right=right
        self.center=center
        return


if __name__=='__main__':
        mydirectory=r'C:\13165\13165\data'
        myfilebase='PSD_A4_SpacingApr1108.dat'
        myend='bt7'
        flist=[]
        rlist=[56421,56420,56419]
        myfilestr=r'C:\13165\PSD_A4_SpacingApr1108.dat'
        ch_a4=N.loadtxt(myfilestr, unpack=True)
        ch_a4=ch_a4.T.flatten()
        myfilestr=r'C:\13165\PSD_Channel_April1208.dat'
        ch_eff=N.loadtxt(myfilestr, unpack=True)
        ch_eff=ch_eff.T.flatten()
        #ch_space+0.5*(-ch_space+shift(ch_space,1))+var(var_pos,i)

        mypsd=psd()
        #print (ch_a4-ch_a4[mypsd.center])
        ch_boundary=(ch_a4-ch_a4[mypsd.center])+0.5*N.concatenate((N.array([0]),N.diff(ch_a4)))
        ch_boundary[0]=(ch_a4[0]-ch_a4[mypsd.center])-0.5*(ch_a4[1]-ch_a4[0])
        print ch_boundary

        pylab.plot(N.arange(ch_eff.size),ch_eff,'ro')
        pylab.show()