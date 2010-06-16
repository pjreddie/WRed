from django.db import models
from django.db.models.signals import post_save, post_delete
import xmlrpclib
import sys


# Create your models here.
class DataFile(models.Model):
    md5 = models.CharField(max_length = 32)
    name = models.CharField(max_length = 50)
    proposal_id = models.CharField(max_length = 50)
    dirty = models.BooleanField()
class MetaData(models.Model):
    dataFile = models.ForeignKey(DataFile)
    field = models.CharField(max_length = 20)
    low = models.FloatField()
    high = models.FloatField()
def updated_callback(sender, **kwargs):
    proxy = xmlrpclib.ServerProxy("http://localhost:8045")
    print("transmitting...")
    try:
      proxy.transmit('/updates/files/all', 'Update!!')
      proxy.transmit('/updates/files/' + str(kwargs['instance'].id), 'Update to that file!!')
    except:
      print "transmission failed, error: ",sys.exc_info()[0]
    print "...end of transmission"

post_save.connect(updated_callback, sender = DataFile)
post_delete.connect(updated_callback, sender = DataFile)
