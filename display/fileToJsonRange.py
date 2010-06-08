import md5, os
from display.models import MetaData, DataFile
from django.db import models
from utilities import data_abstraction

def displayfile(filestr):
    f = open(filestr, 'r')
    t = []
    out = []
    for lines in f:
        lines = lines.split()
        if lines[0] == '#Columns':
            print 'Columns'
            t.append(lines[1:])
            break

    for lines in f:
        t.append(lines.split())
    for j in range(len(t[0])):
        column = []
        for i in range(len(t)):
            column.append(t[i][j])
        out.append(columns)
    return out
