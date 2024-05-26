from django import forms
from .models import Task


# Form for Task
class TaskForm(forms.ModelForm):
    date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'}, time_attrs={'type': 'time'})
    )

    class Meta:
        model = Task
        fields = ['name', 'date']
