from django.contrib.auth import get_user
from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser


class RegistrationTest(TestCase):

    def setUp(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='CustomUser',
            email='testCustomUser@gmail.com',
            password='testpassword'
        )

    def test_CustomUser_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data={
                'username': "firdavs",
                'first_name': 'Frank',
                'last_name': "Jalolov",
                'email': 'firdavs@gmail.com',
                'password': 'anypassword'
            }
        )
        user = CustomUser.objects.get(username='firdavs')

        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(user.username, 'firdavs')
        self.assertEqual(user.first_name, 'Frank')
        self.assertEqual(user.last_name, 'Jalolov')
        self.assertEqual(user.email, 'firdavs@gmail.com')
        self.assertNotEqual(user.password, 'anypassword')
        self.assertTrue(user.check_password('anypassword'))

    def test_required_fields(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'first_name': 'Frank',
                'last_name': "Jalolov",
                'email': 'invalid-email'
            }
        )

        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_unique_username(self):
        response = self.client.post(reverse('users:register'),
                                    data={
                                        'username': "testuser",
                                        'first_name': 'Frank',
                                        'last_name': "Jalolov",
                                        'email': 'firdavs@gmail.com',
                                        'password': 'anypassword'
                                    })
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create_user(
            username='firdavs',
            password='anypassword'
        )

    def test_successful_login(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'firdavs',
                'password': 'anypassword'
            }
        )
        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        self.client.post(
            reverse('users:login'),
            data={
                'username': 'wrong-username',
                'password': 'wrong-password',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                'username': 'firdavs',
                'password': 'wrong-password',
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username=self.db_user.username, password='anypassword')

        self.client.get(reverse('users:logout'))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):

    def test_redirect_to_login(self):
        response = self.client.get(reverse('users:profile'))

        self.assertEqual(response.url, reverse('users:login') + "?next=/users/profile/")

    def test_user_information_on_login(self):
        user = CustomUser.objects.create_user(
            username='test',
            first_name='Test',
            last_name="User",
            email='test@gmail.com',
            password='anypassword'
        )

        self.client.login(username='test', password='anypassword')
        response = self.client.get(reverse('users:profile'))
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_profile_update(self):
        CustomUser.objects.create_user(
            username='test',
            first_name='Test',
            last_name="CustomUser",
            email='test@gmail.com',
            password='anypassword'
        )
        self.client.login(username='test',password='anypassword')
        user=get_user(self.client)
        response=self.client.post(reverse(
            'users:profile-edit'),
            data={
                "username" : 'testuser',
                "first_name":'Test1',
                'last_name':'User',
                'email':'test1@gmail.com',
                'password':'anypassword',
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.username,'testuser')
        self.assertEqual(user.first_name,'Test1')
        self.assertEqual(user.last_name,'User')
        self.assertEqual(response.status_code,302)
