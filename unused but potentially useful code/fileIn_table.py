import line_profiler
import os,sys
#print sys.path
#print __file__
from display.models import Table, DataFile
from django.db import models

from utilities import data_abstraction
#DJANGO_SETTINGS_MODULE = fileviewer.settings
#@profile
def addfile(filestr):


    #filestr = 'sample.bt7'
    f = DataFile(name = filestr, metaData = 'sample meta data')
    f.save()
    data = data_abstraction.processfile(filestr)
    baselayer = ['primary_motors', 'physical_motors', 'monochromator']
    sublayer = [['a1','a2','a3','a4','a5','a6','sample_elevator','sample_upper_tilt', 'sample_upper_translation', 'sample_lower_tilt','sample_upper_translation','dfm_rotation','analyzer_rotation'],['h','k','l','e','qx','qy','qz','hkl'],['name','vertical_focus','horizontal_focus','blades','mosaic','dspacing','focus_cu','focus_pg','translation','elevation']]
    for i in range(len(baselayer)):
        for j in range(len(sublayer[i])):
            attr = getattr(getattr(data, baselayer[i]), sublayer[i][j])
            try: 
                it = iter(attr)
                count = 0
                for val in it:
                    t = Table(fileid = f, value = str(val), field = sublayer[i][j], pointid = count)
                    t.save()
                    ++count
            except TypeError:
                t = Table(fileid = f, value = str(attr), field = sublayer[i][j], pointid = 0)
                t.save()
    

