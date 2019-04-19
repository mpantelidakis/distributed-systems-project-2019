from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    # function that runs before all tests
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # use reverse instead of hardcoding the url so it auto-updates
        url = reverse('admin:core_user_changelist')
        # perform an http request at the target url
        res = self.client.get(url)

        # checks the http response object and its content
        # also checks that http response is 200
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # eg. /admin/core/user/args
        res = self.client.get(url)

        # Check the Http response code is 200
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
