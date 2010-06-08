import md5, os
from display.models import MetaData, DataFile
from django.db import models
from utilities import data_abstraction

def handle_uploaded_file(files):
    filename = files.name
    tempfile = file('db/temp', 'wb+')
    for chunk in files.chunks():
        tempfile.write(chunk)
    tempfile.close()
    addfile('db/temp', filename)


def addfile(filestr, filename):
    m = md5.new()
    filein = file(filestr, 'rb') # open in binary mode
    
    while True:
        t = filein.read(1024)
        if len(t) == 0: break # end of file
        m.update(t)
    print m.hexdigest()
    
    f = DataFile(name = filename, md5 = m.hexdigest())
    f.save()
    filein.close()
    filein = file(filestr, 'rb') # open in binary mode
    fileout = file('db/' + m.hexdigest() + '.file', 'wb')
    
    while True:
        t = filein.read(1024)
        if len(t) == 0: break # end of file
        fileout.write(t)
    fileout.close()
    filein.close()
    fd = open(filestr, 'r')
    t = []
    for lines in fd:
        lines = lines.split()
        if lines[0] == '#Columns':
            print 'Columns'
            t.append(lines[1:])
            break

    for lines in fd:
        t.append(lines.split())
    fd.close()
    rows = t[1:]
    variables = t[0]
    out = []

    for j in range(len(variables)):
        column = []
        for i in range(len(rows)):
            column.append(rows[i][j])
        out.append(column)

    for i in range(len(variables)):
        try:
            maxval = float(max(out[i]))
            minval = float(min(out[i]))
            metadata = MetaData(dataFile = f, field = variables[i], low = minval, high = maxval)
            metadata.save()
        except ValueError:
            pass
