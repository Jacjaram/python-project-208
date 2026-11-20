from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status, Label, Task


class TaskCRUDTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.status = Status.objects.create(name='Nuevo')
        self.label = Label.objects.create(name='Urgente')
        self.task = Task.objects.create(
            name='Tarea 1', description='Descripción', status=self.status,
            author=self.user1, executor=self.user2
        )
        self.task.labels.add(self.label)

    def test_task_create(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('task_create'), {
            'name': 'Nueva tarea',
            'description': 'Desc',
            'status': self.status.pk,
            'executor': self.user2.pk,
            'labels': [self.label.pk],
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(name='Nueva tarea').exists())
        nueva = Task.objects.get(name='Nueva tarea')
        self.assertEqual(nueva.author, self.user1)

    def test_task_update(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('task_update', args=[self.task.pk]), {
            'name': 'Tarea editada',
            'description': 'Nueva desc',
            'status': self.status.pk,
            'executor': self.user2.pk,
            'labels': [self.label.pk],
        })
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Tarea editada')

    def test_task_delete_by_author(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_by_other_user_forbidden(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.post(reverse('task_delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Task.objects.filter(pk=self.task.pk).exists())