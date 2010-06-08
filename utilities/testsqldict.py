import sqlite3
import numpy as N
import readicp
mydatbstr=r'c:\sqltest\test.dat'
mydatbstr=r':memory:'

def sqlexecute(conn,s,splacevalues=None):
    c = conn.cursor()
    if splacevalues!=None:
        c.execute(s,splacevalues)
    else:
        c.execute(s)
    id=c.lastrowid
    c.close()
    conn.commit()
    return id

def sqlselect(conn,s,splacevalues=None):
    c = conn.cursor()
    if splacevalues!=None:
        c.execute(s,splacevalues)
    else:
        c.execute(s)
    rows=c.fetchall()
    c.close()
    conn.commit()
    return rows
    
if __name__=="__main__":
    g=N.array([1,2,3],'d')
    mydict={}
    mydict['myarr']=g

    for k,v in mydict.iteritems():
        print k,v
        s='create table '+k
        s=s+'(%sid integer primary key'%(k)
        print s
        if isinstance(v,N.ndarray):
            print 'true'
            for i in N.arange(v.shape[0]):
                print v[i]

    #qbuffer
    myfilestr=r'c:\sqltest\\mnl1p004.ng5'
    mydatareader=readicp.datareader()
    mydata=mydatareader.readbuffer(myfilestr)
    print mydata.header['filename']
    
    #create our database
    #conn=sqlite3.connect(':memory:')
    conn=sqlite3.connect(mydatbstr)
    
    #create a table with our list of files
    s='create table catalog(file_id integer primary key, file_name varchar(12),sample_id integer)'
    sqlexecute(conn,s)
    print 'created catalog table'


    s='create table fields'
    s=s+'(field_id integer primary key, file_id integer, field_name varchar(20))'
    sqlexecute(conn,s)
    print 'created fields table'

    s='create table measurement'
    s=s+'(measurement_id integer primary key, file_id integer, field_id integer'
    s=s+',point_num integer, value float, error float)'
    print s
    sqlexecute(conn,s)
    print 'measurement table created'
    
    
    
    s='insert into catalog VALUES(NULL,?,NULL)'
    splacevalues=(mydata.header['filename'],)
    file_id=sqlexecute(conn,s,splacevalues)
    print 'catalog instantiated'
    #print 'file_id ',file_id

    for tablename, tablevalues in mydata.data.iteritems():
        s='insert into fields VALUES(NULL,?,?)'
        sparams=(file_id, tablename)
        field_id=sqlexecute(conn,s,sparams)
        print 'inserted %s into field table'%(tablename,)
        #print 'field_id ',field_id
        #print 'type ',type(tablevalues)
        if isinstance(tablevalues,list):
            for point_num in N.arange(len(tablevalues)):
                
                
                if tablename=='Counts':
                    s='insert into measurement VALUES (NULL,?,?,?,?,?)'
                    sparams=(file_id,field_id,point_num,tablevalues[point_num],N.sqrt(tablevalues[point_num]))
                else:
                    s='insert into measurement VALUES (NULL,?,?,?,?,NULL)'
                    sparams=(file_id,field_id,point_num,tablevalues[point_num])
                #print s
                #print sparams
                sqlexecute(conn,s,sparams)
                #print 'point inserted!'
                
                

   
    s='select file_id,file_name from catalog'
    print s
    rows=sqlselect(conn,s)
    print rows
    s='select field_id from fields where field_name=?'
    sparam=('Temp',)
    print s,sparam
    field_id=sqlselect(conn,s,sparam)
    print 'field_id= ',field_id
    s='select measurement.file_id,point_num,value,error from measurement where field_id=? order by point_num'
    sparam=field_id[0]
    print s
    mypoints=sqlselect(conn,s,sparam)
    print 'selected'    
    print mypoints
    print "done"