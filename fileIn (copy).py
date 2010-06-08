#from display.models import Point, DataSet
#from django.db import models
import os
#from fileio import data_abstraction
def processfile(filestr):
    modeltemplate = open('display/models_template.py', 'r')
    modelfile = open('display/models2.py', 'w')
    for lines in modeltemplate:
        modelfile.write(lines)
    filestr = 'sample.bt7'
    #data = processfile(filestr)

    f = open(filestr, 'r')
    variables = []
    
    print 'hey'
    for lines in f:
        lines = lines.split()
        print lines
        print 
        if lines[0] == '#Columns':
            print 'Columns'
            variables = lines[1:]
            break
    for i in variables:
        modelfile.write('    ' + i + '= models.FloatField(null = True)\n')

"""
    os.system('python manage.py syncdb --noinput')

    p = Point
    data = DataSet(name= filestr, metaData= 'metadata')
    data.save()

    for line in f:
        line.split()
        
        for i in range(len(line)):
            value = line[i]
            v = value
            try:
                v = float(value)
            except ValueError:
                pass
            if isinstance(v, str) == False: setattr(p, variables[i], v)

        setattr(p, 'dataSet', data.id)
        p.save()
    return data
"""
