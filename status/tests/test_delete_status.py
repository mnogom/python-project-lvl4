"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_last_message)

from status.models import Status
from task.models import Task
from user.models import User


class DeleteStatus(TestCase):
    def setUp(self):
        user = {'username': 'User',
                'password': 'qwerty'}
        create_user(client=self.client,
                    user=user,
                    follow=False)
        login_user(client=self.client,
                   **user,
                   follow=False)
        self.messages = {
            'success': 'Статус успешно удалён',
        }
        self.client.post(reverse_lazy('create_status'),
                         data={'name': 'Name'})

    def test_delete_status(self):
        response = self.client.post(reverse_lazy('delete_status',
                                                 kwargs={'pk': 1}),
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['success'])
        self.assertEqual(Status.objects.count(), 0)


class DeleteProtectedStatus(TestCase):
    fixtures = ['user/fixtures/users.yaml',
                'status/fixtures/statuses.yaml',
                'label/fixtures/labels.yaml',
                'task/fixtures/tasks.yaml']

    def setUp(self):
        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.status_pk = 1
        self.status = Status.objects.get(pk=self.status_pk)
        self.messages = {
            'protected_element': 'Статус используется. Вы не можете её удалить.'
        }

    def test_delete_protected_status(self):
        if Task.objects.filter(status_id=self.status_pk).count() == 0:
            raise IndexError(f'Status with pk {self.status_pk} has not protection. '
                             f'Switch to pk to another.')
        response = self.client.post(reverse_lazy('delete_status',
                                                 kwargs={'pk': self.status_pk}),
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['protected_element'])
