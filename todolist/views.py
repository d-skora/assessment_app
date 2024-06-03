from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404

from todolist.forms import TaskForm
from todolist.models import Task, Weather, Location, LastWeatherRead
from todolist.weather import fetch_weather


# Endpoint for listing all tasks
def index(request):
    tasks = Task.objects.order_by('date')
    # Get weather data for active locations
    active_locations = tasks.exclude(done=True).values('location').distinct()
    locations = Location.objects.filter(id__in=active_locations)
    weather_reads = {}
    for location in locations:
        weather_reads[location.id] = fetch_weather(location)
    # Expand tasks with weather information
    for task in tasks:
        if task.done and hasattr(task, 'last_weather_read'):
            task.weather = {
                'temp': task.last_weather_read.temperature,
                'weather': task.last_weather_read.status
            }
        elif task.location is not None:
            task.weather = weather_reads[task.location.id]

    return render(
        request,
        "tasks/index.html",
        {'tasks': tasks, 'weather_reads': weather_reads}
    )


# Endpoint for task details
def details(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.location is not None:
        weather = fetch_weather(task.location)
    else:
        weather = None
    return render(request, "tasks/details.html", {'task': task, "weather": weather})


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
    if task.location is not None:
        weather = fetch_weather(task.location)
    else:
        weather = None
    form = TaskForm(request.POST or None, instance=task)
    # process form data if this is a POST
    if request.method == "POST" and form.is_valid() and form.has_changed():
        # save existing Task
        form.save()
        # redirect to index:
        return HttpResponseRedirect("/")
    if not form.has_changed():
        form.add_error(None, 'Nothing changed')

    return render(request, "tasks/edit.html", {"form": form, "task": task, "weather": weather})


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
        if hasattr(task, 'location'):
            last_weather_read = Weather.objects.filter(location=task.location).first()
            if last_weather_read:
                LastWeatherRead.objects.create(
                    task=task,
                    temperature=last_weather_read.temperature,
                    status=last_weather_read.status
                )

        task.save()

    # redirect to index:
    return HttpResponseRedirect("/")


# Endpoint for fetching weather for fetch API calls
def get_weather(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    data = fetch_weather(location)

    return JsonResponse(data)


# Endpoint for clearing all weather data to force it to be re-fetched
def force_weather_refresh(request):
    if request.method == "POST":
        entries = Weather.objects.all()
        entries.delete()

    return HttpResponseRedirect("/")
