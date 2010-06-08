import numpy as N
import math
import readncnr

def autovectorized(f):
     """Function decorator to do vectorization only as necessary.
     vectorized functions fail for scalar inputs."""
     def wrapper(input):
         if N.isscalar(input)==False:
             return N.vectorize(f)(input)
         return f(input)
     return wrapper



@autovectorized
def myradians(x):
    return math.radians(x)

def calc_energy(angle,dspace):
    anglerad=myradians(angle)
    tau=2*N.pi/dspace
    k=tau/N.sqrt(2-2*N.cos(anglerad))
    energy=2.072142*k*k
    return energy

class polarization_correct:
    def __init__(self,files):
        mydata={}
        self.counts={}
        self.ei={}
        self.ef={}
        self.timestamp={}
        
        for key,myfilestr in files.iteritems():
            mydatareader=readncnr.datareader()
            mydata[key]=mydatareader.readbuffer(myfilestr)
            self.counts[key]=N.array(mydata[key].data['Detector'])
            self.timestamp[key]=N.array(mydata[key].data['timestamp'])
            #TODO currently, we assume that the files are taken at the same points--is this safe?
            self.length=self.counts[key].shape[0]
            a2=N.array(mydata[key].data['A2'])
            a6=N.array(mydata[key].data['A5'])*2.0
            #TODO who's bright idea was it to have A6 listed as "IN"
            #TODO we also assume that the energies will be the same!!!
            dmono=mydata[key].header['dmono']
            dana=mydata[key].header['dana']
            #print a6
            self.ei=calc_energy(a2,dmono)
            self.ef=calc_energy(a6,dana)
            #print self.length
        #print mydata[key].data.keys()
        return
    def output(self,outputfile=None):
        keys=['off_off','on_on','on_off','off_on',]
        s=''
        if outputfile!=None:
            f=open(outputfile,'wt')
        for i in range(self.length):
            s=s+'%f %f '%(self.ei[i],self.ef[i])
            for key in keys:
                if self.counts.has_key(key):
                    s=s+'%f '%(self.counts[key][i],)
                    s=s+'%f '%(self.timestamp[key][i],)
                else:
                    s=s+'* * '
            s=s+'\n'
            print i
        if outputfile==None:
            print s
        else:
            f.write(s)
        if outputfile!=None:
            f.close()
        return

  


if __name__=="__main__":
    myfilestr_on_off=r'c:\bifeo3xtal\jan8_2008\9175\fieldscansplusminus53566.bt7'
    myfilestr_off_on=r'c:\bifeo3xtal\jan8_2008\9175\fieldscanminusplus53567.bt7'
    files={}
    #files['on_on']=myfilestr_on_on
    files['on_off']=myfilestr_on_off
    files['off_on']=myfilestr_off_on
    #files['off_off']=myfilestr_off_off    
    mypolcor=polarization_correct(files)
    outstr=r'c:\sqltest\pol.txt'
    mypolcor.output(outstr)

    