"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.db.models import Q

from task_manager.tests.utils import get_last_message

from task.models import Task
from status.models import Status
from label.models import Label
from user.models import User


class DeleteTask(TestCase):
    fixtures = ['user/fixtures/users.yaml',
                'status/fixtures/statuses.yaml',
                'label/fixtures/labels.yaml',
                'task/fixtures/two_tasks.yaml']

    def setUp(self):
        self.client = Client()
        author = User.objects.get(pk=1)
        self.client.force_login(author)

        self.author_task = Task.objects.get(author_id=author.pk)
        self.another_author_task = Task.objects.get(~Q(author_id=author.pk))

        self.messages = {
            'success': 'Задача успешно удалена',
            'access_denied': 'Только автор может изменить задачу',
        }

    def test_delete_task(self):
        obj_counts_before = {'labels': Label.objects.count(),
                             'statuses': Status.objects.count(),
                             'users': User.objects.count()}
        response = self.client.post(reverse_lazy('delete_task',
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


    def test_delete_task_of_another_user(self):
        response = self.client.post(reverse_lazy('delete_task',
                                                 kwargs={'pk': self.another_author_task.pk}),
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['access_denied'])
