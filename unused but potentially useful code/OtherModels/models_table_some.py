from django.db import models

# Create your models here.
class DataFile(models.Model):
    metaData = models.CharField(max_length = 500)
    name = models.CharField(max_length = 50)
#END

class Table(models.Model):
    fileid = models.ForeignKey(DataFile)
    value = models.CharField(max_length = 50)
    field = models.CharField(max_length = 50)
    pointid = models.IntegerField()
