'''
Test for models
'''

from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    ''' Test models.'''

    def test_create_user_with_email_successful(self):
        ''' Creating user with email successful'''

        email = 'test@test.in'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
