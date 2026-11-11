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


class StartUnraidTests(TestCase):
    def test_requires_login(self):
        self.assertEqual(self.client.post('/start-unraid/').status_code, 302)

    def test_get_not_allowed(self):
        User.objects.create_user('u', password='pw12345!x')
        self.client.login(username='u', password='pw12345!x')
        self.assertEqual(self.client.get('/start-unraid/').status_code, 405)

    def test_runs_script(self):
        import tempfile, os
        from django.test import override_settings
        User.objects.create_user('u', password='pw12345!x')
        self.client.login(username='u', password='pw12345!x')
        with tempfile.NamedTemporaryFile('w', suffix='.sh', delete=False) as f:
            f.write('echo hello-unraid\n')
        try:
            with override_settings(UNRAID_SCRIPT=f.name):
                r = self.client.post('/start-unraid/')
            self.assertTrue(r.json()['ok'])
            self.assertIn('hello-unraid', r.json()['output'])
        finally:
            os.unlink(f.name)
