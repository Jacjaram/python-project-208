from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Status


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