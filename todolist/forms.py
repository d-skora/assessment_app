from django import forms
from .models import Task, Location


# Form for Task
class TaskForm(forms.ModelForm):
    date = forms.SplitDateTimeField(
        widget=forms.SplitDateTimeWidget(date_attrs={'type': 'date'}, time_attrs={'type': 'time'})
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'onChange': 'getWeatherForLocation(this.value)'
            }
        ),
        empty_label="No location",
        required=False,
        blank=True,
    )

    class Meta:
        model = Task
        fields = ['name', 'date', 'location']
