import numpy as N
import  pylab

def get_tokenized_line(myfile):
        lineStr=myfile.readline()
        strippedLine=lineStr.rstrip()
        tokenized=strippedLine.split()
        return tokenized


class datareader:
    def __init__(self,myfilestr=None):
        self.myfilestr=myfilestr
        
    def readimotors(self,myfile):
    #motor1
        tokenized=get_tokenized_line(myfile)
    #    print tokenized
        motor1={'start':float(tokenized[1])}
        motor1['step']=float(tokenized[2])
        motor1['end']=float(tokenized[3])
        self.header['motor1']=motor1

    #motor2
        tokenized=get_tokenized_line(myfile)
    #    print tokenized
        motor2={'start':float(tokenized[1])}
        motor2['step']=float(tokenized[2])
        motor2['end']=float(tokenized[3])
        self.header['motor2']=motor2
        
    #motor3
        tokenized=get_tokenized_line(myfile)
    #    print tokenized
        motor3={'start':float(tokenized[1])}
        motor3['step']=float(tokenized[2])
        motor3['end']=float(tokenized[3])
        self.header['motor3']=motor3

    #motor4
        tokenized=get_tokenized_line(myfile)
    #    print tokenized
        motor4={'start':float(tokenized[1])}
        motor4['step']=float(tokenized[2])
        motor4['end']=float(tokenized[3])
        self.header['motor4']=motor4

    #motor5
        tokenized=get_tokenized_line(myfile)
    #    print tokenized
        motor5={'start':float(tokenized[1])}
        motor5['step']=float(tokenized[2])
        motor5['end']=float(tokenized[3])
        self.header['motor5']=motor5

    #motor6
        tokenized=get_tokenized_line(myfile)
    #    print tokenized
        motor6={'start':float(tokenized[1])}
        motor6['step']=float(tokenized[2])
        motor6['end']=float(tokenized[3])
        self.header['motor6']=motor6
        #skip line describing Motor Start Step End
        lineStr = myfile.readline()
        return
    
    def readiheader(self,myfile):
    #experiment info
        tokenized=get_tokenized_line(myfile)
        print "tokenized"
        print tokenized
        collimations=[] #in stream order
        collimations.append(float(tokenized[0]))
        collimations.append(float(tokenized[1]))
        collimations.append(float(tokenized[2]))
        collimations.append(float(tokenized[3]))
        self.header['collimations']=collimations
        mosaic=[] #order is monochromator, sample, mosaic
        mosaic.append(float(tokenized[4]))
        mosaic.append(float(tokenized[5]))
        mosaic.append(float(tokenized[6]))
        self.header['mosaic']=mosaic
        self.header['wavelength']=float(tokenized[7])
        self.header['Tstart']=float(tokenized[8])
        self.header['Tstep']=float(tokenized[9])
        self.header['Hfield']=float(tokenized[10])
        #print tokenized
        #skip field names of experiment info
        lineStr=myfile.readline()
        self.readimotors()
        return


    def readqheader(self,myfile):
    #experiment info
        print "qheader"
        tokenized=get_tokenized_line(myfile)
        collimations=[] #in stream order
        collimations.append(float(tokenized[0]))
        collimations.append(float(tokenized[1]))
        collimations.append(float(tokenized[2]))
        collimations.append(float(tokenized[3]))
        self.header['collimations']=collimations
        mosaic=[] #order is monochromator, sample, mosaic
        mosaic.append(float(tokenized[4]))
        mosaic.append(float(tokenized[5]))
        mosaic.append(float(tokenized[6]))
        self.header['mosaic']=mosaic
        orient1=[]
        orient1.append(float(tokenized[7]))
        orient1.append(float(tokenized[8]))
        orient1.append(float(tokenized[9]))
        self.header['orient1']=orient1
        #ignore the "angle" field
        orient2=[]
        orient2.append(float(tokenized[11]))
        orient2.append(float(tokenized[12]))
        orient2.append(float(tokenized[13]))
        self.header['orient2']=orient2
        #skip line with field names
        myfile.readline()
        tokenized=get_tokenized_line(myfile)
        lattice={}
        lattice['a']=float(tokenized[0])
        lattice['b']=float(tokenized[1])
        lattice['c']=float(tokenized[2])
        lattice['alpha']=float(tokenized[3])
        lattice['beta']=float(tokenized[4])
        lattice['gamma']=float(tokenized[5])
        self.header['lattice']=lattice
        #skip line with field names
        myfile.readline()
        tokenized=get_tokenized_line(myfile)
        self.header['ecenter']=float(tokenized[0])
        self.header['deltae']=float(tokenized[1])
        self.header['ef']=float(tokenized[2])
        self.header['monochromator_dspacing']=float(tokenized[3])
        self.header['analyzer_dspacing']=float(tokenized[4])
        self.header['tstart']=float(tokenized[5])
        self.header['tstep']=float(tokenized[6])
        tokenized=get_tokenized_line(myfile)
        self.header['Efixed']=tokenized[4]
        tokenized=get_tokenized_line(myfile)
        qcenter=[]
        qstep=[]
        qcenter.append(float(tokenized[0]))
        qcenter.append(float(tokenized[1]))
        qcenter.append(float(tokenized[2]))
        qstep.append(float(tokenized[3]))
        qstep.append(float(tokenized[4]))
        qstep.append(float(tokenized[5]))
        self.header['qcenter']=qcenter
        self.header['qstep']=qstep
        self.header['hfield']=float(tokenized[6])
        #skip line describing fields
        linestr=myfile.readline()
        print linestr
        print "done"
        return

    def readbheader(self,myfile):
        self.readqheader(myfile)
        self.readimotors(myfile)
        return



    def get_columnheaders(self,myfile):
    #get first line
        tokenized=get_tokenized_line(myfile)
        self.columndict={}
        self.columndict['columnlist']=[]
        for i in N.arange(len(tokenized)):
            self.columndict[tokenized[i]]=[]
            self.columndict['columnlist'].append(tokenized[i])
