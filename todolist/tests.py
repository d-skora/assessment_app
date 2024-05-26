from django.test import TestCase
from .models import Task


def create_task(name, date):
    return Task.objects.create(name=name, date=date)


class TaskModelTest(TestCase):

    def test_string_representation(self):
        task = Task(name="Eat chips")
        self.assertEqual(str(task), task.name)


class ProjectTests(TestCase):

    def test_homepage(self):
        task1 = create_task('Eat chips', '2024-05-26T10:00:00Z')
        task2 = create_task('Drink cola', '2024-05-30T12:00:00Z')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['tasks'], [task1, task2])
