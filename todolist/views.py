from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from todolist.forms import TaskForm
from todolist.models import Task


# Endpoint for listing all tasks
def index(request):
    return render(request, "tasks/index.html", {'tasks': Task.objects.order_by('date')})


# Endpoint for adding new tasks
def add(request):
    # process form data if this is a POST
    if request.method == "POST":
        # create form and complete with request data
        form = TaskForm(request.POST)
        # validate
        if form.is_valid():
            # Save new Task
            task = Task.objects.create(name=form.cleaned_data['name'], date=form.cleaned_data['date'])
            # redirect to index:
            return HttpResponseRedirect("/")

    # display blank form if not a POST
    else:
        form = TaskForm()

    return render(request, "tasks/add.html", {"form": form})


# Endpoint for clearing the entire list of tasks
def clear(request):
    if request.method == "POST":
        entries = Task.objects.all()
        entries.delete()

    return HttpResponseRedirect("/")
