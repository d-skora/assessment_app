from django.shortcuts import render

from todolist.models import Task


# Endpoint for listing all tasks
def index(request):
    return render(request, "tasks/index.html", {'tasks': Task.objects.order_by('date')})

