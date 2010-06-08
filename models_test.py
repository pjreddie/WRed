from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length = 30)
    city = models.CharField(max_length = 30)
    date = models.IntegerField()

