"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_form_errors,
                                      get_last_message)
from user.models import User

class EditUser(TestCase):
    def setUp(self):
        self.client = Client()
        self.users = [{'username': 'Ana',
                       'password': 'PasswordForAna'},
                      {'username': 'Pharah',
                       'password': 'PasswordForPharah'}]
        self.updated_user = {'username': 'Zarya',
                             'password1': 'PasswordForZarya',
                             'password2': 'PasswordForZarya'}
        for user in self.users:
            create_user(client=self.client,
                        user=user,
                        follow=False)
        login_user(client=self.client,
                   **self.users[0],
                   follow=False)

        self.messages = {
            'success': 'Пользователь успешно изменён',
            'access_denied': 'У Вас нет прав изменять пользователей'
        }
        self.fields_errors = {
            'username_not_unique': 'username:Пользователь с таким именем уже существует.',
            'username_required': 'username:Обязательное поле.',
            'password1_required': 'password1:Обязательное поле.',
            'password_doesnt_math': 'password2:Пароли не совпадают',
        }

    def test_edit_user(self):
        response = self.client.post(reverse_lazy('update_user',
                                                 kwargs={'pk': 1}),
                                    data=self.updated_user,
                                    follow=True)
        updated_user_from_db = User.objects.get(pk=1)
        self.assertEqual(get_last_message(response),
                         self.messages['success'])
        self.assertEqual(
            [
                self.updated_user.get('username', ''),
                self.updated_user.get('first_name', ''),
                self.updated_user.get('last_name', ''),
                self.updated_user.get('email', '')
            ],
            [
                updated_user_from_db.username,
                updated_user_from_db.first_name,
                updated_user_from_db.last_name,
                updated_user_from_db.email
            ]
        )

    def test_edit_another_user(self):
        response = self.client.post(reverse_lazy('update_user',
                                                 kwargs={'pk': 2}),
                                    data=self.updated_user,
                                    follow=True)
        updated_user_from_db = User.objects.get(pk=2)
        self.assertEqual(
            [
                self.users[1].get('username', ''),
                self.users[1].get('first_name', ''),
                self.users[1].get('last_name', ''),
                self.users[1].get('email', '')
            ],
            [
                updated_user_from_db.username,
                updated_user_from_db.first_name,
                updated_user_from_db.last_name,
                updated_user_from_db.email
            ]
        )
        self.assertEqual(get_last_message(response),
                         self.messages['access_denied'])

    def test_edit_user_to_not_unique(self):
        updated_user = {'username': 'Pharah',
                       'password1': '123',
                       'password2': '123'}
        response = self.client.post(reverse_lazy('update_user',
                                                 kwargs={'pk': 1}),
                                    data=updated_user)
        updated_user_from_db = User.objects.get(pk=1)
        self.assertEqual(
            [
                self.users[0].get('username', ''),
                self.users[0].get('first_name', ''),
                self.users[0].get('last_name', ''),
                self.users[0].get('email', '')
            ],
            [
                updated_user_from_db.username,
                updated_user_from_db.first_name,
                updated_user_from_db.last_name,
                updated_user_from_db.email
            ]
        )
        self.assertIn(self.fields_errors['username_not_unique'],
                      get_form_errors(response))

    def test_edit_user_data_not_full_for_update(self):
        updated_user = {'password1': '123',
                       'password2': '123'}
        response = self.client.post(reverse_lazy('update_user',
                                                 kwargs={'pk': 1}),
                                    data=updated_user)
        self.assertIn(self.fields_errors['username_required'],
                      get_form_errors(response))

        updated_user = {'username': 'Zarya',
                       'password2': '123'}
        response = self.client.post(reverse_lazy('update_user',
                                                 kwargs={'pk': 1}),
                                    data=updated_user)
        self.assertIn(self.fields_errors['password1_required'],
                      get_form_errors(response))

    def test_if_passwords_doesnt_match(self):
        updated_user = {'username': 'Zarya',
                        'password1': '123',
                        'password2': '321'}
        response = self.client.post(reverse_lazy('update_user',
                                                 kwargs={'pk': 1}),
                                    data=updated_user)
        self.assertIn(self.fields_errors['password_doesnt_math'],
                      get_form_errors(response))