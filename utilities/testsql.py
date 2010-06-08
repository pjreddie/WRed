import sqlite3
mydatbstr=r'c:\sqltest\test.dat'
#conn = sqlite3.connect(mydatbstr)
conn=sqlite.connect(':memory:')
c = conn.cursor()
c.execute('''
   create table members(
       id int,
       name varchar,
       login timestamp
   )
''')
c.execute('''
   insert into members
   values (1,'jeff','2006-10-01')
''')
c.execute('''
   insert into members
   values (2,'angie','2006-10-02')
''')
c.execute('''
   insert into members
   values (3,'dylan','2006-10-03')
''')
print "done"