"""Tests delete label."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (create_user,
                                      login_user,
                                      get_last_message)

from task_manager.apps.label.models import Label
from task_manager.apps.user.models import User


class DeleteLabel(TestCase):
    """Label delete case."""

    def setUp(self) -> None:
        """Set up method."""

        user = {'username': 'User',
                'password': 'qwerty'}
        create_user(client=self.client,
                    user=user,
                    follow=False)
        login_user(client=self.client,
                   **user,
                   follow=False)
        self.messages = {
            'success': 'Метка успешно удалена',
        }
        self.client.post(reverse_lazy('label:create'),
                         data={'name': 'Name'})

    def test_delete_label(self) -> None:
        """Test delete label."""

        response = self.client.post(reverse_lazy('label:delete',
                                                 kwargs={'pk': 1}),
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['success'])
        self.assertEqual(Label.objects.count(), 0)


class DeleteProtectedLabel(TestCase):
    """Delete protected label case."""

    fixtures = ['task_manager/fixtures/users.yaml',
                'task_manager/fixtures/statuses.yaml',
                'task_manager/fixtures/labels.yaml',
                'task_manager/fixtures/tasks.yaml']

    def setUp(self) -> None:
        """Set up method."""

        self.client = Client()
        self.user = User.objects.get(pk=1)
        self.client.force_login(self.user)
        self.label_pk = 1
        self.label = Label.objects.get(pk=self.label_pk)
        self.messages = {
            'protected_element': 'Метка используется. Вы не можете её удалить.'
        }

    def test_delete_protected_label(self) -> None:
        """Test delete protected label."""

        if self.label.task_set.count() == 0:
            raise IndexError(f'Label with pk {self.label_pk} has not protection. '
                             f'Switch to pk to another.')
        response = self.client.post(reverse_lazy('label:delete',
                                                 kwargs={'pk': self.label_pk}),
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['protected_element'])
