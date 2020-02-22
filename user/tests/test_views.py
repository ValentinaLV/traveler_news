from django.test import TestCase


class TestViews(TestCase):

    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logout_view(self):
        response = self.client.get('/accounts/logout/')
        self.assertEquals(response.status_code, 302)
