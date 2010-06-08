import numpy as N
import  pylab
import scipy.sandbox.delaunay as D
import numpy.core.ma as ma

def plot_nodes(tri):
    for nodes in tri.triangle_nodes:
        D.fill(x[nodes],y[nodes],'b')
    pylab.show()

def plot_data(xi,yi,zi):
    zim = ma.masked_where(N.isnan(zi),zi)
    pylab.figure(figsize=(8,8))
#    pylab.pcolor(xi,yi,zim,shading='interp',cmap=pylab.cm.gray)
    pylab.pcolor(xi,yi,zim,shading='interp',cmap=pylab.cm.jet)
#    pylab.contour(xi,yi,zim,cmap=pylab.cm.jet)
    pylab.show()


class datareader:
    def __init__(self,myfilestr=None):
        self.myfilestr=myfilestr
        
    def readheader(self,myfile):
    #get first line
        lineStr=myfile.readline()
        strippedLine=lineStr.rstrip()
        tokenized=strippedLine.split()
    #    print tokenized
        self.header={'filetype':tokenized[5]}
        self.header['monitor_base']=float(tokenized[6])
        self.header['monitor_prefactor']=float(tokenized[7])
        self.header['monitor']=self.header['monitor_base']*self.header['monitor_prefactor']
        self.header['count_type']=tokenized[8]
        self.header['npts']=float(tokenized[9])
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
        self.header['motor1']=motor1

    #motor2
        lineStr=myfile.readline()
        strippedLine=lineStr.rstrip()
        tokenized=strippedLine.split()
    #    print tokenized
        motor2={'start':float(tokenized[1])}
        motor2['step']=float(tokenized[2])
        motor2['end']=float(tokenized[3])
        self.header['motor2']=motor2
        
    #motor3
        lineStr=myfile.readline()
        strippedLine=lineStr.rstrip()
        tokenized=strippedLine.split()
    #    print tokenized
        motor3={'start':float(tokenized[1])}
        motor3['step']=float(tokenized[2])
        motor3['end']=float(tokenized[3])
        self.header['motor3']=motor3

    #motor4
        lineStr=myfile.readline()
        strippedLine=lineStr.rstrip()
        tokenized=strippedLine.split()
    #    print tokenized
        motor4={'start':float(tokenized[1])}
        motor4['step']=float(tokenized[2])
        motor4['end']=float(tokenized[3])
        self.header['motor4']=motor4

    #motor5
        lineStr=myfile.readline()
        strippedLine=lineStr.rstrip()
        tokenized=strippedLine.split()
    #    print tokenized
        motor5={'start':float(tokenized[1])}
        motor5['step']=float(tokenized[2])
        motor5['end']=float(tokenized[3])
        self.header['motor5']=motor5

    #motor6
        lineStr=myfile.readline()
        strippedLine=lineStr.rstrip()
        tokenized=strippedLine.split()
    #    print tokenized
        motor6={'start':float(tokenized[1])}
        motor6['step']=float(tokenized[2])
        motor6['end']=float(tokenized[3])
        self.header['motor6']=motor6
        return

    def get_columnheaders(self,myfile):
    #get first line
        lineStr=myfile.readline()
        strippedLine=lineStr.rstrip()
        tokenized=strippedLine.split()
        self.columndict={}
        self.columndict['columnlist']=[]
        for i in N.arange(len(tokenized)):
            self.columndict[tokenized[i]]=[]
            self.columndict['columnlist'].append(tokenized[i])
#        print self.columndict['columnlist']
        return 



    def readibuffer(self,myfilestr):
        self.myfilestr=myfilestr
        myfile = open(myfilestr, 'r')
        # Get the header information
        self.readheader(myfile)
        #skip over the comment
        lineStr = myfile.readline()
        self.get_columnheaders(myfile)
        # get the names of the fields
##        lineStr=myfile.readline()
##        strippedLine=lineStr.rstrip()
##        tokenized=strippedLine.split()
##        scan1=tokenized[0]
##        scan2=tokenized[1]
    #    print scan1
    #    print scan2
    #   prepare to read the data    
        count =  0
#        scan1arr=[]
#        scan2arr=[]
#        intensity=[]
#        intensityerr=[]
##        while 1:
##            lineStr = myfile.readline()
##    #        print lineStr
##    #        print 'Count ', count
##            if not(lineStr):
##                break
##            count = count + 1
##            if lineStr[0] != "#":
##                #print "#:",count,lineStr.rstrip()
##                strippedLine=lineStr.rstrip()
##                tokenized=strippedLine.split()
##                scan1arr.append(float(tokenized[0]))
##                scan2arr.append(float(tokenized[1]))
##                intensity.append(float(tokenized[3]))
##                intensityerr.append(N.sqrt(float(tokenized[2])))
##        myfile.close()
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
        myfile.close()
#        print self.columndict['COUNTS']
#        print self.header
        mydata=Data(self.header,self.columndict)
#        data={scan1:N.array(scan1arr,'d')}
#        data[scan2]=N.array(scan2arr,'d')
#        data['intensity']=N.array(intensity,'d')
#        data['intensity_err']=N.array(intensityerr,'d')
                  
        return mydata

class Data:
    def __init__(self,header,data):
        self.header=header
        self.data=data
    def get_monitor(self):
        return self.header['monitor']
    def get_filetype(self):
        return self.header['filetype']
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
    monitor=property(get_monitor)
    count_type=property(get_count_type)
    filetype=property(get_filetype)
    npts=property(get_npts)
    motor1=property(get_motor1)
    motor2=property(get_motor2)
    motor3=property(get_motor3)
    motor4=property(get_motor4)
    motor5=property(get_motor5)
    motor6=property(get_motor6)    
    data_fields=property(get_data_fields)
    
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
    myfilestr=r'c:\summerschool2007\\qCdCr014.ng5'
    mydirectory=r'c:\summerschool2007\\' 
    myfilenumbers=range(4,33,1)
    myend='.ng5'
    myfilehead='qCdCr'
    data=DataCollection()
    mydatareader=datareader()
    mydata=mydatareader.readibuffer(myfilestr)
#    print mydata.gen_motor6_arr()
#    print mydata.gen_motor5_arr()
#    print mydata.gen_motor4_arr()
#    print mydata.gen_motor3_arr()
#    print mydata.gen_motor2_arr()
#    print mydata.gen_motor1_arr()
    for i in range(len(myfilenumbers)):
        myfilenum=num2string(myfilenumbers[i])
#        print myfilenum
        myfilestr=mydirectory+myfilehead+myfilenum+myend
        print myfilestr
        data.add_datum(mydatareader.readibuffer(myfilestr))
#        header,datum=readibuff(myfilestr)
#        headers.append(header)
#        data.append(datum)
#    print data.get_data()[1].gen_motor1_arr()
#    print data.extract_a4()
    a3,a4,counts=data.extract_a3a4()
#    a3=N.array(a3,'d')
#    a4=N.array(a4,'d')
#    counts=N.array(counts,'d')
    print a3.shape
    print a4.shape
    print counts.shape

    # Grid
#    xi, yi = N.mgrid[-5:5:100j,-5:5:100j]
    xi,yi=N.mgrid[a3.min():a3.max():.1,a4.min():a4.max():.1]
    # triangulate data
    tri = D.Triangulation(a3,a4)

    # interpolate data
    interp = tri.nn_interpolator(counts)

    zi = interp(xi,yi)
    # or, all in one line
    #    zi = Triangulation(x,y).nn_interpolator(z)(xi,yi)

    plot_data(xi,yi,zi)
    
#    mydatareader.readibuffer(myfilestr)




