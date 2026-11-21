from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status, Label, Task


# ============ ESTADOS ============

class StatusCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.status = Status.objects.create(name='Nuevo')

    def test_status_list_requires_login(self):
        response = self.client.get(reverse('status_list'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('status_list')}")

    def test_status_create(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('status_create'), {'name': 'En progreso'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='En progreso').exists())

    def test_status_update(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('status_update', args=[self.status.pk]), {'name': 'Terminado'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Terminado')

    def test_status_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('status_delete', args=[self.status.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(name='Nuevo').exists())


# ============ TAREAS ============

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


# ============ ETIQUETAS ============

class LabelCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.label = Label.objects.create(name='Urgente')

    def test_label_create(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('label_create'), {'name': 'Bug'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Label.objects.filter(name='Bug').exists())

    def test_label_update(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('label_update', args=[self.label.pk]), {'name': 'Importante'})
        self.assertEqual(response.status_code, 302)
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Importante')

    def test_label_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('label_delete', args=[self.label.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Label.objects.filter(pk=self.label.pk).exists())

    def test_label_delete_protected(self):
        status = Status.objects.create(name='Nuevo')
        task = Task.objects.create(
            name='Tarea', status=status, author=self.user, executor=self.user
        )
        task.labels.add(self.label)
        self.client.login(username='testuser', password='testpass123')
        self.client.post(reverse('label_delete', args=[self.label.pk]))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())


# ============ FILTROS ============

class TaskFilterTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.status1 = Status.objects.create(name='Nuevo')
        self.status2 = Status.objects.create(name='Terminado')
        self.label1 = Label.objects.create(name='Urgente')
        self.label2 = Label.objects.create(name='Bug')

        self.task1 = Task.objects.create(
            name='Tarea 1', status=self.status1, author=self.user1, executor=self.user1
        )
        self.task1.labels.add(self.label1)

        self.task2 = Task.objects.create(
            name='Tarea 2', status=self.status2, author=self.user2, executor=self.user2
        )
        self.task2.labels.add(self.label2)

    def test_filter_by_status(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('task_list'), {'status': self.status1.pk})
        self.assertContains(response, 'Tarea 1')
        self.assertNotContains(response, 'Tarea 2')

    def test_filter_by_executor(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('task_list'), {'executor': self.user2.pk})
        self.assertContains(response, 'Tarea 2')
        self.assertNotContains(response, 'Tarea 1')

    def test_filter_by_label(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('task_list'), {'label': self.label1.pk})
        self.assertContains(response, 'Tarea 1')
        self.assertNotContains(response, 'Tarea 2')

    def test_filter_self_tasks(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('task_list'), {'self_tasks': 'on'})
        self.assertContains(response, 'Tarea 1')
        self.assertNotContains(response, 'Tarea 2')
