import datetime

from django.core import mail
from django.test import TestCase

from user.models import CustomUser


class CustomerUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = CustomUser.objects.create_user(email='test_user@test.com',
                                                       username='test_user',
                                                       password='12345',
                                                       first_name='Valentyna',
                                                       last_name='Lysenok',
                                                       date_of_birth=datetime.date(1992, 7, 14))

    def test_email_label(self):
        field_label = self.test_user._meta.get_field('email').verbose_name
        self.assertEquals(field_label, 'email address')

    def test_username_label(self):
        field_label = self.test_user._meta.get_field('username').verbose_name
        self.assertEquals(field_label, 'username')

    def test_first_name_label(self):
        field_label = self.test_user._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_last_name_label(self):
        field_label = self.test_user._meta.get_field('last_name').verbose_name
        self.assertEquals(field_label, 'last name')

    def test_date_of_birth_label(self):
        field_label = self.test_user._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'date of birth')

    def test_object_name(self):
        expected_object_name = self.test_user.username
        self.assertEquals(expected_object_name, str(self.test_user))

    def test_email_data(self):
        self.assertEquals(self.test_user.email, 'test_user@test.com')

    def test_username_data(self):
        self.assertEquals(self.test_user.username, 'test_user')

    def test_first_name_data(self):
        self.assertEquals(self.test_user.first_name, 'Valentyna')

    def test_last_name_data(self):
        self.assertEquals(self.test_user.last_name, 'Lysenok')

    def test_date_of_birth_data(self):
        self.assertEquals(self.test_user.date_of_birth, datetime.date(1992, 7, 14))

    def test_send_link_confirm_email_new_user(self):
        message = f'Hi {self.test_user.username}\n' \
                  f'http://{self.test_user.id}'
        mail.send_mail('Activate Your Account', message, 'traveller@gmail.com', [self.test_user.email],
                       fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate Your Account')
