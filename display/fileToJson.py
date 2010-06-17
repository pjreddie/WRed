#Author: Joe Redmon
#fileToJson.py

import md5, os
from display.models import MetaData, DataFile
from django.db import models
from utilities import data_abstraction

def displayfile(filestr):
    f = open(filestr, 'r')
    out = []
    
    for lines in f:
        lines = lines.split()
        if lines[0] == '#Columns':
            out.append(lines[1:])
            break

    for lines in f:
        if lines[0] == '#': break
        out.append(lines.split())
    return out
