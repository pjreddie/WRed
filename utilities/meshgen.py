import numpy as N
import copy

def init_scan():
    scandes={}
    scandes['Title']='MyTitle'
    scandes['SubID']=0
    scandes['JTYPE']='VECTOR'
    scandes['Fixed']=1 #0=monochormator, 1=analyzer
    scandes['FixedE']=14.7
    scandes['Filename']='mesh'
    scandes['Npts']=5
    scandes['Counts']=1.0
    scandes['Prefac']=1.0
    scandes['DetectorType']='detector'
    scandes['CountType']='monitor'
    scandes['HoldScan']=0.0
    scandes['Range']={}
    scandes['Range']['Q']={}
    scandes['Range']['Q']['type']='S' # S denotes using start and stop positions, default is central position, increment]
    scandes['Range']['Q']['initial']=N.array([1.0,0.0,0.0])
    scandes['Range']['Q']['final']=N.array([2.0,0.0,0.0])
#    scandes['Range']['Q']['type']='' # S denotes using start and stop positions, default is central position, increment]
#    scandes['Range']['Q']['center]=N.array([1.0,0.0,0.0])
#    scandes['Range']['Q']['step]=N.array([0.2,0.0,0.0])
    scandes['Range']['E']={}
    scandes['Range']['E']['type']='S'
    scandes['Range']['E']['initial']=N.array([0.0])
    scandes['Range']['E']['final']=N.array([0.0])
    return scandes

class scangen:
        def __init__(self,scandes):
            self.scandes=copy.deepcopy(scandes)
            return
        
        def printarr(self,arr,delimeter='~'):
            outstr=''
            for i in range(arr.shape[0]-1):
               outstr=outstr+str(arr[i])+delimeter 
            outstr=outstr+str(arr[-1])
            return outstr
            
        def output(self):
            scanstr='Scan'
            for key, value in self.scandes.iteritems():
                if key!='Range':
                    scanstr=scanstr+':'+key+'='+str(value)
                else:
                    for rangetype,rangevalue in value.iteritems():
                        scanstr=scanstr+':Range='+rangetype+'='
                        arr=value[rangetype]['initial']
                        delimeter=''
                        if rangetype=='Q':
                            delimeter='~'
                        scanstr=scanstr+self.printarr(arr,delimeter)
                        arr=value[rangetype]['final']
                        scanstr=scanstr+' '
                        scanstr=scanstr+self.printarr(arr,delimeter)
                        scanstr=scanstr+' '
                        scanstr=scanstr+value[rangetype]['type'] 
            scanstr=scanstr+'\n'
            return scanstr
            
    
class meshgen:
    def __init__(self,field1,field2):
        self.field1=copy.deepcopy(field1)
        self.field2=copy.deepcopy(field2)
        self.field2['final']=field2['final'].astype(float)
        self.field2['initial']=field2['initial'].astype(float)
        self.field2['Npts']=int(field2['Npts'])
        return
    def genscans(self):
        scanstr=''
        field1=self.field1
        field2=self.field2
        step=((field2['final']-field2['initial'])/(field2['Npts']-1))[0]
        print step
        curr=field2['initial'][0]
#        for curr in N.arange(field2['initial'][0],field2['final'][0]+step,step):
        for i in range(field2['Npts']):
            scandes=init_scan()
            scandes['Range']['Q']['initial']=field1['initial']['Q'].astype(float)
            scandes['Range']['Q']['final']=field1['final']['Q'].astype(float)
            scandes['Range']['E']['initial']=field1['initial']['E'].astype(float)
            scandes['Range']['E']['final']=field1['final']['E'].astype(float)
            scandes['Npts']=field1['Npts']
            scandes['Range'][field2['type']]['initial'][field2['idx']]=curr
            scandes['Range'][field2['type']]['final'][field2['idx']]=curr
            myscan=scangen(scandes=scandes)   
            scanstr=scanstr+'scan set '+myscan.output()
            scanstr=scanstr+'scan run\n'
            curr=curr+step
            print curr
        return scanstr

if __name__=="__main__":
#
# Scan:Title=Scan1:SubID=0:JTYPE=VECTOR:FIXED=1:FIXEDE=14.7:Filename=blah:Npts=5:Counts=1.0:Prefac=1.0:
#DetectorType=detector:CountType=monitor:HoldScan=0.0:Range=E=0.0 0.0 S:Range=Q=1.0~1.0~1.0 0.5~1.0~1.0 S
    #field 1 is the inner loop, field 2 is the outer loop
    field1={}
    field1['initial']={}
    field1['final']={}
    field1['initial']['Q']=N.array([1,0,0])
    field1['final']['Q']=N.array([2,0,0])
    field1['initial']['E']=N.array([0])
    field1['final']['E']=N.array([0])
    field1['Npts']=11
    field2={}
    field2['idx']=2 #idx [Qx,Qy,Qz] or [E], starts from 0
    field2['type']='Q' # should be 'Q' or 'E'
    field2['initial']=N.array([1])
    field2['final']=N.array([2])
    field2['Npts']=11
    mymesh=meshgen(field1,field2)
    scanstr=mymesh.genscans()
    print scanstr
    f=open('myseq.seq.txt','wt') #mode t to make sure output character is correct for os
    f.write(scanstr)
    f.close()
