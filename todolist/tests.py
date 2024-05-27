from django.test import TestCase

from .forms import TaskForm
from .models import Task
from django.urls import reverse


def create_task(name, date):
    return Task.objects.create(name=name, date=date)


class TaskModelTest(TestCase):

    def test_string_representation(self):
        task = Task(name="Eat chips")
        self.assertEqual(str(task), task.name)


class TaskFormTest(TestCase):
    # Valid Form Data
    def test_TaskForm_valid(self):
        form = TaskForm({'name': 'Eat crisps', 'date_0': '2024-05-26', 'date_1': '10:00:00'})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_TaskForm_invalid(self):
        form = TaskForm({'name': "", 'date': "bad text"})
        self.assertFalse(form.is_valid())


class ProjectTests(TestCase):

    def test_index(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task2 = create_task('Drink cola', '2024-05-30T12:00:00Z')
        response = self.client.get(reverse('todolist:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['tasks'], [task1, task2])

    def test_add_GET(self):
        response = self.client.get(reverse('todolist:add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/add.html")

    def test_add_POST_invalid(self):
        response = self.client.post(
            reverse('todolist:add'),
            {'name': 'Drink soda', 'date_0': 'bad', 'date_1': 'data'}
        )
        self.assertTemplateUsed(response, "tasks/add.html")
        self.assertFormError(
            response.context['form'], 'date', ['Enter a valid date.', 'Enter a valid time.']
        )

    def test_add_POST_valid(self):
        task_count = Task.objects.count()
        response = self.client.post(
            reverse('todolist:add'),
            {'name': 'Drink soda', 'date_0': '2024-05-31', 'date_1': '12:00:00'}
        )
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), task_count + 1)

    def test_clear(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task2 = create_task('Drink cola', '2024-05-30T12:00:00Z')
        self.assertEqual(Task.objects.count(), 2)
        response = self.client.post(reverse('todolist:clear'))
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), 0)

    def test_edit_GET_invalid(self):
        response = self.client.get(reverse('todolist:edit', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_edit_GET_valid(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        response = self.client.get(reverse('todolist:edit', args=[task1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tasks/edit.html")

    def test_edit_POST_missing(self):
        response = self.client.post(
            reverse('todolist:edit', args=[1]),
            {'name': 'Drink soda', 'date_0': 'bad', 'date_1': 'data'}
        )
        self.assertEqual(response.status_code, 404)

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

    def test_edit_POST_valid(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task_count = Task.objects.count()
        response = self.client.post(
            reverse('todolist:edit', args=[task1.id]),
            {'name': 'Drink soda', 'date_0': '2024-05-31', 'date_1': '12:00:00'}
        )
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), task_count)

    def test_delete_GET(self):
        response = self.client.get(reverse('todolist:delete', args=[1]))
        self.assertRedirects(response, '/')

    def test_delete_POST_invalid(self):
        response = self.client.post(reverse('todolist:delete', args=[1]))
        self.assertEqual(response.status_code, 404)

    def test_delete_POST_valid(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task_count = Task.objects.count()
        response = self.client.post(reverse('todolist:delete', args=[task1.id]))
        self.assertRedirects(response, '/')
        self.assertEqual(Task.objects.count(), task_count - 1)
