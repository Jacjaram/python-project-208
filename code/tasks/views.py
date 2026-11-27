from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib import messages
from django_filters.views import FilterView
from .models import Status, Label, Task
from .forms import StatusForm, LabelForm, TaskForm
from .filters import TaskFilter


# ============ ESTADOS ============

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'tasks/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'tasks/status_create.html'
    success_url = reverse_lazy('status_list')
    success_message = 'Estado creado exitosamente.'


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'tasks/status_update.html'
    success_url = reverse_lazy('status_list')
    success_message = 'Estado actualizado exitosamente.'


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'tasks/status_delete.html'
    success_url = reverse_lazy('status_list')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Estado eliminado exitosamente.')
            return response
        except ProtectedError:
            messages.error(self.request, 'No se puede eliminar el estado porque está en uso.')
            return redirect('status_list')


# ============ TAREAS ============

class TaskListView(LoginRequiredMixin, FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('task_list')
    success_message = 'Tarea creada con éxito.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('task_list')
    success_message = 'Tarea actualizada con éxito.'


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        return self.get_object().author == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Tarea eliminada con éxito.')
        return super().form_valid(form)


# ============ ETIQUETAS ============

class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'tasks/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'tasks/label_create.html'
    success_url = reverse_lazy('label_list')
    success_message = 'Etiqueta creada exitosamente.'


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'tasks/label_update.html'
    success_url = reverse_lazy('label_list')
    success_message = 'Etiqueta actualizada exitosamente.'


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'tasks/label_delete.html'
    success_url = reverse_lazy('label_list')

    def form_valid(self, form):
        label = self.get_object()
        if label.task_set.exists():  # o label.tasks.exists() según el related_name
            messages.error(self.request, 'No se puede eliminar la etiqueta porque está en uso.')
            return redirect('label_list')
        response = super().form_valid(form)
        messages.success(self.request, 'Etiqueta eliminada exitosamente.')
        return response