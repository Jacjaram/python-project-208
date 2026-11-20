from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib import messages
from .models import Status
from .forms import StatusForm


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