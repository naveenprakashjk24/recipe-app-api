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

    def test_email_normalized_create_user(self):
        ''' checking the email normalized'''

        sample_email = [['test123@GMAIL.com', 'test123@gmail.com'],
                        ['TEST321@GMAIL.COM', 'TEST321@gmail.com']]
        for email, excepted in sample_email:
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, excepted)

    def test_new_user_without_email_validation(self):
        ''' validating the empty user'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        '''create super user.'''
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)