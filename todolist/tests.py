from django.test import TestCase
from .models import Task


class TaskModelTest(TestCase):

    def test_string_representation(self):
        task = Task(name="Eat chips")
        self.assertEqual(str(task), task.name)
