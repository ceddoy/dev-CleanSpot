from http import HTTPStatus

from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from authapp.models import CleanspotUser, CleanspotUserType


class TestProfileappSmoke(TestCase):

    def setUp(self) -> None:
        call_command('flush', '--noinput')
        call_command('loaddata', 'db.json')
        self.client = Client()
        self.superuser = CleanspotUser.objects.create_superuser(
            email='mail_ad@mail.com',
            password='123',
            user_type=CleanspotUserType.objects.get(name='Moderator'),
        )
        self.user = CleanspotUser.objects.create_user(
            email='mail_ad1@mail.com',
            password='123123123qw',
            user_type=CleanspotUserType.objects.get(name='Юридические лица'),
        )

    def test_user_moderator_urls(self):

        self.client.login(email='mail_ad@mail.com', password='123')
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.superuser)

        response = self.client.get(f'/edit/{self.superuser.email}/lk_admin_cleaner_add/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.get(f'/edit/{self.superuser.email}/lk_admin_cleaner_list/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.get(f'/edit/{self.superuser.email}/lk_admin_history/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.get(f'/edit/{self.superuser.email}/lk_admin_users_list/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        for user in CleanspotUser.objects.filter(user_type__name='Cleaner'):
            response = self.client.get(f'/edit/{self.superuser.email}/lk_admin_cleaner_edit/{user.pk}/')
            self.assertEqual(response.status_code, HTTPStatus.OK)

        for user in CleanspotUser.objects.all().exclude(user_type__name='Moderator').exclude(user_type__name='Cleaner'):
            response = self.client.get(f'/edit/{self.superuser.email}/lk_admin_users_edit/{user.pk}/')
            self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_urls(self):
        self.client.login(email='mail_ad1@mail.com', password='123123123qw')
        response = self.client.get(f'/edit/{self.user.email}/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)
        edit_data = {
            'title': 'AndyPanda777',
            'phone_number': '89118887766',
            'email': 'mail_ad1@mail.com'
        }
        response = self.client.post(f'/edit/{self.user.email}/', edit_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        response = self.client.get(f'/edit/{self.user.email}/change_password/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

        change_pass_data = {
            'old_password': '123123123qw',
            'new_password1': '123123123qwe',
            'new_password2': '123123123qwe'
        }

        response = self.client.post(f'/edit/{self.user.email}/change_password/', change_pass_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        response = self.client.get('/auth/logout/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        response = self.client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'orderapp')
