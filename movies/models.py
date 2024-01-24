from django.db import models
from django.core.exceptions import ValidationError


class Country(models.Model): 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)

class Director(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, blank=False, null=False)
    year = models.IntegerField(blank=False, null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    directors = models.ManyToManyField(Director)
    studio = models.CharField(max_length=255)
    