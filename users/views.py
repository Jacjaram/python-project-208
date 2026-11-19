from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm


class UserListView(ListView):
    """Lista de usuarios. Pública (sin login)."""
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    """Registro de usuario. Redirige al login tras éxito."""
    form_class = UserRegisterForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = 'Usuario registrado exitosamente.'


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """Editar usuario. Solo el propio usuario."""
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Usuario actualizado exitosamente.'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    """Eliminar usuario. Solo el propio usuario."""
    model = User
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Usuario eliminado exitosamente.'

    def test_func(self):
        return self.request.user.pk == self.kwargs['pk']