from django.db import models
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Fecha de creación')

    def __str__(self):
        return self.name