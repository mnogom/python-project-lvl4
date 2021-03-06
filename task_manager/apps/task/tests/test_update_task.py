"""Tests update task."""

from django.test import TestCase, Client
from django.urls import reverse_lazy

from task_manager.tests.utils import (get_form_errors,
                                      get_last_message)

from task_manager.apps.user.models import User
from task_manager.apps.task.models import Task


class UpdateTask(TestCase):
    """Update task case."""

    fixtures = ['task_manager/fixtures/users.yaml',
                'task_manager/fixtures/statuses.yaml',
                'task_manager/fixtures/labels.yaml',
                'task_manager/fixtures/two_tasks.yaml']

    def setUp(self) -> None:
        """Set up method."""

        self.client = Client()
        self.author = User.objects.get(pk=1)
        self.client.force_login(self.author)

        self.task_to_update = Task.objects.filter(author_id=self.author.pk).first()
        self.updated_task = {'name': 'Updated task',
                             'executor': 3,
                             'status': 3}
        self.task_with_another_author = Task.objects.filter(author_id=2).first()
        self.exists_task = {
            'name': self.task_with_another_author.name,
            'executor': 1,
            'status': 1
        }

        self.messages = {
            'success': 'Задача успешно изменена'
        }
        self.fields_errors = {
            'editor_not_author': 'Только автор может изменить задачу',
            'task_name_not_unique': 'name:Задача с таким названием уже существует',
            'executor_required': 'executor:Обязательное поле.',
        }

    def test_update_task(self) -> None:
        """Test update task."""

        response = self.client.post(reverse_lazy('task:update',
                                                 kwargs={'pk': self.task_to_update.pk}),
                                    data=self.updated_task,
                                    follow=True)
        self.assertEqual(get_last_message(response),
                         self.messages['success'])
        self.assertNotEqual(
            [self.updated_task.get('name', ''),
             self.updated_task.get('description', ''),
             self.updated_task.get('status', ''),
             self.author.pk,
             self.updated_task.get('executor', ''),
             self.updated_task.get('labels', [])],
            [self.task_to_update.name,
             self.task_to_update.description,
             self.task_to_update.status.pk,
             self.task_to_update.author.pk,
             self.task_to_update.executor.pk,
             list(
                 self.task_to_update.labels.values_list('pk', flat=True))])

    def test_update_task_of_another_user(self) -> None:
        """Test update task where user not author."""

        response = self.client.post(reverse_lazy('task:update',
                                                 kwargs={'pk': self.task_with_another_author.pk}),
                                    data=self.updated_task,
                                    follow=True)
        self.assertIn(self.fields_errors['editor_not_author'],
                      get_last_message(response))

    def test_update_task_if_not_unique(self) -> None:
        """Test update task with not unique fields."""

        response = self.client.post(reverse_lazy('task:update',
                                                 kwargs={'pk': self.task_to_update.pk}),
                                    data=self.exists_task,
                                    follow=True)
        self.assertIn(self.fields_errors['task_name_not_unique'],
                      get_form_errors(response))

    def test_update_if_task_not_full(self) -> None:
        """Test update task without required fields."""

        updated_task = self.updated_task.copy()
        updated_task.pop('executor')
        response = self.client.post(reverse_lazy('task:update',
                                                 kwargs={'pk': self.task_to_update.pk}),
                                    data=updated_task,
                                    follow=True)
        self.assertIn(self.fields_errors['executor_required'],
                      get_form_errors(response))
