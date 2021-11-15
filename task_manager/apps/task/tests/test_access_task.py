"""Tests access labels."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.apps.user.views import LoginUserView
from task_manager.apps.task.models import Task

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_last_message)


class TaskAccessCase(TestCase):
    """Task access case."""

    fixtures = ['task_manager/fixtures/users.yaml',
                'task_manager/fixtures/statuses.yaml',
                'task_manager/fixtures/labels.yaml',
                'task_manager/fixtures/tasks.yaml']

    def setUp(self) -> None:
        """Set up method"""

        self.user = {'username': 'User',
                     'password': 'Password'}
        self.client = Client()
        create_user(client=self.client,
                    user=self.user)
        self.messages = {
            'login_required': 'Вам необходимо войти для этого действия'
        }

    def test_not_login_access(self) -> None:
        """Test access without user login."""

        response = self.client.get(reverse_lazy('task:list'),
                                   follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['login_required'])
        self.assertEqual(response.resolver_match.func.__name__,
                         LoginUserView.as_view().__name__)

    def test_login_access(self) -> None:
        """Test access with user login."""

        login_user(client=self.client,
                   **self.user)
        response = self.client.get(reverse_lazy('task:list'),
                                   follow=True)
        self.assertQuerysetEqual(response.context['object_list'].order_by('pk'),
                                 Task.objects.all().order_by('pk'))
