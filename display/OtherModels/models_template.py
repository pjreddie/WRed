from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length = 30)
    city = models.CharField(max_length = 30)
    date = models.IntegerField()

# Create your models here.
class DataSet(models.Model):
    metaData = models.CharField(max_length = 500)
    name = models.CharField(max_length = 50)
#END

