import sys,os,shutil


def readfile(filename):
    myfile=open(filename,'r')
    flag=True
    first=True
    line_num=0
    mark=None
    linetoexecute=None
    while flag:
        myline=myfile.readline()
        if not(myline):
            break
        if first:
            firstline=myline
            first=False
        if myline[0]=='*':
            linetoexecute=myline[1:]
            mark=line_num+1
            break
        line_num=line_num+1
    myfile.close()
    if mark==None:
        mark=0
        linetoexecute=firstline

    return linetoexecute,mark

def writefile(filename,linetoexecute,mark):
    myfile=open(filename+'_tmp','w')
    myfilein=open(filename,'r')
    flag=True
    i=0
    while flag:
        myline=myfilein.readline()
        if not(myline):
            break
        if i==mark-1:
            myfile.write(linetoexecute)
        elif i==mark:
            myfile.write('*'+myline)
            #elif i==mark-1:
            #    myfile.write('*'+myline)
        else:
            myfile.write(myline)
        #else:
            #myfile.write('*'+linetoexecute)  #if there was no star in the file, then execute the first line
        i=i+1
    myfile.close()
    return i
    
def driver(myfilestr,overwrite=True):
    linetoexecute,mark=readfile(myfilestr)
    #print linetoexecute, mark
    i=writefile(myfilestr,linetoexecute,mark)
    if overwrite:
        shutil.copyfile(myfilestr+'_tmp', myfilestr)
    #if i==mark:
    #    raise SequenceEndError,'sequence ended'
    return linetoexecute, i,mark
    

class SequenceEndError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

    
    
if __name__=="__main__":
    myfilestr=r'c:\dum'
    print driver(myfilestr)
    
    
            
        
        