from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Result:
    def __init__(self, name, distance, category=None):
        self.name = name
        self.distance = distance
        self.category = category

    def __str__(self):
        return self.name