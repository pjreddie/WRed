#Author: Joe Redmon
#models.py

from django.db import models
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
class Pipeline(models.Model):
    proposal_id = models.CharField(max_length = 50)
    pipeline = models.CharField(max_length = 10000)
    name = models.CharField(max_length = 50)
