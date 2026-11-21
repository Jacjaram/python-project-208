import django_filters
from django import forms
from django.contrib.auth.models import User
from .models import Task, Status, Label


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(
        field_name='status',
        queryset=Status.objects.all(),
        label='Estado',
        empty_label='Todos los estados',
    )
    executor = django_filters.ModelChoiceFilter(
        field_name='executor',
        queryset=User.objects.all(),
        label='Ejecutor',
        empty_label='Todos los ejecutores',
    )
    label = django_filters.ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
        label='Etiqueta',
        empty_label='Todas las etiquetas',
    )
    self_tasks = django_filters.BooleanFilter(
        field_name='author',
        method='filter_self_tasks',
        label='Solo mis tareas',
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']

    def filter_self_tasks(self, queryset, name, value):
        if value and self.request and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset