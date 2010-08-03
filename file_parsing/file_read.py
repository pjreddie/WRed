#Author: Joe Redmon
#fileRead.py

import md5, os
from display.models import *
from django.db import models, transaction
from utilities import data_abstraction
from file_operator import *

def handle_uploaded_file(files, proposal_id):
    filename = files.name
    tempfile = file('db/temp.' + filename.split('.')[-1], 'wb+')
    for chunk in files.chunks():
        tempfile.write(chunk)
    tempfile.close()
    addfile('db/temp.' + filename.split('.')[-1], filename, proposal_id, False)

def handle_uploaded_live_file(files, filename, proposal_id):
    print '*******livefile: ',filename
    tempfile = file('db/temp.' + filename.split('.')[-1], 'wb+')
    for chunk in files.chunks():
        tempfile.write(chunk)
    tempfile.close()
    addfile('db/temp.' + filename.split('.')[-1], filename, proposal_id, True)

@transaction.commit_manually
def addfile(filestr, filename, proposal_id, dirty):
    m = md5.new()
    print '1', filestr
    a = Data(filestr)
    m.update(a.__str__())
    print m.hexdigest()
    f = DataFile()
    print 1
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
            f.save()
    else:
        f, created = DataFile.objects.get_or_create(
            md5 = m.hexdigest(),
            defaults = {'dirty': False, 'name': filename,'proposal_id':proposal_id},
        )
        if not created:
            f.dirty = False
            f.save()
    print 3
    a.correct_scan()
    print 4
    a.write('db/' + m.hexdigest() + '.file')
    print 5
    fd = open('db/' + m.hexdigest() + '.file', 'r')
    print 6
    t = []
    for lines in fd:
        lines = lines.split()
        if len(lines) == 0:
            continue
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
    transaction.commit()
