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
        #collimations=[] #in stream order
        self.header['collimations']={}
        self.header['collimations']['coll1']=float(tokenized[0])
        self.header['collimations']['coll2']=float(tokenized[1])
        self.header['collimations']['coll3']=float(tokenized[2])
        self.header['collimations']['coll4']=float(tokenized[3])
        #collimations.append(float(tokenized[1]))
        #collimations.append(float(tokenized[2]))
        #collimations.append(float(tokenized[3]))
        #mosaic=[] #order is monochromator, sample, mosaic
        self.header['mosaic']={}
        self.header['mosaic']['mosaic_monochromator']=float(tokenized[4])
        self.header['mosaic']['mosaic_sample']=float(tokenized[5])
        self.header['mosaic']['mosaic_analyzer']=float(tokenized[6])
        
        self.header['energy_info']={}
        self.header['energy_info']['wavelength']=float(tokenized[7])
        
        self.header['temperature_info']={}
        self.header['temperature_info']['Tstart']=float(tokenized[8])
        self.header['temperature_info']['Tstep']=float(tokenized[9])
        
        self.header['magnetic_field']={}
        self.header['magnetic_field']['Hfield']=float(tokenized[10])
        #print tokenized
        #skip field names of experiment info
        lineStr=myfile.readline()
        self.readimotors(myfile)
        return


    def readqheader(self,myfile):
        #experiment info
        tokenized=get_tokenized_line(myfile)
##        collimations=[] #in stream order
##        collimations.append(float(tokenized[0]))
##        collimations.append(float(tokenized[1]))
##        collimations.append(float(tokenized[2]))
##        collimations.append(float(tokenized[3]))
##        self.header['collimations']=collimations
##        mosaic=[] #order is monochromator, sample, mosaic
##        mosaic.append(float(tokenized[4]))
##        mosaic.append(float(tokenized[5]))
##        mosaic.append(float(tokenized[6]))
##        self.header['mosaic']=mosaic

        
        self.header['collimations']={}
        self.header['collimations']['coll1']=float(tokenized[0])
        self.header['collimations']['coll2']=float(tokenized[1])
        self.header['collimations']['coll3']=float(tokenized[2])
        self.header['collimations']['coll4']=float(tokenized[3])
        
        self.header['mosaic']={}
        self.header['mosaic']['mosaic_monochromator']=float(tokenized[4])
        self.header['mosaic']['mosaic_sample']=float(tokenized[5])
        self.header['mosaic']['mosaic_analyzer']=float(tokenized[6])

        
        self.header['orient1']={}
        self.header['orient1']['h']=float(tokenized[7])
        self.header['orient1']['k']=float(tokenized[8])
        self.header['orient1']['l']=float(tokenized[9])
        #ignore "angle" field
        self.header['orient2']={}
        self.header['orient2']['h']=float(tokenized[11])
        self.header['orient2']['k']=float(tokenized[12])
        self.header['orient2']['l']=float(tokenized[13])
        
