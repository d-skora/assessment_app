from django.db import models


# Model for todolist item
class Task(models.Model):
    name = models.CharField(max_length=500)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.name
