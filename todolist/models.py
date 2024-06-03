from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Model for todolist item
class Task(models.Model):
    name = models.CharField(max_length=500)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    done = models.BooleanField(default=False)
    location = models.ForeignKey(
        'Location', on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


# Model for Location
class Location(models.Model):
    name = models.CharField(max_length=500)
    lat = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    lon = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])

    def __str__(self):
        return self.name


# Model for Weather
class Weather(models.Model):
    # When the location for the weather read is deleted, the read is obsolete and should be deleted along
    location = models.OneToOneField(
        'Location', on_delete=models.CASCADE, primary_key=True, related_name='weather'
    )
    temperature = models.FloatField()
    status = models.CharField(max_length=500)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.status + ', ' + str(self.temperature)


# Model for last weather reads of Done Tasks
class LastWeatherRead(models.Model):
    task = models.OneToOneField(
        'Task', on_delete=models.CASCADE, primary_key=True, related_name='last_weather_read'
    )
    temperature = models.FloatField()
    status = models.CharField(max_length=500)
