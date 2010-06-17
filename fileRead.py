#Author: Joe Redmon
#fileRead.py

import md5, os
from display.models import *
from django.db import models, transaction
from utilities import data_abstraction

def handle_uploaded_file(files, proposal_id):
    filename = files.name
    tempfile = file('db/temp', 'wb+')
    for chunk in files.chunks():
        tempfile.write(chunk)
    tempfile.close()
    addfile('db/temp', filename, proposal_id, False)

def handle_uploaded_live_file(files, filename, proposal_id):
    print '*******livefile: ',filename
    tempfile = file('db/temp', 'wb+')
    for chunk in files.chunks():
        tempfile.write(chunk)
    tempfile.close()
    addfile('db/temp', filename, proposal_id, True)

@transaction.commit_manually
def addfile(filestr, filename, proposal_id, dirty):
    m = md5.new()
    filein = file(filestr, 'rb') # open in binary mode
    
    while True:
        t = filein.read(1024)
        if len(t) == 0: break # end of file
        m.update(t)
    print m.hexdigest()
    filein.close()
    f = DataFile()
    if dirty:
        f, created = DataFile.objects.get_or_create(
            name = filename, 
            dirty = True,
            proposal_id = proposal_id,
            defaults = {'md5': m.hexdigest()}
        )
        if not created:
            os.remove(os.path.join('db', f.md5)+ '.file')
            f.md5 = m.hexdigest()
            f.metadata_set.all().delete()
    else:
        f, created = DataFile.objects.get_or_create(
            md5 = m.hexdigest(),
            defaults = {'dirty': False, 'name': filename,'proposal_id':proposal_id},
        )
        if not created:
            f.dirty = False
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
        if lines[0] == '#': break
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
    f.save()
    transaction.commit()
