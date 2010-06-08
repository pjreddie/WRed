from django.db import models

# Create your models here.
class DataFile(models.Model):
    md5 = models.CharField(max_length = 32)
    name = models.CharField(max_length = 50)
class MetaData(models.Model):
    dataFile = models.ForeignKey(DataFile)
    field = models.CharField(max_length = 20)
    low = models.FloatField()
    high = models.FloatField()
