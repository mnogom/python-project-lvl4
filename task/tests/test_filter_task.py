"""Tests."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task.models import Task
from user.models import User


# ?author=&executor=&label=&status=&self_tasks=on
def get_filter_url(**kwargs):
    base_url = reverse_lazy('tasks')
    filter_query = '&'.join(f'{key}={value}' for key, value in kwargs.items())
    return f'{base_url}?{filter_query}'


class FilterTask(TestCase):
    fixtures = ['user/fixtures/users.yaml',
                'status/fixtures/statuses.yaml',
                'label/fixtures/labels.yaml',
                'task/fixtures/tasks.yaml']

    def setUp(self):
        self.client = Client()
        self.author = User.objects.get(pk=1)
        self.client.force_login(self.author)

    def test_filter_by_author(self):
        author_pk = 2
        response = self.client.get(get_filter_url(author=author_pk))
        tasks_from_response = response.context['object_list']
        self.assertQuerysetEqual(tasks_from_response.order_by('pk'),
                                 Task.objects.filter(author_id=author_pk).order_by('pk'))
        self.assertEqual(list(tasks_from_response.values_list('author_id', flat=True)),
                         [author_pk] * tasks_from_response.count())

    def test_filter_by_executor(self):
        executor_pk = 1
        response = self.client.get(get_filter_url(executor=executor_pk))
        tasks_from_response = response.context['object_list']
        self.assertQuerysetEqual(tasks_from_response.order_by('pk'),
                                 Task.objects.filter(executor_id=executor_pk).order_by('pk'))
        self.assertEqual(list(tasks_from_response.values_list('executor_id', flat=True)),
                         [executor_pk] * tasks_from_response.count())

    def test_filter_by_status(self):
        status_pk = 1
        response = self.client.get(get_filter_url(status=status_pk))
        tasks_from_response = response.context['object_list']
        self.assertQuerysetEqual(tasks_from_response.order_by('pk'),
                                 Task.objects.filter(status_id=status_pk).order_by('pk'))
        self.assertEqual(list(tasks_from_response.values_list('status_id', flat=True)),
                         [status_pk] * tasks_from_response.count())

    def test_filter_by_label(self):
        label_pk = 3
        response = self.client.get(get_filter_url(label=label_pk))
        tasks_from_response = response.context['object_list']
        self.assertQuerysetEqual(tasks_from_response.order_by('pk'),
                                 Task.objects.filter(tasklabel__label_id=label_pk).order_by('pk'))
        self.assertEqual(list(tasks_from_response.values_list('labels', flat=True)),
                         [label_pk] * tasks_from_response.count())

    def test_filter_my(self):
        author_pk = self.author.pk
        response = self.client.get(get_filter_url(self_tasks='on'))
        tasks_from_response = response.context['object_list']
        self.assertQuerysetEqual(tasks_from_response.order_by('pk'),
                                 Task.objects.filter(author_id=author_pk).order_by('pk'))
        self.assertEqual(list(tasks_from_response.values_list('author_id', flat=True)),
                         [author_pk] * tasks_from_response.count())

    def test_several_filters(self):
        author_pk = 9
        executor_id = 9
        response = self.client.get(get_filter_url(author=author_pk,
                                                  executor=executor_id))
        tasks_from_response = response.context['object_list']
        self.assertQuerysetEqual(tasks_from_response.order_by('pk'),
                                 Task.objects.filter(author_id=author_pk)
                                 .filter(executor_id=executor_id).order_by('pk'))
        self.assertEqual(list(tasks_from_response.values_list('author_id', flat=True)),
                         [author_pk] * tasks_from_response.count())
        self.assertEqual(list(tasks_from_response.values_list('executor_id', flat=True)),
                         [executor_id] * tasks_from_response.count())
