from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserCRUDTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123',
            first_name='Test', last_name='User'
        )

    def test_user_registration(self):
        response = self.client.post(reverse('user_create'), {
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'username': 'nuevo',
            'password1': 'claveSegura123',
            'password2': 'claveSegura123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='nuevo').exists())

    def test_user_update(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('user_update', args=[self.user.pk]), {
            'first_name': 'Editado',
            'last_name': 'Usuario',
            'username': 'testuser',
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Editado')

    def test_user_delete(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('user_delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='testuser').exists())