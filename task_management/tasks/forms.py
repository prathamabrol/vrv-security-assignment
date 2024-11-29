# tasks/forms.py
from django import forms
from .models import Task

class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['completed', 'comments']
        widgets = {
            'comments': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add comments here...'})
        }
