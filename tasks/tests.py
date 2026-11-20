from .models import Status, Label, Task


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
        response = self.client.post(reverse('label_delete', args=[self.label.pk]))
        self.assertTrue(Label.objects.filter(pk=self.label.pk).exists())