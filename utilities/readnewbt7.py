import numpy as N
import pylab
import sys


def readheader(myfile):
#get first line
    myFlag=True
    while myFlag:
        lineStr=myfile.readline()
        strippedLine=lineStr.rstrip()
        tokenized=strippedLine.split()
        if tokenized[0]=='#Columns':
            columndict={}
            columndict['columnlist']=[]
            for i in N.arange(len(tokenized)-1)+1:
                columndict[tokenized[i]]=[]
                columndict['columnlist'].append(tokenized[i])
            myFlag=False
    print columndict['columnlist']
    return columndict


def readbt7file(myfilestr):
    myfile = open(myfilestr, 'r')
    # Get the header information
    columns=readheader(myfile)
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
                field=columns['columnlist'][i]
                columns[field].append(tokenized[i])
    myfile.close()
    return columns

def outputresult(columns,fields):
    for i in range(len(columns['A4'])):
        lineStr=''
        for j in range(len(fields)):
            lineStr=lineStr+columns[fields[j]][i]+' '
        print lineStr
    return

def saveresult(columns,fields,outputfile):
    myfile = open(outputfile, 'w')
    lineStr='# '
    for i in range(len(fields)):
        lineStr=lineStr+ fields[i]+' '
    myfile.write("%s\n" % lineStr)
    for i in range(len(columns['A4'])):
        lineStr=''
        for j in range(len(fields)):
            lineStr=lineStr+columns[fields[j]][i]+' '
        myfile.write("%s\n" % lineStr)
    myfile.close()
    return




if __name__=="__main__":
    if 0:
        mydirectory=r'c:\bt7calibrate\\'
        
        myfiles=['46625']
        myend='.bt7'
        myfilehead='al2o3nightscan'
        alldata=[]
        for i in range(len(myfiles)):
            myfilestr=mydirectory+myfilehead+myfiles[i]+myend
            columns=readbt7file(myfilestr)
            alldata.append(columns)
        print alldata[0].keys()
        print (alldata[0])['TDC5']
    if 1:
        argv = sys.argv
        if argv==None:
            argv[1]='al2o3nightscan4665.bt7'
            argv[2]='out.txt'
            argv[3]='A4'
            argv[4]='TDC5'
 	if argv!=None:
		print argv
		inmyfilestr=argv[1]
		outmyfilestr=argv[2]
		fields=argv[3:len(argv)]
		columns=readbt7file(inmyfilestr)
		print fields
		# to really do error checking, you need to check all the fields
		if columns.has_key(fields[0]):
                    outputresult(columns,fields)
                    saveresult(columns,fields,outmyfilestr)
                else:
                    print 'bad field entered'
		



