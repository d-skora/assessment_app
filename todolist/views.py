from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

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
            form.save()
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


# Endpoint for editing existing tasks
def edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    form = TaskForm(request.POST or None, instance=task)
    # process form data if this is a POST
    if request.method == "POST" and form.is_valid() and form.has_changed():
        # save existing Task
        form.save()
        # redirect to index:
        return HttpResponseRedirect("/")
    if not form.has_changed():
        form.add_error(None, 'Nothing changed')

    return render(request, "tasks/edit.html", {"form": form, "task": task})


# Endpoint for deleting existing tasks
def delete(request, task_id):
    if request.method == "POST":
        # fetch Task to be deleted
        task = get_object_or_404(Task, pk=task_id)
        # delete existing Task
        task.delete()

    # redirect to index:
    return HttpResponseRedirect("/")


# Endpoint for marking an existing task as done
def complete(request, task_id):
    if request.method == "POST":
        # fetch Task to be updated
        task = get_object_or_404(Task, pk=task_id)
        # update Task
        task.done = True
        task.save()

    # redirect to index:
    return HttpResponseRedirect("/")
