"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_last_message)
from user.models import User


class DeleteUser(TestCase):
    def setUp(self):
        self.client = Client()
        user = {'username': 'User',
                'password': 'qwerty'}
        create_user(client=self.client,
                    user=user,
                    follow=False)
        login_user(client=self.client,
                   **user,
                   follow=False)
        self.messages = {
            'success': 'Пользователь успешно удалён',
            'access_denied': 'У Вас нет прав удалять пользователей'
        }

    def test_delete_user(self):
        response = self.client.post(reverse_lazy('delete_user',
                                                 kwargs={'pk': 1}),
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['success'])
        self.assertEqual(User.objects.count(), 0)

    def test_delete_another_user(self):
        user_2 = {'username': 'User_2',
                  'password': 'asdfgh'}
        create_user(client=self.client,
                    user=user_2,
                    follow=False)
        response = self.client.post(reverse_lazy('delete_user',
                                                 kwargs={'pk': 2}),
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['access_denied'])
        self.assertEqual(User.objects.count(), 2)


class DeleteProtectedUser(TestCase):
    fixtures = ['user/fixtures/users.yaml',
                'status/fixtures/statuses.yaml',
                'label/fixtures/labels.yaml',
                'task/fixtures/tasks.yaml']

    def setUp(self):
        self.client = Client()
        self.user_pk = 1
        self.user = User.objects.get(pk=self.user_pk)
        self.client.force_login(self.user)
        self.messages = {
            'protected_element': 'Пользователь используется. Вы не можете его удалить.'
        }

    def test_delete_protected_user(self):
        if self.user.author.count() == 0 and self.user.executor.count() == 0:
            raise IndexError(f'User with pk {self.user_pk} has not protection. '
                             f'Switch to pk to another.')
        response = self.client.post(reverse_lazy('delete_user',
                                                 kwargs={'pk': self.user_pk}),
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['protected_element'])
