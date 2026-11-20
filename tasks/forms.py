from django import forms
from .models import Status, Task


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': 'Nombre',
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': 'Nombre',
            'description': 'Descripción',
            'status': 'Estado',
            'executor': 'Ejecutor',
            'labels': 'Etiquetas',
        }
