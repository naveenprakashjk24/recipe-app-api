'''
Test for User api.
'''

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """ Create and return new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """ Test the public feature of the user API"""

    def setup(self):
        self.client = APIClient()

    # def test_create_user_success(self):
    #     """ Test creating a user is successfully"""
    #     payload = {
    #         'email':'test123@gmail.com',
    #         'password':'testpass123',
    #         'name' : 'test name'
    #     }
    #     res = self.client.post(CREATE_USER_URL, payload)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    #     user = get_user_model().objects.create_user(email = payload['email'])
    #     self.assertTrue(user.check_password(payload['password']))
    #     self.assertNotIn('password',res.data)

    # def test_user_with_exists_error(self):
    #     """Test error returned if user with email exists."""
    #     payload = {
    #         'email':'test123@gmail.com',
    #         'password':'testpass123',
    #         'name' : 'test name'
    #     }

    #     create_user(**payload)
    #     res = self.client.post(CREATE_USER_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_password_too_short_error(self):
    #     """ Test an error returned if password less than 5 chars."""
    #     payload = {
    #         'email':'test123@gmail.com',
    #         'password':'testpass123',
    #         'name' : 'test name'
    #     }
    #     res = self.client.post(CREATE_USER_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    #     user_exists = get_user_model().objects.filter(email =  payload['email']).exists()
    #     self.assertFalse(user_exists)

    def test_create_toker_for_user(self):
        """ Test generate token for valid user"""

        user_details = {
            'name': 'Test User',
            'email': 'testuser123@gmail.com',
            'password': 'test123'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credential(self):
        """ Test return error if credentials invalid"""

        create_user(name='Test User', email='testuser123@gmail.com',
                    password='test123')

        payload = {
            'name': 'testuser123@gmail.com',
            'password': 'test'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """ Test return error if credentials invalid"""

        payload = {
            'name': '',
            'password': 'test123'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        '''Test authendications is required for user'''

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserTestcases(TestCase):
    pass