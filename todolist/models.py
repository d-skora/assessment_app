from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Model for todolist item
class Task(models.Model):
    name = models.CharField(max_length=500)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# Model for Location
class Location(models.Model):
    name = models.CharField(max_length=500)
    lat = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    lon = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

    def __str__(self):
        return self.name
