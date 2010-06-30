#Author: Joe Redmon
#fileToJson.py

import md5, os
import simplejson
from display.models import MetaData, DataFile
from django.db import models
from utilities import data_abstraction

def displayfile(filestr):
    f = open(filestr, 'r')
    metadata = []
    data = []
    
    for line in f:
        line_array = line.split()
        if line[0] == '#':
            metadata_name = line_array[0][1:]
            metadata_data = ' '.join(line_array[1:])
            metadata.append(dict(name=metadata_name, data=metadata_data))
            
        if line_array[0] == '#Columns':
            data.append(line_array[1:])
            break

    for line in f:
        if line[0] == '#': break
        data.append(line.split())
        
    return dict(metadata=metadata, data=data)
