import sqlite3
import numpy as N
import readncnr2 as readncnr
import pylab
#mydatbstr=r'c:\sqltest\test.dat'
mydatbstr=r':memory:'
#testq1=r'c:\sqltest\testq1.ng5'
testq2=r'c:\sqltest\testq2.ng5'
testq1=r'c:\bifeo3xtal\jan8_2008\9175\fieldscansplusminusreset53630.bt7'



def sqlexecute(conn,s,splacevalues=None):
    c = conn.cursor()
    if splacevalues!=None:
        try:
            c.execute(s,splacevalues)
        except sqlite3.InterfaceError:
            print 'failed %s %s',(s,splacevalues)
    else:
        try:
            c.execute(s)
        except sqlite3.InterfaceError:
            print 'failed %s',(s)
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

def mytype(myobj):
    pytype=type(myobj)
    print 'python type ',pytype
    if pytype==type('test'):
        sqltype='varchar(20)'
    if pytype==type(4):
        sqltype='integer'
    if pytype==type(4.0):
        sqltype='real'
    if pytype==type(None):
        sqltype='real'
    if pytype==type([]):
        sqltype='BLOB'
    return sqltype


class sqlreader:
    def __init__(self,database=r':memory:'):
        self.conn=sqlite3.connect(database)
        self.create_tables()
        return
    def create_meta_tables(self,metadata,file_id):

        for metaname, metadict in metadata.iteritems():
            tablename='meta%s'%(metaname,)
            s='insert into metadata VALUES(NULL,?,?)'
            #print s
            print 'metatablename ',tablename
            sparams=(file_id, tablename)
            meta_id=sqlexecute(self.conn,s,sparams)
            print 'inserted %s into metadata table'%(tablename,)
            for metakey, metavalue in metadict.iteritems():
                s='create table %s'%(tablename,)
                s=s+'(%s_id integer primary key'%(tablename,)
                s_insert='insert into %s VALUES(NULL'%(tablename,)
                s_insertp={}
                for key, value in metadict.iteritems():
                    s=s+',%s %s'%(key,mytype(value))
                    s_insert=s_insert+',:%s'%(key)
                    s_insertp[key]=value
                s=s+')'
                s_insert=s_insert+')'
            print s
            try:
                metatable_id=sqlexecute(self.conn,s)
                print 'created table %s'%(tablename,)
            except sqlite3.OperationalError:
                pass
            print s_insert
            print s_insertp
            try:
                sqlexecute(self.conn,s_insert,s_insertp)
                print 'inserted values into table %s'%(tablename,)
            except sqlite3.OperationalError:
                print 'could not insert value into table %s'%(tablename,)
                
        return
    def create_tables(self):
        s='create table catalog(file_id integer primary key, file_name varchar(12),sample_id integer,filetype integer)'
        sqlexecute(self.conn,s)
        print 'created catalog table'


        s='create table fields'
        s=s+'(field_id integer primary key, file_id integer, field_name varchar(20))'
        sqlexecute(self.conn,s)
        print 'created fields table'

        s='create table measurement'
        s=s+'(measurement_id integer primary key, file_id integer, field_id integer'
        s=s+',point_num integer, value float, error float)'
        print s
        sqlexecute(self.conn,s)
        print 'measurement table created'
        print 'creating metadata table'
        s='create table metadata(metaid integer primary key, file_id integer, meta_name varchar(20))'
        print s
        sqlexecute(self.conn,s)
        print 'metadata table created'
        return
 
    
    def insert_file(self,myfilestr=r'c:\sqltest\\mnl1p004.ng5'):
        mydatareader=readncnr.datareader()
        mydata=mydatareader.readbuffer(myfilestr)
        print mydata.metadata['file_info']['filename']
        #insert file into database
        s='insert into catalog VALUES(NULL,?,NULL,0)'
        splacevalues=(mydata.metadata['file_info']['filename'],)
        file_id=sqlexecute(self.conn,s,splacevalues)
        print 'catalog instantiated'
        
        for tablename, tablevalues in mydata.data.iteritems():
            s='insert into fields VALUES(NULL,?,?)'
            sparams=(file_id, tablename)
            field_id=sqlexecute(self.conn,s,sparams)
            print 'inserted %s into field table'%(tablename,)
            if isinstance(tablevalues,list):
                for point_num in N.arange(len(tablevalues)):   
                    if tablename=='detector':
                        s='insert into measurement VALUES (NULL,?,?,?,?,?)'
                        sparams=(file_id,field_id,point_num,tablevalues[point_num],N.sqrt(tablevalues[point_num]))
                    else:
                        s='insert into measurement VALUES (NULL,?,?,?,?,NULL)'
                        sparams=(file_id,field_id,point_num,tablevalues[point_num])
                    sqlexecute(self.conn,s,sparams)
        self.create_meta_tables(mydata.metadata,file_id)
        return
    def select(self,field_selected='e'):
        s='select file_id,file_name from catalog'
        #print s
        rows=sqlselect(self.conn,s)
        #print rows
        s='select field_id from fields where field_name=?'
        sparam=(field_selected,)
        #print s,sparam
        field_id=sqlselect(self.conn,s,sparam)
        #print 'field_id= ',field_id
        if field_selected=='detector':
            s='select value,error from measurement where field_id=? order by point_num'
        else:
            s='select value from measurement where field_id=? order by point_num'
        sparam=field_id[0]
        #print s
        mypoints=sqlselect(self.conn,s,sparam)
        #print 'selected'    
        #print mypoints
        #print "done"
        return mypoints
    
if __name__=="__main__":
    mysqlreader=sqlreader(mydatbstr)
    mysqlreader.insert_file(testq1)
    #mysqlreader.insert_file(testq2)
    

    if 1:
        mypoints=mysqlreader.select('qx')
        qx=N.array(mypoints).flatten()
        print qx
        mypoints=mysqlreader.select('detector')
        Counts=N.array(mypoints)
        print Counts
        #print Counts[:,0]
        #print Counts[:,1]
    if 0:
        pylab.plot(T,Counts)
        #pylab.errorbar(T,Counts[:,0],Counts[:,1],marker='s')
        pylab.show()