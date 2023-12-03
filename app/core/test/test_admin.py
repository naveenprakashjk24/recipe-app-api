'''
Testing the admin page
'''
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='test123@test.com',
            password='test123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test321@gmail.com',
            password='testpass321',
            name='Test User',
        )

    def test_users_list(self):
        '''Test that users are listed'''
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        ''' Test edit users page'''
        url = reverse('admin:core_user_changelist', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
