from django.contrib.auth.models import User
from django.test import TestCase


class HomeTests(TestCase):
    def test_home_requires_login(self):
        r = self.client.get('/')
        self.assertRedirects(r, '/accounts/login/?next=/')

    def test_login_shows_unraid_button(self):
        User.objects.create_user('u', password='pw12345!x')
        r = self.client.post('/accounts/login/', {'username': 'u', 'password': 'pw12345!x'}, follow=True)
        self.assertContains(r, '啟動unraid')