##        orient1.append(float(tokenized[7]))
##        orient1.append(float(tokenized[8]))
##        orient1.append(float(tokenized[9]))
##        self.header['orient1']=orient1
##        #ignore the "angle" field
##        orient2=[]
##        orient2.append(float(tokenized[11]))
##        orient2.append(float(tokenized[12]))
##        orient2.append(float(tokenized[13]))
##        self.header['orient2']=orient2
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
        self.header['energy_info']={}
        self.header['q_center']={}
        self.header['q_step']={}
        self.header['q_center']['e_center']=float(tokenized[0])
        self.header['q_step']['delta_e']=float(tokenized[1])
        self.header['energy_info']['ef']=float(tokenized[2])
        self.header['dspacing']={}
        self.header['dspacing']['monochromator_dspacing']=float(tokenized[3])
        self.header['dspacing']['analyzer_dspacing']=float(tokenized[4])
        self.header['temperature_info']={}
        self.header['temperature_info']['Tstart']=float(tokenized[5])
        self.header['temperature_info']['Tstep']=float(tokenized[6])
        tokenized=get_tokenized_line(myfile)
        self.header['energy_info']['Efixed']=tokenized[4]
        tokenized=get_tokenized_line(myfile)
        #qcenter=[]
        #qstep=[]
        self.header['q_center']['h_center']=float(tokenized[0])
        self.header['q_center']['k_center']=float(tokenized[1])
        self.header['q_center']['l_center']=float(tokenized[2])
        self.header['q_step']['delta_h']=float(tokenized[3])
        self.header['q_step']['delta_k']=float(tokenized[4])
        self.header['q_step']['delta_l']=float(tokenized[5])
        self.header['magnetic_field']={}
        self.header['magnetic_field']['Hfield']=float(tokenized[6])
        #skip line describing fields
        linestr=myfile.readline()
        return

    def readbheader(self,myfile):
        self.readqheader(myfile)
        self.readimotors(myfile)
        return



    def get_columnheaders(self,myfile):
    #get first line
        tokenized=get_tokenized_line(myfile)
        self.columndict={}
        #self.columndict['columnlist']=[]
        self.columnlist=[]
        for i in N.arange(len(tokenized)):
            field=tokenized[i]
            if field=='Q(x)':
                field='Qx'
            if field=='Q(y)':
                field='Qy'
            if field=='Q(z)':
                field='Qz'
            if field=='T-act':
                field='Temp'
            self.columndict[field]=[]
            #self.columndict['columnlist'].append(field)
            self.columnlist.append(field)
        return 

    def determinefiletype(self,myfile):
    #get first line
        tokenized=get_tokenized_line(myfile)
        #self.header={'filetype':tokenized[5].strip("'")}
        self.header={}
        self.header['count_info']={}
        self.header['count_info']['monitor_base']=float(tokenized[6])
        self.header['count_info']['monitor_prefactor']=float(tokenized[7])
        self.header['count_info']['monitor']=self.header['count_info']['monitor_base']*self.header['count_info']['monitor_prefactor']
        self.header['count_info']['count_type']=tokenized[8].strip("'")
                
        self.header['file_info']={}
        self.header['file_info']['filename']=tokenized[0].strip("'")
        self.header['file_info']['filebase']=self.header['file_info']['filename'][0:5]
        self.header['file_info']['scantype']=tokenized[5].strip("'")
        self.header['file_info']['instrument']=self.header['file_info']['filename'].split('.')[1]
        
        self.header['timestamp']={}
        self.header['timestamp']['month']=tokenized[1].strip("\'")
        self.header['timestamp']['day']=tokenized[2].strip("\'")
        self.header['timestamp']['year']=tokenized[3].strip("\'")
        self.header['timestamp']['time']=tokenized[4].strip("\'")
        
        #I put this away for now, because it is not reliable about the actual number of points in the file, just the desired number
        #self.header['npts']=int(tokenized[9])
        
        
        
        #skip over names of fields 
        lineStr=myfile.readline()
        #comment and filename
        self.header['file_info']['comment']=myfile.readline().rstrip()
        return self.header['file_info']['scantype']

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
                    field=self.columnlist[i]
                    self.columndict[field].append(float(tokenized[i]))


    def readbuffer(self,myfilestr):
        self.myfilestr=myfilestr
        myfile = open(myfilestr, 'r')
        # Determine FileType
        self.determinefiletype(myfile)
        if self.header['file_info']['scantype']=='I':
            print "calling readibuffer"
            self.readiheader(myfile)
        if self.header['file_info']['scantype']=='B':
            print "calling readbbuffer"
            self.readbheader(myfile)
        if self.header['file_info']['scantype']=='Q':
            print "calling readqbuffer"
            self.readqheader(myfile)
        
        #read columns
        self.readcolumns(myfile)
        myfile.close()
        mydata=Data(self.header,self.columndict)
        print self.header
        print self.columnlist        
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
    #def get_data_fields(self):
    #    return self.data['columnlist']
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
    
    #count_type=property(get_count_type)
    #filetype=property(get_filetype)
    #npts=property(get_npts)
    motor1=property(get_motor1)
    motor2=property(get_motor2)
    motor3=property(get_motor3)
    motor4=property(get_motor4)
    motor5=property(get_motor5)
    motor6=property(get_motor6)    
    #data_fields=property(get_data_fields)
    #monitor=property(get_monitor)
    
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

    if 1:
        #ibuff
        myfilestr=r'c:\summerschool2007\\qCdCr014.ng5'
    if 0:
        #bragg
        myfilestr=r'c:\sqltest\\nuc10014.bt9'
    if 0:
        #qbuff
        myfilestr=r'c:\sqltest\\mnl1p004.ng5'

    mydirectory=r'c:\summerschool2007\\' 
    myfilenumbers=range(4,33,1)
    myend='.ng5'
    myfilehead='qCdCr'
    data=DataCollection()
    mydatareader=datareader()
    mydata=mydatareader.readbuffer(myfilestr)
#    print mydata.npts
#    print mydata.monitor
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




