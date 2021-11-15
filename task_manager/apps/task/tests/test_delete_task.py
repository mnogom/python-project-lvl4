"""Tests delete task."""

from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.db.models import Q

from task_manager.tests.utils import get_last_message

from task_manager.apps.task.models import Task
from task_manager.apps.status.models import Status
from task_manager.apps.label.models import Label
from task_manager.apps.user.models import User


class DeleteTask(TestCase):
    """Task delete case."""

    fixtures = ['task_manager/fixtures/users.yaml',
                'task_manager/fixtures/statuses.yaml',
                'task_manager/fixtures/labels.yaml',
                'task_manager/fixtures/two_tasks.yaml']

    def setUp(self) -> None:
        """Set up method"""

        self.client = Client()
        author = User.objects.get(pk=1)
        self.client.force_login(author)

        self.author_task = Task.objects.get(author_id=author.pk)
        self.another_author_task = Task.objects.get(~Q(author_id=author.pk))

        self.messages = {
            'success': 'Задача успешно удалена',
            'access_denied': 'Только автор может изменить задачу',
        }

    def test_delete_task(self) -> None:
        """Test delete task."""

        obj_counts_before = {'labels': Label.objects.count(),
                             'statuses': Status.objects.count(),
                             'users': User.objects.count()}
        response = self.client.post(reverse_lazy('task:delete',
                                                 kwargs={'pk': self.author_task.pk}),
                                    follow=True)
        obj_counts_after = {'labels': Label.objects.count(),
                            'statuses': Status.objects.count(),
                            'users': User.objects.count()}

        self.assertEqual(get_last_message(response),
                         self.messages['success'])
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(obj_counts_before,
                         obj_counts_after)

    def test_delete_task_of_another_user(self) -> None:
        """Test delete task where user not author."""

        response = self.client.post(reverse_lazy('task:delete',
                                                 kwargs={'pk': self.another_author_task.pk}),
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['access_denied'])