#        print self.columndict['columnlist']
        return 

    def determinefiletype(self,myfile):
    #get first line
        tokenized=get_tokenized_line(myfile)
        #self.header={'filetype':tokenized[5].strip("'")}
        self.header={}
        self.header['monitor_base']=float(tokenized[6])
        self.header['monitor_prefactor']=float(tokenized[7])
        self.header['monitor']=self.header['monitor_base']*self.header['monitor_prefactor']
        self.header['count_type']=tokenized[8].strip("'")
        self.header['npts']=float(tokenized[9])
        self.header['filename']=tokenized[0].strip("'")
        self.header['scantype']=tokenized[5].strip("'")
        timestamp={}
        timestamp['month']=tokenized[1].strip("\'")
        timestamp['day']=tokenized[2].strip("\'")
        timestamp['year']=tokenized[3].strip("\'")
        timestamp['time']=tokenized[4].strip("\'")
        self.header['timestamp']=timestamp
        #skip over names of fields 
        lineStr=myfile.readline()
        #comment and filename
        self.header['comment']=myfile.readline().rstrip()
        return self.header['scantype']

    def readcolumns(self,myfile):
        self.get_columnheaders(myfile)
        # get the names of the fields
    #   prepare to read the data    
        count =  0
        while 1:
            lineStr = myfile.readline()
            if not(lineStr):
                break
            if lineStr[0] != "#":
                count=count+1
                strippedLine=lineStr.rstrip()
                tokenized=strippedLine.split()
                for i in range(len(tokenized)):
                    field=self.columndict['columnlist'][i]
                    self.columndict[field].append(float(tokenized[i]))


    def readbuffer(self,myfilestr):
        self.myfilestr=myfilestr
        myfile = open(myfilestr, 'r')
        # Determine FileType
        self.determinefiletype(myfile)
        print self.header['scantype']
        if self.header['scantype']=='I':
            print "calling readibuffer"
            self.readiheader(myfile)
        if self.header['scantype']=='B':
            print "calling readbbuffer"
            self.readbheader(myfile)
        if self.header['scantype']=='Q':
            print "calling readqbuffer"
            self.readqheader(myfile)
        
        #read columns
        self.readcolumns(myfile)
        myfile.close()
        mydata=Data(self.header,self.columndict)
        print self.header
        print self.columndict['columnlist']        
        return mydata


