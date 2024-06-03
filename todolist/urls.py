from django.urls import path

from . import views

app_name = 'todolist'
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:task_id>/details", views.details, name="details"),
    path("add", views.add, name="add"),
    path("clear", views.clear, name="clear"),
    path("<int:task_id>/", views.edit, name="edit"),
    path("<int:task_id>/delete", views.delete, name="delete"),
    path("<int:task_id>/complete", views.complete, name="complete"),
    path("<int:location_id>/get_weather", views.get_weather, name="get_weather"),
    path("weather_refresh", views.force_weather_refresh, name="force_weather_refresh"),
]
