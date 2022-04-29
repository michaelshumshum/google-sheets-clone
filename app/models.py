from django.db import models
from picklefield.fields import PickledObjectField


class File(models.Model):
    name = models.CharField(max_length=64, default='null')
    dataframe = PickledObjectField()
