from django.test import TestCase

from .forms import TaskForm
from .models import Task, Location, Weather
from django.urls import reverse


# Helper for creating simple tasks
def create_task(name, date):
    return Task.objects.create(name=name, date=date)


# Test of Task model
class TaskModelTest(TestCase):

    def test_string_representation(self):
        task = Task(name="Eat chips")
        self.assertEqual(str(task), task.name)


# Test of Location model
class LocationModelTest(TestCase):

    def test_string_representation(self):
        task = Task(name="Rome")
        self.assertEqual(str(task), task.name)


# Test for Task form
class TaskFormTest(TestCase):
    # Valid Form Data
    def test_TaskForm_valid(self):
        form = TaskForm(
            {'name': 'Eat crisps', 'date_0': '2024-05-26', 'date_1': '10:00:00'}
        )
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_TaskForm_invalid(self):
        form = TaskForm({'name': "", 'date': "bad text"})
        self.assertFalse(form.is_valid())


# Tests for endpoints
class ProjectTests(TestCase):

    # Tests index returns current Tasks
    def test_index(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task2 = create_task('Drink cola', '2024-05-30T12:00:00Z')
        response = self.client.get(reverse('todolist:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['tasks'], [task1, task2])

    # Tests details fail when Task is not found
    def test_details_invalid(self):
        response = self.client.get(reverse('todolist:details', args=[1]))
        self.assertEqual(response.status_code, 404)

    # Tests details return the correct Task details when Task is found
    def test_details_valid(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        response = self.client.get(reverse('todolist:details', args=[task1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/details.html")
        self.assertEqual(response.context['task'], task1)

    # Tests Add Task form is rendered
    def test_add_GET(self):
        response = self.client.get(reverse('todolist:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/add.html")

    # Tests adding a Task fails for invalid data and returns errors for the form
    def test_add_POST_invalid(self):
        response = self.client.post(
            reverse('todolist:add'),
            {'name': 'Drink soda', 'date_0': 'bad', 'date_1': 'data'}
        )
        self.assertTemplateUsed(response, "tasks/add.html")
        self.assertFormError(
            response.context['form'], 'date', ['Enter a valid date.', 'Enter a valid time.']
        )

    # Tests adding a Task creates a new Task and redirects back to the list
    def test_add_POST_valid(self):
        task_count = Task.objects.count()
        response = self.client.post(
            reverse('todolist:add'),
            {'name': 'Drink soda', 'date_0': '2024-05-31', 'date_1': '12:00:00'}
        )
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), task_count + 1)

    # Tests clearing all Tasks removes all tasks
    def test_clear(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task2 = create_task('Drink cola', '2024-05-30T12:00:00Z')
        self.assertEqual(Task.objects.count(), 2)
        response = self.client.post(reverse('todolist:clear'))
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), 0)

    # Tests opening the Edit Task form fails when the Task is not found
    def test_edit_GET_invalid(self):
        response = self.client.get(reverse('todolist:edit', args=[1]))
        self.assertEqual(response.status_code, 404)

    # Tests opening the Edit Task form correctly for a Task
    def test_edit_GET_valid(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        response = self.client.get(reverse('todolist:edit', args=[task1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/edit.html")

    # Tests submitting an Edit Task form fails when the Task is not found
    def test_edit_POST_missing(self):
        response = self.client.post(
            reverse('todolist:edit', args=[1]),
            {'name': 'Drink soda', 'date_0': 'bad', 'date_1': 'data'}
        )
        self.assertEqual(response.status_code, 404)

    # Tests submitting an Edit Task form with no changes to the task fails and returns errors to the form
    def test_edit_POST_no_changes(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task_count = Task.objects.count()
        response = self.client.post(
            reverse('todolist:edit', args=[task1.id]),
            {'name': 'Eat chips', 'date_0': '2024-05-26', 'date_1': '10:00:00'}
        )
        self.assertTemplateUsed(response, "tasks/edit.html")
        self.assertFormError(
            response.context['form'], None, ['Nothing changed']
        )

    # Tests submitting an Edit Task form fails when data is invalid
    def test_edit_POST_invalid(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        response = self.client.post(
            reverse('todolist:edit', args=[task1.id]),
            {'name': 'Drink soda', 'date_0': 'bad', 'date_1': 'data'}
        )
        self.assertTemplateUsed(response, "tasks/edit.html")
        self.assertFormError(
            response.context['form'], 'date', ['Enter a valid date.', 'Enter a valid time.']
        )

    # Tests submitting an Edit Task form updates the task and redirects to the task list
    def test_edit_POST_valid(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task_count = Task.objects.count()
        response = self.client.post(
            reverse('todolist:edit', args=[task1.id]),
            {'name': 'Drink soda', 'date_0': '2024-05-31', 'date_1': '12:00:00'}
        )
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), task_count)

    # Tests Delete Task doesn't do anything on a GET request
    def test_delete_GET(self):
        response = self.client.get(reverse('todolist:delete', args=[1]))
        self.assertRedirects(response, '/')

    # Tests Delete Task fails when the task is not found
    def test_delete_POST_invalid(self):
        response = self.client.post(reverse('todolist:delete', args=[1]))
        self.assertEqual(response.status_code, 404)

    # Tests Delete Task removes the task and redirects to the task list
    def test_delete_POST_valid(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task_count = Task.objects.count()
        response = self.client.post(reverse('todolist:delete', args=[task1.id]))
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), task_count - 1)

    # Tests Mark Task as Done doesn't do anything on a GET request
    def test_complete_GET(self):
        response = self.client.get(reverse('todolist:complete', args=[1]))
        self.assertRedirects(response, '/')

    # Tests Mark Task as Done fails when the task is not found
    def test_complete_POST_invalid(self):
        response = self.client.post(reverse('todolist:complete', args=[1]))
        self.assertEqual(response.status_code, 404)

    # Tests Mark Task as Done changes the Task to be Complete and redirects to the Task list
    def test_complete_POST_valid(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task2 = create_task('Drink cola', '2024-05-30T12:00:00Z')
        self.assertFalse(Task.objects.get(pk=task1.id).done)
        task_count = Task.objects.count()
        done_count = Task.objects.filter(done=True).count()
        response = self.client.post(reverse('todolist:complete', args=[task1.id]))
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), task_count)
        self.assertEqual(Task.objects.filter(done=True).count(), done_count + 1)
        self.assertTrue(Task.objects.get(pk=task1.id).done)

    # Tests recent weather is fetched for a location
    def test_fetch_weather(self):
        location1 = Location.objects.create(name='Paris', lat=48.864716, lon=2.349014)
        recent_weather_read1 = Weather.objects.create(temperature=26, status='good', location=location1)
        response = self.client.post(reverse('todolist:get_weather', args=[location1.id]))
        self.assertJSONEqual(
            response.content,
            {
                'temp': recent_weather_read1.temperature,
                'weather': recent_weather_read1.status
            }
        )

    # Tests forcing a weather check updates the weather information and provides a newer weather read on the Task list
    def test_weather_refresh(self):
        location1 = Location.objects.create(name='Paris', lat=48.864716, lon=2.349014)
        task1 = Task.objects.create(name='Play basketball', date='2024-05-26T10:00:00Z', location=location1)
        recent_weather_read1 = Weather.objects.create(temperature=26, status='good', location=location1)
        # Note the time of the last weather read for this location
        old_weather_modified_time = recent_weather_read1.modified_at
        # Force refresh
        response = self.client.post(reverse('todolist:force_weather_refresh'))
        # Go to task list
        response = self.client.get(reverse('todolist:index'))
        # Note the time of the current weather read for this location
        new_weather_modified_time = Weather.objects.get(location=location1).modified_at
        # The new weather read should be newer than the previous one
        self.assertGreater(new_weather_modified_time, old_weather_modified_time)

    # Tests Tasks that are complete no longer have their weather reads refreshed
    def test_complete_tasks_dont_refresh_weather_reads(self):
        location1 = Location.objects.create(name='Paris', lat=48.864716, lon=2.349014)
        task1 = Task.objects.create(name='Play basketball', date='2024-05-26T10:00:00Z', location=location1)
        # Note the time of the last weather read for this location
        recent_weather_read1 = Weather.objects.create(temperature=26, status='good', location=location1)
        # Mark as complete
        response = self.client.post(reverse('todolist:complete', args=[task1.id]))
        # Force refresh
        response = self.client.post(reverse('todolist:force_weather_refresh'))
        # Go to task list
        response = self.client.get(reverse('todolist:index'))
        # Fetch the updated task
        task1_updated = Task.objects.get(pk=task1.id)
        # Check that the task list contains the updated task
        self.assertQuerySetEqual(response.context['tasks'], [task1_updated])
        # Check that the updated task has the old weather read regardless of the forced refresh
        self.assertEqual(task1_updated.last_weather_read.temperature, recent_weather_read1.temperature)
        self.assertEqual(task1_updated.last_weather_read.status, recent_weather_read1.status)