class Data:
    def __init__(self,header,data):
        self.header=header
        self.data=data
        
    
    def get_monitor(self):
        return self.header['monitor']
    #@property
    #def monitor(self):
    #    "The monitor rate"
    #    def fget(self):
    #        return self.header['monitor']
    ##def get_filetype(self):
    ##    return self.header['filetype']
    def get_npts(self):
        return self.header['npts']
    def get_count_type(self):
        return self.header['count_type']
    def get_data_fields(self):
        return self.data['columnlist']
    def get_motor1(self):
        return self.header['motor1']
    def get_motor2(self):
        return self.header['motor2']
    def get_motor3(self):
        return self.header['motor3']
    def get_motor4(self):
        return self.header['motor4']
    def get_motor5(self):
        return self.header['motor5']
    def get_motor6(self):
        return self.header['motor6']
    def get_field(self,field):
        return self.data[field]
    def gen_motor1_arr(self):
        motor=self.get_motor1()
        step=motor['step']
        start=motor['start']
        if step==0.0:
            res=start*N.ones((1,self.npts),'d')
        else:
            res=N.arange(start,motor['end'],step)
        return res
    def gen_motor2_arr(self):
        motor=self.get_motor2()
        step=motor['step']
        start=motor['start']
        if step==0.0:
            res=start*N.ones((1,self.npts),'d')
        else:
            res=N.arange(start,motor['end'],step)
        return res
    def gen_motor3_arr(self):
        motor=self.get_motor3()
        step=motor['step']
        start=motor['start']
        if step==0.0:
            res=start*N.ones((1,self.npts),'d')
        else:
            res=N.arange(start,motor['end'],step)
        return res
    def gen_motor4_arr(self):
        motor=self.get_motor4()
        step=motor['step']
        start=motor['start']
        if step==0.0:
            res=start*N.ones((1,self.npts),'d')
        else:
            res=N.arange(start,motor['end'],step)
        return res
    def gen_motor5_arr(self):
        motor=self.get_motor5()
        step=motor['step']
        start=motor['start']
        if step==0.0:
            res=start*N.ones((1,self.npts),'d')
        else:
            res=N.arange(start,motor['end'],step)
        return res        
    def gen_motor6_arr(self):
        motor=self.get_motor6()
        step=motor['step']
        start=motor['start']
        if step==0.0:
            res=start*N.ones((1,self.npts),'d')
        else:
            res=N.arange(start,motor['end'],step)
        return res
    

#   self.columndict[field]
    
    count_type=property(get_count_type)
    #filetype=property(get_filetype)
    npts=property(get_npts)
    motor1=property(get_motor1)
    motor2=property(get_motor2)
    motor3=property(get_motor3)
    motor4=property(get_motor4)
    motor5=property(get_motor5)
    motor6=property(get_motor6)    
    data_fields=property(get_data_fields)
    monitor=property(get_monitor)
    
class DataCollection:
    def __init__(self):
        self.data=[]
    def get_data(self):
        return self.data
    def add_datum(self,datum):
        self.data.append(datum)
        return
    def extract_a4(self):
        a4=[]
        for i in range(len(self.data)):
            motor4=self.data[i].get_motor4()
            a4.append(motor4['start'])
        return N.array(a4,'d')
    def extract_a3a4(self):
        a4=[]
        a3=[]
        counts=[]
        for i in range(len(self.data)):
            motor4=self.data[i].get_motor4()
            a4.append(self.data[i].gen_motor4_arr())
            a3.append(self.data[i].get_field('A3'))
            counts.append(self.data[i].get_field('COUNTS'))
        return N.ravel(N.array(a3,'d')),N.ravel(N.array(a4,'d')),N.ravel(N.array(counts,'d'))
    
    data=property(get_data,add_datum)

def num2string(num):
    numstr=None
    if num<10:
        numstr='00'+str(num)
    elif (num>=10 & num <100):
        numstr='0'+str(num)
    elif (num>100):
        numstr=str(num)
    return numstr

if __name__=='__main__':

    if 0:
        #ibuff
        myfilestr=r'c:\summerschool2007\\qCdCr014.ng5'
        mydirectory=r'c:\summerschool2007\\' 
        myfilenumbers=range(4,33,1)
        myend='.ng5'
        myfilehead='qCdCr'
    if 1:
        #bragg
        myfilestr=r'c:\sqltest\\nuc10014.bt9'
    if 0:
        #qbuff
        myfilestr=r'c:\sqltest\\mnl1p004.ng5'
    data=DataCollection()
    mydatareader=datareader()
    mydata=mydatareader.readbuffer(myfilestr)
    print mydata.npts
    print mydata.monitor
#    print mydata.gen_motor6_arr()
#    print mydata.gen_motor5_arr()
#    print mydata.gen_motor4_arr()
#    print mydata.gen_motor3_arr()
#    print mydata.gen_motor2_arr()
#    print mydata.gen_motor1_arr()
    if 0:
        for i in range(len(myfilenumbers)):
            myfilenum=num2string(myfilenumbers[i])
            myfilestr=mydirectory+myfilehead+myfilenum+myend
            print myfilestr
            data.add_datum(mydatareader.readibuffer(myfilestr))
        a3,a4,counts=data.extract_a3a4()
        print a3.shape
        print a4.shape
        print counts.shape




