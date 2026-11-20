from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    status = models.ForeignKey(Status, on_delete=models.PROTECT, verbose_name='Estado')
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='authored_tasks', verbose_name='Autor'
    )
    executor = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='executed_tasks', verbose_name='Ejecutor'
    )
    labels = models.ManyToManyField(Label, blank=True, verbose_name='Etiquetas')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')

    def __str__(self):
        return self.name